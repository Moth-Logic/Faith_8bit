import pygame
import sys
import random


# ============================================================
# INITIALIZATION
# ============================================================

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

pygame.display.set_caption(
    "FAITH 8BIT - Sprite Test"
)

clock = pygame.time.Clock()


# ============================================================
# CONSTANTS
# ============================================================

NORMAL_SPRITE_SIZE = 16

# June and monsters are the same visual size.

DISPLAY_SIZE = 192
JUNE_DISPLAY_SIZE = DISPLAY_SIZE

JUNE_PIXEL_SCALE = (
    DISPLAY_SIZE // NORMAL_SPRITE_SIZE
)


# ------------------------------------------------------------
# Attack
# ------------------------------------------------------------

JUNE_ATTACK_LOGICAL_SIZE = 32

JUNE_ATTACK_DISPLAY_SIZE = (
    JUNE_ATTACK_LOGICAL_SIZE
    * JUNE_PIXEL_SCALE
)


# ------------------------------------------------------------
# Movement
# ------------------------------------------------------------

MOVE_SPEED = 250
MONSTER_MOVE_SPEED = 70


# ------------------------------------------------------------
# Animation
# ------------------------------------------------------------

WALK_FPS = 10
MONSTER_WALK_FPS = 6
ACTION_FPS = 12
BALL_FPS = 8


# ------------------------------------------------------------
# June hurt
# ------------------------------------------------------------

JUNE_HURT_DURATION = 1.5
JUNE_HURT_PUSHBACK = 75


# ------------------------------------------------------------
# Monster hurt
# ------------------------------------------------------------

MONSTER_HURT_PUSHBACK = 55


# ------------------------------------------------------------
# Hurt animation
# ------------------------------------------------------------

HURT_FRAME_DURATION = 0.08

HURT_SEQUENCE = [
    2,
    1,
    2,
    1,
    1
]

TREE_HURT_SEQUENCE = [
    2,
    0,
    2,
    0,
    0
]


# ------------------------------------------------------------
# Special monsters
# ------------------------------------------------------------

SOLDIER_HURT_DURATION = 10.0
TREE_SHOOT_DURATION = 1.0


# ------------------------------------------------------------
# Projectile
# ------------------------------------------------------------

BALL_SPEED = 350


# ------------------------------------------------------------
# Monster wandering
# ------------------------------------------------------------

MONSTER_DIRECTION_MIN_TIME = 0.7
MONSTER_DIRECTION_MAX_TIME = 1.8


# ------------------------------------------------------------
# Practice mode
# ------------------------------------------------------------

PRACTICE_MONSTER_HP = 5
PRACTICE_JUNE_HEARTS = 4

PRACTICE_DAMAGE_COOLDOWN = 0.8

PRACTICE_ATTACK_HIT_WIDTH = 120
PRACTICE_ATTACK_HIT_HEIGHT = 120

PRACTICE_MONSTER_CONTACT_DISTANCE = 135

MONSTER_DEATH_FPS = 8

RED_FLASH_DURATION = 0.25


# ============================================================
# COLORS
# ============================================================

BACKGROUND_COLOR = (25, 25, 25)
TEXT_COLOR = (255, 255, 255)
SUBTEXT_COLOR = (180, 180, 180)
RED_FLASH_COLOR = (255, 0, 0)


# ============================================================
# SPRITE HELPER
# ============================================================

def get_sprite(
    sheet,
    x,
    y,
    width=16,
    height=16,
    scale=DISPLAY_SIZE
):
    """
    Extract and scale a sprite.

    16x16 source -> 192x192 display.
    """

    sprite = sheet.subsurface(
        pygame.Rect(
            x,
            y,
            width,
            height
        )
    ).copy()

    scale_factor = scale / 16

    new_width = int(
        width * scale_factor
    )

    new_height = int(
        height * scale_factor
    )

    sprite = pygame.transform.scale(
        sprite,
        (
            new_width,
            new_height
        )
    )

    return sprite


# ============================================================
# ATTACK SPRITE HELPER
# ============================================================

def get_attack_sprite(
    sheet,
    x,
    y,
    width,
    height,
    pivot
):
    """
    Creates a fixed attack canvas.

    The actual 16x16 portion containing June's body
    is used as the pivot.

    This prevents June from visually moving during attacks.
    """

    frame = sheet.subsurface(
        pygame.Rect(
            x,
            y,
            width,
            height
        )
    ).copy()

    frame = pygame.transform.scale(
        frame,
        (
            width * JUNE_PIXEL_SCALE,
            height * JUNE_PIXEL_SCALE
        )
    )

    canvas = pygame.Surface(
        (
            JUNE_ATTACK_DISPLAY_SIZE,
            JUNE_ATTACK_DISPLAY_SIZE
        ),
        pygame.SRCALPHA
    )

    canvas.fill(
        (0, 0, 0, 0)
    )

    body_size = (
        16 * JUNE_PIXEL_SCALE
    )

    canvas_center = (
        JUNE_ATTACK_DISPLAY_SIZE // 2
    )

    if pivot == "top":

        frame_rect = frame.get_rect()

        frame_rect.centerx = (
            canvas_center
        )

        frame_rect.top = (
            canvas_center
            - body_size // 2
        )

    elif pivot == "bottom":

        frame_rect = frame.get_rect()

        frame_rect.centerx = (
            canvas_center
        )

        frame_rect.bottom = (
            canvas_center
            + body_size // 2
        )

    elif pivot == "left":

        frame_rect = frame.get_rect()

        frame_rect.centery = (
            canvas_center
        )

        frame_rect.left = (
            canvas_center
            - body_size // 2
        )

    elif pivot == "right":

        frame_rect = frame.get_rect()

        frame_rect.centery = (
            canvas_center
        )

        frame_rect.right = (
            canvas_center
            + body_size // 2
        )

    else:

        raise ValueError(
            "Invalid attack pivot."
        )

    canvas.blit(
        frame,
        frame_rect
    )

    return canvas


# ============================================================
# LOAD SPRITE SHEETS
# ============================================================

try:

    june_sheet = pygame.image.load(
        "Sprite_June_Overworld.png"
    ).convert_alpha()

    june_attack_sheet = pygame.image.load(
        "Sprite_June_Attacking.png"
    ).convert_alpha()

    monster_sheet = pygame.image.load(
        "Sprite_Monsters.png"
    ).convert_alpha()

    hearts_sheet = pygame.image.load(
        "Hearts.png"
    ).convert_alpha()

except pygame.error as error:

    print(
        "Could not load sprite sheet:"
    )

    print(error)

    pygame.quit()
    sys.exit()


# ============================================================
# JUNE NORMAL SPRITES
# ============================================================

june_sprites = {

    "down": [

        get_sprite(
            june_sheet,
            0,
            0
        ),

        get_sprite(
            june_sheet,
            16,
            0
        )
    ],

    "left": [

        get_sprite(
            june_sheet,
            32,
            0
        ),

        get_sprite(
            june_sheet,
            48,
            0
        )
    ],

    "up": [

        get_sprite(
            june_sheet,
            64,
            0
        ),

        get_sprite(
            june_sheet,
            80,
            0
        )
    ],

    "right": [

        get_sprite(
            june_sheet,
            96,
            0
        ),

        get_sprite(
            june_sheet,
            112,
            0
        )
    ],

    "obtain": get_sprite(
        june_sheet,
        0,
        16
    ),

    "hurt": {

        "down": [

            get_sprite(
                june_sheet,
                0,
                32
            ),

            get_sprite(
                june_sheet,
                16,
                32
            )
        ],

        "left": [

            get_sprite(
                june_sheet,
                32,
                32
            ),

            get_sprite(
                june_sheet,
                48,
                32
            )
        ],

        "up": [

            get_sprite(
                june_sheet,
                64,
                32
            ),

            get_sprite(
                june_sheet,
                80,
                32
            )
        ],

        "right": [

            get_sprite(
                june_sheet,
                96,
                32
            ),

            get_sprite(
                june_sheet,
                112,
                32
            )
        ]
    }
}


# ============================================================
# JUNE ATTACK SPRITES
# ============================================================

june_attack_sprites = {

    "down": [

        get_attack_sprite(
            june_attack_sheet,
            0,
            0,
            16,
            32,
            "top"
        ),

        get_attack_sprite(
            june_attack_sheet,
            16,
            0,
            16,
            32,
            "top"
        ),

        get_attack_sprite(
            june_attack_sheet,
            32,
            0,
            16,
            32,
            "top"
        )
    ],

    "up": [

        get_attack_sprite(
            june_attack_sheet,
            48,
            0,
            16,
            32,
            "bottom"
        ),

        get_attack_sprite(
            june_attack_sheet,
            64,
            0,
            16,
            32,
            "bottom"
        ),

        get_attack_sprite(
            june_attack_sheet,
            80,
            0,
            16,
            32,
            "bottom"
        )
    ],

    "right": [

        get_attack_sprite(
            june_attack_sheet,
            0,
            32,
            32,
            16,
            "left"
        ),

        get_attack_sprite(
            june_attack_sheet,
            32,
            32,
            32,
            16,
            "left"
        ),

        get_attack_sprite(
            june_attack_sheet,
            64,
            32,
            32,
            16,
            "left"
        )
    ],

    "left": [

        get_attack_sprite(
            june_attack_sheet,
            0,
            48,
            32,
            16,
            "right"
        ),

        get_attack_sprite(
            june_attack_sheet,
            32,
            48,
            32,
            16,
            "right"
        ),

        get_attack_sprite(
            june_attack_sheet,
            64,
            48,
            32,
            16,
            "right"
        )
    ]
}


# ============================================================
# MONSTER SPRITE MAP
# ============================================================

monster_coordinates = {

    "wolf": [
        (0, 0),
        (1, 0),
        (2, 0)
    ],

    "spider": [
        (3, 0),
        (4, 0),
        (5, 0)
    ],

    "tormented_soul": [
        (6, 0),
        (7, 0),
        (8, 0)
    ],

    "cursed_tree": [
        (0, 1),
        (1, 1),
        (2, 1)
    ],

    "hellish_spider": [
        (6, 1),
        (7, 1),
        (8, 1)
    ],

    "hellish_hand": [
        (0, 2),
        (1, 2),
        (2, 2)
    ],

    "demon": [
        (3, 2),
        (4, 2),
        (5, 2)
    ],

    "soldier": [
        (6, 2),
        (7, 2),
        (8, 2)
    ]
}


# ============================================================
# MONSTER SPRITES
# ============================================================

monster_sprites = {}

for monster_name, coordinates in monster_coordinates.items():

    monster_sprites[monster_name] = []

    for column, row in coordinates:

        monster_sprites[
            monster_name
        ].append(

            get_sprite(
                monster_sheet,
                column * 16,
                row * 16
            )
        )


# ============================================================
# MONSTER POP / DEATH SPRITES
#
# ROW 4
#
# (0,48)
# (16,48)
# (32,48)
# ============================================================

monster_pop_sprites = [

    get_sprite(
        monster_sheet,
        0,
        48
    ),

    get_sprite(
        monster_sheet,
        16,
        48
    ),

    get_sprite(
        monster_sheet,
        32,
        48
    )
]


# ============================================================
# BALL SPRITES
# ============================================================

ball_sprites = [

    get_sprite(
        monster_sheet,
        3 * 16,
        1 * 16
    ),

    get_sprite(
        monster_sheet,
        4 * 16,
        1 * 16
    ),

    get_sprite(
        monster_sheet,
        5 * 16,
        1 * 16
    )
]


# ============================================================
# HEART SPRITES
#
# Hearts.png = 32x64
#
# Row 1 = 4 hearts
# Row 2 = 3 hearts
# Row 3 = 2 hearts
# Row 4 = 1 heart
# ============================================================

heart_sprites = [

    hearts_sheet.subsurface(
        pygame.Rect(
            0,
            0,
            32,
            16
        )
    ).copy(),

    hearts_sheet.subsurface(
        pygame.Rect(
            0,
            16,
            32,
            16
        )
    ).copy(),

    hearts_sheet.subsurface(
        pygame.Rect(
            0,
            32,
            32,
            16
        )
    ).copy(),

    hearts_sheet.subsurface(
        pygame.Rect(
            0,
            48,
            32,
            16
        )
    ).copy()
]


# Scale the heart display.

HEART_DISPLAY_WIDTH = 128
HEART_DISPLAY_HEIGHT = 64

heart_sprites = [

    pygame.transform.scale(
        sprite,
        (
            HEART_DISPLAY_WIDTH,
            HEART_DISPLAY_HEIGHT
        )
    )

    for sprite in heart_sprites
]


# ============================================================
# JUNE CLASS
# ============================================================

class June:

    def __init__(self):

        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

        self.facing = "down"

        self.frame = 0
        self.frame_timer = 0

        self.action = None
        self.action_timer = 0

        # Practice combat.

        self.hearts = PRACTICE_JUNE_HEARTS

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

            self.y -= JUNE_HURT_PUSHBACK

        elif self.facing == "up":

            self.y += JUNE_HURT_PUSHBACK

        elif self.facing == "left":

            self.x += JUNE_HURT_PUSHBACK

        elif self.facing == "right":

            self.x -= JUNE_HURT_PUSHBACK


        self.damage_cooldown = (
            PRACTICE_DAMAGE_COOLDOWN
        )


        half_size = (
            JUNE_DISPLAY_SIZE // 2
        )

        self.x = max(
            half_size,
            min(
                self.x,
                SCREEN_WIDTH - half_size
            )
        )

        self.y = max(
            half_size,
            min(
                self.y,
                SCREEN_HEIGHT - half_size
            )
        )


    # ========================================================
    # TAKE DAMAGE
    # ========================================================

    def take_damage(self):

        if self.damage_cooldown > 0:
            return

        if self.hearts <= 0:
            return

        self.hearts -= 1

        self.damage_cooldown = (
            PRACTICE_DAMAGE_COOLDOWN
        )

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

    def update(
        self,
        dt,
        practice_mode=True
    ):

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

            frame_duration = (
                JUNE_HURT_DURATION / 2
            )

            self.frame = (
                int(
                    self.action_timer
                    / frame_duration
                )
                % 2
            )

            if (
                self.action_timer
                >= JUNE_HURT_DURATION
            ):

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

            frame_duration = (
                1 / ACTION_FPS
            )

            self.frame = int(
                self.action_timer
                / frame_duration
            )

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

            length = (
                dx ** 2
                + dy ** 2
            ) ** 0.5

            dx /= length
            dy /= length

            self.x += (
                dx
                * MOVE_SPEED
                * dt
            )

            self.y += (
                dy
                * MOVE_SPEED
                * dt
            )


            self.frame_timer += dt

            if (
                self.frame_timer
                >= 1 / WALK_FPS
            ):

                self.frame_timer = 0

                self.frame = (
                    self.frame + 1
                ) % 2

        else:

            self.frame = 0
            self.frame_timer = 0


        # ----------------------------------------------------
        # SCREEN BOUNDS
        # ----------------------------------------------------

        half_size = (
            JUNE_DISPLAY_SIZE // 2
        )

        self.x = max(
            half_size,
            min(
                self.x,
                SCREEN_WIDTH - half_size
            )
        )

        self.y = max(
            half_size,
            min(
                self.y,
                SCREEN_HEIGHT - half_size
            )
        )


    # ========================================================
    # ATTACK HITBOX
    # ========================================================

    def get_attack_hitbox(self):

        """
        Returns June's directional attack hitbox.

        The hitbox extends out from June in the direction
        she is attacking.
        """

        width = PRACTICE_ATTACK_HIT_WIDTH
        height = PRACTICE_ATTACK_HIT_HEIGHT


        if self.facing == "down":

            return pygame.Rect(
                self.x - width // 2,
                self.y + DISPLAY_SIZE // 2,
                width,
                height
            )


        if self.facing == "up":

            return pygame.Rect(
                self.x - width // 2,
                self.y
                - DISPLAY_SIZE // 2
                - height,
                width,
                height
            )


        if self.facing == "right":

            return pygame.Rect(
                self.x + DISPLAY_SIZE // 2,
                self.y - height // 2,
                height,
                width
            )


        if self.facing == "left":

            return pygame.Rect(
                self.x
                - DISPLAY_SIZE // 2
                - width,
                self.y - height // 2,
                height,
                width
            )


    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        # ----------------------------------------------------
        # HURT
        # ----------------------------------------------------

        if self.action == "hurt":

            sprite = (
                june_sprites["hurt"]
                [self.facing]
                [self.frame]
            )

            rect = sprite.get_rect(
                center=(
                    self.x,
                    self.y
                )
            )

            surface.blit(
                sprite,
                rect
            )

            return


        # ----------------------------------------------------
        # OBTAIN
        # ----------------------------------------------------

        if self.action == "obtain":

            sprite = (
                june_sprites["obtain"]
            )

            rect = sprite.get_rect(
                center=(
                    self.x,
                    self.y
                )
            )

            surface.blit(
                sprite,
                rect
            )

            return


        # ----------------------------------------------------
        # ATTACK
        # ----------------------------------------------------

        if self.action == "attack":

            sprite = (
                june_attack_sprites
                [self.facing]
                [self.frame]
            )

            rect = sprite.get_rect(
                center=(
                    self.x,
                    self.y
                )
            )

            surface.blit(
                sprite,
                rect
            )

            return


        # ----------------------------------------------------
        # NORMAL
        # ----------------------------------------------------

        sprite = (
            june_sprites
            [self.facing]
            [self.frame]
        )

        rect = sprite.get_rect(
            center=(
                self.x,
                self.y
            )
        )

        surface.blit(
            sprite,
            rect
        )


# ============================================================
# PROJECTILE
# ============================================================

class Projectile:

    def __init__(
        self,
        x,
        y,
        direction
    ):

        self.x = x
        self.y = y

        self.direction = direction

        self.frame = 0
        self.frame_timer = 0

        self.alive = True


    def update(self, dt):

        if self.direction == "up":

            self.y -= (
                BALL_SPEED * dt
            )

        elif self.direction == "down":

            self.y += (
                BALL_SPEED * dt
            )

        elif self.direction == "left":

            self.x -= (
                BALL_SPEED * dt
            )

        elif self.direction == "right":

            self.x += (
                BALL_SPEED * dt
            )


        self.frame_timer += dt

        if (
            self.frame_timer
            >= 1 / BALL_FPS
        ):

            self.frame_timer = 0

            self.frame = (
                self.frame + 1
            ) % 3


        margin = 100

        if (
            self.x < -margin
            or self.x > SCREEN_WIDTH + margin
            or self.y < -margin
            or self.y > SCREEN_HEIGHT + margin
        ):

            self.alive = False


    def draw(self, surface):

        sprite = ball_sprites[
            self.frame
        ]

        rect = sprite.get_rect(
            center=(
                self.x,
                self.y
            )
        )

        surface.blit(
            sprite,
            rect
        )


# ============================================================
# MONSTER
# ============================================================

class Monster:

    def __init__(
        self,
        monster_type
    ):

        self.monster_type = monster_type

        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

        self.frame = 0
        self.frame_timer = 0

        self.action = None
        self.action_timer = 0

        self.facing = random.choice(
            [
                "up",
                "down",
                "left",
                "right"
            ]
        )

        self.direction = self.facing

        self.direction_timer = random.uniform(
            MONSTER_DIRECTION_MIN_TIME,
            MONSTER_DIRECTION_MAX_TIME
        )

        self.shoot_direction = "down"

        # Practice combat.

        self.hp = PRACTICE_MONSTER_HP

        self.hit_cooldown = 0

        self.death_frame = 0
        self.death_timer = 0

        self.defeated = False


    # ========================================================
    # CHOOSE DIRECTION
    # ========================================================

    def choose_direction(self):

        self.direction = random.choice(
            [
                "up",
                "down",
                "left",
                "right"
            ]
        )

        self.facing = self.direction

        self.direction_timer = random.uniform(
            MONSTER_DIRECTION_MIN_TIME,
            MONSTER_DIRECTION_MAX_TIME
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

            self.y -= MONSTER_HURT_PUSHBACK

        elif self.facing == "up":

            self.y += MONSTER_HURT_PUSHBACK

        elif self.facing == "left":

            self.x += MONSTER_HURT_PUSHBACK

        elif self.facing == "right":

            self.x -= MONSTER_HURT_PUSHBACK


        half_size = (
            DISPLAY_SIZE // 2
        )

        self.x = max(
            half_size,
            min(
                self.x,
                SCREEN_WIDTH - half_size
            )
        )

        self.y = max(
            half_size,
            min(
                self.y,
                SCREEN_HEIGHT - half_size
            )
        )


    # ========================================================
    # PRACTICE DAMAGE
    # ========================================================

    def take_practice_damage(self):

        if self.defeated:
            return

        if self.hit_cooldown > 0:
            return

        self.hp -= 1

        self.hit_cooldown = (
            PRACTICE_DAMAGE_COOLDOWN
        )

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

        self.shoot_direction = random.choice(
            [
                "up",
                "down",
                "left",
                "right"
            ]
        )


    # ========================================================
    # UPDATE
    # ========================================================

    def update(
        self,
        dt,
        projectiles
    ):

        if self.hit_cooldown > 0:

            self.hit_cooldown -= dt

            if self.hit_cooldown < 0:

                self.hit_cooldown = 0


        # ----------------------------------------------------
        # DEATH
        # ----------------------------------------------------

        if self.action == "death":

            self.action_timer += dt

            frame_duration = (
                1 / MONSTER_DEATH_FPS
            )

            self.death_frame = int(
                self.action_timer
                / frame_duration
            )

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

                if (
                    self.action_timer
                    >= SOLDIER_HURT_DURATION
                ):

                    self.action = None
                    self.action_timer = 0
                    self.frame = 0

                return


            if self.monster_type == "cursed_tree":

                sequence = (
                    TREE_HURT_SEQUENCE
                )

            else:

                sequence = (
                    HURT_SEQUENCE
                )


            sequence_index = int(
                self.action_timer
                / HURT_FRAME_DURATION
            )


            if (
                sequence_index
                >= len(sequence)
            ):

                self.action = None
                self.action_timer = 0
                self.frame = 0

            else:

                self.frame = (
                    sequence[
                        sequence_index
                    ]
                )

            return


        # ----------------------------------------------------
        # TREE SHOOT
        # ----------------------------------------------------

        if self.action == "shoot":

            self.action_timer += dt

            self.frame = 1

            if (
                self.action_timer
                >= TREE_SHOOT_DURATION
            ):

                projectiles.append(
                    Projectile(
                        self.x,
                        self.y,
                        self.shoot_direction
                    )
                )

                self.action = None
                self.action_timer = 0
                self.frame = 0

            return


        # ----------------------------------------------------
        # TREE
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

            self.y -= (
                MONSTER_MOVE_SPEED
                * dt
            )

            self.facing = "up"


        elif self.direction == "down":

            self.y += (
                MONSTER_MOVE_SPEED
                * dt
            )

            self.facing = "down"


        elif self.direction == "left":

            self.x -= (
                MONSTER_MOVE_SPEED
                * dt
            )

            self.facing = "left"


        elif self.direction == "right":

            self.x += (
                MONSTER_MOVE_SPEED
                * dt
            )

            self.facing = "right"


        # ----------------------------------------------------
        # SCREEN BOUNDS
        # ----------------------------------------------------

        half_size = (
            DISPLAY_SIZE // 2
        )

        self.x = max(
            half_size,
            min(
                self.x,
                SCREEN_WIDTH - half_size
            )
        )

        self.y = max(
            half_size,
            min(
                self.y,
                SCREEN_HEIGHT - half_size
            )
        )


        # ----------------------------------------------------
        # WALKING
        # ----------------------------------------------------

        self.frame_timer += dt

        if (
            self.frame_timer
            >= 1 / MONSTER_WALK_FPS
        ):

            self.frame_timer = 0

            self.frame = (
                self.frame + 1
            ) % 2


    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        # ----------------------------------------------------
        # DEAD / POPPING
        # ----------------------------------------------------

        if self.action == "death":

            sprite = monster_pop_sprites[
                self.death_frame
            ]

            rect = sprite.get_rect(
                center=(
                    self.x,
                    self.y
                )
            )

            surface.blit(
                sprite,
                rect
            )

            return


        # ----------------------------------------------------
        # COMPLETELY DEFEATED
        # ----------------------------------------------------

        if self.defeated:

            return


        # ----------------------------------------------------
        # NORMAL
        # ----------------------------------------------------

        sprite = (
            monster_sprites
            [self.monster_type]
            [self.frame]
        )

        rect = sprite.get_rect(
            center=(
                self.x,
                self.y
            )
        )

        surface.blit(
            sprite,
            rect
        )


# ============================================================
# PRACTICE MODE
# ============================================================

class PracticeMode:

    def __init__(
        self,
        monster_type
    ):

        self.monster_type = monster_type

        self.june = June()

        self.monster = Monster(
            monster_type
        )

        # Put June and monster apart.

        self.june.x = (
            SCREEN_WIDTH // 2
            - 220
        )

        self.june.y = (
            SCREEN_HEIGHT // 2
        )

        self.monster.x = (
            SCREEN_WIDTH // 2
            + 220
        )

        self.monster.y = (
            SCREEN_HEIGHT // 2
        )

        self.projectiles = []

        self.red_flash_timer = 0

        self.finished = False
        self.completed = False


    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.__init__(
            self.monster_type
        )


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


        attack_hitbox = (
            self.june.get_attack_hitbox()
        )


        monster_rect = pygame.Rect(
            self.monster.x
            - DISPLAY_SIZE // 2,

            self.monster.y
            - DISPLAY_SIZE // 2,

            DISPLAY_SIZE,
            DISPLAY_SIZE
        )


        if attack_hitbox.colliderect(
            monster_rect
        ):

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

        dx = (
            self.monster.x
            - self.june.x
        )

        dy = (
            self.monster.y
            - self.june.y
        )

        distance = (
            dx * dx
            + dy * dy
        ) ** 0.5


        if (
            distance
            <= PRACTICE_MONSTER_CONTACT_DISTANCE
        ):

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


        # ----------------------------------------------------
        # JUNE
        # ----------------------------------------------------

        self.june.update(
            dt,
            True
        )


        # ----------------------------------------------------
        # MONSTER
        # ----------------------------------------------------

        self.monster.update(
            dt,
            self.projectiles
        )


        # ----------------------------------------------------
        # ATTACK HIT
        # ----------------------------------------------------

        self.check_attack_hit()


        # ----------------------------------------------------
        # MONSTER CONTACT
        # ----------------------------------------------------

        self.check_monster_contact()


        # ----------------------------------------------------
        # PROJECTILES
        # ----------------------------------------------------

        for projectile in self.projectiles:

            projectile.update(dt)


        self.projectiles = [

            projectile

            for projectile in self.projectiles

            if projectile.alive

        ]


        # The monster has completed its full death/pop animation.
        # Mark the practice fight complete; the main loop will leave
        # practice mode only after this frame has been drawn.
        if self.monster.defeated:

            self.completed = True


    # ========================================================
    # DRAW
    # ========================================================

    def draw(self, surface):

        surface.fill(
            BACKGROUND_COLOR
        )


        # ----------------------------------------------------
        # PRACTICE MODE TITLE
        # ----------------------------------------------------

        title = font.render(
            "PRACTICE MODE",
            True,
            TEXT_COLOR
        )

        surface.blit(
            title,
            (20, 20)
        )


        monster_name = (
            self.monster_type
            .replace(
                "_",
                " "
            )
            .upper()
        )

        monster_text = small_font.render(
            monster_name,
            True,
            SUBTEXT_COLOR
        )

        surface.blit(
            monster_text,
            (20, 55)
        )


        # ----------------------------------------------------
        # HEARTS
        # ----------------------------------------------------

        if self.june.hearts > 0:

            heart_sprite = heart_sprites[
                PRACTICE_JUNE_HEARTS - self.june.hearts
            ]

            surface.blit(
                heart_sprite,
                (
                    20,
                    90
                )
            )


        # ----------------------------------------------------
        # MONSTER HP
        # ----------------------------------------------------

        if not self.monster.defeated:

            hp_text = small_font.render(
                "MONSTER HP: "
                + str(self.monster.hp)
                + " / "
                + str(PRACTICE_MONSTER_HP),
                True,
                TEXT_COLOR
            )

            surface.blit(
                hp_text,
                (
                    20,
                    165
                )
            )


        # ----------------------------------------------------
        # CONTROLS
        # ----------------------------------------------------

        controls = small_font.render(
            "WASD: Move | E: Attack | 0: Exit",
            True,
            SUBTEXT_COLOR
        )

        surface.blit(
            controls,
            (
                20,
                SCREEN_HEIGHT - 30
            )
        )


        # ----------------------------------------------------
        # DRAW PROJECTILES
        # ----------------------------------------------------

        for projectile in self.projectiles:

            projectile.draw(
                surface
            )


        # ----------------------------------------------------
        # DRAW MONSTER
        # ----------------------------------------------------

        if not self.monster.defeated:

            self.monster.draw(
                surface
            )


        # ----------------------------------------------------
        # DRAW JUNE
        # ----------------------------------------------------

        self.june.draw(
            surface
        )


        # ----------------------------------------------------
        # DEATH SCREEN
        # ----------------------------------------------------

        if self.june.hearts <= 0:

            overlay = pygame.Surface(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                ),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 160)
            )

            surface.blit(
                overlay,
                (0, 0)
            )


            death_text = font.render(
                "YOU DIED",
                True,
                TEXT_COLOR
            )

            death_rect = (
                death_text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 - 30
                    )
                )
            )

            surface.blit(
                death_text,
                death_rect
            )


            retry_text = small_font.render(
                "PRESS R TO TRY AGAIN",
                True,
                TEXT_COLOR
            )

            retry_rect = (
                retry_text.get_rect(
                    center=(
                        SCREEN_WIDTH // 2,
                        SCREEN_HEIGHT // 2 + 25
                    )
                )
            )

            surface.blit(
                retry_text,
                retry_rect
            )


        # ----------------------------------------------------
        # RED FLASH
        # ----------------------------------------------------

        if self.red_flash_timer > 0:

            flash = pygame.Surface(
                (
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT
                ),
                pygame.SRCALPHA
            )

            alpha = int(
                180
                * (
                    self.red_flash_timer
                    / RED_FLASH_DURATION
                )
            )

            flash.fill(
                (
                    255,
                    0,
                    0,
                    alpha
                )
            )

            surface.blit(
                flash,
                (0, 0)
            )


# ============================================================
# TEST ORDER
# ============================================================

test_order = [

    "june",
    "wolf",
    "spider",
    "tormented_soul",
    "cursed_tree",
    "hellish_spider",
    "hellish_hand",
    "demon",
    "soldier"
]

test_index = 0


# ============================================================
# MAIN STATE
# ============================================================

june = June()

monster = None

projectiles = []

practice_mode = None


if test_order[test_index] != "june":

    monster = Monster(
        test_order[test_index]
    )


# ============================================================
# RESET NORMAL TEST
# ============================================================

def reset_test():

    global june
    global monster
    global projectiles

    june = June()

    projectiles = []

    current_test = (
        test_order[test_index]
    )

    if current_test == "june":

        monster = None

    else:

        monster = Monster(
            current_test
        )


# ============================================================
# CONTROLS
# ============================================================

def get_controls():

    current_test = (
        test_order[test_index]
    )

    if current_test == "june":

        return (
            "WASD: Move | "
            "H: Hurt | "
            "O: Obtain | "
            "E: Attack"
        )

    if current_test == "cursed_tree":

        return (
            "H: Hurt | "
            "E: Shoot | "
            "P: Practice"
        )

    return (
        "H: Hurt | "
        "P: Practice"
    )


# ============================================================
# FONTS
# ============================================================

font = pygame.font.Font(
    None,
    32
)

small_font = pygame.font.Font(
    None,
    24
)


# ============================================================
# MAIN LOOP
# ============================================================

running = True


while running:

    dt = (
        clock.tick(FPS)
        / 1000.0
    )


    # ========================================================
    # PRACTICE MODE
    # ========================================================

    if practice_mode is not None:

        # Keep a local reference for this frame. This prevents the
        # practice object from becoming None halfway through a frame.
        current_practice = practice_mode

        # ----------------------------------------------------
        # EVENTS
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                running = False


            elif event.type == pygame.KEYDOWN:

                # --------------------------------------------
                # EXIT PRACTICE
                # --------------------------------------------

                if event.key == pygame.K_0:

                    practice_mode = None
                    reset_test()
                    continue


                # --------------------------------------------
                # RETRY AFTER DEATH
                # --------------------------------------------

                elif (
                    event.key == pygame.K_r
                    and
                    current_practice.june.hearts <= 0
                ):

                    current_practice.reset()


                # --------------------------------------------
                # ATTACK
                # --------------------------------------------

                elif (
                    event.key == pygame.K_e
                    and
                    current_practice.june.hearts > 0
                    and
                    not current_practice.completed
                ):

                    current_practice.june.attack()


        # ----------------------------------------------------
        # UPDATE / DRAW
        # ----------------------------------------------------

        if running and practice_mode is not None:

            previous_hearts = current_practice.june.hearts

            current_practice.update(dt)

            if (
                previous_hearts > 0
                and
                current_practice.june.hearts <= 0
            ):

                current_practice.red_flash_timer = (
                    RED_FLASH_DURATION
                )

            current_practice.draw(screen)

            pygame.display.flip()

            # Only leave practice mode AFTER the completed frame has
            # been drawn. By this point the three pop frames have
            # already finished and the monster is no longer drawn.
            if current_practice.completed:

                practice_mode = None
                reset_test()

        continue


    # ========================================================
    # NORMAL TEST MODE
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False


        elif event.type == pygame.KEYDOWN:

            # ------------------------------------------------
            # PREVIOUS TEST
            # ------------------------------------------------

            if event.key == pygame.K_LEFT:

                test_index -= 1

                if test_index < 0:

                    test_index = (
                        len(test_order)
                        - 1
                    )

                reset_test()


            # ------------------------------------------------
            # NEXT TEST
            # ------------------------------------------------

            elif event.key == pygame.K_RIGHT:

                test_index += 1

                if (
                    test_index
                    >= len(test_order)
                ):

                    test_index = 0

                reset_test()


            # ------------------------------------------------
            # ENTER PRACTICE MODE
            # ------------------------------------------------

            elif (
                event.key == pygame.K_p
                and
                test_order[test_index]
                != "june"
            ):

                practice_mode = PracticeMode(
                    test_order[test_index]
                )


            # ------------------------------------------------
            # JUNE TEST
            # ------------------------------------------------

            elif (
                test_order[test_index]
                == "june"
            ):

                if event.key == pygame.K_h:

                    june.hurt()

                elif event.key == pygame.K_o:

                    june.obtain()

                elif event.key == pygame.K_e:

                    june.attack()


            # ------------------------------------------------
            # MONSTER TEST
            # ------------------------------------------------

            else:

                if event.key == pygame.K_h:

                    monster.hurt()

                elif (
                    event.key == pygame.K_e
                    and
                    test_order[test_index]
                    == "cursed_tree"
                ):

                    monster.shoot()


    # ========================================================
    # UPDATE NORMAL TEST
    # ========================================================

    current_test = (
        test_order[test_index]
    )


    if current_test == "june":

        june.update(dt)

    else:

        monster.update(
            dt,
            projectiles
        )

        for projectile in projectiles:

            projectile.update(dt)


        projectiles = [

            projectile

            for projectile in projectiles

            if projectile.alive

        ]


    # ========================================================
    # DRAW NORMAL TEST
    # ========================================================

    screen.fill(
        BACKGROUND_COLOR
    )


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    title = font.render(
        "FAITH 8BIT - Sprite Test",
        True,
        TEXT_COLOR
    )

    screen.blit(
        title,
        (20, 20)
    )


    # --------------------------------------------------------
    # CURRENT TEST
    # --------------------------------------------------------

    current_name = (
        current_test
        .replace(
            "_",
            " "
        )
        .upper()
    )

    test_text = font.render(
        "TEST: " + current_name,
        True,
        TEXT_COLOR
    )

    screen.blit(
        test_text,
        (20, 55)
    )


    # --------------------------------------------------------
    # CONTROLS
    # --------------------------------------------------------

    controls = small_font.render(
        get_controls(),
        True,
        SUBTEXT_COLOR
    )

    screen.blit(
        controls,
        (
            20,
            SCREEN_HEIGHT - 45
        )
    )


    navigation = small_font.render(
        "LEFT / RIGHT: Change Test",
        True,
        SUBTEXT_COLOR
    )

    screen.blit(
        navigation,
        (
            20,
            SCREEN_HEIGHT - 22
        )
    )


    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    if current_test == "june":

        june.draw(
            screen
        )

    else:

        monster.draw(
            screen
        )

        for projectile in projectiles:

            projectile.draw(
                screen
            )


    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()


# ============================================================
# CLEANUP
# ============================================================

pygame.quit()
sys.exit()