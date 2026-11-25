# THE SKRAUN — GRAPHICS II / MAIN V FINAL EIGHT WORLDS (2026-11-25)

**SOURCE_ONLY.** User-approved visual reference → 16 motifs → eight unique Atari 2600 PF1 map tables (8 × 96 = 768 bytes). No ROM implementation, no Stella render of new graphics, no canon change or merge to main.

## Files
- `03_PLAYFIELD_DATA.asm`: verified-byte-identical to the complete package source. Replace only existing bank3 `PlayPF1` table between `ORG $FA00` and `ORG $FD00`, after separate MAIN ROM authorization.
- `04_MOTIFS_SOURCE_ONLY.json`: 16 source motifs, stage mapping and mirror/repeat flags.
- `THE_SKRAUN_MAIN_V_FINAL_EIGHT_WORLDS_GRAPHICS_SOURCE_ONLY_2026-11-25.zip`: **complete 118-file package** with all eight individual scenes, 16 motif images, gold palettes, actor scale references, collision candidate overlays, before/after source comparisons, eight original PR60 Stella captures (unaltered), supplied approved image, exact assembler source, full JSON, proposed AABB WorldRects, source audit, tested reproducible generator and SHA256SUMS.

## Exact provenance and tests
- Baseline: [draft PR #60](https://github.com/Odourman/the-skraun/pull/60), immutable source head `2af9855fbe8d3edbe6d01609d3e539547b744aef`; original ROM SHA256 `3977c1e04e2cb5a43944e32477b8fa6f443bff270e3af8db4ae3d25e497b9647` (baseline, *not* new art ROM).
- PF1 byte stream SHA256 `deba82b22fae37567f885a90e4ea4a862e893d3be1f91653c21c8ef53d3c824e`.
- Complete ZIP SHA256 `35673f0474790336cfea58326ca318f444cc2175297e8cc7b86f3b2881233a78`, size 692409 bytes, 118 files. ZIP CRC and 117 SHA256 manifest entries PASS; generator reproduces file contents byte-for-byte.
- Main existing source pointer table and mirror/repeat behavior remain exactly the same. Same eight stage table addresses; no new TIA registers in visible loop.
- *SOURCE_ONLY collision proposal:* 4 half-open AABB envelope rectangles per stage in complete ZIP, not applied. Source BFS L3 navigation connected from (80,88), but actual joystick, orb placement, sprite timing, exact collider fairness and 262-scanline Stella must still be tested by ROM DEVELOPMENT after new MAIN order.

[Complete ZIP in Google Drive](https://drive.google.com/file/d/1SLLWRmuxhMSBAALzuCHJm11rWFDgbo2r/view)

**Status: GRAPHICS II source-only delivered, STOP.**