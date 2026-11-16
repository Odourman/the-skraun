# THE SKRAUN — MAIN TO ROM DEVELOPMENT: P01-ART1 SINGLE-PLAYER STELLA VISUAL READOUT
**AUTHORIZATION ISSUED 2026-11-16 — new separate scope, deliberately NOT R4 or B3c.**  
**A narrowly isolated P0 pixel-art/perceptual proof only.** No full renderer, no gameplay or new graphic decisions.

## 0. Read before any coding
1. [MAIN P1 graphics disposition](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_GRAPHICS_P1_HORIZONTAL_AXIS_REVIEW_AND_DECISION_2026-11-16.md): GRAPHICS P1 accepted as source, horizontal A preferred as test candidate, not as finished Skraun.
2. [P1 exact source / A/B/Q1 bitmaps](https://github.com/Odourman/the-skraun/tree/graphics/p1-horizontal-axis-perspective-proof-20261116/graphics/skraun_p1_horizontal_axis). Source branch reviewed SHA `b5bc31a3485faf67199631c01768bf221f061292`; use the **exact** JSON masks rather than inventing/lookalike redrawn silhouettes.
3. [P1 GRAPHICS archive](https://drive.google.com/file/d/1ouk4vL_gBVcb3Jc_-EP5UKSQLV1mEaSC/view), externally checked ZIP SHA256 `d716e93cf6f15f5944fb9716efffd1217d2c716dbc3909906c2ba382aa728cd1`; 15 entries, 14/14 manifest PASS. **PNG/GIF are art previews, not Stella.**
4. [MAIN design decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [visual direction](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md) and [old row-order/orientation audit](https://github.com/Odourman/the-skraun/blob/main/docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md). Read real current source before modification.
5. A known functional isolated gray-player hardware reference exists on `experiment/gray-topdown-skraun` at `experiments/p01_skraun_gray_topdown.asm`. **Use as technical inspiration and verify its actual assembler logic, not its old frontal artwork or old orientation assertions as authority for new horizontal bodies.**
6. [P01-R3 original renderer technical NO-GO, separate](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md). Full-scene feasibility is NOT the subject of P01-ART1.

## 1. Question to answer

**Can a light-gray 8×12 horizontal-body Skraun be visibly readable, consistently facing left/right and recognizably four-legged in actual NTSC Stella at 3 levels, and does the 2-pose walk look like locomotion rather than a flashing bug?**

Compare **only**:
- P1 **A_rounded_back** = primary test silhouette.
- P1 **B_low_long_back** = one alternate to test a different body/back line.
- v0.3 **Q1_splayed_quad** = fixed negative/control comparison, previous front-facing anatomy.

**Do NOT expand into P1 C/D, new sketched graphics, 8×14, three new extra sprite facings, enemies, game objects or full engine.** The user has NOT accepted any final character form or a loss of original ears/horns/eyes/mouth identity.

## 2. Exact authorized implementation

- Create a **new experiment-only GitHub branch**, suggested `experiment/romdev-p01-art1-p0-stella-readout`; draft PR, never merge to `main`, do not modify the frozen P1 graphics source or historical R3/ R3-VFIX evidence.
- Build **up to 3 authentic 4096-byte NTSC diagnostic ROMs with DASM**, one for each *existing* A/B/Q1 exact bitmap, or fewer ROMs using a deterministic in-ROM test-mode selector if that is clearly simpler. **No new mapper, no SC/ARM/DPC.**
- Each candidate must demonstrate the same exact reproducible state matrix: **3 scaled P0 sizes** at baseline 8 color clocks×12 scanlines, 16×24, 32×36; **2 A/B animation poses**; **both right-facing and left-facing with exact horizontal row-wise mirror**. Fixed centered visible player and optional documented fixed horizontal offsets; **no requirement for actual 8-way joystick, AI or fire physics**.
- Playfield must be blank/single flat dark reference background, optionally two simple fixed forest/night background colors so gray contrast is examined. **No gold halo, no enemy sprites, no obstacles, no projectile/orb/HUD and no gameplay/score.** Do not claim full-game overlap performance based on isolated P0.
- Produce actual **consecutive frame** Stella captures to show A/B animation cadence under one or more *clearly stated* diagnostic frame periods; distinguish this from natural game movement. Capture a static sheet for all 3 levels × 2 poses × 2 facings × 3 candidates = 36 visual states (can use automation and an appropriate documented subset of 262-line debugger traces).
- Use the console's actual NTSC TIA pixel rendering; in reports show *real emulator source image* plus 4:3 nearest-neighbor aspect reference. No AI concept art or mockup may be labeled Stella.
- Ensure source top-to-bottom physical scanline order is correct in the chosen 6507 raster, regardless of whether source data stored top-first or bottom-first. In new A/B **head is to the right for right-facing, left for left-facing**, and there are two upper/lower fore/rear paw stations. The old R3-VFIX regression's "head at top" is ONLY valid for its old frozen vertical bitmap; keep it intact and write **new per-candidate semantic head-x and paw orientation tests** for ART1. For Q1 reference use its original top-head semantic contract.
- Verify no unexpected vertical flip, no FINE position drift, no silent clipping at center or near a meaningful edge; record orientation and mirror pixel-by-pixel from *actual captured P0 component* (not only projected JSON or rendered source masks). Detect regression when one bitmap is purposefully inverted or wrong-facing where possible.
- Full NTSC frame length **262 scanlines** for representative states. Provide DASM `.lst`, `.sym`, static worst visible scanline cycles from code, plus debugger counts where feasible; never conflate calculated and measured. State RAM/ROM use and any color-register/NUSIZ assumptions. This is only a P0 visualization baseline, not headroom proof for R3's full playfield renderer.
- Compare the actual original-sized display at level1: **does A look more like a turtle/beetle than Skraun?** Does B read like an insect? Can one perceive left vs right from the snout/eye-holes alone? Do animations look like leg motion or simply alternating flicker? If the original character's *identity* remains missing, report **NO ART IDENTITY PASS** even if all hardware assertions pass. User/MAIN decides aesthetic approval, not ROM DEVELOPMENT.

## 3. What an actual PASS means

Separate:
- **Technical PASS** if DASM+Stella images truly show the exact right bitmap/mirror, 3 sizes, 2 poses and 262 NTSC timing without orientation or visible-geometry bugs.
- **Visual perception observation** (developer may compare, but no final artistic PASS): leg count, head side, resemblance to original troll vs turtle/insect, distinct poses, readability at real size and motion.
- **Full-game renderer status remains BLOCKED** under prior R3 tests. ART1 must not claim three independently placed knights/archer + arrow/orb, gold halo/solid obstacle coexistence, real gameplay UI, or a solution to 2–4 raster cycles.

The key question is whether **A is a plausible *engineerable presentation baseline*** for later MAIN design approval, not whether the complete game works.

## 4. Test/artifact package and stop conditions

Deliver **one consolidated reproducible package** with 1–3 actual NTSC ROMs SHA256 and bytes, exact source and commands, per-frame Stella captures + frame-sequence/gif if useful (mark any generated animation faithfully as compiled original capture frames), controlled per-P0-component pixel assertions for A/B/Q1, 262-line evidence, cycle/RAM/ROM ledgers, portrait/mirror tests and honest qualitative notes. Include all 36 logical source/pose/level/facing combinations (via actual captures or explicitly identify gaps); no hidden PASS claims for untested states.

Keep an isolated draft PR and original R3 evidence intact; if no sprite reads acceptably as Skraun in real Stella, state NO-GO for final art and **STOP**, handing the visual trade-off back to MAIN. Do not attempt more pixel revisions in the ROM team.

**P01-ART1 finishes after one reported test package. No automatic P01-ART2, R4, B3c, new sprite/arena hardware decisions, graphic canon edits, live gameplay implementation, merges, independent VERIFICATION or closing issue #15.**
