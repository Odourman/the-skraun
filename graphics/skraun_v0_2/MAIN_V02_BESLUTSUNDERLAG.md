# THE SKRAUN – GRAPHICS v0.2: MAIN decision memo

**Date:** 2026-11-16. Status: preliminary design candidates, not final or Stella-tested.

## Art comparisons

| Candidate | Benefits | Risks | Status |
|---|---|---|---|
| v0.1 C | MAIN-accepted reference bitmap, readable limbs | Dominant frontal face | Reference only |
| C-refined | Keeps sketch-like character and more marked A/B limb movement | Still somewhat humanoid/front-facing | Candidate |
| C-overhead | More continuous quadruped-like back, shorter head, stronger limb/hip differentiation | Eyes and 8-bit visual constraints still invite frontal interpretation | **Recommended for aesthetic exploration** |

All candidates have 8 columns × 12 top-first rows, one bit per pixel, a two-pose A/B walk and exact bitwise left/right reflections. Levels use the same anatomical pixel source widened x1/x2/x4 and repeated vertically x1/x2/x3. The two facings are not new up/down artwork.

## Enemy silhouettes

Riddare: helmet and blade silhouette, neutral and warning/raised sword pose. Grön bågskytt: attempted separate left-curved bow contour and drawing pose; **still uncertain recognition at tiny normal size**. Green applies to archer; knight's color is exploratory.

## Scenery

Skog, berg, dröm, natt each have two distinct masked layouts at 40 PF cells × 24 bands × 8 scanlines; half PF mirror to represent a plausible CTRLPF scheme, without asserting runtime support or obstacle-halo coexistence. Provisional color swatches not verified NTSC codes.

## Halo proportionality

| Family | Level 1 | Level 2 | Level 3 |
|---|---|---|---|
| Original v0.1 | 40 cc × 80 lines | 64 cc × 128 lines | **88 cc × 176 lines** |
| Alternative A: compact | 48 cc × 48 lines | 72 cc × 64 lines | 96 cc × 80 lines |
| Alternative B: dramatic | 64 cc × 64 lines | 96 cc × 96 lines | 128 cc × 112 lines |

Geometric footprints measured from the actual binary PF masks. 4 clock widths per PF cell; 8 scanlines per vertical band. For original level 3, 176/192 = 91.7%. With conceptual ring centered at (80,96), only 8 lines remain both above and below. Moving the unmodified ring center to y=24 or y=168 clips roughly 39.3% of its colored mask pixels; similarly x=12 or x=148. These are offscreen clipping simulations, **not** a working dynamic ring.

Actual graphics depend on one TIA playfield color per pixel in the tested renderer. Independently colored gold halo and blue obstacle at the same PF pixel are unproved. Never interpret alternative size as an authorized attack-radius change, and do not compare v0.1's 176-line mask with R3's 72-line diagnostic as if same rendering experiment.

## Decision recommended

Use C-overhead as the next artistic base, retain C-refined as fallback, require explicit future independent ROM implementation authorization before claims about Stella, same-Y enemy visibility, register timing, RAM or halo/hinder coexistence. **Do not mark v0.2 art as MAIN-approved without explicit choice.**

Complete pictures, animated pose comparisons and exact source files are in [v0.2 Drive ZIP](https://drive.google.com/file/d/13lmZX_SbFm27fceYJuE0DdYiZhO7U2q_/view), SHA-256 `17227108204134d2fc3cb3dccad69f7633d8d092dd824aa6172bd88c09e9f9ff`.
