from flask import Flask, render_template, redirect, request
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
    con.hero.name = None
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
    con.hero.name = None
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
            'money': 10000,
            'in_battle': False,
            'exp': 0,
            'equip': [],
            'invent': [],
            'characteristics': {
                'Damage': 1,
                'Armor': 1,
                'HealPoints': 1
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
    if con.hero.name is None:
        return redirect('/log_in')
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


@con.app.route('/inventar_tranzit/<a>', methods=['GET', 'POST'])
def invent(a):
    if con.hero.name is None:
        return redirect('/log_in')
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

        con.hero.total_dm = con.hero.data['characteristics']['Damage']
        con.hero.total_df = con.hero.data['characteristics']['Armor']
        for i in range(len(con.hero.data['equip'])):
            if con.hero.data['equip'][i][-1] == 'Да':
                if 'df' in con.hero.data['equip'][i][-2]:
                    con.hero.total_df += int(con.hero.data['equip'][i][-2].split()[0])
                else:
                    con.hero.total_dm += int(con.hero.data['equip'][i][-2].split()[0])
    return redirect('/inventar')


@con.app.route('/main_window')
def main_window():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('test.html')


@con.app.route('/help')
def help():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('help.html')


@con.app.route('/settings')
def settings():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('Settings.html')


@con.app.route('/map')
def map():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('Dark Quest.html')


@con.app.route('/no')
def no():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('no_money.html')


@con.app.route('/tranzit/<item>')
def tranzit(item):
    if con.hero.name is None:
        return redirect('/log_in')
    co = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    if item == 'хилка' or item == 'манка':
        if int(con.hero.data['money']) > 1:
            con.hero.data['invent'].append(item)
            con.hero.data['money'] -= 1
            resulte = cur.execute('''UPDATE users
            SET data = ? 
            WHERE name = ?''', (str(con.hero.data), con.hero.name,))
            co.commit()
        return redirect('/map')


def tranzit_armor(item):
    if con.hero.name is None:
        return redirect('/log_in')
    co = sqlite3.connect('db/items.sqlite')
    ca = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    car = ca.cursor()
    mon = cur.execute('''SELECT cost FROM Armor WHERE name = ?''', (item,)).fetchone()
    if int(con.hero.data['money']) >= int(mon[0]):
        con.hero.data['money'] -= int(mon[0])
        result = list(cur.execute('''SELECT * FROM Armor WHERE name = ?''', (item,)).fetchone())[1:]
        result.append('Нет')
        print(result)
        con.hero.data['equip'].append(result)
        resulte = car.execute('''UPDATE users
                SET data = ? 
                WHERE name = ?''', (str(con.hero.data), con.hero.name,))
        co.commit()
        ca.commit()
        return redirect('/map')
    else:
        return redirect('/no')


def tranzit_gear(item):
    if con.hero.name is None:
        return redirect('/log_in')
    co = sqlite3.connect('db/items.sqlite')
    ca = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    car = ca.cursor()
    mon = cur.execute('''SELECT cost FROM Weapons WHERE name = ?''', (item,)).fetchone()
    if int(con.hero.data['money']) >= int(mon[0]):
        con.hero.data['money'] -= int(mon[0])
        result = list(cur.execute('''SELECT * FROM Weapons WHERE name = ?''', (item,)).fetchone())[1:]
        result.append('Нет')
        print(result)
        con.hero.data['equip'].append(result)
        resulte = car.execute('''UPDATE users
                    SET data = ? 
                    WHERE name = ?''', (str(con.hero.data), con.hero.name,))
        co.commit()
        ca.commit()
        return redirect('/map')
    else:
        return redirect('/no')


@con.app.route('/armor', methods=['GET', 'POST'])
def choice():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('choice.html')


@con.app.route('/buy_armor', methods=['GET', 'POST'])
def buy_armor():
    if con.hero.name is None:
        return redirect('/log_in')
    item = request.form['test']
    return tranzit_armor(item)


@con.app.route('/weapon', methods=['GET', 'POST'])
def choice1():
    if con.hero.name is None:
        return redirect('/log_in')
    return render_template('choice1.html')


@con.app.route('/buy_gear', methods=['GET', 'POST'])
def buy_gear():
    if con.hero.name is None:
        return redirect('/log_in')
    item = request.form['test2']
    return tranzit_gear(item)


@con.app.route('/show_cost_armor', methods=['GET', 'POST'])
def show_cost_armor():
    if con.hero.name is None:
        return redirect('/log_in')
    import sqlite3
    item = request.form['test']
    co = sqlite3.connect('db/items.sqlite')
    cur = co.cursor()
    result = cur.execute('''SELECT * FROM Armor WHERE name = ?''', (item,)).fetchone()
    print(result)
    '''сюда надо запихнуть покозатель денег игрока ---->'''
    return render_template('success.html', item=item, full=result)


@con.app.route('/show_cost_gear', methods=['GET', 'POST'])
def show_cost_gear():
    if con.hero.name is None:
        return redirect('/log_in')
    import sqlite3
    item = request.form['test2']
    co = sqlite3.connect('db/items.sqlite')
    cur = co.cursor()
    result = cur.execute('''SELECT * FROM Weapons WHERE name = ?''', (item,)).fetchone()
    print(result)
    '''сюда надо запихнуть покозатель денег игрока ---->'''
    return render_template('success2.html', item=item, full=result)


def init_hero(name):
    co = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    con.hero.name = name
    con.hero.data = eval(cur.execute('''SELECT data FROM users
    WHERE name = ?''', (name,)).fetchall()[0][0])
    con.hero.total_dm = con.hero.data['characteristics']['Damage']
    con.hero.total_df = con.hero.data['characteristics']['Armor']
    for i in range(len(con.hero.data['equip'])):
        if con.hero.data['equip'][i][-1] == 'Да':
            if 'df' in con.hero.data['equip'][i][-2]:
                con.hero.total_df += int(con.hero.data['equip'][i][-2].split()[0])
            else:
                con.hero.total_dm += int(con.hero.data['equip'][i][-2].split()[0])
    co.close()


if __name__ == '__main__':
    db_session.global_init("db/base.sqlite")
    con.app.run(port=8080, debug=True)
