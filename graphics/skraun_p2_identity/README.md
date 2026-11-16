# THE SKRAUN - GRAPHICS P2 / Identity Silhouette Proof

**Authority:** MAIN II bounded design-only [order](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_GRAPHICS_P2_SKRAUN_IDENTITY_SILHOUETTE_PROOF_AUTHORIZED_2026-11-16.md), [issue #20](https://github.com/Odourman/the-skraun/issues/20).

**Status: DESIGN PREVIEW ONLY, NOT STELLA, NOT FINAL ART. Exactly two new 8×12 sprites; P1-A is unchanged benchmark.** The owner's original hand-drawn photograph was reviewed privately in Drive; it is not copied to this package or GitHub.

## Read in order (L1 FIRST)

- `01_L1_NATIVE_160x192_UNENHANCED.png`: exact original native 160 color-clock by 192-line flattened glyphs on all three candidates, both poses; actual glyph area is only 8×12. NO rescaling of the arena pixels.
- `02_L1_TV_4x3_NATIVE_COMPARISON.png`: fixed 160×192 native mock screen nearest-neighbor to 640×480 for approximate NTSC 4:3. All three candidates, both frames. Not Stella.
- `03_BLACK_WHITE_SOURCE_SILHOUETTES.png`: monochrome shapes, larger only to inspect binary outlines. The tiny real-size test takes precedence.
- `04_EXACT_BITMAPS_BOTH_FACINGS.png`: all top-first exact 8×12 rows of the old P1-A and two new sprite families in both poses and both facings.
- `05_L2_L3_CONCEPTUAL_LEVELS.png`: three historical scale modes: L1=8cc×12 lines (in above files), L2=16cc×24, L3=32cc×36. **The real ART1 L3 defect (#19) remains unfixed.** These are purely theoretical expansions.
- `06_L1_FOREST_NIGHT_FLAT_BACKGROUND.png`: constant forest/night colors, not PF/renderer tests.
- `07_GAIT_BITS_BOTH_POSES.png`: A/B changed cells in amber purely as an explanatory overlay (not source colors).
- `08_ANATOMY_HYPOTHESIS_NOT_VISUAL_PROOF.png`: intended holes and open-mouth notch. These geometric annotations do NOT prove character identity at native size.
- `NATIVE_8x12_*.png`: exact six raw 8×12 glyph PNGs, with no scaling, both poses.
- `09_GIF_P1_A_FROZEN.gif`, `10_GIF_I1_HEAD.gif`, `11_GIF_I2_LIMBS.gif`: equally paced 2-frame, 133ms per pose mock loops (8 simulated NTSC frames per pose), fixed centered position, conceptual 4:3, not real Stella.
- `P2_SPRITES_SOURCE.json`, `P2_BITMAPS_GRAPHICS_ONLY.inc`: original 8-bit rows, true mirrors, anatomical intentions, historical source hash, all sizes, exact diff cells. The include file contains **only data bytes**, no runnable code. Not drop-in to any old descending raster table.
- `generate_previews.py`, `validate_p2.py`: deterministic image generation and non-game checks; requires Python and Pillow.
- `MAIN_II_P2_HANDOFF.md`: one decision-oriented comparative report.
- `SHA256SUMS.txt`: expected hashes for every other member of the ZIP.

## Provenance and constraints

Frozen baseline P1-A source: `graphics/p1-horizontal-axis-perspective-proof-20261116/graphics/skraun_p1_horizontal_axis/SKRAUN_P1_PIXEL_MASKS.json` on GitHub; exact original source SHA256 `bf818ec4b998fa66c2ab1db26a637e807737f830efab04854219ab14b9dd99b0`. Binary `A`+`B` row-set hash (canonical UTF-8 JSON) `b69419965ff4c6e350c02b1360958aa99f3e35a95734cf07dee1db1e8083921b`. B is unchanged too.

Technical precedent: P01-ART1 actual Stella v6.7.1 3 ROM × 3 sizes × 2 facings × 2 poses, 24/36 pixel exact (L1/L2), L3 12/12 failed one scanline; isolated test did not demonstrate original sketch identity. We directly read the real report and original ART1 ZIP of screenshots from Google Drive **as reference only**. Those emulator screenshots and source ROMs are not reproduced in P2. No Stella or ROM run for I1/I2 has been performed.

The 160×192 raster is approximated as 640×480 nearest-neighbor (4 output pixels per color clock; vertical nearest-neighbor ~2.5 output pixels per scanline) to compare, not to assert precise CRT phosphor geometry. Proposed light gray `#CAD2D5` is a studio RGB mock; actual Stella ART1 gray is 210,210,209 for COLUP0=$0C. Forest `#13261E` and night `#0A1423` are flat sample backgrounds only.

To reproduce: in this folder run `python generate_previews.py`, then `python validate_p2.py`. To check the original ZIP without regenerating, extract files and run validator. **The source validator PASS does not mean aesthetic identity PASS.** External ZIP SHA-256 is reported in the MAIN II delivery message, not inside the archive (avoids circular checksum).

**Strict stop:** no P3, no art-approval, no extra 8×14, no ROM or `main` merge, no P01-ART1 bug repair, no R4/B3c, no independent verification, no change to halo/worlds/enemies/gameplay. MAIN II controls any next decision.
