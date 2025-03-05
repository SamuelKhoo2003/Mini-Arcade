import sys
import pygame as pg

import utils
from pages import custom, gameengine, menu, loadingscreen

def main():
    states = {
        "Custom": custom.Custom(),
        "GameEngine": gameengine.GameEngine(),
        "NewGameMenu": menu.NewGameMenu(),
        "MainMenu": menu.MainMenu(),
        "LoadingScreen": loadingscreen.LoadingScreen(),
    }

    # Initialise the starting state of game
    current_state = states[utils.START_STATE_NAME]
    current_state.enter(utils.START_STATE_NAME, {}, pg.display.get_surface())
    clock = pg.time.Clock()

    while True:
        delta_time = clock.tick(utils.FPS_MAX)
        if pg.event.get(pg.QUIT) or current_state.exit_game:
            break
        current_state.handle_events(pg.event.get())
        if current_state.is_done:
            current_state.is_done = False
            shared_data = current_state.shared_data
            next_state = current_state.next_state
            current_state = states[next_state]
            current_state.enter(next_state, shared_data, utils.display_surface)
        current_state.update(delta_time)
        current_state.draw(utils.display_surface)
        pg.display.update()

    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()

