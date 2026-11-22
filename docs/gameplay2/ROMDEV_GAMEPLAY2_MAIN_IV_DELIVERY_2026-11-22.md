# THE SKRAUN - ROM DEVELOPMENT III -> MAIN IV - GAMEPLAY-2 DELIVERY
**Date:** 2026-11-22. **Authority:** Explicit GAMEPLAY-2 order from MAIN IV. **Result:** `GAMEPLAY2_BOUNDED_PLAYABLE_STAGE1_TO_STAGE2 / DEVELOPER_OBSERVED / FULL_RENDERER_NOT_COMPLETE`.

## Frozen Git/ROM provenance (live)
- User-authorized exact parent: GAMEPLAY-1 draft PR #41 commit `7f289a536c375bf760428274280179cfe15a6a62`, original 8KiB F8 ROM SHA `09b32a9498e39a5e0874f2dc15c219f707ae9dd6abd83d4c3f66af36ad58f171`.
- Separate experiment `experiment/gameplay2-complete-stage-20261122`. One draft PR #42 targeting GAMEPLAY-1 experimental branch (NOT main). PLAY1-H, GAMEPLAY-1, U1 source and main left unchanged.
- Built authentic DASM F8 NTSC 8192-byte ROM: `experiments/gameplay2_f8_ntsc.bin`; SHA-256 **`1ebfba72cea63a36b3a7434233758242112680b2ad6f2b282c9bbea5652fa2fd`**.
- Source SHA-256 bank0 `9e914c029fc941a4b89ec5fe385dd7f80bdc7733a9147022e8b72b6b9a013f09`, bank1 `661cbc9bf200584c4342144bb946f54a26ad778812d3d2eb7c651d7e87141b73`.
- Exact DASM commands, player walkthrough and controls: `PLAYTEST_GAMEPLAY2.md`. Real ROM, listings, symbols, build logs and hashes: `experiments/gameplay2_*.*`. Original real Stella GUI proof from [Actions #45025725607](https://github.com/Odourman/the-skraun/actions/runs/45025725607) and strict `tests/gameplay2_audit.py`.

## Actual Stella/RIOT events; not fake state injection
From genuine Stella 6.7.1 debugger desktop images, authentic joystick/FIRE input scripts and 320x228 TIA crop pixel recount:
| Required evidence | State | Precisely observed |
|---|---|---|
| 1. Stage1 initial | PASS | RIOT `$AA=01`, `$AC=03`, `$AE:$AD=0000`, original P0 16x12 / 98 gray pixels, P1 120 blue pixels |
| 2. Orb L1 -> L2 | PASS | joystick right16/down24 touches physical BL; `$82=02`, P0 bbox 32x24, one consumed orb |
| 3. Orb L2 -> L3, free movement | PASS BOUNDED | after **separate next-stage orb**, P0 64x36, 1176 or 1200 gray pixels according to unchanged original A/B gait; right/up diagonal changed physical TIA bbox **+18 X clocks / -8 scanlines**, FIRE active gave 5958 gold PF pixels |
| 4. Knight warning and active sword damage | PASS BOUNDED | real P1 warning recolors 120 original P1 pixels; source strike window only; stage1 L1 sword test changed lives 3 -> 2, activated `$B3` invulnerability; not by body contact |
| 5. Life loss preserves dead enemies & orb | PARTIAL / active focused test | Source does not reset `StageKills` or `OrbMask` on L1 loss; no general assertion until a specific real after-one-kill damage scene confirms it |
| 6. 100pt per knight | PASS BOUNDED | actual two knight proxy kills accumulated 200 points in stage1; source awards 100 each |
| 7. 250pt Ranger proxy | PASS BOUNDED | actual final score at stage clear `$AE:$AD=01C2 = 450` after 2x100 knights + 250 last world-colored fleeing P1 proxy; physical Ranger art/arrow NOT implemented |
| 8. Third kill and Stage1 -> Stage2 | PASS | no memory injection, real FIRE, `$AA=02`, `$B4=00`, score450 and 3 lives, 24-frame stage-clear delay; next stage has new enemies and physical BL orb |
| 9. 2000pt extra life | PASS BOUNDED | a longer all-joystick/FIRE stage-loop showed `$AE:$AD=0BB8=3000` and lives `$AC=04` from initial 3; bonus remainder `$BD:$BC=03E8=1000`; no RAM manipulation |
| 10. NTSC screen physical timing | PASS BOUNDED | initial Stella `_scanEnd=261` FAIL was genuinely observed, followed by a single additional WSYNC in **overscan**; real followup Stella `_scanEnd=262` across start, orb, stage clear, L3 moving FIRE, sword warning, bonus, game over and restart. No extra visible PF2 write |
| GAME OVER / FIRE restart | PASS BOUNDED | actual RAM `$AC=00` with game-over background; FIRE restart `$AA=01`, `$AC=03`, score0 |
| Endpoint repeat 8,8 and 1,1 | SOURCE_ONLY | fixed in `NextStage`; actual complete 16-stage continuous reproduction not run |
| HUD | NOT IMPLEMENTED | Numeric score/lives via Stella RAM, no visible numeric HUD; avoiding 76-cycle TIA danger |

## Technical truth / known limits
**F8:** Each bank assembled independently to exactly 4096B by genuine DASM; concatenated ROM 8192B, exact SHA; runtime Stella disassembly shows Cartridge F8 and frames persist across F8 RAM logic/graphics transfers. Original U1-LEG1 visual-left/right A/B source rows unchanged, new `gameplay2_bank1.asm` added one WSYNC in overscan and stopped a consumed orb from automatically respawning 90 frames later. Player level, lives and score are retained across real stage transition.

**RAM/stack SOURCE_ONLY:** bank0 gameplay variables from `$AA..$BE`, original source `$80..$A9`; full-body collision rectangles `$C0..$EF` 48 bytes. Stack allowed `$F0..$FF` (16B). Nesting is statically small (<= about 8 bytes in scoped calls), but **actual worst SP high-water NOT measured**. No hidden expansion to >128 RIOT bytes should be claimed from this.

**NTSC:** Physical completed-frame raster count 262 in measured scenes. The visible kernel was not rewritten; worstcase branch/page-crossing could exceed 76 cycles on rare lines (old PLAY1-H source-static 77/76 risk). Actual per-instruction `GRP0/PF0/PF1/PF2/GRP1/ENABL` highwater, critical exact beam deadline, and frame-to-frame timing over every hard scene are **NOT VERIFIED**. A green CI or consistent 262 does not prove those. Thus hardware renderer is still only a bounded prototype.

**Preserved unfulfilled canon:** two independent simultaneous knights + Ranger renderer **OPEN**; sequential only, no Ranger-specific sprite or arrow; halo visual follows Y, not X, no unauthorized attempt to fix it; only two provisional obstacle maps, no eight production maps; no approved U1 or graphics modifications; no physical HUD. GRAPHICS II A_Glanta and K1_VISIR were intentionally deferred rather than risk the working 262-line gameplay kernel.

## Top remaining playable problems for MAIN IV
1. Full three-simultaneous-enemy physical renderer (no permanent sequential concession).
2. X/Y-following visual 360-degree halo (no recycled double-PF2 experiment).
3. Original-hardware beamdeadline 76-cycle path and real stack highwater (262 frames alone do not qualify).
4. Eight authentic arena layouts, full-size L3 collision/gliding breadth, actual Ranger arrow and knight sword poses.
5. Readable HUD and polished audio/visuals, repeated-endpoint 16-visit regression, full hit/respawn integration.

**Delivery ends GAMEPLAY-2 here.** No merge to main, new mapper, independent Verification, N8/N9 or follow-up implementation authorized. MAIN IV to review this actual frozen F8 ROM and decide next bounded step.
