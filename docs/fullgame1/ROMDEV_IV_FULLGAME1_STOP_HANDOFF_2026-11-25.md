# THE SKRAUN - ROM DEVELOPMENT IV - FULLGAME-1 STOP / HANDOFF

**Recorded:** 2026-11-25 (Europe/Stockholm)  
**Owner / task:** ROM DEVELOPMENT IV, FULLGAME-1, Issue #50  
**State:** PAUSED_BY_USER / NOT_RELEASE_CANDIDATE / NO_NEW_IMPLEMENTATION  
**Basis:** User explicitly said "Avbryt" after the 2026-11-23 implementation activity, then explicitly requested this Google Drive/GitHub status update. This is an administrative handoff only; it does **not** restart implementation. MAIN IV's older instructions to complete the game are not an instruction to override the user's later stop.

## Exact live provenance at update

- Source repository: https://github.com/Odourman/the-skraun
- Development branch: `experiment/fullgame1-complete-skraun-20261123`
- Last IMPLEMENTATION HEAD before this status-only commit: `59a343afb2d7de15bb04b239dd4c02bd005667ef`
- Draft PR #51: https://github.com/Odourman/the-skraun/pull/51 — open, unmerged, **not release-ready**.
- FULLGAME-1 authority: https://github.com/Odourman/the-skraun/issues/50 ; 16 KiB maximum, standard F6 supported in the current implementation.
- Last successful four-bank DASM / physical Stella / audio Actions run: https://github.com/Odourman/the-skraun/actions/runs/45192954403 (commit `59a343afb2d7de15bb04b239dd4c02bd005667ef`).
- Fast real DASM: https://github.com/Odourman/the-skraun/actions/runs/45192954271 (success).
- Full development artifact containing ROM, generated assembler sources, logs, Stella captures and WAV: https://github.com/Odourman/the-skraun/actions/runs/45192954403/artifacts/14827545837
- Original frozen GAMEPLAY-5 F8 ROM: 8,192 bytes, SHA-256 `b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca` — **unchanged**.

## What passed (DEVELOPER_OBSERVED, bounded)

- Real DASM assembled four F6 banks and built a 16,384-byte NTSC test ROM. Current F6 artifact ROM SHA-256: `30982fe58368e4796a5acb8999a263a1bed35ef6251d8511dac26032e3877f9d`. This is an **experimental development ROM**, not a complete game.
- Stella 6.7.1 executed the selected game scenarios. **17/17 independently sampled final endpoints** reported `_scanEnd=262`, including `gameover_restart`. The archive also contains 120 successive Stella state captures, but their per-frame `_scanEnd` measurements were **0/120**, so continuous NTSC timing is **NOT VERIFIED**.
- Real SDL/Stella sound capture produced 7.012 seconds of interleaved stereo float32 audio at 44,100 Hz, converted to WAV. WAV SHA-256: `b909999e75b4a4574cd5da6c6a2c74aa3bc6d8f05416be24ca79c0616c45106c`. Audio generation is observed; **event-by-event audit and subjective listening NOT performed**. Do not call the complete sound design approved.
- Source has independent logical states for K1, K2 and Ranger, obstacle-avoidance attempts, reserve timing, two-channel priority/envelope SFX in F6 bank1, and removal of unconditional arrow deletion whenever any halo is active. These source changes do **not** prove physical simultaneous sprites or correct visible arrow flight.

## Open release blockers (NOT VERIFIED / PARTIAL)

1. Shared physical renderer for **two separate knights plus a world-camouflaged Ranger simultaneously**, especially overlapping Y and Level 3; present visual `ChooseP1` selects one actor per frame.
2. Actual visible Ranger arrow across successive physical frames and correct collisions (player / world solids / halo radius / edge). Prior test frames alone are insufficient evidence of full arrow mechanics.
3. A readable magic 360-degree halo following **both player X and Y**; current visual PF2 path remains partial/occasionally displaced or obscuring; logical radius is not a render PASS.
4. Eight distinct finished open worlds (forest, mountain, dream/static spiral, night), collision-safe routes and meaningful art. Existing layouts and palette changes are provisional.
5. Physical numerical score/lives/stage HUD, complete game-over presentation, full scoring/extra lives and 1..8..8..1 progression in a genuine uninterrupted playthrough.
6. Full dual-voice SFX repertoire with verified warning priority, overlap, real sound output audition, final volume envelopes and no stuck notes.
7. Full-stage and long-run tests, 262 NTSC **each** active frame under combat, 76 CPU cycles/physical scanline and real beam write deadlines; RIOT/stack high-water and no aliasing; final gameplay and hardware compatibility.

## Work boundaries and preservation

- **STOP applies now:** no further gameplay coding, design changes, emulator tests, commits or automation beyond this explicitly requested archival/status write.
- Keep F8 frozen checkpoint and latest F6 artifacts accessible; leave PR #51 **draft/unmerged**; leave `main` untouched; do not publish a public release, claim independent Verification, close Issue #50 as completed, or label this ROM release candidate.
- Resume only after an explicit new user instruction. When resuming, check live branch/PR, full authority chain and current CI/artifacts first, because the values in this document are a dated snapshot.
- This handoff records an honest developer checkpoint. `SOURCE_ONLY` changes remain distinguishable from `DEVELOPER_OBSERVED` emulator results; `MAIN_REVIEWED` and `INDEPENDENT_VERIFICATION` are not implied.

## Relevant controlling sources

- MAIN IV reviewed finish order: https://github.com/Odourman/the-skraun/blob/handoff/mainiv-fullgame1-finish-entire-skraun-20261123/handoff/MAIN_IV_FULLGAME1_COMPLETE_GAMEPLAY_VISUAL_AUDIO_REVIEW_AND_FINISH_ORDER_2026-11-23.md
- FULLGAME-1 16 KiB handoff: https://github.com/Odourman/the-skraun/blob/handoff/mainiv-fullgame1-finish-entire-skraun-20261123/handoff/MAIN_IV_TO_ROM_DEVELOPMENT_IV_FULLGAME1_COMPLETE_PLAYABLE_RELEASE_CANDIDATE_2026-11-23.md
- Prior progress snapshot: `docs/fullgame1/IMPLEMENTATION_PROGRESS.md`.
