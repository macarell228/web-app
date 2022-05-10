import logging
import datetime
import json

from pymorphy2 import MorphAnalyzer

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask import render_template, redirect, request, abort, make_response, jsonify

from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import Api

from config import Config

from data import db_session
from data.users import User
from data.news import News
from data.teachers import Teacher
from data.prof_devops import ProfessionalDevelopment
from api import news_resources

from forms.user import init_register_form, init_optional_register_form, LoginForm
from forms.news import init_news_form


async def upd():
    db_sess = db_session.create_session()
    date = datetime.datetime.now()
    delta = datetime.timedelta(days=(app.config["CLEAN_TIME_YEARS"] * 365))
    before = date - delta
    table = app.config["TABLE_CLEAN"]
    await db_sess.execute("DELETE FROM ? WHERE date<?", (table, before))

    logging.warning(f"Очищена таблица {table} с записями, выпущенными до {before}")


def update_lists():
    db_sess = db_session.create_session()
    app.config["ROLES"] = [item[0] for item in db_sess.execute("""SELECT status FROM statuses""").fetchall()]
    app.config["ROLES_REVERSE"] = {item[0]: item[1] for item in
                                   db_sess.execute("""SELECT id, status FROM statuses""").fetchall()}
    app.config["CLASSES"] = [' '.join(map(str, item)) for item in
                             db_sess.execute("""SELECT class_number, class_letter FROM classes""").fetchall()]
    app.config["SUBJECTS"] = {item[1]: item[0] for item in
                              db_sess.execute("""SELECT id, subject FROM subjects""").fetchall()}

    logging.warning(f"Обновлены переменные конфигурации.")


app: Flask = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)

morph = MorphAnalyzer(lang='ru')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Декоратор делает так, чтобы функции внутри можно было использовать с движком Jinja2, который использует  Flask
@app.context_processor
def utility_processor():
    def make_readable_status(status_id):
        return app.config["ROLES_REVERSE"][status_id]

    return dict(make_readable_status=make_readable_status)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/news/<int:news_id>')
def news_view(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == news_id).first()
    return render_template("view.html", title=app.config["TITLES"]['news'], pages=app.config["PAGES"], news=news)


@app.route('/teachers/<int:teacher_id>')
def teacher(teacher_id):
    db_sess = db_session.create_session()
    teacher_object = db_sess.query(Teacher).filter(Teacher.account_id == teacher_id).first()
    subjects = list(map(lambda x: x[0],
                        db_sess.execute(
                            f"""SELECT subject FROM subjects WHERE id IN ({teacher_object.subjects_ids})""").fetchall()))
    prepare = db_sess.query(ProfessionalDevelopment).filter(ProfessionalDevelopment.account_id == teacher_id).all()
    return render_template("teacher_page.html", title=app.config["TITLES"]['teachers'], pages=app.config["PAGES"],
                           teacher=teacher_object, subjects=subjects, prepare=prepare)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register/<account_id>/<filename>', methods=['GET', 'POST'])
def _back_func(account_id, filename):
    form = init_optional_register_form(_classes=app.config["CLASSES"], _choices=app.config["SUBJECTS"].keys(),
                                       state=(filename == app.config["REDIR"]["ученик"]))
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if filename == app.config["REDIR"]["ученик"]:
            tmp = form.education_class.data
            class_number, class_letter = int(tmp[:-1]), tmp[-1]
            class_id = db_sess.execute(f"""
                SELECT id FROM classes 
                WHERE class_number={class_number} AND class_letter='{class_letter}'""").fetchone()[0]
            db_sess.execute(f"""INSERT INTO students(account_id, class_id) VALUES({account_id}, {class_id})""")
        else:
            if not form.subjects.data:
                return render_template(filename, title=app.config["TITLES"]['register'],
                                       pages=app.config["PAGES"], form=form, account_id=account_id,
                                       filename=filename, message="Выберите предмет, который вы преподаете.")

            quality = db_sess.execute("""SELECT COUNT(*) FROM professional_development""").fetchone()[0]
            q_elems = 0
            for data in form.prof_devop_list.data:
                date = data['date'].__str__()
                description = data['description']
                during = data['during'].__str__()
                if date and description and during:
                    db_sess.execute(f"""
                        INSERT INTO 
                            professional_development (account_id, date, description, during) 
                        VALUES ({account_id}, "{date}", "{description}", {during})""")
                    db_sess.commit()
                    q_elems += 1
            prof_devop_ids = ', '.join(list(map(str, range(quality, quality + q_elems))))
            subject_ids = ', '.join([str(app.config["SUBJECTS"][item]) for item in form.subjects.data])
            db_sess.execute(f"""
                INSERT INTO 
                    teachers (account_id, subjects_ids, academics, dir_of_preparation, prof_devop_ids, work_exp) 
                VALUES ({account_id}, "{subject_ids}", "{form.academics.data}", "{form.dir_of_preparation.data}", 
                "{prof_devop_ids}", {form.work_exp.data})""")

        db_sess.commit()
        return redirect('/login')
    return render_template(filename, title=app.config["TITLES"]['register'],
                           pages=app.config["PAGES"], form=form, account_id=account_id, filename=filename)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = init_register_form([item for item in app.config["ROLES"] if item != 'гость'])
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            patronymic=form.patronymic.data,
            email=form.email.data,
            status_id=db_sess.execute(f'''SELECT id FROM statuses WHERE status="{form.status.data}"''').fetchone()[0]
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        acc_id = db_sess.execute(f"""SELECT id FROM accounts WHERE email='{user.email}'""").fetchone()[0]
        if form.status.data in app.config["REDIR"]:
            return redirect(f'/register/{acc_id}/{app.config["REDIR"][form.status.data]}')
        return redirect('/login')
    return render_template('register.html', title=app.config["TITLES"]['register'], pages=app.config["PAGES"],
                           form=form)


@app.route('/news_change/<int:news_id>', methods=['GET', 'POST'])
@login_required
def edit_news(news_id):
    form = init_news_form(
        _choices=[morph.parse(item)[0].inflect({'plur', 'datv'}).word for item in app.config["ROLES"]])
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == news_id,
                                          News.user == current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.seem_for.data = news.seem_for
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == news_id,
                                          News.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.seem_for = ', '.join(
                map(lambda x: str(db_sess.execute(f"""SELECT id FROM statuses WHERE status='{x}'""").fetchone()[0]),
                    [morph.parse(item)[0].normal_form for item in form.seem_for.data]))
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/news_delete/<int:news_id>', methods=['GET', 'POST'])
@login_required
def news_delete(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == news_id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/news-add', methods=['GET', 'POST'])
@login_required
def add_news():
    form = init_news_form(
        _choices=[morph.parse(item)[0].inflect({'plur', 'datv'}).word for item in app.config["ROLES"]])
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.seem_for = ', '.join(
            map(lambda x: str(
                db_sess.execute(f"""SELECT id FROM statuses WHERE status LIKE '%{x.split()[0]}%'""").fetchone()[0]),
                [morph.parse(item)[0].normal_form for item in form.seem_for.data]))
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='Добавление новости',
                           form=form)


@app.route('/teachers')
def teachers():
    try:
        with open('static/json/content.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        db_sess = db_session.create_session()
        teachers_user = db_sess.query(User).filter(
            User.status_id == db_sess.execute("""SELECT id FROM statuses WHERE status='учитель'""").fetchone()[0])
        return render_template("teachers.html", title=app.config["TITLES"]["teachers"], pages=app.config["PAGES"],
                               **(data["/teachers"]), teachers=teachers_user)
    except Exception as error:
        logging.fatal(error)


@app.route('/docs')
def docs():
    try:
        with open('static/json/content.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template("some_page.html", title=app.config["TITLES"]["docs"], pages=app.config["PAGES"],
                               **(data["/docs"]))
    except Exception as error:
        logging.fatal(error)


@app.route('/raise')
def raising():
    try:
        with open('static/json/content.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template("some_page.html", title=app.config["TITLES"]["raise"], pages=app.config["PAGES"],
                               **(data["/raise"]))
    except Exception as error:
        logging.fatal(error)


@app.route('/')
def index():
    try:
        with open('static/json/content.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)

        db_sess = db_session.create_session()
        if current_user.is_authenticated:
            news = db_sess.query(News).filter(
                News.seem_for.like(f'%{ current_user.status_id }%')
            ).order_by(News.date).all()[::-1]  # питонист
        else:
            news = db_sess.query(News).filter(
                News.seem_for.like('%5%')
            ).order_by(News.date).all()[::-1]

        return render_template("index.html", title="Главная", pages=app.config["PAGES"], **(data["/"]), news=news)
    except Exception as error:
        logging.fatal(error)


if __name__ == '__main__':
    db_session.global_init("db/school_relations.db")
    update_lists()

    api.add_resource(news_resources.NewsListResource, '/api/news')
    api.add_resource(news_resources.NewsResource, '/api/news/<int:news_id>')

    sched = BackgroundScheduler(daemon=True)
    # каждые 2 года чистим БД от старых новостей
    sched.add_job(upd, 'interval', minutes=60 * 24 * 366)
    # каждый час обновляем конфиг
    sched.add_job(update_lists, 'interval', minutes=60)
    sched.start()

    app.run()
