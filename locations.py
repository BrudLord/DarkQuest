from random import *
import os
import config as con

m_properties = {}


class Monster():
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


# Объявление монтра
class Rat(Monster):
    def __init__(self):
        self.name = 'Маленькая крыса'
        self.lvl = 1
        self.atk = 4
        self.defence = 1
        self.hp = 10

    def victory(self):
        con.hero.data['money'] += 3
        con.hero.data['exp'] += 150
        con.check_player_stats()
        return ({'status': 'victory',
                 'exp': 15,
                 'money': 3})

    def lose(self):
        con.hero.data['money'] -= 3
        con.hero.data['c_hp'] = 15
        con.check_player_stats()
        con.hero.data['in_battle'] = False
        return ({'status': 'lose',
                 'money': -3})


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


class dart_smesharus(Monster):
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
            return ({
                'status': 'processing',
                'delta_hero_hp': delta_hero_hp,
                'delta_monster_hp': delta_monster_hp
            })
        elif con.hero.data['c_hp'] <= 0:
            return (player_opponent.lose())
        elif m_properties['hp'] <= 0:
            return (player_opponent.victory())


class Event:
    def __init__(self, form='', properties={}):
        self.form = form
        self.properties = {'hp': 0,
                           'max_hp': 0,
                           'defence': 0,
                           'atk': 0,
                           'gold': 0,
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
                con.check_player_stats()
                return ({'text': ''.join(event_form),
                         'stats': self.properties})
        except Exception:
            return ({'text': 'Error with file "' + self.form + '".'})


# Объявление эвента
Waterfall = Event(form=os.path.abspath('static/events/waterfall.txt'),
                  properties={'hp': 10})
# Объявление локации
location_forest = Location([Rat, Big_rat, Fire_rat, Opa, Small_Supoed, Satanuga, Supoed, Big_Supoed, dart_smesharus,
                            Sharik], [Waterfall])

# DarkQuest/location/monstr/to_do

# Hero
# id_monstr
# hp mostr
