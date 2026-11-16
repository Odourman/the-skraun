# THE SKRAUN — MAIN II TO GRAPHICS: U1-LEG1 CAPRINE TWO-POSE GAIT
**Explicit, separate authorization issued 2026-11-16, solely in response to new USER aesthetic feedback**
**Scope:** ONE source-art-only two-pose *leg-region* design correction. This is NOT P3-F1 reopening, not U1-FIX1 reopening, not a sprite-format change, not Stella/ROM.

## 1. Binding user input and actual source
> "Övre delen är perfekt nu. Men det hade varit bra om benen rörde sig lika bra, som att den går med getben. Ben som en get har."

**Interpretation:** User has now positively approved the *LOOK of the present U1-FIX1 upper portion*. Do not call it full sprite approval. User specifically wants the **two lower legs to have a recognizable, articulated goat/satyr-like gait**, not generic swinging human legs. This is design feedback, not an instruction to change gameplay, actual four-direction sprites, sprite size or hardware.

**Mandatory SOURCE, NOT older U1:** [U1-FIX1 JSON on exact isolated GRAPHICS branch](https://github.com/Odourman/the-skraun/blob/graphics/u1-fix1-facing-headpixel-20261116/graphics/u1_fix1/U1_FIX1_BITMAPS.json), GitHub blob SHA `811bd1f7da51d1003174423f30e6b8d0ebe77b1c`; use `single_corrected_U1_FIX1.A` and `.B` as the immutable base. Do not accidentally use older P3 U1 (it includes the unwanted right-head pixel). Read [independent MAIN II receipt](../docs/MAIN_II_U1_FIX1_SOURCE_REVIEW_AND_DIRECTION_GATE_2026-11-16.md) and [visual direction](../docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md).

**The private original user hand-drawn image is reference only:** https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view . It MUST NOT be copied/embedded in a public GitHub repo or ZIP.

## 2. ABSOLUTE FROZEN UPPER REGION
At raw 8×12 source pixels with TOP-FIRST zero-indexed rows:
- For each of RIGHT pose A and RIGHT pose B, **rows y=0 through y=8 (NINE complete rows) MUST BE EXACTLY BIT IDENTICAL to the existing U1-FIX1 source**. This includes both horns, the corrected x=7,y=3 head cell, eyes, mouth, head/shoulders, both animated arms, trunk and lower-torso edge. Do NOT even shift the entire sprite one source cell.
- Allowed edit coordinates: **EXACTLY ROWS y=9, y=10 and y=11, columns x=0..7**, the existing **lower legs and hoof silhouettes only**. Any edit outside this region = automatic source compliance FAIL.
- **Two source animation poses A and B only**, preserving their original order/cadence unless MAIN explicitly says otherwise. RIGHT and LEFT are exact per-row bit mirrors; no special upward/downward facing or alternate goat head.
- Keep 8×12, source gray (210,210,209 in conceptual preview), the three existing level scale mappings as **conceptual only** and native screen 160×192 vs 4:3 presentation 640×480. No new dimensions/frame count/color, NUSIZ change, missile, P1, extra mapper, raster effects or kernel changes.

This freeze is deliberate: **the user says the upper part is perfect**. Protect this positive result, including existing arm animation. If three pixels of vertical leg area prove insufficient, do NOT steal approved head/arm/torso rows or silently introduce a taller new art format.

## 3. One sharply bounded gait hypothesis
Create **ONE new U1-LEG1 8×12 design family**, not a menu of unrelated art concepts. Two A/B frames; render both mirrored facings.

Visual objective, if achievable in 3 bottom source rows:
- Suggest **two CAPRINE/SATYR-LIKE rear legs** attached to the body's existing hip area, not human upright straight calves and not a four-legged horizontal animal.
- Convey **a deliberate hock bend/ankle kink** (goat hindlimb hock) through offset leg pixels and **recognizable hoof-like flared tips** rather than sneakers. At such low resolution, suggest split/cloven hooves only if clear without clutter.
- The two poses should show **alternating weight support and step**: one hoof pushes off/lifts while the other plants; on B exchange relative roles. Leg movement should add to, not erase, the already-approved A/B arm motion.
- Keep exactly **two lower legs / feet** as visible as feasible. Avoid disconnected "flying hoof" pixels, limb merging, apparent three/four feet, or dramatic torso/bouncing/repositioning which breaks the frozen upper region.
- The anatomy reference is suggestive, NOT a detailed realistic skeletal recreation. Real goat hindlimb has a stifle and a distinct hock/tarsus above the cannon/pastern and hoof; [National Goat Handbook](https://richland.extension.wisc.edu/files/2010/11/national_goat_handbook.pdf) or [North American Packgoat anatomy list](https://napga.org/wp-content/uploads/2022/12/Packgoat-Guidebook-v2021.2.pdf) identify hock, pastern and hoof. Do not claim goats' knees bend backwards.

**CRITICAL FEASIBILITY/HONEST STOP:** only three raster rows are editable in this scope. It may be IMPOSSIBLE to visibly convey both hock bend and cloven hoof AND alternating action. If the exact-size source image still looks human-straight or 'walking in place' with no recognizable goat legs, **deliver a truthful NEGATIVE LEG ANIMATION result and STOP**, not a visual-pass assertion. The only possible later step would be a **NEW, SEPARATE user/MAIN authorization to explore taller-than-8x12 source geometry** with full L3/full-scene hardware costs. NOT AUTHORIZED HERE.

## 4. Source + evidence contract
- Use a **NEW isolated GRAPHICS U1-LEG1 branch**, separate from original P3, post-research P3-F1 and U1-FIX1; do not amend these frozen branches.
- Author exact A/B RIGHT/LEFT bit rows in one machine-readable source file (JSON), human-readable `8×12` tables, source-only .inc top/bottom order as needed. Create deterministic Python validator that **independently asserts all 9 upper rows of both original RIGHT A/B identical**, exact L/R row reversal, source dimensions, only lower 3 rows modified, hoof/body continuity, two animation frames, and no forbidden assets.
- Produce (a) **before/after true L1 scale** comparison against exact FIX1 using native 160×192 and 640×480 approximate 4:3 nearest-neighbor on forest AND night, (b) two stationary RIGHT/LEFT two-frame GIFs with same 180ms per frame as current FIX1, (c) optional enlarged *clearly labeled diagnostic pixels* (never use it alone to claim success), (d) an **unlabeled face/gait comparison + answer key** if useful to user, (e) data audit listing EVERY leg-region changed cell per pose.
- A/B GIF animation must NOT translate whole sprite horizontally or move camera artificially to fake perceived direction. Do not assert "faces right" based solely on mirrored bit counts. Explicitly say if visual stepping direction at actual L1 remains ambiguous.
- Rebuild in clean directory; package EXACT ONE ZIP, SHA-256 manifest of all included files, log archive size/full SHA, verify download of the real uploaded Drive bytes against ZIP hash. No fabricated images/frames/test scores.
- Include direct user-oriented review panels, exact original source provenance and MAIN II handoff. Keep the original sketch private.

## 5. Interpretation/acceptance
- **Source PASSES** only when source snapshot, frozen y0..8 rows, 8×12, mirrored L/R, two A/B frames and file checks reproducibly PASS.
- **Aesthetic success is NOT asserted by GRAPHICS.** The user evaluates whether 'goat legs' and gait are actually readable in normal size. A negative output is legitimate.
- [Visual gate #15](https://github.com/Odourman/the-skraun/issues/15) stays OPEN until user expressly accepts.
- [ART1 L3 #19](https://github.com/Odourman/the-skraun/issues/19), [P01 independent #1](https://github.com/Odourman/the-skraun/issues/1), R3 same-Y + PF halo complete-scene NO-GO unaffected.

## 6. HARD STOP
After ONE bounded source-art U1-LEG1 delivery or an explained negative limitation, STOP. No new other-family D3/P3-F2/P4, no altered head/torso/arm pixels, no 8×16/8×20, no >2 frames, no real DASM or Stella, no ROM hardware integration, no 6502 implementation, no R4/B3c, no ART1 repair, no merge to main, no independent Verification. Any future broader work needs distinct explicit MAIN + user authorization.
