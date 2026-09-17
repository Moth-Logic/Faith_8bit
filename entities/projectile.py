"""
Projectile — the ball shot by the cursed tree monster.
"""

import pygame

import config


class Projectile:
    def __init__(self, assets, x, y, direction):
        self.assets = assets

        self.x = x
        self.y = y

        self.direction = direction

        self.frame = 0
        self.frame_timer = 0

        self.alive = True

    def update(self, dt):
        if self.direction == "up":
            self.y -= config.BALL_SPEED * dt
        elif self.direction == "down":
            self.y += config.BALL_SPEED * dt
        elif self.direction == "left":
            self.x -= config.BALL_SPEED * dt
        elif self.direction == "right":
            self.x += config.BALL_SPEED * dt

        self.frame_timer += dt

        if self.frame_timer >= 1 / config.BALL_FPS:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % 3

        margin = 100

        if (
            self.x < -margin
            or self.x > config.SCREEN_WIDTH + margin
            or self.y < -margin
            or self.y > config.SCREEN_HEIGHT + margin
        ):
            self.alive = False

    def get_hitbox(self):
        """Return a collision rect around the projectile center."""
        size = config.DISPLAY_SIZE // 2
        return pygame.Rect(
            self.x - size,
            self.y - size,
            config.DISPLAY_SIZE,
            config.DISPLAY_SIZE,
        )

    def draw(self, surface):
        sprite = self.assets.ball_sprites[self.frame]
        rect = sprite.get_rect(center=(self.x, self.y))
        surface.blit(sprite, rect)
