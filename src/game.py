"""Dynamic AI-driven game engine for CYOA horror game."""

import sys
import time
import os
import random
from typing import Optional
from ai_service import StoryGenerator, get_ai_provider
from ascii_art import ASCIIArt
from config_manager import ConfigManager


class AIGame:
    """Game controller with AI-generated story."""

    def __init__(self, ai_provider: str = "openai", api_key: Optional[str] = None):
        try:
            provider = get_ai_provider(ai_provider, api_key)
            self.story_generator = StoryGenerator(provider)
            self.running = True
            self.game_state = {
                "health": 100,
                "sanity": 100,
                "turn": 0,
                "actions": [],
            }
        except (ValueError, RuntimeError) as e:
            print(f"Error initializing AI: {e}")
            sys.exit(1)

    def display_briefing(self):
        """Display the mission briefing before the game starts."""
        briefing = """
╔════════════════════════════════════════════════════════════╗
║                    DISPATCH BRIEFING                      ║
╚════════════════════════════════════════════════════════════╝

INCIDENT: Emergency 911 Call
TIME: 11:47 PM
LOCATION: Thornfield Mansion (isolated, 5 miles from town)

CALLER: Female voice, panicked
LAST WORDS: "He's here... Thornfield Mansion... he's going to 
           kill me..." [Screaming] [Sound of struggle] [SILENCE]

SUSPECT PROFILE:
• Serial killer - Operating in region for 6 months
• Confirmed victims: 4+ (possibly more)
• Method: Home invasions at isolated properties
• Pattern: Targets remote estates with minimal oversight

THORNFIELD MANSION - WHY HERE:
• Abandoned for 10 years - perfect hunting ground
• Recent signs of habitation detected
• Suspected killer base of operations
• Police surveillance scheduled for tomorrow (too late)

YOUR ROLE:
• First responder on scene
• Victim may be bleeding out RIGHT NOW
• Backup arrives in 15 minutes - you're alone
• Objective: Extract victim, apprehend suspect, preserve evidence

CURRENT TIME: 11:50 PM (3 minutes since the call went dead)

⚠️  EVERY SECOND COUNTS ⚠️

════════════════════════════════════════════════════════════
"""
        print(briefing)
        input("Press Enter to proceed to the scene...\n")

    def display_opening_scene(self):
        """Display the opening narrative."""
        scene_intro = """
╔════════════════════════════════════════════════════════════╗
║                    THORNFIELD MANSION                     ║
║                        MIDNIGHT                           ║
╚════════════════════════════════════════════════════════════╝
"""
        print(scene_intro)

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system("clear" if os.name == "posix" else "cls")

    def display_header(self):
        """Display the game header."""
        header = """
╔════════════════════════════════════════════════════════════╗
║         🏚️  MANSION OF SHADOWS  🏚️                      ║
║                                                            ║
║         AI-Powered Choose Your Own Adventure             ║
║                    Horror Game                            ║
╚════════════════════════════════════════════════════════════╝
"""
        print(header)

    def display_stats(self):
        """Display current game stats."""
        health = self.game_state["health"]
        sanity = self.game_state["sanity"]
        turn = self.game_state["turn"]

        health_bar = self._create_bar(health)
        sanity_bar = self._create_bar(sanity)

        stats = f"""
╔════════════════════════════════════════════════════════════╗
║ Health: {health_bar} {health}%  │  Sanity: {sanity_bar} {sanity}%  │  Turn: {turn}
╚════════════════════════════════════════════════════════════╝
"""
        print(stats)

    def _create_bar(self, value: int, length: int = 15) -> str:
        """Create a visual bar for stats."""
        filled = int((value / 100) * length)
        empty = length - filled
        return "█" * filled + "░" * empty

    def update_game_state(self):
        """Update game state based on AI assessment."""
        try:
            state = self.story_generator.get_game_state_summary()
            self.game_state["health"] = max(0, min(100, state.get("health", 100)))
            self.game_state["sanity"] = max(0, min(100, state.get("sanity", 100)))
        except Exception:
            # On error, slightly degrade sanity each turn
            self.game_state["sanity"] = max(0, self.game_state["sanity"] - 2)

    def display_scene(self, scene_text: str):
        """Display a scene with ASCII art."""
        self.clear_screen()
        self.display_header()

        # Try to generate ASCII art for the scene
        print("\n[Generating atmospheric visuals...]\n")
        try:
            ascii_art = self.story_generator.generate_ascii_for_scene(scene_text[:200])
            if ascii_art and ascii_art.strip():
                print(ascii_art)
            else:
                # Use random preset art if generation fails
                print(ASCIIArt.get_random_scene())
        except Exception:
            print(ASCIIArt.get_random_scene())

        print("\n" + "=" * 60)
        print(scene_text)
        print("=" * 60)

    def get_player_action(self) -> str:
        """Get the player's action input."""
        while True:
            try:
                action = input("\n➤ What do you do?: ").strip()
                if action:
                    return action
                else:
                    print("Please describe an action.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted by player.")
                sys.exit(0)

    def check_game_over(self) -> bool:
        """Check if the game should end."""
        if self.game_state["health"] <= 0:
            print("\n💀 Your health has reached zero. You succumb to the darkness...\n")
            return True
        if self.game_state["sanity"] <= 0:
            print("\n👻 Your mind shatters. You've gone completely insane...\n")
            return True
        return False

    def play(self):
        """Main game loop."""
        try:
            # Show briefing first
            self.display_briefing()
            self.display_opening_scene()
            
            print("\n[Generating scene...]\n")
            time.sleep(1)

            # Initialize the game
            opening = self.story_generator.initialize_game()
            self.game_state["turn"] = 1

            while True:
                # Display current scene
                self.display_scene(opening)
                self.display_stats()

                # Check for game over conditions
                if self.check_game_over():
                    break

                # Get player action
                action = self.get_player_action()
                self.game_state["actions"].append(action)
                self.game_state["turn"] += 1

                # Generate next story beat
                print("\n[The story unfolds...]\n")
                time.sleep(1)
                opening = self.story_generator.process_action(action)

                # Update game state based on actions
                self.update_game_state()

                # Give a moment for dramatic effect
                time.sleep(0.5)

        except KeyboardInterrupt:
            print("\n\nGame interrupted by player.")
        except Exception as e:
            print(f"\nError during gameplay: {e}")
            print("Check your API key and try again.")

    def display_end_stats(self):
        """Display final game statistics."""
        print("\n" + "=" * 60)
        print("FINAL STATISTICS")
        print("=" * 60)
        print(f"Final Health: {self.game_state['health']}/100")
        print(f"Final Sanity: {self.game_state['sanity']}/100")
        print(f"Total Turns: {self.game_state['turn']}")
        print(f"\nYour Actions:")
        for i, action in enumerate(self.game_state["actions"], 1):
            print(f"  {i}. {action}")
        print("=" * 60)

    def start(self):
        """Start the game."""
        self.display_header()
        print("\n  Welcome to Mansion of Shadows!")
        print("  An AI-Generated Horror Adventure\n")
        print("  In this game, YOU shape the story through your choices.")
        print("  The AI will respond to your actions and create a unique")
        print("  narrative tailored to your decisions.\n")
        print("  Be careful—your choices affect your health and sanity.\n")

        input("  Press Enter to begin your nightmare...\n")

        self.play()
        self.display_end_stats()

        # Ask to play again
        print("\n" + "=" * 60)
        while True:
            response = input("Play again? (yes/no): ").strip().lower()
            if response in ["yes", "y"]:
                self.__init__()  # Reset game
                self.play()
                self.display_end_stats()
            elif response in ["no", "n"]:
                print("\nThanks for playing Mansion of Shadows!")
                print("Sleep well... if you can.\n")
                break
            else:
                print("Please enter 'yes' or 'no'.")


def main():
    """Entry point for the game."""
    print("""
╔════════════════════════════════════════════════════════════╗
║         🏚️  MANSION OF SHADOWS SETUP  🏚️                ║
╚════════════════════════════════════════════════════════════╝
""")

    print("Choose your AI provider:")
    print("1. OpenAI (GPT-3.5/GPT-4)")
    print("2. Claude (Anthropic)")
    print("3. Change stored API key")

    choice = input("\nEnter choice (1, 2, or 3): ").strip()

    if choice == "1":
        provider = "openai"
    elif choice == "2":
        provider = "claude"
    elif choice == "3":
        print("\nWhich provider's key do you want to change?")
        print("1. OpenAI")
        print("2. Claude")
        reset_choice = input("\nEnter choice (1 or 2): ").strip()
        provider = "openai" if reset_choice == "1" else "claude"
        api_key = ConfigManager.reset_api_key(provider)
        print("\nAPI key updated! Run the game again to play.")
        return
    else:
        print("Invalid choice. Defaulting to OpenAI.")
        provider = "openai"

    try:
        api_key = ConfigManager.get_or_prompt_api_key(provider)
        game = AIGame(ai_provider=provider, api_key=api_key)
        game.start()
    except ValueError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
