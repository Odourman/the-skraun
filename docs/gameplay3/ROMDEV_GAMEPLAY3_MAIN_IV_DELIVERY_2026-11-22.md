# THE SKRAUN — ROM DEVELOPMENT III → MAIN IV — GAMEPLAY-3 FROZEN PHYSICAL DELIVERY
**Datum:** 2026-11-22. **Order:** MAIN IV GAMEPLAY-3, Issue #43. **Resultat:** `GAMEPLAY3_K1T_R1_REAL_STELLA_PIXEL_PASS / H1_H2_THREE_INDEPENDENT_ENEMIES_FAIL_FOR_TESTED_APPROACHES / PARTIAL_GAMEPLAY_INTEGRATION / DEVELOPER_OBSERVED / STOP`.

## Authority, frozen provenance and deliverables
- Exactly authorized base: GAMEPLAY-2 commit `18f385f2f7665d68e8542f2abb155105702dd267`, actual 8192 B F8 ROM SHA-256 `1ebfba72cea63a36b3a7434233758242112680b2ad6f2b282c9bbea5652fa2fd`, reproduced byte-for-byte by genuine DASM before GAMEPLAY-3 changes.
- New branch `experiment/gameplay3-physical-enemies-20261122`. ONE DRAFT PR [#44](https://github.com/Odourman/the-skraun/pull/44), base GAMEPLAY-2 experiment, never `main`. The original frozen GAMEPLAY-2 branch/commit, immutable U1-LEG1 source, main and other tasks remain unchanged.
- Graphics II exact source-only K1-T and R1 masks from commit `4960d1661ad9764ce257a59053a981f46b09cff2`, original JSON git blob `9d55ff2435bff6e7cf820da21ea05d9bfd033702`, frozen in `experiments/gameplay3/P1_K1T_R1_FROZEN_SOURCE.json`. Experimental graphics trial, NOT final art approval.
- Best main playable F8 executable `experiments/gameplay3_f8_ntsc.bin`: **8192 bytes SHA-256 `0d636327a3b7024634c6f251ea327fcbaa0dc3c5e04d602fefe543a072abc02e`**.
- Genuine DASM bank0 ASM SHA `4260271466438b453ea1432bdf9a925c75236ca8a87425bdc23c7ba2d295d09c`; bank1 ASM SHA `05eca3f0cec600f2a7b00d3e375fd1264f06d9f27b06cf741158c6f7aa910817`. See committed `experiments/gameplay3_SHA256SUMS.txt`, `gameplay3_bank{0,1}.lst/.sym/.bin`, DASM output logs. Exact frozen ROM built by [real one-shot workflow run 45028598977](https://github.com/Odourman/the-skraun/actions/runs/45028598977).
- Gameplay instructions, real Stella test commands and RAM mapping: `PLAYTEST_GAMEPLAY3.md`.

## Actual source-faithful 8×16 TIA native art (DEVELOPER_OBSERVED)
**PASS:** 12 distinct 8 KiB F8 diagnostic ROMs were built by authentic DASM then each actually run in Stella 6.7.1. Genuine 320×228 TIA crops matched **every foreground pixel** of the six frozen 8×16 source masks, both native and REFP1-bit-reversed. Physical palette blue K1-T, forest-green R1, no synthetic mock-up or combined fake pass. Each tested frame reported `_scanEnd #262`.
| Pose | Physical foreground pixels on 320-wide TIA crop | Stage game pose status |
|---|---:|---|
| K1-T neutral | 116 | INTEGRATED in real playable GAMEPLAY-3 |
| K1-T raised 24f warning | 134 | INTEGRATED with gameplay warning state |
| K1-T active strike | 130 | DIAGNOSTIC REAL STELLA ONLY; dynamic runtime animation NOT PROVEN |
| R1 neutral | 106 | INTEGRATED as sequential world-camouflaged Ranger phase |
| R1 bow draw | 118 | DIAGNOSTIC REAL STELLA ONLY; no arrow |
| R1 bow release | 110 | DIAGNOSTIC REAL STELLA ONLY; no arrow |

Actual source/pixel/format evidence: `scripts/gameplay3_generate_art_roms.py`, `scripts/gameplay3_stella_art.sh`, `tests/gameplay3_real_art_pixels.py`, [successful developer physical run 45028071154](https://github.com/Odourman/the-skraun/actions/runs/45028071154), its downloadable action artifact with exact masks, 12 ROMs, 12 original Stella desktop PNGs, TIA crops, `_scanEnd` captures, and JSON pixel oracle.

## Exactly TWO physically executed triple-renderer hypotheses (DEVELOPER_OBSERVED bounded negative)
Real code, assembled 8192B binaries, full authentic Stella screenshots, physical 320×228 TIA crops, 262-scanline sessions and code are in [successful run 45028262936](https://github.com/Odourman/the-skraun/actions/runs/45028262936), test modules `scripts/gameplay3_build_three_hypotheses.py`, `scripts/gameplay3_stella_three_hypotheses.sh`, `tests/gameplay3_three_hypotheses_audit.py`.
1. **H1 same/near Y:** TIA NUSIZ1 triple same P1 hardware copies, early GRP1. Real **322 blue pixels vs expected 348** for even three clean identical K1T P1 copies, `_scanEnd=262`, baseline green PF pixel count 2832, gray P0 98. Same sprite bitmap and color for all copies, positions ~x67, x83, x99, NOT precisely independently addressable historical x67/83/101 and **no actual Ranger identity**. **FAIL_FOR_TESTED_APPROACH** for independent Knight 1/Knight 2/Ranger on same Y.
2. **H2 separated Y:** 193-row precomputed scan data with exact K1T/R1/K1T source rows. Actual **338/338** foreground blue pixels in three separate native 16-line bands y39–55,99–115,159–175 and `_scanEnd=262`, P0 98. Three actual distinct source forms in one frame, but they all share one P1 X and one COLUP1 color, so neither independent movement nor Ranger world camouflage. Not same-Y performance evidence. **PARTIAL FOR SEPARATED-Y ART / FAIL FOR THREE INDEPENDENT ACTORS**.
These bounded failures **DO NOT** prove three independent actors universally impossible on Atari 2600. Tested-scene N7 F2b, PLAY1-X or other previously negative shortcut does not justify a permanent gameplay compromise. H1/H2 exhausted this order's MAX TWO material renderer approaches; no third renderer experiment authorized.

## GAMEPLAY-2 regressions and timing
- Actual Stella developer test runs preserved core GAMEPLAY-2 joystick, orb 1→2 and 2→3 on later stage visit, real stage1→2, FIRE attack, player damage, gameover/restart, with frozen U1-LEG1 masks. Multiple sampled `_scanEnd=262` NTSC, not a blanket full-scene timing certification. Gameplay still sequential single-P1 target during *main playable* ROM, not fully three simultaneous enemies. Earlier GAMEPLAY-2 proof remains separately frozen.
- F8 bank0 gameplay code + bank1 graphics ROM; 4096+4096 byte exact executable. Reproduced frozen GAMEPLAY-2 SHA before changes, true 8KiB GAMEPLAY-3 SHA after changes. Real Stella bank switching and sustained frames observed; exhaustive bank-crossing register trace NOT independently certified.
- Critical TIA source-only: existing visible PF2-write arrangement retained. New `LDA (EnemyRowPtr),Y` to GRP1 may change critical cycle timing; H1 early GRP1 trades PF beam deadlines. Some source-static and sampled 262 results do NOT prove all `<=76` 6507 cycles, write-before-beam deadlines, all level3/sword/halo/hardcase paths. Label **NOT_VERIFIED** for complete worst-case beam trace.
- RIOT 128B inclusive stack: original game state `$80..$BE`, P1 ROM pointer `$B6:$B7`, sound `$BF`, 48B full-body collision rectangles `$C0..$EF`, reserved stack `$F0..$FF`. Actual *separately instrumented* startup stack canary F0..FF experiment run [45028527679](https://github.com/Odourman/the-skraun/actions/runs/45028527679) shows on one real debugger screenshot F0–F9 retained canary values, FA–FF altered (at least six stack bytes touched in that sampled execution). **Automated 16-byte text-address readback FAILED** (read_count=0 in all scenes). Therefore precise runtime worst-case stack high-water, SP under all interrupts/branches, and collision-array underflow remain **NOT_VERIFIED**, not PASS.

## PASS/PARTIAL/FAIL summary
| Contract | Classification |
|---|---|
| Frozen GAMEPLAY-2 genuine DASM SHA checkpoint | PASS (DEVELOPER_OBSERVED) |
| 6 exact poses × 2 facing physical Stella pixel mask identity | PASS (12 separate ROMs) |
| Native physical K1-T neutral, warning in playable ROM | PASS BOUNDED |
| R1 neutral image/forest-green color in playable sequential phase | PARTIAL / real diagnostic support |
| K1-T strike and R1 draw/release automatically timed in PLAYABLE loop | NOT_IMPLEMENTED |
| True 2 simultaneous knights + independent Ranger, same-Y x67/83/101 | FAIL FOR TESTED H1/H2, remains OPEN |
| 262 NTSC complete frames in measured art/H1/H2/regression scenes | PASS BOUNDED |
| Worst-case per-instruction 76c TIA beam deadlines | NOT_VERIFIED |
| Runtime full stack high-water and 128B collision integrity hard proof | NOT_VERIFIED |
| U1-LEG1, orb, L3, FIRE, stage1→2, score/lives regression | DEVELOPER_OBSERVED BOUNDED, full worstcase NOT VERIFIED |
| Visible moving X-follow halo, arrows, eight production forest/maps, HUD | OUT OF SCOPE; unchanged PARTIAL/OPEN |

## Three most important blockers and MAIN IV decision
1. **Real same-Y three independently positioned K1T/K1T/R1 masks/colors/movement** on original TIA: H1 duplicates a single image, H2 stacks images at one X. Requires separate next authorization to explore a qualitatively different physical schedule/resource tradeoff, without deleting any canonical actor.
2. **Real 76c/beamdeadline and RIOT stack highwater traces**, especially with new indirect ROM P1 read and high-stress same-Y scene; current bounded 262 does not certify the frame kernel.
3. **Actual per-actor timed combat animation and resource ownership** (K1-T true strike, Ranger draw/release/arrow) while preserving the already playable U1-L3, obstacles and halo. New native art is good in isolation but not complete enemy gameplay.

**STOP** after GAMEPLAY-3 delivery. Do NOT start further implementation, mapper changes, new X/Y halo, graphics creation, N8/N9, main merge or automatic independent Verification. MAIN IV must review this actual frozen delivery and separately authorize any next scope.
