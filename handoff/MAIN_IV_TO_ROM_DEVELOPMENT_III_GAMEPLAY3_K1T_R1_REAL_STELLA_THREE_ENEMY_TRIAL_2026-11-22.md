# MAIN IV → ROM DEVELOPMENT III | GAMEPLAY-3: REAL K1-T / R1 PHYSICAL STELLA + THREE ENEMY TRIAL
**Date:** 2026-11-22  
**Authority:** User explicitly approved the visual direction and asked to try realizing the sprites in ROM: "Nu ser de bra ut. Jag gillar det. Låt oss försöka göra dem till verklighet." This is a NEW separate **bounded implementation order**, not automatic continuation of GAMEPLAY-2.  
**Tracking:** [Issue #undefined](https://github.com/Odourman/the-skraun/issues/undefined)  
**Status:** AUTHORIZED_TO_ROM_DEVELOPMENT_III / NOT_STARTED_BY_MAIN / MAIN_UNCHANGED

## 1. Goal
Turn two user-favoured graphics candidates into **actual Atari 2600 DASM-built, Stella-rendered, physically pixel-verifiable enemies** within a playable scene. Knight = **K1-T**, light blue 8x16, helmet with transparent T visor and one neutral/chase stance, ~24 NTSC-frame raised-sword warning, short active horizontal sword-extension pose, ~1s recovery. Ranger = **R1**, slender hood/bow silhouette, one color at a time (forest green), neutral/draw/release poses, 8x16 **authorized for experimental physical trial only**. Two knights + one independently placed Ranger remains mandatory final gameplay; active Ranger is not a sequential placeholder.

## 2. Exact frozen inputs (recheck live before coding)
- [GAMEPLAY-2 PR #42](https://github.com/Odourman/the-skraun/pull/42), commit `18f385f2f7665d68e8542f2abb155105702dd267`, ordinary F8 **8192 B** ROM `experiments/gameplay2_f8_ntsc.bin`, SHA-256 `1ebfba72cea63a36b3a7434233758242112680b2ad6f2b282c9bbea5652fa2fd`. Known **DEVELOPER_OBSERVED**: actual stage1→2, two distinct orb visits to L3, L3 64x36 TV footprint and diagonal move, correct 100+100+250 sequential score, life loss, bonus, game over, 262 NTSC completed-frame raster count in 13 Stella scenarios. **Not yet worst-case 76-cycle/beam or complete RAM/stack proof**. Do not change this frozen commit.
- [Graphics II report](https://github.com/Odourman/the-skraun/blob/4960d1661ad9764ce257a59053a981f46b09cff2/graphics/mainiv_tvisor_ranger_ref_20261122/GRAPHICS_II_TO_MAIN_IV_HANDOFF_2026-11-22.md), source commit `4960d1661ad9764ce257a59053a981f46b09cff2`. Exact six K1-T/R1 top-first and mirrored/bottom-first tables [here](https://github.com/Odourman/the-skraun/blob/4960d1661ad9764ce257a59053a981f46b09cff2/graphics/mainiv_tvisor_ranger_ref_20261122/P1_SOURCE_MASKS_TOP_BOTTOM_MIRRORED.json), Git blob `9d55ff2435bff6e7cf820da21ea05d9bfd033702`. All graphics **SOURCE_ONLY**; no ROM integration proof.
- Forest `A_Glanta` from `f34d3a31b4581432b89e0b9ed1293116914a0d43` is an **earlier preferred source-only test candidate**, not a GAMEPLAY-3 dependency. Keep existing prototype layout if replacing PF would crowd the kernel.
- Unchanged original approved Skraun [U1-LEG1](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json), blob `48332690d58aecf70d986eeee075dd3156bbf102`.
- Binding game logic: [Design decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md) plus more recent Ranger world-camouflage decision. N6-C open; N7 S2-close F2b failed only in that tested implementation, not globally impossible; PLAY1-X double PF2 failed NTSC timing. Read material failed-scene evidence and avoid repeating same path.

## 3. Implementation phases inside ONE sprint, without micro-approval
### A. Prove exact real sprites first
Create `experiment/gameplay3-physical-enemies-20261122` based on exact GAMEPLAY-2 commit. Reproduce exact existing GAMEPLAY-2 DASM/Stella 8KiB checkpoint before modifying. Bring in six unmodified source masks, correctly reorder top-first rows for scanline kernel and bit-reverse horizontal facings, with SHA/provenance. Demonstrate genuine Stella pixel geometry of:
- K1-T neutral, raised warning (T visor readable), strike (sword extends **within** P1 eight columns; don't claim a blade beyond P1).
- R1 bow neutral, draw, release, forest green with physical contrast against PF.
- Show each separately at native 8-bit source resolution (16 TV pixels under Stella's horizontal 2x display) and enlarged *pixel-faithful* crops, not artificial composite PASSES.
- Preserve P0 original grey U1-LEG1, orb BL, input, collision and stage progress.

### B. Integrate with the real playable loop
Actual knights and Ranger need distinct actor identities, positions, states, and per-actor hit/score bookkeeping. Exercise actual 0.4s warning and active sword-damage window; body contact must not inflict damage. Existing source-only Ranger shoot/draw graphic is visual; **do not call an arrow implemented** if no physical projectile. Preserve actual orb L1→L2→L3 across stage visits, 8-way movement, level3 obstacle freedom, life loss, 450 stage score with knight+knight+Ranger and stage1→2 game loop. No HUD/art campaign mandatory now.

### C. Bold but bounded physical simultaneous-rendering trial
Attempt two independently rendered knights + one Ranger concurrently in one physical forest stage. Begin with separated-Y positions; then same/near-Y hard case, including previously failed diagnostic positions **K1 x67, K2 x83, R x101 at arena y78**. Distinct art and stable identities, not all three sharing a single bitmap, not 3 sequential target waves or fake mockups. Measure if reliable physical visibility can be achieved using P1 raster reuse, HMOVE/RESP scheduling, VDEL/row interleaving where valid, precomputed offscreen schedule and/or selective perceptually acceptable flicker. Maximum two **materially different** renderer hypotheses in this sprint; quickly abandon nonviable variants, never hide missed copies or permanently reduce concurrent enemy design. A successful easy-separated-Y test is PARTIAL until worst-case or specified scene is proven. Keep body/hit/AI semantics honest.

### D. Optional strictly isolated sword visibility probe
If P1-only strike is inadequate at native size, you **may** test P1+M1 as a separate diagnostic candidate, recording cycle/beam/resource conflict (not production canon). M1 belongs to P1's color and may be needed for other attacks; never silently take it away from Ranger arrow/three-enemy renderer. Do not expand this into new projectile-system implementation.

## 4. Hard invariants and measurement
- **Original Atari 2600** NTSC target: **262 actual physical scanlines per frame**; **76 6507 cycles per physical raster row**, real write-before-beam deadlines. A Stella `NTSC*` label or 262 by itself is NOT proof of beam safety. Avoid extra late PF2 writes and the previous FAIL technique.
- 128 B RIOT RAM **including stack**; measure runtime stack high-water, not only static addresses.
- Correct original U1-LEG1 A/B and horizontal facings, three player levels, player mobility.
- Knight warning 24 frames, locked direction, sword hits only while active, blocked by solids; ranger world-camouflage and bow readability; arrows (when actually implemented later) obey existing gameplay decisions.
- Same-frame same-Y P1 object pixel identity: actual frame/crop and register trace per candidate. Source-only tables are not a physical 3-enemy renderer.
- The visually chosen enemy 8x16 masks are user-favoured **for physical testing**, but not final art/hardware certification. Renderer failures do not supersede gamecanon.

## 5. Scope limits
No new X/Y halo algorithm, no mapper change from conventional F8 8KiB, no new 8-world maps, no new graphics authoring, no main merge, no N8/N9/full release, no automatic independent VERIFICATION II. Leave current Y-only visible halo as explicit PARTIAL. Do not change level3 movement, halo range, 2 knights + Ranger, or use permanent sequential proxy as gameplay workaround. If RAM/ROM/CPU budget runs out, report hard numbers and candidate options, rather than silently degrading features. Source-only checks, developer-observed Stella and independent verification must be distinguished.

## 6. Deliver and stop
1. Reproducible **DASM-built executable 8192B ROM** (or explicit truthful FAIL), SHA256 + frozen source and commit/one DRAFT PR, no merge.
2. Native-resolution physical Stella K1-T and R1 pose/color/sprite evidence, with exact source-pixel oracle and screenshots.
3. Real Stella test of three independent enemies (separated and close/same Y), all 262 frames, 76-cycle/beam deadlines and actual register trace, plus RAM/stack high-water. If only partial or failed, deliver measured negative.
4. Regression of GAMEPLAY-2 real playable stage + L3, score, lives, orb; label every non-executed check.
5. Short PASS/PARTIAL/FAIL table, strongest 3 blockers, clear next user-facing choice. STOP after bounded scope. No downstream implementation triggered automatically.

**MAIN IV instructs ROM DEVELOPMENT III to implement this scope NOW after its separate chat receives this handoff.** This GitHub issue/handoff does **not** automatically start the separate ROM DEVELOPMENT III chat.
