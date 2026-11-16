# THE SKRAUN – MAIN decision: GRAPHICS P1 horizontal-axis perspective proof
**Date:** 2026-11-16.  
**Authority:** MAIN review of an isolated design-only proof.  
**Disposition:** **P1 DONE – SOURCE/DELIVERY ACCEPTED; PERSPECTIVE HYPOTHESIS SUPPORTED; NO FINAL CHARACTER ART ACCEPTED.**

## 1. Reviewed actual evidence, not only the handoff text
- Actual [Drive P1 ZIP](https://drive.google.com/file/d/1ouk4vL_gBVcb3Jc_-EP5UKSQLV1mEaSC/view): `THE_SKRAUN_GRAPHICS_P1_HORIZONTAL_AXIS_2026-11-16.zip`, **376608 bytes**, SHA256 `d716e93cf6f15f5944fb9716efffd1217d2c716dbc3909906c2ba382aa728cd1`. MAIN actually downloaded the ZIP: central directory **15** members, `testzip()=None`, **14 of 14** SHA256SUMS entries match their extracted files; `verify_p1.py` executed successfully locally.
- Examined the **actual** designer PNGs, in particular `00_MAIN_DECISION_SHEET.png`, `01_ANATOMICAL_8x12_BITMASKS.png`, `02_BLACK_WHITE_SILHOUETTES.png`, `03_ALL_THREE_LEVELS_NTSC.png`, `04_AB_AND_EXACT_MIRRORS.png`; both 2-frame GIFs and metadata are in the verified archive. They are **design pixel previews, NOT Stella screenshots**.
- [P1 GitHub sources](https://github.com/Odourman/the-skraun/tree/graphics/p1-horizontal-axis-perspective-proof-20261116/graphics/skraun_p1_horizontal_axis), reviewed branch HEAD `b5bc31a3485faf67199631c01768bf221f061292`; actual `SKRAUN_P1_PIXEL_MASKS.json`, `.inc`, `MAIN_P1_DECISION.md` and test source.
- Compared with the user's **private original hand drawing** in Drive, fixed [decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), previous [GRAPHICS v0.3 decision](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_V03_FINAL_DELIVERY_DECISION_2026-11-16.md), and expressly authorized [P1 scope](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_P1_HORIZONTAL_AXIS_PERSPECTIVE_PROOF_2026-11-16.md).

## 2. Technical-source and visual findings
- **PASS source provenance**: all candidates are *exactly* 8×12 and retain two A/B frames with four body-anchor paw stations, head-right on right-facing and precise row-wise horizontal mirror for left-facing; **12 changed bitmap cells** between A/B for both designs; 3 legacy conceptual level sizes 8×12, 16×24, 32×36. This is SOURCE inspection, not a hardware runtime PASS.
- **Actual aesthetic observation**: Original Q1 still looks like a front-facing standing character. The P1 proposal changes the body axis from vertical to horizontal. **Both A and B are more consistent with a creature viewed from directly overhead** and are clearly distinguishable from the old front-facing sprite at original raster size.
- **A / rounded back** is MAIN's **preferred physical-perspective comparison candidate**: best continuous back/trunk, four projecting paws and less insect-like than B. **But it reads like a turtle/beetle/abstract small creature**, not unmistakably the user's original grinning, horned troll; the open mouth and readable horns are absent, and eye cutouts are fragile at level1.
- **B / long low back** has a clearer narrower body and more separate limbs but looks **more insect-like**, especially in black silhouette and level1. Keep only as a deliberately different control.
- The approximate 160cc×192-line game-size mockups viewed at 4:3 reduce the already-small level1 to a **few physical pixels**. The larger levels help body readability but are merely scaling; enlarging a bitmap will **not restore omitted mouth/horns**. Higher bit-count A/B pose changes do not automatically prove a compelling animation.
- Do not call A the **final** Skraun, and do not quietly reinterpret the original hand drawing. Artistic recognizability is a USER/MAIN approval gate.
- This is **not proof** all possible 8×12 topdown troll sprites are impossible; it does show a more meaningful perspective trade-off than adding two vertical rows.

## 3. MAIN decisions: what is accepted and what is not

**APPROVED AS TECHNICAL/ART REFERENCE ONLY:**
1. A *horizontal body axis*, head right for right-facing, head left as **exact horizontal mirror** for left-facing, **upper/lower pairs of front and rear paws**, remains MAIN's **preferred VISUAL DIRECTION for evaluation**. Camera stays overhead, 2 A/B poses, 3 sizes, gray color; no change to eight gameplay movement directions.
2. **P1 candidate A** becomes the **sole preferred NEW ART1 P0 sprite-under-test**, with B and v0.3 Q1 as control/test comparisons. These are **placeholders / test candidates**; **NO final character aesthetic approval**. Original character's horns/mouth personality remains an **open identity risk**; no silent removal of requirements.
3. GRAPHICS P1 is **closed as a bounded graphics investigation**. No further tiny revisions, no P2/v0.4 automatically authorized.

**NOT APPROVED:**
- A/B as final sprites, new mandatory 8×14 or other dimensions, any change to body/species/identity or permanent design canon, any production renderer, R4, B3c, enemy animation/render integration, full game halo/PF collision, new cartridge mapper, merges to `main`, issue #15 closure or independent VERIFICATION.

## 4. Why a single isolated real Stella art test is worth doing

All P1 imagery is source-authored design preview; no real Stella output supports how P0 will look with its actual color-clock scaling, raster row repetition, two A/B frames and left/right head orientation at levels 1–3. This matters for user aesthetic evaluation; a raster preview cannot decide the TV-sized silhouette and subtle gait.

MAIN therefore issues a **separate, tightly bounded P01-ART1 ROM DEVELOPMENT authorization** in [its own handoff](../handoff/MAIN_TO_ROM_DEV_P01_ART1_SKRAUN_STELLA_VISUAL_READOUT_AUTHORIZED_2026-11-16.md). This is **only** a P0 visual readout of **A** against comparison **B** and **Q1**, not the production sprite decision or the full scene renderer. NO full R3 overlap, enemy AI, halo, obstacle colors or gameplay. Keep this separate from the currently blocked P02 engine work. This is a distinct explicit authorization, not automatic R4/B3c.

### Essential orientation regression warning
The historical R3-VFIX tested the then-current sprite whose **head belongs at the top of the image**. That remains a valid test for its original frozen ROM. For P01-ART1 new A/B, visual orientation must be tested instead as **head at right for right-facing, at left for mirrored left-facing**, with fore/hind paws on upper/lower raster bands; memory addressing still must render correct physical scanline order. **Never remove or rewrite original orientation regression tests.**

## 5. Remains blocked
R3 NO-GO applies unchanged to the full game: approximate 20Hz three same-Y competing enemies, 30Hz haloring-versus-obstacle appearance, 2–4 static worst-line cycles of headroom, and unproved arrow/orb/HUD/AI coexistence. Proving an isolated P0 sprite looks correct is **NOT** proof the full Atari 2600 scene architecture is feasible.

**Stop at P01-ART1 handoff for MAIN's later actual user-visible aesthetic decision. GRAPHICS no further scope. VERIFICATION remains dormant.**
