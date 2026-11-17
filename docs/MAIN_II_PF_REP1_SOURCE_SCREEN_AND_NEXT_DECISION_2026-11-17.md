# THE SKRAUN — MAIN II / PF-REP1: frozen R3 source-mask and colour feasibility screen
**2026-11-17 | ONE bounded SOURCE-ONLY research deliverable | NO new 6507 ROM, NO Stella or Verification | PF-REP1 issue #25 remains OPEN for full scheduling proof**

## Executive decision
**Negative for DIRECT use of Hugg's simple single-PF-register-per-two-scanlines model with the unchanged R3 halo/obstacle representations.** Positive on a **real need for selective writes**, since the existing R3 engine redundantly writes six PF registers per visible scanline. **Neither a general multi-stream kernel nor a different physical colour ownership is disproven.**

**User goals preserved:** original user-approved U1-LEG1 8×12 A/B with correct semantically swapped facing, same graphic at all three sizes, responsive easily maneuverable L3, eight open arenas/four worlds, two sword knights plus fleeing green archer, gold 360° halo passing solids, real obstacles stopping player/sword/arrow, orb/HUD/lives, minimal disturbing flicker. No unapproved reduction of gameplay or artwork.

## Sources read before implementation selection
1. User-attached **2026-11-17 RESEARCH handoff v1** `SKRAUN_RESEARCH_AVHANDLING_v1(1).md` (194 lines), plus actual **30-row** `30_TRICK_TEKNISK_MATRIS(1).csv`.
2. Existing Skraun R1 [all-30 renderer audit](R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md), [all-30 player-identity audit](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md), [decision 01-60 plus later gameplay rule](DESIGN_DECISIONS_01-60_2026-11-16.md), [visual authority](SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [actual project status](PROJECT_STATUS_2026-11-16.md), already authorized [COL1](../handoff/MAIN_II_TO_ROM_DEV_P01_COL1_ONE_ARENA_COLLISION_DIAGNOSTIC_AUTHORIZED_2026-11-16.md).
3. Primary Steven Hugg [Versatile Playfield Kernel (11 Oct 2025)](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html) and [Three-Stream (13 Oct 2025)](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html), plus Stella TIA PF register-order reference and exact [R3 ASM](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), source Git blob `3c9ed79078eee6a0c63100614a593f92e240b5e8`.
4. [Previous first-pass MAIN PF screen](MAIN_II_RESEARCH_HANDOFF_V1_RECEIPT_AND_PF_SOURCE_TRIAGE_2026-11-17.md), whose R3 loop direction was subsequently corrected to **88 pairs x=176,174,...2**.

**Relevance of tricks after fresh review:** #24 offline/precomputed register streams and collision tables; #14 multiple kernels; #08 two-line kernel; #07 asymmetric PF; #12 raster colours; #21 RIOT scheduling; #01/#03 sprite-sharing remain separate same-Y challenge. Hugg's 2025 delta streams are not a substitute for #24 cycle-proof. #27–30 cannot add raster cycles or a new independent PF colour mask. Hugg historical technique has already been cited in the old R1 30-trick audit; the NEW evidence here is applying an exact source-data representability screen.

## Exactly what was executed
GitHub **unmerged isolated research source branch**:
[research/pf-rep1-geometry-colour-source-20261117](https://github.com/Odourman/the-skraun/tree/research/pf-rep1-geometry-colour-source-20261117/research/pf_rep1_20261117)

Files:
- `R3_SOURCE_EXACT_MASKS.json`: connector-fetched 177-byte original `RingRowMap` and 26 original `M_halo`/`M_scenery` mask groups at all X=56,60,...104, each **five alias-resolved 19-byte PF arrays**, with originating Git blob SHA. NOT invented from images.
- `PF_REP1_REPRODUCE.py`: complete Python 3 stdlib source-only reproducer, generates `PF_REP1_RESULTS.json` on a machine with repository checkout.
- `PF_REP1_RESULTS.json`: computed source-only report, cross-checked by rereading the just-written GitHub source records; 13/13 original R3 X positions. The results derive directly from the source mask bytes in the GitHub connector, and core invariants were asserted when authoring.
- `README.md`: reproduction, scope and non-production STOP.

**Now actually reproduced:** GitHub Actions [run 44053841359](https://github.com/Odourman/the-skraun/actions/runs/44053841359) executed the actual published Python 3 script, reported PASS on all 13 X positions and cross-compared **seven per-X metric families** against the independently authored JS/source results; the existing repository's ordinary CI [run 44053841435](https://github.com/Odourman/the-skraun/actions/runs/44053841435) also succeeded. MAIN downloaded the real GitHub Actions ZIP, validated archive CRC and all **four included SHA256SUMS**, extracted it and **reran Python locally, PASS**. The actual five-file [Google Drive ZIP](https://drive.google.com/file/d/1AvRZt2oy496uWSYDhJubmepXOqm-SO5X/view) was uploaded, re-downloaded, and SHA256/size independently checked: **7603 bytes, SHA256 `d1c409ece3254833e6199c665bb8a8e2ca3d43a77d7cc222dc310f7f69a8da99`**, identical to GitHub artifact ZIP. The ZIP includes the real source snapshot, reproducible Python tool, runtime-generated JSON results, README and actual Actions run metadata/hash evidence. Still **NO real 6507 cycle measurements, DASM build, ROM or Stella screenshots**. Direct pixel decoding uses the **idealized left-PF/right-PF physical half** and documented PF0 D4..D7, PF1 D7..D0, PF2 D0..D7 bit order. Without tracing the exact GRP/PF write cycle timestamps and beam timing, real on-screen pixel-perfect fidelity is not proved.

## 1. Static geometry representability (R3 HALO source-only)
There are **88 actual two-scanline groups** per original R3 176-raster-line arena loop. Its original six writes per physical line give nominal **1056 PF register stores** per frame across that diagnostic arena.

For each X position, compare its five stored source-field values `[L1,L2,R0,R1,R2]` to the preceding source pair:
- **Every one of the 13 X positions** contains **6–12 pairs** where **two or three source-field values need to change together**.
- Source pairs are often constant vertically, but **left/right differences within the SAME physical scanline** remain a separate register ownership issue, not solved by a vertical delta stream.
- In a naive **idealized register-state transition** where the kernel may write only PF register values that differ, and left/right PF half phases count separately, there are **248–288 theoretical PF zero-page store events** per 176 scanlines, versus the old routine's fixed 1056. **This is NOT a faster usable implementation**: it ignores table lookup, conditional branches, context, P0/P1, vertical deadlines, scanline colour changes and hardware placement restrictions. Such a strategy could be slower or infeasible on critical lines even while storing fewer values.

| R3 X | Two-line source bursts (>1 changed field) | Idealized minimum PF register store events |
|---:|---:|---:|
| 56 | 8 | 272 |
| 60 | 6 | 256 |
| 64 | 6 | 248 |
| 68 | 8 | 264 |
| 72 | 12 | 288 |
| 76 | 12 | 288 |
| 80 | 12 | 288 |
| 84 | 12 | 288 |
| 88 | 12 | 288 |
| 92 | 12 | 280 |
| 96 | 12 | 280 |
| 100 | 12 | 280 |
| 104 | 8 | 272 |

**Formal bounded ruling:** exact *unchanged* R3 source register streams CANNOT be expressed by Hugg's simple **one update per two rasterlines** if no additional register writes or representational change are permitted. The R3 two-half asymmetric PF schedule itself is not the same problem as Hugg's single PF background stream. This test does not automatically exclude Hugg three-stream (which can borrow register writes from other streams at a price) or source-data-specific multiwrite schedules.

## 2. Independent colour ownership (halo vs scenery from original separate diagnostic modes)
The R3 `M_halo_*` and `M_scenery_*` masks are **SEPARATE MODES, not an already combined render**. The following is explicitly an ADVERSARIAL hypothetical combined-mode composition and not a previously running frame.

Using original PF0/PF1/PF2 bit order, evaluate which 4-colour-clock PF cells would light in EACH physical half:
- For EVERY original X=56..104: **16/88 two-line pairs** contain at least one halo bit and at least one scenery bit on the **same raster row**, and in the **same physical half-screen** (same half, not necessarily same exact pixel).
- For SIX of the thirteen X positions (64, 68, 76, 80, 84, 88) there are pairs in which *the same four-clock pixel cell* is demanded by BOTH halo and scenery. Counts vary: X68 and X88 each have **16 such pairs**; X76 **14**; X64, X80, X84 **2**. One final pixel cannot be two colours at once; a priority/occlusion rule or alternative visible representation is needed, and the user has NOT selected any art priority.
- A hypothetical one-PF-layer `COLUPF` colour-priority merger, taking active cells in spatial order and ignoring gaps, produces a **lower bound of THREE horizontal colour transitions** on most of those mixed rows, **FOUR on some X80/X84 mixed rows**. That means multiple precisely timed `COLUPF` writes on the **same physical scanline** IN ADDITION TO PF register changes, unless a different object/fixed zone or accepted graphical compromise is used.

**IMPORTANT:** the current R3 design uses frame-alternating `COLUPF` gold `$2E` vs blue `$86`, not true simultaneous separate PF foreground colours. A bitmap OR by itself loses identity between halo and scenery. A SCORE split, a PF ball or changing PF priority alone does not grant arbitrary independently coloured PF pixel objects. The proposed colour lower-bound is conditional on the hypothetical one-layer priority choice, NOT an exhaustive TIA hardware impossibility proof across all register/colour timing architectures.

## 3. What research still must establish (PF-REP1 #25 stays OPEN)
- **Real scanline timing/deadlines:** derive per-register TIA data and update cutoff clocks for PF0/1/2 and `COLUPF`, including right-half write schedules; transform each theoretical event into a legal actual write slot.
- **RAM-live ranges, data preparation and stack:** compare R3's 112B region/state with a replacement stream; do not add two 32B lists without explicitly discarding other buffer data.
- **Alternative resource ownership:** if gold halo is PF, where are the solid obstacle pixels kept/colored? If obstacle PF, where does moving circular gold attack come from? Confirm all pieces at same Y with P0 and P1; a ball is NOT a second independent-color PF plane.
- **ROM vs Stella gate:** only when a geometrically/colour-representable design survives this source-only hard screen, commission a separately authorized tiny genuine DASM/Stella proof, then independent Verification later. Current P01-COL1 already authorized under [#24](https://github.com/Odourman/the-skraun/issues/24) remains separate and not duplicated.

## 4. MAIN decision
**Accepted** as a reproducible, meaningful SOURCE-ONLY frozen-R3 mask screen and exact original data archive. **Rejected** Hugg simple single-register direct drop-in. **No GO** for complete three-stream, specialized multiwrite, colour co-display or same-Y three enemies yet. Research must now tackle the more fundamental resource/colour conflict before MAIN invests in another full-scene ROM architecture. Keep [PF-REP1 #25](https://github.com/Odourman/the-skraun/issues/25) OPEN for true timing/deadline and alternative-architecture decision. No P01-COL1 rewrite, R4/B3c, art change, map canon promotion, kernel cutover, main code merge or independent VERIFICATION authorized by this source-only study.
