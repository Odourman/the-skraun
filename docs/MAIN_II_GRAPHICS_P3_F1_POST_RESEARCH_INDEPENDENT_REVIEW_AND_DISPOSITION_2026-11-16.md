# THE SKRAUN — MAIN II: GRAPHICS P3-F1 post-research independent receiving review
**2026-11-16 | FINAL MAIN II RECEIPT: SOURCE DELIVERY PASS, ORIGINAL IDENTITY FAIL/NO FINAL ART APPROVAL**

## 1. Authority and protected scope
User's explicit direction remains binding:
- The **GAME PLAN/CAMERA** is overhead, but **SKRAUN is drawn UPRIGHT standing**, head/horns above body, expressive lateral/upward arms, two feet below; NEVER a prone four-footed side-view body.
- Only LEFT and RIGHT visual facings, exact horizontal mirror of the eight bitmap bits per raster row; up/down movement retains one of these two facings.
- User's reaction to frozen U1: **"U1 är lite åt rätt håll"**, partial approval of the approach and **NOT** sprite acceptance.
- Original user hand-drawn image is PRIVATE. Read for this decision from Drive and local private copy; **no original photo copied into GitHub or submitted art archives**.
- Read [MAIN II's release-of-research-hold binding order](../handoff/MAIN_II_TO_GRAPHICS_P3_F1_UPRIGHT_FACING_READABILITY_AUTHORIZED_2026-11-16.md), [all-30 Atari trick research](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md), and [three TIA mechanism design comparison](MAIN_II_P3_TIA_VISUAL_MECHANISMS_CONCEPT_PROOF_AND_DECISION_2026-11-16.md). M0, NUSIZ resizing and dual-gray schemes had **negative specific visual gain**, hence none is included in this P3-F1 candidate package.

## 2. Exact independent delivery/provenance audit
**CURRENT post-research deliverable:** [Full source/preview ZIP on Google Drive](https://drive.google.com/file/d/1GjHMHqYeQRVyRiqc9dTf264qo_OEQlsq/view) `THE_SKRAUN_GRAPHICS_P3_F1_POST_RESEARCH_2026-11-16.zip`.
- Actual raw Drive ZIP **232136 bytes**, actual independently calculated **SHA-256 `33fd0729b90cc502f51668fde8268df9ba347f5e0cdebbe385388bfc27898215`** = declared hash, **PASS**.
- ZIP **40 members**, CRC **PASS**, **39/39 SHA256SUMS** entries match exact compressed-content extractions, **PASS**.
- Actually extracted package and executed `validate_package.py` separately: **PASS**. Validates 8x12, exact A/B, bit-reversed LEFT for both, 12 raw glyph images, six two-frame GIFs, still-standing frame rows, source distance matrix, exact art-only `.inc` tables, media sizes/durations, privacy exclusions and archive manifest.
- In **clean temporary directory** copied only unchanged input source/config/program files, ran `generate_previews.py`, `generate_bitmap_tables.py`, `audit_hamming.py` with Python. **All 40 resulting media/source/static files match the original archive byte-for-byte**, then independently re-ran validator PASS. Generated **22 PNG**, **six GIF**; not edited/overwritten frozen P3 baseline.
- [Actual isolated public GitHub branch](https://github.com/Odourman/the-skraun/tree/graphics/p3-f1-post-research-identity-20261116/graphics/p3_f1_post_research) compared against `main`: **13 added text/source/documentation files only**, 13 commits ahead, 0 behind at time of review; no prior ROM, gameplay or native art sources modified, no merge; historical pre-research P3-F1 branch remains separate.
- Reviewed [P3-F1 exact JSON](https://github.com/Odourman/the-skraun/blob/graphics/p3-f1-post-research-identity-20261116/graphics/p3_f1_post_research/SOURCE_8x12.json), and older [P3 U1 frozen JSON](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json). Verified preserved A/B U1 rows and exact L/R mirror. No P3 source mutation. The earlier pre-research P3-F1 package is a different frozen artifact **SHA256 `53adadae16e9698cc38a6083abc62101455ded8438e1e0d9b02d530452d47ef6`** and is NOT the current delivery.
- **All preview images are design-only (software image generator), NOT genuine Stella**, ROM, TIA precision timing, hardware or independent VERIFICATION.

## 3. Objective source-cell audit (all values out of 96)
| Pair | Frozen U1 | D1 new | D2 new |
|---|---:|---:|---:|
| A-right vs A-left | 10 | 16 | 18 |
| B-right vs B-left | 12 | 22 | 22 |
| A-right vs B-left | 5 | 15 | 14 |
| A-right vs B-right (gait) | 7 | 9 | 8 |

Exact horizontal mirror is SOURCE PASS; increased difference is a **geometric result**, not proof that humans perceive correct facing. No external human blinded reading performed by MAIN; the bundled unlabeled/answer-key panel is test material, not a recorded study.

## 4. Direct visual reading
MAIN inspected the actual [TV-format fixed-size labeled crop `02_L1_LABELED_IDENTICAL_SCALE.png`](https://drive.google.com/file/d/1GjHMHqYeQRVyRiqc9dTf264qo_OEQlsq/view) (from extracted original ZIP), full unzoomed `04_L1_FULL_4_3_TV.png`, enlarged silhouettes `06_BLACK_WHITE_SILHOUETTES.png` for anatomy only, exact row sheet `05_EXACT_SOURCE_MATRICES.png` and user's **PRIVATE ORIGINAL HAND DRAWING** (not republished).

**Original character:** extremely expressive LARGER head with two horns/ears, TWO BIG DARK EYES and a WIDE open dark mouth, slender neck/narrower trunk, **LONG thin raised arms with distinct hands/fingers**, long bent legs and oversized projecting feet. **Game camera overhead** does not cancel these visually UPRIGHT anatomical requirements.

**U1:** improved from prior P1/P2 prone errors, but at actual L1 the overall source still resembles a small biped/creature; expression and long arms almost disappear.

**D1 — Head Expression:** head/front contour is obviously wider, two head points, separated holes and a larger 2×2 mouth, but **near-square silhouette dominates**, expression looks like a MASK/HELMET. Arms too short; original's thin expressive long limbs and oversized projecting feet are not recognisable at native L1. **The current most useful *face-design reference* among new options**, not close enough for acceptance.

**D2 — Swaying Arms:** better arm motion/shoulder shape but limbs still very short relative to user's original, and its U1 upper face remains tiny. At native L1 it looks like a small GENERIC creature/person/robot. **BODY/ANIMATION comparative reference only**, not final.

Both candidate families are sprite upright (not prone) and two A/B poses actually change arm and leg cells. L/R source mirroring and physical two-direction contract are met. They do NOT yield a compelling original-specific character in actual-size L1. Source masks aren't **intrinsically impossible** at 8×12 but repeated P1/P2/P3/P3-F1 studies have given diminishing returns, so another almost-identical 8×12 pixel-tweak cycle is a weak next investment.

**Visual gates:** D1 aesthetic identity **FAIL/not accepted**, D2 **FAIL/not accepted**, left/right **UNPROVEN perceptually**, all L1 normal-size comparisons **DESIGN not Stella**. No user choice is invented or inferred.

## 5. MAIN II final disposition
1. **P3-F1 accepted as CLOSED AND COMPLETED REPRODUCIBLE GRAPHICS STUDY**, NOT successful final art. No additional D1/D2 inside P3-F1, no remake, no automatic P3-F2 or P4.
2. Freeze D1 as **preferred face study reference only**; D2 as body-motion comparative reserve; original U1 historical partial-positive reference. Freeze all historic original user source and prior experimental negatives unchanged.
3. **Issue #21 may be closed with reason COMPLETED, but only because authorized work was delivered.** This does **NOT** close [#15 visual-identity gate](https://github.com/Odourman/the-skraun/issues/15) or approve any sprite. [#19 ART1 L3 bug](https://github.com/Odourman/the-skraun/issues/19) and [#1 independent P01 gate](https://github.com/Odourman/the-skraun/issues/1) remain OPEN.
4. Maintain R3 full-scene resource feasibility **NO-GO**: 2–4 remaining worst-path CPU cycles, same-Y enemies and PF halo/scenery not independently solved; adding M0/P1, NUSIZ manipulation, wider rendered sprite or more level3 scanlines is NOT assumed safe. The older ART1 L3 first-raster-row defect remains frozen and unresolved.
5. **NEXT RECOMMENDED (NOT YET AUTHORIZED):** **a separate design/technical footprint feasibility decision**, not another free-form artwork version: compare whether a **taller 8-bit P0 single-player source** (e.g. 8×16 or 8×20 instead of 8×12) can provide enough vertical room for original long raised arms/legs/large feet and still keep the big face. Note **no added horizontal face detail**. Explicitly cost each of three scale levels including L3 expansion, halo collision footprint, proximity/overlap with enemies, raster update and per-row CPU/RAM budget, and compatibility with original design decisions. Optionally compare more than 8 horizontal independent bits only as **a separate, costed alternative requiring P1 or special rendering**; P1 is currently needed for monsters and is NOT freely available. An 8×14 tweak alone will not solve horizontal mouth/eye separation. An alternative is for user to consciously accept a stylized, less detailed troll within the native 8×12 limit. No path is pre-approved.
6. Do not authorise or perform ROM DEVELOPMENT, Stella hardware test, ART1 fix, P02-R4/B3c, alternative mapper/cart, P3-F2/P4/v0.4, actual level size change, main source merge, independent VERIFICATION or closing #15. **MAIN retains decision authority.**

**Source-of-truth:** current visual direction and design decisions with subsequent user's upright correction; study does not supersede canonical game design or the user's original drawing.
