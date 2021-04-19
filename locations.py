from random import *
import os
import config as con


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
        global m_properties
        current_event = choice(choice(self.all_options))
        if current_event in self.monsters:
            con.hero.data['in_battle'] = True
            player_opponent = current_event()
            m_properties = player_opponent.info()
            with open(os.path.abspath('static/events/monster_preview.txt'), 'r', encoding='UTF-8') as file:
                event_form = file.read().split('|')
                for elem in event_form:
                    if elem in m_properties:
                        event_form[event_form.index(elem)] = str(m_properties[elem])
                return ({'text': ''.join(event_form),
                         'stats': m_properties})

        else:
            return (current_event.execute())


class Rat(Monster):
    def __init__(self):
        self.name = 'Small rat'
        self.lvl = 1
        self.atk = 4
        self.defence = 1
        self.hp = 10

    def victory(self):
        con.hero.data['money'] += 3
        return ({'status': 'victory',
                 'exp': 0,
                 'money': 3})

    def lose(self):
        con.hero.data['money'] -= 3
        con.hero.data['c_hp'] = 15
        con.check_player_stats()
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
                return ({'text': ''.join(event_form),
                         'stats': self.properties})
        except Exception:
            return ({'text': 'Error with file "' + self.form + '".'})


Waterfall = Event(form=os.path.abspath('static/events/waterfall.txt'),
                  properties={'c_hp': 0})

location_forest = Location([Rat], [Waterfall])

# DarkQuest/location/monstr/to_do

# Hero
# id_monstr
# hp mostr
