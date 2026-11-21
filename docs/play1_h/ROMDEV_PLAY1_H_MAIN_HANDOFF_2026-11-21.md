# THE SKRAUN – ROM DEVELOPMENT II → MAIN III: PLAY1-H frozen physical Y-follow, X counterexample

**Date:** 2026-11-21. **Result: PLAY1_H_PARTIAL (DEVELOPER_OBSERVED)**, not an independently verified PASS. This is one authorized PLAY1-H implementation; issue #36. No N8/N9, changed mapper, sprite production, unapproved gameplay concession or main merge.

## 1. Provenance and exact artifacts

MAIN III authorization: https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_PLAY1_H_MOVING_VISIBLE_HALO_AUTHORIZED_2026-11-21.md

- Frozen original PLAY1 PR #35 source basis: commit 8247a3ba2b723c88336b63d5666503bed72cf2af, 4 KiB ROM SHA256 cbc296309d60a35debb7bd6980ea5f61db5101bff48c4397f4c5569a8d33aedd.
- Isolated new branch: experiment/play1-h-moving-visible-halo-20261121. Draft PR #37 targets frozen PLAY1 experiment branch, stays DRAFT/UNMERGED.
- **Final PLAY1-H ASM:** experiments/play1_h_single_arena.asm, SHA256 **0aa5cf5d14e1eba0b786965fe316327810de01d36a4a32202651e06f36255c16**.
- **Final actual 4096-byte ROM:** experiments/play1_h_single_arena.bin, SHA256 **6e5e203ff2715fac650b76a620bc1e3e3b0084d67e82452842edd7b5e1903bca**.
- Actual DASM listing, symbols, build log and SHA256 manifest: experiments/play1_h_single_arena.lst, .sym, experiments/play1_h_DASM_BUILD.log and experiments/play1_h_SHA256SUMS.txt.
- Rebuild exact ROM using: dasm experiments/play1_h_single_arena.asm -f3 -oexperiments/play1_h_single_arena.bin -lexperiments/play1_h_single_arena.lst -sexperiments/play1_h_single_arena.sym; then sha256sum -c experiments/play1_h_SHA256SUMS.txt.
- Real reproducible Stella debugger gameplay: scripts/play1h_stella_abc.sh, tests/play1h_pixels.py, GitHub Actions workflow .github/workflows/play1h-real.yml. **The fail-closed final eight-scenario run is #44920971754**, completed SUCCESS including pixel oracle with explicit set -euo pipefail; original 50-entry Actions ZIP sha256 **a81be0452a36dcd4b949b334d7415c74d91922d554b7d5f90e2a3575f2a478e6** (CRC PASS). Exact compiled ROM and ASM hashes confirmed from ZIP, not assumed.
- Prior X-mirror **NEGATIVE** captured in actual Stella run #44920592381 on temporary commit c16c2c2667ef476943d3c6f09ffe80820124fb42. X-candidate was deliberately **reverted**; no such code remains in final ROM.

## 2. Concrete physical Stella pixel observations (320x228 original TIA pane)

Stella 6.7.1 on Ubuntu-24.04 Xvfb, real original 6507 ASM ROM; joystick/FIRE commands in authentic Stella Debugger autoexec, **no RAM injection for gameplay**, all eight cases display NTSC*. Screenshot files are actual debugger GUI and cropped TIA pixels, original 1400x1000 desktop / 320x228 TIA RGB.

| Case | Physical P0 bbox (TV pixels, half-open) | R3 P1 blue pixels | Gold PF pixels |
|---|---|---:|---:|
| baseline L1 / FIRE OFF | (146,114,162,126), 16x12 |120|0|
| pickup_L2_off, true BL orb pickup | (172,132,204,156), 32x24 |120|0|
| L1_on FIRE | (146,114,162,126), 16x12 |120|3744|
| L2_on FIRE | (172,132,204,156), 32x24 |120|4784|
| A_L3_on FIRE, after orb respawn | (156,126,220,162), 64x36 |0|5676|
| B_L3_right8 while FIRE | (172,126,236,162), 64x36 |0|5616|
| C_L3_right8_up8 while FIRE | (172,118,236,154), 64x36 |0|5632|
| D_L3_right8_down8 at lower obstacle | (172,128,236,164), 64x36 |0|5632|

The final TIA A→B physically moves P0 +16 TV horizontal pixels (8 game x), A→B P0/P1-occlusion-masked **gold ring differences 0**: **visible X-follow FAIL**. B→C moves P0 up 8 actual scanlines. The non-occluded gold PF mask changes **1516 pixels** in bbox [96,106,224,173]: **Y-follow physically observed**. A fixed-upper-obstacle gold row y60 has 0 changes: preserved world geometry. B→D move DOWN was limited to 2 TV/scanline pixels from obstacle, demonstrating at least one Level3 full-body block, while B→C UP8 is freely traversable. Original R3 P1 exactly 120 bright blue physical pixels before kill and 0 after; FIRE while L3 erases dummy without P0 loss. Original U1-LEG1 P0 16x12/32x24/64x36 on original Stella TV; no new sprites. Baseline blue world+BL 2832 pixels → consumed-orb L2 OFF 2816 (16 world-blue BL pixels disappear), no erroneous extra PF gold OFF; the 90f controlled orb respawn permits genuine L3 contact, not SELECT debug.

Level-dependent gold PF area L1 3744 < L2 4784 < L3 5676 and real added PF2 bits beyond recolored scenery. **These are not proof of a fully satisfactory circle, nor physical X motion or all obstacle worst cases**. Ring center/X/range remains diagnostic and not user-approved final art.

## 3. Actual implementation and beam constraints

Instead of adding arithmetic into the already packed raster loop, PLAY1-H prepares signed PlayerY-dependent pointer in VBLANK into level-baked 193-row PF2 ROM tables (L1 F820, L2 FB30, L3 FE40), and selects a full 193-byte OFF-zero strip beginning FF01 to avoid aliasing hidden BL/halo into L3. Distinct zero guard prevents the first physical regression failure observed in a prior candidate (L2 OFF P0 32x34 and P1 144/120). TIA static mirrored synthetic PF obstacles are reproduced bit-exactly from PlayPF1 via PF1 AND $80 for PF0, reducing source work two cycles per row; BL shown/hidden by preselected ROM pointer; original P0 gait/size and R3 P1 masks intact.

**SOURCE_STATIC critical scanline, not a Stella instruction-by-instruction trace** after the visible STA WSYNC:
- Write GRP0 around CPU cycle 3 (preloaded from prior row).
- PF1 c10; PF0 c15, from same original playfield source mask.
- PF2 c27 or c28 depending (HaloRowPtr),Y crossing; GRP1 c34/35; ENABL c42..44 depending (OrbRowPtr),Y crossing.
- Indirect indexed loads and display-source pixel decisions also have conditional branches/page crossings. Conservatively the combined worst visible row may reach **~77/76 CPU cycles** when all relevant page crossings coincide. **Do not call this a complete worstcase beam or 262-row proof** on source-only bounds; all eight actual screenshot states show Stella NTSC* and source sprite correctness. Need an independently measured all-positions beam/path audit before full engine integration; not within PLAY1-H authorization.
- RIOT static variable footprint $80..$A9 inclusive **42 bytes**, plus maximum 4 return stack bytes statically derived from 2-level JSR nesting, **NOT** actual Stella live stack highwater. No mapper/extra RAM.

## 4. Negative X counterexample, preserved honestly

At temporary test commit c16c2c..., changing CTRLPF mirror to repeat for PlayerX≥100 caused gold geometry X variation, **but** genuine Stella showed 64 changed pixels in an *upper solid obstacle row* where scene geometry must remain unchanged; L2 P0 bbox 32x34 (must 32x24) and P1 blue pixels 144 (must 120). The attempt is **REJECTED AND REVERTED**. That is not proof a TIA X/Y halo cannot work, only that this simple X reflection shortcut destroys approved PLAY1 scene sprites/obstacles and must not be merged. Earlier B3b 16-frame stepping remains explicitly rejected.

## 5. Exact decision MAIN III needs

**PLAY1_H_PARTIAL**: Y follow works in actual Stella and gameplay remains working in sampled 8 scenes. Full physical 360° halo following both X and Y **FAIL in this tested implementation**, because X remains unchanged after P0 actually moves +8. Main III may accept bounded negative X and physical positive Y, or separately define a new narrow architectural decision. This report is a final delivery and STOP, **not authorizing another renderer or N8/N9**. No independent Verification is claimed and old N7 read-only verification #33 remains separate.
