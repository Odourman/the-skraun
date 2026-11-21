# The Skraun

> **AKTUELL INGÅNG FÖR CHATGPT-PROJEKTET (21 NOVEMBER 2026):** [Project Source 00 – Läs först](docs/PROJECT_SOURCE_00_START_HERE_2026-11-21.md), [Project Source 01 – spelcanon](docs/PROJECT_SOURCE_01_GAME_CANON_2026-11-21.md), [Project Source 02 – teknisk status/roller](docs/PROJECT_SOURCE_02_STATUS_GATES_AND_ROLES_2026-11-21.md), [förslag till Project Instructions](docs/CHATGPT_PROJECT_INSTRUCTIONS_SUGGESTED_2026-11-21.md). **N7/F2b är nu uttryckligen AUKTORISERAT som en minimal test-ROM för ROM DEVELOPMENT II**, [Issue #31](https://github.com/Odourman/the-skraun/issues/31), men är **inte byggt enligt senast kontrollerad status**. N6-C fullspelsrenderern är fortsatt obevisad [Issue #30](https://github.com/Odourman/the-skraun/issues/30). **Skraun är användargodkänd UPPRÄTT ljusgrå U1-LEG1 med getben** – de gamla README-avsnitten nedan om horisontellt troll och "LATEST" från 16–17 november är **HISTORIK, inte aktuell canon eller arbetsorder**. Kontrollera alltid live-branch, issue och handoff.


> **MAIN III migration / current snapshot, 2026-11-17:** [Read the live-updated entry state](docs/CURRENT_MAIN_STATE_2026-11-17.md), [full MAIN II → MAIN III handoff](handoff/MAIN_II_TO_MAIN_III_MIGRATION_2026-11-17.md), and [exact clean-chat start prompt](handoff/MAIN_III_STARTPROMPT_2026-11-17.md). [Google Drive migration document](https://docs.google.com/document/d/1QdaWnlqMevGmjX6gaYUttTCvJ7yn0XCPukBEpUzyEfA/edit) and [Google Drive startprompt](https://docs.google.com/document/d/1XLphoOEHNGxGH5mC4Yd6BJCDflOyx56xYuEBPIYyGwo/edit). All older "latest" statements below are dated history: current P01-COL1 [draft PR #27](https://github.com/Odourman/the-skraun/pull/27) has real DASM/CPU-model PASS, genuine Stella job still **FAIL** due workflow shell error; [PF-REP1 #25](https://github.com/Odourman/the-skraun/issues/25) research remains SOURCE-ONLY; R3 full-scene NO-GO. Verify live sources before acting.

**The Skraun** is an Atari 2600 top-down action game about a four-legged troll fighting knights and a green archer.

## Project status (2026-11-16)

**LATEST MAIN REVIEW OF GRAPHICS P1 (2026-11-16):** [Actual independent P1 ZIP archive verification and aesthetic decision](docs/MAIN_GRAPHICS_P1_HORIZONTAL_AXIS_REVIEW_AND_DECISION_2026-11-16.md): 376,608-byte [Drive ZIP](https://drive.google.com/file/d/1ouk4vL_gBVcb3Jc_-EP5UKSQLV1mEaSC/view), 15 entries, full SHA256 `d716e93cf6f15f5944fb9716efffd1217d2c716dbc3909906c2ba382aa728cd1`, 14/14 inner checks and local graphics validator PASS. Horizontal torso with head left/right and four upper/lower feet is a **better overhead perspective** than old front-facing Q1; **P1 A rounded-back is preferred as an experimental reference**, B remains only control. None is final Skraun art: original mouth/horns/identity remain weak and A may look turtle-like. GRAPHICS P1 frozen/complete. MAIN has **separately authorized ONE isolated [P01-ART1 P0-only actual NTSC Stella visual readout](handoff/MAIN_TO_ROM_DEV_P01_ART1_SKRAUN_STELLA_VISUAL_READOUT_AUTHORIZED_2026-11-16.md)**: A against B and Q1, 3 level sizes, 2 gait frames and both mirrored directions, actual pixel/orientation tests and 262-line frames. Not R4/B3c/full renderer; no graphics canon, production merge, next step or independent VERIFICATION authorized. R3 full-game NO-GO and issue #15 remain open.


**Latest MAIN scoped graphic study (2026-11-16):** [GRAPHICS P1 horizontal-axis perspective proof](handoff/MAIN_TO_GRAPHICS_P1_HORIZONTAL_AXIS_PERSPECTIVE_PROOF_2026-11-16.md) authorized as a **ONE-OFF post-v0.3 design study** based on a concrete visual insight: earlier Skraun 8×12 art made the head/face the top of the bitmap and rear feet the bottom, which reads frontal/humanoid although the user requires an overhead four-legged creature with only left/right facings. Test whether **head at right (mirrored to left), back along X, four paws projecting above/below** can produce a genuinely overhead 8×12 identity. Two A/B poses, actual-size silhouettes, exactly two design candidates, then stop for MAIN review. Existing R3-VFIX head-above-feet test remains valid for its *old bitmap*; a future sideways character needs a separate semantic head-at-right/left test. New pixel outlines and original reference identity are NOT approved final canon. **No automatic GRAPHICS v0.4, ROM work, R4, B3c, 8×14, main merge or VERIFICATION.**


**LATEST MAIN GRAPHICS DECISION (2026-11-16):** [GRAPHICS v0.3 final design gate](docs/MAIN_GRAPHICS_V03_FINAL_DELIVERY_DECISION_2026-11-16.md) accepted as a reproducible **graphic source package**, NOT approved final art or a Stella test. Verified Drive archive [THE_SKRAUN_GRAPHICS_V0_3_2026-11-16.zip](https://drive.google.com/file/d/1-nlqRBYSmFJG0xRm90DpDBFYud7tgCPh/view) 386,046 bytes, 27 entries, SHA256 `e74757e9877d7f7ea6837721a30633b0d224c13ac4ff189d1fb12aca6a797e26` and 26 matching manifest checks; developer art validator passes. **Q1 is the provisional 8×12 engineering candidate**, but a convincingly overhead **quadruped is NOT achieved** and **neither 8×12 nor 8×14 are final-approved**. v0.3 rounded three-level gold halo is accepted as an **aesthetic proportion reference**, forest/mountain/dream/night as themed design directions only. Graphic work is stopped pending a separate perspective/representation choice; no automatic v0.4, R4, B3c, ROM implementation, main merge or independent verification. [Open visual gate #15](https://github.com/Odourman/the-skraun/issues/15) remains open.


**Latest MAIN graphics checkpoint (2026-11-16):** GRAPHICS [v0.2 source branch](https://github.com/Odourman/the-skraun/tree/graphics/skraun-v0-2-refinement-20261116/graphics/skraun_v0_2) and [complete Drive ZIP](https://drive.google.com/file/d/13lmZX_SbFm27fceYJuE0DdYiZhO7U2q_/view) are accepted **as reproducible candidate art only**: exact downloaded ZIP 314,330 bytes, 20 entries, all 19 inner SHA256 manifest checks PASS, archive SHA256 `17227108204134d2fc3cb3dccad69f7633d8d092dd824aa6172bd88c09e9f9ff`. **C-overhead is a preferred baseline, NOT final approval.** Sword warning changes only 4 bits, bow draw only 2 bits; both enemy designs still read as frontal, not clearly overhead. 4-world PF boards are insufficiently distinct in silhouette. Both new halo families appear wide/elliptical under estimated 4:3 NTSC physical aspect (level3 A ~1.92, B ~1.83 visible width/height); historic ring is tall and gets clipped. MAIN authorized **[GRAPHICS v0.3 design-only readability gate](handoff/MAIN_TO_GRAPHICS_V0_3_OVERHEAD_READABILITY_FINAL_DESIGN_GATE_2026-11-16.md)** to resolve these issues, then stop for aesthetic choice. **No ROM, R4/B3c, merge, issue closure or independent VERIFICATION.**


**Latest MAIN graphics review (2026-11-16):** [GRAPHICS v0.1 on separate graphics branch](https://github.com/Odourman/the-skraun/tree/graphics/skraun-pixel-candidates-v0-1-20261116) is accepted as **exploratory 8×12 graphics source data only**, NOT final art or Stella-verified. Candidate C is a **provisional design baseline**; it still reads too front-facing versus the binding top-down direction. Current static 40×24 halo masks occupy 80/128/**176** visible scanlines at levels 1/2/3 (8 lines per band); gameplay reach not decided. [MAIN GRAPHICS v0.2 refinement handoff](handoff/MAIN_TO_GRAPHICS_V0_2_VISUAL_REFINEMENT_2026-11-16.md) asks for genuinely overhead silhouette comparisons, recognizable knight and green archer, real PF-world art, proportional halo study and an accessible versioned ZIP. **No R4, B3c, ROM implementation, merging, artistic acceptance or independent verification.**


**New MAIN visual DESIGN PROPOSAL (advisory only, 2026-11-16):** [Post-R3-VFIX visual identity/readability review](docs/SKRAUN_POST_R3_VISUAL_DESIGN_REVIEW_PROPOSAL_2026-11-16.md) compares the user's original gray overhead Skraun, real Stella A/B sprites, the R3 placeholder knights/archer and synthetic scenery; proposes visually recognizable enemies and forest/mountain/dream/night world silhouettes, with exact criteria for later original-TIA art testing. **No graphic asset, renderer, B3c/R4, or production merge is approved by this proposal.** R3-VFIX passed developer tests but final art and full-game feasibility remain open.


**LATEST MAIN REVIEW – R3-VFIX completed as developer self-test (2026-11-16):** [draft PR #16](https://github.com/Odourman/the-skraun/pull/16) fixes upside-down Skraun in all three frozen R3 diagnostic variants. [Authentic Stella regression #43925833442](https://github.com/Odourman/the-skraun/actions/runs/43925833442) shows 57/57 old captures FAIL the upright pixel contract and 57/57 corrected PASS; 57 sampled states are 262 NTSC scanlines. Exactly **36 active P0 sprite ROM bytes** change in each 4096-byte ROM; no kernel/PF/P1/input data changes. [Final reproducible package #43926438951](https://github.com/Odourman/the-skraun/actions/runs/43926438951). This is a **source/render orientation correction only**, not approved character art, recognizable knights/archer, world scenery, HUD or full-game renderer. [Visual gate #15](https://github.com/Odourman/the-skraun/issues/15) remains **OPEN for art/readability**, with orientation component resolved. R3's full-game architecture **NO-GO remains**. No R4, B3c, new art implementation, merge or independent VERIFICATION authorized.


**NEW MAIN VISUAL GATE after R3 (2026-11-16):** R3 technical developer self-tests support a **NO-GO** for full-game continuation in the tested renderers (same-Y enemy 20 Hz each, alternate halo/scenery 30 Hz, 2–4 static cycles spare), and **the R3 Stella screenshot shows a confirmed UPSIDE-DOWN player regression**: its descending `Troll3` reader draws feet before ears. Its tiny red/green enemies and three blue columns are **diagnostic placeholders, not final knights/archer or four-world scenery**. [Visual FAIL issue #15](https://github.com/Odourman/the-skraun/issues/15); [narrow MAIN-approved R3-VFIX source/real Stella regression task](handoff/MAIN_TO_ROM_DEV_R3_VFIX_ORIENTATION_REGRESSION_2026-11-16.md). No R4/B3c/art implementation authorized; no independent verification yet.


**Latest MAIN decision — P02-R2 accepted as bounded developer evidence (2026-11-16):** [R2 report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r2-two-line-scheduler/docs/ROMDEV_P02_R2_RENDERER_SCHEDULING_MAIN_HANDOFF_2026-11-16.md), [draft PR #13](https://github.com/Odourman/the-skraun/pull/13), [genuine Stella test](https://github.com/Odourman/the-skraun/actions/runs/43912037744), [16 debugger frame-state tests](https://github.com/Odourman/the-skraun/actions/runs/43911806707). Two-line/P1 diagnostic 68/76 static worst line, dual different P1 bitmaps 76/76 at fixed 64-clock spacing, HUD placeholder arena 64/76 without P1, alternating gold/blue raster 74/76 with 50% gold ring rows. **Not a feasible production proof for free-positioning three actors plus arrow/orb/level3 halo/scenery.** MAIN separately authorizes [P02-R3 decisive scene/sprite scheduler feasibility](handoff/MAIN_TO_ROM_DEV_P02_R3_DECISIVE_SCENE_SCHEDULER_AUTHORIZED_2026-11-16.md) as a bounded go/no-go architecture decision. **No B3c, no R4, no merge, VERIFICATION deferred.**


**Latest MAIN decision — R1 completed as developer self-test; R2 separately authorized (2026-11-16):** [R1 report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r1-renderer-feasibility/docs/ROMDEV_P02_R1_RENDERER_FEASIBILITY_MAIN_HANDOFF_2026-11-16.md), [draft PR #12](https://github.com/Odourman/the-skraun/pull/12), [green real-Stella self-test](https://github.com/Odourman/the-skraun/actions/runs/43906912249). Fast input 1–2-frame diagnostic, 528 ROM mask bytes saved, but same-PF-color obstacle/halo ambiguity and P1-only 71/76 cycle worst line mean R1 is NOT a validated full-game architecture. **[New MAIN authorization: P02-R2 renderer/sprite scheduling feasibility](handoff/MAIN_TO_ROM_DEV_P02_R2_RENDERER_SCHEDULING_AUTHORIZED_2026-11-16.md)** compares two-line raster scheduling, split/multi-region kernels, selective PF writes and conservative same-Y enemy slot tests. **No P02-B3c, no mainline merge, no independent VERIFICATION at this stage.**


**Research advisory for the currently authorized P02-R1 study:** [Critical audit of all 30 classic Atari 2600 tricks against The Skraun's measured PF/cycle/scenery constraints](docs/R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md). Focus on #08 two-line kernels, #14 multiple display kernels and #24 disciplined precomputed masks; #05/#07/#16/#18/#24 are already used or being evaluated. This advisory does **not** authorize any additional development stage.


**Most recent MAIN decision — P02-B3b completed (2026-11-16):** The [B3b experiment in draft PR #11](https://github.com/Odourman/the-skraun/pull/11) was accepted as a **bounded developer self-test**: 13 horizontal joystick-following ring positions and precomposed scene masks. The current driver moves only one 4-clock step per 16 NTSC frames (not playable-final). A static worst-case kernel estimate is **63/76 CPU cycles per scanline**; runtime general scenery composition exceeds this budget in the unchanged kernel, while ring and obstacles visually merge into one PF color. No enemy or HUD feasibility has been proven. [Full B3b report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-b3b-horizontal-follow/docs/ROMDEV_B3B_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md). **MAIN now authorizes only [P02-R1 renderer architecture feasibility](handoff/MAIN_TO_ROM_DEV_P02_R1_RENDERER_FEASIBILITY_AUTHORIZED_2026-11-16.md), not B3c or mainline integration.** Independent VERIFICATION remains deferred.


**Latest MAIN decision (2026-11-16):** ROM DEVELOPMENT's A/B/C developer self-tests are accepted as *bounded engineering evidence*, not independently verified or merged. A: gray walking Skraun. B: REFP0 horizontal hardware mirroring (24 source ROM bytes saved). C: three fixed asymmetric playfield ring centers with actual Stella screenshots and a sampled 262-line frame; **not** free joystick following. The C kernel's 64/76-cycle worst-case is currently a static calculation only. [Full A/B/C handoff](https://github.com/Odourman/the-skraun/blob/experiment/romdev-c-b3a/docs/ROMDEV_ABC_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md). [New MAIN-authorized P02-B3b task](handoff/MAIN_TO_ROM_DEV_B3B_AUTHORIZED_SCOPE_2026-11-16.md) tests horizontal joystick follow and bounded scenery competition. **No independent VERIFICATION now; no B3c authorization.**


**Current MAIN-authorized ROM DEVELOPMENT sprint (2026-11-16):** [Combined scope: gray Skraun animation self-tests, REFP0 hardware mirror experiment, and P02-B3a three-position asymmetric playfield feasibility](handoff/MAIN_TO_ROM_DEV_AUTHORIZED_SCOPE_2026-11-16.md). This is not implementation completion, a verified release, or permission for B3b/B3c. Independent VERIFICATION is deferred until MAIN requests a substantial milestone package.


**Upright sprite correction (2026-11-16):** The static gray troll+halo experiment was found to display its sprite vertically inverted because its bottom-to-top ROM row table contradicted a descending scanline index. Corrected in [draft PR #6](https://github.com/Odourman/the-skraun/pull/6), with a passing real-Stella per-pixel orientation regression across all 3 levels. See [the row-order audit](docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md). This remains developer self-test, not independent acceptance.

**Separate workstreams:** [ROM DEVELOPMENT handoff](handoff/ROM_DEVELOPMENT_START.md) | [Independent VERIFICATION handoff](handoff/VERIFICATION_START.md). These are prompts for separate conversations, not automatically created chats.

[Current verified project status and next gates](docs/PROJECT_STATUS_2026-11-16.md).

**Design established; P01 baseline runs in Stella but independent verification remains open.** A new light-gray overhead sprite is being tested separately in draft PR #4. B1/B2 static halo experiments passed bounded Stella visual tests; the moving B3 halo, complete enemies and world backgrounds are not implemented.

The project currently has 60 gameplay design decisions documented in the MAIN conversation and its exported design log. Those decisions govern implementation; this README is only an overview.

### Core design constraints

- Eight screens in four worlds: forest (1–2), mountains (3–4), dream (5–6), and dark night (7–8).
- One green archer per screen. Two knights can be active at once; additional knights arrive after earlier ones are defeated.
- A moving, 360-degree magic halo replaces a physical weapon. It destroys enemies and arrows, and passes through obstacles.
- The troll grows through levels 1–3 by collecting one orb per screen. A hit lowers its level; a hit at level 1 costs a life.
- **Level 3 must feel overpowered**; do not add difficulty scaling that nullifies player progression.
- When the eighth screen is cleared, the sequence reverses: 1→8, 8→1, 1→8, and so forth. Difficulty does not increase between loops.
- Simple, sparse solid obstacles stop arrows and sword attacks but not the troll's halo.
- Target authentic Atari 2600 hardware, with NTSC first and PAL examined separately.

## Development and verification

A working prototype must be reproducible from its 6502 source and a documented build procedure. Source changes, emulator screenshots, cycle/scanline measurements and a build log are not substitutes for independent verification.

Recommended gates:
1. **P01:** Display and move the troll; investigate three sizes and simple leg animation.
2. **P02:** Render a halo centered on the moving troll; separately establish collision logic.
3. **P03:** Stress-test sprite reuse for the troll, two knights and the archer, with projectile and orb.
4. **P04:** Implement a small combat arena and the agreed rules.
5. **P05:** Integrate progression, scoring, level transitions, and world order.

Each gate requires a testable artifact and explicit statement of what was actually verified. Do not treat design or feasibility research as successful implementation.

See [the first prototype gate](docs/PROTOTYPE_01_PLAN.md).

## License

No license has been selected yet. Do not assume permission to reuse this project's original assets or code.


## Design, research and CI

- [MAIN design decisions 01–60](docs/DESIGN_DECISIONS_01-60_2026-11-16.md) — the gameplay rules to preserve, including the level-3 overpowered design and reversed world order.
- [Atari 2600 comparison, decisions 01–60](docs/ATARI2600_COMPARISON_01-60_2026-11-16.md) — advisory research and engineering risks; not implementation proof.
- [P01 prototype plan](docs/PROTOTYPE_01_PLAN.md) — source implemented; independent runtime approval pending.
- [P01 source code](src/main.asm) — 6502 / DASM movement, three sizes and two leg poses.
- [P01 build report](docs/P01_BUILD_REPORT_2026-11-16.md) — CI evidence, SHA-256 and still-open tests.
- [P01 Stella screenshot evidence](docs/P01_STELLA_VISUAL_EVIDENCE_2026-11-16.md) — actual emulator PNGs, three sizes, rightward motion and test limitations.
- [P01 Stella scanline observation](docs/P01_STELLA_TIMING_EVIDENCE_2026-11-16.md) — direct 262-line debugger screenshot; not yet a full CPU timing audit.
- [P01 independent verification](https://github.com/Odourman/the-skraun/issues/1) — still open; no independent approval yet.
- [P02 halo feasibility plan](docs/P02_HALO_FEASIBILITY_PLAN.md) — original technical research scope.
- [P02-A P1 halo experiment (draft PR #2)](https://github.com/Odourman/the-skraun/pull/2) — separate executable ROM and Stella captures; rejected as a final rendering solution because of level-3 width and P1 occupation; not merged.
- [P02-B playfield halo plan](docs/P02_B_PLAYFIELD_FEASIBILITY_PLAN.md)
- [P02-B1 static playfield ring result](docs/P02_B1_PLAYFIELD_RESULT_2026-11-16.md) — real Stella PASS for static mirrored ring (96×84 screenshot pixels), not a moving halo.
- [P02-B2 ring with three troll sizes](docs/P02_B2_PLAYFIELD_RESULT_2026-11-16.md) — real Stella PASS for static P0+PF ring with three sizes; no FIRE or movement.
- [P02-B1/B2 experimental code (draft PR #3)](https://github.com/Odourman/the-skraun/pull/3) — evidence-only branch, not merged.
- [Confirmed Skraun visual direction](docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md) — user's sketch, neutral light-gray color, true overhead camera, two short walking poses and horizontal mirroring.
- [Gray overhead sprite experimental ROM report](docs/SKRAUN_GRAY_OVERHEAD_ROM_TEST_2026-11-16.md) — separate 4K NTSC Stella self-test, three sprite sizes, no independent approval.
- [Draft PR #4: gray overhead Skraun](https://github.com/Odourman/the-skraun/pull/4) — source and tests; do not merge before appearance and timing review.
- [Gray Skraun with a static gold PF ring](docs/GRAY_SKRAUN_STATIC_HALO_RESULT_2026-11-16.md) — Stella three-level combination PASS; **not** a moving ring.
- [Draft PR #5: static gray halo combination](https://github.com/Odourman/the-skraun/pull/5) — isolated source, not merged.
- [GitHub Actions CI](.github/workflows/ci.yml) — checks document completeness on pushes and pull requests. With `src/main.asm` present, also assembles a 4 KiB NTSC prototype with DASM and publishes its ROM, listing, symbols and SHA-256 as a workflow artifact.

Regular CI verifies assembly and model-based logic. Separate Stella visual CI verifies three sprite sizes and one movement direction. **Neither is independent verification or proof of original-hardware timing.**

Google Drive retains a separate project folder named **THE SKRAUN - Atari 2600**, including historic decisions 01–19 and exported decisions 01–60. GitHub provides the tracked code, CI and revisioned engineering documents.
