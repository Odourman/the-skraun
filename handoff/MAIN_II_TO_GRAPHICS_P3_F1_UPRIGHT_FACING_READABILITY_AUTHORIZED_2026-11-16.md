# THE SKRAUN — MAIN II TO GRAPHICS: P3-F1 UPRIGHT FACING READABILITY PROOF

**A NEW, EXPLICIT, SINGLE BOUNDED DESIGN-ONLY AUTHORIZATION BY MAIN II — 2026-11-16.**
**Reason:** After P3 delivery MAIN II was asked to continue, without any declaration that U1 is final art. The narrow unresolved question is whether the upright standing troll actually **looks turned left versus right** while keeping the original recognisable face and animation. This is **not** P4/v0.4, P01-ART2, new ROM, an acceptance of U1, or permission to iterate indefinitely.

## 1. Binding authority & required reads
Before work, check the ACTUAL GitHub and Google Drive sources and verify access:
- The user's more recent DIRECT clarification, written into [MAIN II's reviewed visual direction](../docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [MAIN II's formal P3 review](../docs/MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md), and [decisions 01–60 with later correction note](../docs/DESIGN_DECISIONS_01-60_2026-11-16.md).
- [Private original user drawing — Drive only](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view): preserve two horns/ears, visible eyes, open mouth, outstretched arms, legs/feet. Never distribute or reproduce this private photograph in public GitHub/ZIP.
- [Actual frozen P3 U1/U2/Q1/P1-A source](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json), [P3 final author report](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/MAIN_II_P3_FINAL_REPORT.md), and [original source-derived design preview ZIP](https://drive.google.com/file/d/196UpbC1Kl400BcMj5zZ44Y48p7-WW7-W/view).
- [Visual approval gate #15](https://github.com/Odourman/the-skraun/issues/15) remains OPEN. Earlier P1/P2 prone horizontal-quad models are ONLY incorrect anatomical reference and must not be promoted.

## 2. Non-negotiable actual game/character contract
- **PLAYFIELD / GAME CAMERA** is topdown; **CHARACTER STANDS UPRIGHT ON THE SCREEN**: horns/head at top, recognisable eyes/open mouth as pixel-art symbols, shoulders/arms outward, two separate legs/feet below. **Never lie down**. Do not demand photorealistic topdown optical anatomy of the face; a stylized readable upright face is valid.
- Exactly **two** visual facings, RIGHT and its **exact per-row horizontal bitwise reverse LEFT**. No extra up/down facing sprite. 8-way joystick movement is unchanged: vertical movement reuses prior R/L orientation; no ROM joystick implementation in this task.
- **8×12 logical monochrome/light-gray P0-style source only**, two A/B limb-walking poses, conceptual scaling L1 8×12, L2 16×24, L3 32×36 only, no new height or wider 2-player composite. All game/halo rules remain unchanged.
- U1 is **provisional reference only**, not approved final sprite. P3 original source is frozen. No silent overwrites or source-hash changes.

## 3. Newly independently measured risk: MIRROR ≠ VISUALLY DISTINCT FACING
In the exact current P3 U1 bitmap, source Hamming cell differences (of 96):
- U1 pose A RIGHT vs pose A LEFT = **10**.
- U1 pose B RIGHT vs pose B LEFT = **12**.
- U1 pose A RIGHT vs pose B LEFT = **5**; pose A LEFT vs pose B RIGHT = **5**.
- U1 pose A RIGHT vs pose B RIGHT = **7** (likewise LEFT). 
Head crown rows 0–2 are exactly symmetrical; four R/L changed cells lie in rows 3–4. The rest arises in limbs/feet that animate, so the apparent facing cue may be swamped by gait changes.
**These numbers are strictly source geometry, not proof of human perceptual direction recognition.**

## 4. Two limited U1-derived direction-visibility hypotheses
Make **exactly two** U1-derived 8×12 families, not a new unrestricted sprite search:
1. **D1 – Permanent face/ear cue.** Try ONE stable left/right asymmetric head/cheek/horn/ear cue, present in both A and B, retaining two horns, eyes, open-mouth signature and upright stance. It should mirror conspicuously but remain a troll face, not a profile animal or one-eyed human.
2. **D2 – Permanent shoulder/arm/torso cue.** Preserve the U1 head/face as much as practicable; create a stable facing-dependent shoulder/upper-arm/torso asymmetry *not accidentally reversed by the A/B gait*, retaining standing posture and two separate feet. Avoid recreating turtle/insect/prone anatomy.

All D1/D2 right-facing A/B bitmaps must be authored, with left-facing derived by **exact mirror**. Upper face/identity and permanent orientation cues should ideally remain invariant across walking poses; limb pixels should animate independently. Do not change the two-pose animation into a horizontal flip. Do not add a colored marker or a second sprite. Changes may produce a negative result — report failure rather than overclaim.

## 5. Non-circular proof and required presentation
- Primary criterion is **recognisable left vs right at NATIVE LEVEL-1 4:3 approximate TV scale** while standing upright, with face preserved. Show randomized, **unlabeled** R/L A/B images first (with an answer key on another page), plus clearly labeled source-grid sheets, equivalent 8×12 native glyphs, source-based two-pose loops and one unzoomed full-playfield 160×192/4:3 display. All previews marked DESIGN, NOT STELLA.
- Show at least 4 cases per family: A-R, A-L, B-R, B-L at identical position/background/scale. Compare against **frozen original U1**, optionally Q1 as past upright control. Full 2×2 cross-facing comparisons are important: if A-R still resembles B-L more than B-R, disclose it.
- Provide an objective, reproducible script reporting source bit Hamming for (AR, AL, BR, BL) and pose differences; **never assert that an arbitrary Hamming threshold proves human-facing recognition**. Describe head, limb and mouth readability in natural size and any tradeoff.
- At most **two** D1/D2 new families. Unsuccessful result is acceptable. Do not run a subjective test with fabricated blind-viewer results. MAIN and user remain independent aesthetic approvers.

## 6. Delivery and STOP
Complete ONE reproducible design package: JSON exact bitmaps, assembly-friendly **non-executable** tables with TOP_FIRST/BOTTOM_FIRST clearly labeled, automated validator for exact dimensions/mirrors/frozen U1 provenance/pose changes, native pixel PNG and conceptual 4:3 nearest-neighbor comparison, A/B GIFs with same cadence, 2×2 facing confusion / source-difference audit, complete ZIP with SHA-256 manifest and report. Publish **separate P3-F1-only branch and draft PR or clearly linked branch**, complete Google Drive ZIP, and a clear MAIN II handoff. Keep the original user sketch private.
- **STOP after ONE P3-F1 delivery.** If neither D1 nor D2 makes facing visually readable while retaining identity, deliver a **NEGATIVE FACING RESULT** and explicitly preserve unresolved issues.
- **NO** P3-F2/P4/v0.4, ROM, actual Stella, ART1 level3 fix [#19](https://github.com/Odourman/the-skraun/issues/19), P01-ART2, R4, B3c, new enemy/halo/world/HUD art, gameplay/joystick implementation, independent VERIFICATION, merge to main, closing #15, or claiming final art acceptance.
- This scope **adds no authorization** to ROM DEVELOPMENT; full-game R3 feasibility NO-GO remains unchanged.
