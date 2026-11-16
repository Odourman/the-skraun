# THE SKRAUN – GRAPHICS P3-F1 post-research release (2026-11-16)

**Only new candidate families: D1_head_expression and D2_swaying_arms.** P3 U1 is frozen as a control. The earlier P3-F1 package (SHA-256 `53adadae16e9698cc38a6083abc62101455ded8438e1e0d9b02d530452d47ef6`) predates MAIN II's research HOLD and remains unchanged as historical evidence. This distinct archive is the **single post-research submission**, not permission for additional P3-F1 iterations.

**Design only / not Stella / no ROM / no art approval.** The user's original photograph was inspected privately from Google Drive; it is not here or in public GitHub. The game camera is overhead but the character stands upright with head/horns above arms and feet; only horizontal left/right visual facing, no separate vertical sprites.

## MAIN II review order

1. `00_BLIND_L1_UNLABELED.png` FIRST. Twelve randomly ordered, unlabeled views (except sample number), at 4:3 TV-approximate native level-1 scale. No human blind-viewer responses have been collected.
2. `01_BLIND_ANSWER_KEY.md` AFTER attempting the visual test.
3. `02_L1_LABELED_IDENTICAL_SCALE.png` shows U1, D1, D2, two poses and two facings, identically presented.
4. `03_L1_NATIVE_160x192.png` and `04_L1_FULL_4_3_TV.png` are full-size 160 color-clock x 192 scanline source rasters and 640x480 nearest-neighbor 4:3 approximations. Original sprite is 8x12, not 8x12 LCD square pixel aspect ratio.
5. `05_EXACT_SOURCE_MATRICES.png`, `06_BLACK_WHITE_SILHOUETTES.png`, `08_GAIT_SOURCE_DIFFS.png`, `09_STABLE_FACING_SOURCE.png` are *enlarged source-audit imagery only*, never evidence of natural-size readability.
6. `07_LEVELS_1_2_3_CONCEPTUAL.png` illustrates 8x12, 16x24, 32x36; *not* a Stella test, and ART1 L3 defect #19 remains.
7. `10_L1_FOREST_NIGHT_FLAT.png` illustrates only flat contrast, not world playfields or collisions.
8. `GIF_*.gif` are U1/D1/D2 two-frame loops for both facings, 140 ms per frame; `NATIVE_8x12_*.png` are exact raw pixel-grid images.

## Machine-readable sources and reproducibility

`SOURCE_8x12.json` is authoritative for the candidate bits: top-first row zero is the horns; left-facing rows are each bit-reversed; bit7 is the screen's leftmost pixel. `PIXEL_DATA_ONLY.inc` contains *only* 8-bit `dc.b` graphical row data with explicit `TOP_FIRST`/`BOTTOM_FIRST` forms and no runnable code. No M0, missile, NUSIZ mode change, extra colors or extra sprite.

With Python 3 and Pillow, inside the directory:

```
python generate_previews.py
python audit_hamming.py
python generate_bitmap_tables.py
python validate_package.py
python package_release.py
```

`SOURCE_DISTANCE_AUDIT.json` contains a full pairwise 4x4 bit Hamming matrix; **bit differences do not constitute human recognition.** All other files are SHA-256-listed in `SHA256SUMS.txt` (the manifest itself omitted to avoid circular hashing). `validate_package.py` checks exact file bytes in manifest; after source changes in a future *separately authorized* design job the manifest would have to be independently regenerated. P3-F1 is stopped now.

MAIN II result and user-facing risks in `MAIN_II_POST_RESEARCH_HANDOFF.md`.
