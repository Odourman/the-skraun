# GRAPHICS II – MAIN VI Knight & Eight Worlds (2026-11-27)

**SOURCE_ONLY; for MAIN VI selection.** No ROM implementation, no merge, no independent Verification.

Based on exact [PR76/C](https://github.com/Odourman/the-skraun/pull/76), code SHA `bd499a0736a8ed09c9e733e90387188176870039`. Existing ROM SHA-256 `1170604965d062916b71b48335f5ffef089bf89b8eec0418f6b17b9582d82dc1`.

## Browse
- [MAIN_HANDOFF.md](MAIN_HANDOFF.md): technical review, source checks, navigation and integration constraints
- [WORLD_PF1_DROPIN_SOURCE_ONLY.asm](WORLD_PF1_DROPIN_SOURCE_ONLY.asm): **exact 8×96 bytes** replacement table
- [KNIGHT_P1_DROPIN_SOURCE_ONLY.asm](KNIGHT_P1_DROPIN_SOURCE_ONLY.asm): **3×17 bytes**, including existing zero guard
- [COMPLETE_SOURCE_ONLY.zip](COMPLETE_SOURCE_ONLY.zip): 131-file reproducible delivery: all source masks, Python generator, original PR76 bank0/bank2/bank3, actual original gameplay video contact sheet, all 8 worlds at multiple sizes, 16 motifs, two knight families and GIFs, JSON and SHA256SUMS.

**Recommendation:** K1 T-visor; refined eight PF1 stages. Ranger/R1, P0/U1-LEG1, halo, orb, HUD, M1 arrow, collision code and original ROM are untouched. Existing four AABB collision rectangles per stage preserved; source-only 4-way BFS confirms both alternative orb centers reachable from stage center at L3 in all eight worlds.

**Full ZIP SHA-256:** `aa29c82918804472adca6bd276b724964f03ab7df703e3562ffe57b3f869f4fb`. **PF1 byte stream SHA-256:** `5ed1067c44dba05bb4da19920c659167f1828d99ec5b52210f634a14b72c0ec8`.

[Same ZIP in Google Drive](https://drive.google.com/file/d/1kUHpqhWJiNyj0rHwL1SoPDH_zyIcoA4e/view)

**STOP after delivery.** MAIN must separately authorize ROM integration.
