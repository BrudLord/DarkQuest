from flask import Flask
from flask import render_template

app = Flask(__name__)

enemy_hp = 20
my_hp = 20
my_atk = 3
e_atk = 1


def attack(is_attack_postion, player_id):
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

# Нужно создать три таких - по одной на каждую локацию.
#WORK IN PROGRESS
def trip_location_name(location, player_id):
    if player_id['in_battle'] is not True:
        location.next_event(player_id)
    else:
        response = attack(player_id)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')