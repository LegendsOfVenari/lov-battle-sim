from flask import Flask, render_template, request, session
from battle import Battle, ActionType
from venari import Aharas, Akulaw, Algala
from config import akulaw_base_stats, aharas_base_stats, algala_base_stats
import os

app = Flask(__name__)
app.secret_key = "some_secret_key"


def serialize_teams(team1, team2):
    serialized_team1 = [serialize_venari(venari) for venari in team1]
    serialized_team2 = [serialize_venari(venari) for venari in team2]
    return serialized_team1, serialized_team2


def serialize_venari(venari):
    """Convert a Venari object into a serializable dictionary."""
    return {
        'name': venari.name,
        'level': venari.level,
        'hp': venari.hp,
        'energy': venari.energy,
        'next_attack': venari.attack_tick_counter,
        'swap_cooldown': venari.swap_cooldown,
        'active_effects': [effect.description() for effect in venari.active_effects]
    }


def deserialize_teams(serialized_team1, serialized_team2):
    team1 = [deserialize_venari(data) for data in serialized_team1]
    team2 = [deserialize_venari(data) for data in serialized_team2]
    return team1, team2


def deserialize_venari(data):
    """Convert a serialized dictionary into a Venari object."""
    name = data['name']
    level = data['level']

    if name == "Akulaw":
        venari = Akulaw(name, akulaw_base_stats, level)
    elif name == "Aharas":
        venari = Aharas(name, aharas_base_stats, level)
    elif name == "Algala":
        venari = Algala(name, algala_base_stats, level)
    else:
        raise ValueError(f"Unknown Venari name: {name}")

    venari.hp = data['hp']
    venari.energy = data['energy']
    venari.attack_tick_counter = data.get('next_attack', 0)
    venari.swap_cooldown = data.get('swap_cooldown', 0)
    # Note: We're not deserializing 'active_effects' here since it requires a deeper understanding of the effect system.
    # You'd need another deserialization function for effects if you want to restore them.
    return venari

def deserialize_effect(data):
    pass

def serialize_effect(effect):
    pass


@app.route('/', methods=['GET', 'POST'])
def index():
    print("Index route hit!")

    messages = []

    if 'game_started' not in session or request.form.get('new_game'):
        session['game_started'] = True
        team1, team2 = initialize_teams()
        session['team1'], session['team2'] = serialize_teams(team1, team2)
        session['tick'] = 0

    team1, team2 = deserialize_teams(session['team1'], session['team2'])
    tick_count = session['tick']
    battle = Battle(team1, team2, tick_count)

    if request.method == 'POST':
        action = request.form.get('action')
        print(f"Received action: {action}")

        if action == ActionType.ABILITY.value:
            result = battle.interactive_battle_simulation(ActionType.ABILITY)
        elif "swap_" in action:
            swap_index = int(action.split("_")[1])  # Extract Venari index from the action
            result = battle.interactive_battle_simulation(ActionType.SWAP, swap_index)
        elif action == ActionType.NEXT_TICK.value:
            result = battle.interactive_battle_simulation(ActionType.NEXT_TICK)
        elif action == ActionType.NEW_GAME.value:
            result = battle.interactive_battle_simulation(ActionType.NEW_GAME)
        else:
            result = None

        if result:
            messages.extend(result["messages"])
            session['tick'] = result["tick_count"]
            session['team1'], session['team2'] = serialize_teams(result['team1_status'], result['team2_status'])

    # Deserialize the teams for displaying in the template
    team1_status, team2_status = serialize_teams(team1, team2)
    return render_template('index.html', team1_status=team1_status, team2_status=team2_status, tick=session['tick'], messages=messages)


def initialize_teams():
    team1 = [
        Aharas("Aharas", aharas_base_stats, 4), 
        Akulaw("Akulaw", akulaw_base_stats, 6), 
        Algala("Algala", algala_base_stats, 5)
    ]
    team2 = [
        Akulaw("Akulaw", akulaw_base_stats, 5), 
        Akulaw("Akulaw", akulaw_base_stats, 7), 
        Akulaw("Akulaw", akulaw_base_stats, 2)
    ]
    return team1, team2


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
