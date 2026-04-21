# Mansion of Shadows

An AI-powered horror detective game. You're a first responder arriving at an abandoned mansion to a 911 call about a serial killer. Investigate, survive, and uncover the truth—or die trying.

## Concept

- **Mission**: Extract a victim and apprehend a serial killer at Thornfield Mansion
- **Gameplay**: Your actions are described naturally (not menu-driven)
- **AI Storytelling**: Every playthrough is unique—the AI adapts to your choices in real-time
- **Consequences**: Your decisions affect your health, sanity, and the victim's fate
- **Ending**: Multiple outcomes based on your choices and survival

## Installation

### Requirements
- Python 3.8+
- OpenAI API key (get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys))

### Setup

1. Clone/download this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

### Web Version (Recommended)

1. Run the Flask web server:
   ```bash
   python web_app.py
   ```

2. Open your browser and go to:
   ```
   http://localhost:5000
   ```

3. Click "Enter the Mansion" to start your adventure

4. Describe your actions naturally in the text input:
   ```
   I carefully approach the front door and listen for sounds
   ```

### Terminal Version

1. Run the game:
   ```bash
   cd src
   python main.py
   ```

When prompted, you can either:
- Set `OPENAI_API_KEY` as an environment variable, or
- Enter your API key directly when the game asks

## How to Play

When the game starts, you'll receive a mission briefing, then be placed at the scene. Describe your actions naturally:

```
➤ What do you do?: I carefully approach the front door and listen for sounds
```

The AI will respond with what happens next, including consequences for your actions. Continue investigating, gathering clues, and making decisions to uncover the killer's identity and save the victim.

---

**Ready to enter the mansion?** 👻

```bash
cd src
python game.py
```

Select your preferred AI provider when prompted, then describe your actions as you would in a conversation. The AI will generate the story based on your input.

### Example Gameplay

```
➤ What do you do?: I cautiously enter the mansion through the front door

[The story unfolds...]

You push the heavy oak door open. It creaks ominously on its hinges, 
revealing a grand foyer shrouded in darkness and dust. Your phone's 
flashlight illuminates dust particles dancing through the stale air...
```

## 🎯 Game Mechanics

- **Health (0-100)**: Decreases when you encounter danger or make risky choices
- **Sanity (0-100)**: Decreases when you witness disturbing events or learn dark truths
- **Natural Language Input**: Describe your actions however you want—the AI understands context
- **Dynamic Consequences**: Actions have immediate and lasting effects on the story
- **Game Over Conditions**:
  - Health reaches 0: You succumb to death
  - Sanity reaches 0: Your mind breaks

## 📁 Project Structure

```
cyoa-game/
├── src/
│   ├── game.py           # Main game engine with AI integration
│   ├── ai_service.py     # AI provider abstraction (OpenAI, Claude)
│   ├── ascii_art.py      # ASCII art generation and presets
│   ├── story.py          # Legacy story system (presets)
│   └── main.py           # Legacy main entry point
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── assets/               # Future expansion for assets
```

## 💡 Tips for a Great Experience

1. **Be Descriptive**: Instead of just "go left," try "I carefully explore the left hallway, listening for any sounds"
2. **Roleplay**: Immerse yourself in the character and describe how you react emotionally
3. **Pay Attention**: The AI picks up on details in your descriptions to create consequences
4. **Watch Your Stats**: Let paranoia influence your decisions when sanity gets low
5. **Experiment**: Try different approaches—the AI responds to variety

## 🔧 Configuration

### Switching Providers

You can easily switch between OpenAI and Anthropic Claude:

```bash
python game.py
# Choose option 2 when prompted to use Claude instead of OpenAI
```

### Custom System Prompts

Edit `ai_service.py` to modify the `SYSTEM_PROMPT` constant to change the AI's behavior and personality.

## 🚀 Future Enhancements

- [ ] Save/load game state
- [ ] Multiple character options
- [ ] Inventory system with AI-aware items
- [ ] Memory system (AI remembers past choices)
- [ ] Multiple story arcs and campaign modes
- [ ] Difficulty levels (affects sanity/health drain rates)
- [ ] Sound effects (ASCII bell, text-based descriptions)
- [ ] Web-based interface
- [ ] Multiplayer mode with shared narratives

## ⚠️ Content Warning

This game contains themes of:
- Psychological horror
- Death and violence (described)
- Existential dread
- Disturbing imagery (ASCII-based)

## 📝 License

MIT License

## 🤝 Contributing

Feel free to fork and submit pull requests to improve the game!

---

**Ready to enter the mansion? Your nightmare awaits...** 👻