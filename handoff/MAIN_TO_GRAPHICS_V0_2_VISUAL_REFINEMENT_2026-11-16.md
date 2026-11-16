# THE SKRAUN — MAIN TO GRAPHICS — v0.1 REVIEW / v0.2 VISUAL REFINEMENT
**Date:** 2026-11-16  
**Authority:** MAIN, continuing the existing GRAPHICS design-only assignment.  
**Status:** v0.1 ACCEPTED **AS EXPERIMENTAL GRAPHICS SOURCE DATA ONLY**. Candidate C is the **working comparison baseline**, NOT final artistic approval or a production sprite. No ROM implementation, R4, B3c, MAIN merge, issue closure or independent VERIFICATION is authorized.

## 1. Exact material reviewed

- Graphics branch `graphics/skraun-pixel-candidates-v0-1-20261116`, checked HEAD `e3da7c4efb9ee031543821ba945a8ca2d91c66dd`.
- `graphics/skraun_v0_1/sprites.json`: 8×12 bitmaps for A/B/C, two frames; logical top-first; direct mirror per direction.
- `graphics/skraun_v0_1/SKRAUN_PIXEL_DATA.inc`: right/left top-first and bottom-first assembler data, not drop-in replacements for indexed R3-VFIX tables.
- `graphics/skraun_v0_1/skraun_C_preview.svg`: exact SVG preview, **not Stella**.
- `graphics/skraun_v0_1/halo_pf_static_art_mask.json`: static PF-art draft; not gameplay reach or implemented dynamic ring.
- `graphics/skraun_v0_1/README.md` and [Google Docs design report v0.1](https://docs.google.com/document/d/1zMKBqW84Oe6nPXUYEfrqOE4JxqusD3m8E5C3QVTSPZ8/edit).
- Governing: [user's private original drawing](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view), [decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [confirmed top-down visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [MAIN post-R3 visual design proposal](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_POST_R3_VISUAL_DESIGN_REVIEW_PROPOSAL_2026-11-16.md), [open visual gate #15](https://github.com/Odourman/the-skraun/issues/15).

### Confirmed distinctions

- The A, B and C candidates all share the same **five upper logical bitmap rows** (ears/head and oversized forward-facing eyes). New C changes primarily **rows 5–10** relative to A. Its two animation frames are exact horizontal mirrors in the shape of limb movement, and only rows 5, 6, 9 and 10 change between C's frames; left/right mirror sources appear consistent.
- **C has clearer leg/forelimb separation than A/B**, but the display still looks largely like a *front-facing little monster with limbs*, not an unmistakably **top-down four-legged creature**. The user explicitly rejected the earlier front-facing camera interpretation. Improving anatomical overhead readability must come **before final C approval**.
- The data are **static pixel art**, not Stella implementation. The 8×12 bitmap's logical head/feet order is correct top-first; actual ROM kernel order must be independently mapped when ROM DEVELOPMENT is later authorized.
- The static ring masks use 40 PF cells × 24 bands, 8 scanlines per band. Calculating nonzero vertical footprint from the exact JSON: **level 1 = 10 bands = 80 scanlines**, **level 2 = 16 bands = 128 scanlines**, **level 3 = 22 bands = 176 scanlines**. This is nearly an entire 192-visible-line NTSC arena for level 3. These art footprints are NOT accepted as attack reach or gameplay rule and require an accurate **TV pixel-aspect**, clipping, PF-mask-capacity and obstacle overlap evaluation, contrasted with R3's separately documented 48-color-clock × 72-scanline level-3 diagnostic.
- The cited GitHub graphics branch currently contains **five files** under `graphics/skraun_v0_1/`; the indicated Drive graphics v0.1 folder currently contains **the Google Doc only**. MAIN has **not located or independently validated the claimed local 14-file / 156KB ZIP** or its SHA256 `034e9c221fed003e1bf163f4dbddef7711be8dc72214d727a9f17a73f068eedf`. Early knight/archer drawings, GIF and world contrast boards may be embedded in the Doc or exist locally, but their individually reproducible source files have **not** been found in this handoff. **Do not call them source-audited or final.**

## 2. GRAPHICS v0.2 work authorized within existing design remit (NO ROM development)

### A. Rework Skraun's actual overhead silhouette
Deliver at least two focused variants:
1. `C-refined`: retain C's readable limbs and the user's head/eye/horn identity, but reduce visual dominance of the frontal face; improve four-legged body, front legs and separated hind feet.
2. `C-overhead`: a genuinely top-down interpretation of the same original four-legged creature, preserving ears/eyes where legible and exactly two A/B step poses, two mirrored facings. This is **a distinct art comparison**, not a unilateral change of camera/game rules.

- Keep light-gray appearance; two horizontal facings are exact bitwise reflections; eight joystick directions remain a gameplay matter for ROM DEVELOPMENT; three levels share anatomical identity.
- Prefer starting from 8×12 logical pixels, but explicitly mark any proposed size change and its implications rather than quietly expanding sprite resources.
- Compare **actual 8×12 pixels** (not just enlarged smooth rendering), black silhouette, realistic TV-sized 160-wide Atari view at correct NTSC pixel aspect, A/B consecutive frames, and 3 scaled levels. Show which limbs move and distinguish figure from front-facing humanoid appearance.
- Preserve exact row-order metadata. Include an automated check for logical head/ears above rear paws, not merely a bounding box. Do not claim actual sprite orientation in Stella without a ROM experiment.

### B. Riddare and grön bågskytt next
- Publish explicit source bitmap tables and side-by-side visuals for a recognizable **knight with sword** (idle + warning/raised sword) and **green archer with bow**.
- At genuine candidate TIA 8-bit widths, evaluate small-size silhouette in grayscale and colored forest backdrop. Do not accept colored 8-byte blobs as identities.
- Distinguish separate *art proof* from any claim three independently placed enemies can be drawn in one ROM/scanline. R3's 20-Hz same-Y and RAM/cycle limits remain open.

### C. Four-world scene boards and halo proportionality
- Create a small controlled art board for forest, mountain, dream, night using sparse **realistic PF cell shapes** and dark backgrounds, with contrast tests for gray player, green bow archer, arrow and gold halo.
- For every halo level, provide **visible color-clock width, scanline height, visual aspect on NTSC, distance from P0 edge**, centered-on-player example and edge clipping cases. Compare 176-scanline draft to previous R3 72-scanline prototype as **non-equivalent experiments**, not quietly altering decided attack geometry.
- Suggest at most two alternate aesthetic halo silhouettes/line thicknesses for MAIN to choose, without changing mechanic that larger/tougher halo at higher levels passes through solid obstacles. Make any same-PF-pixel conflict with scenery conspicuous.

### D. Make delivery inspectable
- Publish exact source files, PNG overview montages, an animated GIF / consecutive-frame sheet if used, static enemy + world mockups, JSON masks, assembler-ready art data and a README with source/provenance.
- Upload **one complete versioned ZIP to the project graphics Drive folder** and supply a usable direct link, file count and SHA-256; check the file actually exists in Drive and matches manifest. Mirror text-based sources in the isolated GitHub graphics branch. Do not assume a local ZIP is remotely accessible from a statement alone.
- Label every asset **pixel art design / concept / static mockup / authentic Stella** accurately. The unrelated online green dragon stock/AI image from the first handoff must not appear as original project evidence.
- Keep the user's original hand-drawn photo private in Drive; no inclusion in public repo/ZIP unless explicitly authorized.
- Continue independently within GRAPHICS' existing design work. Gather a small *decision-ready visual comparison* for MAIN; do not request approvals for each tiny edit.

## 3. Explicitly NOT approved

- **No final acceptance of C**. C is a useful working baseline only.
- No permanent ring dimensions/reach, final color register values, level3 scaling or new gameplay rules.
- No new ROM/6502 kernel, real Stella claim, integration, R4, B3c, sprite-scheduler change, `main` merge or issue #15 closure. ROM DEVELOPMENT must receive a later separate MAIN authorization.
- No independent VERIFICATION now; the existing R3 visual/technical gates stay distinct.

## 4. Finish line

Send MAIN one concise, **visually inspectable** v0.2 package with:
- C-refined versus C-overhead versus v0.1 C at real pixel size and magnification;
- 2 pose A/B exact bitmaps, mirror pair and 3 levels, with visual quality tradeoffs;
- knight sword+warning pose and archer bow recognizability, visibly evaluated at 8-pixel width;
- 4 world contrast/obstacle boards;
- halo size/time-constraint notes;
- complete Drive ZIP and GitHub text art sources;
- explicit recommendation **and what still remains unproven in Stella/hardware**.

MAIN will make the aesthetic choice afterwards. Do not start a ROM feasibility study or change decided project canon on your own.
