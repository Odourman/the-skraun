# THE SKRAUN – FULLGAME-1 – ROM DEVELOPMENT IV: improved combat halo and shared HMOVE
Date: 2026-11-25 (Europe/Stockholm)

**Outcome:** DEVELOPER_OBSERVED_BOUNDED_PASS / NEW_PLAYABLE_EXPERIMENT / NOT_FINAL_RELEASE_CANDIDATE.

## Exact source and checkpoints

- Isolated draft PR #55: https://github.com/Odourman/the-skraun/pull/55
- Parent last accepted bounded developer checkpoint: PR #54, ROM SHA-256 `45a6c84b01910e6021e398f71096e435ea68c750867eaa826d0ee03dc64e1dbf`. Existing PR #54 and frozen adaptive PR #53 are unchanged, and rejected sparse PR #52 is not integrated.
- Current new source: `experiments/fullgame1_arrow_halo_20261125/bank0.asm`–`bank3.asm`, `build.py`. The prior checked-in `THE_SKRAUN_ARROW_HALO_F6_NTSC_EXPERIMENT.bin` was **removed from this new branch** because it had obsolete bytes; old binary remains available in frozen predecessor branches. Regenerate exact new .bin from source using DASM and the pinned builder or download the GitHub Actions artifact.
- New ROM: **standard F6, 4 × 4096 bytes = 16384 bytes**, SHA-256 **`9f5cc2440405ffeb9ca25eaf62a9deafd1432f90d4db56d2863f863cf19bda90`**. The builder asserts this exact result; it copies the generated playable file to `build/fullgame1/THE_SKRAUN_FULLGAME1_F6_NTSC.bin` for Stella.
- CI: https://github.com/Odourman/the-skraun/actions/runs/45630157117 — actual DASM plus Stella 6.7.1 **SUCCESS**. Source/binary/listings/debugger artifacts: https://github.com/Odourman/the-skraun/actions/runs/45630157117/artifacts/15030019192

## Actual implemented improvements

1. Three **closed inner elliptical P0 magic-runic outlines** (37,57,77 source raster rows), ORed into active player rune while normal U1-LEG1 A/B source masks remain unchanged. This improves gold pulse continuity without increasing any hot raster instruction count. The effect is not a physically faithful full-radius perimeter.
2. M0 side arc width increased to 2,4,8 TIA missile pixels for levels 1,2,3 using high NUSIZ0 bits while preserving low P0 sizing bits.
3. Ranger physical M1 arrow width 2 pixels using high NUSIZ1 bits set once during Reset; actual Y is still the independent 2-rasterline arrow sprite and game logic still enforces first visible-frame grace, fixed shot direction, world/edge damage and radial halo collision. Precise physical projectile hitbox vs 2px drawn width is not fully proved.
4. Knight warning's 24-frame animation additionally has **steady gold armour**, active strike orange, neutral knight blue. Ranger becomes bright during bow draw/release or while its M1 is active, not invisible by world-color camouflage. The old unconditional M1-time COLUP1 override was removed so sword warning remains readable while a shot is in flight.
5. Three independently positioned TIA objects (P0,P1,M1) now share **one WSYNC/HMOVE per frame**, instead of separate HMOVEs, saving 1–2 VBLANK lines while preserving independent RESP0/RESP1/RESM1 + fine-HM registration. Original optional M0/BL setup and orb placement remain separate; after the saved timing slack, their INTIM threshold was safely lowered from 12 to 9 ticks and M0 gate 14 to 11 ticks.
6. The full original ongoing FULLGAME-1 gameplay code, actor AI, eight test worlds, sound bank, HUD, lives, stage transitions, and core player movement are retained. No new >16KiB mapper, no F6SC RAM, no main merge.

## Exact real tests (no inflated evidence)

- GitHub Actions native 16 KiB DASM and SHA verification: PASS.
- Real Stella 6.7.1 **17/17 sampled final-frame scenes**: 262 NTSC lines, including `stage2_L3`, `arrow_first`, `gameover_restart`, and the previous `stress_120` endpoint.
- **120 consecutive real Stella frame steps with 120 individually printed `_scanEnd` values**, preserved in 12 separate 10-frame debugger-session blocks, each 262 NTSC. Dedicated second test prints `DEVELOPER_OBSERVED_120_CONSECUTIVE_INDIVIDUAL_NTSC_PASS` and saves a JSON audit. This is different from the old stress_120 scenario that merely saved states without separately measured counts.
- Local, separately marked **synthetic** screenshots: actual TV image after L3 + active halo and actual 2px M1. Synthetic RAM fixtures are not natural uninterrupted playtests. A separate local `stage2_L3` run on this exact byte-for-byte ROM ended at 262.
- **NOT TESTED:** original console / RetroN77; complete 76 CPU cycle + all TIA beam-write deadline paths; independent RIOT RAM/stack high water; exhaustive projectile collision under every overlapping actor; long natural 1-8-8-1 run; sound audition on the new exact ROM.

## Remaining scope / known design compromises

- The gold runic outline is **closed inside the physically expanded P0 footprint**, but the entire logical 18/28/38 halo radius is *not* drawn as a complete coherent outer circle: M0/BL are side arcs sharing scarce TIA resources with the orb. Under high VBLANK load the optional setup may still be skipped despite improved budget. Do not claim FULL_HALO_VISUAL_PASS.
- Three enemy AI actors remain logically alive concurrently, but *only one full physical P1 image is shown per frame*, adaptively prioritized for warnings/bow; full three-sprite same-Y simultaneous rendering has NOT been solved.
- The Ranger remains camouflaged outside danger/draw periods, but flashes bright during aimed threats to avoid unfair invisible attacks; source-level creative concession, not user-aesthetic signoff.
- Enemy beam overlap, exact octagonal vs displayed perimeter, L3 open-route geometry, full progression and physical stack extremes remain pending.

## Next meaningful development direction

Do not re-run unchanged 262-frame tests alone. Focus on a genuinely radius-faithful halo presentation while P0 is moving and M1 arrow / P1 warning / BL orb remain visible; then targeted combined combat/beam/RIOT hardware checks. Preserve all previous 16KiB SHA checkpoints. No autonomous main merge, independent Verification or public release.

**Disposition:** BEST_BOUNDED_DEVELOPER_IMPROVEMENT / MAIN_REVIEW_REQUIRED / FULLGAME1_STILL_OPEN.
