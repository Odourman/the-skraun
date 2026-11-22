# THE SKRAUN — ROM DEVELOPMENT III → MAIN IV
## GAMEPLAY-4: actual K1-T strike and R1 draw/release; bounded negative moving M1 arrow
**2026-11-22.** **Authority:** MAIN IV GAMEPLAY-4 explicit implementation order, Issue #45. **Status:** `GAMEPLAY4_DELIVERED / K1T_STRIKE_PASS_BOUNDED / R1_DRAW_RELEASE_PASS_BOUNDED / ARROW_FAIL_FOR_TESTED_M1_KERNEL / ROMDEV_III_STOPPED / MAIN_IV_REVIEW_REQUIRED`.
**Evidence label: DEVELOPER_OBSERVED** for genuine DASM and Stella captures; no independent Verification.

### 1. Frozen starting point and safety
- Exact parent GAMEPLAY-3 commit `07de8f907421e22b8b444200389a21c42dca330d` (draft PR #44), genuine 8192B conventional F8 ROM SHA256 `0d636327a3b7024634c6f251ea327fcbaa0dc3c5e04d602fefe543a072abc02e`. Reassembled and identical **byte-for-byte**, real DASM in [workflow #45031915618](https://github.com/Odourman/the-skraun/actions/runs/45031915618).
- Exactly one new isolated experiment branch `experiment/gameplay4-dynamic-combat-arrow-20261122` from that commit and one [DRAFT PR #46](https://github.com/Odourman/the-skraun/pull/46) against previous experiment; NOT main.
- Exact six immutable K1-T/R1 Graphics II 8x16 masks from source commit `4960d1661ad9764ce257a59053a981f46b09cff2` included in runtime compact table, no new graphics authoring, original approved Skraun U1-LEG1 untouched.
- **Best executable F8 NTSC checkpoint = `experiments/gameplay4a_f8_ntsc.bin`, exactly 8192 bytes, SHA256 `8bb19a9d58b6a4f608f1ab10adbb622b9e70d0f44b39e247c68feb3a974427bd`.** Two actual compiled banks committed with exact assembler .lst .sym .log and SHA manifest `experiments/gameplay4a_SHA256SUMS.txt`. Source SHA bank0 `fee3d2c4f957814b565a9c2f0fda5a0a7453ac2287f9a8a7fe239d57b352d07a`, bank1 `7dc6fb78f78ad67853178c02169633227c99db010819ea8670f516f389e76da8`. This real binary was committed by [successful one-shot genuine DASM freeze #45032790426](https://github.com/Odourman/the-skraun/actions/runs/45032790426). Repro instructions in `PLAYTEST_GAMEPLAY4.md`.
- The original executable GAMEPLAY-3 and current main unchanged. No mapper changes, no new same-Y three independent enemies, no X/Y halo remake.

### 2. Same-cartridge real K1-T native animation **PASS, bounded**
A gameplay joystick-only real Stella 6.7.1 sequence in the **same executable**, not standalone pose ROM and not screenshot montage, renders K1-T exact physical source pixel masks:
| Genuine gameplay phase | NTSC scan count | Native 320-wide TIA blue P1 pixels | Interpretation |
|---|---:|---:|---|
| Neutral/chase | 262 | 116 | Exact K1-T neutral |
| Raised sword warning | 262 | 134 | Exact 8x16 K1-T warning; source~24-frame warning |
| Active strike | 262 | 130 | Exact 8x16 K1-T **strike**; source 7-frame active sword window |
| Recovery | 262 | 116 | Neutral mask shown; 60-frame logical rest |
Player original frozen level1 P0 98 gray pixels in all four. Same light-blue armor mask; transparent T visor preserved; original U1-LEG1 source unchanged. Genuine screenshots, input and typed `_scanEnd` in [successful physical checkpoint run #45032475262](https://github.com/Odourman/the-skraun/actions/runs/45032475262).
Game logic in bank0 locks sword direction at warning start; source guards damage to 7-frame active state and actual direction/nearby hitbox, not body overlap during warning/recovery. **NOT VERIFIED:** hard sword obstruction with an obstacle in the current y96 training scene, all horizontal facings/hard beam x, actual hit vs non-hit paired RAM audit, per-instruction worst 76c deadlines. P1-only blade never exceeds eight source columns; no M1 sword.

### 3. Same-cartridge real R1 bow animation **PASS, bounded**
Actual forest-stage sequential Ranger slot (NOT 3 simultaneous actors) was reached via real joystick + FIRE; temporary world camouflage R1 one-color forest green was captured as pixels from the same frozen executable. The original first two quick snapshots were already in recovery, so five phase-offset tests plus independent safe-retarget snapshots were executed with no RAM or PC mutation.
- [Original five-phase draw scan #45032953257](https://github.com/Odourman/the-skraun/actions/runs/45032953257): two actual `ranger_phase4` and `ranger_phase12` 320x228 TIA crops **bit-for-bit** match mirrored R1 **draw** source mask, **118 exact green physical pixels**, at position crop x246..261, y119..134; `_scanEnd=262` in both. 8x16 native bow readable against the arena.
- [Focused five-phase post-FIRE-release #45033250389](https://github.com/Odourman/the-skraun/actions/runs/45033250389), same frozen ROM+native joystick: phase18 exact mirrored R1 **draw** 118 pixels, `_scanEnd=262`; phase21 and phase24 exact mirrored R1 **release** 110 pixels, `_scanEnd=262`; phase27 exact mirrored **release** 110 pixels but **`_scanEnd=263`** (NOT a clean 262-frame PASS); phase30 exact mirrored R1 **neutral** 106 pixels and `_scanEnd=262`. Exact source matrix rows, bit mirroring and 16 physical TV rows were compared against the committed Graphics II source arrays, not just screenshot appearance. Frozen source colors forest green `$C6`, but some prior held-FIRE snapshots produced gold PF/red temporary background: do not call those clean Ranger visual poses.
- Draw logic nominal 24 frames, release source shown 8 frames, recovery 60. These are source-defined durations with bounded real states, not a complete timing proof across all combat encounters.
- **No independent Ranger arrow is in the delivered ROM**; bow release visibly animates but does not spawn a damaging invisible projectile.

### 4. Real M1 projectile attempt **FAIL for tested NTSC renderer**
A separate genuine 8KiB F8 test variant `experiments/gameplay4_bank0.asm` + `experiments/gameplay4_bank1.asm` was assembled and actually run in Stella. Game-source design: one M1 arrow object (neither P0 nor BL orb stolen), X/Y RAM `$B8/$B9`, fixed directional DX/DY `$A3/$A4` sampled only when leaving bow, cool-down 180 NTSC frames `$9D` from release, intended offscreen/solid/P0/halo termination and level/life effect. That logic is **SOURCE_ONLY IN AN UNSAFE VARIANT**, not working combat proof.
- Actual M1 graphical scanline enable added `LDA (ArrowRowPtr),Y; STA ENAM1` to already heavy P0/PF/P1/BL per-row kernel. Physical Stella debugger observed **`_scanEnd=360` and PAL* or inconsistent stopped frame** in several real joystick scenes, even after removing 2+3 cycles elsewhere (see [actual measured negative #45032475336](https://github.com/Odourman/the-skraun/actions/runs/45032475336)). Thus this executable cannot be advertised as a working original-NTSC, moving, colliding arrow. No pixel sequence proving an actual moving arrow, no physical Skraun hit, halo intercept, wall intercept or one-arrow-max has been proven. **FAIL_FOR_TESTED_IMPLEMENTATION**, not proof of universal impossibility.
- The last safe checkpoint generator `scripts/gameplay4_make_checkpoint_a.py` explicitly removes the `jsr LaunchArrow` and M1 `ENAM1` scanline writes **before** compiling the delivered `gameplay4a_...` ROM. No invisible arrow/damage. BL orb remains the authentic separate TIA Ball. Do not present the source-only arrow routine as implemented gameplay.
- An optional P1+M1 sword was never undertaken (resource priority belongs to Ranger arrow).

### 5. Preserved real gameplay / hard technical budget
- **Genuine bounded run**: start level1 3 lives; stage1→2, real successive BL orb visits L1→L2→L3 (source sprite L3 64x36; actual gray TV pixel count **1200** in stationary pose). [Stella checkpoint #45032475262](https://github.com/Odourman/the-skraun/actions/runs/45032475262) verified `_scanEnd=262` in **all eight named snapshots** including Level2 Ranger and level3. Actual stage2 L3 desktop debugger shows `$AA=02` stage2, `$82=03` L3, `$AC=03` lives3, score `$AE:$AD=$028A=650` (450 stage1 + 2×100 stage2), no pixel composite. Gameover FIRE restarts and frame262 sampled. The 2,000-point bonus, all directional collisions and every L3 corner route were inherited source and parent developer evidence, **NOT fully re-exercised in this GAMEPLAY-4 sprint**. Original moving/contour halo still Y-only visible **PARTIAL**, not X-following.
- Original 128B RIOT RAM includes `$C0..$EF` 48B collision rectangles and stack reserve `$F0..$FF`. Safe checkpoint uses reclaimed **unused** `$A5` for held facing, `$9D` inactive unused OrbTimer, projectile registers `$A3,$A4,$B8,$B9` are zero/untriggered in delivered ROM. No stack or collision overlap added. Actual maximum nested stack pointer highwater **NOT VERIFIED**.
- Hot physical visible kernel paths optimized to remove unconditional P0-source JMP 3c and redundant underflow BCC 2+c; source-only nominal hot-line sum about 74 6507 cycles plus dynamic page-cross risk, but **no exhaustive actual per-instruction 76-cycle/beamdeadline proof** for all possible x, level3 and IF branches. Relative PF2, GRP1 and missile beam writes in hard positions NOT VERIFIED. **One actual Ranger release transition yielded 263**, so claiming unconditional 262 NTSC is false. This timing issue may appear as a single extra line under a specific overscan path and requires separate targeted stabilization decision.
- All real gameplay source/joystick inputs, screenshot captures, TIA pixel oracle and original typed Stella logs live in linked workflow artifacts, not manufactured GIFs.

### 6. PASS/PARTIAL/FAIL and blockers
| Contract | Status / scope |
|---|---|
| Genuine 8KiB F8 executable and baseline SHA reproducibility | **PASS** |
| K1-T real neutral/warning/strike/rest in one normally played ROM | **PASS BOUNDED**: 116/134/130/116 source-exact physical pixels, 262 tested |
| R1 real neutral/draw/release in one normally played ROM | **PASS BOUNDED**: 106/118/110 source-exact physical pixels; one 263-line transition |
| Single genuine visible moving arrow in safe ROM | **FAIL / NOT IMPLEMENTED**: M1 full physical test fails NTSC |
| Arrow target lock, 180-frame cooldown, walls, halo, player hit | **SOURCE_ONLY in rejected M1 variant / NOT VERIFIED physically** |
| Stage1→2, two orb visits to L3, FIRE, lives, score | **DEVELOPER_OBSERVED BOUNDED / source inherited** |
| 262 scanlines in all frames | **PARTIAL / FAIL strict**: 8/8 primary scenes 262; targeted release scene at phase27 **263** |
| Per-instruction beam deadline, worst stack highwater | **NOT VERIFIED** |
| Final 2 simultaneous knights + independent Ranger | **NOT IMPLEMENTED**, excluded by order, canonical requirement unchanged |

**Top three technical blockers:**
1. **M1 extra per-scanline load/write costs too much** in current active P0/P1/BL/PF F8 kernel: physical 360-line NTSC failure, no safe real arrow.
2. **One real 263-line frame during R1 release**, and still no complete hard-case 76-cycle / register-before-beam certification; even usable 262-based A ROM remains a bounded developer checkpoint, not hardware release.
3. **Projectile collision/trajectory across solids, halo and L3 plus true RAM/stack high-water** cannot be certified until a real physically timed projectile can coexist with full player/BL/enemy scene. Mandatory two independently visible knights + Ranger remains a separate known unresolved renderer problem, NOT attempted anew here.

**Smallest meaningful separate MAIN IV choice:** Preserve and playtest the real native combat checkpoint now; authorize a *separate* narrowly scoped physical M1 arrow raster timing/resource feasibility experiment only if the goal is a visible arrow. No permanent deletion of 2 knights, Ranger, halo range, BL orb or original joystick allowed.

### 7. Stop
`GAMEPLAY4_DELIVERED / ROMDEV_III_STOPPED / MAIN_IV_REVIEW_REQUIRED`. No main merge, no later mapper, new X/Y halo, new three-enemy renderer, N8/N9, additional graphics production or automatic independent Verification triggered. MAIN IV reviews this one DRAFT PR and accepts/rejects separately.
