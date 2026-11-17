# THE SKRAUN — MAIN II: PF-REP1B conditional PF/COLUPF deadline feasibility

**Date 2026-11-17 · SOURCE-ONLY research (NOT ROM/NOT STELLA/NOT independent Verification).**

## Authority and original goals

The user asked MAIN II to continue self-directed while preserving the selected game: exact U1-LEG1 sprite source with approved reversed visual L/R mapping, same two A/B frames scaled across levels 1–3, Level3 easy movement through spacious eight maps, two sword knights + fleeing archer same-Y worst case, gold 360° halo passing through SOLID obstacles, sword/arrow blocking against solids, orb, score and lives. Do not covertly change game behaviour or visual canon to make a kernel demo pass.

Read actual [project decisions 01–60 + later L3 amendments](DESIGN_DECISIONS_01-60_2026-11-16.md), the existing [30 trick renderer audit](R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md) and [30 trick visual identity audit](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md), [Research v1 receipt](MAIN_II_RESEARCH_HANDOFF_V1_RECEIPT_AND_PF_SOURCE_TRIAGE_2026-11-17.md) and [PF-REP1 source mask result](MAIN_II_PF_REP1_SOURCE_SCREEN_AND_NEXT_DECISION_2026-11-17.md).

First-party hardware study cross-checked with primary source [Andrew Davie Sessions 17–18](https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-17.html), [8Blit S04E01 PF write timing](https://8blit.com/s04e01/), [Steven Hugg 2025 sparse PF kernel](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html) and [Hugg 2025 three-stream](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html).

## Actual source and code evidence — successfully executed

**Original exact frozen R3 input:** [R3 overlap ASM source](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), Git blob `3c9ed79078eee6a0c63100614a593f92e240b5e8`. Existing PF-REP1 exact 13×(halo+scenery) source-mask and 177-element rowmap snapshot was reused, as was the previous separately CI-verified results JSON.

**Complete fully reproducible nine-member ZIP in Google Drive:** [THE_SKRAUN_PF_REP1B_SOURCE_TIMING_MODEL_2026-11-17.zip](https://drive.google.com/file/d/1mEpLUB6jMd5UyUyav1gRlVK63fjQ4IVd/view); **17,537 bytes**, SHA-256 `af7b6e75ccef34392f10e92ba857b24532a2f8db4ec9b15fede15e65e0504b27`, **9 files including 8/8 SHA256SUMS entries; CRC PASS**. MAIN actually executed the Python 3 stdlib `PF_REP1B_SCHEDULE.py` and `PF_REP1B_REGRESSION.py` against ALL 13 X positions, reproduced the prior 13 PF pixel-overlap counts, and ran intentional impossible/easy writer schedule controls. In an entirely fresh directory, extracted ZIP, reran regression, rebuilt ZIP and compared **ALL 10 available files (9 extracted members and final ZIP) byte-for-byte identical**. Then uploaded ZIP to Google Drive, downloaded RAW file and byte-/SHA-256-compared to original — **PASS**.

All scripts, full per-X JSON results, counterexamples, timing model assumptions, bibliography, README and reproduction command are inside the unchanged Drive ZIP; no hand-waved undocumented local-only file.

## What was modeled, and what was NOT

Source-only hypothetical *simultaneous* `M_halo` and `M_scenery` source mask composition, originally two ALTERNATE diagnostic R3 picture modes. All 13 X positions 56..104 by 4, 88 real R3 raster pairs descending 176,174...2. The combined diagnostic masks contain 16 active two-line pairs per X where halo and scenery are lit in the same physical scanline and half. Six X values 64/68/76/80/84/88 contain **exact same four-colour-clock PF-cell ownership conflicts**, requiring an explicit future colour/occlusion strategy; **no priority has user approval**.

Each of those 16×13=208 source pairs has TWO physical raster lines, giving **416 hypothetical combined lines per priority**. The model uses 8Blit/Andrew Davie PF0,PF1,PF2 asymmetrical safe CPU-completion windows (left latest 18/24/34 cycles; right PF0 25–45, PF1 35–50, PF2 46–61), and approximate hypothetical colour change windows between active PF cells. It then uses a memoized exact job allocator for all required changes to PF0/PF1/PF2/COLUPF in one line and probes FOUR simplified fixed per-event execution costs. The colour switches are placed after prior lit cell and before next lit cell, generously rounded to integer cycles.

**CRUCIAL LIMITS:**
- THIS IS NOT an emulator: no TIA register latch latency, real beam colour sampling, or exact 6502 instruction schedule. PF writes between physical scanlines could outperform the in-line-only left writes. In particular, ±2 cycle artificial window extension is a sensitivity study, NOT a real hardware property.
- First colour loaded free; no actual data fetch/conditional branches or RAM, no P0, P1, HMOVE, M0/BL, collision, halo physics, moving enemies, HUD, AI, sprite masking or ROM storage cost.
- The two possible H/S pixel priorities at exact bit overlaps are HYPOTHETICAL UNSIGNED visual compromises.
- Model suitability does not imply any real multikernel is feasible; a simple 3-cycle `STA` cost assumes completely preloaded values without proving how such preloads happen.

## Precise verified conditional results

| Hypothetical sequential cost per required register event | H priority possible / 416 | H priority rejected | S priority possible / 416 | S priority rejected |
|---|---:|---:|---:|---:|
| 3 CPU cycles (STA only, values magically ready) | 416 | 0 | 416 | 0 |
| 5 CPU cycles (LDA immediate 2 + STA zero-page 3) | 360 | **56** | 356 | **60** |
| 5 cycles with artificial ±2-cycle window extension | 416 | 0 | 416 | 0 |
| 6 cycles generic illustrative cost | 240 | **176** | 264 | **152** |

**Every failed five-cycle mixed-colour line is associated with source R3 positions X80 or X84**. First reproducible counterexample: X80, R3 descending row index 98, four COLUPF colour transitions around PF cells 14→15, 15→22, 22→25 and 25→27, with left/right PF1/PF2 updates. Machine-readable jobs, cycle-completion deadlines and priority choices are in `PF_REP1B_RESULTS.json`. This case would be a mandatory negative control in any future narrow genuine DASM/Stella kernel diagnostic.

**Interpretation:** a naive constant five-cycle load+store implementation cannot meet this *particular simplified* schedule, while a highly idealized three-cycle-only stream can, with much of the actual game removed. The +2-cycle sensitivity case eliminates all toy failures. Thus it is **not scientifically justified** to call the whole physics impossible, nor to claim an actual 6507-compatible three-stream full renderer GO. The exact TIA deadline and colour resource owner problem remains the top priority.

## MAIN II decision / gate

**PF-REP1B source-only model package: COMPLETE, independently replayable and clean-rebuilt.**
**Simple Hugg one-register-per-2-line direct R3 drop-in: still SOURCE-LEVEL FAIL.**
**Naive 5-cycle continuous PF+COLUPF writer on unchanged hypothetical dual-colour R3 masks: CONDITIONAL FAIL on 56/60 of 416 mixed lines.**
**Full-game display engine feasibility: UNPROVEN, R3 full scene NO-GO stands.**

Keep existing [PF-REP1 tracking #25](https://github.com/Odourman/the-skraun/issues/25) **OPEN** for actual TIA physical per-register deadlines, full-frame colours, P0/P1 same-Y data, RAM+stack and separate drawing resource ownership. **Next source research task:** compare genuine alternative TIA colour ownership / object allocation rather than assuming three/four COLUPF writes with a one-layer PF at moving boundaries. Only after a full-scene-respecting candidate survives should MAIN explicitly authorize one small real 6507/DASM/Stella micro-ROM; NO R4/B3c integration now. Already authorized [P01-COL1 collision #24](https://github.com/Odourman/the-skraun/issues/24) remains distinct and unmodified.

Retain #15 full visual, #19 L3 top-raster, #23 L3 navigation, #1 independent P01 OPEN. Do not merge a source-study into production ROM, author new canonical maps, overwrite user-accepted U1-LEG1, change gameplay, cartridge or run unasked independent VERIFICATION.
