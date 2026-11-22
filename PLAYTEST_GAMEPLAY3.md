# THE SKRAUN / GAMEPLAY-3 – ROM DEVELOPMENT III playtest
**Status 2026-11-22:** DEVELOPER_OBSERVED / K1T_R1_PHYSICAL_ART_PASS / THREE_INDEPENDENT_ENEMIES_FAIL_FOR_TESTED_H1_H2. Production renderer and sprites NOT approved.

## Download and run
- Best preserved **real 8192B conventional F8 cartridge**: `experiments/gameplay3_f8_ntsc.bin`.
- Reproducible SHA256 in `experiments/gameplay3_SHA256SUMS.txt`. K1-T/R1 mask provenance: exact frozen `experiments/gameplay3/P1_K1T_R1_FROZEN_SOURCE.json` from graphics commit `4960d1661ad9764ce257a59053a981f46b09cff2`.
- Open ROM with Stella; joystick moves all 8 directions; FIRE casts halo during movement. Console RESET/FIRE after GAME OVER starts new game. Press no debug memory commands while playtesting.

## Genuine one-stage game loop
- Stage 1 starts at level1, three lives and score zero, with P0 exactly the original U1-LEG1 sprite A/B and one P1 training target.
- Right ~16 frames and down ~24 collects original BL orb, L1→L2.
- Hold FIRE and move around obstacles; the diagnostic sequential enemies are beaten by the original logical halo and 100, 100, 250 points; last slot is world-color Ranger proxy. After a short stage-transition delay, stage 2 starts at retained level/lives/score.
- On stage2, collect its new orb by right~8 and down~24; L2→L3 and continue diagonal movement with FIRE. Only one orb per actual stage visit.
- Knight neutral and 24-frame warning now use the **actual 8x16 K1-T T-visor masks** in the real playable ROM; P1 is light blue even during warning. Actual strike still uses the same K1-T neutral bitmask, not yet physically correct K1-T strike pose. Source-driven sword hit window and life loss remain from GAMEPLAY-2.
- Ranger final slot uses real R1 neutral source bitmap and color from the environment. The three color/pose tables used in the running ROM are P1 K1-neutral, K1-warning and R1-neutral; drawing/shooting an arrow is NOT implemented.

## Six physical 8x16 pose proofs, including real TIA mirror
- `scripts/gameplay3_generate_art_roms.py` creates **12 diagnostic F8 assembly variants**, one ROM per each of K1-T neutral/warning/strike and R1 neutral/draw/release × normal/mirrored.
- `scripts/gameplay3_stella_art.sh` opens **each genuine 8192B assembled cartridge** in Stella Debugger, uses no memory or PC injections and saves genuine full desktop, 320x228 TIA crop, actual completed-frame scanline measurement and reproducible input script.
- `tests/gameplay3_real_art_pixels.py` compares source **each bit of each 16-row pose** to actual TIA foreground pixels with x2 width (320-screen representation). It rejects wrong source orientation, TIA mirroring, pixel count and non-262 frame.
- Physical P1 pixel counts are **K1 neutral116, warning134, strike130; R1 neutral106, draw118, release110**, each matching actual source in both mirrored directions. No screenshots are manufactured by montage. The diagnostics prove native size only in the tested test-ROMs, **not that all six change during normal gameplay**.

## Exact two triple-renderer trial branches – DO NOT claim canonical success
- **H1 same Y:** `build/gameplay3/hypotheses/H1_sameY_three_NUSIZ_copies.bin`. Three hardware P1 close-spaced copies set by NUSIZ1 and an early GRP1. Physical Stella **322** blue pixels vs **348** expected for three clean copies, 262 completed scanlines, obstacle-green 2832. Same K1 mask/color per copy; not three independently controlled enemies. Positions approximate x67/x83/x99, **NOT** exact historical Ranger x101 and not a hard-case pass.
- **H2 separated Y:** `build/gameplay3/hypotheses/H2_separatedY_three_mask_stream.bin`. Precomputed three P1 image bands (K1/R1/K1) at y39–55,99–115,159–175; actual **338/338** blue pixels and 262 completed scanlines, but all three share **one** P1 X/color and do not interact as separate actors. Does not prove same-Y.
- Source, exact ROMs, Stella screenshots and literal `_scanEnd` logs in successful workflow artifact `GAMEPLAY3-REAL-DASM-STELLA-ENEMY-ART` from [Actions run 45028262936](https://github.com/Odourman/the-skraun/actions/runs/45028262936). Both are NEGATIVE for mandatory two active knights plus independently positioned Ranger.

## NTSC and budget
- Authentic measured completed NTSC frames: **262** for 12 art variants, H1/H2, and sampled primary gameplay scenes.
- TIA writes remain one visible PF2 write per row; H1 deliberately advances GRP1 ~7 cycles before left playfield writes and therefore requires exact beam audit (262 alone is not physical PF deadline proof).
- Main P1 indirect-ROM source load adds a physical cycle over the old absolute indexed K1 dummy. Exact worst-case 76-cycle/beam deadline, stack highwater and every hard L3/FIRE/sword encounter are separately labelled **NOT_VERIFIED** until actual instrumented evidence is available.
- Original RIOT RAM 128B incl. stack. `$80..$BE` normal game state, `$B6:B7` P1 pointer, `$BF` sound timer, `$C0..$EF` 48-byte collision rectangles, `$F0..$FF` 16B stack reservation. The original `BonusCount` register B6 was unused and reused without changing the fixed collision/stack bounds.

## Strict boundaries
No full three-enemy physical renderer, no all-six-runtime P1 animation, no Ranger arrow, no X/Y-following new halo, no new mapper, no eight final worlds, no HUD or production art approval. The best ROM is a bounded GAMEPLAY-2-derived playable diagnostic plus physically true new masks. No main merge or independent Verification. **STOP after MAIN IV handoff**.
