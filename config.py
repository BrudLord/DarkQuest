import player
import sqlite3


app = None
logged_in = False
hero = player.Hero()


def check_player_stats():
    if hero.data['exp'] >= 10 * 2 ** (hero.data['lvl'] + 2):
        hero.data['exp'] -= 10 * 2 ** (hero.data['lvl'] + 2)
        hero.data['lvl'] += 1
        hero.data['characteristics']['Damage'] += 1
        hero.data['characteristics']['Armor'] += 1
        hero.data['characteristics']['HealPoints'] += 25
        co = sqlite3.connect('db/base.sqlite')
        cur = co.cursor()
        resulte = cur.execute('''UPDATE users
            SET data = ? 
            WHERE name = ?''', (str(hero.data), hero.name,))
        co.commit()
    if hero.data['c_hp'] > hero.data['characteristics']['HealPoints']:
        hero.data['c_hp'] = hero.data['characteristics']['HealPoints']
    if hero.data['money'] < 0:
        hero.data['money'] = 0
