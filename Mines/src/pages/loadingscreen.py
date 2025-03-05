import pygame as pg
from components import box, basestate
import utils

class LoadingScreen(basestate.BaseState):
    """State that represents the loading screen before the game starts."""

    def __init__(self):
        """Initializes the loading screen state.

        Attributes:
            next_state (str): The name of the next game state.
            continue_textbox (box.Box): A UI element displaying the start prompt.
        """
        super().__init__()
        self.next_state = "MainMenu"
        self.game_name_textbox = box.Box(
            (220, 50),
            (self.window_size[0] // 2,
            self.window_size[1] // 2 - 25),
            text="MineMaster",
            font=utils.BIG_FONT,
            center_x=True,
            center_y=True
        )
        self.continue_textbox = box.Box(
            (230, 25),
            (self.window_size[0] // 2, self.window_size[1] - 50),
            text="Click or press any key to start!",
            font=utils.SMALL_FONT,
            center_x=True,
            center_y=True
        )

    def enter(self, current_state, shared_data, surface):
        """Handles setup when entering the loading screen state.

        Args:
            current_state (str): The current state before transitioning.
            shared_data (dict): Shared data between states.
            surface (pygame.Surface): The game screen where elements are drawn.
        """
        super().enter(current_state, shared_data, surface)
        if "has_seen_loading" not in shared_data:
            shared_data["has_seen_loading"] = True
        surface.blit(utils.LOADINGSCREEN_IMAGE, (0, 0))
        self.continue_textbox.draw(surface)
        self.game_name_textbox.draw(surface)

    def handle_events(self, events):
        """Processes user input events on the loading screen.

        Args:
            events (list): A list of pygame events (e.g., mouse clicks, key presses).
        """
        for event in events:
            if event.type in (pg.MOUSEBUTTONDOWN, pg.KEYDOWN):
                self.is_done = True
