from flask import Flask, render_template, redirect
import os
import sqlite3
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
            init_hero(form.name.data)
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
        sl = {
            'lvl': 1,
            'money': 0,
            'equip': [['1', '2', '3', '4 dm', 'Нет'],
                      ['2', '3', '4', '5 dm', 'Нет'],
                      ['1', '2', '3', '4 df', 'Нет'],
                      ['2', '3', '4', '5 df', 'Нет']],
            'invent': [],
            'characteristics': {
                'Damage': 1,
                'CritChance': 1,
                'Armor': 1,
                'HealPoints': 1,
                'Agility': 1,
                'Accurancy': 1,
            }
        }
        user = User(
            name=form.name.data,
            data=str(sl)
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        init_hero(form.name.data)
        return redirect('/main_window')
    return render_template('registration.html', title='DarkQuest', form=form)


@con.app.route('/inventar', methods=['GET', 'POST'])
def inventar():
    sl = []
    for i in con.hero.data['characteristics'].keys():
        sl.append([i, con.hero.data['characteristics'][i]])
    eq = con.hero.data['equip'][:]
    eq.extend((5 - len(con.hero.data['equip'])) * [5 * [' ']])
    tables = {
        'table_1': {
            'header': ['Характеристика', 'Значение'],
            'character': sl,
        },
        'table_2': {
            'header': ['Название', 'Доступ', 'Цена', 'Урон/Защита', 'Надето'],
            'equip': eq,
        },
        'table_3': {
            'header': ['Название', 'Количество'],
            'invent': [['Презренный металл', str(con.hero.data['money'])],
                       ['Зелье здоровья', str(con.hero.data['invent'].count('хилка'))],
                       ['Зелье маны', str(con.hero.data['invent'].count('манка'))]]
        },
    }
    return render_template('inventar.html', title='DarkQuest', tables=tables, level=con.hero.data['lvl'])


@con.app.route('/main_window', methods=['GET', 'POST'])
def main_window():
    return str(con.hero.data)


@con.app.route('/inventar_tranzit/<a>', methods=['GET', 'POST'])
def invent(a):
    a = int(a)
    if a != 0 and a <= len(con.hero.data['equip']):
        if con.hero.data['equip'][a - 1][-1] == 'Да':
            con.hero.data['equip'][a - 1][-1] = 'Нет'
        else:
            con.hero.data['equip'][a - 1][-1] = 'Да'
            for i in range(len(con.hero.data['equip'])):
                if a - 1 != i:
                    if 'dm' in con.hero.data['equip'][a - 1][-2]:
                        if 'dm' in con.hero.data['equip'][i][-2] and con.hero.data['equip'][i][-1] == 'Да':
                            con.hero.data['equip'][i][-1] = 'Нет'
                    else:
                        if 'df' in con.hero.data['equip'][i][-2] and con.hero.data['equip'][i][-1] == 'Да':
                            con.hero.data['equip'][i][-1] = 'Нет'
    return redirect('/inventar')



def init_hero(name):
    co = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    con.hero.name = name
    con.hero.data = eval(cur.execute('''SELECT data FROM users
    WHERE name = ?''', (name, )).fetchall()[0][0])
    co.close()


if __name__ == '__main__':
    db_session.global_init("db/base.sqlite")
    con.app.run(port=8080, debug=True)
