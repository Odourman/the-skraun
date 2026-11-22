# THE SKRAUN – MAIN IV -> ROM DEVELOPMENT III
## GAMEPLAY-5: ARCADE COMBAT PUSH – ONE BIG PLAYABLE SPRINT

**Date:** 2026-11-22
**Status:** NEW EXPLICITLY AUTHORIZED ROM IMPLEMENTATION by MAIN IV following the user's direct instruction.
**Issue:** https://github.com/Odourman/the-skraun/issues/48
**Executor:** ROM DEVELOPMENT III, after receiving this handoff in the separate ROM DEVELOPMENT III chat.
**Class:** Actual DASM/Stella ROM development, not source-only research or independent Verification.

## 0. User-approved development METHOD: no more tiny approval cycles

User: "Du skrev: 'Jag rekommenderar ett mycket litet uppdrag till ROM DEVELOPMENT III:'. Men vi ska inte hålla på med 'mycket små uppdrag'. Kör på, dundra på istället."

MAIN IV decision: **ONE integrated, ambitious, self-directed ROM sprint.** Do not keep asking MAIN for approval after each trace, optimization, assembler refactor or unsuccessful technique WITHIN this authorized scope. ROM DEVELOPMENT III may debug, implement, test, refine and pivot between the five named workstreams below. Preserve working executable checkpoints throughout and submit ONE final consolidated delivery.

Aim to make a genuinely more fun, fast, playable original Atari 2600 game. Test physical results rigorously, but avoid administration becoming the central activity. This is NOT unlimited permission for later GAMEPLAY-6/N8/N9, mapper change, main merge, gameplay downgrade, new graphics commissioning, or independent Verification.

## 1. Exact frozen inputs; verify LIVE before starting

1. Start the new experiment branch suggested as experiment/gameplay5-arcade-combat-push-20261122 from **exactly** GAMEPLAY-4A commit bc2ef9249b4e13701647850d89cb631c43190c65, not main. DRAFT [PR #46](https://github.com/Odourman/the-skraun/pull/46) is the frozen GAMEPLAY-4A checkpoint, not a file to overwrite.
2. Baseline F8 8192-byte ROM: experiments/gameplay4a_f8_ntsc.bin, SHA256 **8bb19a9d58b6a4f608f1ab10adbb622b9e70d0f44b39e247c68feb3a974427bd**. Source original bank0 experiments/gameplay4a_bank0.asm blob d6cc7f1bf759d5fa2f0a9698046d5fa581016e11; bank1 experiments/gameplay4a_bank1.asm blob 98d6c4d0eebcb315f7141272399a4d5af0b8213b. Reassemble, hash and run actual Stella before editing.
3. K1-T and R1 source masks frozen by GRAPHICS II commit 4960d1661ad9764ce257a59053a981f46b09cff2; file graphics/mainiv_tvisor_ranger_ref_20261122/P1_SOURCE_MASKS_TOP_BOTTOM_MIRRORED.json. Three exact 8x16 poses each, both facings; user liked appearance. Approved U1-LEG1 original 8x12 A/B never modified, same source at all player levels and user-approved reversed direction labels.
4. Read Project Sources 00–04 as dated navigation and the actual higher-authority [game decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), most recent implementation handoffs, [GAMEPLAY-4 report](https://github.com/Odourman/the-skraun/blob/bc2ef9249b4e13701647850d89cb631c43190c65/docs/gameplay4/ROMDEV_GAMEPLAY4_MAIN_IV_DELIVERY_2026-11-22.md), and [Research II #47](https://github.com/Odourman/the-skraun/issues/47#issuecomment-7081118726) with [MAIN review](https://github.com/Odourman/the-skraun/issues/47#issuecomment-7081247166). Research is SOURCE_ONLY, no new physical proof.
5. Physical baseline: K1-T neutral/warning/strike and R1 draw/release visibly render in one ROM; GAMEPLAY-2 stage loop, orb levels, lives/score survive bounded tests. R1 five focus phases 18/21/24/27/30 have actual scan counts **262/262/262/263/262**. Original M1 per-visible-line indirect fetch/write generated 360 and incomplete frames, no arrow exists in the safe ROM. Y-following halo but not X-following. Currently sequential visible enemy waves, not three independent actors. Older H1/H2, N7/F2b and R3 20Hz failures are bounded negatives. Main HEAD at order publication was 46d31504cccc5d17b521f7b9f01b7aded003de1a and must stay unchanged.

## 2. ONE substantial playable GAMEPLAY-5 deliverable, FIVE preauthorized workstreams

These workstreams A–E are all **explicitly included in this single implementation authorization**, with internal checkpoints rather than a chain of approvals. They are not separate future phases to auto-start. Prioritize A/B/C for actual playable combat, D for a major genuine renderer attempt, E as a budget-dependent integrated enhancement. Continue working on other authorized workstreams if a specific technical submethod fails; keep the best real playable ROM.

### A. Fix real NTSC instability AND instrument critical TIA timings

- Reproduce the same GAMEPLAY-4A SHA and actual joystick/Stella R1 phases 18,21,24,27,30; examine K1 attack, BL reposition, stage/orb, L2/L3 and restart as well.
- Find first divergent **physical scanline/PC/cycle/colourclock**, including INTIM/TIM64T=34, variable overscan GameBankTick, optional PositionBall + WSYNC, extra final WSYNC, visible P0/PF/P1/BL loop page crossings/branch paths. Record PC, bank, SP, _scan, _scanEnd, _sCycles, _cClocks, _fWsyncCycles, _fTimReadCycles when Stella exposes them. Avoid asserting a root cause from a single 263 counter.
- **Make and physically test a causal timing correction in this same sprint**, not just a diagnostic report. A clean 262-line scene is necessary but does not alone prove all 76-6507-cycle or write-before-beam deadlines. Stress genuine worst-case screen positions while preserving exact masks and animation timing.
- The 128-byte RIOT RAM includes stack: build a compact live-range/high-water record, take measured runtime SP evidence including nested bankswitch/overscan interactions when feasible. An unmeasured path must be labelled NOT VERIFIED.

### B. Make R1 launch ONE ACTUALLY VISIBLE moving arrow with hit/collision

- Preserve real R1 neutral→draw→release poses in normal live play. At the ACTUAL release sample current Skraun X/Y and freeze direction, never home. At most one projectile in flight. Real forest launch interval ~180 NTSC frames from previous launch; provisional other-world intervals ~150/120/90f. Do not fire invisible damage when no visible projectile.
- **Try M0 first**: a small gray arrow shares P0 color but is not the P0 sprite. Do not steal P1 or BL orb. Precompute M0 X outside hot visible beam where possible, respect RESM0/HMM0/HMOVE, NUSIZ0 coupling to scaled Skraun, and generate a short vertically gated 1–2-scanline projectile through at most edge-enable events where feasible. All ENAM0 stores cost cycles and need real phase alignment. Do not blindly insert the rejected old 8/9-cycle M1 indirect LDA+STA into each of 192 hot scanlines.
- If M0 has a measured hard conflict, try a **distinct edge-cached M1** trial with full P1 color ownership/accounting as a fallback, not a repeat of the former failed M1 kernel. Rework raster schedule if needed but preserve playable code checkpoints.
- Arrow must visibly move across successive genuine Stella frames (including vertical component where aim requires), disappear on real solid obstacles, moving halo, hit or offscreen, reduce Skraun level/lives only when collision actually occurs, respect invulnerability, keep fixed velocity and world cooldown. Prove actual positional pixels AND logical state separately. Test L1/L3, blocked arrow, halo intercept, body-hit and max-one.
- If the physically safe missile architecture is impossible within the tested approach, preserve working K1/R1 gameplay and document exact cycle/beam/RAM conflict; never present arrow as PASS.

### C. Improve combat and actual gameplay AI in same cartridge

- Keep K1-T warning ~24 NTSC frames with locked direction, a short ~7-frame active sword pose, ~60-frame rest; only active strike can hurt, not body contact or warning/rest. Fix **source-detected sword-through-obstacle defect** in CloseForSword: presently proximity/facing only, no actual obstacle gate. Use the game's real solid rectangles; test unblocked and obstructed attacks in both facings.
- Give knight and ranger meaningful independent X/Y logical state and simple two-axis movement: knight chases/steers around obstacles, ranger retreats/searches useful shot lines and briefly stops to draw. Do this without disabling eight-direction player movement, diagonal slide or level-3 collision.
- Preserve orb pickup L1→L2→L3 on visits, level/life damage, score 100 per knight and 250 for Ranger, 2000 bonus, GAME OVER/FIRE, 1→2 stage progress, wave quota and 8-stage pendulum source loop. Where cheap, bring nominal ~45f invulnerability nearer ~60f and ~24f stage-transition pause nearer ~120f, avoiding a fresh CPU regression. Sound/feedback secondary to stable visuals and actual arrow.
- Existing sequential visible P1 target is TEMPORARY and must be marked as such if three independent actors are not yet physically rendered. Never silently pretend AI state is the same thing as concurrent visibility.

### D. Serious new physical three-actor renderer/AI attempt in this SAME sprint

- Source and logic must contain three distinct LIVE enemy identities: K1-T knight 1, K1-T knight 2, and world-green R1 Ranger, each with independent X/Y, state, timer and relevant actor death/score. Show two knights + Ranger physically simultaneously where possible.
- Physically test separated Y then **same-Y S2-close K1 x67, K2 x83, Ranger x101 around Y78**, plus scene with large P0 level3 physically occupying the overlap. Each correct source mask/facing, two identical blue knight colors plus distinct world-green ranger, readable 24f telegraph.
- Develop a **materially new timed P1-owner / GRP1/RESP1/COLUP1/HMOVE/NUSIZ/VDEL scheduling path**, not three fixed NUSIZ clones H1, three same-X Y strips H2, old 20Hz all-frame rotation, or old failed N7/F2b timing with a superficial NOP alteration. Precompute actor schedule offscreen when viable; account for P0, PF0/1/2, BL and potential M0 arrow on the same hard row. Genuine source rows, complete 76-cycle beam ledger, 128B RAM+stack, colour switches and screen X/Y identity are required for a PASS.
- Try substantive revisions within scope, but after a reproducible hard resource contradiction stop *this renderer subtrack*, write the first failing instruction/cycle/pixel evidence and continue delivering best other A–C work. Do NOT call tested failure general impossibility.
- Controlled local flicker, limited line-striping or visual Y offsets may be displayed ONLY as labelled alternatives; **not** adopted canon without separate user approval. Reducing enemy count, sword range, simultaneous AI, player L3 movement, halo reach or world-camouflage is prohibited without new user decision.

### E. If real A–D budget makes it plausible, attempt X/Y-following physical halo

- Current golden PF halo follows player **Y**, not X, whereas a 360° attack must surround moving Skraun and grow in radius/thickness at L2/L3, pass through obstacles and destroy arrow. Prefer offscreen computed X buckets/row masks with single early-PF-write arrangements and explicit beam deadlines. World PF when OFF, all arena PF gold when ON is a test colour-model, not automatically complete.
- Do NOT reintroduce PLAY1-X extra late PF2 write which gave >76 source cycles / real 273/285/297 scanlines, or CTRLPF mirror trick that moved static obstacles and stretched sprites.
- If time/cycles permit, show genuine Stella X56→80→104 with Y changes, U1 level3, BL orb, unchanged solid PF geometry, new enemy/arrow resource ownership, 262 rows and source-consistent damage. A 13-bucket exploratory halo is not automatically final full 0..159 following.
- If measured budget prevents an honest X/Y halo attempt, preserve latest stable Y-only partial checkpoint and report first credible beam/register conflict; do not hide the feature or silently shrink range.

## 3. Developer freedom, but strict hard requirements

**Developer AUTONOMY:** ROM DEVELOPMENT III may restructure F8 bank code, precompute tables, optimize/replace scanline loops, add compact actor state, and make as many directly motivated DASM/Stella revisions as needed within A–E. No separate approval required to do an additional internal test of the same authorized GAMEPLAY-5 feature. However *new mapper/extra cartridge RAM, new artwork, any new later scope, different gameplay canon, merger or independent verification* remain OUTSIDE authorization.

**Hard invariants:** original-compatible Atari 2600 NTSC 262 physical raster rows, 76 6507 CPU cycles per real row and actual PF/GRP/Missile register beam deadlines; RIOT 128B including hardware stack; conventional 8KiB F8; exact frozen upright light-gray U1-LEG1 8x12 A/B and display-direction flip (L2 16x24, L3 32x36 test form); real K1-T visor/sword and R1 bow masks; two active knights plus world-camouflaged Ranger as future full canon; 360° halo through obstacles and meaningful larger level3, open 8 directions with slide, BL orb, stage/lives/score. NO hidden degradation.

**Physical evidence:** Reproducible actual DASM build logs, listing/symbols, Stella debugger and genuine native 320-wide screenshots/sequence. Same playable ROM must be distinguished from separate diagnostics; source-only papers cannot prove hardware. Measure true CPU scanlines and colour-clock deadlines, plus RIOT live overlap and stack where feasible. Avoid needless repetitive independent audits after every checkpoint.

## 4. Suggested internal checkpoints (NOT extra user authorization gates)

0. Baseline reassembly 8KiB F8 exact SHA, frozen copy safe; new experiment branch & ONE DRAFT PR against previous experiment branch, no main merge.
1. TIMING checkpoint: corrected 262 in R1 all five phases and in meaningful active gameplay, masks unchanged; preserve ROM+SHA.
2. ARROW checkpoint: visible projectile in multiple continuous screenshots, x/y and wall/halo/player collisions, screen/cycle sanity; preserve ROM+SHA.
3. COMBAT checkpoint: obstacles block sword, actor AI and genuine stage loop/regressions; preserve ROM+SHA.
4. THREE ACTORS: real positive or measured negative on new scheduler and hard same-Y, without sacrificing earlier playable checkpoint.
5. HALO only if budget allows; integrate or record bounded physical reason to defer.

Do not stop after checkpoints 1,2 or 3: user has explicitly asked for a larger self-contained development run. When a subtrack fails, preserve the checkpoint and continue other authorized areas if possible.

## 5. Final delivery and STOP

Deliver ONE final consolidated bundle to MAIN IV via GitHub:
- BEST actually playable F8/NTSC 8192-byte ROM (if newer work fails, indicate which prior checkpoint is preferred); source ASM, build .lst/.sym/.log, repeatable real Stella scripts, exact branch and HEAD, SHA256 source+binary, screenshots and debugging traces, a new DRAFT PR against the game experiment branch.
- Native authentic sprite/arrow screenshots: K1 warning/strike, R1 draw/release, arrow flight and collision if PASS, level3 Skraun and BL orb; hardest realistic three-actor trial outcome; halo X/Y only if physically measured.
- Concise PASS/PARTIAL/FAIL table with actual runtime-only claims, 262-row counts, 76-cycle and register-write timing claims only where truly measured, stack high-water and worst memory overlap where tested.
- Regress real joystick/FIRE/orb growth, eight-way movement, solid obstacles and sliding, score/lives, stage transitions, GAME OVER/restart, long frame sequence. Label non-tested paths honestly.
- 3 biggest remaining blockers and ONE next recommended playable direction. Avoid fifty-page paperwork.

Final result label: **GAMEPLAY5_DELIVERED / ROMDEV_III_STOPPED / MAIN_IV_REVIEW_REQUIRED**. No main merge, new mapper, N8/GAMEPLAY-6, full 8-world content sprint or independent Verification is automatically initiated.

**This handoff is express authorization for ROM DEVELOPMENT III to implement the whole A–E scope, not just a one-trace microtest. It only starts when handed to the separate ROM DEVELOPMENT III chat.**