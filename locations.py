from random import *
import os


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
            properties = player_opponent.info()
            with open('monster_preview.txt', 'r') as file:
                event_form = file.read().split('|')
                for elem in event_form:
                    if elem in properties:
                        event_form[event_form.index(elem)] = str(properties[elem])
                return ({'text': ''.join(event_form),
                         'stats': properties})

        else:
            return (current_event.execute())



class Rat(Monster):
    def __init__(self):
        self.form = os.path.abspath()
        self.name = 'Small rat'
        self.lvl = 1
        self.atk = 4
        self.defence = 1
        self.hp = 10

    def victory(self):
        return ({'status': 'victory',
                 'exp': 15,
                 'gold': 3})

    def lose(self):
        return ({'status': 'lose',
                 'max_hp': -1,
                 'gold': -3})




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
            with open(self.form, 'r') as file:
                event_form = file.read().split('|')
                for elem in event_form:
                    if elem in self.properties:
                        event_form[event_form.index(elem)] = str(self.properties[elem])
                return ({'text': ''.join(event_form),
                         'stats': self.properties})
        except Exception:
            return ({'text': 'Error with file "' + self.form + '".'})


Waterfall = Event(form=os.path.abspath('static/events/waterfall.txt'),
                  properties={'hp': 0,
                              'max_hp': 0,
                              'defence': 0,
                              'atk': 0,
                              'gold': 0,
                              'exp': 0})

location_forest = Location([Rat], [Waterfall])

# DarkQuest/location/monstr/to_do

# Hero
# id_monstr
# hp mostr
