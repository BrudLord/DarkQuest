from flask import Flask
from flask import render_template
import config as con


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
@app.route('/tranzit/<item>')
def tranzit(item):
    import sqlite3
    from flask import redirect
    con.hero.data['invent'].append(item)
    co = sqlite3.connect('db/base')
    cur = co.cursor()
    if item == 'хилка' or item == 'манка':
        con.hero.data['money'] -= 1
        resulte = cur.execute('''UPDATE users
        SET data = ? 
        WHERE name = ?''', (str(con.hero.data), con.hero.name,))
        co.commit()
    return redirect('/map')






if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
