"""
Central configuration for FAITH 8BIT.

All tunable constants live here so gameplay values can be
adjusted without touching entity or game logic.
"""

# ============================================================
# WINDOW
# ============================================================

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60


# ============================================================
# SPRITE SIZES
# ============================================================

NORMAL_SPRITE_SIZE = 16

# June and monsters are the same visual size.
DISPLAY_SIZE = 192
JUNE_DISPLAY_SIZE = DISPLAY_SIZE

JUNE_PIXEL_SCALE = DISPLAY_SIZE // NORMAL_SPRITE_SIZE


# ------------------------------------------------------------
# Attack
# ------------------------------------------------------------

JUNE_ATTACK_LOGICAL_SIZE = 32
JUNE_ATTACK_DISPLAY_SIZE = JUNE_ATTACK_LOGICAL_SIZE * JUNE_PIXEL_SCALE


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
MONSTER_DEATH_FPS = 8


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

HURT_SEQUENCE = [2, 1, 2, 1, 1]
TREE_HURT_SEQUENCE = [2, 0, 2, 0, 0]


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

RED_FLASH_DURATION = 0.25


# ============================================================
# COLORS
# ============================================================

BACKGROUND_COLOR = (25, 25, 25)
TEXT_COLOR = (255, 255, 255)
SUBTEXT_COLOR = (180, 180, 180)
RED_FLASH_COLOR = (255, 0, 0)


# ============================================================
# HEART DISPLAY
# ============================================================

HEART_DISPLAY_WIDTH = 128
HEART_DISPLAY_HEIGHT = 64


# ============================================================
# MONSTER SPRITE SHEET MAP
# ============================================================

MONSTER_COORDINATES = {
    "wolf": [(0, 0), (1, 0), (2, 0)],
    "spider": [(3, 0), (4, 0), (5, 0)],
    "tormented_soul": [(6, 0), (7, 0), (8, 0)],
    "cursed_tree": [(0, 1), (1, 1), (2, 1)],
    "hellish_spider": [(6, 1), (7, 1), (8, 1)],
    "hellish_hand": [(0, 2), (1, 2), (2, 2)],
    "demon": [(3, 2), (4, 2), (5, 2)],
    "soldier": [(6, 2), (7, 2), (8, 2)],
}

TEST_ORDER = [
    "june",
    "wolf",
    "spider",
    "tormented_soul",
    "cursed_tree",
    "hellish_spider",
    "hellish_hand",
    "demon",
    "soldier",
]
