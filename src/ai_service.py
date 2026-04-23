"""AI service for generating dynamic story responses."""

import os
import json
import re
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

    def generate_image(self, scene_description: str) -> Optional[str]:
        """Generate an image using DALL-E based on scene description."""
        try:
            # Create a concise prompt for image generation
            image_prompt = f"""Horror game scene - {scene_description[:200]}. 
Dark, cinematic, atmospheric horror. 
No text or words in the image."""
            
            print(f"[DALL-E] Requesting image generation with prompt: {image_prompt[:100]}...")
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            url = response.data[0].url
            print(f"[DALL-E] Image generated successfully: {url[:50]}...")
            return url
        except Exception as e:
            # Log and return None if image generation fails
            import traceback
            print(f"[DALL-E ERROR] {str(e)}")
            traceback.print_exc()
            return None


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

END GAME CONDITIONS:
The game ends when ONE of these occurs:
1. ESCAPED: Player drives away or flees the mansion successfully
2. PLAYER_DEAD: Player is killed by the killer or dies from injuries
3. KILLER_DEAD: Player kills/shoots the killer
4. KILLER_RESTRAINED: Player restrains, handcuffs, or traps the killer
5. VICTIM_RESCUED: Player rescues the victim and escapes with them alive
6. VICTIM_DEAD: Victim dies (killed by killer or can't be saved)

When an end condition is met:
- PICK ONLY ONE outcome
- Add EXACTLY ONE of these tags at the END of your response (no others):
  - If escaped: "[GAME_OVER: ESCAPED]"
  - If player dies: "[GAME_OVER: PLAYER_DEAD]"
  - If killer dies: "[GAME_OVER: KILLER_DEAD]"
  - If killer restrained: "[GAME_OVER: KILLER_RESTRAINED]"
  - If victim rescued: "[GAME_OVER: VICTIM_RESCUED]"
  - If victim dies: "[GAME_OVER: VICTIM_DEAD]"

CRITICAL: If multiple outcomes seem possible (e.g., "they could escape or die"), pick the MOST LIKELY based on the action and make that the definitive outcome. Do not add multiple tags. Do not hedge.

NEVER:
- "The killer remains unseen" after multiple encounters
- "You sense danger" without specifics
- Delays when the player makes a direct action (lure, search, provoke)
- Stretching the mystery beyond 5 turns
- Vague responses. Be specific about danger and NPC status."""

    def __init__(self, provider: AIProvider):
        self.provider = provider
        self.conversation_history = []
        self.game_over = False
        self.game_outcome = None
        self.killer_encounter_turns = 0
        self.killer_injured = False

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

        # Hard rule: getting in the car and driving away is always an ESCAPED ending.
        # This prevents incorrect end-state tags from the model.
        if self._is_car_escape_action(user_action):
            response_without_tags = re.sub(r"\s*\[GAME_OVER:\s*[A-Z_]+\]\s*", " ", response).strip()
            if not response_without_tags:
                response_without_tags = "You jump into your car, slam the door, and floor the accelerator into the night."
            response = f"{response_without_tags} [GAME_OVER: ESCAPED]"
            self.game_over = True
            self.game_outcome = "escaped"
            self.conversation_history.append({"role": "assistant", "content": response})
            return response

        # Check if the player has met the killer for three turns without injuring them
        if self.killer_encounter_turns >= 3 and not self.killer_injured:
            self.game_over = True
            self.game_outcome = "player_dead"
            return "The killer strikes! You failed to act in time. [GAME_OVER: PLAYER_DEAD]"

        # Only keep narrative up to and including the first [GAME_OVER: ...] tag, and set the correct outcome
        game_over_match = re.search(r"(.*?)\[GAME_OVER: ([A-Z_]+)\]", response, re.DOTALL)
        if game_over_match:
            narrative = game_over_match.group(1).strip()
            tag = game_over_match.group(2).lower()
            response = narrative + " [GAME_OVER: " + game_over_match.group(2) + "]"
            # Set the game over outcome based on the first tag found
            self.game_over = True
            self.game_outcome = {
                "escaped": "escaped",
                "player_dead": "player_dead",
                "killer_dead": "killer_dead",
                "killer_restrained": "killer_restrained",
                "victim_rescued": "victim_rescued",
                "victim_dead": "victim_dead"
            }.get(tag, None)
        else:
            # Check for game over conditions as fallback
            self._check_game_over(response)

        # Store assistant response
        self.conversation_history.append({"role": "assistant", "content": response})

        return response

    def _is_car_escape_action(self, user_action: str) -> bool:
        """Return True when player clearly chooses to escape by car."""
        text = user_action.lower().strip()

        has_car = any(term in text for term in ["car", "vehicle", "truck", "van"]) 
        has_escape_intent = any(
            term in text
            for term in [
                "drive away",
                "get in",
                "jump in",
                "escape",
                "leave",
                "flee",
                "floor it",
                "speed away",
                "start the engine",
            ]
        )

        return has_car and has_escape_intent
    
    def _check_game_over(self, response: str) -> None:
        """Check if the game has ended based on the response.
        Only accepts the FIRST game-over tag found."""
        response_upper = response.upper()
        
        # Only set game_over once - process in order and stop at first match
        if "[GAME_OVER: ESCAPED]" in response_upper:
            self.game_over = True
            self.game_outcome = "escaped"
        elif "[GAME_OVER: PLAYER_DEAD]" in response_upper:
            self.game_over = True
            self.game_outcome = "player_dead"
        elif "[GAME_OVER: KILLER_DEAD]" in response_upper:
            self.game_over = True
            self.game_outcome = "killer_dead"
        elif "[GAME_OVER: KILLER_RESTRAINED]" in response_upper:
            self.game_over = True
            self.game_outcome = "killer_restrained"
        elif "[GAME_OVER: VICTIM_RESCUED]" in response_upper:
            self.game_over = True
            self.game_outcome = "victim_rescued"
        elif "[GAME_OVER: VICTIM_DEAD]" in response_upper:
            self.game_over = True
            self.game_outcome = "victim_dead"

    def generate_ascii_for_scene(self, scene_description: str) -> str:
        """Generate ASCII art for a scene description."""
        return self.provider.generate_ascii_art(scene_description)

    def generate_image_for_scene(self, scene_description: str) -> Optional[str]:
        """Generate a real image for a scene description."""
        if hasattr(self.provider, 'generate_image'):
            return self.provider.generate_image(scene_description)
        return None

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
