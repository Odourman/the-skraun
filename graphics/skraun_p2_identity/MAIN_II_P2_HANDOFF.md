# THE SKRAUN — GRAPHICS P2 IDENTITY SILHOUETTE PROOF

**Handoff to MAIN II | 2026-11-16 | DESIGN ONLY | STOP AFTER THIS PACKAGE**

## Overall result: NEGATIVE IDENTITY RESULT / NO AESTHETIC PASS

The two new single-color 8×12 families have distinct intentions and exact source data. On a native-color-clock L1, neither is clearly recognizable *without explanatory labels* as the user's original horned, big-eyed, open-mouthed, long-limbed troll viewed directly overhead. The structural left-right quadruped is preserved, but an 8x12 TV-size glyph carries too few legible facial cells. **Source-data tests PASS and identity does NOT PASS.** This does not prove that all possible 8×12 designs are mathematically impossible.

**Comparative reading at actual L1 takes priority over enlarged pixel boards and L2/L3 mocks.** I1 may be a modest improvement over P1 A in an enlarged head-board, but at native L1 the mouth is a small notch and the horns/eyes merge. I2 has more expressive forelimb pixels but risks insect/crab reading. Neither should be pronounced the user's Skraun.

| Category | P1 A — FROZEN | I1 — HEAD SIGNATURE | I2 — LIMB SIGNATURE |
|---|---|---|---|
| Overhead/head axis | right-facing head right (yes) | same (yes) | same (yes) |
| Face / two eyes | 2 negative pixels hard to see | two negative pixel holes (x5,y4),(x5,y7); not convincingly readable at L1 | two negative eye holes (x6,y5),(x6,y7); face weaker |
| Horns / ears | tiny contour / weak | small upper/lower righthead prongs; ambiguous, could read as jaws | short upper/lower head outline; weak |
| Open mouth | absent | two blank right-edge cells (x7,y5–6) as an actual **open notch**. Encoded, but not legible as an expressive open human-like mouth at L1 | absent; deliberately sacrificed for limbs |
| Long upper forelimbs | short paddle shapes | compact upper/lower limbs, less distinctive original movement | longer sweeping arms over upper/lower back contour; movement changes tips |
| Four paws / large hind feet | yes / modest | yes / modest | rear toe pads broader, more distinct |
| Creature-identity risk | turtle / beetle | pincers / open-jaw bug or turtle | insect / crab / generic sprite |
| Identity and topdown both convincing at L1? | NO | **NO** | **NO** |

## Quantitative source comparison (NOT an objective aesthetic score)

- P1 A baseline untouched, both 12-row frames exactly as approved experiment reference, original source-file SHA-256 `bf818ec4b998fa66c2ab1db26a637e807737f830efab04854219ab14b9dd99b0`.
- I1 vs frozen P1 A: 16 changed cells in pose A, 20 in pose B. I1 A/B difference: **16** cells (8 upper rows 0–2; 8 lower rows 9–11). Head/body rows 3–8 stay stable between poses.
- I2 vs frozen P1 A: 19 changed cells in pose A, 27 in pose B. I2 A/B difference: **12** cells (6 upper and 6 lower), head/body rows 3–8 stay stable.
- I1 vs I2: **23** cells differ in pose A, **35** in pose B. They are distinct source silhouettes, not 1–2-pixel variants.
- All have exactly 8×12 right-facing glyphs, source-authored two-frame A/B, and exact row-wise horizontal mirrors for left; tested 3 conceptual size modes L1 8cc×12, L2 16cc×24, L3 32cc×36. The first/last source rows are **upper/lower limb space**, not upright head/feet.

## Camera and mouth feasibility

The private original is a frontal marker drawing with two short upward horns, large widely separated eyes, open dark mouth, hands reaching diagonally up/out and two longer separate legs/large feet. Its face is the most distinctive identity marker. The binding gameplay camera is directly overhead, so moving the eyes/mouth to the right head region compresses these into 1-bit notches. I1's mouth is an honest *open edge pixel gap* but looks more like a bite taken from a silhouette than the original grinning open mouth. More enlargement cannot restore semantics absent in level1. I2 prioritizes limbs, forfeiting readable mouth. **We do not tilt the camera or hide failures.**

## Source and genuine Stella comparison boundaries

MAIN II's P01-ART1 actual DASM/Stella 6.7.1 package was downloaded, opened and a selection of real L1/L2 images inspected as the baseline. Original ART1 reports 24/36 exact source-to-raster states, the other 12 L3 states fail because of a 64-native-pixel erroneously gray first row, 262 NTSC scanlines per tested state. That is an existing defect tracked at issue #19 and NOT fixed. Neither I1 nor I2 ran in Stella, and no images in this P2 package are actual emulator captures. Rendered backgrounds are flat and not evidence of a full game PF renderer.

## MAIN II recommendation / stop

**Do not approve I1 or I2 as the final player sprite.** If MAIN II must retain an *art-only* comparative reference, I1 best probes the head/mouth hypothesis, while I2 demonstrates the cost of favoring limbs, but neither is a visually persuasive final Skraun at L1. This is a **negative identity result** under the bounded source constraints; do not start v0.4/P3, new dimensions, a software-sprite architecture, or a new Stella ROM without separate MAIN authorization and user aesthetic decision. Do not silently erase the original horn, eye and open-mouth identity requirements.

**Technical blockers remain unchanged:** ART1 L3 issue #19; issue #15 visual gate; R3 20 Hz same-Y enemy multiplex, limited kernel cycles, and shared PF color conflict for halo/hinders. No game code, existing canonical art, main branch, issues or independent VERIFICATION modified.
