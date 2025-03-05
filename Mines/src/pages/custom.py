import pygame as pg
from components import button, basestate, box
import utils

class Custom(basestate.BaseState):
    """
    Represents the custom menu of the game, where the player can modify board requirements
    such as the number of mines and the board size.
    """

    def __init__(self):
        """
        Initializes the Custom state, setting up buttons, input fields, and title.
        """
        super().__init__()
        self.buttons = (
            button.Button((self.window_size[0] // 2, 180), "PLAY", size=utils.BIG_BUTTON_SIZE),
            button.Button((self.window_size[0] // 2, 245), "BACK")
        )
        self.play_button = self.buttons[0]
        self.title = "Customise your game!"
        self.title_box = box.Box((280, 35), (self.window_size[0] // 2, 20), self.title, center_x=True)

        self.input_texts = {"width": "width", "height": "height", "mines": "mines"}
        self.input_boxes = {
            "width": box.Box((80, 35), (self.window_size[0] * 0.2, 110), self.input_texts["width"], tiles=utils.spritesheets["textbox"], center_x=True),
            "height": box.Box((80, 35), (self.window_size[0] * 0.5, 110), self.input_texts["height"], tiles=utils.spritesheets["textbox"], center_x=True),
            "mines":  box.Box((80, 35), (self.window_size[0] * 0.8, 110), self.input_texts["mines"], tiles=utils.spritesheets["textbox"], center_x=True),
        }

        self.active_input_box = None
        self.textcursor = "|"

        # Board constraints
        self.min_side_length = 5
        self.max_side_length = 100
        self.min_mines = 1

    def update(self, delta_time):
        """
        Updates the state, handling user input for modifying board parameters.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        super().update(delta_time)

        # Handle mouse clicks for selecting input fields
        if self.left_click:
            self.active_input_box = None
            for input_box_name, input_box in self.input_boxes.items():
                if input_box.rect.collidepoint(self.mouse_position):
                    self.active_input_box = input_box_name
                    if self.input_texts[input_box_name][-1] != self.textcursor:
                        self.input_texts[input_box_name] += self.textcursor
                else:
                    self.input_texts[input_box_name] = self.input_texts[input_box_name].replace(self.textcursor, "")

        # Handle keyboard input for modifying the values
        if self.pressed_keys and self.active_input_box is not None:
            text = self.input_texts[self.active_input_box].replace(self.textcursor, "")
            for event in self.pressed_keys:
                if event.unicode.isdigit():
                    if len(text) < 3:
                        text += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    text = text[:-1]
            self.input_texts[self.active_input_box] = text + self.textcursor

        # Ensure input fields only contain valid values
        for key, text in self.input_texts.items():
            if text != key:
                if not text:
                    text = key
                else:
                    text = text.replace(key, "")
            self.input_texts[key] = text

        # Update input box display values
        for input_box_name, input_box in self.input_boxes.items():
            input_box.update(self.input_texts[input_box_name])

        self.check_input()

    def check_input(self):
        """
        Validates input values and enables or disables the play button accordingly.
        """
        try:
            width = int(self.input_texts["width"].replace(self.textcursor, ""))
            height = int(self.input_texts["height"].replace(self.textcursor, ""))
            mines = int(self.input_texts["mines"].replace(self.textcursor, ""))
        except ValueError:
            self.play_button.is_locked = True
            return

        if (self.min_side_length <= width <= self.max_side_length and
            self.min_side_length <= height <= self.max_side_length and
            self.min_mines <= mines < (width * height) // 3):
            self.play_button.is_locked = False
            window_size = (max(550, width * 40), max(325, height * 25))
            self.shared_data.update({"width": width, "height": height, "total_mines": mines, "window_size": window_size})
        else:
            self.play_button.is_locked = True

    def on_button_click(self, clicked_button):
        """
        Handles button click actions.

        Args:
            clicked_button (Button): The button that was clicked.
        """
        if clicked_button.label == "PLAY":
            self.next_state = "GameEngine"
        elif clicked_button.label == "BACK":
            self.next_state = "MainMenu"

    def draw(self, surface):
        """
        Renders the Custom state, including buttons and input fields.

        Args:
            surface (pygame.Surface): The surface on which to draw.
        """
        super().draw(surface)
        self.title_box.draw(surface)
        for input_box in self.input_boxes.values():
            input_box.draw(surface)