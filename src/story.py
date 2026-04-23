"""Story and scenario management for the CYOA game."""

from typing import Dict, List, Optional, Any
from enum import Enum


class GameEnding(Enum):
    """Possible game endings."""
    SURVIVED = "survived"
    DEAD = "dead"
    POSSESSED = "possessed"
    ESCAPED = "escaped"
    TRAPPED = "trapped"
    TRANSFORMED = "transformed"


class Scenario:
    """Represents a game scenario with text, choices, and ASCII art."""

    def __init__(
        self,
        scene_id: str,
        title: str,
        description: str,
        ascii_art: str,
        choices: List[Dict[str, Any]],
        is_ending: bool = False,
        ending_type: Optional[GameEnding] = None,
    ):
        self.scene_id = scene_id
        self.title = title
        self.description = description
        self.ascii_art = ascii_art
        self.choices = choices
        self.is_ending = is_ending
        self.ending_type = ending_type

    def display(self) -> str:
        """Get the display text for this scenario."""
        output = f"\n{'=' * 60}\n"
        output += f"  {self.title}\n"
        output += f"{'=' * 60}\n"
        output += f"\n{self.ascii_art}\n"
        output += f"\n{self.description}\n"
        return output

    def get_choices_text(self) -> str:
        """Get the formatted choice text."""
        output = "\n"
        for i, choice in enumerate(self.choices, 1):
            output += f"  {i}. {choice['text']}\n"
        return output


class StoryManager:
    """Manages the branching story and game state."""

    def __init__(self):
        self.scenarios = self._build_story()
        self.current_scenario_id = "start"
        self.game_state = {
            "visited_locations": set(),
            "inventory": [],
            "health": 100,
            "sanity": 100,
            "choices_made": [],
        }
        self.story = Story()

    def _build_story(self) -> Dict[str, Scenario]:
        """Build the complete story tree."""
        scenarios = {}

        # START - The Mansion Gate
        scenarios["start"] = Scenario(
            scene_id="start",
            title="The Abandoned Mansion",
            description="""You pull up to the old Victorian mansion at midnight. The wrought iron gates creak
as the wind pushes them open. Your car's headlights illuminate the decrepit structure before you.
Local teenagers had dared you to spend one night here. You thought it was just an old house.

But as you step out of your car, you feel it—a strange chill, despite the warm autumn air.
The mansion looms before you, its windows like hollow eyes staring into the darkness.

What do you do?""",
            ascii_art="""
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
            choices=[
                {
                    "text": "Enter through the front door",
                    "next_scene": "front_door",
                    "health_change": 0,
                    "sanity_change": -5,
                },
                {
                    "text": "Try to find a back entrance",
                    "next_scene": "back_garden",
                    "health_change": 0,
                    "sanity_change": -3,
                },
                {
                    "text": "Search the grounds for clues first",
                    "next_scene": "grounds",
                    "health_change": 0,
                    "sanity_change": 0,
                },
            ],
        )

        # Front Door Path
        scenarios["front_door"] = Scenario(
            scene_id="front_door",
            title="The Grand Entrance",
            description="""You push the heavy oak door. It creaks open with surprising ease. A musty smell hits
your nostrils—decades of decay and abandonment. Your phone's flashlight illuminates a grand foyer.
Dust particles dance through the beam. Ancient furniture sits covered in white sheets.

Then you hear it. A soft scratching sound coming from deeper within the house. It stops.
The silence that follows is somehow worse than the noise.

Suddenly, the door behind you slams shut. You're locked inside.""",
            ascii_art="""
        ___________
       |           |
       |  WELCOME  |
       |___________|
       |    /|\\    |
       |   / | \\   |
       |  /  |  \\  |
       | /___|___\\ |
       |  [LOCK]   |
       |___________|
""",
            choices=[
                {
                    "text": "Try to open the door again (sanity check)",
                    "next_scene": "locked_out",
                    "health_change": 0,
                    "sanity_change": -10,
                },
                {
                    "text": "Explore the foyer",
                    "next_scene": "foyer",
                    "health_change": 0,
                    "sanity_change": -5,
                },
                {
                    "text": "Search for another exit",
                    "next_scene": "hallway",
                    "health_change": 0,
                    "sanity_change": -7,
                },
            ],
        )

        # Foyer
        scenarios["foyer"] = Scenario(
            scene_id="foyer",
            title="The Foyer's Secrets",
            description="""You shine your light around the foyer. A grand staircase dominates the room,
spiraling up into darkness. Portraits line the walls—their painted eyes following your every move.

You notice something strange: fresh flowers in a vase on the table. Impossible. No one has lived
here in years. The flowers are perfectly arranged, and they're still wet.

Someone... or something... has been here very recently.

A cold breath touches your neck. When you spin around, there's nothing there.""",
            ascii_art="""
   _______________
  |   PORTRAITS   |
  |_______________|
  | O o  o  o O  |
  |    ___        |
  |   /   \\       |
  |  | 👀 |      |
  |   \\___/       |
  |               |
  |  [FLOWERS]    |
  |_______________|
""",
            choices=[
                {
                    "text": "Pick up the flowers",
                    "next_scene": "flowers_choice",
                    "health_change": 0,
                    "sanity_change": -8,
                },
                {
                    "text": "Climb the staircase",
                    "next_scene": "upstairs",
                    "health_change": 0,
                    "sanity_change": -10,
                },
                {
                    "text": "Check the portraits more closely",
                    "next_scene": "portraits",
                    "health_change": 0,
                    "sanity_change": -15,
                },
            ],
        )

        # Back Garden Path
        scenarios["back_garden"] = Scenario(
            scene_id="back_garden",
            title="The Overgrown Garden",
            description="""You make your way around the mansion to the back. The garden is a tangled mess
of dead plants and broken statuary. Somewhere in the darkness, you hear water trickling.

There's a cellar door—old and rusted. Next to it, a garden shed with a broken window.
Both doors are unlocked. The cellar door descends into absolute blackness.""",
            ascii_art="""
     ^   ^   ^
    / \\ / \\ / \\
   ^   ^   ^   ^
  / \\ / \\ / \\ / \\
 /   ^   ^   ^   \\
|    / \\ / \\ / \\   |
|   ^  [SHED] ^   |
|  / \\ / \\ / \\ / \\ |
 \\ / [CELLAR] \\ /
  X    ◯     X
 / \\    ↓   / \\
""",
            choices=[
                {
                    "text": "Open the cellar door",
                    "next_scene": "cellar",
                    "health_change": -10,
                    "sanity_change": -20,
                },
                {
                    "text": "Check the garden shed",
                    "next_scene": "shed",
                    "health_change": 0,
                    "sanity_change": -5,
                },
                {
                    "text": "Continue exploring the grounds",
                    "next_scene": "grounds",
                    "health_change": 0,
                    "sanity_change": -3,
                },
            ],
        )

        # Grounds
        scenarios["grounds"] = Scenario(
            scene_id="grounds",
            title="The Grounds",
            description="""You wander the overgrown grounds. Everything is overgrown and neglected. 
You discover an old graveyard off to one side, stones worn by time. Names are barely readable.

Wait. One grave is freshly dug. The earth is still moist. A shovel rests nearby.

You feel watched. The hairs on your neck stand on end.""",
            ascii_art="""
    _____       _____
   /     \\     /     \\
  | R.I.P |   | R.I.P |
   \\_____/     \\_____/
    _____       _____
   /     \\     /     \\
  | R.I.P |   | ???? |
   \\_____/     \\_____/
  
   ~~ fog drifts ~~
   ~~~~~~~~~~~~~~~
""",
            choices=[
                {
                    "text": "Investigate the fresh grave",
                    "next_scene": "grave",
                    "health_change": 0,
                    "sanity_change": -25,
                },
                {
                    "text": "Head back to the mansion",
                    "next_scene": "front_door",
                    "health_change": 0,
                    "sanity_change": -5,
                },
                {
                    "text": "Run away from the grounds",
                    "next_scene": "escape_attempt",
                    "health_change": 0,
                    "sanity_change": -15,
                },
            ],
        )

        # ENDINGS

        # Bad Ending - Locked Out
        scenarios["locked_out"] = Scenario(
            scene_id="locked_out",
            title="TRAPPED",
            description="""You struggle with the door handle, but it won't budge. Your panic grows as
you realize the door is truly locked—from the outside.

Behind you, you hear slow, deliberate footsteps descending the grand staircase.
The steps are uneven... dragging. Something is coming down.

You spin around and see a figure materializing from the shadows. It's vaguely human-shaped,
but something is terribly wrong. Its head tilts at an impossible angle.

You scream as it reaches toward you...

═══════════════════════════════════════════════════════════
YOU ARE TRAPPED. YOUR STORY ENDS HERE.
═══════════════════════════════════════════════════════════""",
            ascii_art="""
  ~~~~~~~~~~~~~~~~~~~
  ~  ~ ~~~~ ~ ~~  ~
  ~  ~~~  ~~~  ~~~  ~
  ~ ~~  ╱╲ ╱╲ ╲╱  ~ ~
  ~~~  ╱  ╲╱  ╲╱  ╲~~~
  ~~  ╱  👁╲  👁╱  👁╲~~ 
  ~~~~~~~~~~~~~~~~~~~~~~~
""",
            is_ending=True,
            ending_type=GameEnding.TRAPPED,
        )

        # Good Ending - Escape
        scenarios["escape_attempt"] = Scenario(
            scene_id="escape_attempt",
            title="THE ESCAPE",
            description="""You sprint toward your car, not daring to look back. Behind you, you hear
an inhuman shriek that freezes your blood. But you don't stop.

Your fingers fumble with the car keys. The engine roars to life. You floor the accelerator,
gravel spraying as you tear away from the mansion.

In your rearview mirror, a figure stands silhouetted against the decrepit house,
watching you leave. It makes no attempt to follow.

As dawn breaks, you wonder if anyone would ever believe what happened in that house.
More importantly, you wonder if you'll ever stop hearing that shriek in your nightmares.""",
            ascii_art="""
  _______________
  |   FREEDOM    |
  |_______________|
  |   🚗 ➡️ 🌅   |
  |               |
  |    [SAFE]     |
  |               |
  |_______________|
""",
            is_ending=True,
            ending_type=GameEnding.ESCAPED,
        )

        # Mystery Ending - Grave
        scenarios["grave"] = Scenario(
            scene_id="grave",
            title="WHAT LIES BENEATH",
            description="""You dig into the fresh grave with trembling hands. Your shovel hits something soft.
A hand. A human hand.

You uncover the body—a woman, freshly buried. She's wearing clothes from decades past,
yet her body shows no sign of decay. Her eyes snap open and lock onto yours.

"Finally," she whispers. "I've been waiting for someone like you..."

═══════════════════════════════════════════════════════════
THE TRUTH IS DARKER THAN YOU IMAGINED...
═══════════════════════════════════════════════════════════""",
            ascii_art="""
    _____
   /     \\
  | R.I.P |
   \\_____/
   
   [THE GROUND OPENS]
   
   👁️ EYES OPEN 👁️
   
   ...WAITING...
""",
            is_ending=True,
            ending_type=GameEnding.POSSESSED,
        )

        # Additional scenario for variety
        scenarios["cellar"] = Scenario(
            scene_id="cellar",
            title="THE CELLAR DEPTHS",
            description="""The cellar is ice cold. Your breath comes in visible clouds. The smell is
overwhelming—rot and rust and something else. Something ancient.

Your flashlight illuminates stone walls covered in what might be writing. Or blood.
It's hard to tell in the darkness.

At the far end of the cellar, you see a door. Not a normal door—it's covered in strange symbols
that seem to writhe in your peripheral vision.

You also notice shelves lined with jars. Jars containing... things. Unidentifiable things.""",
            ascii_art="""
   _______________
  |   LAB HAZARD  |
  |_______________|
  | ☢ ☢ ☢ ☢ ☢ ☢ |
  |               |
  | [?????]       |
  | ================
  | |EXPERIMENT   |
  | |FAILED: ████ |
  | ================
  |               |
  |_______________|
""",
            choices=[
                {
                    "text": "Open the symbol-covered door",
                    "next_scene": "void",
                    "health_change": -20,
                    "sanity_change": -50,
                },
                {
                    "text": "Leave the cellar immediately",
                    "next_scene": "back_garden",
                    "health_change": 0,
                    "sanity_change": -30,
                },
            ],
        )

        scenarios["shed"] = Scenario(
            scene_id="shed",
            title="THE GARDEN SHED",
            description="""The shed is small and cramped. Tools hang on peeling walls. But what catches
your eye is the workbench: covered in notes, diagrams, and photographs.

You pick up a journal. The handwriting is frantic:

"Subject 7 is resisting. Need stronger catalyst. The ritual must be completed by the new moon
or all previous work will be lost. The door must remain sealed. They must not find out what
we've created beneath the house..."

The journal ends abruptly in mid-sentence, the final entry smeared with what looks like blood.""",
            ascii_art="""
  ___________
 |   SHED    |
 |___________|
 | ╱╲ ╱╲ ╱╲  |
 |╱  ╲╱  ╲╱  |
 |  [NOTES] |
 | ╱╲ ╱╲ ╲╱  |
 |╱  ╲╱  ╲╱  |
 |___________|
""",
            choices=[
                {
                    "text": "Take the journal and leave",
                    "next_scene": "escape_attempt",
                    "health_change": 0,
                    "sanity_change": -40,
                },
                {
                    "text": "Search for more information in the shed",
                    "next_scene": "cellar",
                    "health_change": 0,
                    "sanity_change": -35,
                },
            ],
        )

        # Additional scenarios
        scenarios["upstairs"] = Scenario(
            scene_id="upstairs",
            title="THE SECOND FLOOR",
            description="""The staircase creaks beneath your feet. On the second floor, doors line a long
hallway. All are closed except one.

Through the open doorway, you see what appears to be a bedroom. A music box sits on a dresser,
playing a haunting melody by itself. A child's drawings cover the walls—disturbing images in
crayon of stick figures with too many limbs.""",
            ascii_art="""
  [ DOOR ] [ DOOR ] [ DOOR ]
  
  [ OPEN ]
  
   ~~~♫~~~♫~~~
   [MUSIC BOX]
   ~~~♫~~~♫~~~
""",
            choices=[
                {
                    "text": "Enter the bedroom with the music box",
                    "next_scene": "void",
                    "health_change": -15,
                    "sanity_change": -45,
                },
                {
                    "text": "Check the other rooms",
                    "next_scene": "hallway",
                    "health_change": 0,
                    "sanity_change": -20,
                },
                {
                    "text": "Go back downstairs",
                    "next_scene": "foyer",
                    "health_change": 0,
                    "sanity_change": -10,
                },
            ],
        )

        scenarios["hallway"] = Scenario(
            scene_id="hallway",
            title="THE DARK HALLWAY",
            description="""You move through a narrow hallway. Doors flash past in your flashlight beam.
The air grows colder with each step.

At the end of the hall, you see a light—warm and welcoming. It fills you with an inexplicable
sense of dread. Everything in you screams to turn back, but your feet move forward on their own.""",
            ascii_art="""
  [ DOOR ] [ DOOR ] [ DOOR ]
  
  ║ ║ ║ ║ ║ ║ ║
  ║ ║ ║ ║ ║ ║ ║
  ║ ║ ║ ║ ║ ║ ║
  ║ ║ ║ ║ ║ ║ ║
  ▼ ▼ ▼ ▼ ▼ ▼ ▼
  
  ✦ ✦ ✦ LIGHT ✦ ✦ ✦
""",
            choices=[
                {
                    "text": "Move toward the light",
                    "next_scene": "void",
                    "health_change": -25,
                    "sanity_change": -60,
                },
                {
                    "text": "Turn back and find another way",
                    "next_scene": "escape_attempt",
                    "health_change": 0,
                    "sanity_change": -20,
                },
            ],
        )

        scenarios["portraits"] = Scenario(
            scene_id="portraits",
            title="THE FAMILY PORTRAIT",
            description="""As you examine the portraits more closely, you notice something horrifying:
your own face is painted among them. In a portrait dated 1923, a figure that looks exactly like
you stares out from the canvas, dressed in old-fashioned clothes.

Below the portrait is a name: your name.

The lights flicker. When your eyes adjust, you're no longer in the foyer. You're standing in
a room you don't recognize, watching your own life play out on the walls in photographs...
except you've never taken these photographs.

You realize with dawning horror that you've been here before. Many times. Over centuries.""",
            ascii_art="""
   _______________
  |   PORTRAITS   |
  |_______________|
  | O 😱  o  O   |
  |    [YOU??]    |
  |  1923  2024   |
  |   [LOOP]      |
  |               |
  |_______________|
""",
            is_ending=True,
            ending_type=GameEnding.TRANSFORMED,
        )

        scenarios["flowers_choice"] = Scenario(
            scene_id="flowers_choice",
            title="THE BOUQUET",
            description="""You pick up the flowers. They're still warm, like they were just placed there.
A card falls from among the stems. It reads:

"For my love, forever and always. —M"

The handwriting is beautiful but unsettling. It's the same handwriting as in the journal you find later.

The flowers wilt rapidly in your hands, turning black. You drop them in horror as they crumble
to ash on the floor. 

In the ash, a message appears: "WELCOME HOME."

═══════════════════════════════════════════════════════════
YOU HAVE BEEN MARKED. YOU ARE HERS NOW.
═══════════════════════════════════════════════════════════""",
            ascii_art="""
  [FLOWERS]
    ╱ ╲
   ╱   ╲
  [BLACK]
   ╲   ╱
    ╲ ╱
   [ASH]
   
  "WELCOME HOME"
""",
            is_ending=True,
            ending_type=GameEnding.POSSESSED,
        )

        scenarios["void"] = Scenario(
            scene_id="void",
            title="THE VOID",
            description="""Everything goes black. Not the darkness of night, but the absolute absence of
light and existence. You float in nothingness for what feels like eternity.

Gradually, you become aware of presences around you. Shadows of other people. Countless others.
All trapped in this same void. All waiting.

A voice speaks directly into your mind: "Welcome. You are ours now. The mansion collects
interesting souls. You will stay until it finds a replacement."

The collected souls reach for you as you're pulled deeper into the void.

═══════════════════════════════════════════════════════════
GAME OVER. YOU HAVE JOINED THE HOUSE'S COLLECTION.
═══════════════════════════════════════════════════════════""",
            ascii_art="""
    ╔═══════════════╗
    ║               ║
    ║       👻      ║
    ║      👻 👻     ║
    ║     👻   👻    ║
    ║    👻     👻   ║
    ║               ║
    ║    ENDLESS    ║
    ║     VOID      ║
    ╚═══════════════╝
""",
            is_ending=True,
            ending_type=GameEnding.DEAD,
        )

        return scenarios

    def get_current_scenario(self) -> Scenario:
        """Get the current scenario."""
        return self.scenarios[self.current_scenario_id]

    def make_choice(self, choice_index: int) -> bool:
        """Make a choice and update the game state. Returns True if game continues."""
        current = self.get_current_scenario()

        if choice_index < 1 or choice_index > len(current.choices):
            return None

        choice = current.choices[choice_index - 1]
        next_scene = choice.get("next_scene")

        # Update game state
        self.game_state["health"] += choice.get("health_change", 0)
        self.game_state["sanity"] += choice.get("sanity_change", 0)
        self.game_state["choices_made"].append(choice["text"])
        self.game_state["visited_locations"].add(self.current_scenario_id)

        # Clamp values
        self.game_state["health"] = max(0, min(100, self.game_state["health"]))
        self.game_state["sanity"] = max(0, min(100, self.game_state["sanity"]))

        # Move to next scene
        if next_scene in self.scenarios:
            self.current_scenario_id = next_scene
            return True

        return False

    def is_game_over(self) -> bool:
        """Check if the game has ended."""
        current = self.get_current_scenario()
        return current.is_ending

    def get_ending_type(self) -> Optional[GameEnding]:
        """Get the current ending type if game is over."""
        current = self.get_current_scenario()
        return current.ending_type if current.is_ending else None


class Story:
    def __init__(self):
        self.killer_encounter_turns = 0
        self.killer_injured = False

    def encounter_killer(self):
        """Track the killer encounter and increment turns."""
        self.killer_encounter_turns += 1

    def injure_killer(self):
        """Mark the killer as injured."""
        self.killer_injured = True

    def reset_killer_encounter(self):
        """Reset killer encounter tracking."""
        self.killer_encounter_turns = 0
        self.killer_injured = False
