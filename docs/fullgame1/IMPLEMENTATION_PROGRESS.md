# FULLGAME-1 – REAL M1 EXPERIMENT (NOT A RELEASE)

Authorised by MAIN IV Issue #50. Frozen baseline GAMEPLAY-5 is intact on PR #49, 8KiB F8 SHA256 b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca.

The first 16KiB F6 checkpoint is byte-exact in banks 2/3, SHA256 bedf6b67e202bdbebfa5b8a5499a4e99ac9a3509ecc1750e3ca6f5d2aa6536ab (DASM+Stella physical bootstrap only).

An **experimental** bank2/3 patch adds a genuinely released M1 projectile with a second renderer loop. Arrow movement and collision use real ArrowX/Y state, and the M1 two-raster-row profile is selected in the visible kernel only when ArrowDX active. The previous independent halo draw is used otherwise, avoiding one additional row-lookup on the normal loop. **Not yet confirmed by Stella**; no claims for full physical arrow, 76-cycle beam deadlines or all frames.

Current provisional compromise in trial: any active halo clears the in-flight projectile globally, to ensure no invisible projectile damages the player while the arrow-only renderer is selected. This is a **design deviation**, not approved final radius-based arrow cancellation. Needs replacement or explicit final disclosure.

This branch is in progress. Missing: proper 2 knights+Ranger, 8 distinct maps, X/Y halo, HUD, exhaustive timing and playable 8-stage loop. Do not merge or release.

## ROM DEVELOPMENT IV implementation continuation – 2026-11-23

Authority: Issue #50, full 16KiB mandate. This remains a **DEVELOPMENT CHECKPOINT**, NOT a complete-game release candidate. PR #51 remains draft. Frozen GAMEPLAY-5 remains untouched.

Source changes on this branch:
- Independent K1 and K2 chase now test world-solid rectangles and attempt X/Y sliding with actual actor positions, with identical blocker applied to Ranger's flight/flee AI. These are genuine offscreen game-logic source changes, not new physical TIA sprite renderers.
- Knight telegraph/strike have distinct TIA channel-0 sound cues; reserve knights begin a 120-frame wait when a knight slot opens.
- Adjusted stage4/stage7 BL orb X positions for L3 growth and added an eight-stage source-only center-geometry collision assertion.
- Extended real Stella regression test definitions to 17 discrete final-frame scenes plus 120 consecutive state captures, and hardened workflow source-path triggers. The 120 captured saveSes intermediate files do NOT currently provide 120 individually measured scanline counts. Do not call these 120 NTSC PASS.
- Frozen 8KiB GAMEPLAY-5 remains unchanged. The experimental 16KiB F6 test ROM is built from four DASM banks; SHA varies only when source-derived F6 output changes. Do not label this as a finished executable release.

**Observed at authoring time:** fast-DASM built with the corrected orb-source test on commit `7a19cf8060d17a44f07d1b80870807ee69d0ad63`, workflow run https://github.com/Odourman/the-skraun/actions/runs/45167734542 . The full Stella job was still running at authoring time; no result claimed. Previously 17 sampled final frames had _scanEnd 262 in https://github.com/Odourman/the-skraun/actions/runs/45166944683, but this job FAILed the stricter continuity test; those frames do not establish beam timing or full game.

**Still incomplete:** independent physical three-enemy sprite multiplexing at realistic overlapping Y; proved visible Ranger projectile that collides correctly; visually X/Y-following halo; eight genuinely different finished maps; HUD; full progression and long gameplay test; full worst-case 76-cycle/write-deadline and RIOT stack proofs. Never report FULLGAME1_DELIVERED at this checkpoint.
