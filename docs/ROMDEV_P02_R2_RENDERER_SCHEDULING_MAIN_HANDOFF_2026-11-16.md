# THE SKRAUN — P02-R2: TWO-LINE RENDERER & SPRITE SCHEDULING, CONSOLIDATED HANDOFF TO MAIN
**Date:** 2026-11-16. **Role:** ROM DEVELOPMENT, developer self-test only. **Independent VERIFICATION: NONE.**  
**Binding scope:** [MAIN_TO_ROM_DEV_P02_R2_RENDERER_SCHEDULING_AUTHORIZED_2026-11-16.md](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R2_RENDERER_SCHEDULING_AUTHORIZED_2026-11-16.md), read on main with blob SHA \`23d7e4b48c95a1147bc00a1def1662fd88cdf9b4\`.  
**Advisory research:** [MAIN audit of 30 classic Atari tricks](https://github.com/Odourman/the-skraun/blob/main/docs/R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md), read from main, blob SHA \`2ae6811a52e245b0ff88f420c53e1fb2a2639b0e\`. Specific hypotheses: #08 two-line, #14 multikernel/HUD, #24 ROM data and schedule, #02 and #15 same-Y P1 copies. VDEL #09 evaluated as optional later, not falsely credited as tested. NO Steven Hugg source code copied or production license assumed. R1 experiments are comparative baseline, not re-presented as new R2 breakthroughs.

## 1. MAIN DECISION IN ONE PARAGRAPH
**R2 is technically complete as a bounded feasibility study, but the full simultaneous same-scanline design remains BLOCKED in these tested kernels.** A genuine two-physical-line PF routine retains correctly oriented P0 and moving level-2 ring with synthetic scenery, while improving worst-row calculated CPU from the P1-inclusive one-line reference **71 to 68 cycles / 76**. A separate multi-kernel 16-scanline dummy HUD works. A successful, much tighter R2 experiment used **P1 NUSIZ1=$04 plus mid-scanline GRP1 rewriting** to display **TWO different enemy-like 8-bit bitmaps on the same Y band** together with P0, PF halo and fixed obstacles in true Stella; but the X positions are rigidly separated by **64 TIA color-clocks**, one bitmap is a recolored P0 test silhouette, and the pair takes **76/76** cycles on the worst rasterline. It does NOT prove three freely placed opponents, arrow, orb and HUD at overlapping Y. An alternate gold/blue per-scanline interlace shows three independently colored obstacle *rows* but reduces gold halo vertical row duty/pixels to **50%**, gives a striped/broken ring, and still uses **74/76**. Neither is authorized as a production renderer. MAIN should commission a *separately bounded* alternative render/sprite scheduling investigation or identify a higher-level cartridge/hardware/design decision; ROM DEVELOPMENT does NOT initiate R3, B3c, bank-format cutover or design changes.

## 2. FIVE REAL NTSC 4K ROMS / EXACT SOURCE & SHA-256
All five ROMs compiled with DASM (no bank switching, 4096 bytes each), with matching source, .lst, .sym and SHA256SUMS in final GitHub Actions/Google Drive evidence:

| Diagnostic | Exact source (branch relative) | ROM SHA-256 |
|---|---|---|
| R1 one-line+P1, comparison only | experiments/romdev_r1_p1_stress.asm | \`6c0bf9dca066a0777d6e6ef2b63bfe7ae54fe7025749a5cd40693ad02d6c92e9\` |
| R2 2-line+P1 | experiments/romdev_r2_two_line_p1.asm | \`2345a2c25665c316c6fc5525cb217040e09be115f872c329781e405b1d4a92e1\` |
| R2 2-line P1 double-copy / different GRP bitmaps | experiments/romdev_r2_two_line_dualcopy.asm | \`e741a8f37c3d756ae0d1d76d88567e44913ea7ee2d0a1862195014eb8170fee3\` |
| R2 separate 16-line HUD kernel | experiments/romdev_r2_multikernel_hud.asm | \`c4ec8a823403998b3fb5d97f0346c5b5c7bfe1bc729f8b1e9ec46f119fa3a7c6\` |
| R2 gold/blue PF-row interlace, CORRECTED | experiments/romdev_r2_two_line_interlace.asm | \`6d2e05215b4137032d2372de92d94d8251588b08dd56f3ec15549eef18367a72\` |

Build command per file: \`dasm <asm> -f3 -o<ROM.bin> -l<listing.lst> -s<symbols.sym>\`. Result artifact contains the exact sources and ROM binaries, all five Stella screenshots at x56/x80/x104 and reversal. **The ROMs were unchanged after the final source/test compile run**; subsequent updates to tests/research do not assert a different binary. This is experimental source, not game integration.

**Frozen successful final main engineering self-test:** [GitHub Actions #43912037744](https://github.com/Odourman/the-skraun/actions/runs/43912037744), includes **all five 4K ROMs, 20 ORIGINAL unmodified Stella 6.7.1 PNG game frames, 6507 cycle CSV, exact source/symbol/listings, original SHA-256 and explicit hypothetical level3 edge/ROM stress CSV**. Extra direct Stella debugger: [#43911806707](https://github.com/Odourman/the-skraun/actions/runs/43911806707): **four R2 variants × four joystick center/reversal states = 16 real 262-line frame measurements**, center Mode [6,12,0,6]. Those are actual debugger readings, not cycle-trace measurements. Both final runs completed SUCCESS.

## 3. R2-A: ONE-LINE VS ACTUAL TWO-LINE RASTER
New two-line kernel \`R2Pair\` has **two separate visible WSYNC scanlines per pair**, with 192 physical visible scanlines total, and 2-frame SWCHA horizontal control retained from R1. On physical line A it loads \`RingRowMap,x\`; on line B it keeps Y and repeats the adjacent PF mask row. It continues to write left/right PF registers within **both physical scanlines** and updates P0/P1 graphics separately on both. This is NOT an imaginary 152-cycle single line and not a pre-rendered framebuffer. TIA deadlines still apply on **each** of the two lines.

**STATIC SYMBOL-ANCHORED accounting** uses actual assembled \`.sym\`, pointer addresses, all actual index page crossings and branch/WSYNC paths for 13 centers × 192 physical lines per source; \`tests/romdev_r2_static.py\` produces \`R2_ALL_ASSEMBLED_RASTER_PATHS.csv\` and \`R2_STATIC_SUMMARY.csv\`.

| Actually assembled kernel | Physical A worst | Physical B worst | Worst /76 | Margin | Right PF0 latest | Right PF1 latest |
|---|---:|---:|---:|---:|---:|---:|
| R1 one-line + P1 reference | 71 | — | 71 | 5 | 42 | 50 |
| R2 PF two-line + one P1 | **68** | **67** | **68** | **8** | 42 | 50 |
| R2 dual different P1 images | **76** | **75** | **76** | **0** | 42 | 50 |
| R2 HUD region / PF arena | arena same one-line | — | **64** | 12 | 42 | 51 |
| R2 interlace A ring+scene/B blue scene-only | **73** | **74** | **74** | **2** | A 42 | A50/B after handoff |

A gray upright P0 pixelmask stays **32×24 PNG pixels / 24 independent scanline rows**, not two-line-squashed. Its actual pixel set matches the one-line reference in all tested x56/x80/x104/reversal screenshots. Gold PF ring + obstacle output differs from the baseline by **160 colored image pixels** at each compared center because adjacent PF rows are reused: measured gold-mask IoU **0.907–0.915**, so NOT pixel-identical. Ring outer contour still bounds within the same ~80×64 PNG region on each sampled center; no test authorizes accepting any final art. Synthetic obstacles are three fixed columns on rows overlapping the halo, and are **not** a collision representation.

All x56, x80 and x104 centers are real joystick-driven positions from SWCHA, with a reversal screenshot; center grid remains a **diagnostic** range, not a player screen-edge rule. R1's genuine <=2-NTSC-frame first response has not been weakened; R2 debugger Mode [6,12,0,6] after physically injected held direction is direct evidence for all four tested modes but **not** a new full latency-distribution study. No vertical movement/8-way final control implemented.

## 4. R2-C: TWO DIFFERENT P1 BITMAPS ON SAME Y — REAL TECHNIQUE, NONVIABLE COMPLETE ENEMY SYSTEM
In \`romdev_r2_two_line_dualcopy.asm\`, \`NUSIZ1=$04\` generates **two P1 copies with hardware 64-color-clock spacing**. The first uses the original P0 diagnostic \`Troll2\` bytes **recolored green** as a placeholder enemy-like bitmap, preloaded from the previous scanline (1 physical line vertical delay). The second uses a new independent **193-byte ROM-resident \`EnemyArcher\` bitmap**. It is independently shaped, not a redraw of the same graphic or image compositing.

Time-critical direct assembled-symbol schedule: the later Archer \`STA GRP1\` occurs at most **cycle 58**, before beam arrival at its x120 copy (~cycle 62.7). The following Knight/Troll2 \`GRP1\` preload occurs by **cycle 71** for the next scanline, after the second copy is scanned (x128 end, ~cycle 65.3). Actual Stella PNG tests detect **two distinct nonempty green P1 silhouettes on common Y band** for center x56/80/104 and reversed direction. At x80 green first bitmap **220 screenshot pixels**, second **168**; at x56 the first is partially hidden under P0, leaving **56**, while the second remains visible. This is expected actor priority/occlusion and must not be confused with its disappearance.

**Hard constraint**: second actor cannot choose arbitrary X or Y independently of first; both always share P1 horizontal 64-clock hardware spacing and common Y row schedule. The prototype does not implement true knight/archer art or AI, different enemy state, attack, player collision, orb, arrow or player movement in Y. All same-line cycles **76/76 at worst**: even an additional minimum different \`LDA abs,X / STA GRP1\` costs at least ~7–8 cycles (>=83/76), before considering that three independent copies require different NUSIZ spacing and write windows. A minimum \`LDA #enable; STA ENAM0\` for an arrow requires 5 additional cycles (>76). Ball/orb, M1, third actor, score and collision add still more. **PASS** on two diagnostic sprites with fixed positions, **BLOCKED** for real game actor freedom and complete overlapping combat.

## 5. R2-B: MULTIREGION HUD AND VISUAL DIFFERENTIATION
**Multikernel**: test adds a real **16-physical-scanline** blue-violet placeholder status bar with separated indicator groups in the top previously blank region (PNG y15..30), preserving P0's center/y and one-line arena below. It is not a score implementation, not a numeric/lives animation, and it DOES NOT create CPU cycles on overlapping ring/actor rows. Arena worst **64/76** (P0+PF only; P1 is not used in this variant), HUD band worst **28/76** in the STATIC ledger. True Stella shows ~**1,984 nonblack pixels** in the status band; P0 stays at PNG y99..122 (unchanged), and ring and fixed obstacles remain visible. This is a practical *regional separation* technique, not proof for a full HUD.

**Interlace**: alternate two physical raster lines in each frame:
- A: gold combined halo + scene PF mask (same color within that line).
- B: separate scene-only **blue fixed obstacle stencil**, with three explicitly timed register assignments.
- Both lines still draw upright P0 and one P1 bitmap. It is not alternating-frame flicker; it is **1-pixel horizontal striping / 50% row duty**. This is a visual quality tradeoff, not approved ring art or true two independent per-pixel layers.

**Important FAILED prototype and repair:** Initial interlace ROM SHA \`b57e813bd555f04e0dbc1cbfd0395400e93fa16cf2be07b48b006702933947b7\` missed the third blue obstacle and produced spurious right-side PF2 ghost at PNG x272–279. The first attempt is **REJECTED** and is reproducible from preceding CI artifacts. Corrected assembly inserted four timed \`NOP\`s before right-side PF1 and an explicit PF2 zero write **after** the left x56 obstacle had been scanned but **before** right PF2 pixels. This changed the ROM SHA to \`6d2e05215b4137032d2372de92d94d8251588b08dd56f3ec15549eef18367a72\` and its B-line worst cost to **74/76**. New hard-fail image regression proves all **three** blue obstacle columns at original PNG x112,176,216 and **no blue or gold pixels at the former x272 ghost**. At center x80, each blue column contributes 112 actual pixels (obscuration can reduce counts at other P0 X positions). Halo gold pixels fall **exactly from 1792 to 896** at center x80, similarly exactly 50% at other tested centers. The effect is visible, distinctive and striped, and *does not satisfy the full simultaneous same-scanline independent-color-layer specification*. The 2-cycle remaining margin with P1 also cannot fit additional enemies. Report this as a limited visual fallback only, with serious readability/future-art cost, NOT production PASS.

## 6. R2-C LEVEL3 / OBJECT ALLOCATION / MEMORY & ROM BOUNDS
**Mandatory level3 edge/reach research only**, \`tests/romdev_r2_level3_bounds.py\` and corresponding CSV are included in the final green artifact. This is NOT B3c. Level3 P0 source design is 32 TIA color-clocks wide and ~36 physical rows, while R2's current level2 ring is ~40 clocks×64 scanlines; by design, level3 ring must have **larger outer radius and thicker effect**. For a clearly labeled **HYPOTHETICAL NONBINDING stress proxy**, use level3 halo 48 color-clocks wide ×72 scanlines, 4-clock thickness; no such ring was implemented or approved. All 13 R2 diagnostic centers 56..104 fit the screen geometry at this proxy, but center x104 touches TIA x128, requiring **right PF2**, currently forced zero by R1/R2 4-table kernels. More distant real player X could cross screen edges, which must be rendered/clipped without imposing new movement rules. More PF groups imply extra writes and new bank/data architecture work; **not tested**.

**Static ROM data bounds** if compact 33-byte level2 PF row maps grow to ~37-byte level3 row maps:
- L2 13 X positions ×4 PF tables ×33 = **1716 bytes** (without scenery dedup)
- level3 proxy 13×4×37 = **1924 bytes** (**+208**) before scenery
- level3 if all 6 PF groups are needed 13×6×37 = **2886 bytes** (vs L2 **+1170**)
- eight independently duplicated scene maps: **15,392 or 23,088 bytes** (4/6 PF table proxy), before P0/P1 art, code, scripts, HUD or audio; data compression/alias reuse between unrelated layouts unproven
- two-line, dual-copy and interlace each preserve **10 bytes** RIOT RAM \`$80..$89\`, **118 of 128 bytes nominally free** in this isolated diagnostic. Enemy gameplay state, collision truth, input buffering, frame scheduler, score/HUD and dynamic obstacle geometry **not included**.
- each compiled ROM is **4096 bytes** even when much data/ORG-holes are unoccupied; 4K feasibility for full game is NOT demonstrated.
- R2 extra sprite art / blue-row table consume **193 ROM bytes** in respective isolated versions, but no per-scene true collision record. Obstacles, arrows and attacks must obey Decisions 33–37 with collision geometry independent of PF pixels, especially magic passing through obstacles.

**Object slot truth:** TIA P0=Skraun; P1=at most one independent player bitmap at a time and NUSIZ duplicates at prescribed fixed spacings. M0/M1 are narrow missile graphics tied to player color; BL is tied to PF color. Three independent same-Y knights/archer have no guaranteed arbitrary X slots; fixed-distance P1 copies are not a production AI allocation. P1 can be time-multiplexed across **different Y bands** in a future scheduler, but unrestricted moving foes can line up vertically, so this does **not** prove the worst case. A per-row GRP swap, VDEL latency or NUSIZ mode cannot silently invent a third freely positionable player. Narrow missiles/ball can support arrow/orb tests later, but their CPU/collision/priority costs have not been integrated. HUD separated above arena does not free arena cycles.

## 7. TEST GATES
| Gate | Result | Proven boundary |
|---|---|---|
| R2-A actual two-line visible kernel, real ROM and NTSC Stella | **PASS** | 68 A /67 B worst, P0 physical 24 rows intact, ring IoU >0.907 at four snapshots; HUD/enemies not full |
| Three diagnostic halo centers x56/80/104 and joystick reversal | **PASS** | Genuine Stella PNG and direct debugger Mode [6,12,0,6], no B3c Y motion |
| Two distinguishable P1 bitmaps sharing same-Y arena | **PASS (limited)** | Actual different Stella pixel masks, fixed 64-clock X spacing, 76/76 and one-row preload, cannot meet free-positioning mechanic |
| Real 16-row synthetic HUD region | **PASS (limited)** | Visible differentiated status stripe, 64/76 arena without P1, not actual scoring engine |
| Interlace after NOP/PF2 fix: three distinct blue scene columns | **PASS (limited)** | Actual Stella all three and no ghost; ring gold exactly 50%, striped; not independent same-pixel/two-layer renderer |
| Readable FULL gold halo plus independently colored visible obstacles **on same physical scanline** | **FAIL** in tested architectures | Single PF color/layer, interlace only adjacent rows |
| At least P0 + three free-X opponents + arrow + orb + HUD in worst same-Y band with fixed rules | **BLOCKED/FAIL in these kernels** | 76/76 already with two fixed-spaced sprites; no third graphics or projectile cycles |
| Level3 actual larger/thicker ring, all 8 scenes, diagonal/Y movement, FIRE, AI, collision, PAL, physical console | **NOT TESTED / not authorized** | Only explicit geometric/ROM bounded research |
| B3c or later scope, production mapper/merge | **NOT STARTED** | Explicit authorization boundary |
| Independent VERIFICATION | **NONE** | Per MAIN |

## 8. FAILED TRIALS AND CI HARNESS ISSUES
Genuine technical failure: the first blue/gold interlace attempt had a missed third column and an extra x136 TIA PF2 stripe; fixed and retested with fail-closed color-column and ghost assertions. Rejected ROM and earlier action logs retained as evidence; not counted as final PASS. Development test-only failures: CI initially had missing Python files from source-creation order, wrong screenshot dimensions assumption (Stella outputs 320×228 in this runtime), a shell variable quoting mistake in debugger session save, and a HUD-band y-coordinate threshold based on an incorrect crop hypothesis. These were corrected. They were **not** Atari hardware failures and their early red runs are not used for proof. Only final green actual-image + debugger runs are used for acceptance. No test has been described as independent VERIFICATION.

## 9. EXACT EVIDENCE, REPRODUCIBILITY AND NEXT MAIN GATE
- **Authoritative final R2 ROMs/SHA, 20 original game PNG captures, 13-center×raster×phase CSVs, level3 bound CSV, source, .sym, .lst and corrected blue-halo hard-fail tests:** https://github.com/Odourman/the-skraun/actions/runs/43912037744
- **Direct physical original-compatible Stella 6.7.1 NTSC Debugger test (4 ROMs×4 directional positions), real _scanEnd=262:** https://github.com/Odourman/the-skraun/actions/runs/43911806707
- **Google Drive original evidence folder:** https://drive.google.com/drive/folders/16SutItHKN8sm64i387X1ScbR0sVCh19L
- **Final 5-ROM/20-Stella/level3 bounds artifact copy on Drive:** https://drive.google.com/file/d/1hUBOgEhqIq0kDGINCvG8TnDRy518UJAC/view?usp=drivesdk
- **Direct Stella Debugger 16-state evidence ZIP on Drive:** https://drive.google.com/file/d/1mFOkomU_w_RZQwvRdP9JEbPDxdcsTIpZ/view?usp=drivesdk
- **Corrected genuine Stella comparison of all five renderers:** https://drive.google.com/file/d/1j3n1Cnr1V7WYk3X7JNv5UUXyXnYGnYGF/view?usp=drivesdk

**Recommended ranking for MAIN:**
1. **POTENTIAL, but insufficient for B3c authorization:** A line-pair scheduler combined with a separate HUD region, because real P0 identity and 262 NTSC survive with some regained per-line CPU time. Requires a **new authorization** for a genuinely scene-preserving, freely positionable three-opponent renderer and worst-row load, including level3 outer ring and object collision/priority.
2. **VISUAL FALLBACK FOR RESEARCH ONLY:** Gold/blue line interlace gives observable color distinction on adjacent lines with no frame flicker, but loses half the ring rows and has only 2 cycles margin. Do not adopt without explicit visual design approval and a separate same-Y actor solution.
3. **REJECT for production:** The 76/76 NUSIZ double-P1 trick as complete enemy renderer: two distinguishable fixed-spaced graphics proven, but no extra cycles, independent X, third enemy, arrow/orb or safe complete HUD. Plain one-color PF OR is also rejected for distinct halo/obstacle readability.
4. **NOT A CHOSEN SOLUTION:** Banker ROM, DPC/ARM, or nonstandard cartridge hardware; storage is not extra 6507 raster time, and R2 has no mandate to change physical platform.

MAIN alone decides whether to authorize a further bounded scheduler/scene-architecture test or resolve a genuine hardware/design conflict. No unilateral change to Decisions 01–60 or later gray-overhead visual direction. **No R3, no B3c, no B3d, no B3e, no main merge, no independent VERIFICATION.**

## 10. Final packaged delivery, hashes and status
Final distribution [GitHub Actions #43913077850](https://github.com/Odourman/the-skraun/actions/runs/43913077850) completed SUCCESS. It rehydrated the two frozen successful engineering runs (actual ROM/Stella #43912037744, direct debugger #43911806707), included this report and source, validated all five ROM SHA-256 values, and generated a relative-path manifest for the 119 contents prior to adding the manifest and check log (121 total ZIP entries). The inner ZIP was downloaded, unpacked, and its 119 manifest entries were checked again successfully.

- **Complete standalone inner package:** THE_SKRAUN_P02_R2_COMPLETE_MAIN_DELIVERY_2026-11-16.zip, SHA-256: **1f7fd26f3009d70b83813544092504f03c8ebc9a89cbe5b80d9d60a9864eca80**.
- **Package includes:** five exact 4096-byte NTSC ROMs, sources/listings/symbols, twenty original Stella game PNGs, sixteen original Stella Debugger PNGs, all state/session logs, actual-symbol 6507 raster-cycle CSVs, level3 advisory limits, test scripts, complete MAIN report, a per-file SHA manifest and an internal integrity check log.
- **Google Drive package:** https://drive.google.com/file/d/1zlMpV3X09EnFG6xnF8M8pmi1dTDb3Lbo/view?usp=drivesdk. The Drive version is the **outer GitHub Actions ZIP** containing the complete inner ZIP plus its PACKAGE_SHA256.txt. Unzip the wrapper before reading the standalone complete delivery.
- **Draft PR #13:** https://github.com/Odourman/the-skraun/pull/13, targets the preceding experimental R1 branch, not main. **Not merged. No B3c, R3, AI, gameplay or independent VERIFICATION.**
