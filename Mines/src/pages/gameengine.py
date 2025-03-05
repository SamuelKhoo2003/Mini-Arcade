import utils
from components import basestate, minefield, button, box
import time

class GameEngine(basestate.BaseState):
    """
    Manages the game state where the player interacts with the minefield.
    This includes handling game logic, rendering, and user input.
    """

    def __init__(self):
        """
        Initializes the game engine, setting up essential variables like the minefield,
        buttons, borders, and timer.
        """
        super().__init__()
        self.minefield = None
        self.minefield_rect = None
        self.result_displayed = False
        self.buttons = None
        self.border = None

        # Timer attributes
        self.timer_box = None
        self.start_time = None
        self.elapsed_time = 0
        self.win_loss_announced = False

    def enter(self, current_state, shared_data, surface):
        """
        Sets up the game state when entering, initializing the minefield,
        buttons, and display elements.

        Args:
            current_state (str): Name of the current state.
            shared_data (dict): Data shared from the previous state, including board size and mine count.
            surface (pygame.Surface): The main game window surface.
        """
        super().enter(current_state, shared_data, surface)
        self.minefield = minefield.Minefield(shared_data["width"], shared_data["height"], shared_data["total_mines"])
        self.minefield.position = (20, 20)
        self.minefield_rect = self.minefield.surface.get_rect(topleft=self.minefield.position)

        self.buttons = (
            button.Button((self.window_size[0] - 135, 220), "RESTART GAME", size=utils.WIDE_BUTTON_SIZE),
            button.Button((self.window_size[0] - 135, 180), "MAIN MENU", size=utils.WIDE_BUTTON_SIZE),
            button.Button((self.window_size[0] - 130, 260), "QUIT")
        )
        self.border = box.Box((self.minefield_rect.width + utils.TILE_SIZE, self.minefield_rect.height + utils.TILE_SIZE),
                              (self.minefield_rect.topleft[0] - utils.TILE_SIZE // 2, self.minefield_rect.topleft[1] - utils.TILE_SIZE // 2))

        # Display boxes for mines remaining and timer
        self.mines_remaining_box = box.Box((240, 35), (self.window_size[0] - 260, 20),
                                           text="Flags Remaining: {}".format(self.minefield.remaining_mines))
        self.timer_box = box.Box((180, 35), (self.window_size[0] - 230, 60), text="Time: 00:00.000")
        self.start_time = time.time()

    def update(self, delta_time):
        """
        Updates the game logic, handling user input and updating the timer.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        super().update(delta_time)

        if self.minefield_rect.collidepoint(self.mouse_position):
            self.minefield.update(self.mouse_position, self.left_click, self.right_click)

        # Update mines remaining display
        if self.minefield.remaining_mines_updated:
            self.minefield.remaining_mines_updated = False
            self.mines_remaining_box.update("Flags Remaining: {}".format(self.minefield.remaining_mines))

        # Update timer display
        if self.minefield.initial_click and not self.minefield.game_over:
            self.elapsed_time = time.time() - self.start_time
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            milliseconds = int((self.elapsed_time * 100) % 100)
            self.timer_box.update(f"Time: {minutes:02}:{seconds:02}:{milliseconds:02}")

    def on_button_click(self, clicked_button):
        """
        Handles button click events.

        Args:
            clicked_button (Button): The button that was clicked.
        """
        if clicked_button.label == "RESTART GAME":
            self.next_state = "GameEngine"
        elif clicked_button.label == "MAIN MENU":
            self.next_state = "MainMenu"
        elif clicked_button.label == "QUIT":
            self.exit_game = True

    def draw(self, surface):
        """
        Renders the game elements on the screen, including the minefield, UI elements, and buttons.

        Args:
            surface (pygame.Surface): The surface to render elements on.
        """
        super().draw(surface)
        self.border.draw(surface)
        self.minefield.draw(surface)
        self.mines_remaining_box.draw(surface)
        self.timer_box.draw(surface)
        # Display win/loss message if the game is over
        if self.minefield.game_over and not self.win_loss_announced:
            results_textbox = box.Box((180, 35), (self.window_size[0] - 230, 100), text=self.minefield.result_message)
            results_textbox.draw(surface)
