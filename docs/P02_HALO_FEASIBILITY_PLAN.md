# The Skraun — P02 moving 360° halo: feasibility experiment plan

**Status:** Proposed technical research and prototype scope only; **NOT implemented or verified**.
**Date:** 2026-11-16
**Design authority:** MAIN decisions 01–60, especially decisions 01–04, 11–12, 35, 47–50.
**Prerequisite baseline:** P01 ROM, SHA-256 `7f27eb778247afe7ae0f8445d2654bad080ba36aee257ecb78692d9191ba5455`.
**P01 independent gate:** still OPEN (https://github.com/Odourman/the-skraun/issues/1).

## Non-negotiable behaviour

- The club is gone. Fire creates a magic, blinking **360-degree ring**, not a directional attack.
- The player can move freely while the halo lasts approximately 0.5 s.
- The ring thickness and outer reach increase with levels 1–3, with level 3 feeling overpowering.
- Enemy/projectile hit testing is a logical system separate from raster graphics. The visible radius and collision radius must be acceptably consistent.
- Obstacles do not block the magic halo.
- A prospective P02 solution must not silently erase the capacity needed for the troll, two knights and a green archer.

## Candidate drawing strategies to compare (NOT committed implementation choices)

| Candidate | Idea | Benefit | Primary risk |
| --- | --- | --- | --- |
| P1 sprite ring arcs | Use the second TIA player for raster-designed ring segments around P0 | Clear pixel art at levels 1–2 | A 32-pixel maximum wide-player shape may be insufficient at level 3, and P1 will later be needed for enemies |
| Dynamic playfield ring | Compose ring segments in the TIA playfield, recomputed around the troll | Does not permanently occupy P1 | 4-pixel coarse horizontal cells, PF register write timing, RAM/cycle budget and playfield decorations |
| Missile/ball + sparse segments | Use missile or ball objects for ring-side arcs while the kernel draws other segments | Can distribute horizontal/vertical arc tasks | Five primitive objects are also needed by projectiles and enemies; continuous full ring is difficult |
| Selective multiplexing | Alternate objects between raster regions or frames to keep the halo visible | More resources reusable across entities | Flicker and visual instability under worst-case enemy overlap |

Use actual Stella screenshots and debug timing to eliminate candidates. A visually attractive isolated halo is not enough if it cannot coexist with future enemies.

## Test matrix

1. Level 1, 2 and 3 halos: at least 12–20 stills at multiple x/y locations, including edges.
2. Halo active for approximately 0.5 s at 60 Hz (about 30 NTSC frames), then cooldown 1.0 / 0.6 / 0.25 s (provisional values as MAIN decision 48).
3. Move the troll diagonally with halo active; ring must follow without a noticeable lag, disconnect or extreme flicker.
4. Collision test independently from visuals: enemies at 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315° and at inside/outside the level-specific radius.
5. Confirm arrows intersecting the active halo disappear, independently of sprite rendering.
6. Synthetic stress: add two knights and an archer's placeholder graphics; note visible flicker and timing degradation.
7. Measure scanlines and 6502 cycles on actual Stella Debugger, not solely an abstract model; flag if the 262-line NTSC target is broken.

## Deliverable / decision gate

- Distinct experiments with 6502 source and reproducible ROM outputs; do not overwrite the original P01 baseline without explicit evidence.
- Comparative screen captures, profiler/cycle/scanline records, source+binary SHA-256, and known failure cases.
- A recommendation that considers future four-character rendering, not only isolated graphics.
- Independent VERIFICATION before treating any selected strategy as proven.

**No bank-switching size, exact halo pixel diameter, ring palette or rendering technique is being fixed by this plan.**
