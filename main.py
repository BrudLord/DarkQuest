from flask import Flask, render_template, redirect
import os
import config as con
from work_with_db import db_session
from forms.user import RegisterForm
from work_with_db.Users import User


con.app = Flask(__name__)
con.app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@con.app.route('/', methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('login.html', title='DarkQuest',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('login.html', title='DarkQuest',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('login.html', title='DarkQuest', form=form)


if __name__ == '__main__':
    db_session.global_init("db/base.sqlite")
    con.app.run()
