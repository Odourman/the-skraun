# THE SKRAUN — MAIN AUTHORIZATION P02-R2: SCENE-PRESERVING RENDERER & SPRITE SCHEDULING FEASIBILITY
**Date:** 2026-11-16  
**Role:** MAIN authorizes a NEW, separate bounded ROM DEVELOPMENT technical architecture experiment.  
**Scope:** **P02-R2 only.** No automatic R3 or P02-B3c. No independent VERIFICATION now.  
**Source of authority:** Decisions 01–60 and later MAIN-approved light-gray overhead Skraun direction. This scope is NOT a gameplay redesign or a production renderer selection.

## 1. R1 gate: accepted, with exact qualifications

MAIN reviewed ROM DEVELOPMENT R1 against real GitHub source, [draft PR #12](https://github.com/Odourman/the-skraun/pull/12), [consolidated report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r1-renderer-feasibility/docs/ROMDEV_P02_R1_RENDERER_FEASIBILITY_MAIN_HANDOFF_2026-11-16.md), and [green Stella/CI run #43906912249](https://github.com/Odourman/the-skraun/actions/runs/43906912249). Accepted **as completed engineering developer self-tests**, NOT as independent verification or product integration.

- Frozen tested assembler commit: `6ef51beff59b50ccf4c1a541dad22fc3254a3fdb`. PR #12 head at review: `fa12b49b4515f77bdcd111672e1355bccc84de33`, exactly **two report-only documentation commits later**; no assembler changes between these points.
- Four original-compatible 4,096-byte NTSC ROMs built and regression-tested with real Stella 6.7.1 screenshots and direct debugger sessions:
  - FAST PF SHA-256 `02aad43f1e7c10315ca54b50e1ee953e5e2e9ee2401a082754d325ff2ac67e90`;
  - OPT PF SHA-256 `a088b4fd434562edbdc102ba54242fe2477e0b973bfea274fec5856a9e486e57`;
  - SCORE SHA-256 `316067c9c275a93de11dff1d211c50742bd7eae05e7e86a3f600500fbff7632a`;
  - PF + P1 SHA-256 `6c0bf9dca066a0777d6e6ef2b63bfe7ae54fe7025749a5cd40693ad02d6c92e9`.
- R1-A: responsive 2-frame maximum diagnostic joystick gate (observed 1-frame first response for one sampled phase), 13 positions x=56..104, real 262 NTSC scanlines on sampled frames. **Not** a full eight-direction movement engine.
- R1-B: 16/52 identical 33-byte masks deduplicated: **528 bytes** of data saved in fixed obstacle candidate; no reduction of the same-color PF obstacle/halo ambiguity. SCORE only colors PF halves, not overlapping independent objects.
- R1-C: static cycle-path estimates from assembled symbols and page crossings: FAST **63/76**, OPT **64/76**, SCORE **63/76**, P1-stress **71/76** cycles. Values are **static calculations**, NOT direct full per-instruction timings for a finished game. Minimal naive all-object budget exceeds 76 (lower bound >=102/76), NOT an impossibility proof for all TIA techniques.
- P1 stress demonstrates ONE independent P1 bitmap at fixed X on rows overlapping PF+P0. Does not prove two knights+archer or arrow/orb/HUD.
- No permanent final code merge, final background, level-3 halo, B3c, enemies/AI, physics, attack logic or independent VERIFICATION.

**MAIN rejection:** R1's 63-cycle-per-line PF renderer is NOT approved as the base for P02-B3c or the full game. A new scheduling/rendering approach must demonstrate credible scene and actor headroom.

## 2. Input research and constraints

MAIN's advisory [audit of all 30 classic Atari 2600 tricks](https://github.com/Odourman/the-skraun/blob/main/docs/R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md) compares techniques originally researched for **another game** with *The Skraun*. The 30 are **candidate mechanisms**, not 30 mandatory implementations and not validated in Skraun.

Highest-value hypotheses to test in this R2:
- **#08 Two-Line Kernel**: spread PF work across two scanlines while retaining meaningful ring shape and P0/P1 bitmap detail;
- **#14 Multiple Display Kernels**: render HUD and non-overlap zones separately while budgeting worst ring+enemies rows correctly;
- **#24 Precomputed Data & Cycle-Exact Schedule**: reduce actual register writes via ROM precomputation, aliases, register persistence, or safe off-screen preparation rather than runtime PF OR;
- Supporting options: **#09 VDEL**, **#01 sprite multiplexing**, **#02 mid-scanline GRP rewriting**, and **#15 NUSIZ copies** (fixed spacings, not free arbitrary enemy X).

Possible reference patterns: Steven Hugg's 2025 'Versatile Playfield Kernel' and 'Three-Stream Versatile Kernel'. These are research ideas; **verify license, original assembly timing, actual representable shapes and RAM use** before reusing any code. Do not claim they solve arbitrary independent layers.

Historical SCORE mode, flicker, bankswitching, ARM/DPC and stack tricks may be discussed as measured fallback/resource comparisons; do not repeat R1's four existing variants as supposed new breakthroughs. **Do not select a new production cartridge format.**

## 3. Authorized R2 engineering tests

### R2-A: one-line vs two-line PF kernel, genuine original NTSC diagnostic ROM

In an isolated R2 branch, compare a **credible two-line raster kernel** (or similarly explicitly two-scanline scheduled graphics) against the R1 FAST/OPT PF baseline.

- Render a light-gray **upright P0 Skraun**, level-2 moving test halo, at least **two synthetic fixed obstacles whose pixel rows overlap the halo**, and **one active P1 bitmap on overlapping visible rows** where feasible.
- Preserve the visual shape and outline, test horizontal positions **x56, x80, x104**, movement reversal and no clipped pixels; measure ring contour and vertical quantization against the R1 baseline. Test 13 positions where inexpensive; a subset must be explicitly labelled.
- **Do not assume** 2× raster CPU budget automatically. Register writes still have horizontal beam deadlines, and P0/P1 detail must remain visible. Account for line-to-line reprogramming, VDEL latches, and kernel transition timing.
- Show actual Stella frames + real debugger steps, 262-line NTSC on moving/reversal states, time-critical PF left/right write deadlines and worst-case **cycle count on each of the two lines**, with side-by-side cost versus baseline.
- Reject if level-2 ring deforms intolerably, Skraun loses identity/limbs, PF scenery becomes invisible, or same-Y P1 ceases to render. Do NOT change any approved design requirement just to pass.

### R2-B: variable-update or multi-region renderer feasibility

Test **one alternate** design selected based on R2-A (e.g. update only PF registers that change, a compact display-list/event stream, or different kernels for HUD band vs game arena). The point is to reduce real same-row work rather than only ROM size.

- Explain exact PF register persistence across scanlines, how many writes can be omitted **without corrupting the moving ring at any tested center**, the memory footprint of a display list and costly runtime setup, and whether an event-stream format could realistically coexist with eight distinct obstacle layouts.
- If a separate HUD region is tried, demonstrate **a placeholder readable score/lives stripe** only, not finished scoring logic. Compare available arena scanlines/cycles; don't claim the HUD region frees cycles on overlapping ring/enemy rows.
- Test color/visual separation of ring versus scene. A shared PF pixel with one color is NOT two layers. A visual differentiation workaround is admissible as an experiment only if actual Stella images show BOTH ring course and obstacle boundaries remain distinguishable through overlap; note any flicker, flickering duty cycle, color bleed or lost features.
- If all feasible alternatives are still one-color PF, report this as the architectural blocker, not as PASS for independent layers.

### R2-C: representative same-Y actor/halo/scene scheduling stress

Develop a **bounded synthetic timing/slot test**, not game AI, using a *real compiled/observed diagnostic* where practical and a conservative static cost lower bound for anything omitted.

- Reserve screen slots for **P0 Skraun, two distinct knights, one distinct archer, one arrow, one orb and a separate HUD zone**, with the moving halo and obstacles. Their visual and logical identity should be trackable. Probe **same-Y worst overlap** and **staggered-Y best case**, with non-locked representative X positions.
- In the running ROM, attempt at minimum **P0 + moving halo + obstacles + TWO distinguishable enemy bitmaps on a common overlapping vertical band**, subject to honest hardware limits. If it cannot be built without changing confirmed requirements, show the precise timing/slot failure rather than drawing fake extra enemies.
- Compare P1 reuse across Y bands, NUSIZ copies + mid-scanline GRP writes, VDEL, narrow missile/ball role allocation, and a separate HUD raster kernel. Quantify fixed X spacings and sprite color constraints. If flicker is considered, clearly state duty cycle and visible-appearance tradeoff; never treat constant disruptive flicker as default acceptable.
- A lightweight level-3 ring **reach/edge-budget stress** is required: show/bound its intended larger outer radius and thicker ring against player size and PF edge/future-object budget **without implementing full three-level B3c**.
- Do not implement knight/archer AI, real arrow physics, orb pickup, 30-frame halo attack, collision/damage, 8 worlds, sound or full score engine.

### R2-D: evidence, limits, decision

For each candidate make a comparable resource table:
- ROM bytes used/free and optional precomputed mask growth per obstacle layout and 13 X positions;
- RIOT 128-byte RAM allocation and true remaining bytes;
- TIA objects/bitmaps, duplicate-slot/X-spacing constraints, color availability, PF shape/visibility and ring effect;
- worst **per-scanline cycles** (all relevant branch, page-cross and WSYNC cases), right-half PF register deadlines, and cycles genuinely available on worst *same-Y* lines;
- independently observed Stella Debugger frame length (typically 262) vs **static cycle calculations**, correctly labelled;
- approximate 8-layout and level-3 scaling risks;
- quality: readability at level 1/3, flicker, fixed/independent enemy X, ring passes obstacles per design, HUD separated only where genuine.

Final R2 decision must rank:
1. **Potential architecture** worth MAIN's next authorization (with explicit remaining proof obligations);
2. **Fallback** if only a constrained subset works;
3. **Rejected architectures** with reproducible reasons.

It is entirely acceptable to return **BLOCKED** or **FAIL** for impossible same-Y tests. Do not massage the score by dropping necessary future enemies or shrinking the level-3 halo.

## 4. Workflow and strict boundaries

- ROM DEVELOPMENT may code, debug, optimize and retest autonomously **only within R2-A/B/C/D**, and deliver a single coherent handoff at completion. Use DASM, Stella 6.7.1, Stella Debugger, GitHub Actions; record actual screenshot provenance and tests.
- Create a **new isolated experiment branch**, draft PR to its immediate experimental baseline, compiled NTSC test ROM(s), SHA-256 manifest, source and list/sym, deterministic input/log evidence, and one consolidated report in GitHub and Google Drive.
- Use hard-fail tests for missing artifacts and frame captures; no fake images or invented cycle data.
- **Do not start P02-B3c** (free 8-way movement/3 live ring sizes/FIRE), any B3d/B3e gameplay, all actors' AI, final 8-layout backgrounds, final mapper, production integration or `main` merge. **No automatic R3 after R2.**
- No unilateral changes to the user's game design decisions (notably fixed P0 overhead/gray shape, level-3 larger halo, two knights + one archer simultaneous, visible obstacles, pass-through magic, responsive movement, readable HUD).
- **VERIFICATION remains dormant**. Mandatory ordinary ROM DEVELOPMENT self-checks are NOT independent verification.
- Report a material MAIN decision point if evidence shows unavoidable conflict with already fixed mechanics or original-compatible hardware; offer quantified alternatives rather than silently changing the game.

## 5. Finish line

Deliver one R2 handoff with exact branch/commits, reproducible ROMs/hashes, actual Stella evidence, tested timings/scanline cases, credible per-object slots, and explicit PASS/FAIL/BLOCKED/NOT TESTED for R2-A/B/C. MAIN decides the next scope only AFTER reviewing this handoff.

**No promise of a feasible full-game kernel is implied. R2's purpose is to find out, not to assert it.**
