import random
import pygame as pg
import utils
from collections import deque

class Minefield:
    """
    Represents a Minesweeper game board.
    """
    def __init__(self, width, height, total_mines):
        """
        Initializes the Minefield.

        :param width: Number of tiles in width
        :param height: Number of tiles in height
        :param total_mines: Total number of mines on the board
        """
        self.width = width
        self.height = height
        self.total_mines = total_mines
        self.tile_images = utils.minefield_tiles
        self.tile_size = utils.TILE_SIZE
        self.surface = pg.Surface((width * self.tile_size, height * self.tile_size)).convert()
        self.position = (0, 0)
        self.hovered_tile = None
        self.game_over = False
        self.remaining_mines = total_mines
        self.remaining_mines_updated = False
        self.result_message = None
        self.all_tiles = {(x, y) for x in range(self.width) for y in range(self.height)}
        self.hidden_tiles = self.all_tiles.copy()
        self.mine_positions = set()
        self.initial_click = None
        self.detonated_mine_tile = None
        self.incorrect_flags = set()
        self.flagged_tiles = set()
        self.hint_numbers = {}
        self.neighbouring_tiles = {
            tile: [(tile[0] + dx, tile[1] + dy) for dx, dy in ((-1, -1), (-1, 0), (-1, 1),
                                                               (0, -1), (0, 1), (1, -1),
                                                               (1, 0), (1, 1))
                  if (tile[0] + dx, tile[1] + dy) in self.all_tiles]
            for tile in self.all_tiles
        }
        self.render_surface()

    def update(self, mouse_position, left_click, right_click):
        """
        Handles user input and updates the game state.

        :param mouse_position: Tuple (x, y) of the mouse position
        :param left_click: Boolean indicating if left mouse button was clicked
        :param right_click: Boolean indicating if right mouse button was clicked
        """
        if self.game_over:
            return
        relative_x = mouse_position[0] - self.position[0]
        relative_y = mouse_position[1] - self.position[1]
        tile_pos = (relative_x // self.tile_size, relative_y // self.tile_size)
        if tile_pos not in self.all_tiles:
            return
        self.hovered_tile = tile_pos
        if left_click and tile_pos in self.hidden_tiles:
            if self.initial_click is None:
                self.initial_click = tile_pos
                safe_zone = {tile_pos} | set(self.neighbouring_tiles[tile_pos])
                self.place_mines(safe_zone)
            if tile_pos not in self.flagged_tiles:
                self.reveal_tile(tile_pos)
                self.check_loss(tile_pos)
                self.check_win()
                self.render_surface()
        elif right_click and tile_pos in self.hidden_tiles:
            self.toggle_flag(tile_pos)

    def place_mines(self, safe_zone):
        """
        Randomly places mines on the board while avoiding the given safe zone.

        :param safe_zone: Set of tiles where mines cannot be placed
        """
        possible_positions = list(self.all_tiles - safe_zone)
        self.mine_positions = set(random.sample(possible_positions, self.total_mines))
        for tile in self.all_tiles:
            if tile not in self.mine_positions:
                self.hint_numbers[tile] = sum(
                    1 for neighbour in self.neighbouring_tiles[tile] if neighbour in self.mine_positions
                )

    def reveal_tile(self, tile):
        """
        Reveals the given tile and automatically expands empty regions.

        :param tile: Tuple (x, y) of the tile to reveal
        """
        tiles_to_reveal = deque([tile])
        while tiles_to_reveal:
            current_tile = tiles_to_reveal.popleft()
            if current_tile not in self.hidden_tiles:
                continue
            self.hidden_tiles.remove(current_tile)
            if self.hint_numbers.get(current_tile, 0) == 0:
                for neighbour in self.neighbouring_tiles[current_tile]:
                    if neighbour in self.hidden_tiles and neighbour not in self.flagged_tiles:
                        tiles_to_reveal.append(neighbour)

    def toggle_flag(self, tile):
        """
        Toggles a flag on the specified tile.

        :param tile: Tuple (x, y) of the tile to flag/unflag
        """
        if self.game_over:
            return
        if tile in self.flagged_tiles:
            self.flagged_tiles.remove(tile)
        elif tile in self.hidden_tiles and len(self.flagged_tiles) < self.total_mines:
            self.flagged_tiles.add(tile)
        self.remaining_mines = self.total_mines - len(self.flagged_tiles)
        self.remaining_mines_updated = True
        self.render_surface()

    def check_loss(self, clicked_tile):
        """
        Checks if the player has clicked on a mine and updates game state.

        :param clicked_tile: Tuple (x, y) of the clicked tile
        """
        if clicked_tile in self.mine_positions:
            self.detonated_mine_tile = clicked_tile
            self.game_over = True
            self.result_message = "GAME OVER"
            self.hidden_tiles -= {tile for tile in self.mine_positions if tile not in self.flagged_tiles}
            self.incorrect_flags = {tile for tile in self.flagged_tiles if tile not in self.mine_positions}
            self.flagged_tiles -= self.incorrect_flags

    def check_win(self):
        """
        Checks if the player has won the game.
        """
        if self.hidden_tiles == self.mine_positions and not self.game_over:
            self.game_over = True
            self.result_message = "YOU WIN"

    def render_surface(self):
        """
        Renders the minefield surface with the current game state.
        """
        for tile in self.all_tiles:
            tile_blit_position = (tile[0] * self.tile_size, tile[1] * self.tile_size)
            if tile in self.hidden_tiles:
                if tile in self.flagged_tiles and tile not in self.incorrect_flags:
                    self.surface.blit(self.tile_images["flag"], tile_blit_position)
                elif tile in self.incorrect_flags:
                    self.surface.blit(self.tile_images["flag_wrong"], tile_blit_position)
                else:
                    self.surface.blit(self.tile_images["covered"], tile_blit_position)
            elif tile == self.detonated_mine_tile:
                self.surface.blit(self.tile_images["mine_exploded"], tile_blit_position)
            elif tile in self.mine_positions:
                self.surface.blit(self.tile_images["mine"], tile_blit_position)
            else:
                self.surface.blit(self.tile_images[self.hint_numbers[tile]], tile_blit_position)

    def draw(self, surface):
        """
        Draws the minefield on the given surface.

        :param surface: Pygame surface to draw on
        """
        surface.blit(self.surface, self.position)
        if self.hovered_tile:
            blit_pos = (self.hovered_tile[0] * self.tile_size + self.position[0], self.hovered_tile[1] * self.tile_size + self.position[1])
            if self.hovered_tile in self.flagged_tiles:
                surface.blit(self.tile_images["flag_highlighted"], blit_pos)
            elif self.hovered_tile in self.hidden_tiles:
                surface.blit(self.tile_images["covered_highlighted"], blit_pos)
        self.hovered_tile = None
