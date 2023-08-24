from flask import Flask, render_template, request, session
from battle import Battle, ActionType
from venari import Aharas, Akulaw, Algala, Venari, Meeka, Nyrie
from config import venari_base_stats_map
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
    messages = session.get('messages', ["Game started!"])

    # Check if the POST request is a result of the team selection form submission
    if request.method == 'POST' and 'player_venari1' in request.form:
        team1 = [initialize_venari(name, messages, True) for name in ['player_venari1', 'player_venari2', 'player_venari3']]
        team2 = [initialize_venari(name, messages, False) for name in ['ai_venari1', 'ai_venari2', 'ai_venari3']]
        battle = Battle(team1, team2, 0, messages)
        session['team1'], session['team2'] = serialize_teams(team1, team2)
        session['tick'] = 0
        session['messages'] = messages
        session['game_started'] = True
        session['team1_arena_effects'] = {}
        session['team2_arena_effects'] = {}

    # If it's not a team selection submission, handle the battle logic
    else:
        if 'game_started' not in session or request.form.get('action') == ActionType.NEW_GAME.value:
            team1, team2 = default_teams(messages)
            session['game_started'] = False
        else:
            team1, team2 = deserialize_teams(session['team1'], session['team2'], messages)

        battle = Battle(team1, team2, session.get('tick', 0), messages)
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
                session['messages'] = result["messages"]
                session['tick'] = result["tick_count"]
                session['team1'], session['team2'] = serialize_teams(result['team1_status'], result['team2_status'])
                session['team1_arena_effects'] = result['team1_arena_effects']
                session['team2_arena_effects'] = result['team2_arena_effects']

    # Deserialize the teams for displaying in the template
    team1_status, team2_status = serialize_teams(team1, team2)
    return render_template('index.html',
                           team1_status=team1_status,
                           team2_status=team2_status,
                           tick=session.get('tick', 0),
                           messages=messages,
                           game_started=session.get('game_started', False))

def initialize_venari(name_key, messages, isPlayerVenari):
    name = request.form.get(name_key)
    base_stats = venari_base_stats_map.get(name)
    return Venari(name, base_stats, 10, messages, isPlayerVenari)

def default_teams(messages):
    # This function can be used to set default teams if needed.
    team1 = [
        Aharas("Aharas", venari_base_stats_map.get("Aharas"), 10, messages, True),
        Akulaw("Akulaw", venari_base_stats_map.get("Akulaw"), 10, messages, True),
        Nyrie("Nyrie", venari_base_stats_map.get("Nyrie"), 10, messages, True)
    ]
    team2 = [
        Algala("Algala", venari_base_stats_map.get("Algala"), 10, messages, False),
        Meeka("Meeka", venari_base_stats_map.get("Meeka"), 10, messages, False),
        Akulaw("Akulaw", venari_base_stats_map.get("Akulaw"), 10, messages, False)
    ]
    return team1, team2

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
