# THE SKRAUN — MAIN: GRAPHICS v0.2 REVIEW AND v0.3 READABILITY GATE
**Issued 2026-11-16.**
**Authority:** MAIN, continuing the standing GRAPHICS-only mandate. **THIS IS NOT ROM DEVELOPMENT AUTHORIZATION.**
**Status:** GRAPHICS v0.2 **accepted as a reproducible exploratory art delivery**, not FINAL art, approved gameplay reach, running Stella integration or an independent VERIFICATION PASS.

## 0. Verified evidence and provenance

MAIN retrieved the actual [GRAPHICS v0.2 Drive ZIP](https://drive.google.com/file/d/13lmZX_SbFm27fceYJuE0DdYiZhO7U2q_/view) from the project visual reference folder, and independently rechecked:
- ZIP size **314,330 bytes**, SHA-256 **17227108204134d2fc3cb3dccad69f7633d8d092dd824aa6172bd88c09e9f9ff**, exact match to reported value.
- ZIP successfully opened: **20 central-directory entries**, **19 covered by SHA256SUMS.txt**. All 19 internal file digests match. Source bitmap checker **PASS** in isolated inspection.
- ZIP contains **eight genuine design PNGs, two 2-frame GIFs, source JSON, two graphics data `.inc` files, validation script, memo, README and manifest**. The images are **pixel-art previews, NOT Stella screenshots**.
- Source GitHub branch: [`graphics/skraun-v0-2-refinement-20261116/graphics/skraun_v0_2`](https://github.com/Odourman/the-skraun/tree/graphics/skraun-v0-2-refinement-20261116/graphics/skraun_v0_2), reviewed HEAD `e43cac9ed84a46dad2729117d6de0355353e8a46`. Source files were read, as well as the actual images.
- Prior MAIN [v0.2 scope](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_V0_2_VISUAL_REFINEMENT_2026-11-16.md), binding [visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md), [decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), user-owned original private Drive sketch, [open issue #15](https://github.com/Odourman/the-skraun/issues/15).

**MAIN verdict:** GRAPHICS met v0.2's **delivery and source-quality obligations**; no need to resend v0.2. Artistic suitability for game is **not passed**.

## 1. Specific visual review findings from actual source and image previews

### Skraun
- **C-overhead is preferable to v0.1 C and C-refined as the next *working* graphics base.** Its trunk/back is more continuous and front limbs are spread. Preserve C-refined as fallback for sketch personality.
- All remain recognizably **front-facing humanoid/ghost-like**, especially at large level-3 scale; 8×12 makes four-legged top-down identity very difficult. Original user instruction demands **camera from directly overhead**. Do NOT approve C-overhead as final yet.
- Candidate C-overhead A/B differ in precisely **6 bitmap cell flips**, concentrated at logical rows 5, 6, 10. C-refined A/B differ by **10 bitmap cell flips**; visual motion in a 2-frame GIF may be too subtle at true level-1 TV size despite source tests PASS. Actual leg/foreleg articulation is more important than satisfying a bit-difference count.
- Current levels use 8/16/32 color-clock sprite width and 12/24/36 scanlines height via scaling, not an approved final artistic shape; 3-level anatomy should remain coherent. Logical top-first ordering and mirror are valid art-source properties; no Stella P0 orientation signoff.

### Enemy sprites
- **Knight warning vs idle:** exactly **4 pixel bits differ**, one at the rightmost column in each of top four rows. This is effectively a vertical line addition, not yet a conspicuous anticipatory sword-swing silhouette at actual size.
- **Archer draw vs idle:** exactly **2 pixel bits differ**, both on a single row; a viewer cannot reliably infer bow draw from that alone.
- More fundamentally, both current enemy sprites resemble **little upright/front-facing humanoids**, not a matching **top-down arena view**. Enemies must be visually compatible with overhead Skraun, while their sword and bow remain recognizable.
- Green is binding for archer, knight colors are proposals only. Avoid final approval by color label alone. Distinct independently placed knights + archer are not technically demonstrated by these static 8×12 masks.

### Worlds
- All eight `40×24` PF masks are mathematically mirrored and are plausible **static constrained PF source mockups**.
- But visual scene PNG `05_4_VARLDAR_8_PF_LAYOUTER.png` shows the four themes share similar isolated blocks / T-columns, with world identity mostly conveyed through color and placement. Forest has recognizable tree-like T shapes; mountain looks like stepped blocks; dream uses T-pillars similar to forest; night has U-like ruins. At natural size, the designs are **too generic for final thematic approval**.
- Screens are mockups layering P0, archer and knight independently, **not real same-Y renderer evidence**. Preserve gameplay visibility as first priority, modest scene elaboration second.

### Gold halo
- Original v0.1 art Level 3 = **88 color-clocks ×176 lines** (91.7% of 192-line arena); clip near edge. v0.2 corrects this identification.
- Alternative A compact footprints (L1/L2/L3): **48×48 / 72×64 / 96×80** (color-clocks × scanlines).
- Alternative B dramatic: **64×64 / 96×96 / 128×112**.
- These alternative PF silhouettes are **too horizontally elongated in the supplied 4:3 approximation** to look like 360° circles. Using the package's approximate pixel aspect of **1 color-clock ≈1.6 physical vertical scanline-units**, visual aspect should be evaluated as `1.6 × color_clock_width / scanline_height`. This gives A level3 ≈**1.92**, B level3 ≈**1.83** (wide ovals), original v0.1 level3 ≈**0.80** (tall ellipse). Target a visually circular outline at the intended NTSC display aspect, NOT naïve equality of logical x/y units. Real CRT scaling remains a later test/uncertainty.
- **No ring radius / power / cooldown / collision geometry is approved or modified** by visual comparisons. The historical R3 48-color-clock ×72-line level-3 diagnostic is a different feasibility experiment, not a gameplay authority. Same-PF-pixel ring/obstacle separate colors remain an unsolved hardware problem.

## 2. SINGLE NEXT GRAPHICS WORK PACKAGE: v0.3 FINAL READABILITY REFINEMENT

GRAPHICS remains authorized to iterate *design data and visual mockups only*. This v0.3 should be a compact **decision-ready** package, not an uncontrolled multi-version art-production series.

### 2A. Overhead anatomy gate – player

- Start from **C-overhead** (recommended base), compare with **C-refined fallback** and the user's original anatomy.
- Produce **two serious overhead-design attempts** rather than near-duplicates. Make the body direction and four limbs convincingly quadrupedal at 8×12. Prefer **less frontal eye/mouth emphasis** and leg/arm arrangement, but preserve ears/horns/two eyes and the original character's charm. Do not alter camera or game design.
- Two A/B walk poses, exact horizontal mirror for each, level1/2/3 previews at native approximate aspect, enlarged pixel boards and black-only silhouette boards. Show **consecutive** A/B frames and annotate precisely which forelimbs and hindlimbs swing. Compare legibility at level1, not solely big level3.
- If no usable four-legged overhead character can be depicted at 8×12, say so with evidence and show ONE separate **nonproduction dimensional thought experiment** (e.g. 8×14) clearly labelled **not approved, ROM/timing change necessary**. Do NOT silently increase production art dimensions.

### 2B. Combat warnings – topdown knight and green bow archer

- For knights, provide clear **overhead** 8-bit sword-bearing idle + genuinely discernible **raised sword/attack warning** silhouette; require a difference that remains recognizable at 160-wide screen scale in 2-frame alternation, not merely increment a single pixel column. Show exact bitmap source/changed rows.
- For green archer, preserve overhead and distinct curved bow/forearm, provide idle and bow-draw; show even in grayscale and against forest green, ensuring the shoot warning remains visible in actual game-size previews. If the 8-bit width is truly insufficient, separately demonstrate a documented static alternative and mark its hardware cost and decision need, no fabricated extra P1/TIA resources.
- Compare knight, archer and Skraun simultaneously only as **clearly labelled conceptual superpositions**; current R3 20Hz same-Y and PF halo/scenery competition are NOT solved.

### 2C. World identity at PF budget

- Keep **two sparse PF layouts per world** (8 total) and the 40×24 + 8-scanline bands as baseline; use recognizable *shape language* that survives grayscale: e.g. forest tree mass and stumps, mountain irregular stepped rock silhouettes, dream asymmetric/strange looping structures only when representable with PF restrictions, night walls/ruins.
- Show all worlds in **monochrome alongside color**; if mirroring prevents sufficient distinction, report it as an explicit representational trade-off, do not claim arbitrary independent 40-cell left/right control without new kernel.
- Prioritize playable open space, a visible light-gray Skraun, green archer, potential arrow and gold ring. No invented final eight world backgrounds.

### 2D. ONE round-looking halo art family

- Draw **one** proportionally round-looking (display-aspect corrected, not physically perfect TIA CRT) three-level halo family with increasing apparent reach and thickness at logical 40 PF columns and explicit band heights. Target near-circle within a stated tolerance (suggest ±15% shape aspect on approximate 4:3 view).
- Compare against v0.2 A, B and v0.1 L3 in the same scale. Include center and all four edge clipping examples and the larger level-3 P0 body with obstacles.
- Show mask width in color clocks, height in scanlines, apparent physical ratio with `1cc≈1.6 scanline-units`, approximate clipping %, left/right PF symmetry, caveats. Do NOT set gameplay collision radius or rewrite decided 0.5s/1s/cooldown mechanics. If art ring/hinder overlap cannot show independent PF colors, mark unmistakably **UNRESOLVED**.

### 2E. Deliverable and stop

- One **complete accessible** versioned ZIP with independent source PNGs, 2-pose GIF or a sequential-frame strip, JSON, `.inc` graphics-only tables, manifest & SHA-256, validator, descriptive README + decision memo. Upload to graphics Drive folder; link exact file. Mirror **text data** to dedicated graphics GitHub branch; original user photo stays private and out of ZIP/public repository.
- Independently validate candidate pixel dimensions, mirror, orientation, distinguishable pose changes, PF shapes/mirror, ring footprint and file/manifest integrity; clearly distinguish **pixel-art preview** from **authentic Stella**.
- Stop at the decision gate. Report 2 overhead player attempts, improved knight warning, improved archer bow draw, world identity comparisons, round visual halo, the remaining **hard technical blockers** and a clear recommendation to MAIN.
- Do not drift into indefinite v0.4/v0.5. If v0.3 art still not convincing at 8×12, submit that negative conclusion and one quantified alternative to MAIN. **MAIN chooses** whether to accept/relax visual constraints or issue a separate isolated ROM art readout.

## 3. Strict boundaries

**No mainline/ROM changes**; no replacement of live `src/main.asm` or production assets; no R4, B3c, AI, gameplay attack/collision changes, enemy slot rendering, cartridge mapper change, three-level gameplay radius decision or independent VERIFICATION. **Do not close issue #15**. C-overhead is a **candidate only**, not a canon silhouette. Artistically correct static preview is not a proven runtime color, alignment, cycle or flicker PASS.

MAIN will decide final visual direction *only* from the next evidence-backed comparison; ROM DEVELOPMENT remains inactive until independently authorized scope.
