"""Main game engine for the CYOA horror game."""

import sys
import time
import os
from typing import Optional
from story import StoryManager, GameEnding
from ascii_art import ASCIIArt


class Game:
    """Main game controller."""

    def __init__(self):
        self.story_manager = StoryManager()
        self.running = True

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system("clear" if os.name == "posix" else "cls")

    def display_header(self):
        """Display the game header."""
        header = """
╔════════════════════════════════════════════════════════════╗
║         🏚️  MANSION OF SHADOWS  🏚️                      ║
║                                                            ║
║              A Choose Your Own Adventure                  ║
║                    Horror Game                            ║
╚════════════════════════════════════════════════════════════╝
"""
        print(header)

    def display_stats(self):
        """Display current game stats."""
        health = self.story_manager.game_state["health"]
        sanity = self.story_manager.game_state["sanity"]

        health_bar = self._create_bar(health)
        sanity_bar = self._create_bar(sanity)

        stats = f"""
╔════════════════════════════════════════════════════════════╗
║ Health: {health_bar} {health}%
║ Sanity: {sanity_bar} {sanity}%
╚════════════════════════════════════════════════════════════╝
"""
        print(stats)

    def _create_bar(self, value: int, length: int = 20) -> str:
        """Create a visual bar for stats."""
        filled = int((value / 100) * length)
        empty = length - filled
        return "█" * filled + "░" * empty

    def display_scenario(self):
        """Display the current scenario."""
        scenario = self.story_manager.get_current_scenario()
        self.clear_screen()
        self.display_header()
        self.display_stats()
        print(scenario.display())
        if not scenario.is_ending:
            print(scenario.get_choices_text())

    def get_player_choice(self) -> Optional[int]:
        """Get the player's choice input."""
        scenario = self.story_manager.get_current_scenario()
        num_choices = len(scenario.choices)

        while True:
            try:
                choice_input = input(f"\n➤ Enter your choice (1-{num_choices}): ").strip()
                choice = int(choice_input)

                if 1 <= choice <= num_choices:
                    return choice
                else:
                    print(f"Please enter a number between 1 and {num_choices}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted by player.")
                sys.exit(0)

    def handle_ending(self):
        """Handle game ending."""
        ending = self.story_manager.get_ending_type()

        ending_messages = {
            GameEnding.SURVIVED: "\n✓ You survived... but at what cost?",
            GameEnding.DEAD: "\n✗ You are dead.",
            GameEnding.POSSESSED: "\n✗ You have been possessed.",
            GameEnding.ESCAPED: "\n✓ You have escaped!",
            GameEnding.TRAPPED: "\n✗ You are trapped forever.",
            GameEnding.TRANSFORMED: "\n✗ You have been transformed.",
        }

        message = ending_messages.get(ending, "\n...The end.")
        print(message)

    def play(self):
        """Main game loop."""
        self.display_scenario()

        while not self.story_manager.is_game_over():
            choice = self.get_player_choice()

            if choice is None:
                continue

            # Make the choice and transition to next scene
            self.story_manager.make_choice(choice)

            # Brief pause for effect
            time.sleep(0.5)

            # Display the next scenario
            self.display_scenario()

        # Game has ended
        time.sleep(1)
        self.handle_ending()
        self.display_end_stats()

    def display_end_stats(self):
        """Display final game statistics."""
        stats = self.story_manager.game_state
        print("\n" + "=" * 60)
        print("FINAL STATISTICS")
        print("=" * 60)
        print(f"Final Health: {stats['health']}/100")
        print(f"Final Sanity: {stats['sanity']}/100")
        print(f"Locations Visited: {len(stats['visited_locations'])}")
        print(f"Total Choices Made: {len(stats['choices_made'])}")
        print("\nChoices:")
        for i, choice in enumerate(stats["choices_made"], 1):
            print(f"  {i}. {choice}")
        print("=" * 60)

    def start(self):
        """Start the game."""
        self.display_header()
        print("\nWelcome to Mansion of Shadows!\n")
        print("This is a text-based horror adventure where your choices")
        print("shape the story. Be careful—some decisions may have")
        print("consequences that affect your health and sanity.\n")

        input("Press Enter to begin your nightmare...\n")

        self.play()

        # Ask to play again
        print("\n" + "=" * 60)
        while True:
            response = input("Play again? (yes/no): ").strip().lower()
            if response in ["yes", "y"]:
                self.__init__()  # Reset game
                self.play()
            elif response in ["no", "n"]:
                print("\nThanks for playing Mansion of Shadows!")
                print("Sleep well... if you can.\n")
                break
            else:
                print("Please enter 'yes' or 'no'.")


def main():
    """Entry point for the game."""
    game = Game()
    game.start()


if __name__ == "__main__":
    main()
