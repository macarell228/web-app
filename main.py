from flask import Flask
from flask import render_template
from config import Config

from data import db_session

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    return render_template("base.html")


if __name__ == '__main__':
    db_session.global_init("db/school_relations.db")
    app.run()
