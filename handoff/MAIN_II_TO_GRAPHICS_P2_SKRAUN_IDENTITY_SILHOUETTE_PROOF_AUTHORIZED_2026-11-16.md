# THE SKRAUN — MAIN II TO GRAPHICS: P2 IDENTITY-SILHOUETTE PROOF
**Authorized by MAIN II, 2026-11-16, following user instruction to continue.**
**ONE strictly bounded DESIGN-ONLY study. Not v0.4, P01-ART2, R4, B3c, ROM work, or art approval.**

## 0. Authority and exact evidence
Read the real current sources before designing:
- [Fixed decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), especially overhead 4-legged character, three sizes, two A/B walking poses, horizontal L/R mirror, 8-way joystick unchanged.
- [Skraun visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md).
- User's [PRIVATE original hand drawing in Drive](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view): broad expressive eyes, open mouth, two ear/horn projections, long independently moving upper limbs and longer lower limbs/large feet. It is an **anatomy/identity reference, not a camera/perspective reference**. **Do not copy the photograph into a public repository, ZIP, screenshots or report.**
- [P1 exact two source candidates](https://github.com/Odourman/the-skraun/tree/graphics/p1-horizontal-axis-perspective-proof-20261116/graphics/skraun_p1_horizontal_axis), especially A_rounded_back and JSON masks, and [accepted bounded P1 decision](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_P1_HORIZONTAL_AXIS_REVIEW_AND_DECISION_2026-11-16.md).
- [P01-ART1 full authentic Stella report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-p01-art1-p0-stella-readout/docs/ROMDEV_P01_ART1_MAIN_II_STELLA_VISUAL_READOUT_2026-11-16.md), [PR #18](https://github.com/Odourman/the-skraun/pull/18), and [real Stella evidence on Drive](https://drive.google.com/drive/folders/11s5rWZTkpHVplOCRcAhGSPnzC4C-iT5l). The 8×12 L1 and 16×24 L2 readout is pixel-exact; ALL 12 L3 readouts failed due to one erroneous 64-native-pixel top row. [Technical defect #19](https://github.com/Odourman/the-skraun/issues/19) is tracked, NOT authorized for repair. [Visual gate #15](https://github.com/Odourman/the-skraun/issues/15) remains open.

## 1. Main problem: identity, NOT another casual pixel tweak
Authentic Stella shows that A's horizontal quadruped is physically more consistent with topdown than frontal Q1, but A reads as turtle/beetle, B as an insect and Q1 as frontal. None clearly resembles the horned, wide-eyed, open-mouthed, long-limbed *Skraun* of the user drawing at L1; A/B gait often only resembles blinking feet.

This ONE study asks whether an 8×12 genuinely overhead, horizontally oriented quadruped can express more of that unique **creature identity** than P1 A **without reverting to a standing/front-facing humanoid**.

## 2. Two deliberately different identity hypotheses ONLY
Create two **new** 8×12 monochrome candidate families with two source-authored A/B walking poses and exact horizontal bit reversal for left-facing. Right-facing head on bitmap RIGHT, rump left, four limb stations extending along both upper and lower silhouette edges. Keep light-gray player on flat dark backgrounds; do not change game rules or adopt other sprite dimensions.

1. **I1 / HEAD-SIGNATURE:** Give strongest feasible visual priority to **two outward head horn/ear points** and a distinctly **open mouth/dark negative-space opening** (with eye separation where genuinely possible). Use a less shell-like back than P1 A and four visible paw/limb contacts. This is a deliberately head/face-led attempt; assess whether it sacrifices quadruped readability or becomes a side-view face.
2. **I2 / LIMB-SIGNATURE:** Give priority to **long, expressive front limbs and distinct hind feet/claws**, and outward ear/horn outline; favor an irregular creature body rather than a turtle shell/segmented insect. Encode as much face as naturally survives in true overhead view, but **do not fake an eye/mouth PASS** merely through explanatory labels. This is genuinely movement/silhouette-led, not a slight recolor or 1–2-pixel variant of I1.

Use frozen **P1 A** as fixed benchmark, with historical Q1 optional as a *labeled* negative perspective reference. Do NOT retouch or replace A/Q1 or invent further I3/I4. Quantify changed pixels versus A and differences between I1/I2; no arbitrary changes to frozen data.

**Important trade-off:** A strict topdown camera may make the front-view open mouth impossible at 8×12. If so, say explicitly which attribute failed and why. Do NOT silently tilt the camera or convert to a humanoid/frontal character. Do not pretend that merely enlarging 8×12 at L3 creates details missing at L1.

## 3. A/B motion and sizes
- Exactly 8×12 logical source bits, 2 distinctive poses, left/right exact row-wise mirror for both.
- Same *conceptual* size scaling as frozen canon: 8×12, 16×24, 32×36 (NUSIZ widths 1×/2×/4×, vertical repeats 1×/2×/3×).
- Show changed foot/limb cells distinctly between poses, upper and lower; avoid moving the head or flipping a whole body as a disguised walk. Compare source-derived two-pose loops at a documented and identical frame cadence.
- Source-created sprite previews are **NOT Stella**. No attempt to repair #19 or generate a new ROM during this design study.

## 4. Required evidence for MAIN/user aesthetic decision
One cohesive comparison package, easy to judge without reading an essay:
- Exact 8×12 native pixel grids for **I1, I2, frozen P1 A** at both poses, both facings; no invented/painterly imagery in the technical comparison.
- Side-by-side **L1 first** in nearest-neighbor, 4:3 approximate TV display; include an unenhanced 1× glyph and monochrome silhouette. Follow with L2/L3 conceptual displays, clearly marked NON-STELLA.
- Honest comparison of horns/ears, eyes, open mouth, long upper limbs, four paws/large hind feet, topdown head-to-right, side-direction readability, turtle/beetle/insect risk, and change from pose A to B. Show at least one forest and one night flat-background legibility reference with no claimed PF renderer.
- Explicit comparative judgment **per candidate**: Identity and topdown both convincingly present? If NOT, label **IDENTITY NOT PROVEN**, even if 100% source tests pass. No self-declared user art approval.
- Include a source validator checking width/height, exact mirror, two distinct poses, meaningful upper/lower limb animation, original benchmark provenance and file manifest integrity. No subjective score turned into automated PASS.
- Original bitmap JSON plus assembler-friendly data as non-executable reference, image/GIF previews, README, SHA-256SUMS, consolidated complete ZIP on Google Drive and an isolated design branch/draft PR or equivalent explicitly linked source evidence. State exact ZIP SHA-256 and provenance.
- **Keep the user's original hand drawing private.** No public original-photo reproduction.

## 5. Formal stop and failure branches
Stop after delivering **I1, I2, and A baseline**. MAIN II will evaluate identity visually, with USER retaining final aesthetic approval.
- If neither outperforms A at actual L1 native size, report **NEGATIVE IDENTITY RESULT**, stop; recommend a future **separate user/MAIN decision** on character reinterpretation, alternate art representation, or sprite geometry. Do NOT autonomously switch to 8×14, larger glyphs, software sprites or multi-player composite sprites.
- No new GRAPHICS P3, v0.4, extra sprite dimensions, sprite finalization, new enemy/environment/HUD/halo art, P01-ART2, ART1-FIX, R4, B3c, gameplay, ROM, main merge, independent VERIFICATION, or issue #15 closure.
- Old R3 full-scene NO-GO and level3 technical defect #19 remain unchanged.

This is a **single comparative visual-identity decision gate**, not permission to iterate indefinitely. Hand completed source/ZIP/draft PR and qualitative report to MAIN II and stop.
