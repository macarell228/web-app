from flask import Flask
from flask import render_template
from config import Config

from data import db_session

app = Flask(__name__)
app.config.from_object(Config)

PAGES = {'Boba': [], 'Ann': ['Qurt', 'Swirt']}


@app.route('/')
def index():
    return render_template("index.html", pages=PAGES, name='Gubareva Ekaterina')


if __name__ == '__main__':
    db_session.global_init("db/school_relations.db")
    app.run()
