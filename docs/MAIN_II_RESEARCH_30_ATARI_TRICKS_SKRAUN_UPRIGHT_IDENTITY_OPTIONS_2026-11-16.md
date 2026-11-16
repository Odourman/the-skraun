# THE SKRAUN — MAIN II RESEARCH: 30 Atari 2600 tricks against upright Skraun identity
**Date:** 2026-11-16
**Classification:** SOURCE AUDIT + TECHNICAL RESEARCH, ADVISORY ONLY. No ROM/graphics implementation, new mapper, canon art, independent Verification or gate acceptance authorized.
**Immediate action:** P3-F1 **ON RESEARCH HOLD** following user's explicit "first inspect research and all 30 tricks" instruction. [Current binding P3-F1 handoff with HOLD](../handoff/MAIN_II_TO_GRAPHICS_P3_F1_UPRIGHT_FACING_READABILITY_AUTHORIZED_2026-11-16.md), [issue #21](https://github.com/Odourman/the-skraun/issues/21). No D1/D2 work can be launched from the old plan while HOLD is in force.

## 1. Actual sources re-read
- **Full original 30-trick index and complete 01–30 explanations**, filename `LET_ME_OUT_30_URSPRUNGLIGA_ATARI_TRICK_MAIN_2026-11-16(4).md` from the prior *Let Me Out!* research package. Its Let Me Out! test verdicts and 6-android scene are **not** Skraun test results.
- [Skraun's prior all-30 audit for P02-R1 (Google Drive)](https://docs.google.com/document/d/1gvEw6Dq6DfNUymKSBcRDmriIinkJmGKbdszwm0cNMdM/edit). That audit focuses on halo/PF/three enemies, not character identity; under it the high-value scene-renderer options are #08 two-line kernels, #14 multiple kernels, #24 precompute, #09 VDEL.
- Current [P3 source exact U1/U2](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json), [formal MAIN P3 ruling](MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md), [current visual authority](SKRAUN_VISUAL_DIRECTION_2026-11-16.md).
- Real [P01-ART1 P0-only 4K Stella report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-p01-art1-p0-stella-readout/docs/ROMDEV_P01_ART1_MAIN_II_STELLA_VISUAL_READOUT_2026-11-16.md): P0-only raster worst approx **41/76 cycles**, true 24/36 pixel-exact states at L1/L2, 12/36 L3 wrong first row, [bug #19](https://github.com/Odourman/the-skraun/issues/19). This is NOT a full-scene budget.
- [R3 actual 6507 overlap diagnostic](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm): P0 + P1 + PF scene; 89-byte P1Buf at $A0–$F8 and 7 free bytes $F9–$FF **in this particular diagnostic layout**. [Main project status](PROJECT_STATUS_2026-11-16.md) documents static worst lines with just **2–4 cycles spare**, same-Y P1 enemies ~20 Hz and PF ring/scenery color/scheduler NO-GO.
- [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) for hard TIA registers/copy/color/76 cycles and [Stella Debugger](https://stella-emu.github.io/docs/debugger.html).
- [Steven Hugg's three-stream versatile kernel (2025)](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html): worked architecture example with NUSIZ/HMOVE different head/body width, but not proven within Skraun; RAM/display-list and write deadline costs explicit.
- [AtariAge programmer discussion on detailed missile drawing (2007–2008)](https://forums.atariage.com/topic/118687-detailed-missle-sprite-drawing-trick-anyone/): **underexplored ninth-pixel trick**, documented use of unused D0 in COLUP0 color data to drive ENAM0 per row, and timing warnings.
- [48-pixel dual-player kernel](https://bumbershootsoft.wordpress.com/2018/09/24/atari-2600-a-48px-kernel/), [versatile PF kernel](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html).

## 2. User's binding visual constraint
The **GAME WORLD** is shown topdown; **SKRAUN'S OWN FIGURE IS ALWAYS UPRIGHT ON THE SCREEN** (horned head above torso, visible eyes/mouth, arms out left/right, separate legs/feet underneath), not a prone four-paw animal. Only RIGHT and exact mirrored LEFT visual variants. Up/down movement does not introduce up/down graphics. The old P1/P2 prone interpretation is superseded. The user said **"U1 är lite åt rätt håll"**: this is partial, not final, approval.

The concrete question here is: *Can ordinary 2600 TIA techniques make that distinctive upright face/body more readable at actual level-1 size without consuming indispensable P1/halo/arrow resources or exceeding cycle and 128-byte RAM limits?*

## 3. Direct findings — ranked by possible graphics benefit

### A. #17 Missile 0 / M0 as an EXTRA edge pixel — most concrete unusual sub-trick
TIA has P0 (an 8-bit row) and M0 (a separate solid strip), both using `COLUP0`; M0 can be horizontally positioned separately, enabled/disabled per raster row via `ENAM0`, and sized 1/2/4/8 clocks via `NUSIZ0` D4–D5. This can add **one independent narrow vertical-column/short-segment silhouette cue** just outside U1's existing eight bitmap columns at a fixed X, e.g. a projecting arm/ear or a facing-side distinctive contour. It **cannot** create independently shaped two eyes, two outward horns AND two arms, or a full 16-bit bitmap. M0 does not automatically mirror when REFP0 flips P0: its X offset must be deliberately updated for RIGHT/LEFT and scaled for all levels. M0 would then be unavailable for some future projectile uses; potential arrow ownership/visibility must be explicitly audited.

**Historical bit-packing trick NOT explicit in the original 30 index:** AtariAge post by vdub_bobby, 2008. `COLUP0` ignores color byte bit D0. Encode M0-on in bit D0 of each row's color byte, then after `STA COLUP0`, `ASL` shifts original D0 into bit D1 read by `ENAM0`, and `STA ENAM0` drives M0 that row. This saves a *separate* missile enable data table but **NOT free CPU**. Relative to an existing per-row color load/write, `ASL` (2 cycles) + `STA ENAM0` (3 cycles) is **5 extra cycles per update**, not including M0 positioning. If current code sets color once and has no per-row color table, a per-row indexed color load/write and enable require additional work (roughly >=12–13 cycles worst example, depending addressing, page crossings) plus ROM/RAM prep. The real crowded R3 lines have only 2–4 cycles nominal headroom; therefore **cannot simply paste M0 into R3**.

**Smallest falsifiable idea if separately authorized:** One isolated P0-only NTSC DASM/Stella proof (not yet ordered), original U1 fixed, M0 edge-pixel controls ON/OFF across exact rows and both facings/poses, all L1/L2/L3, with real raw screenshot pixel oracle, 262 line and cycle ledger. Then test M0 ownership and scheduling against the entire R3 overlap case before considering art acceptance. This is a **test suggestion, NOT an instruction**.

### B. #06 Mid-frame NUSIZ0 changes — possible bigger head proportion, no new information bits
The 2025 three-stream kernel visibly uses mid-screen `NUSIZ`/HMOVE choices to give different **physical** width to the head/body region; the example discusses a 2× head and a 3× body configuration (different player size/copy arrangement). For Skraun this suggests **head rows physically wider than torso/leg rows**, which may improve horn/eye-mouth perception and reduce "generic 8×12 robot" reading. The independent bitmap data remain **8 bits/row**: this stretches existing logical cells rather than adding more freely selectable face pixels. Head/body horizontal alignment requires positioning/HMOVE and exact scanline register transitions; look for stretching, TIA transient glitches, miscentered head and collision-size mismatch. P0's current three level widths are 8/16/32 color clocks with NUSIZ 1×/2×/4×, and **4× is already the normal maximum**: a 2×-versus-1× head strategy cannot simply be multiplied again for L3, risking decision #47's same-character-level silhouette. A physically wide head also must not look like a flattened insect.

**Recommendation:** compare a conceptual variable-width head/body shape at L1 to unchanged U1 **before** any actual ROM proof. This can be a paper/pixel-art feasibility question, but no TIA visual correctness claim until a later authorized DASM/Stella case.

### C. #12 Raster color changes — inexpensive perceptual grouping, not face detail pixels
Change `COLUP0` by coarse horizontal rows/zones, e.g. brighter horns/head and darker torso/legs with neutral gray palette, to reinforce a single standing upright character. It can be scheduled as **a few transitions** instead of a per-row color table. However **one P0 color applies to ALL lit player pixels on a given scanline**, and its dark holes remain background; this does not create a second independently colored eye/mouth inside the same P0 row. Every color change still costs cycles and must obey deadlines. Changing the already preferred neutral light-gray identity is a visual-design decision, not automatically authorized. If combined with A's D0 trick, preserve D0 coding and `COLUP0` bit constraints.

### D. #16 Reflection + #24 precomputed tables — enablers, NOT added pixels
`REFP0` flips the existing eight source bits horizontally (previous graphics/ROM self-tests saved about 24 source ROM bytes). It supports the user's exact L/R requirement without storing separate bit-reversed tables, but if an M0 extension is used the missile itself does **not** mirror with P0. Precomputed scanline streams and source table packing may remove dynamic work from high-pressure visible lines, but F6/ROM expansion does **not** yield more than 76 cycles or a third P1 sprite. A necessary step if A–C ever go beyond a stand-alone demo; do not claim kernel integration from a design mock.

### E. #14 multiple kernels, #08 two-line, #09 VDEL — MAY create scheduling room
The earlier Skraun 30-trick audit correctly ranked these for **entire renderer** feasibility. A specialized player-height kernel, region-specific register update, or two-line stream might allow a few more M0/NUSIZ writes if *the same* halo/PF/P1 overlap can be respected. It costs complexity, vertical precision, display-list RAM, branch timing and exact buffering proof. [Hugg's three-stream example](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html) itself warns display lists may cost about 32 bytes each. R3's 89-byte P1 raster buffer and 7 leftover RAM bytes are strong evidence against casually transplanting that exact example. Separate illustrative kernels are NOT a full-game PASS.

### F. #13 P0+P1 16-bit-ish composite / 48-pixel techniques — very high graphical payoff, but the wrong current resource economics
Two true player bitmaps can compose **more independent horizontal logical pixels** than one 8-bit P0; the documented 48px kernel achieves broad patterns by interleaving both players and timed GRP updates. But **P1 is required by the knights/green archer**, where R3 already fails acceptable simultaneous same-Y visibility; using P1 to complete Skraun's face consumes that object on the same Y. Time-multiplexing P1 for both face and enemy could reintroduce facial flicker or missing enemies. This is **not recommended as ordinary next step** absent a much bigger separately authorized engine architecture and a rigorously tested coexistence case.

### G. #27–30 special cartridge electronics and bank-switching — excluded
SCABS, Superchip/Supercharger, DPC/DPC+/CDF/ARM are not ordinary F6 bank-switching. More ROM/RAM/compute can support data flow and preparation but **cannot change the TIA's own 8-bit GRP0 bitmap register, 2 player generators or 76 cycles per scanline**. Changing cartridge targets is a separate high-cost hardware/compatibility/game-authority decision, not a direct artistic cure.

## 4. Complete original 30-trick applicability ledger to THIS player-identity question

| # | Original technique | Player-identity verdict |
|---:|---|---|
| 01 | Sprite Multiplexing | INDIRECT; reallocates P1 by vertical zones, same-Y enemies remain blocking |
| 02 | Mid-scanline GRP Rewriting | LOW; copies/timing, not free 16-bit P0 face |
| 03 | Venetian Blinds | POOR; harms 12-line L1 face coherence |
| 04 | Sprite Flickering | POOR; unstable eyes/mouth and original goal avoids distracting flicker |
| 05 | Dynamic Playfield Sprites | POOR; PF four-clock resolution and halo/hinder conflict |
| 06 | Mid-frame Sprite Resizing | **PROMISING EXPERIMENTAL PROPORTIONS**; NUSIZ head/body |
| 07 | Asymmetric Playfield | NO extra fine pixels for P0 face; scarce PF deadlines |
| 08 | Two-Line Kernel | INDIRECT possible cycle scheduling, vertical-quality cost |
| 09 | VDEL / Delayed Graphics | INDIRECT GRP data timing, not third player |
| 10 | HMOVE Fine Positioning | NECESSARY for M0/head recentering, not extra pixels |
| 11 | Late HMOVE | POOR/RISKY TIA artefacts, no identity benefit |
| 12 | Raster Color Changes | **PROMISING modest head/body separation** |
| 13 | 48px / Six-Digit Score Kernel | TECHNICALLY RICH, P1 conflicts enemies |
| 14 | Multiple Display Kernels | INDIRECT if future resource proof, does not solve same-Y by itself |
| 15 | NUSIZ Sprite Duplication | Fixed spacing/copies, not independent facial pixels |
| 16 | Sprite Reflection | **DIRECT L/R compliance and ROM saving**, no extra detail; M0 needs independent mirror |
| 17 | Missile and Ball Reuse | **PROMISING M0 ninth-edge-pixel**; limited geometry, shared color/resources |
| 18 | Playfield Score Mode | NO additional facial detail, color conflicts |
| 19 | Playfield Priority Switching | NO new facial pixels, only front/back overlap |
| 20 | Hardware Collision Latches | No visual identity benefit |
| 21 | RIOT Timer Scheduling | Stable sync, no more per-line cycles |
| 22 | Stack/RAM Mirroring | Marginal code/RAM packing, no visible new geometry |
| 23 | Undocumented 6502 Opcodes | Unnecessary hardware/revision risk; no more pixels |
| 24 | Precomputed Tables / Cycle-Exact Kernels | **KEY enabling path** to make selective additional writes measurable |
| 25 | Stack-Based TIA Register Tricks | Specialist timing only, high safety risk |
| 26 | Timing-Based Horizontal Scrolling | No relevance to stationary camera/game world |
| 27 | SCABS Automatic Bank Switching | Requires different special cart, no new player generator |
| 28 | Extra Cart RAM / Superchip / Supercharger | Different mapper/cart, does not enlarge GRP0 |
| 29 | DPC Display Processor Chip | Different hardware, still TIA pixel/register limits |
| 30 | DPC+ / CDF / ARM Coprocessors | Different hardware/software; still two TIA players and same output deadlines |

No cross-project negative result is transferred as a Skraun ROM test result. This is a **research categorization**, not independently verified screen behavior.

## 5. Critical original-game bottlenecks and STOP conditions
- **P3 U1** at logical 8×12 provides barely 10–12 different bits when reflected R/L; the issue is perception and original character identity, not source bitmap correctness. [P3 review](MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md). A more complex M0 composite may make a single asymmetric cue stronger, but it **cannot** magically draw two horns, eyes and mouth with independent 16-bit detail.
- **L3 ART1 glitch #19** is an unfixed ordinary-P0 rendering defect; none of these research routes fixes it automatically. P0+M0 and NUSIZ change must not hide or waiver regression.
- **R3 full-scene resource contradiction remains**: same-Y enemies about 20Hz, PF halo and scenery conflict, 2–4 spare worst-path calculated cycles, only 7 free RIOT RAM bytes in R3's specific 89B P1-buffer layout. Neither P0-only art proof nor new special-kernel article proves coexistence.
- Different sprite dimensions **8×14/8×16** are a separate non-trick **art-footprint tradeoff**: more vertical rows and height might better separate upright horns/face/arms/feet, but do NOT create more than 8 independent horizontal facial pixel positions and enlarge L3 footprint/overlap. Such changes remain **not authorized** by this research.
- No historical third-party code may be copied into the repository without checking code license/provenance.

## 6. MAIN recommendation: RESEARCH HOLD, then an explicit decision gate
**The 30 tricks contain genuine useful ideas but no verified drop-in solution.** Do **not** resume current P3-F1 as just more U1 bitmap tweaks and do **not** command ROM DEVELOPMENT to integrate extra player graphics yet.

Prioritize **one tightly bounded feasibility decision**, optionally later authorized as an isolated diagnostic:
1. Design-only comparison of three U1-based visual *mechanisms* (not an unauthorized new graphics version): unchanged 8×12 baseline vs **M0 one-edge-column** (#17), **head/body width variation** (#6), and **two P0 gray shades** (#12); test conceptual L1 actual 4:3 display first, preserve upright standing, exact L/R, original identity and two A/B poses. Do not claim Stella or final art.
2. If a mechanism visibly beats baseline at actual L1, authorize **separately** a *small P0-only genuine DASM/Stella hardware proof* with exact position, visible source-mask/auxiliary pixel equivalence, both facings, A/B, three sizes, 262 scanlines and cycle/RAM accounting, explicitly testing head/body alignment and existing L3 defect.
3. Only if that isolated proof PASSES, commission a separate **full-R3-scene stress/cycle/ownership feasibility check**. Demand P1 enemies, PF ring and obstacle, missile/arrow resource matrix, same-Y, RAM/ROM, perceptual visibility. If the worst line cannot fit 76 cycles or role resources collide, STOP; do not silently reduce game rules.
4. In parallel, MAIN/user may choose an explicit larger-source-footprint tradeoff (e.g. 8×14/8×16) or accept a stylized face and simplified silhouette; neither was authorized here.

**Current decision:** P3-F1 remains **ON HOLD** until a NEW MAIN authorization says what to test. No new developer assignment, ROM/STELLA, dimensions, source merge, visual acceptance, independent Verification or closure of [issue #15](https://github.com/Odourman/the-skraun/issues/15).
