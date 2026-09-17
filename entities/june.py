"""
June — the player character.
"""

import pygame

import config
from entities.base import Entity


class June(Entity):
    def __init__(self, assets):
        super().__init__(
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2,
            config.JUNE_DISPLAY_SIZE,
        )

        self.assets = assets

        # Practice combat.
        self.hearts = config.PRACTICE_JUNE_HEARTS
        self.damage_cooldown = 0
        self.attack_hit = False

    # ========================================================
    # ATTACK
    # ========================================================

    def attack(self):
        if self.action is not None:
            return
        if self.hearts <= 0:
            return

        self.action = "attack"
        self.action_timer = 0
        self.frame = 0
        self.attack_hit = False

    # ========================================================
    # HURT
    # ========================================================

    def hurt(self):
        if self.action is not None:
            return
        if self.hearts <= 0:
            return

        self.action = "hurt"
        self.action_timer = 0
        self.frame = 0

        # Knockback.
        if self.facing == "down":
            self.y -= config.JUNE_HURT_PUSHBACK
        elif self.facing == "up":
            self.y += config.JUNE_HURT_PUSHBACK
        elif self.facing == "left":
            self.x += config.JUNE_HURT_PUSHBACK
        elif self.facing == "right":
            self.x -= config.JUNE_HURT_PUSHBACK

        self.damage_cooldown = config.PRACTICE_DAMAGE_COOLDOWN

        self.clamp_to_bounds()

    # ========================================================
    # TAKE DAMAGE
    # ========================================================

    def take_damage(self):
        if self.damage_cooldown > 0:
            return
        if self.hearts <= 0:
            return

        self.hearts -= 1
        self.damage_cooldown = config.PRACTICE_DAMAGE_COOLDOWN

        self.hurt()

    # ========================================================
    # OBTAIN
    # ========================================================

    def obtain(self):
        if self.action is not None:
            return

        self.action = "obtain"
        self.action_timer = 0

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

            if self.damage_cooldown < 0:
                self.damage_cooldown = 0

        # ----------------------------------------------------
        # DEAD
        # ----------------------------------------------------

        if self.hearts <= 0:
            return

        # ----------------------------------------------------
        # HURT
        # ----------------------------------------------------

        if self.action == "hurt":
            self.action_timer += dt

            frame_duration = config.JUNE_HURT_DURATION / 2
            self.frame = int(self.action_timer / frame_duration) % 2

            if self.action_timer >= config.JUNE_HURT_DURATION:
                self.action = None
                self.action_timer = 0
                self.frame = 0

            return

        # ----------------------------------------------------
        # OBTAIN
        # ----------------------------------------------------

        if self.action == "obtain":
            self.action_timer += dt

            if self.action_timer >= 0.5:
                self.action = None
                self.action_timer = 0
                self.frame = 0

            return

        # ----------------------------------------------------
        # ATTACK
        # ----------------------------------------------------

        if self.action == "attack":
            self.action_timer += dt

            frame_duration = 1 / config.ACTION_FPS
            self.frame = int(self.action_timer / frame_duration)

            if self.frame >= 3:
                self.action = None
                self.action_timer = 0
                self.frame = 0
                self.attack_hit = False

            return

        # ----------------------------------------------------
        # MOVEMENT
        # ----------------------------------------------------

        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
            self.facing = "up"

        if keys[pygame.K_s]:
            dy += 1
            self.facing = "down"

        if keys[pygame.K_a]:
            dx -= 1
            self.facing = "left"

        if keys[pygame.K_d]:
            dx += 1
            self.facing = "right"

        if dx != 0 or dy != 0:
            length = (dx ** 2 + dy ** 2) ** 0.5

            dx /= length
            dy /= length

            self.x += dx * config.MOVE_SPEED * dt
            self.y += dy * config.MOVE_SPEED * dt

            self.frame_timer += dt

            if self.frame_timer >= 1 / config.WALK_FPS:
                self.frame_timer = 0
                self.frame = (self.frame + 1) % 2

        else:
            self.frame = 0
            self.frame_timer = 0

        # ----------------------------------------------------
        # SCREEN BOUNDS
        # ----------------------------------------------------

        self.clamp_to_bounds()

    # ========================================================
    # ATTACK HITBOX
    # ========================================================

    def get_attack_hitbox(self):
        """
        Returns June's directional attack hitbox, extending out
        from June in the direction she is attacking.
        """

        width = config.PRACTICE_ATTACK_HIT_WIDTH
        height = config.PRACTICE_ATTACK_HIT_HEIGHT

        if self.facing == "down":
            return pygame.Rect(
                self.x - width // 2,
                self.y + config.DISPLAY_SIZE // 2,
                width,
                height,
            )

        if self.facing == "up":
            return pygame.Rect(
                self.x - width // 2,
                self.y - config.DISPLAY_SIZE // 2 - height,
                width,
                height,
            )

        if self.facing == "right":
            return pygame.Rect(
                self.x + config.DISPLAY_SIZE // 2,
                self.y - height // 2,
                height,
                width,
            )

        if self.facing == "left":
            return pygame.Rect(
                self.x - config.DISPLAY_SIZE // 2 - width,
                self.y - height // 2,
                height,
                width,
            )

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):
        sprites = self.assets.june_sprites

        if self.action == "hurt":
            sprite = sprites["hurt"][self.facing][self.frame]

        elif self.action == "obtain":
            sprite = sprites["obtain"]

        elif self.action == "attack":
            sprite = self.assets.june_attack_sprites[self.facing][self.frame]

        else:
            sprite = sprites[self.facing][self.frame]

        rect = sprite.get_rect(center=(self.x, self.y))
        surface.blit(sprite, rect)
