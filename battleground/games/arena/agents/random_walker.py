from battleground.agent import Agent
import random


class ArenaAgent(Agent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, state):
        """
        This method is written such that this agent can also play the bunnies
        game and the basic games.
        :param state: state of the game
        :return: dict of chosen move
        """
        move = {}

        if state is not None:
            if "move_options" in state:
                options = state["move_options"]
                if isinstance(options, list):
                    options = random.choice(options)
                if "type" in options:
                    move["type"] = options["type"]
                else:
                    move["type"] = options

                has_tools = False
                if isinstance(options, dict) and "tools" in options:
                    options = random.choice(options["tools"])
                    has_tools = True
                if isinstance(options, dict) and "tool" in options:
                    move["tool"] = options["tool"]
                elif has_tools:
                    move["tool"] = options

                has_targets = False
                if isinstance(options, dict) and "targets" in options:
                    options = random.choice(options["targets"])
                    has_targets = True
                if isinstance(options, dict) and "target" in options:
                    move["target"] = options["target"]
                elif has_targets:
                    move["target"] = options

                has_values = False
                if isinstance(options, dict) and "values" in options:
                    options = random.choice(options["values"])
                    has_values = True
                if isinstance(options, dict) and "value" in options:
                    move["value"] = move["value"]
                elif has_values:
                    move["value"] = options

            else:
                # default values
                move["type"] = "stay"
                move["tool"] = None
                move["target"] = None
                move["value"] = 1
                print("Agent is taking default values.")

        return move
