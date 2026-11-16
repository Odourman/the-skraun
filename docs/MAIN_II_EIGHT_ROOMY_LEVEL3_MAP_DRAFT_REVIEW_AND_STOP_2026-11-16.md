# THE SKRAUN — MAIN II: 8 roomy Level3 draft arenas, source-only comparison and disposition
**2026-11-16 | MAIN II DESIGN STUDY COMPLETED | NOT CANONICAL MAPS / NOT STELLA / NOT ROM / NOT VERIFICATION**

## Background and authority
The user explicitly asked MAIN II to continue after binding the Level3 navigation requirement that **even Level3 Skraun must be easy to control with enough wide empty room to avoid hitting/sticking on obstacles**. This follows [the prior MAIN II navigation design gate](MAIN_II_LEVEL3_ARENA_FREE_MOVEMENT_AND_COLLISION_GATE_2026-11-16.md) and [design decisions 01–60](DESIGN_DECISIONS_01-60_2026-11-16.md), particularly #33,#34–37,#46–47,#51–55.

**Important authority distinction:** these eight are freshly authored **candidate layout sketches** to support the next design choice. They are NOT eight already existing canonical or playable maps. The original main repo contains no integrated eight maps with collision or true enemy AI, and R3 only renders a few synthetically placed PF pillars without physics.

## Delivered and independently checked
- **Self-contained source ZIP:** [Google Drive THE_SKRAUN_EIGHT_OPEN_ARENAS_SOURCE_STUDY_2026-11-16.zip](https://drive.google.com/file/d/1MePHLlCFKRD07kibk9qoUKmw8Ea9jTQC/view), **128926 bytes**, exact SHA256 **`686ff1f22298ccac812d0b526869707e2661649c9f6fb7e8e4ac93cd00b517ee`**. ZIP CRC PASS, 23 archive members, **22/22 SHA256SUMS** PASS. **Actually uploaded then downloaded from Google Drive**, compared bytes and SHA256 against original — exact PASS.
- **Reproduction:** Python source and frozen original approved U1-LEG1 source included. In CLEAN directory re-run validation, 40×22 mask generation, all eleven PNG previews, detailed sprite/pixel authenticity check and deterministic ZIP packaging: **24/24 resulting files (including final ZIP) byte-for-byte identical** to original.
- **Separate GitHub draft branch:** [design/l3-eight-open-arena-drafts-20261116/design/l3_eight_open_arenas_20261116](https://github.com/Odourman/the-skraun/tree/design/l3-eight-open-arena-drafts-20261116/design/l3_eight_open_arenas_20261116), with readable source coordinate/index, study report and ZIP link, strictly unmerged. Complete reproducible images/program/masks are in Drive ZIP.
- Frozen pixel art: U1-LEG1 original approved 8×12 source exactly, Level3 displayed at conceptual **P0 4x horizontal × row 3x vertical**, future visual RIGHT = original source mirrored LEFT. No modifications to sprite or game canon.
- All colours and thematic square blocks are **diagnostic illustration concepts only**, not chosen final four-world palettes nor proven TIA shapes.

## Eight draft maps and exact results

| Draft ID | World / readable name | Rectangular obstacles | L3 legal centre positions | Proportion vs clear arena | Extra double-margin stress |
|---|---|---:|---:|---:|---:|
| F01 | Forest, Öppen glänta | 3 | 11421 | 70.97% | 66.92% |
| F02 | Forest, Skogsbryn | 3 | 12797 | 79.52% | 76.67% |
| M03 | Mountain, Stenfält | 3 | 12413 | 77.13% | 70.32% |
| M04 | Mountain, Bruten mur | 3 | 12929 | 80.34% | 76.47% |
| D05 | Dream, Fyra ruiner | 4 | 11453 | 71.17% | 67.15% |
| D06 | Dream, Drömport | 3 | 12093 | 75.14% | 68.06% |
| N07 | Night, Skuggmurar | 3 | 11549 | 71.76% | 67.83% |
| N08 | Night, Nattglänta | 4 | 11453 | 71.17% | 67.15% |

All eight have distinct L3 legal centre position SHA256 masks even where counts coincide. 160×176 screen below 16 diagnostic placeholder HUD; actor is **center anchored only in analytical model**, full L1 8×12/L2 16×24/L3 32×36 visual bounding box is conservatively treated as collision body, plus 4 color-clock/scanline clearance on every side. This is NOT yet the selected real hitbox or scene bounding box.

Tests performed:
1. All eight layouts have **100% of physically legal actor-center positions** reachable from candidate start by 4-neighbour flood fill at all three sizes. Four preselected mid-arena checkpoints are accessible at every level, not a handful of disconnected passages.
2. At least **70%** of legal Level3 actor-center positions compared with the unobstructed reference rectangle remain, with only 3–4 obstacle blocks. This is **area of valid actor CENTRES**, NOT 70–80% of floor pixel cells or proof of human ease.
3. All Level3 legal regions remain connected with **double clearance buffer (8 each side)**, with at least 65% actor-center positions remaining in this more conservative alternative.
4. Two **alternative orb candidates** for each map (one real orb per visited stage still applies): for **every reachable Level1 or Level2 player-center coordinate whose actual body overlaps an illustrative 8×8 orb**, immediate upgrade at the SAME coordinate to the next full-body size remains solid-free and inside arena. Both L1→L2 and L2→L3 possible pickups PASS; no invented teleport or delayed growth.
5. All eight possible joystick move directions were evaluated from **every Level3 legal actor-center coordinate** under an axis-slide toy rule (whole diagonal if possible, else X alone or Y alone, else stop). Result always within legal centres, some actual slide instances present. This tests only the reference implementation, **not 6507 code or real physical corner feel**.
6. 40×22 conceptual TIA-PF-aligned 0/1 solid occupancy strings exactly roundtrip every rectangle at native source pixel coordinates. **No real PF0/PF1/PF2 write scheduling or halo coexistence is proven**.
7. Negative controls correctly detect one deliberately too-narrow Level3 passage and **248** illegal Level2→Level3 collision growth contact positions around a deliberately badly positioned orb.

## Design judgement / negative findings
The eight sketches adequately embody the *spacious navigation intention* under one conservative box model, leaving the middle mainly clear for fighting and presenting some world-side solids. HOWEVER they are **not yet artistically distinct enough as final themed environments**: simple coloured rectangles are only placeholders, not convincing forest/mountain/dream/night shapes. Gameplay enemy lines of sight, reinforcements, corner fights, sword/blocking, escape behavior of archer, projectile trajectories, halo passing obstacles, actual game HUD boundaries and full original-compatible TIA frame resource budget were not solved here.

The biggest physical blocker remains **R3 NO-GO** for tested full arena renderer: 20Hz per competing same-Y enemies, 30/30Hz halo/obstacle or merged-color compromise, only 2–4 cycles/scanline spare before real arrow/orb/AI/collision. More spacious maps improve gameplay concept but **do not change 76 cycles/scanline or add PF layers**. The level3 extra full-width top scanline ART1 defect [#19](https://github.com/Odourman/the-skraun/issues/19) is still OPEN, and x4/y3 conceptual enlargement is not true uniform proportion scaling.

## MAIN II ruling and next responsible gate
**ACCEPTED as a complete, reproducible DRAFT source-only geometry study; NOT canonical map art or production collision acceptance.** Retain [Issue #23](https://github.com/Odourman/the-skraun/issues/23) OPEN. [#15](https://github.com/Odourman/the-skraun/issues/15) full visual gate OPEN, [#19](https://github.com/Odourman/the-skraun/issues/19) ART1 unresolved, [#1](https://github.com/Odourman/the-skraun/issues/1) independent P01 OPEN; R3 NO-GO unchanged. No new ROM, B3c/R4, ART1 repair, gameplay integration, 8-map canon promotion, main-merge or independent VERIFICATION authorized.

The next separate gated decision, when MAIN initiates it, should confirm actual actor collision footprint/anchor and final map-area/HUD bounds vs the approved U1-LEG1 3 sizes, obtain four-world recognizable obstacle art and run real same-Y/halo/CPU feasibility before attempting gameplay collision engine. The user's fundamental preference is not negotiable: **Level3 must be able to maneuver easily even at its visually large size.**
