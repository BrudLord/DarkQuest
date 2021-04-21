from random import *
import os
import config as con

m_properties = {}


class Monster:
    def __init__(self):
        self.form = ''
        self.name = 'Void creature'
        self.lvl = 0
        self.atk = 0
        self.defence = 0
        self.hp = 0

    def victory(self):
        pass

    def lose(self):
        pass

    def info(self):
        return {
            'name': self.name,
            'lvl': self.lvl,
            'atk': self.atk,
            'defence': self.defence,
            'hp': self.hp
        }


class Event:
    def __init__(self, form='', properties={}):
        self.form = form
        self.properties = {'hp': 0,
                           'lvl': 0,
                           'HealPoints': 0,
                           'arm': 0,
                           'dm': 0,
                           'money': 0,
                           'exp': 0}
        for elem in properties:
            self.properties[elem] = properties[elem]

    def execute(self):
        try:
            with open(self.form, 'r', encoding='UTF-8') as file:
                event_form = file.read().split('|')
                for elem in event_form:
                    if elem in self.properties:
                        event_form[event_form.index(elem)] = str(self.properties[elem])
                con.hero.data['c_hp'] += self.properties['hp']
                con.hero.data['money'] += self.properties['money']
                con.hero.data['characteristics']['Damage'] += self.properties['dm']
                con.hero.data['characteristics']['Armor'] += self.properties['arm']
                con.hero.data['characteristics']['HealPoints'] += self.properties['HealPoints']
                con.hero.data['exp'] += self.properties['exp']
                con.hero.data['lvl'] += self.properties['lvl']
                con.check_player_stats()
                return ({'text': ''.join(event_form),
                         'stats': self.properties})
        except Exception:
            return ({'text': 'Error with file "' + self.form + '".'})


class Location:
    def __init__(self, monsters, events):
        self.monsters = monsters
        self.events = events
        self.all_options = [self.monsters, self.events]

    def next_event(self):
        global player_opponent
        current_event = choice(choice(self.all_options))
        if current_event in self.monsters:
            con.hero.data['in_battle'] = True
            player_opponent = current_event()
            global m_properties
            m_properties = player_opponent.info()
            con.hero.data['m_hp'] = m_properties['hp']
            with open(os.path.abspath('static/events/monster_preview.txt'), 'r', encoding='UTF-8') as file:
                event_form = file.read().split('|')
                for elem in event_form:
                    if elem in m_properties:
                        event_form[event_form.index(elem)] = str(m_properties[elem])
                return ({'text': ''.join(event_form),
                         'stats': m_properties})
        else:
            return (current_event.execute())


def attack(is_attack_postion):
    global m_properties
    monster_hp_before = m_properties['hp']
    hero_hp_before = con.hero.data['c_hp']
    if con.hero.data['in_battle'] is True:
        if m_properties['hp'] > 0 and con.hero.data['c_hp'] > 0:
            if is_attack_postion:
                if m_properties['defence'] < con.hero.total_dm:
                    m_properties['hp'] -= con.hero.total_dm - m_properties['defence']
                else:
                    m_properties['hp'] -= int(con.hero.total_dm * 0.01) + 1
                if m_properties['atk'] < con.hero.total_df:
                    con.hero.data['c_hp'] -= m_properties['atk'] - con.hero.total_df
                else:
                    con.hero.data['c_hp'] -= int(m_properties['atk'] * 0.01) + 1
            else:
                if m_properties['defence'] < int((con.hero.total_dm - 1) * 0.6) + 1:
                    m_properties['hp'] -= int((con.hero.total_dm - 1) * 0.6) + 1 - m_properties[
                        'defence']
                else:
                    m_properties['hp'] -= 1
                if m_properties['atk'] < int(con.hero.total_df * 1.5):
                    con.hero.data['c_hp'] -= m_properties['atk'] - con.hero.total_df
                else:
                    con.hero.data['c_hp'] -= 1
            delta_monster_hp = monster_hp_before - m_properties['hp']
            delta_hero_hp = hero_hp_before - con.hero.data['c_hp']
            con.hero.data['m_hp'] = m_properties['hp']
            if m_properties['hp'] > 0 and con.hero.data['c_hp'] > 0:
                return ({
                    'status': 'processing',
                    'delta_hero_hp': delta_hero_hp,
                    'delta_monster_hp': delta_monster_hp
                })
            elif con.hero.data['c_hp'] <= 0:
                return player_opponent.lose()
            elif m_properties['hp'] <= 0:
                return player_opponent.victory()
        elif con.hero.data['c_hp'] <= 0:
            return player_opponent.lose()
        elif m_properties['hp'] <= 0:
            return player_opponent.victory()


# Объявление монтров полей
class Mouse(Monster):
    def __init__(self):
        self.name = 'полевая мышь'
        self.lvl = 1
        self.atk = 1
        self.defence = 1
        self.hp = 5

    def victory(self):
        con.hero.data['money'] += 1
        con.hero.data['exp'] += 5
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 5,
                 'money': 1})

    def lose(self):
        con.hero.data['money'] -= 2
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -1})


class Rat(Monster):
    def __init__(self):
        self.name = 'маленькая крыса'
        self.lvl = 2
        self.atk = 3
        self.defence = 2
        self.hp = 12

    def victory(self):
        con.hero.data['money'] += 2
        con.hero.data['exp'] += 15
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 15,
                 'money': 3})

    def lose(self):
        con.hero.data['money'] -= 3
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -3})


class Volf(Monster):
    def __init__(self):
        self.name = 'юный волк'
        self.lvl = 3
        self.atk = 6
        self.defence = 3
        self.hp = 20

    def victory(self):
        con.hero.data['money'] += 3
        con.hero.data['exp'] += 15
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 15,
                 'money': 3})

    def lose(self):
        con.hero.data['money'] -= 5
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -5})


class Fox(Monster):
    def __init__(self):
        self.name = 'юный волк'
        self.lvl = 3
        self.atk = 5
        self.defence = 3
        self.hp = 18

    def victory(self):
        con.hero.data['money'] += 2
        con.hero.data['exp'] += 17
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 17,
                 'money': 2})

    def lose(self):
        con.hero.data['money'] -= 7
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -7})


class Rob(Monster):
    def __init__(self):
        self.name = 'раненый разбойник'
        self.lvl = 5
        self.atk = 10
        self.defence = 5
        self.hp = 35

    def victory(self):
        con.hero.data['money'] += 8
        con.hero.data['exp'] += 30
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 30,
                 'money': 8})

    def lose(self):
        con.hero.data['money'] -= 15
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -15})


class Mag(Monster):
    def __init__(self):
        self.name = 'деревенский колдун'
        self.lvl = 7
        self.atk = 20
        self.defence = 10
        self.hp = 50

    def victory(self):
        con.hero.data['money'] += 15
        con.hero.data['exp'] += 45
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 45,
                 'money': 15})

    def lose(self):
        con.hero.data['money'] -= 30
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -30})


class Necr(Monster):
    def __init__(self):
        self.name = 'некромант-ученик'
        self.lvl = 9
        self.atk = 45
        self.defence = 8
        self.hp = 30

    def victory(self):
        con.hero.data['money'] += 18
        con.hero.data['exp'] += 50
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 50,
                 'money': 18})

    def lose(self):
        con.hero.data['money'] -= 39
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -39})

# Объявление монтров пещер
class Demonic_kashevar_1(Monster):
    def __init__(self):
        self.name = 'юный демонический кашевар'
        self.lvl = 20
        self.atk = 150
        self.defence = 70
        self.hp = 500

    def victory(self):
        con.hero.data['money'] += 24
        con.hero.data['exp'] += 150
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 150,
                 'money': 24})

    def lose(self):
        con.hero.data['money'] -= 30
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -30})


class Demonic_kashevar_2(Monster):
    def __init__(self):
        self.name = 'демонический кашевар'
        self.lvl = 22
        self.atk = 170
        self.defence = 85
        self.hp = 580

    def victory(self):
        con.hero.data['money'] += 28
        con.hero.data['exp'] += 170
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 170,
                 'money': 28})

    def lose(self):
        con.hero.data['money'] -= 36
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -36})


class Demonic_kashevar_3(Monster):
    def __init__(self):
        self.name = 'опытный демонический кашевар'
        self.lvl = 24
        self.atk = 190
        self.defence = 100
        self.hp = 650

    def victory(self):
        con.hero.data['money'] += 31
        con.hero.data['exp'] += 200
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 200,
                 'money': 31})

    def lose(self):
        con.hero.data['money'] -= 41
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -41})


class Demonic_kashevar_4(Monster):
    def __init__(self):
        self.name = 'заместитель главы демонических кашеваров'
        self.lvl = 28
        self.atk = 230
        self.defence = 130
        self.hp = 750

    def victory(self):
        con.hero.data['money'] += 46
        con.hero.data['exp'] += 300
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 300,
                 'money': 46})

    def lose(self):
        con.hero.data['money'] -= 60
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -60})


class Demonic_kashevar_5(Monster):
    def __init__(self):
        self.name = 'глава демонических кашеваров'
        self.lvl = 34
        self.atk = 250
        self.defence = 175
        self.hp = 900

    def victory(self):
        con.hero.data['money'] += 100
        con.hero.data['exp'] += 500
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 500,
                 'money': 100})

    def lose(self):
        con.hero.data['money'] -= 150
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -150})


class Cultist_1(Monster):
    def __init__(self):
        self.name = 'юный культист'
        self.lvl = 23
        self.atk = 200
        self.defence = 100
        self.hp = 600

    def victory(self):
        con.hero.data['money'] += 34
        con.hero.data['exp'] += 200
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 200,
                 'money': 34})

    def lose(self):
        con.hero.data['money'] -= 45
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -45})


class Cultist_2(Monster):
    def __init__(self):
        self.name = 'культист'
        self.lvl = 25
        self.atk = 248
        self.defence = 100
        self.hp = 750

    def victory(self):
        con.hero.data['money'] += 56
        con.hero.data['exp'] += 300
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 300,
                 'money': 56})

    def lose(self):
        con.hero.data['money'] -= 78
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -78})


class Cultist_3(Monster):
    def __init__(self):
        self.name = 'старший культист'
        self.lvl = 29
        self.atk = 270
        self.defence = 150
        self.hp = 800

    def victory(self):
        con.hero.data['money'] += 80
        con.hero.data['exp'] += 400
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 400,
                 'money': 80})

    def lose(self):
        con.hero.data['money'] -= 100
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -100})


class Cultist_4(Monster):
    def __init__(self):
        self.name = 'заместитель главы культистов'
        self.lvl = 33
        self.atk = 310
        self.defence = 190
        self.hp = 900

    def victory(self):
        con.hero.data['money'] += 110
        con.hero.data['exp'] += 500
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 500,
                 'money': 110})

    def lose(self):
        con.hero.data['money'] -= 150
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -150})


class Cultist_5(Monster):
    def __init__(self):
        self.name = 'глава культистов'
        self.lvl = 40
        self.atk = 400
        self.defence = 210
        self.hp = 1111

    def victory(self):
        con.hero.data['money'] += 250
        con.hero.data['exp'] += 1000
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 1000,
                 'money': 250})

    def lose(self):
        con.hero.data['money'] -= 500
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -500})


class Lich_1(Monster):
    def __init__(self):
        self.name = 'лич'
        self.lvl = 31
        self.atk = 310
        self.defence = 170
        self.hp = 500

    def victory(self):
        con.hero.data['money'] += 70
        con.hero.data['exp'] += 450
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 450,
                 'money': 70})

    def lose(self):
        con.hero.data['money'] -= 95
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -95})


class Lich_2(Monster):
    def __init__(self):
        self.name = 'древний лич'
        self.lvl = 37
        self.atk = 450
        self.defence = 200
        self.hp = 400

    def victory(self):
        con.hero.data['money'] += 111
        con.hero.data['exp'] += 470
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 470,
                 'money': 111})

    def lose(self):
        con.hero.data['money'] -= 177
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -177})


class Lich_3(Monster):
    def __init__(self):
        self.name = 'древний архилич'
        self.lvl = 50
        self.atk = 666
        self.defence = 50
        self.hp = 200

    def victory(self):
        con.hero.data['money'] += 300
        con.hero.data['exp'] += 1500
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 1500,
                 'money': 300})

    def lose(self):
        con.hero.data['money'] -= 750
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -750})


class Strange_thing_1(Monster):
    def __init__(self):
        self.name = 'слепая мохнолапка'
        self.lvl = 34
        self.atk = 30
        self.defence = 250
        self.hp = 50

    def victory(self):
        con.hero.data['money'] += 30
        con.hero.data['exp'] += 100
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 100,
                 'money': 30})

    def lose(self):
        con.hero.data['money'] -= 100
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -100})


class Strange_thing_2(Monster):
    def __init__(self):
        self.name = 'сигмойдообразная эркуция'
        self.lvl = 37
        self.atk = 327
        self.defence = 100
        self.hp = 500

    def victory(self):
        con.hero.data['money'] += 1
        con.hero.data['exp'] += 150
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 150,
                 'money': 1})

    def lose(self):
        con.hero.data['money'] -= 150
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -150})


class Strange_thing_3(Monster):
    def __init__(self):
        self.name = 'скелет-воин'
        self.lvl = 20
        self.atk = 107
        self.defence = 100
        self.hp = 500

    def victory(self):
        con.hero.data['money'] += 2
        con.hero.data['exp'] += 159
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 159,
                 'money': 2})

    def lose(self):
        con.hero.data['money'] -= 150
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -150})


class Strange_thing_4(Monster):
    def __init__(self):
        self.name = 'красноглазая ложноножка'
        self.lvl = 21
        self.atk = 168
        self.defence = 70
        self.hp = 300

    def victory(self):
        con.hero.data['money'] += 17
        con.hero.data['exp'] += 100
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 10,
                 'money': 17})

    def lose(self):
        con.hero.data['money'] -= 150
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -150})


class Boss(Monster):
    def __init__(self):
        self.name = 'Повелитель'
        self.lvl = 100
        self.atk = 850
        self.defence = 100
        self.hp = 2000

    def victory(self):
        con.hero.data['money'] += 1000
        con.hero.data['exp'] += 10000
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 10000,
                 'money': 1000})

    def lose(self):
        con.hero.data['money'] -= 1500
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -1500})

# Объявление монтров леса
class Big_rat(Monster):
    def __init__(self):
        self.name = 'Большая крыса'
        self.lvl = 4
        self.atk = 9
        self.defence = 3
        self.hp = 20

    def victory(self):
        con.hero.data['money'] += 9
        con.hero.data['exp'] += 25
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 15,
                 'money': 9})

    def lose(self):
        con.hero.data['money'] -= 9
        con.hero.data['c_hp'] = 20
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -9})


class Fire_rat(Monster):
    def __init__(self):
        self.name = 'Огненная крыса'
        self.lvl = 7
        self.atk = 14
        self.defence = 0
        self.hp = 40

    def victory(self):
        con.hero.data['money'] += 30
        con.hero.data['exp'] += 50
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 50,
                 'money': 30})

    def lose(self):
        con.hero.data['money'] -= 30
        con.hero.data['c_hp'] = 50
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -30})


class Supoed(Monster):
    def __init__(self):
        self.name = 'Злобный супоед'
        self.lvl = 9
        self.atk = 3
        self.defence = 0
        self.hp = 70

    def victory(self):
        con.hero.data['money'] += 3
        con.hero.data['exp'] += 50
        con.check_player_stats()
        con.hero.data['invent'].append('хилка')
        return ({'status': 'victory',
                 'exp': 50,
                 'money': 3})

    def lose(self):
        con.hero.data['money'] -= 30
        con.hero.data['c_hp'] = 50
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -30})


class Big_Supoed(Monster):
    def __init__(self):
        self.name = 'Большой Злобный Супоед'
        self.lvl = 10
        self.atk = 16
        self.defence = 0
        self.hp = 50

    def victory(self):
        con.hero.data['money'] += 6
        con.hero.data['exp'] += 100
        con.hero.data['invent'].append('хилка')
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 100,
                 'money': 30})

    def lose(self):
        con.hero.data['money'] -= 30
        con.hero.data['c_hp'] = 50
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -30})


class Small_Supoed(Monster):
    def __init__(self):
        self.name = 'Маленький Здобный Супоед'
        self.lvl = 7
        self.atk = 6
        self.defence = 0
        self.hp = 35

    def victory(self):
        con.hero.data['money'] += 30
        con.hero.data['exp'] += 50
        con.hero.data['invent'].append('хилка')
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 50,
                 'money': 30})

    def lose(self):
        con.hero.data['money'] -= 30
        con.hero.data['c_hp'] = 50
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -30})


class Opa(Monster):
    def __init__(self):
        self.name = 'Рыцарь с К.У.К.У.Р.У.З.О.Й.'
        self.lvl = 20
        self.atk = 140
        self.defence = 30
        self.hp = 90

    def victory(self):
        con.hero.data['money'] += 300
        con.hero.data['exp'] += 700
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 700,
                 'money': 300})

    def lose(self):
        con.hero.data['money'] -= 300
        con.hero.data['c_hp'] = 1
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -300})


class Sharik(Monster):
    def __init__(self):
        self.name = 'Смешарик с бинзопелой'
        self.lvl = 17
        self.atk = 90
        self.defence = 20
        self.hp = 40

    def victory(self):
        con.hero.data['money'] += 170
        con.hero.data['exp'] += 540
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 540,
                 'money': 170})

    def lose(self):
        con.hero.data['money'] -= 300
        con.hero.data['c_hp'] = 5
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -300})


class Dart_smesharus(Monster):
    def __init__(self):
        self.name = 'Дарт смешарус'
        self.lvl = 20
        self.atk = 78
        self.defence = 100
        self.hp = 1000

    def victory(self):
        con.hero.data['money'] += 3000
        con.hero.data['exp'] += 1000
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 1000,
                 'money': 3000})

    def lose(self):
        con.hero.data['money'] -= 3000
        con.hero.data['c_hp'] = 5
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -3000})

class Satanuga(Monster):
    def __init__(self):
        self.name = 'АЦЦЦкий Сатанюга666'
        self.lvl = 21
        self.atk = 90
        self.defence = 150
        self.hp = 150

    def victory(self):
        con.hero.data['money'] += 666
        con.hero.data['exp'] += 666
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 666,
                 'money': 666})

    def lose(self):
        con.hero.data['money'] -= 666
        con.hero.data['c_hp'] = 6
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -666})


# Объявление эвентов лесов
Waterfall = Event(form=os.path.abspath('static/events/waterfall.txt'),
                  properties={'hp': 10})
# Объявление эвентов полей

# Объявление эвентов пещер

# Объявление локации
location_forest = Location([Rat, Big_rat, Fire_rat, Opa, Small_Supoed, Satanuga, Supoed, Big_Supoed, Dart_smesharus,
                            Sharik], [Waterfall])

# DarkQuest/location/monstr/to_do

# Hero
# id_monstr
# hp mostr
