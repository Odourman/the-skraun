# Revisionsproveniens och tillstånd

- 2026-11-25. MAIN V grafisk explicit revisionsorder från denna konversation.
- User APPROVED_GRAPHICS direction: `11_APPROVED_VISUAL_REFERENCE/USER_APPROVED_GRAPHIC_REFERENCE_UNMODIFIED.png` (användarbild, ej TIA-proof).
- R1 image: `11_APPROVED_VISUAL_REFERENCE/REVISION1_EIGHT_WORLDS_UNMODIFIED.png`, source-based screenshot, not Stella.
- R1 public frozen HEAD `bd18c41fc24e56759d13a182dceea6e4932eb16b`; delivered package, 118 files, SHA256 `35673f0474790336cfea58326ca318f444cc2175297e8cc7b86f3b2881233a78`.
- ROM baseline: draft [PR #60](https://github.com/Odourman/the-skraun/pull/60) frozen HEAD `2af9855fbe8d3edbe6d01609d3e539547b744aef`; 16KiB actual ROM SHA256 `3977c1e04e2cb5a43944e32477b8fa6f443bff270e3af8db4ae3d25e497b9647` (NOT updated by GRAPHICS).
- PR60 `bank3.asm` GitHub blob `62e88de692df80024db8342e0990640a5310f620` read through GitHub connector 2026-11-25; frozen exact original code snapshot in 09_GENERATOR.
- R2 new PF1 bytes SHA256 `253bd7180259cf699a4315379b900ca47801ae6259f0955a002bc601f5ef98f8` 768 bytes; created from exactly 16 source masks in generator.
- Rendering: Python Pillow nearest neighbour, derived from raw PF1 data; R2 previews are **NOT actual Stella**.
- Unmodified 8 older PR60 Stella images in 08_BEFORE_AFTER/ are for historic comparison only, not from a new R2 ROM.
- Bounded SOURCE_ONLY geometry BFS and mask parser, NOT actual joystick input, physical beam timings, RAM/stack or independent verification.
- No player/enemy sprite, sprites' original U1 masks, mapper, RAM, game ROM, gameplay rules, active branch or main were touched.
