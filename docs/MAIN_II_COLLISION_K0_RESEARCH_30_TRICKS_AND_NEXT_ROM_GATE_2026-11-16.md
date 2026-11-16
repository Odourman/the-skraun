# THE SKRAUN — MAIN II K0 collision research, all 30 tricks re-review and next test gate
**Date:** 2026-11-16 · **Class:** SOURCE-ONLY independent model audit, not real 6502/Stella, not production implementation, not independent VERIFICATION

## User mandate and priorities
The user delegated continued development without routine prompts, explicitly instructed MAIN to re-read research and all 30 tricks **before** deciding what to implement, and to work independently while preserving what the user actually wants. MAIN's standing goal: a real Atari 2600 arcade game with approved upright gray U1-LEG1 two-pose troll / corrected mirrored visual facing, 8 visually distinct levels across forest/mountain/dream/night, 3 sizes of the same troll, two sword knights plus fleeing green archer, arrow, orb, gold halo that passes obstacles, lives/score, and **plenty of non-sticky open maneuvering room for Level 3**. No quiet gameplay or aesthetics compromises to make the hardware appear easier.

**Sources actually re-read before the decision:**
- [All 30 tricks vs Skraun renderer](R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md) and its synchronized [Google Doc](https://docs.google.com/document/d/1gvEw6Dq6DfNUymKSBcRDmriIinkJmGKbdszwm0cNMdM/edit).
- [All 30 tricks vs sprite identity](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md).
- [Decisions 01–60 including later L3 navigability instruction](DESIGN_DECISIONS_01-60_2026-11-16.md), [current visual authority](SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [status](PROJECT_STATUS_2026-11-16.md).
- [Actual original R3 source and result](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md), [current prototype src/main.asm](https://github.com/Odourman/the-skraun/blob/main/src/main.asm), [the eight unmerged draft map study](MAIN_II_EIGHT_ROOMY_LEVEL3_MAP_DRAFT_REVIEW_AND_STOP_2026-11-16.md).
- Atari [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) and [MOS 6502 CMP cycle table](https://csh.rit.edu/~moffitt/docs/6502.html) checked for timing terminology. The original 30-trick research's Let Me Out! hardware experiments are NOT Skraun PASS/FAIL data.

## 30-trick findings for this specific problem
- **#24 Precomputed tables** — actionable: 8 draft maps × 3 troll sizes × max 4 rectangle bounds. Compute actor-centre exclusion rectangles OFFLINE and store in ROM, not extra RIOT RAM.
- **#21 RIOT timer / VBLANK/overscan scheduling** — plausible: collision must be attempted outside visible beam if there is free frame budget; cannot steal 76-cycle scanline deadline time already reserved for P0/P1/PF.
- **#20 Hardware TIA collision latches** — inadequate as sole gameplay physics. TIA PF flicker and halo-PF overlap means the game must preserve independent logical SOLID geometry.
- **#08 two-line; #14 multiple kernels; #01 P1 multiplex; #02 mid-line writes; #09 VDEL; #17 missile/ball** remain possible future renderer alternatives, but no source-only geometry result resolves same-Y 20Hz flicker or PF halo/obstacle colour conflict.
- **#27–30 additional ROM/RAM/coprocessors** do not manufacture third player, extra PF colour layer or >76 CPU cycles per visible scanline. No special-cartridge cutover authorised.
- **#06/#12/#16** for sprite art are advisory; user's approved U1-LEG1 art and facing mapping are now frozen, not to be revisited without a new user request.

## K0 actual executed evidence
**Source-only exact research package:** [Drive THE_SKRAUN_COLLISION_K0_SOURCE_AUDIT_2026-11-16.zip](https://drive.google.com/file/d/174OGOSl7eHkAqAtB53oFWTTrVlclTcre/view) **31,825 bytes**, SHA-256 **`7f69f2a2c699ccd417be78e94f2cc44680d5c581fa83ff619e228869e8f57537`**, **14 ZIP entries, 13/13 SHA256SUMS entries PASS, ZIP CRC PASS**. Real uploaded Drive ZIP downloaded back: **identical SHA256 and bytes**. Fresh unpack in a separate clean directory, reran the full source model and quick independent exact validator, rebuilt all files + deterministic ZIP; **all files and archive byte-identical, including ZIP SHA256**.

**Scope:** read-only snapshots of the previously unmerged, NON-CANONICAL eight draft layouts. No game repository ROM changes, no new graphic pixels, no authored canonical map changes.

**Precisely observed:**
- Generated **24 sets of forbidden player-centre rectangles** (8 maps × L1/L2/L3), padded to 4 rect records × 4 bytes each = **384 source-data ROM candidate bytes**, plus hypothetical 48-byte pointer + 12-byte border tables (~444 bytes data before code). NOT a DASM assembled memory ledger.
- Per-level table vs prior continuous half-open AABB collision: **675,840/675,840 integer player centre positions matched exactly**.
- An earlier endpoint-only source model allowed **66** unsafe 1-clock corner diagonals and **660** unsafe 4-clock shortcuts in eight draft maps. Those are negative-control reference counts, NOT real 6502 runtime observations.
- New conservative full-swept-centre-area collision + x/y slide model: **768,864/768,864** Level-3 **ONE-UNIT** directional moves produced the SAME destination as the strict step-by-step reference, with no invalid body/obstacle overlap. Both 1- and 4-unit cases combined: **1,537,728** model moves stayed legal. The full swept *rectangle* inclusion test is stronger than testing only the diagonal endpoint.
- **Rejection of 4-unit single-sweep:** **39,348/768,864** Level-3 4-unit moves differed from strict 4-unit microstepping (14,055 complete stops + 25,293 different lateral slides). Safe against tunnelling, but liable to feel sticky; do not promote this workaround simply because it has fewer lookup loops.
- The accepted study's 160×176 arena, 32×36 Level3 full-body hitbox, 4-clocks/4-lines margin, central player anchor and 3–4 rectangular obstacles per map remain **test assumptions only**.
- The original R3: 23 bytes in $80..$96, 89-byte P1Buf $A0..$F8, only 9 bytes $97..$9F readily free before verified stack analysis. It has no solid collision. R3 same-Y/PF renderer remains NO-GO; worst visible rows have only 2–4 estimated spare cycles. Adding software collision directly to visible rows is NOT allowed.

## MAIN II decision
**ACCEPT K0 as a reproducible source-only data-and-geometry result**, NOT an Atari game implementation. Prefer **small strict input substeps** and off-kernel precomputed rectangular collision tables. Preserve the user's Level3 open-arena and safe-level-up requirements and the approved original U1-LEG1 pixel source.

**NO actual DASM/Stella timing PASS was achieved in this run.** The local attempt to obtain a real DASM/Stella executable did not complete successfully. More bytes/ROM savings do not prove that collision + AI + P1 schedules can fit all frame and visible-line budgets. The strict source model is not final physics; it has no enemy occupancy, arrow/sword trajectories or human feel-test.

## Next separately bounded ROM diagnostic requirement
A single **P0-only NTSC 4K collision feasibility proof** with one expressly NON-CANONICAL arena, a 3-obstacle sparse layout, the actual approved U1-LEG1 A/B mirrored art across three scale settings, 8 joystick directions, true centre-to-body collision and 1-clock conservative steps/sliding, safe level-change/growth tests, exact register ownership, measured 262 line frames and genuine DASM/Stella screenshots/logs. Compare actual ALU branches/cycles and VBLANK/overscan budget to expected bound. **No R4/B3c, new full P1 enemy/halo/HUD renderer, integration into R3 main, extra 8 maps or independent VERIFICATION in this small diagnostic.** If CPU/time/stack fails, report the defect and stop, no cherry-picked images.

**Gate status unchanged:** [L3 navigation #23](https://github.com/Odourman/the-skraun/issues/23) OPEN, [visual #15](https://github.com/Odourman/the-skraun/issues/15) OPEN, [ART1 L3 first scanline #19](https://github.com/Odourman/the-skraun/issues/19) OPEN, [independent P01 #1](https://github.com/Odourman/the-skraun/issues/1) OPEN. R3 full-scene NO-GO and no production merge.
