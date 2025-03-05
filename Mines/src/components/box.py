import pygame as pg
import utils

class Box:
    """
    A class representing a box with a customizable background and optional text.

    Attributes:
        tiles (dict): A dictionary of tile images used for the box's background.
        width (int): The width of the box.
        height (int): The height of the box.
        tile_width (int): The width of each tile used for the background.
        tile_height (int): The height of each tile used for the background.
        box_surface (Surface): The surface that holds the box's image.
        background (Surface): The surface that holds the background tiles.
        rect (Rect): The rectangle representing the position and size of the box.
        font (Font): The font used for rendering text.
        name (str, optional): The name of the box (optional).
    """

    def __init__(self, size, position, text=None, font=utils.MEDIUM_FONT,
                 tiles=utils.spritesheets["box"], center_x=False, center_y=False,
                 name=None):
        """
        Initializes a new Box instance.

        Args:
            size (tuple): The size of the box as a tuple (width, height).
            position (tuple): The position of the box as a tuple (x, y).
            text (str, optional): The text to display inside the box (default is None).
            font (Font, optional): The font to use for the text (default is utils.MEDIUM_FONT).
            tiles (dict, optional): A dictionary containing tile images (default is utils.box_tiles).
            center_x (bool, optional): Whether to center the box horizontally (default is False).
            center_y (bool, optional): Whether to center the box vertically (default is False).
            name (str, optional): The name of the box (default is None).
        """
        self.tiles = tiles
        self.width, self.height = size
        self.tile_width, self.tile_height = tiles["topleft"].get_rect().size
        self.box_surface = pg.Surface(size).convert()
        self.background = pg.Surface(size).convert()
        x, y = position

        if center_x:
            x -= size[0] // 2
        if center_y:
            y -= size[1] // 2

        self.rect = pg.Rect((x, y), size)
        self.font = font
        if name:
            self.name = name

        self._draw_background()

        if text:
            self.update(text)

    def _draw_background(self):
        # fill center of box with the center tile
        for x in range(self.tile_width, self.width - self.tile_width, self.tile_width):
            for y in range(self.tile_height, self.height - self.tile_height, self.tile_height):
                self.background.blit(self.tiles["center"], (x, y))

        # drawing the top and bottom edges
        for x in range(0, self.width, self.tile_width):
            self.background.blit(self.tiles["top"], (x, 0))
            self.background.blit(self.tiles["bottom"], (x, self.height - self.tile_height))

        # draw the left and right edges
        for y in range(0, self.height, self.tile_height):
            self.background.blit(self.tiles["left"], (0, y))
            self.background.blit(self.tiles["right"], (self.width - self.tile_width, y))

        self.box_surface.blit(self.background, (0, 0))

    def update(self, text):
        """
        Updates the text displayed inside the box.

        This method renders the provided text and places it at the center of the box.

        Args:
            text (str): The new text to display inside the box.
        """
        self.box_surface.blit(self.background, (0, 0))
        rendered_text = self.font.render(text, True, utils.COLOURS["white"]) # uses render method for font.Font from pygame pg.font.Font
        text_rect = rendered_text.get_rect(center=(self.width // 2, self.height // 2))
        text_rect.y -= self.font.get_descent() // 2 # accounts for font descent
        self.box_surface.blit(rendered_text, text_rect)

    def draw(self, surface):
        """
        Draws the box onto a given surface.

        This method blits the box surface onto the provided surface at the box's position.

        Args:
            surface (Surface): The surface onto which the box will be drawn.
        """
        surface.blit(self.box_surface, self.rect)