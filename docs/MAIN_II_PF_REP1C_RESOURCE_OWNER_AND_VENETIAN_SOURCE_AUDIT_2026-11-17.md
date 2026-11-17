# THE SKRAUN — MAIN II PF-REP1C: TIA object-colour ownership and Venetian source study
**Date: 2026-11-17 | SOURCE-ONLY evidence, no ROM / Stella / independent Verification**

## Binding user goals
Continue toward a *real enjoyable original Atari 2600 game*: frozen approved gray U1-LEG1 original 8×12 A/B with corrected visual L/R direction labels, identical art enlarged at levels 1/2/3, very open eight maps allowing free Level3 movement, two recognizable sword knights + green fleeing archer (including same-Y worst case), circular gold attack halo that passes solid obstacles, solids stopping body/sword/arrow, orb, HUD/lives/score and minimal distracting flicker. No experimental convenience change to canonical visuals or mechanics silently accepted.

## Exact sources read
- [Current status](PROJECT_STATUS_2026-11-16.md) and [decisions](DESIGN_DECISIONS_01-60_2026-11-16.md); existing [R1 30 tricks review](R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md) and [MAIN 30 tricks graphical review](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md).
- [R3 actual assembler](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), exact blob `3c9ed79078eee6a0c63100614a593f92e240b5e8`; frozen [PF-REP1](MAIN_II_PF_REP1_SOURCE_SCREEN_AND_NEXT_DECISION_2026-11-17.md) and [PF-REP1B](MAIN_II_PF_REP1B_CONDITIONAL_TIA_WRITE_WINDOWS_2026-11-17.md) negative/cost evidence.
- Primary hardware: [1979 Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html), especially colours and player/missile/ball/NUSIZ; [Andrew Davie's asymmetric PF timing](https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-17.html); [Hugg 2025 versatile PF](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html) and [three-stream](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html).

## Original new quantitative study — verified
**Actual complete self-contained Google Drive ZIP:** [THE_SKRAUN_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_2026-11-17.zip](https://drive.google.com/file/d/1-MN_WleLizpnzK8u_2xaoAAsIgjJIWxM/view), **16,690 bytes**, exact **SHA256 `9b707a24395bb0f0597f1dbf4e5367d767b2a1fa8372003d7f93c1dc8a6959a7`**. It contains **8 members including 7/7 SHA256SUMS entries, ZIP CRC PASS**, complete actual 1979 TIA source references in report, original unchanged 13×halo/scenery source bytes and rowmap, two independent Python 3 stdlib test/control scripts, result JSON and deterministic package builder. **Actual test executed**, not planned. A truly CLEAN directory from copied source inputs reran both tests and rebuilt **all nine files (including ZIP) byte-for-byte identical**. Google Drive upload subsequently downloaded as raw ZIP and actual bytes/SHA256 compared identical to source original.

**Source scope:** `R3_SOURCE_EXACT_MASKS.json` from the original R3 blob. All 13 positions X56..104 by4, exact 177-byte row map and **88 actually executed R3 two-line pair scans x176,174,...2**. Each half-screen decodes PF0 D4..D7, PF1 D7..D0, PF2 D0..D7 to 20 × four-color-clock cells. Source R3 `halo` vs `scenery` are **TWO SEPARATE, FRAME-ALTERNATING DIAGNOSTIC MODES**: any simultaneous mask compositing is HYPOTHETICAL, not actual original R3 operation or final eight world maps.

### Test A — one Missile with no within-line reposition cannot stand in for 3 synthetic obstacle columns
At original R3 source row-index 98, visible scenery has **three separated four-clock blocks [56,60), [88,92), [108,112)**, with asymmetric start distances **32 and 20** clocks; all 13 X modes share this same diagnostic scenery. Each of 16 mixed two-line groups per X has 3 separate scenery runs. A single unrepositioned M0 or M1 has one contiguous single-bit strip width 1/2/4/8 clocks and FAILS in **13/13** cases. Automatic equal-spaced NUSIZ triple copies cannot match unequal 32/20 spacings, and NUSIZ0 is already selected for a **quadruple-width P0 at Level3**, not three missile copies. This does NOT prove no specialized mid-scanline reset scheme can draw the bars, nor that users' unfinished themed obstacle maps have these coordinates.

### Test B — Venetian alternating raster row assignment has exact source pixel loss
Hypothetical one-foreground-PF-colour/physical-scanline policy: on rows where both source masks are present, choose ONLY HALO or ONLY SCENERY in alternating physical lines (or two-line pairs), otherwise show the sole present mask. Exact per-X two-line repeated source counts:

| Original synthetic mask cell-lines / 176-line arena | Count | Remaining after Venetian in all 13 X |
|---|---:|---:|
| Halo four-clock PF-cell-lines | 184 | **150/184 = 81.522%** |
| Scenery four-clock PF-cell-lines | 96 | **48/96 = 50.000%** |

In the 16 two-line groups with both sources active, **half of each shape's originally lit cells are omitted**. This is NOT a percentage of luminance or TV flicker perception, and the alternative odd/even pair phase gives the same source-loss result. It is a rigorous **SOURCE PIXEL-EXACTNESS FAIL** for this defined Venetian allocation, not a 6507/VENETIAN runtime feasibility test. If time-sharing whole frames, it reverts to the original gold-versus-blue 30/30Hz R3 alternation; still not simultaneous independent colours.

### Test C — restricted fixed-resource two-colour mask allocation
1979 hardware grouping is **P0+M0 via COLUP0**, **P1+M1 via COLUP1**, **PF+BL via COLUPF**, and **global background via COLUBK**. With P0 reserved for user's gray Skraun and P1 for differently shaped/coloured knight/archer, only PF is an arbitrary multi-segment width plane per line. M0/M1/BL are each narrow, contiguous ≤8-color-clock streams without extra midline resets; BK paints every uncovered background cell in its band. A very restricted enumeration of assigning TWO separately-coloured, independently multi-segment source shapes to **distinct fixed owners PF/M0/M1/BL/BK** gives **ZERO assignments**. This is a LOWER-BOUND RESULT for a NO-REPOSITION, NO-INTRALINE-COLOUR-CHANGE class, **NOT a universal hardware impossibility theorem**.

**Directly inadequate apparent shortcuts:**
- BL is not another gold overlay if PF is blue obstacles: **BL shares COLUPF**.
- M0/M1 do not supply a separately chosen gold ring colour while P0 gray and P1 the enemy colour: they share player colour.
- `CTRLPF.SCORE` uses P0 hue on left, P1 hue on right, not independently moving gold-ring versus static environment colours.
- `COLUBK` changes background everywhere uncovered by a mask; making a *moving circular outline* needs additional raster masking / colour transitions.
- Three pillar spots could be reassigned to M0/M1/BL only with the distinct P0/P1/PF colour couplings, arrow/orb allocation and arbitrary X/Y timing still solved; do not silently turn the environments multicoloured or delete an attack object.

**Candidate surviving as research only:** sophisticated **time-varying PF + raster COLUPF** geometry/colour schedule with explicit object overlap priority and exact WRITE DEADLINES, perhaps with separately proven P1 reuse. Previous PF-REP1B showed 5-cycle LDA/STA conditional scheduling FAIL at X80/84 on 56/60 of 416 hypothetical mixed lines, and sensitivity to 2-cycle shift. The simple one-register/2-line Hugg kernel remains direct source-mask FAIL. None of this is a full-game engine GO. Additional complex routes might emerge through specialized line kernels/colour preparation; they require real measured 6507 cycle and TIA timing proof.

## Regression method
The ZIP includes `PF_REP1C_RESOURCE_TEST.py` and `PF_REP1C_REGRESSION.py`. The independently written regression asserts 13 exact mask data sets; six X with same PF-cell ownership overlap; three synthetic scenery bands and their coordinates; positive and negative single-Missile controls; fixed-copy spacing negative; exactly 184/96 original / 150/48 Venetian cell-line counts; the constrained no-static-second-plane model; and original source blob SHA. No real 6507 CPU, frame, P1 multiplex or Stella was run; no project production code changed.

## MAIN II ruling and technical priority
**Receive PF-REP1C as completed REPRODUCIBLE SOURCE-ONLY research delivery.**
1. **REJECT** single-Missile/BL or naive NUSIZ-copy reassignment as exact unchanged R3 scene solution under the tested fixed-owner class. **REJECT** simple Venetian as pixel-exact reproduction.
2. **Keep PF-REP1 #25 OPEN**: the remaining hard proof is a design that gives independently readable gold halo + solid obstacles at *same physical Y*, without sacrificing P0 hero/three same-Y P1 enemies. Require cycle-accurate colour/PF physical deadlines, RAM+stack, actual input and enemy visibility across frames.
3. **Prioritize already AUTHORISED collision-only ROM diagnostic P01-COL1 #24 as a separate development track**. Do not duplicate it as a PF or full-renderer test. No additional ROM authorization generated by this research report.
4. Retain #15 visual, #19 ART1 L3, #23 L3 navigation, #1 P01 independent verification OPEN and R3 full-scene NO-GO. No new sprite/canon/map/gameplay compromise, main product merge, mapper switch, R4/B3c or independent VERIFICATION authorized.
