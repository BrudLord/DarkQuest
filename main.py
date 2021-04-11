from flask import Flask, render_template
import os
import config as con
from work_with_db import db_session


con.app = Flask(__name__)
con.app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@con.app.route('/')
def login():
    params = {
    }
    return render_template('login.html', **params)


if __name__ == '__main__':
    db_session.global_init("db/base.sqlite")
    con.app.run()
