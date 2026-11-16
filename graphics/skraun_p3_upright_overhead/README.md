# The Skraun — GRAPHICS P3: Upright Overhead Character Proof

**Design only. No ROM. No Stella. No final aesthetic acceptance.** Date: 2026-11-16.

## Authority

The user's direct P3 / MAIN II instruction supersedes the *horizontal-prone body-axis* assumption of P1/P2 for visual interpretation: **standing upright at all times, viewed overhead, exactly two visual facings (R + exact L mirror); joystick up/down reuses existing facing**. Original 01–60 game decisions, previously frozen sources, original image privacy and other systems are unchanged. Original photo reviewed from private Google Drive; intentionally **not distributed in ZIP or public GitHub**.

## Start here (actual level 1 first)

- `00_MAIN_II_P3_DECISION_SHEET.png`: four way qualitative comparison with *unzoomed 4:3 crop above enlarged, explicitly labeled, source bitmap below*.
- `01_L1_NATIVE_160x192.png`: 160×192 unscaled 1:1 color-clock native arena, two poses, no interpolation. 8×12 actual sprite pixels.
- `02_L1_TV_4x3_FULL_A_B.png`: nearest-neighbor full 4:3 reconstructed display from same arena.
- `03_L1_UNZOOMED_CONTEXT_CROPS.png`: direct native-display crops **without further enlargement**. Not a tiny poster pretending to show detail.
- `04_BLACK_WHITE_SILHOUETTES_ENLARGED.png`: enlarged **source** binary outlines (not player-on-TV size).
- `05_EXACT_8x12_ROWS_ALL_DIRECTIONS.png`: four source groups × two poses × two mirror facings, exact bit labels.
- `06_ALL_THREE_LEVELS_CONCEPTUAL.png`: L1 8×12; L2 16×24; L3 32×36 mockup. Original L3 Stella defect remains #19.
- `07_L1_FOREST_NIGHT_FLAT.png`: flat backgrounds, not game renderer proof.
- `08_AB_GAIT_BIT_DIFFERENCES.png`: yellow annotation means changed bit, never additional source sprite color.
- `09_UPRIGHT_VS_PRONE_DIRECTION.png`: U1/U2 upright vs P1-A lying reinterpretation.
- `10_UP_DOWN_REUSES_SAME_TWO_FACINGS.png`: visual diagram for UP/DOWN motion using the **same** RIGHT/LEFT artwork, without authoring any UP/DOWN sprite.
- `NATIVE_8x12_*.png`: unscaled original 8×12 images, exact raw RGB pixels.
- `GIF_*.gif`: same frame duration 140ms across candidates and frozen controls, two-frame loops. Output is *design imagery, not Stella*.

## Reproduction

1. Install Python 3 and Pillow.
2. Run `python generate_previews.py` in the extracted directory; this writes all PNG/GIF deterministic previews from `P3_SOURCE_BITMAPS.json` (no original photo).
3. Run `python validate_p3.py` after extraction or after regeneration. Tests all source masks, nonexecutable `P3_GRAPHICS_ONLY_PIXEL_DATA.inc`, all generated PNG/GIF and SHA-256 manifest.
4. Run `python package_release.py` for a stable ZIP in parent directory after checks.

`P3_SOURCE_BITMAPS.json` contains **exactly two new** families: `U1_upright_face_priority`, `U2_upright_body_priority`, each 8×12 A/B and exact per-row reversed left. Frozen references `Q1_prior_best_upright` and `P1_A_negative_prone` are controls, **not** new candidates. `P3_GRAPHICS_ONLY_PIXEL_DATA.inc` contains only `dc.b %xxxxxxxx` art rows and labels in top-first and bottom-first forms; not an executable ROM patch. All files in `SHA256SUMS.txt` are hashed, except manifest itself to avoid circular hash.

## Conclusion and boundaries

**Upright composition improved; distinct Skraun identity and strict physically overhead viewing at L1 still NOT PROVEN.** U1 preserves the face but can read frontally; U2 improves posture/limbs but reads generic. Full explanation: `MAIN_II_P3_FINAL_REPORT.md`.

P3 ends here. No P4, v0.4, ROM, Stella, new dimensions, gameplay changes, independent VERIFICATION, merge, or issue closure.
