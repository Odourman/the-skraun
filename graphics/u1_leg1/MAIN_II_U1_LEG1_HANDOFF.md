# THE SKRAUN — U1-LEG1 one-source-family graphical handoff

**2026-11-16 | Single GRAPHICS source-only lower-leg deliverable | STOP | NOT STELLA OR FINAL ART**

User: "Övre delen är perfekt nu. Men det hade varit bra om benen rörde sig lika bra, som att den går med getben. Ben som en get har."

One new **U1-LEG1** candidate based on actual **U1-FIX1** (not original unfixed U1). Frozen upper rows **0..8 exactly unchanged in BOTH A/B**, including corrected head x7,y3, horns, face, shoulders, arms and torso. Only **y9–11** altered.

| Pose | Prior U1-FIX1 y9..11 | New U1-LEG1 y9..11 |
|---|---|---|
| A | `01100110 / 01000110 / 11000011` | `00100110 / 00100011 / 01100000` |
| B | `01100110 / 01100010 / 10000011` | `01100100 / 11000100 / 00000110` |

**Changed cells only in allowed lower three rows:** A=**9**, B=**8**. Each changed cell is listed in `LEG_REGION_CHANGE_LEDGER.json`. LEFT = exact 8-bit row-reversed RIGHT. A contains grounded left hoof at y11 and lifted right tip at y10. B exchanges sides. Four-neighbor pixel continuity from upper body maintained. **No new size, frame, TIA color, missile, NUSIZ, P1 or ROM program.**

**Verified package:** [Google Drive ZIP](https://drive.google.com/file/d/1hMP78tBR5NrBnaBXdvc3yub23xTJB8vv/view), 39124 bytes, SHA-256 `bd0d303f9793e43f6945a51b2e85aa5b0adfd4e9f17b7912b67229651c49db5c`; 22 files / 21 manifest hashes. Clean build identical for all 23 local files including ZIP; actual raw Drive download byte identical. 10 PNG previews, 2 x 2-frame stationary 640×480 4:3 GIFs (180ms/frame), full generator, validator, audit, art-only .inc and separate blind-view key. Check covers pixel positions inside each GIF against actual source 160×192 nearest-neighbor 640×480.

**Uncomfortable but necessary limitation:** the visual difference at regular L1 size is *a leg lift/plant* and a tiny pixel staircase, **not convincing specific goat hind-leg anatomy**. Both hooves' shapes and the hock joint cannot clearly be independently recognized with only three source pixel rows; any claim of "getben PASS" would be unsupported. The older left/right perceptual direction complaint is also not proved solved. The upper region is kept because user positively approved it. **NEGATIVE GOAT-HOCK IDENTITY**, but source-delivery/self-test PASS. No human blind test, no Stella nor independent Verification. User is artistic judge.

**STOP:** no LEG2/P4, 8×16 format, new ROM, Stella, merge, #19 fix, or closing #15 authorized from this result. Only recommendation is that MAIN/user consider a separately authorized taller-source-format technical/visual cost decision if they want recognizable goat anatomy.
