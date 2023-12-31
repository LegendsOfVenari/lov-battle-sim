from flask import Flask, render_template, request, session
from battle import Battle, ActionType
from venari import Aharas, Akulaw, Algala, Venari, Meeka, Nyrie
from arena_effect import ArenaEffect
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


def serialize_arena_effects(team1_arena_effects, team2_arena_effects):
    serialized_team1_arena_effect = {key: effect.serialize()
                                     for key, effect in team1_arena_effects.items()}

    serialized_team2_arena_effect = {key: effect.serialize()
                                     for key, effect in team2_arena_effects.items()}

    return serialized_team1_arena_effect, serialized_team2_arena_effect


def deserialize_arena_effects(serialized_team1_arena_effect, serialized_team2_arena_effect, messages):
    team1_arena_effects = {arena_effect_id: ArenaEffect.deserialize(data, messages) 
                           for arena_effect_id, data in serialized_team1_arena_effect.items()}

    team2_arena_effects = {arena_effect_id: ArenaEffect.deserialize(data, messages) 
                           for arena_effect_id, data in serialized_team2_arena_effect.items()}

    return team1_arena_effects, team2_arena_effects

@app.route('/', methods=['GET', 'POST'])

def index():
    # messages = session.get('messages', ["Game started!"])
    messages = []
    team1_arena_effects = {}
    team2_arena_effects = {}

    # Check if the POST request is a result of the team selection form submission
    if request.method == 'POST' and 'player_venari1' in request.form:
        team1 = [initialize_venari('player_venari' + str(i), 'player_venari' + str(i) + '_level', messages, True) for i in range(1, 4) if request.form.get('player_venari' + str(i)) != "None"]
        team2 = [initialize_venari('ai_venari' + str(i), 'ai_venari' + str(i) + '_level', messages, False) for i in range(1, 4) if request.form.get('ai_venari' + str(i)) != "None"]
        team1_arena_effects = {}
        team2_arena_effects = {}
        battle = Battle(team1, team2, 0, messages)
        session['team1'], session['team2'] = serialize_teams(team1, team2)
        session['tick'] = 0
        session['messages'] = [messages]
        session['game_started'] = True
        session['team1_arena_effects'] = {}
        session['team2_arena_effects'] = {}

    # If it's not a team selection submission, handle the battle logic
    else:
        if 'game_started' not in session or request.form.get('action') == ActionType.NEW_GAME.value:
            team1, team2 = default_teams(messages)
            team1_arena_effects = {}
            team2_arena_effects = {}
            session['game_started'] = False
        else:
            if 'team1' in session and 'team2' in session:
                team1, team2 = deserialize_teams(session['team1'], session['team2'], messages)
                team1_arena_effects, team2_arena_effects = deserialize_arena_effects(session['team1_arena_effects'], session['team2_arena_effects'], messages)
            else:
                team1, team2 = default_teams(messages)
                team1_arena_effects = {}
                team2_arena_effects = {}
                session['game_started'] = True

        battle = Battle(team1, team2, session.get('tick', 0), messages, team1_arena_effects, team2_arena_effects)

        for venari in team1:
            venari.battle = battle
        for venari in team2:
            venari.battle = battle

        if request.method == 'POST':
            action = request.form.get('action')
            result = None
            if action == "next_battle":
                # Reset the AI's Venari team
                # _, team2 = default_teams(messages)
                for venari in team1:
                    venari.battle_handler.energy = 0
                    venari.battle_handler.is_assist = False
                    venari.battle_handler.assist_cooldown = 0
                team2 = [initialize_venari(name, name + '_level', messages, False) for name in ['ai_venari1', 'ai_venari2', 'ai_venari3'] if request.form.get(name) != "None"]
                team2 = list(filter(None, team2))  # This will remove any None values from the list
                if len(team2) == 0:
                    _, team2 = default_teams(messages)

                team2_arena_effects = {}
                battle = Battle(team1, team2, 0, messages)
                session['team1'], session['team2'] = serialize_teams(team1, team2)
                session['tick'] = 0
                session['messages'] = [messages]
                session['game_started'] = True
                session['team1_arena_effects'] = {}
                session['team2_arena_effects'] = {}
            elif action == ActionType.HEAL.value:
                for venari in team1:
                    venari.battle_stats.hp = venari.battle_stats.initial_hp
                    venari.battle_handler.energy = 0
                    venari.battle_handler.is_assist = False
                    venari.battle_handler.assist_cooldown = 0

                session['team1'], session['team2'] = serialize_teams(team1, team2)
                print("Healed!")
            elif action == ActionType.ABILITY.value:
                result = battle.interactive_battle_simulation(ActionType.ABILITY)
            elif "swap_" in action:
                swap_index = int(action.split("_")[1])  # Extract Venari index from the action
                result = battle.interactive_battle_simulation(ActionType.SWAP, swap_index)
            elif action == ActionType.NEXT_TICK.value:
                result = battle.interactive_battle_simulation(ActionType.NEXT_TICK)
            elif action == ActionType.NEW_GAME.value:
                result = battle.interactive_battle_simulation(ActionType.NEW_GAME)

            if result:
                session['messages'] = result["messages"]
                session['tick'] = result["tick_count"]
                session['team1'], session['team2'] = serialize_teams(result['team1_status'], result['team2_status'])
                session['team1_arena_effects'], session['team2_arena_effects'] = serialize_arena_effects(result['team1_arena_effects'], result['team2_arena_effects'])

    # Deserialize the teams for displaying in the template
    team1_status, team2_status = serialize_teams(team1, team2)
    team1_arena_effects_status, team2_arena_effects_status = serialize_arena_effects(team1_arena_effects, team2_arena_effects)
    return render_template('index.html',
                           team1_status=team1_status,
                           team2_status=team2_status,
                           team1_arena_effects_status=team1_arena_effects_status,
                           team2_arena_effects_status=team2_arena_effects_status,
                           tick=session.get('tick', 0),
                           messages=messages,
                           game_started=session.get('game_started', False))

def initialize_venari(name_key, level_key, messages, isPlayerVenari):
    name = request.form.get(name_key)
    level = int(request.form.get(level_key, 1))  # Fetch level; default to 1 if not found
    if not name:
        return None  # If name is None or empty, return None
    base_stats = venari_base_stats_map.get(name)
    print(f"Name: {name}, Base Stats: {base_stats}")  # Add this line
    return Venari(name, base_stats, level, messages, isPlayerVenari)

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
