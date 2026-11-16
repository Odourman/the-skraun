# THE SKRAUN — MAIN II: TIA-inspired U1 visual mechanism concept comparison
**2026-11-16 | RESEARCH / SOURCE-DERIVED VISUAL PROOF ONLY | NO DASM, STELLA, VERIFICATION OR PRODUCTION ART**

## 1. Actual completed work
User asked MAIN to *continue* after the all-30 Atari-trick research. MAIN completed exactly the recommended **FIRST, NON-ROM** comparison before making any decision about ROM or additional GRAPHICS work.

**Frozen real source:** [P3 U1 8×12 bitmap](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json) from P3 author's genuine full Drive package **SHA256 `84129bc78fa5a0884fb3866fe6b20f18ba7b4ff2b0f3d2aa2d784431b2d86a2a`**. Source blob SHA `16f3c53d809fb3b3d67e52512199ddc3f40d450b`; **both A/B and their exact per-row mirrored L/R source bitmaps were held unchanged**.

**New self-contained evidence package:** [THE_SKRAUN_P3_TIA_TECHNIQUE_DESIGN_COMPARISON_2026-11-16.zip in Google Drive](https://drive.google.com/file/d/1LkX5DZ9vGacznqaTPRZfbbQ-zHXnfLpF/view). MAIN created a deterministic Pillow-based source-driven **technical visualization**, not generative picture art. Uploaded the actual ZIP to project graphics Drive folder, then downloaded it back and verified the actual returned bytes:
- ZIP **61,970 bytes**, SHA256 **`d2c1d3184c34dd64ae6cc7d9ac54a703feeaf39b01c3b595074f251bb700fb0a`**, ZIP CRC **PASS**, **44 members**, **43/43 SHA256SUMS** manifest entries **PASS**.
- `build_concept_comparison.py` and `validate_concepts.py`; validation **PASS** for frozen source, mirrors, each native 160×192 color-clock preview matching its 640×480 nearest-neighbor 4:3 image exactly, M0 specific cells and generated asset integrity. 4 visual mechanisms × A/B × R/L = **16 source variants**, with 16 160×192 native and 16 TV images; 5 contact sheets, JSON ledger and blind-labeled image + separately held key. Nothing simulates actual TIA write deadlines or cycles.
- The user's original handdrawn sketch was read **privately** but neither included in this ZIP nor committed to public GitHub.

**Review in this order INSIDE the ZIP:**
1. `01_FOUR_METHODS_FULL_TV_4x3_A_RIGHT_LEFT.png` full TV-sized comparison.
2. `02_L1_NATIVE_DISPLAY_CROPS_NO_EXTRA_ZOOM.png` normal TV pixel scale, no second enlargement.
3. `03_WALK_A_B_FOREST_NIGHT_NATIVE_DISPLAY_CROPS.png`.
4. `04_ENLARGED_SCHEMATIC_NOT_REAL_SIZE.png` for audit only; gold M0 cells there are **annotation**, the actual visual uses the same gray as P0.
5. `05_BLIND_L1_VIEWS_NO_FACING_LABELS.png` and `05_BLIND_ANSWER_KEY.json` for an independent future human reading test. **No human blind-viewer test was performed or scored.**

## 2. Head-to-head result: actual full-screen Level-1 impression

| Exact technique hypothesis | Main source-geometry change | SOURCE-ONLY visual observation | MAIN judgment |
|---|---|---|---|
| Baseline P3 U1 | None. 53 lit 8×12 cells pose A, 52 pose B | Original face/horns small; upstanding troll-like but generic and left/right subtle | **FROZEN REFERENCE ONLY** |
| **#17 M0 'ninth contour pixel'** | Extra one-clock column x8 on R/x−1 on L, M0 enabled only at fixed scanline rows 3 and 4; +2 color-clock cells each pose, same P0 gray | Slightly elongated outside right/left cheek/ear edge, still tiny eyes and mouth; contour may look beaklike, not uniquely the user's troll | **NO MEANINGFUL IDENTITY WIN; NO ROM GO** |
| **#06 NUSIZ larger head** | Head source rows 0–4 drawn schematically at 2× width, centered over unmodified 1× body, so 16-clock head vs 8-clock torso; source P0 still eight independent bits | Head reads broader but also flattened and bar-like, horns/eyes stretch without gaining detail. At L3 the nominal P0 width is already 4× maximum, so cannot preserve the same 2:1 ratio at all sizes | **NO MEANINGFUL IDENTITY WIN; technical centering UNPROVEN** |
| **#12 two gray P0 color bands** | Original mask and silhouette unchanged; concept head RGB235/235/233 rows 0–4, body RGB190/190/188 rows 5–11 (illustrative, NOT measured NTSC palette) | Head/body separation slightly improved; mouth/eye geometry unchanged; cannot color eyes separately inside a P0 raster line | **NO MEANINGFUL IDENTITY WIN** |

**MAIN verdict:** The three independently tested idea families are real or physically plausible *categories* of TIA tricks, but the three **specific visually simulated concepts** produce **NO clear original-character likeness improvement** over frozen U1. This does NOT prove that every M0 shape, NUSIZ timing strategy or color palette is useless; it does establish that **a simplistic hardware overlay/size/shade is not an adequate reason to build a new production ROM**. User called U1 only 'lite åt rätt håll', so don't mistake a two-color head or two additional edge pixels for the unique horned, large-eyed, open-mouthed, expressive-armed original.

## 3. Real-world feasibility not assumed
- `M0` shares `COLUP0` with P0, so this is NOT a second independent-colored bitmap. `REFP0` does not reposition M0; the mirrored left missile X must be updated independently. The documented 2008 AtariAge `COLUP0` bit-D0/ASL/ENAM0 technique needs **at least five EXTRA CPU cycles per affected line** **if** the per-row color byte is already loaded; data/addressing/positioning may cost more. Existing R3 full-scene worst rows reportedly have only 2–4 cycles spare, so **not a drop-in integration**.
- `NUSIZ0` 1×/2×/4× width cannot make an independent 8× expanded face, and enlarging only head rows while horizontally **centering** them needs correctly timed mid-sprite positioning/HMOVE. [Steven Hugg's 2025 three-stream reference](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html) uses HMOVE/HMP0 but does not prove it fits **our** R3 scene. At Skraun L3 head is already at nominal 4×: different proportions across levels could violate player-level visual design and original #19 first-row glitch remains.
- `COLUP0` colors ALL lit P0 pixels on a raster line (and same M0), not two eyes/mouth independently. The two RGB values used here are **not verified Stella NTSC values or authorized alternate art palettes**.
- None of these concepts is a playable ROM; no enemies, PF halo/obstacles, game-world backgrounds, 262-frame timing, genuine TIA color or CPU-cycle constraints were exercised. The full game R3 same-Y 20Hz and halo/scenery/PF/color technical **NO-GO remains**, as do [ART1 raster defect #19](https://github.com/Odourman/the-skraun/issues/19) and [open aesthetic gate #15](https://github.com/Odourman/the-skraun/issues/15).

## 4. Decision after SOURCE-ONLY experiment
1. **RESEARCH STEP COMPLETE with clear NEGATIVE VISUAL-GAIN conclusion for these three simple variants.** No final sprite selected, no ROM/Stella authorization. Evidence ZIP and hashes above are binding evidence of *source-derived design images only*.
2. **Recommended next, as a SEPARATE MAIN decision:** resume the previously bounded **GRAPHICS P3-F1** design-only effort: exactly two new U1-derived **8×12** standing troll candidates **D1 face/original identity-first and D2 distinct upright arm/torso silhouette with persistent R/L cue**, four facing/pose states each, original reference kept private, true-size 4:3 comparisons, reproduceable source masks and STOP. These are **new P0 bitmap design hypotheses**, not claims that M0/NUSIZ/two gray shades work with R3.
3. No reason to commission M0/NUSIZ P0-only Stella test based on this weak visual result. If later P3-F1 likewise fails convincingly, MAIN should ask the user about **fundamentally different sprite footprint/character readability tradeoffs**, rather than silently iterating P4 or sacrificing original likeness.
4. This report itself does not release the earlier P3-F1 research HOLD. Release must be recorded explicitly in the binding handoff and issue #21. No P4, R4/B3c, graphics integration, ROM, new format, main merge, independent Verification or closing #15.
## 5. Source references
- [THE SKRAUN full original 30-trick audit for upright identity](MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md)
- [TIA original programmer guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html)
- [Historical detailed missile-row art discussion, 2008](https://forums.atariage.com/topic/118687-detailed-missle-sprite-drawing-trick-anyone/)
- [Three-stream display-list/head-body NUSIZ proof of principle (2025)](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html)
