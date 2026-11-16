# THE SKRAUN — MAIN II | U1-FIX1 source audit and remaining direction gate
**Date 2026-11-16 · MAIN II independent receipt · SOURCE-ART ONLY · NOT STELLA/ROM/FINAL ART**

## 1. Provenance and strict boundaries
- The user's instruction after viewing the actual U1 GIF: **"U1 ser bra ut, men den ser ut att gå till vänster på höger bilden och till höger på vänster bilden. Det är en pixel förmycket på ena sidan av huvudet också"**. This is positive feedback on overall U1 appearance **with two explicit outstanding defects**, not a final visual acceptance.
- Original frozen P3 U1: [actual P3 JSON](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json), source GitHub blob `16f3c53d809fb3b3d67e52512199ddc3f40d450b`.
- Corrected source-only [isolated U1-FIX1 branch](https://github.com/Odourman/the-skraun/tree/graphics/u1-fix1-facing-headpixel-20261116/graphics/u1_fix1); [developer's precise report](https://github.com/Odourman/the-skraun/blob/graphics/u1-fix1-facing-headpixel-20261116/graphics/u1_fix1/MAIN_II_U1_FIX1_REPORT.md).
- Source branch compared against `main`: **10 commits ahead / 0 behind, ten added art/docs/scripts files only**, no old ROM/source modified, not merged.
- THIS IS NOT a new graphics family, revised game canon, new rendering mode, ART1 L3 fix, or independent Verification.

## 2. Actual independent Drive ZIP verification
[Exact original complete package](https://drive.google.com/file/d/1brrYlMseD8rmRaVRQ2CAvanVUkRjI_xs/view), file `THE_SKRAUN_U1_FIX1_DIRECTION_HEADPIXEL_2026-11-16.zip`.
- Downloaded actual ZIP bytes from Drive and checked **118516 bytes**, SHA-256 **`02ef45d636867a384dc88dabeac4338996e2f0f6b275b2d5e17dacaa6fea935a`** — **PASS**.
- **21 entries**, ZIP CRC **PASS**, **20/20** SHA256SUMS entries compared against actual archive members — **PASS**.
- Extracted in own workspace, ran bundled `validate_u1_fix1.py`: **PASS** (8×12 exact source, frozen baseline, bit-exact left mirror, source diff ledger, image/gif dimensions, manifest, no private drawing).
- In a clean directory, regenerated all **10 PNG, two GIF** from unchanged JSON and render script; **12/12 generated visual files matched the submitted ZIP byte-for-byte**, including original A/B/LEFT/RIGHT images. Exact regenerated answer key also identical. Existing source-only `.inc` tables independently checked against JSON and validator PASS. **Do not assert literal whole-package 21/21 regeneration**: that requires also regenerating the frozen manifest/docs/source and was not independently repeated in this audit.
- Images are *Pillow-generated conceptual design previews* (160×192/640×480 4:3 and resized detail views), NOT actual Stella screenshots or measured raster traces. GIFs: two frames of 180 ms each, stationary no induced right/left translation. No human panel test performed.

## 3. Exact source diff, 0-based coordinates
- **Head original RIGHT x7,y3:** original `01100111` → corrected `01100110`, both A and B. Corresponding LEFT mirror is x0,y3. All OTHER FACE/HEAD ROWS, HORNS AND EYES unchanged. **This specific source-bit removal is proven**, though the user has not yet separately confirmed that this is exactly the excess pixel they perceived.
- **Pose A RIGHT row y5 arms:** `11111110` → `01111111` (**2** bit flips).
- **Pose B RIGHT row y6 arms:** `00111101` → `01111101` (**1** bit added).
- **Pose B RIGHT row y11 feet:** `11000001` → `10000011` (**2** bits flipped).
- Total source changed pixel-cells **A 3/96, B 4/96**. LEFT exactly mirrored on all 12 rows. Original face and 8×12 body maintained; two poses.

## 4. Independent numeric geometry finding (NOT human readability)
| Comparison of 96 logical cells | Frozen U1 | U1-FIX1 |
|---|---:|---:|
| A RIGHT vs A LEFT | 10 | **8 (decreased)** |
| B RIGHT vs B LEFT | 12 | **12 (unchanged)** |
| A RIGHT vs B LEFT | 5 | **6** |
| B RIGHT vs A LEFT | 5 | **6** |
| A RIGHT vs B RIGHT animation difference | 7 | **6 (decreased)** |

These are **precise observed bitmap-cell distances**, not direction identification accuracy. This means one cannot describe FIX1 as a verified increase in face-direction discriminability: first-pose mirror asymmetry became **smaller**, and overall A/B bit animation also shrank by one cell. The actual shape may nonetheless look more directional to a person; that hypothesis is **NOT PROVEN** until the user assesses the real-size GIF and/or unlabeled four-state sheet without labels.

## 5. MAIN independent normal-scale visual assessment
- MAIN inspected `00_L1_BLIND_FACING.png` **before** `00_L1_BLIND_ANSWER_KEY.md`, `01_L1_BEFORE_AFTER_SAME_SCALE.png`, and `04_EXACT_8x12_BITMAPS.png` from the **actual extracted source ZIP**. The head edge asymmetry is removed in both poses and mirrors; on the real-size 4:3 crops the change is very subtle.
- A front-facing symbolic troll head remains visually dominant in the 8×12 sprite, so A/B limb movements look largely like **walking/arm-swinging in place** rather than a clearly identified direction of travel.
- **Do not relabel a bit-mirror PASS as a perceived right-facing or left-facing PASS**, nor infer the user's reaction. In a stationary two-frame cycle, horizontal *travel* cannot be demonstrated without a separate actual motion scenario; not adding artificial motion to the GIF is correct for inspecting facing.
- USER is the needed final aesthetic judge for which direction looks correct and whether the removed head cell is the unintended cell.

## 6. MAIN II ruling
1. **U1-FIX1 accepted as a completed narrow SOURCE GRAPHICS CORRECTION** with ZIP/provenance/bitmask integrity PASS; the x7,y3 source head pixel has been removed correctly. No rewrite or second FIX1 cycle.
2. **Facing/gait real-size recognizability remains OPEN and unproven.** Do not claim user-visible correction of 'right reads as left' until user verifies. User had said U1 overall looks good; do not downgrade that to complete identity failure nor promote it to final approval.
3. **Keep [visual gate #15](https://github.com/Odourman/the-skraun/issues/15) OPEN**, [ART1 L3 #19](https://github.com/Odourman/the-skraun/issues/19) OPEN and independent P01 #1 OPEN. R3 same-Y/halo/full-engine NO-GO unchanged.
4. No further graphics iteration, renderer/stella integration, P3-F2/P4, enlarging 8×12, M0, NUSIZ, hardware mapper, new ROM, ART1 bugfix, merge or independent Verification is authorized by this receipt. A distinct user decision is necessary for any subsequent work.

**Immediate next action (user review, not a developer task):** present the actual submitted U1-FIX1 stationary RIGHT and LEFT GIFs and before/after true-size panel, and ask the user whether they now **perceive** RIGHT as right, LEFT as left, and whether this is the exact head pixel intended. If not, keep the gate blocked until a separately authorized correction strategy.
