# THE SKRAUN – MAIN PERSPECTIVE REFRAME / LIMITED GRAPHICS STUDY P1
**Date:** 2026-11-16  
**Status:** MAIN authorizes **ONE narrow, design-only, post-v0.3 perspective test**. This is **not** an automatic `GRAPHICS v0.4`, a final art decision, a change to the user's game mechanics, a ROM/6507 implementation, R4/B3c, a mapper decision, a main merge or independent VERIFICATION.

## 1. Authority and exact problem

Source authority in order: user-drawn [original Skraun](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view) (private), [Decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [confirmed visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [MAIN v0.3 review](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_V03_FINAL_DELIVERY_DECISION_2026-11-16.md), [GRAPHICS v0.3 reproducible source](https://github.com/Odourman/the-skraun/tree/graphics/skraun-v0-3-final-readability-20261116/graphics/skraun_v0_3).

User-established hard constraints remain: **light-gray four-legged troll, camera straight overhead, 2-step A/B limb/leg walking, only left/right mirror graphics, 8-way motion as gameplay, 3 level sizes, small ears/horns and eyes, orange/gold magic halo** (the halo color is gold; do not change it). The original hand drawing is a *character/anatomy reference* but is read frontally, **not an approved camera view**. Do not publish the private photo.

**Structural diagnosis:** Every v0.1–v0.3 main player 8×12 candidate starts with ears/head at the *top of the sprite array*, eyes across the upper rows and hind feet at the bottom. This encodes a mostly frontal/upright humanoid silhouette, so even Q1/Q2 limb changes and the 8×14 thought experiment cannot reliably read as *an overhead quadruped moving left/right*.

**MAIN's new design hypothesis — NOT adopted final canon:** reorient the **anatomical forward axis horizontally**. For the right-facing sprite, put the **head/snout toward the right bitmap edge**; rump/back toward the left; four short paws/limbs emerging **above and below the central back at two separated X positions**, instead of two arms extending sideways from a frontal head plus feet at the bottom. Left-facing is exact bitmap mirror (REFP0 candidate). Two eyes and small ears/horns may be simplified and should be evaluated as negative pixels or marginal contour, without changing the character identity. This is fully compatible *in principle* with the current rule of 2 facings; but no final face or pose has been approved.

**Important correction to previous sprite-test assumptions:** An old P0 orientation regression expects "head above / feet below" because it validates *that particular old bitmap*. If MAIN eventually chooses a left/right-headed quadruped, **the new sprite's semantic orientation ground truth MUST become right-facing head-at-right, left-facing head-at-left, four paws in upper/lower bands**, plus correct row memory order in each actual raster kernel. Do not remove the historical R3-VFIX regression or silently reinterpret it for the new art. All existing ROMs retain their current P0 image until a separate implementation scope.

## 2. New MAIN concept proof (illustrative, not candidate acceptance)

MAIN created two *crude 8×12* digital masks against Q1 to examine whether anatomical axis is the blocker rather than sprite size. The small examples `H1` and `H2` read closer to turtle/creature silhouettes than the frontal Q1, but remain generic, may resemble insects, and do NOT adequately express the original's eyes/personality. They are **research aids only**, NOT mandatory assets or approved designs, and neither is Stella-tested.

**8×12 H1 A (right-facing; bit 7 = left, bit 0 = right; row0 = upper body-space):**
```
01000100
11001100
01000100
01101110
01111101
11111111
11111111
01111101
01101110
01000100
11001100
01000100
```

**8×12 H1 B:**
```
00101000
01101100
01000100
01101110
01111101
11111111
11111111
01111101
01101110
01000100
11011000
01010000
```

**8×12 H2 A:** same as H1 A except logical row 5 is `01111111`. **H2 B:** same as H1 B except row 5 also `01111111`. That creates a slim rump; not necessarily better. These masks are deliberately crude tests of head direction and leg topology, not aesthetic direction.

## 3. Single authorized GRAPHICS subtask: overhead 8×12 anatomical reframe

**Scope:** create only **TWO distinct design candidates**, not an unlimited iteration series and not incremental `Q3/Q4` face modifications.

- Both must be **light-gray overhead quadrupeds with head toward right for the right-facing pose**, exact mirror for the left-facing pose, two A/B stepping poses and same **8×12** logical grid. Do not silently enlarge to 8×14 or use new TIA hardware.
- One candidate should favor a **rounded broad back + short lateral paws**; the other a **longer low-backed body + head/snouthorns more distinct**, both unmistakably **not** a standing humanoid. Preserve two eyes if physically readable at level1, and disclose if visibility tradeoff requires de-emphasizing one facial detail. Do not quietly erase important user-original features or reinterpret as different species.
- Test **two forepaws plus two hindpaws**: they must arise from **two distinct body-X stations** on both upper/lower outline. Document foot body anchors, not just pixel-count differences. A/B must actually move the front and rear feet.
- Display against the fixed v0.3 Q1 **at approximate 4:3 NTSC color-clock aspect** (each color-clock ~1.6 display height units) at 1×,2×,4× width with 12/24/36 nominal heights, in black silhouette and gray against forest/night. Make two-frame GIF or consecutive frame strips. Include all original bitmap rows, mirrored rows, and deterministic structural validators.
- Provide a **qualitative honest judgment**: is this more genuinely topdown? Does it look like the *same Skraun* or an insect/turtle unrelated to the drawing? Is it readable at level1? If the approach fails, say **FAIL** and stop rather than producing more variations.
- Keep prior v0.3 knights/archer/world/halo files unchanged. **Do NOT** attempt to solve R3's sprite multiplex/CPU/halo-PF conflict. R3's technical NO-GO remains a separate issue.
- One isolated graphics branch / coherent tiny 8×12 pixel data + PNG/GIF and complete manifest with one accessible Google Drive package only if actual assets justify it. Keep original photo privately in Drive. Do not create new game code or call an AI image a Stella capture.

## 4. User approval gate / stop conditions

At completion, present a **single decision sheet** for MAIN: current Q1 vs overhead Candidate A vs B; anatomically labeled head/eyes/horns, torso, four paws; two frames, mirrored left/right, 3 levels at NTSC aspect; exact bitmaps and self-tests. **Deliver PASS as source data, not as final user aesthetic acceptance**.

No automatic follow-on GRAPHICS P2, `v0.4`, R4, B3c, ROM work, changes to prior `Troll3` table, production pixel sizes, accepted attack/ring/level mechanics, GitHub main merge, close of issue #15, or VERIFICATION. If neither candidate meets the four-legged/identity goal, MAIN should stop and explicitly decide between a stylized first-level visual, different sprite dimensions, or a deliberate camera compromise rather than continuing tiny pixel edits.

**MAIN's current decision is only to investigate the *horizontal body-axis* representation. No final player sprite or new canon silhouette is approved.**
