"""
PracticeMode — a 1v1 combat sandbox: June vs one monster type,
entered from the normal test screen with P.
"""

import pygame

import config
from entities.june import June
from entities.monster import Monster


class PracticeMode:
    def __init__(self, assets, fonts, monster_type):
        self.assets = assets
        self.fonts = fonts
        self.monster_type = monster_type

        self.june = June(assets)
        self.monster = Monster(assets, monster_type)

        # Put June and monster apart.
        self.june.x = config.SCREEN_WIDTH // 2 - 220
        self.june.y = config.SCREEN_HEIGHT // 2

        self.monster.x = config.SCREEN_WIDTH // 2 + 220
        self.monster.y = config.SCREEN_HEIGHT // 2

        self.projectiles = []

        self.red_flash_timer = 0

        self.finished = False
        self.completed = False

    # ========================================================
    # RESET
    # ========================================================

    def reset(self):
        self.__init__(self.assets, self.fonts, self.monster_type)

    # ========================================================
    # ATTACK COLLISION
    # ========================================================

    def check_attack_hit(self):
        if self.june.action != "attack":
            return
        if self.june.attack_hit:
            return
        if self.monster.defeated:
            return
        if self.monster.action == "death":
            return

        attack_hitbox = self.june.get_attack_hitbox()

        monster_rect = pygame.Rect(
            self.monster.x - config.DISPLAY_SIZE // 2,
            self.monster.y - config.DISPLAY_SIZE // 2,
            config.DISPLAY_SIZE,
            config.DISPLAY_SIZE,
        )

        if attack_hitbox.colliderect(monster_rect):
            self.monster.take_practice_damage()
            self.june.attack_hit = True

    # ========================================================
    # MONSTER CONTACT
    # ========================================================

    def check_monster_contact(self):
        if self.monster.defeated:
            return
        if self.monster.action == "death":
            return
        if self.june.hearts <= 0:
            return

        dx = self.monster.x - self.june.x
        dy = self.monster.y - self.june.y

        distance = (dx * dx + dy * dy) ** 0.5

        if distance <= config.PRACTICE_MONSTER_CONTACT_DISTANCE:
            self.june.take_damage()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):
        if self.red_flash_timer > 0:
            self.red_flash_timer -= dt

            if self.red_flash_timer < 0:
                self.red_flash_timer = 0

        # ----------------------------------------------------
        # DEAD
        # ----------------------------------------------------

        if self.june.hearts <= 0:
            return

        self.june.update(dt, True)
        self.monster.update(dt, self.projectiles)

        self.check_attack_hit()
        self.check_monster_contact()

        for projectile in self.projectiles:
            projectile.update(dt)

        self.projectiles = [
            projectile for projectile in self.projectiles if projectile.alive
        ]

        # The monster has completed its full death/pop animation.
        # Mark the practice fight complete; Game leaves practice
        # mode only after this frame has been drawn.
        if self.monster.defeated:
            self.completed = True

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):
        font = self.fonts.font
        small_font = self.fonts.small_font

        surface.fill(config.BACKGROUND_COLOR)

        # ----------------------------------------------------
        # PRACTICE MODE TITLE
        # ----------------------------------------------------

        title = font.render("PRACTICE MODE", True, config.TEXT_COLOR)
        surface.blit(title, (20, 20))

        monster_name = self.monster_type.replace("_", " ").upper()
        monster_text = small_font.render(monster_name, True, config.SUBTEXT_COLOR)
        surface.blit(monster_text, (20, 55))

        # ----------------------------------------------------
        # HEARTS
        # ----------------------------------------------------

        if self.june.hearts > 0:
            heart_sprite = self.assets.heart_sprites[
                config.PRACTICE_JUNE_HEARTS - self.june.hearts
            ]
            surface.blit(heart_sprite, (20, 90))

        # ----------------------------------------------------
        # MONSTER HP
        # ----------------------------------------------------

        if not self.monster.defeated:
            hp_text = small_font.render(
                "MONSTER HP: "
                + str(self.monster.hp)
                + " / "
                + str(config.PRACTICE_MONSTER_HP),
                True,
                config.TEXT_COLOR,
            )
            surface.blit(hp_text, (20, 165))

        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        controls = small_font.render(
            "WASD: Move | E: Attack | 0: Exit", True, config.SUBTEXT_COLOR
        )
        surface.blit(controls, (20, config.SCREEN_HEIGHT - 30))

        # ----------------------------------------------------
        # PROJECTILES / MONSTER / JUNE
        # ----------------------------------------------------

        for projectile in self.projectiles:
            projectile.draw(surface)

        if not self.monster.defeated:
            self.monster.draw(surface)

        self.june.draw(surface)

        # ----------------------------------------------------
        # DEATH SCREEN
        # ----------------------------------------------------

        if self.june.hearts <= 0:
            overlay = pygame.Surface(
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))

            death_text = font.render("YOU DIED", True, config.TEXT_COLOR)
            death_rect = death_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 - 30)
            )
            surface.blit(death_text, death_rect)

            retry_text = small_font.render(
                "PRESS R TO TRY AGAIN", True, config.TEXT_COLOR
            )
            retry_rect = retry_text.get_rect(
                center=(config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2 + 25)
            )
            surface.blit(retry_text, retry_rect)

        # ----------------------------------------------------
        # RED FLASH
        # ----------------------------------------------------

        if self.red_flash_timer > 0:
            flash = pygame.Surface(
                (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA
            )
            alpha = int(180 * (self.red_flash_timer / config.RED_FLASH_DURATION))
            flash.fill((255, 0, 0, alpha))
            surface.blit(flash, (0, 0))
