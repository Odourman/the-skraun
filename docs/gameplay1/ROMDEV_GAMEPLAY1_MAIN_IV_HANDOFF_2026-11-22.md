# ROM DEVELOPMENT III -> MAIN IV | GAMEPLAY-1 bounded accelerated playable F8 prototype

**Date:** 2026-11-22. **Authority:** User-supplied MAIN IV GAMEPLAY-1 accelerated full-game prototype work order (2026-11-22). **Recipient:** MAIN IV. **Developer status:** GAMEPLAY1_PARTIAL / DEVELOPER_OBSERVED. **No independent Verification, no production main merge.**

## Lineage and reproducible build
- Exact frozen source parent: PLAY1-H `79b9739e77741c74ae5228f3c63d64449af7bc9f`; original 4096B ROM SHA256 `6e5e203ff2715fac650b76a620bc1e3e3b0084d67e82452842edd7b5e1903bca`.
- New branch `experiment/gameplay1-accelerated-full-prototype-20261122`; **only new GAMEPLAY-1 experiment**.
- Two DASM banks: `experiments/gameplay1_bank0.asm` gameplay, `experiments/gameplay1_bank1.asm` preserved PLAY1-H TIA. Assemble with `-f3`, concatenate 4096+4096 bytes into **8192B conventional F8**. See `PLAYTEST_GAMEPLAY1.md`.
- Reproducible CI uses real Ubuntu DASM/Stella 6.7.1 + Xvfb, joystick/FIRE input scripts and physical debugger desktop PNG, not synthetic mockups: `.github/workflows/gameplay1-real.yml`.
- A separate single-use `.github/workflows/gameplay1-freeze.yml` writes the **actual** DASM executable to `experiments/gameplay1_f8_ntsc.bin` with `experiments/gameplay1_SHA256SUMS.txt`, full listings and symbols. Confirm exact final commit and hash from live GitHub; do not infer them from this dated report.
- TEST STANDARD: NTSC 262 scanlines; `NTSC*` alone never proves correct scanline timings. Full beamdeadline and overscan worst-case still unqualified.

## What is implemented (source) versus physically observed
| Function | Status | Scope & evidence |
|---|---|---|
| PLAY1-H source U1-LEG1 A/B and horizontal facings | WORKING_BOUNDED | Identical source bytes compared; physical L1 P0 16x12, 98 gray pixels in Stella baseline |
| Joystick 8-way and selected collision | PARTIAL | Built from proven PLAY1-H; new alternate obstacle geometry not physically audited in stage 2 |
| Orb physical BL / L2 pickup | WORKING_BOUNDED | Real Stella scene P0 L2 32x24; dynamic orb X placement on stage changes source-only |
| Player level3 free walking | NOT_VERIFIED | SELECT script attempts did not raise P0 to level3 in current run; do NOT claim pass |
| FIRE halo gold/PF | PARTIAL | Physically gold / attack frames; Y follow inherited, X follow still FAIL |
| Knight physical P1 | WORKING_BOUNDED | Original blue 120 pixels in baseline and FIRE scenes; X chasing in developer screenshots |
| Warning/sword damage | PARTIAL | P1 warning changed 120 color pixels in actual Stella screenshot; damage/level loss implementation source reviewed, full multi-event integration not validated |
| Ranger | PARTIAL_DIAGNOSTIC_PROXY | Sequential single P1 world-camouflaged fleeing proxy in source with 250pt score. No separate sprite, no arrow, and NOT 2 knights plus Ranger simultaneously |
| Scoring and extra lives | SOURCE_ONLY | 100pt per knight-proxy, 250pt ranger-proxy, 2000pt bonus threshold; no HUD; full scoring simulation not captured |
| Stage loop / layouts | SOURCE_ONLY | 1..8..1 pendulum counters, eight temporary world colors/BL X's, two alternating PF layouts with matching RIOT collision rectangles; no eight final maps |
| Three independent simultaneous enemies | NOT_IMPLEMENTED | N6-C remains open; not a permanent one-enemy gameplay compromise |
| HUD, authentic sound/worlds, arrows, full GAME OVER UX | NOT_IMPLEMENTED/PARTIAL | One sound channel has short events and background-color GAME OVER only; no graphical HUD or arrow |
| Strict physical scanline/76-cycle/128B stack worst case | NOT_VERIFIED | ROM 8192 size builds; bank0 RIOT variables $AA..$BD, collision rectangles $C0..$EF, stack $F0..$FF nominal. Stack highwater and worst beam trace not measured |

**One screen P1 at a time is a diagnostic temporary proxy. The canonical game still requires two simultaneous knights plus Ranger, distinct sword poses, a mobile 360-degree halo, eight distinct navigable maps and full smooth L3 movement. Source-only is never renderer PASS.**

## Actual tested source/body identity
The strict `tests/gameplay1_pixels.py` runs on genuinely captured TIA crops, rejects wrong P0 bbox/pixel counts (8x12 => 16x12 TV; L2 32x24), wrong P1 source pixels (120 blue), missing gold PF and missing warning color. `L3_select` cannot silently pass by filename; actual bboxes are checked and print NOT_VERIFIED if physically still L1. The current CI run and artifacts must be consulted for exact PASS/FAIL and screenshots. Not independent VERIFICATION.

## Key unfinished technical problems (priority)
1. **Simultaneous three-enemy P1 rendering** with recognisable knight and world-camouflaged Ranger; 76c/beam constraints / no permanent combat downgrade.
2. **Correct X+Y following 360-degree halo** without the failed double-PF2 273/285/297-line renderer; preserve NTSC 262 and exact U1 artwork.
3. **Eight real separate maps and free level3 collision/navigation** with accessible orbs; current two provisional layouts are insufficient.
4. **Physical Ranger bow/arrow and knight sword poses** with correct per-hit windows and obstacles; current P1 is a proxy.
5. **HUD, balanced 2000pt/life progression, sounds and whole-frame pixel/register/stack verification**, including real level3 and 262-scanline worst cases.

## Minimum meaningful next playable step (not self-authorized)
MAIN IV to decide one bounded next direction: preserve the 8KiB F8 gameplay prototype and concentrate on **one genuine screen with visually correct simultaneous 2 knights + Ranger** and correct X/Y halo timing *only after* reviewing measured frame/beam traces and trade-offs. Avoid replay of PLAY1-X double PF2 failure. A simpler independent subgoal is to physically confirm one complete stage transition with joystick/FIRE/score before large renderer integration. Do not treat either recommendation as a new implementation order.

**BOUNDARY:** Stop after this GAMEPLAY-1 delivery. No N8/N9, no new hardware mapper, no changed canon, no main merge or independent Verification on our own authority.
