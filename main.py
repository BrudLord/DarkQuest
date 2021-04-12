from flask import Flask, render_template, redirect
from flask_login import LoginManager
import os
import config as con
from work_with_db import db_session
from forms.user import RegisterForm, LoginForm
from work_with_db.Users import User


con.app = Flask(__name__)
con.app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(con.app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@con.app.route('/', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    form_log = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('login.html', title='DarkQuest',
                                   form=form,
                                   form_log=form_log,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            data='[]'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/fdb')
    return render_template('login.html', title='DarkQuest', form=form, form_log=form_log)


if __name__ == '__main__':
    db_session.global_init("db/base.sqlite")
    con.app.run()