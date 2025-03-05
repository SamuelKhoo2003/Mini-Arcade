import os
import pygame as pg

# ---- Constants ----
STANDARD_WINDOW_SIZE = (400, 300)
FPS_MAX = 60
START_STATE_NAME = "LoadingScreen"
TILE_SIZE = 21  # Size of minefield tiles
ASSETS_DIR = os.path.join("..", "assets")

# ---- Colors ----
COLOURS = {
    "background_colour": (170, 170, 170),
    "white": (255, 255, 255),
    1: (0, 170, 225),
    2: (0, 186, 101),
    3: (223, 138, 0),
    4: (207, 0, 239),
    5: (0, 117, 207),
    6: (0, 138, 0),
    7: (239, 85, 32),
    8: (117, 0, 255),
    "?": (170, 0, 0)
}

# ---- Box Tiles ----
BOX_TILE_NAMES = (
    "topleft", "top", "topright",
    "left", "center", "right",
    "bottomleft", "bottom", "bottomright"
)

# ---- Button Sizes ----
BUTTON_SIZE = (100, 35)
WIDE_BUTTON_SIZE = (200, 35)
BIG_BUTTON_SIZE = (150, 50)


# ---- Pygame Initialization ----
def init_pygame():
    """Initialize pygame and set up the display."""
    pg.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"  # Center the window
    pg.display.set_caption("Mines")
    return pg.display.set_mode(STANDARD_WINDOW_SIZE)


display_surface = init_pygame()


# ---- Fonts ----
FONT_PATH = os.path.join(ASSETS_DIR, "freesansbold.ttf")
SMALL_FONT = pg.font.Font(FONT_PATH, 15)
MEDIUM_FONT = pg.font.Font(FONT_PATH, 20)
BIG_FONT = pg.font.Font(FONT_PATH, 30)


# ---- Utility Functions ----
def load_image(image_path, alpha=True):
    """Load an image with optional alpha transparency."""
    image = pg.image.load(image_path)
    return image.convert_alpha() if alpha else image.convert()


def cut_sheet(sheet, tile_width, tile_height):
    """Cut the spritesheet into individual tiles."""
    sheet_width, sheet_height = sheet.get_size()
    cols, rows = sheet_width // tile_width, sheet_height // tile_height
    images = []

    for r in range(rows):
        for c in range(cols):
            image = pg.Surface((tile_width, tile_height), pg.SRCALPHA).convert_alpha()
            image.blit(sheet, (0, 0), (c * tile_width, r * tile_height, tile_width, tile_height))
            images.append(image)

    return images


def load_tiles(sheet, tile_width=None, tile_height=None):
    """Load tile images from the spritesheet."""
    if tile_width is None or tile_height is None:
        tile_width, tile_height = (dim // 3 for dim in sheet.get_size())

    images = cut_sheet(sheet, tile_width, tile_height)
    return {name: img for name, img in zip(BOX_TILE_NAMES, images)} | {"width": tile_width, "height": tile_height}


def load_minefield_tiles():
    """Load minefield tiles and create necessary numbered and special tiles."""
    minefield_spritesheet = load_image(os.path.join(ASSETS_DIR, "minefield.png"))
    minefield_tile_images = cut_sheet(minefield_spritesheet, TILE_SIZE, TILE_SIZE)

    minefield_tile_names = (
        0, "covered", "covered_highlighted", "mine_exploded",
        "mine", "flag", "flag_highlighted", "flag_wrong"
    )
    minefield_tiles = dict(zip(minefield_tile_names, minefield_tile_images))

    # Build numbered tiles (1-8)
    tile_font = pg.font.Font(None, 25)
    for i in range(1, 9):
        num = tile_font.render(str(i), True, COLOURS[i])
        tile = minefield_tile_images[0].copy()
        tile.blit(num, num.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2)))
        minefield_tiles[i] = tile

    # Create '?' tiles
    questionmark = tile_font.render("?", True, COLOURS["?"])
    for tile_name in ["covered", "covered_highlighted"]:
        tile = minefield_tile_images[1 if "highlighted" in tile_name else 2].copy()
        tile.blit(questionmark, questionmark.get_rect(center=(TILE_SIZE // 2, TILE_SIZE // 2)))
        minefield_tiles[f"questionmark_{tile_name}"] = tile

    return minefield_tiles


def load_spritesheets():
    """Load all spritesheets and generate tile dictionaries."""
    spritesheet_files = ["box.png", "textbox.png", "button_idle.png",
                         "button_active.png", "button_locked.png"]
    spritesheets = {name: load_image(os.path.join(ASSETS_DIR, name)) for name in spritesheet_files}

    return {
        "box": load_tiles(spritesheets["box.png"]),
        "textbox": load_tiles(spritesheets["textbox.png"]),
        "button_idle": load_tiles(spritesheets["button_idle.png"]),
        "button_active": load_tiles(spritesheets["button_active.png"]),
        "button_locked": load_tiles(spritesheets["button_locked.png"])
    }


# ---- Load Assets ----
LOADINGSCREEN_IMAGE = load_image(os.path.join(ASSETS_DIR, "loadingscreen.png"))
display_surface.blit(LOADINGSCREEN_IMAGE, (0, 0))
pg.display.update()

minefield_tiles = load_minefield_tiles()
spritesheets = load_spritesheets()
