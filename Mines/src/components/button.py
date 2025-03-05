from components import box
import utils

class Button:
    """
    A UI button class that changes appearance based on user interaction.
    """

    def __init__(self, position, label, center_x=True, center_y=False, size=utils.BUTTON_SIZE):
        """
        Initializes a Button instance.

        Args:
            position (tuple): The (x, y) coordinates of the button.
            label (str): The text displayed on the button.
            center_x (bool, optional): Whether to center the button horizontally. Defaults to True.
            center_y (bool, optional): Whether to center the button vertically. Defaults to False.
            size (tuple, optional): The width and height of the button. Defaults to utils.BUTTON_SIZE.
        """
        self.label = label
        self.center_x = center_x
        self.center_y = center_y

        # Determine font based on button size
        self.font = utils.BIG_FONT if size == utils.BIG_BUTTON_SIZE else utils.MEDIUM_FONT

        # Create button surfaces for different states
        self.idle_surface = box.Box(size, position, text=self.label, font=self.font,
                                    tiles=utils.spritesheets["button_idle"],
                                    center_x=center_x, center_y=center_y)

        self.active_surface = box.Box(size, position, text=self.label, font=self.font,
                                      tiles=utils.spritesheets["button_active"],
                                      center_x=center_x, center_y=center_y)

        self.locked_surface = box.Box(size, position, text=self.label, font=self.font,
                                      tiles=utils.spritesheets["button_locked"],
                                      center_x=center_x, center_y=center_y)

        # Get the button's rectangular area
        self.rect = self.idle_surface.rect

        # Button states
        self.is_active = False   # True if hovered over
        self.is_clicked = False  # True if clicked
        self.is_locked = False   # True if disabled

    def update(self, mouse_position, is_left_click):
        """
        Updates the button state based on mouse interaction.

        Args:
            mouse_position (tuple): The (x, y) coordinates of the mouse cursor.
            is_left_click (bool): Whether the left mouse button is clicked.
        """
        if self.rect.collidepoint(mouse_position) and not self.is_locked:
            self.is_active = True
            if is_left_click:
                self.is_clicked = True
        else:
            self.is_active = False

    def draw(self, surface):
        """
        Draws the button onto the given surface based on its current state.

        Args:
            surface (pygame.Surface): The surface on which to render the button.
        """
        if self.is_locked:
            self.locked_surface.draw(surface)
        elif self.is_active:
            self.active_surface.draw(surface)
        else:
            self.idle_surface.draw(surface)

