from flask import Flask, render_template, redirect
import os
import config as con
from work_with_db import db_session
from forms.user import RegisterForm, LoginForm
from work_with_db.Users import User
from flask_login import LoginManager, login_user


con.app = Flask(__name__)
con.app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(con.app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@con.app.route('/', methods=['GET', 'POST'])
@con.app.route('/log_in', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.name == form.name.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect("/main_window")
        return render_template('login.html',
                               title='DarkQuest',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='DarkQuest', form=form)


@con.app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='DarkQuest',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.name == form.name.data).first():
            return render_template('registration.html', title='DarkQuest',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            data='[]'
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/main_window')
    return render_template('registration.html', title='DarkQuest', form=form)


@con.app.route('/inventar', methods=['GET', 'POST'])
def inventar():
    return render_template('inventar.html', title='DarkQuest')


if __name__ == '__main__':
    db_session.global_init("db/base.sqlite")
    con.app.run(port=8080, debug=True)
