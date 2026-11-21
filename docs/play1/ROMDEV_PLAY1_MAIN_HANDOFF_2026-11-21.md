# THE SKRAUN – ROM DEVELOPMENT II → MAIN III: PLAY1 first playable one-arena 4KiB NTSC
**2026-11-21 | DEVELOPER_OBSERVED_PARTIAL | no main merge | no independent Verification**

## 0. Exact binding authorization and disposition
- [MAIN III → ROM DEVELOPMENT II PLAY1 order](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_PLAY1_SINGLE_ARENA_GAMEPLAY_ROM_AUTHORIZED_2026-11-21.md), [issue #34](https://github.com/Odourman/the-skraun/issues/34).
- [Draft PR #35](https://github.com/Odourman/the-skraun/pull/35) on the isolated branch `experiment/play1-single-arena-orb-halo-20261121`. **Base** exact frozen COL1 source/commit `90f89441b41a2e82408581b81d3743b1423e5cdb` (original 4096-byte ROM SHA256 `f36217f9ae96a1e927795ca639b9d6b6cca68ad3e8e4f296afadcdb52d6a6ad2`). Do not merge PR#27/#32 or this PR to main.
- **Technical status: `PLAY1_DEVELOPER_OBSERVED_PARTIAL`.** Genuine DASM and Stella 6.7.1 demonstrate **playable movement, real BL-orb L1→L2→L3, FIRE attack, physically visible level-dependent extra gold PF ring, stationary R3 P1 dummy hit/disappear, movement under FIRE**. However the current PF2 visual ring is centered **at fixed arena x80,y112**; it **does not follow player's X/Y**. The logical attack does follow. This violates the full authorized dynamic halo visual and prohibits claiming a complete PLAY1 PASS. This is a bounded, playable prototype and precise first remaining technical blocker, not full-game approval.
- Immutable user-approved U1-LEG1 source art, original eight-direction joystick, physical L1 8×12, L2 16×24, L3 32×36 sizes (Stella horizontally 2x), existing four-synthetic-solid K0 arena full-body obstacle checks retained. No new sprite art, enemy AI, mapper, extra enemy or final world maps. R3/F2b negative and N6-C remain separate.

## 1. Real machine-built binary
```sh
dasm experiments/play1_single_arena.asm -f3 -oexperiments/play1_single_arena.bin -lexperiments/play1_single_arena.lst -sexperiments/play1_single_arena.sym
test "$(stat -c %s experiments/play1_single_arena.bin)" -eq 4096
sha256sum -c experiments/play1_SHA256SUMS.txt
```
- **Actual ROM standard NTSC 4K, 4096 bytes**, SHA256 `cbc296309d60a35debb7bd6980ea5f61db5101bff48c4397f4c5569a8d33aedd`.
- **Exact gameplay assembler** SHA256 `69898159cd4261a7f77365ef7e21da1bb30194770762f4f7292c9f52b542f606`.
- Genuine DASM built repeatedly on Ubuntu-24.04 GitHub Actions with actual Stella emulation (not Python source simulation). Original `.asm`, exact binary `.bin`, listing `.lst`, symbols `.sym`, build-log and manifest are frozen on the PLAY1 experimental branch (freeze workflow stores binaries).
- **Real Stella 6.7.1** `NTSC*, Bankswitch Type:4K*`, not fake screenshot.

## 2. Seven authentic Stella gameplay scenes (NO RAM joystick shortcuts)
[Real last 7-scene source-exact Action](https://github.com/Odourman/the-skraun/actions/runs/44918066283): script executes `joy0Right #0`, `joy0Down #0`, `joy0Fire #0` in Stella Debugger and captures actual raw GUI at 1400×1000; `ACTUAL_STELLA_TIA.png` crops exact genuine 320×228 source pixels.

| Scenario | P0 actual 2× GUI bbox (left,top,right,bottom) | Authentic R3 blue P1 bright pixels | Real gold PF pixels |
|---|---|---:|---:|
| Baseline L1 | (146,114,162,126), 16×12 | 120 | 0 |
| L1 FIRE | (146,114,162,126), 16×12 | 120 | 3744 |
| Move x16/y24 + actual BL pickup L2 | (172,132,204,156), 32×24 | 120 | 0 |
| L2 FIRE | (172,132,204,156), 32×24 | 120 | 4784 |
| 90f BL respawn+actual second pickup L3 | (156,126,220,162), 64×36 | 120 | 0 |
| L3 FIRE + dummy hit | (156,126,220,162), 64×36 | **0** | 5676 |
| Hold FIRE, move P0 right8 actual game pixels | (172,126,236,162), 64×36 | 0 | 5616 |

**Strict real-pixel Python audit in the same job reports PASS for all seven observable objectives it tests**. The P1 baseline has **120/120** blue TV physical pixels corresponding to original R3 K1 eight bitmap rows repeated twice (20 additional BL/world-color pixels vanish on orb pickup). P0 physical bbox scales correct. FIRE destroys dummy from image without rotating/eliminating P0. Gold PF count grows L1→L2→L3: 3744/4784/5676 vs just 2816 recolored obstacles; **there is actually added PF geometry**, not merely scenery color toggle. Actual L3 movement shifts P0 horizontally 16 TIA GUI pixels while halo stays on. The geometry pattern remains fixed: visual tracking FAIL, so combined scope PARTIAL.

## 3. Gameplay code actually implemented / limitations
- Orb is actual TIA **BL** at game x96/y110..113, and shares `COLUPF`. Explicit collision at center x96/y112, tolerance based on level, then original `CandidateValid` verifies *prospective larger full-body clearance*; success levels 1→2→3. Orb disappears for 90 frames and safely reappears at same synthetic point. On L3 the visible orb is not consumed. SELECT old COL1 debug-growth still exists only as test-helper, **not** the real gameplay pickup claimed above. No new eight banor.
- FIRE `INPT4` active-low starts `HaloFrames=30` (~0.5s NTSC). Recovery loaded as L1 60f, L2 36f, L3 15f after active period; decrement implementation includes one recovery decrement on the expiry frame (not a rigorously timed retrigger test). Logical attack follows actual PlayerX/PlayerY, square/Chebyshev `max(abs(dx),abs(dy))` radius 18,28,40 as level increases; acts in 360 directions and through walls logically. Visual static PF2 contour contains nested bands via mask `03/1F/FF`, whole-PF B Gold `$2E` ON, world `$86` OFF, Ball inherits `COLUPF`. Exact ring shape/radii and palette are **diagnostic candidates, NOT permanent canon**.
- One stationary P1 knight test target, original R3 eight-byte `18 3C 7E DB 5A 24 66 42`, 16 rendered rows, tentative shared light-blue TIA byte `$9E`, placed around game x125,y96; logical active halo kill marks `TargetAlive=0`, `COLUP1=0`, red background flash20f. No sword/AI/other knights/Ranger, score HUD, weapon collision or true enemy-same-Y renderer. One test dummy **does not replace user-approved two concurrent knights plus one Ranger**.
- **Remaining failing gate:** the visible PF2 halo is anchored x80/y112, so with P0 moving it remains behind (in displayed screen screenshot). Current P0+PF0/PF1/PF2+P1+BL kernel is already at the conservative 76-cycle physical row budget with no modeled slack; recentering the PF2 geometry by X and Y on every frame/row in the current code is not implemented or measured as feasible. Do not assume a different complex renderer impossible generally; separate MAIN decision is required before wider redesign. **No more code iteration outside the explicit PLAY1 authorization.**

## 4. 6507/TIA, beam, ROM and RIOT – evidence classification
- **SOURCE_STATIC timing using the actual DASM instruction order/listing**, not instrumented full-frame dynamic trace: for the critical visible row worst source path after `STA WSYNC`, the source gives **73 instruction CPU cycles** incl taken branch, plus **3 cycles next WSYNC** = **76/76**. Tables `PlayPF0` $F900+X, `PlayPF1` $FA00+X, `HaloPF2Rows` $FB00+X, `DummyScan` $FC00+X and `OrbScan` $FD00+X are deliberately 193-byte page-aligned arrays for X=192..1, avoiding ABS,X page crossing. All P0 L3 sprite arrays are aligned at $F700 and within that page, avoiding (GfxPtr),Y crossing. TIA writes source-derived relative to start of physical row: `GRP0` CPU c3, `PF0` c10, `PF1` c17, `PF2` c27, `GRP1` c34, `ENABL` c44. This is **source-opcode schedule, NOT an independent per-instruction actual Stella beam trace**. Actual Stella screenshots and bitmaps show P0/one P1/BL/PF physically present, 193-entry table fix removed phantom first scanline.
- **Stella GUI physically showed `Scn Ln 261` (0-index), consistent with 262 NTSC lines** after its `frame #N` debugger command. This is developer-observed UI, not a machine-read worst-case 262-line exhaustive frame trace.
- **RIOT** original COL1 variables $80..$9B inclusive 28B, added $9C..$A5 inclusive 10B => **38B statically allocated**. Deepest call-graph two nested `JSR` = 4B return-address stack (static), so ~86B unallocated RAM budget. There is **no live debugger stack high-water trace** and no full N6 enemy-buffer ownership integration. 4KiB NTSC no mapper or extra RAM was actually built.
- Source-only rigorous corner/edge COL1 N2 worst-case audits and prior 19 genuine Stella controlled-state cases belong to **frozen COL1**, not new independent PLAY1 corner-regression PASS. In PLAY1, seven true joystick source scenarios including level3 long movement under FIRE did pass; all four obstacle contacts have NOT been separately reinstrumented after gameplay integration.

## 5. Reproducible evidence and handoff
- `PLAYTEST_PLAY1.md` has real gameplay instructions and reproducible commands.
- `scripts/play1_gameplay_capture.sh`, `tests/play1_gameplay_audit.py`, `.github/workflows/play1-gameplay.yml`: seven actual joystick+FIRE Stella scenes, strict bitmap/bbox/gold/target asserts.
- `scripts/play1_stella_capture.sh`, `tests/play1_image_audit.py`, `.github/workflows/play1-real-ntsc.yml`: 12 additional consecutive genuine TIA frame screenshots, not replacements for the seven gameplay scenes.
- All materials are in draft PR #35 and native Action artifacts. MAIN III should assess **bounded gameplay/visual PARTIAL**, then choose a separate scoped direction if dynamic PF halo is still wanted. No N8/N9, no mapper change, no main merge, no independent Verification claims.

**Final status: `PLAY1_PARTIAL_REAL_GAMEPLAY_RUNNING / VISIBLE_DYNAMIC_PF_HALO_NOT_MET / STOP_AFTER_DELIVERY`.**
