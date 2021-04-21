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
            if con.hero.data['lvl'] <= 5 and con.hero.data['lvl'] < m_properties['lvl']:
                return self.next_event()
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
        self.name = 'Small rat'
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
                if m_properties['atk'] > con.hero.total_df:
                    con.hero.data['c_hp'] -= (m_properties['atk'] - con.hero.total_df)
                else:
                    con.hero.data['c_hp'] -= int(m_properties['atk'] * 0.01) + 1
            else:
                if m_properties['defence'] < int((con.hero.total_dm - 1) * 0.6) + 1:
                    m_properties['hp'] -= int((con.hero.total_dm - 1) * 0.6) + 1 - m_properties[
                        'defence']
                else:
                    m_properties['hp'] -= 1
                if m_properties['atk'] > int(con.hero.total_df * 1.5):
                    con.hero.data['c_hp'] -= (m_properties['atk'] - con.hero.total_df)
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
                  properties={'hp': 10 * con.hero.data['lvl']})
Backpack = Event(form=os.path.abspath('static/events/backpack.txt'),
                 properties={'money': -5 * con.hero.data['lvl']})
ChickenFight_win = Event(form=os.path.abspath('static/events/chickenfight_win.txt'),
                         properties={'money': randint(185, 215)})
ChickenFight_lose = Event(form=os.path.abspath('static/events/chickenfight_lose.txt'),
                          properties={'money': -randint(125, 156)})
ChickenFight_neutral = Event(form=os.path.abspath('static/events/chickenfight_neutral.txt'),
                             properties={'dm': 1})
Farmer = Event(form=os.path.abspath('static/events/farmer.txt'),
               properties={'hp': 5 * con.hero.data['lvl']})
ForestTraining = Event(form=os.path.abspath('static/events/forest_training.txt'),
                       properties={'HealPoints': 5 * (con.hero.data['invent'].count('манка') // 15),
                                   'dm': (con.hero.data['invent'].count('манка') // 15),
                                   'arm': (con.hero.data['invent'].count('манка') // 15)})
GoblinEvent = Event(form=os.path.abspath('static/events/goblin.txt'),
                    properties={'money': -10 * con.hero.data['lvl']})
Graveyard = Event(form=os.path.abspath('static/events/goblin.txt'),
                  properties={'money': (-100 // con.hero.data['lvl'])})
KnightEvent = Event(form=os.path.abspath('static/events/goblin.txt'), properties={})

# Объявление локации
location_forest = Location([Rat], [Waterfall])

# DarkQuest/location/monstr/to_do

# Hero
# id_monstr
# hp mostr
