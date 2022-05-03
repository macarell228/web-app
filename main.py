from flask import Flask
from flask import render_template
from config import Config

from data import db_session

app = Flask(__name__)
app.config.from_object(Config)

PAGES = {('Boba', 'https://yandex.ru'): [],
         'Ann': [('Qurt', 'https://mail.ru'), ('Swirt', 'https://github.com')]}


@app.route('/news/')
def news_view(kwargs):
    return render_template("view.html", pages=PAGES, **kwargs)


if __name__ == '__main__':
    db_session.global_init("db/school_relations.db")
    app.run()
