# MAIN VI → GRAPHICS II / SOURCE_ONLY completed 2026-11-27

## Authorized work and provenance
Exact PR76/C commit `bd499a0736a8ed09c9e733e90387188176870039`, original 16384-byte ROM SHA `1170604965d062916b71b48335f5ffef089bf89b8eec0418f6b17b9582d82dc1`. Original bank3 Git blob `8d839fee0eb4ec4ef9708490a25672b5a4819b13`. Developer-observed 120-second gameplay video read from original Drive archive. All new art is SOURCE_ONLY and not Stella-verified.

## Select a Knight
Recommend **K1_T_VISOR** over K2_BARREL_HELM. Exactly 3 × 17 bytes replacing existing K1NeutralBytes/K1WarningBytes/K1StrikeBytes only, 16 visible P1 bits per row, bit7 leftmost, ROM rows bottom-first, 17th byte zero guard, same center and foot positions, mirrored with existing REFP1. Visor is transparency, so P1 stays single colour. 0.4s warning remains controlled by existing gameplay code. Horizontal strike cannot extend outside 8-bit P1 footprint; visible and logical sword reach must be compared in real ROM. Optional walking B mask in archive is not a drop-in (requires selection/ROM work). Preserve R1 entirely and do not appropriate M1, presently the arrow.

## World data and scene differences
Each of stages 1–8 has a separate 96 byte source table, 768 bytes total. `WorldPFIndex` maps 2 physical scanlines per source entry. Odd stages use reflected PF1 (right x112–143 colour clocks). Even stages repeat PF1 (right x96–127); all even-source bit7 are zero, moving their active geometry to right x100–127 and left x20–47, consistent with existing stage rectangle X bounds. New world PF1 SHA-256 `5ed1067c44dba05bb4da19920c659167f1828d99ec5b52210f634a14b72c0ec8`. No changes to world colours, aura test model or TIA register writers.

## Source-only collision proof and limitations
All 8 maps have 0 painted PF1 pixels outside existing `WorldRects` envelopes under source-derived screen/game Y offset of +10. Four-direction (conservative) reachable-center BFS from center (80,88) with current L3 half width16 height15 and permitted x20..140/y19..157 reaches both potential orb positions (22,68) and (138,68), for all eight maps. However actual real joystick movement, orb acquisition/growth and physics were not emulated; AABB rectangles remain coarser than hollow windows in spirals/portals. No collider modification proposed for a graphics-only drop-in.

## ROM DEVELOPMENT future steps (not authorized now)
Only after explicit MAIN implementation order: preserve PR76 code and guard addresses, insert exactly two provided source-table replacements, DASM build, bank/hash check, test stage1–8 native Stella pixel profiles, P1 neutral/warning/strike VDEL/REFP1 under multiplexing, collision and orbs at L3, true halo coexistence, beam deadlines and 262 scanlines. If visual sword reach mismatches logical hitbox, report and stop for MAIN decision; do not change mechanics from graphics task.

Full reproducible ZIP (131 files) includes generator, binary/hex JSON, all previews, two GIFs, source records, original bank sources, actual gameplay contact sheet and 130 SHA256SUMS. [Drive mirror](https://drive.google.com/file/d/1kUHpqhWJiNyj0rHwL1SoPDH_zyIcoA4e/view).

**Status: SOURCE_ONLY / delivered / STOP. No main merge, no ROM changes.**
