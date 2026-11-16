# GRAPHICS P3-F1: reproducible upright standing Skraun design-only proof

**Bounded authorization:** https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_GRAPHICS_P3_F1_UPRIGHT_FACING_READABILITY_AUTHORIZED_2026-11-16.md  
**Issue:** https://github.com/Odourman/the-skraun/issues/21  
**NO final sprite approval, ROM, Stella, game implementation, merges or independent VERIFICATION.**

## Read in this order

1. `00_BLIND_L1_UNLABELED.png` — 12 randomized but deterministic source states, unlabeled as to family, left/right or A/B, at identical actual L1 TV-approximation scale. Decide what you see FIRST.
2. `01_BLIND_ANSWER_KEY.md` — answer key deliberately separate. No actual user/person perception evaluation has yet been performed.
3. `02_L1_LABELED_SAME_SCALE.png` — exact same source-derived images now labeled.
4. `03_L1_NATIVE_160x192.png` — unscaled full playfield: 8x12 native sprite pixel dimensions.
5. `04_L1_FULL_4_3_SCREEN.png` — full 640x480 approximate TV render (nearest neighbor from 160x192), no invented antialias/blur.
6. `05_EXACT_8x12_GRIDS_ALL_STATES.png` — exact source-bit grids, all families including unchanged U1, A/B and L/R.
7. `06_BLACK_WHITE_SILHOUETTES_ZOOMED.png` — ONLY for audit. Not natural-size readability proof.
8. `07_L1_L2_L3_CONCEPTUAL.png` — L2, L3 conceptual scaling only (no repair to ART1 defect #19).
9. `08_GAIT_HIGHLIGHTS_SOURCE_ONLY.png`, `09_STABLE_FACING_CUES.png` — annotated changed bits; overlay colors are not sprite colors.
10. `10_FOREST_NIGHT_FLAT_CONTEXT.png` — flat backgrounds, not TIA PF implementation.
11. `NATIVE_8x12_*.png` — 12 actual tiny 8x12 sprite PNGs.
12. `GIF_*.gif` — 6 equally timed two-frame animations for U1, D1, D2 each in both directions.
13. `MAIN_II_P3_F1_HANDOFF.md` — candid aesthetic assessment and objective metrics.

## Reproduce (Python 3 + Pillow)

`python generate_previews.py`  
`python audit_hamming.py`  
`python validate_p3_f1.py`  
`python package_release.py`

The 8-bit source glyphs live in `P3_F1_SOURCE_BITMAPS.json`; `P3_F1_GRAPHICS_ONLY_DATA.inc` contains only `dc.b` pixel tables with explicit TOP_FIRST/BOTTOM_FIRST label and no CPU instructions. `HAMMING_AUDIT.json` includes full four-state difference matrices. `SHA256SUMS.txt` covers every other file, not itself (no circular checksum). To regenerate from JSON, run the first two commands before the validator; with an unchanged source, they should yield byte-identical images. When editing data for a *new authorized study*, regenerate the manifest separately; P3-F1 is final and must **not** be edited now.

Frozen original U1 is embedded unmodified for comparison. The real original drawing was privately inspected and is **NOT packaged**, reproduced, or publicly uploaded. Current color preview gray RGB(210,210,209); no hardware claim. Screen 160 color-clock columns ×192 scanlines approximated as 640×480 at 4:3; native sprite remains 8×12 source cells. L1, L2, L3 are 8×12, 16×24 and 32×36 conceptual source displays, respectively. Source bit7 corresponds to image x=0.

All rendered PNG/GIF images are **DESIGN PREVIEWS, NOT ACTUAL STELLA CAPTURES**. Face visibility can be symbolically frontal on an overhead PLAYFIELD as later MAIN II clarified; sprite itself must STAND UPRIGHT.
