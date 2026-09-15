"""
Asset loading for FAITH 8BIT.

The game code lives OUTSIDE the ASSETS folder, laid out like:

    FAITH_8BIT/
        ASSETS/            <- spritesheets (.png) go here
            Sprite_June_Overworld.png
            Sprite_June_Attacking.png
            Sprite_Monsters.png
            Hearts.png
        assets.py          <- this file
        config.py
        ...

ASSETS_DIR is resolved relative to this file (not the current
working directory), so the game finds its sprites no matter
where you launch it from.
"""

import os
import sys

import pygame

import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "ASSETS")


def _asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)


def get_sprite(sheet, x, y, width=16, height=16, scale=config.DISPLAY_SIZE):
    """
    Extract and scale a sprite.

    16x16 source -> display size (192x192 by default).
    """

    sprite = sheet.subsurface(pygame.Rect(x, y, width, height)).copy()

    scale_factor = scale / config.NORMAL_SPRITE_SIZE

    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    sprite = pygame.transform.scale(sprite, (new_width, new_height))

    return sprite


def get_attack_sprite(sheet, x, y, width, height, pivot):
    """
    Creates a fixed attack canvas.

    The actual 16x16 portion containing June's body is used as
    the pivot. This prevents June from visually moving during
    attacks.
    """

    frame = sheet.subsurface(pygame.Rect(x, y, width, height)).copy()

    frame = pygame.transform.scale(
        frame,
        (width * config.JUNE_PIXEL_SCALE, height * config.JUNE_PIXEL_SCALE),
    )

    canvas = pygame.Surface(
        (config.JUNE_ATTACK_DISPLAY_SIZE, config.JUNE_ATTACK_DISPLAY_SIZE),
        pygame.SRCALPHA,
    )

    canvas.fill((0, 0, 0, 0))

    body_size = config.NORMAL_SPRITE_SIZE * config.JUNE_PIXEL_SCALE
    canvas_center = config.JUNE_ATTACK_DISPLAY_SIZE // 2

    frame_rect = frame.get_rect()

    if pivot == "top":
        frame_rect.centerx = canvas_center
        frame_rect.top = canvas_center - body_size // 2

    elif pivot == "bottom":
        frame_rect.centerx = canvas_center
        frame_rect.bottom = canvas_center + body_size // 2

    elif pivot == "left":
        frame_rect.centery = canvas_center
        frame_rect.left = canvas_center - body_size // 2

    elif pivot == "right":
        frame_rect.centery = canvas_center
        frame_rect.right = canvas_center + body_size // 2

    else:
        raise ValueError("Invalid attack pivot.")

    canvas.blit(frame, frame_rect)

    return canvas


class Assets:
    """
    Holds every loaded/scaled sprite the game needs.

    Must be constructed AFTER pygame.display.set_mode(), since
    convert_alpha() requires an active display surface.
    """

    def __init__(self):
        self._load_sheets()
        self._build_june_sprites()
        self._build_june_attack_sprites()
        self._build_monster_sprites()
        self._build_ball_sprites()
        self._build_heart_sprites()

    # --------------------------------------------------------
    # SHEETS
    # --------------------------------------------------------

    def _load_sheets(self):
        try:
            self.june_sheet = pygame.image.load(
                _asset_path("Sprite_June_Overworld.png")
            ).convert_alpha()

            self.june_attack_sheet = pygame.image.load(
                _asset_path("Sprite_June_Attacking.png")
            ).convert_alpha()

            self.monster_sheet = pygame.image.load(
                _asset_path("Sprite_Monsters.png")
            ).convert_alpha()

            self.hearts_sheet = pygame.image.load(
                _asset_path("Hearts.png")
            ).convert_alpha()

        except pygame.error as error:
            print("Could not load sprite sheet from:", ASSETS_DIR)
            print(error)

            pygame.quit()
            sys.exit()

    # --------------------------------------------------------
    # JUNE
    # --------------------------------------------------------

    def _build_june_sprites(self):
        sheet = self.june_sheet

        self.june_sprites = {
            "down": [get_sprite(sheet, 0, 0), get_sprite(sheet, 16, 0)],
            "left": [get_sprite(sheet, 32, 0), get_sprite(sheet, 48, 0)],
            "up": [get_sprite(sheet, 64, 0), get_sprite(sheet, 80, 0)],
            "right": [get_sprite(sheet, 96, 0), get_sprite(sheet, 112, 0)],
            "obtain": get_sprite(sheet, 0, 16),
            "hurt": {
                "down": [get_sprite(sheet, 0, 32), get_sprite(sheet, 16, 32)],
                "left": [get_sprite(sheet, 32, 32), get_sprite(sheet, 48, 32)],
                "up": [get_sprite(sheet, 64, 32), get_sprite(sheet, 80, 32)],
                "right": [get_sprite(sheet, 96, 32), get_sprite(sheet, 112, 32)],
            },
        }

    def _build_june_attack_sprites(self):
        sheet = self.june_attack_sheet

        self.june_attack_sprites = {
            "down": [
                get_attack_sprite(sheet, 0, 0, 16, 32, "top"),
                get_attack_sprite(sheet, 16, 0, 16, 32, "top"),
                get_attack_sprite(sheet, 32, 0, 16, 32, "top"),
            ],
            "up": [
                get_attack_sprite(sheet, 48, 0, 16, 32, "bottom"),
                get_attack_sprite(sheet, 64, 0, 16, 32, "bottom"),
                get_attack_sprite(sheet, 80, 0, 16, 32, "bottom"),
            ],
            "right": [
                get_attack_sprite(sheet, 0, 32, 32, 16, "left"),
                get_attack_sprite(sheet, 32, 32, 32, 16, "left"),
                get_attack_sprite(sheet, 64, 32, 32, 16, "left"),
            ],
            "left": [
                get_attack_sprite(sheet, 0, 48, 32, 16, "right"),
                get_attack_sprite(sheet, 32, 48, 32, 16, "right"),
                get_attack_sprite(sheet, 64, 48, 32, 16, "right"),
            ],
        }

    # --------------------------------------------------------
    # MONSTERS
    # --------------------------------------------------------

    def _build_monster_sprites(self):
        self.monster_sprites = {}

        for monster_name, coordinates in config.MONSTER_COORDINATES.items():
            self.monster_sprites[monster_name] = [
                get_sprite(self.monster_sheet, column * 16, row * 16)
                for column, row in coordinates
            ]

        # Monster pop / death sprites. Row 4: (0,48) (16,48) (32,48)
        self.monster_pop_sprites = [
            get_sprite(self.monster_sheet, 0, 48),
            get_sprite(self.monster_sheet, 16, 48),
            get_sprite(self.monster_sheet, 32, 48),
        ]

    def _build_ball_sprites(self):
        self.ball_sprites = [
            get_sprite(self.monster_sheet, 3 * 16, 1 * 16),
            get_sprite(self.monster_sheet, 4 * 16, 1 * 16),
            get_sprite(self.monster_sheet, 5 * 16, 1 * 16),
        ]

    # --------------------------------------------------------
    # HEARTS
    # --------------------------------------------------------

    def _build_heart_sprites(self):
        # Hearts.png = 32x64. Row 1 = 4 hearts, row 2 = 3, row 3 = 2, row 4 = 1.
        raw = [
            self.hearts_sheet.subsurface(pygame.Rect(0, 0, 32, 16)).copy(),
            self.hearts_sheet.subsurface(pygame.Rect(0, 16, 32, 16)).copy(),
            self.hearts_sheet.subsurface(pygame.Rect(0, 32, 32, 16)).copy(),
            self.hearts_sheet.subsurface(pygame.Rect(0, 48, 32, 16)).copy(),
        ]

        self.heart_sprites = [
            pygame.transform.scale(
                sprite,
                (config.HEART_DISPLAY_WIDTH, config.HEART_DISPLAY_HEIGHT),
            )
            for sprite in raw
        ]
