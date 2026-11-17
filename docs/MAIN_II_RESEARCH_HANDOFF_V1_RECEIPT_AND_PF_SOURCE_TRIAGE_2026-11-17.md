# THE SKRAUN — MAIN II receipt of RESEARCH handoff v1 and preliminary PF source triage
**Date 2026-11-17 | Classification: ADVISORY RECEIPT + INDEPENDENT SOURCE-ONLY SCREEN; NOT AN ATARI ROM PASS**

## 1. What was actually received and reviewed
User supplied two directly accessible research artifacts in the current MAIN chat:
1. `SKRAUN_RESEARCH_AVHANDLING_v1(1).md` — 194 lines / about 36 KiB, heading "THE SKRAUN – RESEARCH HANDOFF v1 / Full-game architecture, 17 november 2026".
2. `30_TRICK_TEKNISK_MATRIS(1).csv` — **exactly 30 rows indexed 1 through 30** with headers Nr, Teknik, Funktion, Kontrollerade historiska/projektbelägg, Kostnad/risk, Bedömning, Minsta beslutsprov, Evidensklass.

The handoff text says a seven-file full ZIP including `KALLREGISTER.csv`, `KODSTUDIER_EXAKTA_RADER.md` and `SOKLOGG.md` was prepared; **this complete ZIP and the other five files were NOT attached to this MAIN message** and were not found through an exact-title Drive search when receiving it. Therefore MAIN has **NOT** independently verified its ZIP/manifest SHA256, original code-specific citations or international search log. All historical project claims in the report remain *RESEARCH claims* unless independently checked below. No invented ZIP/hash or artifact delivery accepted.

## 2. Independent source checks, 2026-11-17
- Real original [Steven Hugg 11-Oct-2025 Versatile PF kernel](https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html): alternating register-index / register-value table and `STA $00,X`, **ONE TIA register changed per TWO scanlines**; author estimates <=9 cycles per scanline for this PF stream under assumptions, not total renderer. Author explicitly says complex horizontal lines may need multiple PF register changes and thus cannot be represented by the simple scheme.
- Real [Hugg 13-Oct-2025 Three-Stream kernel](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html): up to **three** TIA register writes each scanline, with explicit tearing risk, sprite repositioning complexity, and two **32-byte** RAM display lists plus build-time frame preparation. It is NOT a three-independent-sprites same-Y demonstration.
- Historic [IEEE Spectrum / AtariAge "Design Case" Video Chess Venetian](https://www.atariage.com/2600/archives/design_case.html?SystemID=2600) actually documents Bob Whitehead's alternating-raster sprite technique. [Kovi Kovi developer thread](https://forums.atariage.com/topic/349506-kovi-kovi-for-atari-2600/) describes E7 special-cartridge 2 KiB RAM and a self-modifying Venetian kernel. These historical examples do not prove three small readable knights/archer sharing P1 at arbitrary overlapping X/Y under halo/PF workload.
- Actual R3 assembler inspected via [experiment branch `romdev_r3_overlap.asm`](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), Git blob `3c9ed79078eee6a0c63100614a593f92e240b5e8`. Its `R3Pair` uses **six PF register writes each physical scanline** (left PF0=0, PF1, PF2; then right PF0/PF1/PF2). The published 19-byte named arrays and 177-entry `RingRowMap` can be source analyzed, but are not a new final full-scene mask.
- [Current issue #24](https://github.com/Odourman/the-skraun/issues/24) P01-COL1 remained OPEN at receipt; open is NOT evidence of actual ROM progress. Navigation #23, Level3 ART1 defect #19 and visual gate #15 also OPEN. R3 remains full-scene NO-GO, no merger.

## 3. MAIN II first independent PF representability source screen (NEW PRELIMINARY EVIDENCE)
**Hypothesis checked:** Can the SIMPLE single-register-per-2-scanline Hugg PF scheme reproduce the exact existing **R3 halo-only** PF register-state transition streams unchanged without adding further PF writes?

**Input/algorithm:** From frozen real R3 `romdev_r3_overlap.asm`, parse all `M_halo_{L1,L2,R0,R1,R2}_{X}` `dc.b` arrays with exact aliases (`M_halo_R2_56 = M_halo_R1_56` etc.), each 19 B. Parse the 177-byte `RingRowMap` used by `R3Pair`. Follow the ACTUAL `LDX #176` / pair-loop order x=176,174,...,2 to get precisely **88 active two-scanline groups**; index 0 of the source map is not executed by this loop. For all 13 R3 diagnostic X values **56,60,...104**, sample the original five PF values at successive executed two-scanline boundaries. Initialize PF stream at all zero, compare each sampled 5-value left/right register tuple to previous tuple and count positions where **at least two distinct left/right timed PF values must change in one 2-scanline group**. This is a simple static transition *lower-bound proxy*, not a full TIA compile/simulation or final user sprite mask proof.

**Observed results:**
| X | Two-scanline groups with >1 source PF value changed | Max simultaneous source value changes |
|---:|---:|---:|
| 56 | 8 | 2 |
| 60 | 6 | 2 |
| 64 | 6 | 3 |
| 68 | 8 | 3 |
| 72 | 12 | 2 |
| 76 | 12 | 2 |
| 80 | 12 | 2 |
| 84 | 12 | 3 |
| 88 | 12 | 3 |
| 92 | 12 | 3 |
| 96 | 12 | 3 |
| 100 | 12 | 3 |
| 104 | 8 | 2 |

All **13/13** cases require >1 source PF-value change in at least 6 two-line windows. Of the 88 active paired windows per X, **70** had zero changes under this grouping, so the underlying shape is quite sparse *but has bursts of simultaneous changes*. The existing source also demands distinct LEFT and RIGHT timed PF register values in many scanlines; the simple Hugg one-register stream is not a drop-in replacement for this fixed asymmetric schedule.

**PRELIMINARY FAIL for direct, exact, unchanged one-write-per-two-line substitution into existing R3 halo schedule.** The same finding is compatible with **selective multiple writes, Hugg three-stream, staggered kernel preparation, a redrawn/rasterized approximation (which would require distinct user visual approval), or different ownership of halo/hindrance**. Do not assert a general impossibility or that worst-case full-scene is compiled. To meet a stronger proof, build a source-only representability compiler with true scanline timing/deadlines, decoded 160 horizontal PF pixels, original R3 colour data, *actual* halo+hinder mask for simultaneous scene, and different X/Y across all selected worlds. **DO NOT conflate PF geometry coverage with distinct gold/obstacle colours**: a single TIA PF colour source cannot magically become two independently coloured overlapping objects because it has fewer value updates.

## 4. MAIN II research decision
**Receive research v1 as ADVISORY, source novelty is methodological not a new Skraun ROM pass.** The Hugg algorithm was already referenced in prior Skraun R1 30-trick research; its newly valuable contribution is a falsifiable representability test. Venetian blinds moves from earlier "poor fit" to **testable but HIGH VISUAL-RISK** for P1 weapon-bearing same-Y sprites, not a preferred committed solution.

**Ranked next research action:**
1. **PF-REP1 SOURCE-ONLY:** before any new renderer ROM, test exact existing R3 halo/hinder source masks and visual requirements with a deterministic per-register/per-left-right-half representability/deadline compiler. First reject mathematically impossible PF + separate-colour cases; then check single-, multi- and three-stream PF schedules and record lower-bound update/raster-cycle and RAM/ROM costs. Include meaningful negative controls and explicit failures. Do not alter U1-LEG1 source, actual 8 map canon or graphics approval.
2. If (and only if) a plausible screen-side strategy survives, a separately authorized minimal **P1 same-Y** genuine DASM/Stella comparison with 3 distinct weapon-bearing enemies at arbitrary X, 12 frame captures and full P0/PF coexistence. Compare R3 20 Hz to Venetian 1/3-scanline and relevant selective reuse; preserve attack telegraph and fairness. Negative results acceptable.
3. Need actual source provenance audit of remaining five handoff artifacts if later supplied; don't imply they were received.
4. Keep **already authorised P01-COL1** isolated and unmodified; don't duplicate it. Do not automatically begin R4/B3c full-engine cutover or new mapper/ARM strategy.

## 5. User goals remain binding
The user's actual game is a fast top-down original Atari 2600 arcade game, with frozen user-approved light-gray upright U1-LEG1 A/B two mirrored facing variants (original source LEFT mapped to visual RIGHT), all three sizes of same art, eight roomy maps/four worlds with Level3 free movement, 2 sword knights + fleeing archer (3 enemies at same Y worst case), gold 360° halo passing solids, visible obstacles blocking body/sword/arrow, orb, score/lives and readable/fair audiovisual feedback. No silent downgrades to make a demo PASS. Research may invalidate a *technical mechanism*, but cannot change approved game or user visual canon.

**Disposition:** one source-only PF representability research gate may be started separately; no independent Verification, no real ROM implementation, no authored canonical map/graphics changes, no main production merge, no issue #15/#19/#23/#24 closure. Report and recommendation are strictly MAIN audit, not user approval or emulator proof.
