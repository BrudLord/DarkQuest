import player
import sqlite3


app = None
logged_in = False
hero = player.Hero()


def check_lvl():
    if hero.data['exp'] >= 10 * 2 ** (hero.data['lvl'] + 2):
        hero.data['exp'] -= 10 * 2 ** (hero.data['lvl'] + 2)
        hero.data['lvl'] += 1
        co = sqlite3.connect('db/base.sqlite')
        cur = co.cursor()
        resulte = cur.execute('''UPDATE users
            SET data = ? 
            WHERE name = ?''', (str(hero.data), hero.name,))
        co.commit()
