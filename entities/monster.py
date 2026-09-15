"""
Monster — wandering enemy actor. Also handles the cursed
tree's stationary shoot behaviour.
"""

import random

import config
from entities.base import Entity
from entities.projectile import Projectile


class Monster(Entity):
    def __init__(self, assets, monster_type):
        super().__init__(
            config.SCREEN_WIDTH // 2,
            config.SCREEN_HEIGHT // 2,
            config.DISPLAY_SIZE,
        )

        self.assets = assets
        self.monster_type = monster_type

        self.facing = random.choice(["up", "down", "left", "right"])
        self.direction = self.facing

        self.direction_timer = random.uniform(
            config.MONSTER_DIRECTION_MIN_TIME,
            config.MONSTER_DIRECTION_MAX_TIME,
        )

        self.shoot_direction = "down"

        # Practice combat.
        self.hp = config.PRACTICE_MONSTER_HP
        self.hit_cooldown = 0

        self.death_frame = 0
        self.death_timer = 0

        self.defeated = False

    # ========================================================
    # CHOOSE DIRECTION
    # ========================================================

    def choose_direction(self):
        self.direction = random.choice(["up", "down", "left", "right"])
        self.facing = self.direction

        self.direction_timer = random.uniform(
            config.MONSTER_DIRECTION_MIN_TIME,
            config.MONSTER_DIRECTION_MAX_TIME,
        )

    # ========================================================
    # HURT
    # ========================================================

    def hurt(self):
        if self.action is not None:
            return
        if self.defeated:
            return

        self.action = "hurt"
        self.action_timer = 0
        self.frame = 0

        # Cursed Tree does not move.
        if self.monster_type == "cursed_tree":
            return

        if self.facing == "down":
            self.y -= config.MONSTER_HURT_PUSHBACK
        elif self.facing == "up":
            self.y += config.MONSTER_HURT_PUSHBACK
        elif self.facing == "left":
            self.x += config.MONSTER_HURT_PUSHBACK
        elif self.facing == "right":
            self.x -= config.MONSTER_HURT_PUSHBACK

        self.clamp_to_bounds()

    # ========================================================
    # PRACTICE DAMAGE
    # ========================================================

    def take_practice_damage(self):
        if self.defeated:
            return
        if self.hit_cooldown > 0:
            return

        self.hp -= 1
        self.hit_cooldown = config.PRACTICE_DAMAGE_COOLDOWN

        # Knockback.
        self.hurt()

        # Monster defeated.
        if self.hp <= 0:
            self.hp = 0
            self.action = "death"
            self.action_timer = 0
            self.death_frame = 0
            self.frame = 0

    # ========================================================
    # SHOOT
    # ========================================================

    def shoot(self):
        if self.monster_type != "cursed_tree":
            return
        if self.action is not None:
            return
        if self.defeated:
            return

        self.action = "shoot"
        self.action_timer = 0
        self.frame = 1

        self.shoot_direction = random.choice(["up", "down", "left", "right"])

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt, projectiles):
        if self.hit_cooldown > 0:
            self.hit_cooldown -= dt

            if self.hit_cooldown < 0:
                self.hit_cooldown = 0

        # ----------------------------------------------------
        # DEATH
        # ----------------------------------------------------

        if self.action == "death":
            self.action_timer += dt

            frame_duration = 1 / config.MONSTER_DEATH_FPS
            self.death_frame = int(self.action_timer / frame_duration)

            if self.death_frame >= 3:
                # All three pop frames have finished.
                # The monster is now completely gone.
                self.death_frame = 2
                self.defeated = True
                self.action = None

            return

        # ----------------------------------------------------
        # HURT
        # ----------------------------------------------------

        if self.action == "hurt":
            self.action_timer += dt

            if self.monster_type == "soldier":
                self.frame = 2

                if self.action_timer >= config.SOLDIER_HURT_DURATION:
                    self.action = None
                    self.action_timer = 0
                    self.frame = 0

                return

            if self.monster_type == "cursed_tree":
                sequence = config.TREE_HURT_SEQUENCE
            else:
                sequence = config.HURT_SEQUENCE

            sequence_index = int(self.action_timer / config.HURT_FRAME_DURATION)

            if sequence_index >= len(sequence):
                self.action = None
                self.action_timer = 0
                self.frame = 0
            else:
                self.frame = sequence[sequence_index]

            return

        # ----------------------------------------------------
        # TREE SHOOT
        # ----------------------------------------------------

        if self.action == "shoot":
            self.action_timer += dt
            self.frame = 1

            if self.action_timer >= config.TREE_SHOOT_DURATION:
                projectiles.append(
                    Projectile(self.assets, self.x, self.y, self.shoot_direction)
                )

                self.action = None
                self.action_timer = 0
                self.frame = 0

            return

        # ----------------------------------------------------
        # TREE (stationary, idle)
        # ----------------------------------------------------

        if self.monster_type == "cursed_tree":
            self.frame = 0
            return

        # ----------------------------------------------------
        # WANDERING
        # ----------------------------------------------------

        self.direction_timer -= dt

        if self.direction_timer <= 0:
            self.choose_direction()

        if self.direction == "up":
            self.y -= config.MONSTER_MOVE_SPEED * dt
            self.facing = "up"
        elif self.direction == "down":
            self.y += config.MONSTER_MOVE_SPEED * dt
            self.facing = "down"
        elif self.direction == "left":
            self.x -= config.MONSTER_MOVE_SPEED * dt
            self.facing = "left"
        elif self.direction == "right":
            self.x += config.MONSTER_MOVE_SPEED * dt
            self.facing = "right"

        # ----------------------------------------------------
        # SCREEN BOUNDS
        # ----------------------------------------------------

        self.clamp_to_bounds()

        # ----------------------------------------------------
        # WALKING
        # ----------------------------------------------------

        self.frame_timer += dt

        if self.frame_timer >= 1 / config.MONSTER_WALK_FPS:
            self.frame_timer = 0
            self.frame = (self.frame + 1) % 2

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):
        if self.action == "death":
            sprite = self.assets.monster_pop_sprites[self.death_frame]
            rect = sprite.get_rect(center=(self.x, self.y))
            surface.blit(sprite, rect)
            return

        if self.defeated:
            return

        sprite = self.assets.monster_sprites[self.monster_type][self.frame]
        rect = sprite.get_rect(center=(self.x, self.y))
        surface.blit(sprite, rect)
