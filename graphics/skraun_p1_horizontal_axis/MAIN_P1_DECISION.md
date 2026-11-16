# THE SKRAUN – MAIN DECISION – GRAPHICS P1 HORIZONTAL AXIS

**Status:** bounded post-v0.3 art proof only; NOT production art or a new v0.4.

## Decision: does horizontal body-axis solve the long-standing FRONT-vs-TOPDOWN problem?

**PARTIAL VISUAL PASS for camera geometry; NO FINAL IDENTITY ACCEPTANCE.** Previous Q1 placed a two-eyed head on top and two feet below, leading to a visually upright biped. A and B place the muzzle/head at the right edge, horizontal back to the left, and four up/down paws at two distinct X anchors. Left-facing forms are EXACT bit reversal. This is more consistent with a four-legged overhead animal and demonstrates that previous vertical/anatomical mapping was a central error, rather than solely 8×12 sprite size.

| Version | Geometry | Identity | Level1 readability | Recommendation |
| --- | --- | --- | --- | --- |
| Q1 v0.3 | head above, feet below | recognizable original face, incorrect camera | frontal humanoid | retained reference only |
| A – rounded back | horizontal torso, broad back, 4 short paddles | weaker eyes/horns, lost mouth, turtle/beetle ambiguity | legs and right head just visible; needs scale/contrast | **better candidate for further DESIGN decision** |
| B – low long back | thinner torso and head-right snout, 4 longer legs | eyes/horns equally sparse; increased insect risk | anatomy more leggy but not unmistakable troll | comparison / reserve |

**Best aesthetic option for MAIN to evaluate is A, with B as an alternative**, not an automatic approval. I would not tell the user the drawn Skraun identity is already preserved. All source-level geometry checks pass, aesthetic identity remains an OPEN decision.

## Anatomical coordinates (right-facing bitmap)

Both A and B: 8×12 and 2 A/B frames, left counterpart via reversing each 8-bit row. x0=picture left, x7=picture right. `row0` top paw region and `row11` bottom paw region. Rear paw upper/lower body anchors are at approx x1; fore paw anchors near x4-5; head rightmost x7, eye holes at x6/y5 and x6/y7, small ear/horn contour in y3-4 and y8. **No frontal head at top**. A/B tip shifts upper and lower feet without moving body center. Exact changed cells in JSON and heatmap; these features are visually fragile at 8×12.

## Physical-size and tech constraints

1. Nominal scales: L1 8cc ×12 lines, L2 16cc ×24 lines, L3 32cc ×36 lines; all use unchanged original dimensions and NUSIZ0 modes. 1cc≈1.6 scanline-units on 160cc×192lines 4:3 preview. L1 appears roughly 12.8×12 display units, i.e. square; a horizontal quadruped may read like turtle or insect even when axis is correct.
2. Both designs lose original's distinct open mouth and waving hands; two dark holes read as eyes in the upper/lower head region mainly at higher level. Some original character identity requires extra artistic/hardware headroom or a deliberate simplifying decision.
3. Compared with Q1, A and B do remove obvious bipedal upright reading. However neither is proved to be a recognisable troll at L1, and there is NO user aesthetic approval. This outcome is not a basis for automatic game integration.
4. New art must not inherit the old historical R3-VFIX "head-at-top" oriented pixel regression as semantic truth. It also must not delete that historical test. New future test would assert **head-right on right-facing, head-left on left-facing and all four paws upper/lower**, while independently checking scanline memory order. Absolutely NO ROM work was done in P1.
5. R3 practical issues (same-Y three enemies ~20Hz, ~2–4 spare worst-line cycles, halo and obstacle same PF pixels) are unchanged. No new mechanic, ring size, P1 enemy, kernel or TIA technique implied.

## MAIN gate / stop

- **Approve only P1 source production as a concept investigation.** No sprite final approval.
- MAIN should explicitly decide whether A's quadrupedal but turtle-like look is acceptable as a stylized Skraun, whether B is better, or whether original-face fidelity is more important than strict 8×12 topdown.
- If neither is acceptable, stop and consciously choose between a stylized Level1 silhouette, separately authorized different source dimensions, or deliberately changing visual camera constraints. Do not iterate into P2/v0.4 without MAIN scope.

**STOP: no ROM, R4, B3c, main merge or independent VERIFICATION. Issue #15 remains open.**
