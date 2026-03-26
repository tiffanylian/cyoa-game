# Quick Start Guide

## Setup Instructions

### 1. Get an API Key

Choose one of the following:

**Option A: OpenAI (Recommended for GPT)**
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set it as an environment variable:
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

**Option B: Anthropic Claude**
1. Go to https://console.anthropic.com/
2. Create a new API key
3. Set it as an environment variable:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

For Claude support (optional):
```bash
pip install anthropic
```

### 3. Run the Game

```bash
cd src
python game.py
```

### 4. Choose Your Provider

When prompted, select:
- Option 1 for OpenAI
- Option 2 for Claude

## Playing the Game

- Describe your actions naturally: "I slowly open the door and look inside"
- The AI generates the story based on your input
- Your health and sanity decrease based on your decisions
- Game ends when health or sanity reaches 0
- Each playthrough is unique!

## Troubleshooting

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### "API key not found"
Make sure your environment variable is set:
```bash
# Check if it's set
echo $OPENAI_API_KEY  # or echo $ANTHROPIC_API_KEY

# Set it (macOS/Linux)
export OPENAI_API_KEY="your-key-here"

# Set it (Windows PowerShell)
$env:OPENAI_API_KEY = "your-key-here"
```

### "Rate limit exceeded"
You may have hit your API provider's rate limit. Wait a moment and try again.

### "Connection error"
Check your internet connection and that the API service is online.

## Game Tips

- Be creative with your descriptions
- Your word choices matter—the AI reacts to them
- Watch your sanity meter
- Some choices are more dangerous than others
- Try different paths for new stories

Enjoy your nightmare! 👻
