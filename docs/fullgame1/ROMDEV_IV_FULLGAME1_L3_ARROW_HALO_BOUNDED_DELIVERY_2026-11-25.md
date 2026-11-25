# The Skraun – ROM DEVELOPMENT IV / FULLGAME-1 L3 raster repair (2026-11-25)

**Classification: DEVELOPER_OBSERVED / BOUNDED_NTSC_PASS / NOT_RELEASE_READY.** Original Issue #50 scope remains in force. This is not independent Verification or MAIN review.

## Source chain and runnable ROM
- Frozen adaptive source baseline: PR #53, commit `7a2f34e267a46bfcac909a5d96d6589f98f8ec67`, ROM SHA `d2a0a1b57ac9c78b2af14f77800f7c1ecf99aaa43f60e8c4216974f18aed2a0e`.
- This development branch: `experiment/fullgame1-arrow-halo-romdev4-20261125`, draft PR #54, based on PR #53. The rejected PR #52 is not merged.
- Old arrow/halo experimental ROM SHA `a9189404275d4c3e5f04c246033290384c64d0ffcc127ff73229522d9a81e8a3` had `stage2_L3=263` (real Actions #45602662669) and remains frozen as failed source evidence.
- New fixed-source commit `706b86d7e4c172fa64d1c18fda8a5dd18fad10c5`; CI test script and workflow added through `42b51e3d10a7b2c48553dfa9218e5c785b86a0a5`. Exact regenerated standard F6/NTSC ROM SHA-256 `45a6c84b01910e6021e398f71096e435ea68c750867eaa826d0ee03dc64e1dbf` (16,384 bytes, 4×4096). No F6SC RAM.
- Rebuild from repo: `python3 experiments/fullgame1_arrow_halo_20261125/build.py` using real DASM 2.20.14.1. Builder enforces exact candidate SHA. The old tracked experimental .bin in repo predates the fix; select `build/arrow_halo_romdev4/THE_SKRAUN_FULLGAME1_ARROW_HALO_F6_NTSC.bin` from CI artifacts or the consolidated ZIP for new ROM.

## Actual developer-observed proof (exact new ROM)
- [First physical regression](https://github.com/Odourman/the-skraun/actions/runs/45626337675): real DASM and Stella 6.7.1, **17/17 selected scene endpoints _scanEnd=262**, with `stage2_L3` repaired to 262. This is not each active frame or full beam proof.
- [Full regression with independent per-frame capture](https://github.com/Odourman/the-skraun/actions/runs/45627382380): green **17/17** and **120/120 individually measured consecutive Stage2-Level3 frames _scanEnd=262**, from a genuine Stella debugger, 12 ten-frame preserved typed sessions plus `120_INDIVIDUAL_SCANENDS.json`. The workflow is now required to report each frame, not only save 120 states. Separate developer-local 90/90 individually measured frames also logged.
- CI artifact: https://github.com/Odourman/the-skraun/actions/runs/45627382380/artifacts/15029826123 (DASM source/listings/symbols, ROM, Stella debugger scenes, all 120-frame files).
- Google Drive fully bundled developer checkpoint with ROM, frozen adaptive fallback, 17-scene and 120-frame evidence, source, PLAYTEST and deviations: https://drive.google.com/file/d/127JhRB1OVu5Yr8CVWuux7584cITul26W/view

## Causal technical change
`NewHaloSetup` first reads real TIA/RIOT `INTIM`; with fewer than 12*64 6507 cycles remaining in VBLANK, it clears the optional M0 missile enable and returns rather than doing late M0/BL repositioning. Source-visible P0 player rune and active radial gameplay logic remain in place; the physical M1 ArrowY two-raster-row renderer and frozen adaptive P1 scheduler are untouched. Branch-before-work avoids the previous Stage2 L3 extra 263rd physical scanline; measured result is 262. This choice can remove a side halo accent during a heavy frame and therefore does **not** meet full visual-circumference canon.

## What is not yet finished
- An actually **visually closed, obvious 360-degree ring** at all three radii following both PlayerX/Y under Level3+3 enemies+M1+orb+HUD; current runic P0 plus optional M0/BL segments are visually PARTIAL. Do not call finished halo.
- The original real-arrow graphic uses 2-scanline ArrowY, but full sequential physical pixel-motion and full combined hit/halo/world edge-case coverage not certified beyond selected sampled scenes; actual `SpawnArrow` lives in F6 bank0 and writes two-frame freshness to `$9D`. Bank2 `LaunchArrow` old 180-frame code is a legacy inactive path, **not** the active game behavior.
- Three independent **logical** K1/K2/Ranger with one time-shared P1 full sprite per video frame. Real same-frame triple P1 silhouettes and 24 frames of fully legible simultaneous warning remain unproven.
- Worst-case 76 CPU cycles/physical scanline and TIA write-before-beam deadlines, physical RIOT/stack high-water, original Atari/RetroN77, full 1..8..8..1 uninterrupted player-driven run, naturally reached GAME OVER, all bonus and audio events are still unverified. 120 physical 262 counts do not prove them.
- Some eight-world art and HUD/lives display are provisional. No claim that gameplay balance/visual user acceptance has happened.

**Disposition:** best current developer-tested playable arrow/halo F6 checkpoint, not a complete release candidate. PR #54 stays draft/unmerged; Issue #50 stays open. No main merge, public release or automatic independent Verification.
