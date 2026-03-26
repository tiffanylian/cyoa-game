"""ASCII Art generator for horror scenarios."""

import random


class ASCIIArt:
    """Generate ASCII art for various horror scenarios."""

    # Scenario art templates
    SCENES = {
        "haunted_house": """
    |‾‾‾‾‾‾‾‾‾‾‾‾|
    |   MANSION   |
    |_____________|
    |\\ | | | | / |
    | \\| | | |/ |
    |==============|
    | ~~ o ~~  o  |
    |  ~ o ~ ~~   |
    |_____________|
    |      []     |
    |  ___/  \\    |
        """,
        "dark_forest": """
     ^   ^   ^
    / \\ / \\ / \\
   ^   ^   ^   ^
  / \\ / \\ / \\ / \\
 /   ^   ^   ^   \\
|    / \\ / \\ / \\   |
|   ^   ^   ^   ^  |
|  / \\ / \\ / \\ / \\ |
 \\ /   /   \\   \\ /
  X   X     X   X
 / \\       / \\
        """,
        "abandoned_lab": """
   _______________
  |   LAB HAZARD  |
  |_______________|
  | ☢ ☢ ☢ ☢ ☢ ☢ |
  |               |
  | [CHAMBER 1]   |
  | ================
  | |EXPERIMENT   |
  | |FAILED: ████ |
  | ================
  |               |
  |_______________|
        """,
        "graveyard": """
    _____       _____
   /     \\     /     \\
  | R.I.P |   | R.I.P |
   \\_____/     \\_____/
    _____       _____
   /     \\     /     \\
  | R.I.P |   | R.I.P |
   \\_____/     \\_____/
  
   ~~ fog drifts ~~
   ~~~~~~~~~~~~~~~
        """,
        "creature": """
     ^^--^^
    /      \\
   | O  O  |
   |  <>   |
    \\ ||_ /
    //||\\\\
   (  ||  )
       ||
       ||
      /||\\
        """,
        "shadows": """
  ~~~~~~~~~~~~~~~~~~~
  ~  ~ ~~~~ ~ ~ ~~  ~
  ~  ~~~  ~~~  ~~~  ~
  ~ ~~ ╱╲ ╱╲ ╱╲ ~~ ~
  ~~~╱  ╲╱  ╲╱  ╲~~~
  ~~╱  ?╲  ?╱  ?╲~~ 
  ~~~~~~~~~~~~~~~~~~~~~~~
        """,
        "blood_door": """
        ___________
       |           |
       | [DOOR]    |
       |___________|
       |           |
       |   ◇ ◇     |
       |  ◇ ◇ ◇    |
       | ◇ ◇ ◇ ◇   |
       |◇ ◇ ◇ ◇ ◇  |
       |▓▓▓▓▓▓▓▓▓▓|
       |___________|
        """,
        "void": """
    ╔═══════════════╗
    ║               ║
    ║               ║
    ║      ...      ║
    ║               ║
    ║    ENDLESS    ║
    ║     VOID      ║
    ║               ║
    ║               ║
    ╚═══════════════╝
        """,
    }

    @staticmethod
    def get_scene(scene_name: str) -> str:
        """Get ASCII art for a specific scene."""
        return ASCIIArt.SCENES.get(scene_name, ASCIIArt.SCENES["void"])

    @staticmethod
    def get_random_scene() -> str:
        """Get a random horror scene."""
        return random.choice(list(ASCIIArt.SCENES.values()))

    @staticmethod
    def display_with_effect(scene: str, effect: str = "normal") -> str:
        """Display scene with visual effects."""
        if effect == "glitch":
            # Add glitch effect
            lines = scene.split("\n")
            glitched = []
            for line in lines:
                if random.random() > 0.7:
                    glitched.append("█" * len(line))
                else:
                    glitched.append(line)
            return "\n".join(glitched)
        elif effect == "fade":
            # Add fade effect
            lines = scene.split("\n")
            faded = []
            for i, line in enumerate(lines):
                if i % 2 == 0:
                    faded.append("░" + line[1:-1] + "░")
                else:
                    faded.append(line)
            return "\n".join(faded)
        return scene

    @staticmethod
    def transition(old_scene: str, new_scene: str, duration: int = 5) -> str:
        """Create a transition effect between scenes."""
        transition_frames = [
            "[ ████░░░░░░░░░░░░░░░░░ ]",
            "[ ██████░░░░░░░░░░░░░░░░ ]",
            "[ ████████░░░░░░░░░░░░░░ ]",
            "[ ██████████░░░░░░░░░░░░ ]",
            "[ ████████████░░░░░░░░░░ ]",
        ]
        return "\n".join(transition_frames)
