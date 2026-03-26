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

    SYSTEM_PROMPT = """You are a horror game narrator. The player is a first responder at Thornfield Mansion responding to a serial killer emergency.

CRITICAL:
- A serial killer is operating in the area. At least 4 confirmed victims.
- A woman just called 911 from the mansion screaming. The call went silent.
- The player has 15 minutes before backup arrives.
- This is a RESCUE MISSION that becomes a SURVIVAL HORROR game.

NARRATIVE RULES:
- Keep responses SHORT: 3-4 sentences of vivid description per turn
- Be SPECIFIC: Use concrete details (blood, sounds, smells) not vague atmosphere
- TRACK THE VICTIM: Are they alive? Where? What condition?
- TRACK THE KILLER: Gradual reveals of who/what they are, their methods
- ESCALATE: Each turn, something worse is revealed or a new threat emerges
- GIVE SUGGESTIONS: Suggest 2-3 possible actions, but don't force numbered lists—let player describe what they do

DO NOT:
- Use vague language ("you sense danger")
- Break character or use game-speak
- Drag out the mystery forever—gradually reveal the killer's identity and methods
- Generate long responses that cut off mid-sentence"""

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
        prompt = """OPENING SCENE:

You pull up to Thornfield Mansion at midnight. Your headlights illuminate the front steps.

Describe with vivid detail:
1. What you see (the mansion's condition, blood, damage, entry points)
2. What you hear (movement? crying? silence? screams?)
3. What you smell (metallic? burning? decay?)
4. Signs of where the victim might be

Then suggest 2-3 possible actions the player could try, but don't force them to choose from a list.
Keep it to 3-4 sentences of description plus brief action suggestions."""

        self.conversation_history.append({"role": "user", "content": prompt})
        
        response = self.provider.generate_response(prompt, messages=self.conversation_history)
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response

    def process_action(self, user_action: str) -> str:
        """Process a player action and generate the next story beat."""
        # Add user action to history
        self.conversation_history.append({"role": "user", "content": user_action})
        
        # Generate response using full conversation history
        response = self.provider.generate_response("", messages=self.conversation_history)
        
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
