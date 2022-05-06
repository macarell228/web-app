import logging
import datetime
import json

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask import render_template, jsonify, redirect, flash
from config import Config

from data import db_session
from data.users import User

from forms.user import init_register_form


def job():
    db_sess = db_session.create_session()
    date = datetime.datetime.now()
    delta = datetime.timedelta(days=(app.config["CLEAN_TIME_YEARS"] * 365))
    before = date - delta
    table = app.config["TABLE_CLEAN"]
    db_sess.execute("DELETE FROM ? WHERE date<?", (table, before))

    logging.critical(f"Очищена таблица {table} с записями, выпущенными до {before}")


app = Flask(__name__)
app.config.from_object(Config)

PAGES = {('Boba', 'https://yandex.ru'): [],
         'Ann': [('Qurt', 'https://mail.ru'), ('Swirt', 'https://github.com')]}


def get_custom_choices():
    return """<p>BEBRA HERE LOOK AT ME"""


@app.route("/api/registration-choices/<choice>", methods=["GET"])
def my_route():
    custom_choices = get_custom_choices()
    return jsonify(custom_choices)


@app.route('/news/')
def news_view(kwargs):
    return render_template("view.html", title=kwargs['news'], pages=PAGES, **kwargs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = init_register_form(["работник Администрации", "учитель", "ученик", "специалист"], [2, 3, 4])
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
            status_id=db_sess.execute(f'''SELECT id FROM statuses WHERE status="{form.status.name}"''')
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/')
def index():
    with open('/static/json/content.json', mode='r', encoding='utf-8') as f:
        data = json.load(f)
    print(1)
    print(data["index.html"])
    print(2)
    print(**(data["index.html"]))
    return render_template("index.html", title="Главная", pages=PAGES, **(data["index.html"]))


if __name__ == '__main__':
    db_session.global_init("db/school_relations.db")
    """user = User()
    user.surname = 'Губарева'
    user.name = "Екатерина"
    user.patronymic = "Alexevna"
    user.email = "email@email.ru"
    user.hashed_password = 'afdadfcwe'
    user.access_level_id = 4
    user.status_id = 1
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()"""
    # каждые 2 года чистим БД от старых новостей
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(job, 'interval', minutes=60 * 24 * 366)
    sched.start()

    app.run()
