"""
FAITH 8BIT - Sprite Test

Entry point. Run this file from inside the FAITH_8BIT folder:

    cd FAITH_8BIT
    python main.py

It loads spritesheets from the ASSETS/ folder that sits next
to this file (see assets.py).
"""

import sys

import pygame

import config
from assets import Assets
from game import Game


def main():
    pygame.init()

    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("FAITH 8BIT - Sprite Test")

    clock = pygame.time.Clock()

    # Assets must be built AFTER set_mode() — convert_alpha() needs
    # an active display surface.
    assets = Assets()

    game = Game(screen, assets)

    while game.running:
        dt = clock.tick(config.FPS) / 1000.0

        game.handle_events()

        if not game.running:
            break

        game.update(dt)
        game.draw()

        pygame.display.flip()

        game.finalize_frame()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
