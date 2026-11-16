# THE SKRAUN — MAIN Research Audit: Applicability of 30 Atari 2600 Tricks to P02-R1
**Date:** 2026-11-16
**Type:** ADVISORY RESEARCH ONLY. This is NOT a new implementation authorization, a production renderer decision, an amendment to design decisions 01–60, or independent VERIFICATION.

## Material reviewed and source authority

- Original 30-trick appendix from another Atari project: `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(4).md`. It describes **Let Me Out!** test failures and F6/other cartridge assumptions; those are NOT The Skraun's project state or tests.
- The Skraun MAIN: `docs/DESIGN_DECISIONS_01-60_2026-11-16.md`, `docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md`.
- The Skraun experiment: `experiment/romdev-b3b-horizontal-follow`, `experiments/romdev_b3b_dynamic.asm`, `experiments/romdev_b3b_obstacles.asm`; [B3b report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-b3b-horizontal-follow/docs/ROMDEV_B3B_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md).
- Current authorized research: [MAIN P02-R1 scope](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R1_RENDERER_FEASIBILITY_AUTHORIZED_2026-11-16.md).
- R1 ongoing experiment branch observed while writing: `experiment/romdev-r1-renderer-feasibility`; *work in progress*, not final R1 outcome.
- Historical Atari TIA: [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html).
- Concrete modern kernel references (illustrative, not adopted code): [8bitworkshop versatile PF kernel (2025)](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html), [three-stream follow-on](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html).
- [8Blit multi-kernel explanation](https://8blit.com/s02e04/); [Stella Debugger manual](https://stella-emu.github.io/docs/debugger.html).

## The actual bottlenecks to solve

1. B3b: real SWCHA input, 13 positions at X56..104; but only one 4-TIA-clock step every **16 NTSC frames**; not gameplay responsive.
2. B3b: **63/76 cycles worst visible scanline** by static DASM-symbol accounting, **13 cycles** remaining. Direct Stella showed **262 scanlines** at four sampled joystick states, NOT full cycle headroom for game.
3. Four extra dynamic scenery-byte loads alone need at least **16 cycles**, before OR, making unchanged B3b runtime PF+scene composition **>=79/76 cycles**.
4. Precomposed scene OR is only **one PF color and one PF object**: ring/obstacle overlapping pixels become visually indistinguishable. SCORE changes color between left and right halves, not per ring/obstacle. PFP alters depth priority, not independent layers.
5. P1 is empty in baseline diagnostic but two knights+one archer+arrow+orb+HUD are NOT renderable/proven merely because P1 is unused. Same-Y graphics are the hard stress case.
6. Level 3 must retain greater halo reach; color/size, full X/Y follow and gameplay collisions are not proven and are outside current R1 scope.

## Audit of all original 30 tricks against The Skraun

Legend: **NOW = inside R1 exploratory scope**, **ALREADY = used/currently being tried**, **LATER = relevant after renderer feasibility**, **NO NOW = poor fit/no present mandate**.

| # | Trick | Skraun verdict and why |
|---:|---|---|
| 01 | Sprite Multiplexing | **NOW analysis / LATER implementation.** Useful for 2 knights+archer on different Y bands, not free 3 distinct opponents in one scanline. Test resource/time reservation only under R1. |
| 02 | Mid-scanline GRP rewriting | **NOW theoretical timing / LATER diagnostic.** Can exploit copies in restricted X arrangements; B3b PF writes eat up cycle slots, so a stand-alone Space Invaders demo does not solve same-Y enemies. |
| 03 | Venetian Blinds | **NO NOW.** Costs vertical detail / changes visible rows; original source's FAIL pertains Let Me Out! not The Skraun. Very small Skraun level-1 sprite raises quality risk. |
| 04 | Sprite Flickering | **NO NOW as architecture.** Might be fallback for constrained overlap after actual visibility tests, but conflicts with MAIN goal of readable, nonconstant flicker; do not assume a flicker scheme passes. |
| 05 | Dynamic Playfield Sprites | **ALREADY** B3b ring uses PF. Its PF layer conflicts with scenery, not new available sprite channel. |
| 06 | Mid-frame Sprite Resizing | **LATER** optional visual detail, not independent players or extra PF bandwidth; 3 size levels already use NUSIZ + line repetition. |
| 07 | Asymmetric Playfield | **ALREADY**, six PF writes/line with timed right-side updates. Cost is the current bottleneck, not a newly discovered option. |
| 08 | Two-Line Kernel | **NOW HIGH for micro-feasibility**, if ring/scenery shapes tolerate 2-line vertical updates. May trade vertical precision for time; precise PF left/right deadlines remain. Must test ring contour, upright player and all tested X. |
| 09 | VDEL / delayed graphics | **NOW analysis / LATER tested with alternate P1 kernel.** Supports alternating sprite row updates/two-line kernels; NOT a new sprite and does not solve PF color collision. |
| 10 | HMOVE fine positioning | **ALREADY** for P0; important for future actors, but no extra cycles/resources. Test edge/raster timing when any new renderer uses it. |
| 11 | Late HMOVE | **NO NOW.** Timing/real-TIA risks and no solution to PF/scene competition. |
| 12 | Raster color changes | **NOW restricted color test** on scanline bands; cannot separately color PF ring and PF obstacle at same PF pixel/row unless more resources/other mechanism. Note added STA cost. |
| 13 | 48-pixel score kernel | **LATER** HUD in a separate screen band. Not a solution to overlapping moving arena objects; reserve cost/lines now. |
| 14 | Multiple Display Kernels | **NOW HIGH** schedule separate HUD/unoccupied bands and resource-heavy player+ring bands; dynamic Y overlap and kernel transitions still need measurable proof. |
| 15 | NUSIZ sprite duplication | **NOW theoretical enemy resource matrix / LATER demonstration.** Copies have *fixed spacings*, not arbitrary knight/archer X; P0 already scaled for Skraun. |
| 16 | REFP0/REFP1 | **ALREADY** REFP0 candidate self-tested, saves **24 source ROM bytes**; does not solve cycles or ring. |
| 17 | Missile and Ball reuse | **NOW resource planning / LATER implementation.** May suit arrow, orb or sparse mark, but M0/M1 are coupled to player color and BL to PF color; cannot render whole 360° ring. |
| 18 | Playfield SCORE mode | **ALREADY R1 variant** `romdev_r1_score_contrast.asm` exists: half-screen colors via COLUP0/COLUP1. NOT independent halo/scenery colors within either half; could color left PF gray like P0, and right PF future P1 color. Don't equate with solved overlap. |
| 19 | Playfield priority switching | **NO NOW as solution**; can alter PF vs P0/P1 occlusion, but same-color merged PF pixels remain indistinguishable. Useful later for selected effects. |
| 20 | Hardware collision latches | **LATER** supplementary sprite overlap detection; halo passes obstacles, so separate independent software radial collision model needed. |
| 21 | RIOT Timer Scheduling | **NOW small improvement**, for VBLANK/overscan task scheduling and stable frame lengths, but adds NO cycles to any 76-cycle visible line. |
| 22 | Stack/RAM mirroring | **NO NOW.** 128 RAM unchanged; stack/TIA aliasing risk greater than benefit until real measured RAM pressure. |
| 23 | Undocumented 6502 opcodes | **NO NOW.** Portability/hardware-revision concerns; not a fix for structural register bandwidth. |
| 24 | Precomputed tables, cycle-exact kernel | **ALREADY and NOW HIGH**: B3b uses compact 33-row ROM masks; R1 `romdev_r1_optimized_pf.asm` currently deduplicates **16 of 52 mask blocks** for 528 bytes saved with unchanged pixel masks. Larger 8-level expansion is not automatically reasonable; investigate row reuse/preparation outside visible kernel. |
| 25 | Stack-based TIA writes | **NO NOW.** Fragile cycle/stack tricks do not create independently colored PF objects or new sprites. |
| 26 | Timing-based horizontal scrolling | **NO NOW.** Fixed 8-screen game does not need scroll renderer; cannot solve ring overlap. |
| 27 | SCABS automatic bankswitching | **NO NOW.** Special cartridge feature; normal F6/F8 ROM banking is different. More ROM does not create scanline cycles. |
| 28 | Extra cartridge RAM / Superchip | **NO NOW** without a measured >128-byte staging requirement and explicit cartridge-format decision. Does not fix raster deadlines. |
| 29 | DPC custom chip | **NO NOW** nonstandard cartridge architecture; data hardware not new TIA sprites. |
| 30 | DPC+/CDF/ARM coprocessor | **NO NOW** significant different cartridge requirement and authenticity/emulator distribution decisions; no extra TIA objects or write deadlines. |

**Cross-project warning:** The original 30-trick report attributes particular FAILs to *Let Me Out!* (e.g., Venetian/6-object flicker). Those results cannot be transplanted as Skraun test outcomes. The underlying hardware mechanisms can be considered; each Skraun claim needs its own DASM/Stella evidence.

## What is already happening in live R1

At the time of this research snapshot:
- `experiments/romdev_r1_fast_pf.asm`: actual 2-frame input gating candidate, replacing B3b's 16-frame gate.
- `experiments/romdev_r1_optimized_pf.asm`: deduplicated precomposed masks and same-color PF overlap persists.
- `experiments/romdev_r1_score_contrast.asm`: SCORE-mode feasibility; beware half-screen color limitation.
- `experiments/romdev_r1_p1_stress.asm`: one synthetic P1 sprite added; resource/time lower-bound only, not three enemy instances.
- `tests/romdev_r1_object_headroom.py`: models the difference between minimum extra writes and real full multi-actor slots.
- These are **work-in-progress** experiments and CI runs, NOT an accepted final R1 handoff.

## Focused tests that fit current R1 *without authorizing B3c*

1. **Most valuable untested architecture:** compact two-line / vertical-region PF kernel comparison. Show ring+2–3 obstacle columns with distinct readable representation where technically possible, plus one synthetic P1 load. Record 1-line vs 2-line ring-contour error, actual movement response, 262 scanlines, PF handoff deadlines and worst-path timing. Reject if level-2 ring becomes malformed or image readability regresses; do not alter user design silently. Research-only until separately authorized if such a test would exceed R1's bounded candidate scope.
2. **Multiple kernels:** separate HUD-only zone versus dynamic arena; stress ring & P1 on same Y. Quantify what CPU work is truly saved **on overlapping lines**, not only above/below them.
3. **Variable register update stream** inspired by Steven Hugg's 2025 [versatile PF kernel](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html): rather than six fixed PF writes every scanline, schedule only register changes where persistent TIA values allow it. BUT it may update only one PF register per two scanlines and restrict representable shape. [Three-stream variant](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html) handles players too but its display-list RAM and branch paths are nontrivial. Treat articles as ideas, not code to paste without source/license/compatibility review.
4. **Do not repeat already-running R1 SCORE and dedup tests** as if they were novel alternatives. SCORE-mode half colors do not distinguish halo from obstacles within the same PF half. Note that players can inherit their respective COLUP colors on-screen independently but PF SCORE reuses those colors for corresponding halves.
5. **No SCABS / DPC / ARM migration** and no full actor, AI, HUD or B3c implementation. If all ordinary TIA routes fail a credible multi-object same-Y case, deliver a hard evidence-based stop decision to MAIN rather than making the demo prettier.

## MAIN conclusion

**Partially suitable.** The 30 tricks are a useful *technique catalog*, not a shopping list. Highest new engineering value for P02-R1 is **08 (two-line), 14 (multiple kernels), and further disciplined use of 24 (precompute)**, supported by 09 (VDEL) and selective 01/02 (sprite reuse). **05/07/10/16/18/24 are already used or being tested** in Skraun; 27–30 are not justified today. 18 SCORE, 19 PFP, 12 raster colors, 21 timer **do not** manufacture spare sprites/scanline cycles.

Do not award any new PASS or modify P02-R1 authority based solely on this advisory. ROM DEVELOPMENT should complete its authorized R1 package. MAIN can optionally decide on a dedicated two-line/versatile-kernel proof **after** the R1 report if it cannot be fitted inside its existing scope.
