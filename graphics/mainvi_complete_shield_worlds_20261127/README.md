# THE SKRAUN — GRAPHICS II / MAIN VI — Knights, Shield & Eight Worlds
**SOURCE_ONLY** graphics delivered 2026-11-27. ROM baseline [PR76/C](https://github.com/Odourman/the-skraun/pull/76) at `bd499a0736a8ed09c9e733e90387188176870039`.

The user-provided design references and original graphics source are preserved in [the complete 209-file ZIP package](COMPLETE_SOURCE_ONLY.zip). This package contains: source mask generator and validator, all 8 PF1 stage masks, 16 motifs, 2 knight versions with 4 poses and 8x16 mirrored binary/hex masks, walking/attack GIFs, original-size and zoomed previews, original PR76 gameplay contact sheet, before/after comparisons, source-only L3 orb-access audit and collision overlays, source proofs and SHA256SUMS.

**Recommended shield knight:** `C_SHIELD_CONTOUR` (transparent gap between shield and breastplate), alternative `C_SHIELD_SOLID`. WALK_A, WALK_B, WARNING, STRIKE all constructed in same 8×16 P1 footprint. Existing three poses in [KNIGHT_P1_DROPIN_SOURCE_ONLY.asm](KNIGHT_P1_DROPIN_SOURCE_ONLY.asm) can replace existing 3×17 bytes, after MAIN authorization/ROM tests. WALK_B is NOT a drop-in: requires new pointer/code and relocation because only 9 unused bytes remain in current F7A8..F820 data block.

**Recommended worlds:** [WORLD_PF1_DROPIN_SOURCE_ONLY.asm](WORLD_PF1_DROPIN_SOURCE_ONLY.asm) — 8×96=768 bytes; 37-byte difference from previous source-only graphics, all within stages 2,4,6,8. Odd stages mirrored and even repeated, same PR76 visible renderer. PF1 stream SHA256 `8ee7ac1ee211a84fd9101b105ce86c3b08d412cc02db50e34f5af41678a4826b`.

**Known SOURCE_ONLY limits:** 0 painted PF cells outside current AABBs, but AABBs still have invisible solids 9.3%–44.9% (stage-dependent). Source-only L3 4-neighbor BFS finds paths to both orb sites on all stages. This does NOT prove ROM joystick collisions, beam cycles, gameplay during aura or actual knight readability under P1 multiplex. Current timers in PR76 are 16/9/24 frames for warn/strike/rest; original design intent 24/short/~60. No timer changes.

Read [MAIN_HANDOFF.md](MAIN_HANDOFF.md) and detailed `02_ROM_INTEGRATION.md` inside ZIP. [Same ZIP in Google Drive](https://drive.google.com/file/d/16cxgQDsPhVRKEmP-nlBYLNNw7pcJ0RHy/view?usp=drivesdk).

ZIP SHA256 `d413fbb33a0249fdef7788044fea19909fd0f6886c2a3249a8b0d693030eecad`, 1,144,715 bytes. **No ROM edits, no merge, no independent Verification. STOP after MAIN VI review.**
