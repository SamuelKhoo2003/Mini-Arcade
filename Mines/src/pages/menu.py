from components import button, basestate
import utils

class MainMenu(basestate.BaseState):
    """Represents the main menu of the game, where the player can choose to start or quit."""
    def __init__(self):
        """Initializes the main menu state.

        Attributes:
            buttons (tuple): A collection of buttons for menu navigation.
        """
        super().__init__()
        self.buttons = (
            button.Button((self.window_size[0] // 2, 90), "PLAY", size=utils.BIG_BUTTON_SIZE),
            button.Button((self.window_size[0] // 2, 220), "QUIT")
        )

    def on_button_click(self, clicked_button):
        """Handles button clicks in the main menu.

        Args:
            clicked_button (Button): The button that was clicked.
        """
        if clicked_button.label == "QUIT":
            self.exit_game = True
        elif clicked_button.label == "PLAY":
            self.next_state = "NewGameMenu"
            self.shared_data.update({
                "width": 20,
                "height": 20,
                "total_mines": 30
            })

class NewGameMenu(basestate.BaseState):
    """Represents the new game menu, allowing players to select different game modes."""
    def __init__(self):
        """Initializes the new game menu state.

        Attributes:
            buttons (tuple): A collection of buttons for different difficulty levels.
        """
        super().__init__()
        self.buttons = (
            button.Button((self.window_size[0] // 2, 20), "EASY"),
            button.Button((self.window_size[0] // 2, 70), "MEDIUM"),
            button.Button((self.window_size[0] // 2, 120), "HARD"),
            button.Button((self.window_size[0] // 2, 170), "CUSTOM"),
            button.Button((self.window_size[0] // 2, 245), "BACK")
        )

    def on_button_click(self, clicked_button):
        """Handles button clicks in the new game menu.

        Args:
            clicked_button (Button): The button that was clicked.
        """
        if clicked_button.label == "BACK":
            self.next_state = "MainMenu"
        elif clicked_button.label == "CUSTOM":
            self.next_state = "Custom"
        else:
            self.next_state = "GameEngine"
            game_settings = {
                "EASY": (9, 9, 10, (500, 325)),
                "MEDIUM": (16, 16, 40, (650, 382)),
                "HARD": (30, 16, 99, (950, 382))
            }
            if clicked_button.label in game_settings:
                width, height, n_mines, window_size = game_settings[clicked_button.label]
                self.shared_data.update({
                    "width": width,
                    "height": height,
                    "total_mines": n_mines,
                    "window_size": window_size,
                })
