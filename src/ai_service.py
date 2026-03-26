"""AI service for generating dynamic story responses."""

import os
import json
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """Generate a response from the AI."""
        pass

    @abstractmethod
    def generate_ascii_art(self, scene_description: str) -> str:
        """Generate ASCII art based on scene description."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI API provider for story generation."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )

        try:
            import openai

            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")

    def generate_response(self, prompt: str, messages: Optional[list] = None) -> str:
        """Generate a story response using OpenAI."""
        try:
            if messages:
                # Use full conversation history
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.8,
                    max_tokens=200,
                )
            else:
                # Single message
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8,
                    max_tokens=200,
                )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    def generate_ascii_art(self, scene_description: str) -> str:
        """Generate ASCII art using OpenAI."""
        prompt = f"""Create ASCII art for this horror scene. Use only ASCII characters, keep it under 15 lines.
Scene: {scene_description}

Return ONLY the ASCII art, no explanation."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            return response.choices[0].message.content
        except Exception as e:
            return ""  # Return empty string if ASCII generation fails


class ClaudeProvider(AIProvider):
    """Anthropic Claude API provider for story generation."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable."
            )

        try:
            from anthropic import Anthropic

            self.client = Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")

    def generate_response(self, prompt: str) -> str:
        """Generate a story response using Claude."""
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=240,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Claude API error: {str(e)}")

    def generate_ascii_art(self, scene_description: str) -> str:
        """Generate ASCII art using Claude."""
        prompt = f"""Create ASCII art for this horror scene. Use only ASCII characters, keep it under 15 lines.
Scene: {scene_description}

Return ONLY the ASCII art, no explanation."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text
        except Exception as e:
            return ""  # Return empty string if ASCII generation fails


class StoryGenerator:
    """Generates story content using AI."""

    SYSTEM_PROMPT = """You are a horror game narrator running a deadly serious survival horror game.

THE SETUP:
- Serial killer at large. 4+ confirmed victims. Operating from Thornfield Mansion.
- Woman called 911 screaming. Call went silent 5 minutes ago. She may be dying RIGHT NOW.
- Player is first responder. Alone. 15 minutes until backup. Must survive and solve this.
- The killer is REAL. He is DANGEROUS. He WILL act if provoked or discovered.

CRITICAL NARRATIVE RULES - FOLLOW EXACTLY:
1. PLAYER ACTIONS HAVE IMMEDIATE CONSEQUENCES. If they make noise, the killer hears it. If they search a room, they find something or someone finds them.
2. ESCALATE ACTIVELY. Don't delay. Each turn brings them closer to the killer or danger closer to them.
3. THE KILLER MUST APPEAR. By turn 4-5, the player should encounter the killer or evidence they're being hunted.
4. REAL STAKES. People die. Plans fail. Actions backfire. The victim may be dead. The killer may escape.
5. SHORT RESPONSES: 2-3 sentences max per scene beat, then what happens next.
6. CONCRETE DETAILS: Blood, screams, footsteps, shadows. Real sensory horror.
7. NO DELAYS OR MYSTERY STRETCHING. Move the plot forward aggressively.
8. VICTIM TRACKING: Is the victim alive? Dying? Dead? Where? Make this explicit.
9. KILLER HUNTING: Introduce clues early. Sightings by turn 3. Direct encounter by turn 5.

RESPONSE FORMAT:
[Scene description with action] → [What the player hears/sees/discovers] → [What happens BECAUSE of the player's action]

Example: "Your footsteps echo. Upstairs, something goes silent. Then you hear dragging sounds. A door slams open above. He KNOWS you're here."

NEVER:
- "The killer remains unseen" after multiple encounters
- "You sense danger" without specifics
- Delays when the player makes a direct action (lure, search, provoke)
- Stretching the mystery beyond 5 turns
- Vague responses. Be specific about danger and NPC status."""

    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.conversation_history = []

    def initialize_game(self) -> str:
        """Initialize the game with an opening scene."""
        # Reset history for new game
        self.conversation_history = []
        
        # Build initial message sequence
        self.conversation_history.append({"role": "system", "content": self.SYSTEM_PROMPT})
        
        # Now show the opening scene
        prompt = """OPENING SCENE - BE SPECIFIC AND BRUTAL:

You arrive at Thornfield Mansion. The 911 call ended 5 minutes ago with the woman screaming "He's here! He's—"

Describe what you see as you enter:
- Is there BLOOD? Where? Fresh or old?
- What SOUNDS? Breathing? Footsteps? Dragging? Silence is terrifying too.
- Can you HEAR the victim? Whimpering? Nothing?
- Signs the killer was here: tools, restraints, recent activity

2-3 vivid sentences. Then state the immediate threat/opportunity.
NO vague atmosphere. NO "you sense danger." CONCRETE HORROR."""

        self.conversation_history.append({"role": "user", "content": prompt})
        
        response = self.provider.generate_response(prompt, messages=self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response

    def process_action(self, user_action: str) -> str:
        """Process a player action and generate the next story beat."""
        # Add user action to history
        self.conversation_history.append({"role": "user", "content": user_action})
        
        # Add escalation instruction if the killer hasn't appeared yet
        escalation = ""
        if len(self.conversation_history) < 10:  # Early game
            escalation = " [CRITICAL: Player is actively investigating/acting. Something MUST happen in response. The killer should be closing in or revealing himself.]"
        elif len(self.conversation_history) < 15:  # Mid game
            escalation = " [CRITICAL: By now the killer has been encountered or is hunting the player. Escalate to direct threat/confrontation.]"
        else:  # Late game
            escalation = " [CRITICAL: This is climax time. The killer is present and dangerous. Victim's fate is NOW being decided.]"
        
        # Generate response using full conversation history
        response = self.provider.generate_response("" + escalation, messages=self.conversation_history)
        
        # Store assistant response
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response

    def generate_ascii_for_scene(self, scene_description: str) -> str:
        """Generate ASCII art for a scene description."""
        return self.provider.generate_ascii_art(scene_description)

    def get_game_state_summary(self) -> Dict[str, Any]:
        """Get a summary of the current game state from the AI."""
        if len(self.conversation_history) < 3:
            return {"health": 100, "sanity": 100, "status": "just_started"}

        # Create a summary request
        summary_messages = self.conversation_history.copy()
        summary_messages.append({
            "role": "user",
            "content": """Based on the story so far, evaluate the player's current condition:
- Health (0-100): How physically threatened or hurt are they?
- Sanity (0-100): How much horror/dread have they witnessed?
- Status: One sentence about their immediate situation.

Respond in JSON format ONLY, no other text:
{"health": <number>, "sanity": <number>, "status": "<string>"}"""
        })

        try:
            response = self.provider.generate_response("", messages=summary_messages)
            # Try to parse JSON from response
            import json

            # Find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception:
            pass

        return {"health": 100, "sanity": 100, "status": "in_progress"}

    def reset(self):
        """Reset the conversation history."""
        self.conversation_history = []


def get_ai_provider(provider_name: str = "openai", api_key: Optional[str] = None) -> AIProvider:
    """Factory function to get an AI provider."""
    provider_name = provider_name.lower()

    if provider_name == "openai":
        return OpenAIProvider(api_key)
    elif provider_name == "claude":
        return ClaudeProvider(api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
