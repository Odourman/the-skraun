# ROM DEVELOPMENT IV – FULLGAME-1 – BEST PLAYABLE DEVELOPER HANDOFF (2026-11-25)

**Classification:** `DEVELOPER_OBSERVED / BEST_PLAYABLE_DEVELOPMENT_CHECKPOINT / RELEASE_CANDIDATE_NOT_READY`.

This document is an honest completion-state handoff for the latest MAIN IV whole-game authorization on Issue #50, not a claim of a complete release. The explicit later user request resumed FULLGAME-1 after the earlier pause. Keep the older stop note as historical and separate from this newer implementation work.

## Exact frozen development baseline

- Repository: https://github.com/Odourman/the-skraun
- Latest real **implementation** commit: `5553c419f4bd5159612e79c7bfb5dc17f7c41001`. This handoff commit changes documentation only, not the executable bits.
- Development branch: `experiment/fullgame1-complete-skraun-20261123`, open draft PR https://github.com/Odourman/the-skraun/pull/51.
- Candidate mapper: standard Atari 2600 F6, four 4096-byte banks; **total exactly 16,384 bytes**. No F6SC RAM dependency. Compatible mapper scheme does not establish physical hardware compatibility.
- SHA-256 for actual last successful experimental F6 ROM: `146c6541c673b10d2dc44304627b67ce9a5e3788e39d087d73251cfd3f50767c`.
- Exact frozen earlier GAMEPLAY-5 F8 ROM SHA-256: `b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca`. Frozen F8 untouched.
- Real full DASM/Stella/audio Actions workflow **success**, on implementation SHA above: https://github.com/Odourman/the-skraun/actions/runs/45520490449 ; artifact https://github.com/Odourman/the-skraun/actions/runs/45520490449/artifacts/14979553907.
- Fast real four-bank DASM: https://github.com/Odourman/the-skraun/actions/runs/45520490365 ; artifact https://github.com/Odourman/the-skraun/actions/runs/45520490365/artifacts/14979498633.
- The source is fully reproducible from `python3 scripts/fullgame1_build.py` with real DASM; all four generated source banks, symbols, listings and logs are contained in the workflow artifact. Prior F8 SHA is build-asserted.
- Complete user-playable 16KiB ROM and standalone build/test/source/audio/screenshot ZIP are also provided directly to the user in the requesting conversation. The ZIP was rehashed before handoff.

## What is actually implemented

1. Original source-based Skraun with joystick eight-way movement and levels 1–3, wall avoidance, orb upgrade, FIRE halo logic and gold player/world feedback. The **actual visual halo radius/ring is not represented correctly**; do not imply otherwise.
2. Three independent **logical** actors: K1/K2/Ranger, real X/Y movement, obstacle avoidance, reserve timing, warning and sword-phase semantics. The real visible P1 sprite follows each selected actor's Y instead of old fixed-Y. **Only ONE P1 actor is displayed per frame** with temporal selection among all three. It is **not** a proven physical three-sprite renderer, and produces visible flicker. A logical knight's sword hit is gated to its visible slot so an invisible sword pose should not harm Skraun. This is a significant gameplay/presentation deviation, not full canon.
3. Ranger fire uses physically real TIA missile M1, fixed direction at launch and logical projectile wall/body/halo checks. The sprite visibly moves in sampled consecutive frames at a deliberately **quantized 8-raster-row vertical band**, with real fine X movement. The former bug erasing any arrow anywhere during halo was removed. Full cross-case projectile fairness remains unproven.
4. Eight distinct PF1 metatile patterns and eight different rectangle geometry sets: forest1–2, mountain3–4, static-spiral dream5–6, night7–8. This supersedes shifted-copy test layout but is still lightweight provisional art. Source stage pendulum logic 1–8–8–1–1–2 is present.
5. Five-scanline P0/PF score/lives HUD: four actual decimal BCD point digits, simple life pips, +100 knight/+250 Ranger, 2000-point extra-life accounting in logic (source-only threshold), game-over red "GO" graphic retaining final score, and FIRE/RESET restart. Beyond four lives the pips visually saturate; score wraps beyond 9999. Normal continuous full-game scoring/extra life was not tested.
6. Two-channel TIA sound event system with short envelopes and priority; 7.036 seconds of actual Stella 6.7.1 audio recorded, WAV SHA-256 `7b562bbc8259cc4b1cc18683a094609ef50f9671163a4242c2a81c548f4ae89d`. This is captured output, **not** a subjective listening review or proof of each overlapping event's timing.

## Real developer-observed evidence (bounded)

- GH Actions after actual DASM compiled all 4 banks and ran real Stella, with **17/17 selected endpoint frames** reporting 262 NTSC scanlines. Treat these as selected samples only.
- Additional *local* run on the **same exact ROM SHA** executed 120 consecutive `frame #1`, `print _scanEnd`, `saveSes` iterations. **120/120 physical frame end counts were 262** with an individual complete Stella session file for every measured frame. This fixes older tests that had 120 saved states but no individual _scanEnd proof.
- Additional *local* stage-pendulum source/ROM test issued diagnostic `ram $be #1` to trigger transitions without defeating enemies. It visited **18 physical stages**: 1,2,3,4,5,6,7,8,8,7,6,5,4,3,2,1,1,2; 18 sampled endpoint _scanEnd values were 262. This is **NOT an uninterrupted natural progression test**. Screenshots include different world visual patterns.
- Human joystick/FIRE Stella test killed a knight and awarded a BCD 100 points; separate normal joystick pickup raised Level to 2. Level3 upgrade and Stage2 required a diagnostic forced transition.
- Ranger arrow visually traversed multiple physical frames. A deliberately isolated diagnostic that disabled two knights tested a Ranger projectile hitting the player and reduced lives 3→2. This is **not proof** that all combined K1/K2/Ranger combat sequences are fair.
- GameOver was exercised with diagnostic `ram $ac 0`; red GO and existing score were visible, FIRE returned to Stage1 with 3 lives and 262 end scanlines. Natural loss of all lives in a continuous game was not exhaustively tested.
- Screenshots, debug logs, per-frame results and authentic WAV are in the supplied user ZIP and GitHub artifact. Evidence may be **DEVELOPER_OBSERVED** only; no independent Verification or original hardware measurements.

## Unresolved release gates and explicit deviations

- **Major:** No actual simultaneous physical rendering of three complete independent P1 enemy sprites; current 3-way per-frame slot multiplexing is a compromise, 20Hz-per-actor flicker and danger feedback need human playtest. This remains a breach of desired full visual canon.
- **Major:** Halo's 360-degree *mechanical* radius works, but gold coloration does not show a correctly centered circular outline and range at three sizes. Visually partial, despite X/Y player glow.
- **Major:** No proven uninterrupted gameplay clearing all 8 stages forward and backward with all enemies, reserves, lives, bonuses and normal game-over.
- **Major:** 76 cycles per physical scanline, exact individual TIA write-before-beam deadlines, peak RIOT RAM and 6507 stack use are not fully quantified. NTSC 120/120 alone does not prove these. Original physical Atari 2600 and RetroN77 never tested.
- M1 visual Y only at 8-scanline precision; logical hitbox may diverge a few scanlines from the displayed projectile. Under every pathological moment, unseen hits cannot be ruled out.
- World art remains simplified, stage geometry/movement particularly with largest L3 not exhaustively playtested. Color contrast and Ranger concealment not fully aesthetic-reviewed.
- Score UI tops at four digits/9999 and life pips not distinct above four; red GO is an abbreviated GameOver presentation.
- Sound is demonstrated by authentic audio WAV but no event-by-event or listening/volume review performed.
- U1-LEG1 8x12 original mask source is retained, but not independently pixel-verified for every L2/L3 displayed pose.
- Creative adaptations were taken to keep TIA/6507 raster physical: 8-line arrow visibility; alternating P1; coarse PF stage art; P0 gold halo feedback. These were technically chosen by developer, **not user aesthetic approval**.

## Practical instructions and release handling

For local play: load exact 16KiB F6 .bin in Stella NTSC; joystick directions move; FIRE triggers halo; pick up BL orb for levels; avoid warned sword and Ranger arrow; FIRE/RESET restarts when dead. The downloadable user ZIP contains the full Swedish PLAYTEST manual, generated bank source and reproducible shell build, actual DASM logs, screenshots, 120-frame and 18-visit raw Stella evidence and WAV. Unpack and run `REBUILD_GENERATED_SOURCES.sh` with DASM to reproduce exact hash; or clone PR branch and use `python3 scripts/fullgame1_build.py`.

**Verdict: this is a genuine playable developer checkpoint and best available fallback, NOT yet a full release candidate.** Do not mark FULLGAME-1 as completed, do not mark PR #51 ready for final review, do not merge to `main`, initiate independent Verification, or publish. Next work should address major mechanics/physical playtests, not status-only or sound polishing. Any later resumption should read this document and inspect live code + authority first.
