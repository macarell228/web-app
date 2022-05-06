import logging
import datetime
import json

from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask import render_template, jsonify, redirect

from config import Config

from data import db_session
from data.users import User
from data.news import News

from forms.user import init_register_form, init_optional_register_form


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
    app.config["CLASSES"] = [''.join(map(str, item)) for item in
                             db_sess.execute("""SELECT class_number, class_letter FROM classes""").fetchall()]
    app.config["SUBJECTS"] = db_sess.execute("""SELECT id, subject FROM subjects""").fetchall()

    logging.warning(f"Обновлены переменные конфигурации.")


app: Flask = Flask(__name__)
app.config.from_object(Config)


@app.route('/news/<news_id>')
def news_view(news_id):
    # мусор!!!

    a = News(title="Кто-то съел весь хлеб в столовой!!!!", seem_for="1, 2, 3, 4", content="""Однако для отображения пользователю диалога о подтверждении какого-либо действия или информационного сообщения о каком-нибудь системном событии (например, об ошибке) в PyQT есть более привычный и подходящий инструмент. Это класс QMessageBox, у которого с QInputDialog общий родитель — QDialog. Поэтому импортируем его из PyQt5.QtWidgets, вызовем метод question(), в который передаются следующие параметры:

    Родитель — self
    Заголовок — обычно передается пустое поле, если мы хотим задать пользователю вопрос
    Текст вопроса
    Варианты ответов — QMessageBox.Yes, QMessageBox.No
    Возможности QMessageBox достаточно широки, рекомендуем ознакомиться с ними в документации.

    После того как пользователь нажмет на одну из кнопок, результат будет занесен в переменную valid. А затем будет выполнена проверка и удаление.

    Важно обратить внимание на то, что текст запроса формируется с использованием и конкатенации строк, и оператора "?". В данной задаче мы также столкнулись с методом commit() у соединения с базой данных. Не забывайте фиксировать изменения после изменения данных или их удаления.""",
             author_id=1)

    # мусор!!!!
    return render_template("view.html", title=app.config["TITLES"]['news'], pages=app.config["PAGES"], news=a,
                           surname="Пупкин", name="Вася", status="ученик", date="21.09.2022 10:30")


@app.route('/register/<account_id>/<filename>', methods=['GET', 'POST'])
def _back_func(account_id, filename):
    form = init_optional_register_form(app.config["CLASSES"])
    print(form.education_class.data)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.education_class.data:
            print(form.education_class.data)
            tmp = form.education_class.data
            class_number, class_letter = int(tmp[:-1]), tmp[-1]
            class_id = db_sess.execute("""SELECT id FROM classes WHERE class_number=? AND class_letter='?'""",
                                       (class_number, class_letter)).fetchone()[0]
            db_sess.execute("""INSERT INTO students(account_id, class_id) VALUES(?, ?)""", (account_id, class_id))
            return redirect('/login')
        if form.work_exp.data and form.dir_of_preparation.data and form.academics.data and form.subjects.data:
            print(form.work_exp.data, form.dir_of_preparation.data, form.academics.data, form.subjects.data, sep='\n')

            return redirect('/login')
        return render_template(filename, title=app.config["TITLES"]['register'], pages=app.config["PAGES"],
                               form=form, account_id=account_id, filename=filename, message='Не все поля заполнены.')
    return render_template(filename, title=app.config["TITLES"]['register'],
                           pages=app.config["PAGES"], form=form, account_id=account_id, filename=filename)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = init_register_form(app.config["ROLES"])
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


@app.route('/pages/page-1')
def page1():
    try:
        with open('static/json/content.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
        return render_template("some_page.html", title=app.config["TITLES"]["page"], pages=app.config["PAGES"],
                               **(data["/pages/page-1"]))
    except Exception as error:
        logging.fatal(error)


@app.route('/')
def index():
    try:
        with open('static/json/content.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)

        # мусор!!
        a = News(title="Кто-то съел весь хлеб в столовой!!!!", seem_for="1, 2, 3, 4", content="""Однако для отображения пользователю диалога о подтверждении какого-либо действия или информационного сообщения о каком-нибудь системном событии (например, об ошибке) в PyQT есть более привычный и подходящий инструмент. Это класс QMessageBox, у которого с QInputDialog общий родитель — QDialog. Поэтому импортируем его из PyQt5.QtWidgets, вызовем метод question(), в который передаются следующие параметры:

Родитель — self
Заголовок — обычно передается пустое поле, если мы хотим задать пользователю вопрос
Текст вопроса
Варианты ответов — QMessageBox.Yes, QMessageBox.No
Возможности QMessageBox достаточно широки, рекомендуем ознакомиться с ними в документации.

После того как пользователь нажмет на одну из кнопок, результат будет занесен в переменную valid. А затем будет выполнена проверка и удаление.

Важно обратить внимание на то, что текст запроса формируется с использованием и конкатенации строк, и оператора "?". В данной задаче мы также столкнулись с методом commit() у соединения с базой данных. Не забывайте фиксировать изменения после изменения данных или их удаления.""",
                 author_id=1)
        # мусор!!

        return render_template("index.html", title="Главная", pages=app.config["PAGES"], **(data["/"]),
                               news=[a], surname="Пупкин", name="Вася", status="ученик", date="21.09.2022 10:30")
    except Exception as error:
        logging.fatal(error)


if __name__ == '__main__':
    db_session.global_init("db/school_relations.db")

    update_lists()

    sched = BackgroundScheduler(daemon=True)
    # каждые 2 года чистим БД от старых новостей
    sched.add_job(upd, 'interval', minutes=60 * 24 * 366)
    # каждый час обновляем конфиг
    sched.add_job(update_lists, 'interval', minutes=60)
    sched.start()

    app.run()
