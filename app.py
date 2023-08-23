from flask import Flask, render_template, request, session
from battle import Battle, ActionType
from venari import Aharas, Akulaw, Algala, Venari, Meeka
from config import akulaw_base_stats, aharas_base_stats, algala_base_stats, meeka_base_stats
import os

app = Flask(__name__)
app.secret_key = "some_secret_key"


def serialize_teams(team1, team2):
    serialized_team1 = [Venari.serialize_venari(venari) for venari in team1]
    serialized_team2 = [Venari.serialize_venari(venari) for venari in team2]
    return serialized_team1, serialized_team2

def deserialize_teams(serialized_team1, serialized_team2, messages):
    team1 = [Venari.deserialize_venari(data, messages) for data in serialized_team1]
    team2 = [Venari.deserialize_venari(data, messages) for data in serialized_team2]
    return team1, team2


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'game_started' not in session or request.form.get('action') == ActionType.NEW_GAME.value:
        messages = ["Game started!"]
        team1, team2 = initialize_teams(messages)
        battle = Battle(team1, team2, 0, messages)  # Use a different variable name to avoid confusion
        session['team1'], session['team2'] = serialize_teams(team1, team2)
        session['tick'] = 0
        session['messages'] = messages
        session['game_started'] = True
        session['team1_arena_effects'] = {}
        session['team2_arena_effects'] = {}
    else:
        messages = session.get('messages', [])  # Defaults to an empty list if 'messages' is not found
        team1, team2 = deserialize_teams(session['team1'], session['team2'], messages)
        tick_count = session['tick']
        battle = Battle(team1, team2, tick_count, messages)
        session['team1_arena_effects'] = session.get('team1_arena_effects', {})
        session['team2_arena_effects'] = session.get('team2_arena_effects', {})

    for venari in team1:
        venari.battle = battle
    for venari in team2:
        venari.battle = battle

    if request.method == 'POST':
        action = request.form.get('action')

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
            session['messages'] = (result["messages"])
            session['tick'] = result["tick_count"]
            session['team1'], session['team2'] = serialize_teams(result['team1_status'], result['team2_status'])
            session['team1_arena_effects'] = result['team1_arena_effects']
            session['team2_arena_effects'] = result['team2_arena_effects']

    # Deserialize the teams for displaying in the template
    team1_status, team2_status = serialize_teams(team1, team2)
    return render_template('index.html', team1_status=team1_status, team2_status=team2_status, tick=session['tick'], messages=messages)


def initialize_teams(messages):
    team1 = [
        Aharas("Aharas", aharas_base_stats, 4, messages, True),
        Akulaw("Akulaw", akulaw_base_stats, 6, messages, True),
        Meeka("Meeka", meeka_base_stats, 5, messages, True)
    ]
    team2 = [
        Algala("Algala", algala_base_stats, 5, messages, False),
        Akulaw("Akulaw", akulaw_base_stats, 7, messages, False),
        Akulaw("Akulaw", akulaw_base_stats, 2, messages, False)
    ]
    return team1, team2


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
