# THE SKRAUN – GRAPHICS P3-F1 | MAIN II post-research design handoff

**2026-11-16 | Single post-research P3-F1 submission | GRAPHICS-ONLY | NOT STELLA | NOT FINAL ART**

## Authority and what was actually checked

- Binding hold-release: [MAIN II P3-F1 work order](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_GRAPHICS_P3_F1_UPRIGHT_FACING_READABILITY_AUTHORIZED_2026-11-16.md), including explicit release **above** its historical research-HOLD paragraph.
- Tracking: [issue #21](https://github.com/Odourman/the-skraun/issues/21).
- [MAIN II TIA concept result](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_P3_TIA_VISUAL_MECHANISMS_CONCEPT_PROOF_AND_DECISION_2026-11-16.md): M0 contour, NUSIZ head and dual-gray color-band visual proof all returned NO meaningful L1 identity gain. **None included or recommended here**.
- [P3 U1 actual JSON](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json), SHA-256 `72ebc4dc58200f2761e942b5d6c21ac8e0308fba368d15d976715c850056450f`; U1 source A/B embedded unchanged.
- Privately examined the actual original user sketch: prominent broad head, two protruding ears/horns, **two large separated black eyes and wide open dark mouth**, long upward/outward expressive arms, thin neck/body and distinct legs with oversized feet. **No portion of original photo copied into ZIP or public repo.**
- [MAIN II updated visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md) and [P3 upright clarification](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md): topdown GAME; troll visually STANDING upright with readable symbolic frontal face permitted. Old P1/P2 prone model is rejected. Horizontal mirrored R/L only; vertical movement reuses facing. No ROM implementation.

## One post-release study, only TWO new 8x12 candidate families

### D1: original face/expression priority

- Original-inspired **wider full head**, two *asymmetrically placed* horn tips, two dark-eye gaps, **2×2 dark mouth opening with a solid lower jaw**. Preserves upright narrow torso, moves arms and legs in A/B and keeps two separate big feet. D1 is not a separate bitmap dimension or an extra P0 layer.
- Source shape is square-headed at the real original pixel scale. Despite a larger encoded mouth, the expression may read as a **mask, ghost, or helmet**, not the actual Skraun. The wide head takes pixel rows away from expressive arm movement. Horn asymmetry does not reliably look like a facing turn.

### D2: expressive swaying arms + body priority

- Retains the actual frozen U1 **top four facial rows exactly** (horns/eyes/face contour), carries a stable right-biased cheek/shoulder/torso contour with raised bent arms that move A/B independently from distinct stepping feet. Two directions are exact mirrors.
- Arms appear more outstretched but, at native L1, may look like an **ordinary small person/robot**, not the user's singular troll. The mouth remains a tiny U1-style opening, and the changing arms may still dominate perceived horizontal orientation.

## Objective source geometry (96 bitmap cells, never perceptual scores)

| Pair of source bitmaps | Frozen U1 | New D1 | New D2 |
|---|---:|---:|---:|
| A RIGHT vs A LEFT | 10 | 16 | 18 |
| B RIGHT vs B LEFT | 12 | 22 | 22 |
| A RIGHT vs B LEFT | 5 | 15 | 14 |
| A RIGHT vs B RIGHT (gait) | 7 | 9 | 8 |

`SOURCE_DISTANCE_AUDIT.json` and `audit_hamming.py` carry the full four-state Hamming matrices and reproducible counters. **No claimed recognition threshold.** We deliberately did not optimize for the maximum bit distance: the older pre-research D1/D2 had some larger bit distances but no proven original identity improvement. Neither mathematical metric establishes an aesthetic success.

## Level-1 image-based assessment

**NEGATIVE IDENTITY RESULT FOR BOTH CANDIDATES AT REAL L1.** D1 has the closest *coded* face traits and is the priority for user judgement, but its mouth reads as a block and its head as a rigid square. D2 has more animated body form but weak personality. I cannot assert that either is **substantially closer to the original at the unzoomed L1 screen size**. Left/right facings are geometrically more different from frozen U1, but actual humans have not been blind-tested; **visually reliable facing remains unproven**.

Mandatory review order: view `00_BLIND_L1_UNLABELED.png` at its intended TV scale, form independent impressions without reading `01_BLIND_ANSWER_KEY.md`, THEN inspect `02_L1_LABELED_IDENTICAL_SCALE.png`, `03_L1_NATIVE_160x192.png` and `04_L1_FULL_4_3_TV.png`. Grids and B/W enlargements are audit-only and cannot convert a negative true-scale result into a PASS. All previews marked **DESIGN, NOT STELLA**.

## Reproducibility and STOP

- Exacts: 8 columns ×12 rows; 2 walking A/B poses per D1 and D2; bit-reversed LEFT; raw PNG, GIF, nonexecutable `.inc` with top-/bottom-first, source validator, distance ledger, blind test, all three conceptual level scales, SHA-256 per member and fixed-order ZIP.
- No user private original distributed. No extra art concepts, hardware effects, ROM, Stella, M0, NUSIZ changes, second P sprite, color-band tricks, new format, new world, HUD, enemy or halo implementation.
- **P3-F1 is STOPPED after this single post-research submission.** Previous P3-F1 archive is frozen historical evidence, not overwritten; MAIN II should identify this *post-research* package as current design submission. No final sprite approval. Visual gate #15 remains open; ART1 bug #19 and full R3 NO-GO remain unresolved. No P3-F2, P4, v0.4, merge or independent VERIFICATION without fresh authorization.
