# THE SKRAUN – U1-FIX1 verified single-correction delivery
**2026-11-16 | DESIGN ONLY | NOT STELLA / NOT ROM / NOT APPROVED**

**MAIN II scope:** only the frozen U1, no new candidate families. Exactly one head cell removed, minimal arm/foot gait correction and exact mirrored facings.

- **Full self-contained 21-file ZIP**: https://drive.google.com/file/d/1brrYlMseD8rmRaVRQ2CAvanVUkRjI_xs/view
- Filename: `THE_SKRAUN_U1_FIX1_DIRECTION_HEADPIXEL_2026-11-16.zip`
- **Exact bytes: 118516**
- **Exact SHA-256:** `02ef45d636867a384dc88dabeac4338996e2f0f6b275b2d5e17dacaa6fea935a`
- Google Drive ZIP was fetched back and independently hashed over the actual returned bytes: **EXACT MATCH**.
- ZIP CRC test PASS; 20/20 in `SHA256SUMS.txt` PASS (the manifest itself excluded); clean-directory image/GIF regeneration and 21/21 file-by-file byte identity PASS. Source validator PASS.
- Only `U1_FIX1_BITMAPS.json` and `U1_FIX1_ART_DATA_ONLY.inc` hold the corrected U1 data (RIGHT A/B and exact mirrored LEFT). Original U1 embedded unchanged only as comparison.
- **Exact head fix:** RIGHT bitmap source x7,y3: `01100111` -> `01100110` in BOTH poses; mirrored LEFT x0,y3. No other face/horn pixels altered.
- Gait fix: A RIGHT y5 `11111110` -> `01111111`; B RIGHT y6 `00111101` -> `01111101`; B RIGHT y11 `11000001` -> `10000011`. No width/height change.
- Precise before/after native L1, 160×192, approximate TV 4:3 and source matrix panels plus two equal-cadence GIF animations are in the ZIP.
- The user's private original drawing remains private and **is not in ZIP or public GitHub**.
- **Honest result: EXTRA HEAD PIXEL RESOLVED. DIRECTION READABILITY AT NATIVE L1 STILL NOT PROVEN**; the standing facing may read as front-facing despite source asymmetry. Head side asymmetry and pose bit distances do not demonstrate human perception.
- MAIN II/user alone decides aesthetic acceptance. #15 remains open. Not another P3/P4 study, no ROM, Stella, hardware, integration, merge, implementation, gameplay changes or independent VERIFICATION.

**STOP after this single U1-FIX1 delivery.**