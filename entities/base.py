"""
Shared base for every moving, animated actor in the game
(June, Monster). Holds position, facing, and the
frame/action-timer bookkeeping both subclasses need, plus
screen-bound clamping so that logic only lives in one place.
"""

import config


class Entity:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.facing = "down"

        self.frame = 0
        self.frame_timer = 0

        self.action = None
        self.action_timer = 0

    def clamp_to_bounds(self):
        half_size = self.size // 2

        self.x = max(half_size, min(self.x, config.SCREEN_WIDTH - half_size))
        self.y = max(half_size, min(self.y, config.SCREEN_HEIGHT - half_size))
