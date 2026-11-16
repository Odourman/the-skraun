# THE SKRAUN – GRAPHICS U1-FIX1 | En enda avgränsad U1-korrigering

**2026-11-16 | SOURCE ONLY – NOT STELLA, ROM, INTEGRATED OR ART APPROVAL**

## Exact original source
P3 frozen U1 A/B from [U1 source](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json), original GitHub blob SHA `16f3c53d809fb3b3d67e52512199ddc3f40d450b`. The user original sketch inspected privately but never placed into this package.

## Exactly one U1-FIX1 (not a new family)
- Head: **RIGHT x=7,y=3** (0-indexed from top-left, row originally `01100111`) changed from 1 to 0, leaving row `01100110`. Both A and B. For LEFT the same physical defect is mirrored at x=0,y=3. Head/horns/eyes/mouth in every other row remain identical.
- Facing/gait: RIGHT A arm row y5 changes `11111110` → `01111111` (two bit flips), giving the rightmost raised arm a distinct lead cue. RIGHT B arm row y6 changes `00111101` → `01111101` (one added middle/left arm cell), maintaining a moving right arm. RIGHT B foot row y11 changes `11000001` → `10000011` (two changed bits) so the right foot is wider during that stride. These are only targeted arm/foot changes, not a body redesign.
- LEFT A/B obtained ONLY by exact horizontal row mirror. No third direction. No NUSIZ, M0, additional palette, extra hardware, extra rows, second sprite or ROM work.
- Original vs fixed A source cells modified: **3/96**; B: **4/96**. A/B changed cells in fixed family: **6/96**. Source metrics are not human perception proof.

## Honest visual verdict
The one protruding head pixel is unambiguously corrected in source masks, and the new A/B arm/foot placement creates a right-biased forward cue in the authored RIGHT frames, with exact reversed LEFT cues. **However, reliable perceived walking direction at actual native level-1 cannot be established from these source changes alone.** In particular, 8x12 standing troll has an almost frontal face; body/limb motion across A/B can look like swinging in place, and mirrored silhouettes can remain directionally ambiguous. **DIRECTION: NOT PROVEN / MANUAL USER REVIEW REQUIRED**. Do not claim that visually facing has been fixed until the user personally confirms by viewing the unlabelled L1 panel and both GIFs.

## Inspect in order
1. `00_L1_BLIND_FACING.png` before opening answer key (not a performed human test)
2. `00_L1_BLIND_ANSWER_KEY.md`
3. `01_L1_BEFORE_AFTER_SAME_SCALE.png` and `02_L1_NATIVE_160x192.png` both same-size source derived, no extra zoom
4. `03_L1_FULL_TV_4x3.png` (full 640x480 nearest-neighbor conceptual TV image)
5. `04_EXACT_8x12_BITMAPS.png` and `05_CHANGED_PIXELS_AUDIT.png` for precise cell check only
6. `GIF_U1_FIX1_RIGHT_A_B.gif` and `GIF_U1_FIX1_LEFT_A_B.gif` two pose animations at same cadence, stationary position; no animated directional arrows or motion introduced to bias the evaluation.

## Stop
One single U1 fix only. No additional candidate family, P4, new format, ROM, Stella, independent verification, merge, gameplay change or closure of visual gate #15. Await MAIN II and user aesthetic verdict.
