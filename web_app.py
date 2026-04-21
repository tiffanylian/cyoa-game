"""Flask web server for CYOA Horror Game."""

import os
import sys
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from datetime import timedelta
import uuid
from src.ai_service import StoryGenerator, get_ai_provider
from src.config_manager import ConfigManager

app = Flask(__name__, template_folder='templates')

# Configure session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

# Game instances per session
games = {}

BRIEFING = """
INCIDENT: Emergency 911 Call
TIME: 11:47 PM
LOCATION: Thornfield Mansion (isolated, 5 miles from town)

CALLER: Female voice, panicked
LAST WORDS: "He's here... Thornfield Mansion... he's going to kill me..." [Screaming] [Sound of struggle] [SILENCE]

SUSPECT PROFILE:
• Serial killer - Operating in region for 6 months
• Confirmed victims: 4+ (possibly more)
• Method: Picking off victims at night, dragging them to remote estates, assaulting them, and leaving them to die.

YOUR ROLE:
• First responder on scene
• Victim may be bleeding out RIGHT NOW
• Backup arrives in 15 minutes - you're alone
• Objective: Extract victim, apprehend suspect, preserve evidence

CURRENT TIME: 11:50 PM (3 minutes since the call went dead)

⚠️ EVERY SECOND COUNTS ⚠️
"""


def get_game_instance(session_id):
    """Get or create a game instance for the session."""
    if session_id not in games:
        try:
            api_key = ConfigManager.get_or_prompt_api_key("openai")
            provider = get_ai_provider("openai", api_key)
            games[session_id] = StoryGenerator(provider)
        except Exception as e:
            return None
    return games[session_id]


@app.route('/')
def index():
    """Serve the game homepage."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html', briefing=BRIEFING)


@app.route('/api/start-game', methods=['POST'])
def start_game():
    """Initialize a new game."""
    try:
        session_id = session.get('session_id')
        if not session_id:
            session['session_id'] = str(uuid.uuid4())
            session_id = session['session_id']
        
        # Reset game for this session
        if session_id in games:
            del games[session_id]
        
        game = get_game_instance(session_id)
        if not game:
            return jsonify({"error": "Failed to initialize game. Check API key."}), 500
        
        # Initialize game
        opening_scene = game.initialize_game()
        
        # Generate image for opening scene
        image_url = game.generate_image_for_scene(opening_scene)
        
        return jsonify({
            "success": True,
            "scene": opening_scene,
            "image": image_url,
            "game_over": False,
            "outcome": None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/action', methods=['POST'])
def process_action():
    """Process a player action."""
    try:
        data = request.json
        action = data.get('action', '').strip()
        
        if not action:
            return jsonify({"error": "Action cannot be empty"}), 400
        
        session_id = session.get('session_id')
        game = get_game_instance(session_id)
        
        if not game:
            return jsonify({"error": "Game not initialized"}), 400
        
        # Process the action
        response = game.process_action(action)
        
        # Generate image for this scene
        image_url = game.generate_image_for_scene(response)
        
        # Check if game ended
        game_over = game.game_over
        outcome = game.game_outcome
        
        return jsonify({
            "success": True,
            "scene": response,
            "image": image_url,
            "game_over": game_over,
            "outcome": outcome
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/state', methods=['GET'])
def get_state():
    """Get current game state."""
    try:
        session_id = session.get('session_id')
        game = get_game_instance(session_id)
        
        if not game or not game.conversation_history:
            return jsonify({
                "initialized": False,
                "turn": 0,
                "game_over": False
            })
        
        # Count turns (system messages don't count as turns)
        user_messages = [msg for msg in game.conversation_history if msg['role'] == 'user']
        turn = len(user_messages)
        
        return jsonify({
            "initialized": True,
            "turn": turn,
            "game_over": game.game_over,
            "outcome": game.game_outcome
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/restart', methods=['POST'])
def restart_game():
    """Restart the game."""
    try:
        session_id = session.get('session_id')
        if session_id in games:
            del games[session_id]
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
