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


# Объявление монтров пещер


# Объявление монтров леса


# Объявление эвентов лесов
Waterfall = Event(form=os.path.abspath('static/events/waterfall.txt'),
                  properties={'hp': 10})
# Объявление эвентов полей

# Объявление эвентов пещер

# Объявление локации
location_forest = Location([Rat], [Waterfall])
location_caves = Location([Rat], [Waterfall])
location_fields = Location([Rat], [Waterfall])

# DarkQuest/location/monstr/to_do

# Hero
# id_monstr
# hp mostr
