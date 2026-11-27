# THE SKRAUN — GRAPHICS II → MAIN VI
## Shield knight & eight worlds, SOURCE_ONLY, 2026-11-27

Frozen PR76/C `bd499a0736a8ed09c9e733e90387188176870039`, original ROM 16,384B SHA256 `1170604965d062916b71b48335f5ffef089bf89b8eec0418f6b17b9582d82dc1`; graphical sources based on real PR76 bank0/bank2/bank3 and inspected original gameplay footage.

**Recommend knight `C_SHIELD_CONTOUR`:** narrow transparency between shield and body, human helmet with dark horizontal visor, coherent torso, attached sword, physically stable centre and feet. Alternative `C_SHIELD_SOLID` is also supplied. New masks are 8×16 top-first sources converted to bottom-first ROM with trailing zero byte; REFP1 mirroring and VDELP1 are unchanged. Both offer WALK_A and WALK_B plus WARNING and STRIKE. Current three K1 17-byte tables can be replaced at identical space by the supplied drop-in. **WALK_B requires separately authorized renderer/pose-selection work:** existing F7A8..F820 bank3 data region has only 9 bytes spare, but WALK_B takes 17 bytes plus pointers/code. Keep Ranger masks unchanged and do not claim M1 is available; it is currently the arrow.

**Eight stages:** direct swap of existing `PlayPF1` 768-byte region only after MAIN authorization, preserve `WorldPFIndex`, pointer tables, colours, CTRLPF modes, no new visible TIA writes. Odd stages reflect, even repeat. Total 37 byte changes against previous graphics source, stages 1/3/5/7 bit-identical. New PF1 stream SHA256 `8ee7ac1ee211a84fd9101b105ce86c3b08d412cc02db50e34f5af41678a4826b`. Original WorldRects remain: source-only 0 painted pixels outside AABB and L1/L2/L3 4-way BFS accesses both orb sites in all stages. But AABB invisible-solid fractions vary 9.3–44.9% (largest on forest/spirals); collision opening/visually traversable gaps are NOT fixed just by these bits. New collision code would need a separate scope.

**Timing conflict:** PR76 K1Warn=16 frames (0.267s), K1Strike=9 (0.15s), K1Rest=24 (0.4s), differing from earlier intended ~0.4s warning and ~1s recovery. No gameplay timers changed. Body/sword visual extent cannot equal the entire logical sword threshold with only eight P1 bits. L3 aura borrows P1 sometimes, so appearance under multiplex/colour/beam timings unproven.

**After MAIN graphics decision and separate ROM authorization:** ROM DEVELOPMENT can install the two 3-pose/PF1 table swaps first, verify DASM size and SHA, check Stella 262 scanlines/76 CPU cycles, VDEL/REFP1, enemy multiplex/auras, sword hit windows, orb pickups/collision fairness, palette. WALK_B needs an additional separately scoped step with ROM placement and pointer selection. Independent Verification is separate and not authorized now.

**Complete self-contained 209-file ZIP** with source reference images, full JSON/binary/hex mask sets, all GIFs, eight world previews, battle/L3 static composites, before/after PR76 graphics, exact baseline PR76 asm, reproducible Python generator + checksums: [Google Drive](https://drive.google.com/file/d/16cxgQDsPhVRKEmP-nlBYLNNw7pcJ0RHy/view?usp=drivesdk).
ZIP SHA256 `d413fbb33a0249fdef7788044fea19909fd0f6886c2a3249a8b0d693030eecad`, size 1,144,715 bytes, 209 ZIP entries, CRC PASS.

**Status: SOURCE_ONLY / delivered / STOP.** Do not change PR76 branch, ROM, mapper, current combat scope or main.
