from flask import Flask
from flask import render_template
import config as con
from flask import request

app = Flask(__name__)


@app.route('/')
@app.route('/countdown')
def main_window():
    return render_template('test.html')


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/settings')
def settings():
    return render_template('Settings.html')


@app.route('/map')
def map():
    return render_template('Dark Quest.html')


'''транзиты предметов'''


@app.route('/no')
def no():
    return render_template('no_money.html')


@app.route('/tranzit/<item>')
def tranzit(item):
    import sqlite3
    from flask import redirect
    con.hero.data['invent'].append(item)
    co = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    if item == 'хилка' or item == 'манка':
        if int(con.hero.data['money']) > 1:
            con.hero.data['money'] -= 1
            resulte = cur.execute('''UPDATE users
            SET data = ? 
            WHERE name = ?''', (str(con.hero.data), con.hero.name,))
            co.commit()
        return redirect('/map')


def tranzit_armor(item):
    import sqlite3
    from flask import redirect
    co = sqlite3.connect('db/items.sqlite')
    ca = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    car = ca.cursor()
    mon = cur.execute('''SELECT cost FROM Armor WHERE name = ?''', (item,)).fetchone()
    if int(con.hero.data['money']) >= int(mon[0]):
        con.hero.data['money'] -= int(mon[0])
        result = cur.execute('''SELECT * FROM Armor WHERE name = ?''', (item,)).fetchone()
        print(result)
        con.hero.data['invent'].append(result)
        resulte = car.execute('''UPDATE users
                SET data = ? 
                WHERE name = ?''', (str(con.hero.data), con.hero.name,))
        co.commit()
        ca.commit()
        return redirect('/map')
    else:
        return redirect('/no')


def tranzit_gear(item):
    import sqlite3
    from flask import redirect
    co = sqlite3.connect('db/items.sqlite')
    ca = sqlite3.connect('db/base.sqlite')
    cur = co.cursor()
    car = ca.cursor()
    mon = cur.execute('''SELECT cost FROM Weapons WHERE name = ?''', (item,)).fetchone()
    if int(con.hero.data['money']) >= int(mon[0]):
        con.hero.data['money'] -= int(mon[0])
        result = cur.execute('''SELECT * FROM Weapons WHERE name = ?''', (item,)).fetchone()
        print(result)
        con.hero.data['invent'].append(result)
        resulte = car.execute('''UPDATE users
                    SET data = ? 
                    WHERE name = ?''', (str(con.hero.data), con.hero.name,))
        co.commit()
        ca.commit()
        return redirect('/map')
    else:
        return redirect('/no')


@app.route('/armor', methods=['GET', 'POST'])
def choice():
    return render_template('choice.html')


@app.route('/buy_armor', methods=['GET', 'POST'])
def buy_armor():
    item = request.form['test']
    tranzit_armor(item)


@app.route('/weapon', methods=['GET', 'POST'])
def choice1():
    return render_template('choice1.html')


@app.route('/buy_gear', methods=['GET', 'POST'])
def buy_gear():
    item = request.form['test2']
    tranzit_gear(item)


@app.route('/show_cost_armor', methods=['GET', 'POST'])
def show_cost_armor():
    import sqlite3
    item = request.form['test']
    co = sqlite3.connect('db/items.sqlite')
    cur = co.cursor()
    result = cur.execute('''SELECT * FROM Armor WHERE name = ?''', (item,)).fetchone()
    print(result)
    '''сюда надо запихнуть покозатель денег игрока ---->'''
    return render_template('success.html', item=item, full=result)


@app.route('/show_cost_gear', methods=['GET', 'POST'])
def show_cost_gear():
    import sqlite3
    item = request.form['test2']
    co = sqlite3.connect('db/items.sqlite')
    cur = co.cursor()
    result = cur.execute('''SELECT * FROM Weapons WHERE name = ?''', (item,)).fetchone()
    print(result)
    '''сюда надо запихнуть покозатель денег игрока ---->'''
    return render_template('success2.html', item=item, full=result)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
