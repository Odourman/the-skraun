# THE SKRAUN – GRAPHICS v0.2 (2026-11-16)

**DESIGN CANDIDATES ONLY; not MAIN-approved, not Stella tested, no ROM code, no R4/B3c, no merge and no independent VERIFICATION.**

MAIN authorization: [v0.2 visual refinement](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_V0_2_VISUAL_REFINEMENT_2026-11-16.md).

## Verified full deliverable on Google Drive

**[Download complete ZIP with 20 files, all PNGs and GIFs, source JSON and assembler art](https://drive.google.com/file/d/13lmZX_SbFm27fceYJuE0DdYiZhO7U2q_/view)**.

- File name: `THE_SKRAUN_GRAPHICS_V0_2_2026-11-16.zip`
- Exact bytes: `314330`
- SHA-256 (verified by readback of actual downloaded Drive bytes): `17227108204134d2fc3cb3dccad69f7633d8d092dd824aa6172bd88c09e9f9ff`
- Drive folder: [visual reference and sprites](https://drive.google.com/drive/folders/1udBPud9jpVzvMevcgKL8duib94GyV_yJ)
- Remote ZIP was downloaded back from Drive and its SHA-256 matched the local build.

## Source files mirrored here

- `skraun_sprites_v02.json`: unaltered v0.1 C and new C-refined/C-overhead, A/B poses, exact left-right reflection; 8×12 logical top-first.
- `enemy_sprites_v02.json`: knight idle/raised sword; green archer idle/draw.
- `worlds_playfield_40x24.json`: four worlds × two 40-cell reflective PF raster maps each; 24 × 8-scanline bands.
- `halo_masks_and_metrics_v02.json`: original static v0.1 halo, exactly two aesthetic alternatives, measured footprint/clipping.
- `SKRAUN_GRAPHICS_V02_DATA.inc`, `ENEMIES_GRAPHICS_V02_DATA.inc`: top-first AND bottom-first `dc.b` bitmap tables only. **Not drop-in for the 177-indexed R3-VFIX raster kernel.**

All illustrations (8 PNGs), two GIF A/B pose animations, decision report, README, internal hashes and validation script are in the **complete Drive ZIP**. Original user's hand drawing remains private in Drive and is **not mirrored here**.

## Recommended MAIN visual choice

**C-overhead** as next aesthetic baseline; less frontal face, more longitudinal body, side front limbs and rear feet. **C-refined** is closer to original expressive C but remains notably frontal. Neither is final-approved. Review the actual pixel-scale panels, not merely enlarged portraits.

Atari logical canvas: 160 color clocks × 192 visible scanlines. 8-bit P0 scaled at level 1/2/3 to 8/16/32 clocks × 12/24/36 lines, as *candidate* NUSIZ and row-repeat. NTSC display ratio represented by a 4:3 approximation, not measured CRT.

## Technical honesty

- v0.1 level-3 halo: **88 color clocks × 176 scanlines** = 91.7% of a 192-line arena, 8 scanlines top/bottom center margin. User-approved attack reach is NOT defined by these art masks.
- R3 48-clock × 72-scanline diagnostic is a non-equivalent separate experiment.
- Same-PF-pixel halo+obstacle colors unresolved, three same-Y P1 enemies only ~20 Hz in R3, 2–4 estimated spare cycles on worst lines; no graphical redesign resolves these automatically.
- No Stella screenshot, no renderer integration, no new gameplay rules in this package. Issue #15 remains open.
