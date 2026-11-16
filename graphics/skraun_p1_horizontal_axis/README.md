# THE SKRAUN – GRAPHICS P1: Horizontal Axis Perspective Proof

**2026-11-16 – DESIGN-ONLY PERSPECTIVE STUDY – STOP AFTER THIS DELIVERABLE.**

Authority: https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_P1_HORIZONTAL_AXIS_PERSPECTIVE_PROOF_2026-11-16.md

## One bounded experiment

Two new art candidates only. The verified v0.3 `Q1_splayed_quad` is a **fixed reference**, not a third new candidate. The two crude MAIN H1/H2 tests informed the hypothesis but were NOT used as accepted art. The original sketch stayed private in Google Drive: it was inspected as a character/anatomy reference and is **not bundled or uploaded publicly**.

**A – rounded back:** short paddle-like fore and hind paws; two eyes as negative head pixels; ears/horns reduced to upper/lower head contour. Better non-humanoid shape but **turtle/beetle risk**.

**B – long low back:** slightly narrower trunk, smaller snout tip at right, more separate paws; **insect risk** at level1.

Both are 8×12 logical mono bitmap, right-facing head toward bit0, rear to bit7; exact horizontal mirrors for left; 2 A/B poses changing upper and lower feet, 3 historical scaling modes NUSIZ0 0/5/7 with 12/24/36 line conceptual repeats. 8 joystick directions stay gameplay only; no additional art directions.

## Read this package in order

1. `00_MAIN_DECISION_SHEET.png`: Q1 versus A/B, exact grid and native-size 4:3 forest preview.
2. `01_ANATOMICAL_8x12_BITMASKS.png`: two poses and foot/body/head labels.
3. `02_BLACK_WHITE_SILHOUETTES.png`: shape without gray/forest color advantage.
4. `03_ALL_THREE_LEVELS_NTSC.png`: 1x,2x,4x NUSIZ horizontal and 1x,2x,3x vertical height.
5. `04_AB_AND_EXACT_MIRRORS.png`: right/left exact bit reflections in both poses.
6. `05_FOREST_NIGHT_CONTRAST.png`: all levels against fixed forest/night shades only.
7. `06_GAIT_DIFFERENCES.png`: exact changed bit locations (annotation-only colors).
8. `07_*.gif`: two-frame artist-only walks. Animation pacing is a display proposal, NOT actual game frame timing.
9. `SKRAUN_P1_PIXEL_MASKS.json`: original exact pixel source, mirrors, diff cells, coordinate-labelled anchors, metadata, Q1 reference.
10. `SKRAUN_P1_GRAPHICS_ONLY.inc`: assembler-friendly top-first and bottom-first data with **no executable code**.
11. `verify_p1.py`: kinematic source-data checks, PNG/GIF integrity, manifest integrity – NOT Stella.
12. `MAIN_P1_DECISION.md`: complete candid evaluation and stop recommendation.

## Precise source format

- 8 bits per row, 12 logical rows per pose; `bit7=LEFT`, `bit0=RIGHT`. Bit `1` draws gray pixel.
- `row0` is upper limb region, NOT head; `row11` is lower limb region, NOT hind feet.
- Right-facing head lies at `x=6..7, y=4..8` and two separate eye holes at `(6,5)` and `(6,7)` where visually possible.
- Upper/lower rear foot anchors are near x=1; upper/lower front foot anchors near x=4–5. Body axis is left-to-right.
- Horizontal mirror is 8-character row reversal, not vertical flip.
- Preserve prior historical sprite orientation regression as-is. New semantics would need NEW tests if an independently authorized ROM task later integrates this concept.

## Honest limitations

1. Side-facing topdown quadruped silhouette is **more plausible than Q1**, but neither candidate proves the troll still looks like the user-drawn Skraun at level1. Eyes and ears are thin, no readable mouth. Both can look like a beetle or turtle.
2. 160x192 pixels are stretched to 640x480 with nearest-neighbor to approximate 4:3 (color-clock x4, scanline x2.5). This is NOT measured Stella CRT pixel shape.
3. Color #CAD2D5 is provisional studio gray, NOT NTSC Stella COLUP0 signoff. No new game code, scanline or scheduler claims.
4. R3 20 Hz same-Y fiends, tiny remaining raster cycle budget and halo-PF color conflict remain unresolved and outside P1 scope.

**No ROM development, R4, B3c, gameplay changes, main merge, issue #15 closure or independent verification.**
