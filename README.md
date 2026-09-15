# FAITH 8BIT — Sprite Test

## Layout

```
FAITH_8BIT/
    ASSETS/                 <- your 4 .png spritesheets go here
    entities/
        __init__.py
        base.py              <- shared Entity base (position/facing/frame/bounds)
        june.py               <- June (player)
        monster.py             <- Monster (enemies + cursed tree shooting)
        projectile.py           <- Projectile (the tree's ball)
    assets.py                <- loads/scales sprites from ASSETS/
    config.py                <- every tunable constant
    game.py                  <- game state + event/update/draw flow
    practice_mode.py         <- 1v1 practice sandbox
    main.py                  <- entry point, run this
```

## Running it

```
cd FAITH_8BIT
python main.py
```

Drop your 4 spritesheets into `ASSETS/` first (see `ASSETS/README.txt`
for exact filenames). `assets.py` finds the folder relative to its
own location, so it works no matter what directory you launch from.

## What changed from the single-file version

- One 2,941-line script -> one file per responsibility (config,
  assets, each entity, game state, practice mode, entry point).
- No module-level globals — `Game` holds `june`/`monster`/
  `projectiles`/`test_index`/`practice_mode` as attributes instead
  of variables mutated via `global`.
- `June` and `Monster` now share an `Entity` base class for
  position/facing/frame bookkeeping and screen-bound clamping,
  instead of duplicating that logic in both classes.
- `get_sprite()`'s scale math now uses `NORMAL_SPRITE_SIZE` instead
  of a hardcoded `16`.
- Gameplay logic is otherwise unchanged — same constants, same
  animation timings, same combat/practice behavior.
