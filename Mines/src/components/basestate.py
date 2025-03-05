import pygame as pg
import utils  # Handles global settings and configurations

class BaseState:
    """
    A base class for game states, handling common functionality such as event processing,
    button updates, and rendering.
    """

    def __init__(self):
        """
        Initializes base attributes for game states.
        """
        self.is_done = False         # Marks if the state is finished
        self.exit_game = False       # Indicates if the game should exit
        self.next_state = None       # The next state to transition to
        self.shared_data = {}        # Data shared between states
        self.previous_state = None   # Reference to the previous state
        self.state_id = None         # Identifier for the current state
        self.window_size = utils.STANDARD_WINDOW_SIZE
        self.left_click = False      # Tracks left mouse button clicks
        self.right_click = False     # Tracks right mouse button clicks
        self.mouse_position = (-1, -1)  # Stores the current mouse position
        self.bg_colour = utils.COLOURS["background_colour"]
        self.buttons = ()            # Tuple containing UI buttons
        self.pressed_keys = {}       # Dictionary storing pressed keys

    def enter(self, state_name, shared_data, surface):
        """
        Prepares the state when it becomes active.

        Args:
            state_name (str): Name of the current state.
            shared_data (dict): Data passed from the previous state.
            surface (pygame.Surface): The main display surface.
        """
        self.state_id = state_name
        self.shared_data = shared_data

        if "window_size" in self.shared_data:
            self.window_size = self.shared_data.pop("window_size")

        if surface.get_size() != self.window_size:
            pg.display.set_mode(self.window_size)  # Set the window size

        surface.fill(self.bg_colour)

    def handle_events(self, events):
        """
        Processes input events and updates state attributes.

        Args:
            events (list): A list of pygame events to process.
        """
        self.left_click = False
        self.right_click = False
        self.pressed_keys = []

        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_click = True
                elif event.button == 3:
                    self.right_click = True
            elif event.type == pg.KEYDOWN:
                self.pressed_keys.append(event)

        self.mouse_position = pg.mouse.get_pos() if pg.mouse.get_focused() else (-1, -1)

    def update(self, delta_time):
        """
        Updates game logic, including button states.

        Args:
            delta_time (float): The time elapsed since the last frame.
        """
        self._update_buttons()

    def _update_buttons(self):
        """
        Checks button interactions and triggers actions when clicked.
        """
        for button in self.buttons:
            button.update(self.mouse_position, self.left_click)
            if button.is_clicked:
                button.is_clicked = False
                self.is_done = True
                self.on_button_click(button)

    def on_button_click(self, clicked_button):
        """
        Defines behavior when a button is clicked.
        Should be overridden in subclasses to implement specific actions.

        Args:
            clicked_button (Button): The button that was clicked.
        """
        pass

    def draw(self, surface):
        """
        Renders state visuals, including buttons.

        Args:
            surface (pygame.Surface): The surface on which to render.
        """
        self._draw_buttons(surface)

    def _draw_buttons(self, surface):
        """
        Renders buttons onto the given surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the buttons.
        """
        for button in self.buttons:
            button.draw(surface)
