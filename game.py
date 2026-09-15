"""
Game — owns all mutable game state (previously module-level
globals in the original single-file script) and drives the
normal-test / practice-mode flow.
"""

import pygame

import config
from entities.june import June
from entities.monster import Monster
from practice_mode import PracticeMode


class Fonts:
    def __init__(self):
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)


class Game:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets
        self.fonts = Fonts()

        self.test_order = config.TEST_ORDER
        self.test_index = 0

        self.june = June(assets)
        self.monster = None
        self.projectiles = []

        self.practice_mode = None
        self._exit_practice_after_draw = False

        self.running = True

        if self.current_test() != "june":
            self.monster = Monster(assets, self.current_test())

    # ========================================================
    # HELPERS
    # ========================================================

    def current_test(self):
        return self.test_order[self.test_index]

    def reset_test(self):
        self.june = June(self.assets)
        self.projectiles = []

        if self.current_test() == "june":
            self.monster = None
        else:
            self.monster = Monster(self.assets, self.current_test())

    def get_controls(self):
        current_test = self.current_test()

        if current_test == "june":
            return "WASD: Move | H: Hurt | O: Obtain | E: Attack"

        if current_test == "cursed_tree":
            return "H: Hurt | E: Shoot | P: Practice"

        return "H: Hurt | P: Practice"

    # ========================================================
    # EVENTS
    # ========================================================

    def handle_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False
                return

            if event.type != pygame.KEYDOWN:
                continue

            if self.practice_mode is not None:
                self._handle_practice_key(event)
            else:
                self._handle_test_key(event)

    def _handle_practice_key(self, event):
        current_practice = self.practice_mode

        # --------------------------------------------------------
        # EXIT PRACTICE
        # --------------------------------------------------------

        if event.key == pygame.K_0:
            self.practice_mode = None
            self.reset_test()
            return

        # --------------------------------------------------------
        # RETRY AFTER DEATH
        # --------------------------------------------------------

        if event.key == pygame.K_r and current_practice.june.hearts <= 0:
            current_practice.reset()
            return

        # --------------------------------------------------------
        # ATTACK
        # --------------------------------------------------------

        if (
            event.key == pygame.K_e
            and current_practice.june.hearts > 0
            and not current_practice.completed
        ):
            current_practice.june.attack()

    def _handle_test_key(self, event):
        # ------------------------------------------------
        # PREVIOUS TEST
        # ------------------------------------------------

        if event.key == pygame.K_LEFT:
            self.test_index -= 1

            if self.test_index < 0:
                self.test_index = len(self.test_order) - 1

            self.reset_test()
            return

        # ------------------------------------------------
        # NEXT TEST
        # ------------------------------------------------

        if event.key == pygame.K_RIGHT:
            self.test_index += 1

            if self.test_index >= len(self.test_order):
                self.test_index = 0

            self.reset_test()
            return

        # ------------------------------------------------
        # ENTER PRACTICE MODE
        # ------------------------------------------------

        if event.key == pygame.K_p and self.current_test() != "june":
            self.practice_mode = PracticeMode(
                self.assets, self.fonts, self.current_test()
            )
            return

        # ------------------------------------------------
        # JUNE TEST
        # ------------------------------------------------

        if self.current_test() == "june":
            if event.key == pygame.K_h:
                self.june.hurt()
            elif event.key == pygame.K_o:
                self.june.obtain()
            elif event.key == pygame.K_e:
                self.june.attack()
            return

        # ------------------------------------------------
        # MONSTER TEST
        # ------------------------------------------------

        if event.key == pygame.K_h:
            self.monster.hurt()
        elif event.key == pygame.K_e and self.current_test() == "cursed_tree":
            self.monster.shoot()

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):
        if self.practice_mode is not None:
            self._update_practice(dt)
            return

        current_test = self.current_test()

        if current_test == "june":
            self.june.update(dt)
        else:
            self.monster.update(dt, self.projectiles)

            for projectile in self.projectiles:
                projectile.update(dt)

            self.projectiles = [
                projectile for projectile in self.projectiles if projectile.alive
            ]

    def _update_practice(self, dt):
        current_practice = self.practice_mode

        previous_hearts = current_practice.june.hearts

        current_practice.update(dt)

        if previous_hearts > 0 and current_practice.june.hearts <= 0:
            current_practice.red_flash_timer = config.RED_FLASH_DURATION

        # Don't leave practice mode yet — the completed frame still
        # needs to be drawn. finalize_frame() clears it after draw().
        if current_practice.completed:
            self._exit_practice_after_draw = True

    def finalize_frame(self):
        """
        Call once per frame, AFTER draw() + pygame.display.flip().

        Leaving practice mode is deferred to here so the final
        (completed) practice frame still gets drawn before the
        screen switches back to the normal test view.
        """

        if self._exit_practice_after_draw:
            self._exit_practice_after_draw = False
            self.practice_mode = None
            self.reset_test()

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):
        if self.practice_mode is not None:
            self.practice_mode.draw(self.screen)
            return

        self._draw_normal_test()

    def _draw_normal_test(self):
        screen = self.screen
        font = self.fonts.font
        small_font = self.fonts.small_font

        screen.fill(config.BACKGROUND_COLOR)

        # --------------------------------------------------------
        # TITLE
        # --------------------------------------------------------

        title = font.render("FAITH 8BIT - Sprite Test", True, config.TEXT_COLOR)
        screen.blit(title, (20, 20))

        # --------------------------------------------------------
        # CURRENT TEST
        # --------------------------------------------------------

        current_name = self.current_test().replace("_", " ").upper()
        test_text = font.render("TEST: " + current_name, True, config.TEXT_COLOR)
        screen.blit(test_text, (20, 55))

        # --------------------------------------------------------
        # CONTROLS
        # --------------------------------------------------------

        controls = small_font.render(self.get_controls(), True, config.SUBTEXT_COLOR)
        screen.blit(controls, (20, config.SCREEN_HEIGHT - 45))

        navigation = small_font.render(
            "LEFT / RIGHT: Change Test", True, config.SUBTEXT_COLOR
        )
        screen.blit(navigation, (20, config.SCREEN_HEIGHT - 22))

        # --------------------------------------------------------
        # DRAW ACTOR
        # --------------------------------------------------------

        if self.current_test() == "june":
            self.june.draw(screen)
        else:
            self.monster.draw(screen)

            for projectile in self.projectiles:
                projectile.draw(screen)
