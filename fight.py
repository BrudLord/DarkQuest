from flask import Flask
from flask import render_template
from locations import *

app = Flask(__name__)

enemy_hp = 20
my_hp = 20
my_atk = 3
e_atk = 1


def attack(is_attack_postion):
    monster_hp_before = player_id['opponent']['hp']
    hero_hp_before = player_id['hp']
    if player_id['in_battle'] is True:
        if player_id['opponent']['hp'] > 0 and player_id['hp'] > 0:
            if is_attack_postion:
                if player_id['opponent']['defence'] < player_id['atk']:
                    player_id['opponent']['hp'] -= player_id['atk'] - player_id['opponent']['defence']
                else:
                    player_id['opponent']['hp'] -= int(player_id['atk'] * 0.01) + 1
                if player_id['opponent']['atk'] < player_id['defence']:
                    player_id['hp'] -= player_id['opponent']['atk'] - player_id['defence']
                else:
                    player_id['hp'] -= int(player_id['opponent']['atk'] * 0.01) + 1
            else:
                if player_id['opponent']['defence'] < int((player_id['atk'] - 1) * 0.6) + 1:
                    player_id['opponent']['hp'] -= int((player_id['atk'] - 1) * 0.6) + 1 - player_id['opponent'][
                        'defence']
                else:
                    player_id['opponent']['hp'] -= 1
                if player_id['opponent']['atk'] < int(player_id['defence'] * 1.5):
                    player_id['hp'] -= player_id['opponent']['atk'] - player_id['defence']
                else:
                    player_id['hp'] -= 1
            delta_monster_hp = monster_hp_before - player_id['opponent']['hp']
            delta_hero_hp = hero_hp_before - player_id['hp']
            return ({
                'status': 'processing',
                'delta_hero_hp': delta_hero_hp,
                'delta_monster_hp': delta_monster_hp
            })
        elif player_id['hp'] <= 0:
            return (player_id['opponent']['example'].lose(player_id))
        elif player_id['opponent']['hp'] <= 0:
            return (player_id['opponent']['example'].victory(player_id))


@app.route('/')
def fight_window():
    return render_template('fight.html')


@app.route('/atk')
def defence():
    location_forest(fight_validator(attack(True)))


@app.route('/defence')
def defence():
    location_forest(fight_validator(attack(False)))

@app.route('/atkscr')
def atk_screen(data=None):
    if data is None:
        with open(os.path.abspath('monster_still_fight.txt'), 'r', encoding='UTF-8') as template:
            return (template.read())
    else:
        return data

# Нужно создать три таких - по одной на каждую локацию.
# WORK IN PROGRESS
@app.route('/forest')
def location_forest(atributes=None):
    fight = con.hero.data['in_battle']
    if fight is not True:
        title = 'Dark Forest'
        event_text = location_forest.next_event()
    else:
        event_text = atk_screen(atributes)
    return render_template('forest.html', event_text=event_text, title=title, fight=con.hero.data['in_battle'])

