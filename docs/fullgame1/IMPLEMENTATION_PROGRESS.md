# FULLGAME-1 – REAL M1 EXPERIMENT (NOT A RELEASE)

Authorised by MAIN IV Issue #50. Frozen baseline GAMEPLAY-5 is intact on PR #49, 8KiB F8 SHA256 b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca.

The first 16KiB F6 checkpoint is byte-exact in banks 2/3, SHA256 bedf6b67e202bdbebfa5b8a5499a4e99ac9a3509ecc1750e3ca6f5d2aa6536ab (DASM+Stella physical bootstrap only).

An **experimental** bank2/3 patch adds a genuinely released M1 projectile with a second renderer loop. Arrow movement and collision use real ArrowX/Y state, and the M1 two-raster-row profile is selected in the visible kernel only when ArrowDX active. The previous independent halo draw is used otherwise, avoiding one additional row-lookup on the normal loop. **Not yet confirmed by Stella**; no claims for full physical arrow, 76-cycle beam deadlines or all frames.

Current provisional compromise in trial: any active halo clears the in-flight projectile globally, to ensure no invisible projectile damages the player while the arrow-only renderer is selected. This is a **design deviation**, not approved final radius-based arrow cancellation. Needs replacement or explicit final disclosure.

This branch is in progress. Missing: proper 2 knights+Ranger, 8 distinct maps, X/Y halo, HUD, exhaustive timing and playable 8-stage loop. Do not merge or release.
