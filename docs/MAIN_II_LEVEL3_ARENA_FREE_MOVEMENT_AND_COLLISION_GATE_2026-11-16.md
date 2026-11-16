# THE SKRAUN — MAIN II: Level-3 Arena Free-Movement and Collision Gate
**2026-11-16 | NEW USER GAMEPLAY-DESIGN REQUIREMENT + ANALYTICAL REFERENCE MODEL | NOT GAME IMPLEMENTATION**

## 1. Direct user decision
> "ok, fortsätt. Tänk på att banorna ska vara så pass fria att spelaren kan röra sig lätt även på nivå 3, utan att krocka och fastna överallt"

**Binding gameplay / usability:** The game's eight layouts MUST remain comfortably traversable, even for the **largest Level 3 Skraun**, with plenty of maneuvering space for fighting, turning, passing obstacles and pursuing knights/archer without repeatedly getting stuck in narrow corridors or corners. The Level-3 upgrade should feel physically more powerful, not turn basic movement into an obstacle puzzle.

This clarifies existing 01–60 decisions; it does not replace them:
- #33 sparse SOLID world obstacles, #54 eight fixed distinct layouts across four worlds, two per world.
- #46 eight movement directions; #47 three visual sprite sizes (now locked to same approved U1-LEG1 source art).
- #55 collision blocks solids but diagonal movement should slide along free edges.
- #34 archer arrows blocked by solids, #36 sword blows blocked, #35 halo PASSES through obstacles.
- #30 safe respawn after death, #52 safe enemy placements, #51 orb fixed prechosen valid positions.
- Level3 keeps existing ability to become OP; NO covert reduced size, damage, reach, cooldown or enemy numbers to circumvent lack of space.

## 2. Grounded state of current development (not a map implementation)
- [Current prototype source](https://github.com/Odourman/the-skraun/blob/main/src/main.asm) implements left/right/up/down joystick motion, bounds and 3 sprite width/height choices **WITHOUT ANY REAL OBSTACLES OR COLLISION**. Its temporary clamps are NOT final gameplay dimensions.
- [R3 MAIN technical handoff](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md) used **three diagnostic synthetic playfield columns** (TIA x56,88,108) ONLY for rendering tests; it expressly has **NO obstacle collision logic**. Its 16-line placeholder HUD + 176-row arena provides a possible diagnostic coordinate basis, **NOT the final approved eight world maps**.
- There are **no eight approved collisionable map obstacle masks** in the reviewed main repo. Therefore NO actual game map can presently be certified Level3 traversable.
- [Approved U1-LEG1 art source](https://github.com/Odourman/the-skraun/tree/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1) remains UNCHANGED; user approved same A/B for L1/L2/L3, only larger, with reversed right/left visual source association. Graphical geometry is **L1 8×12, L2 16×24, L3 32×36** on existing P0 width/repeated-row concept. Actual Stella/TV L3 render and #19 leading-row defect NOT accepted as corrected.
- Global full-scene R3 feasibility NO-GO: 20Hz same-Y enemy sharing, PF halo/obstacle color conflict, 2–4 spare worst-line cycles before arrow/orb/AI/collision. A cheap map checker or pretty diagram does NOT resolve this renderer/CPU bottleneck.

## 3. Binding playability goals for future layouts
1. **Open spaces first.** Each world shall have a distinctive arrangement of a **few compact solids** (trees, rocks, ruins etc.) plus large continuous maneuvering zones. Avoid dense mazes, obligatory bottlenecks, closely stacked obstacles or decorative clutter that visually suggests impassable areas.
2. **Full Level3 route connectivity.** From the agreed player start, all necessary destinations and combat positions must be reachable at **every Level 1/2/3**, and all key regions must be mutually usable by Level3. Reaching one corner with L1 while the same region is trapped behind a narrow Level3-only gap is not good enough.
3. **Upgrade-safety at ALL permitted orb placements.** In the existing mechanics an orb can upgrade L2→L3 on any candidate orb location. A position occupied during an upgrade must not suddenly embed the larger body in a solid obstacle, a wall, or an inaccessible pocket. Make orb spots and approach/recovery regions Level3-safe from design time; don't teleport, postpone an earned upgrade or shrink the graphical body without a separate explicit gameplay decision.
4. **Safe enemy and player spawns.** The Level3 footprint must be able to move around the fixed start, enemy approach lanes and reinforcements, with actual collision and enemy occupancy accounted for. After death, existing L1 respawn rules still hold.
5. **Corner-slide rather than dead stops.** When a diagonal input would collide on one axis, a separately clear orthogonal component should still move. This must NOT permit diagonal phasing through solid obstacle corners. When two obstacles approach, a player can back away and reorient without a sticky 1-pixel wedge.
6. **Collision body != halo.** Halo graphics/range are large and pass through solidity; obstacle collision should be based on actual gameplay collision definition, independent of flicker or PF visual gaps. If a smaller central/foot collision box is proposed to improve feel, its dimensions and perceptual fairness must be reviewed explicitly; do not silently allow apparently impossible wall phasing.
7. **Full game remains 8 distinct maps/4 worlds with genuine solids.** This requirement demands better obstacle positioning, not stripping every map to a blank diagnostic arena.

## 4. Provisional quantitative reference thresholds — NOT final collision canon
For a conservative FIRST planning model, treat the entire visible L3 sprite rectangle as the solid body:
- L1 = 8 × 12 Atari logical X/scanline units
- L2 = 16 × 24
- L3 = **32 × 36**
- Add a **test-only 4-clock horizontal / 4-scanline vertical clearance margin on each side**.
- Reference estimated unambiguous L3 minimum corridor clear space: **40 TIA horizontal color clocks** (32+4+4) for left-to-right movement through a vertical channel, or **44 NTSC scanlines** (36+4+4) for up/down movement through a horizontal gap. A corridor at exactly this minimum can still feel constraining; favor clearly wider routes. **These values are provisional calculation thresholds**, *not measured final collision hitbox or official actual maps*.
- Use **160×176 arena** only to match R3's diagnostic 160-wide/176-row scene after a temporary 16-row HUD. HUD, borders, final collision bounds, perspective, actual TIA-PF object geometry and player hitbox require separate technical selection.
- For signed-off maps, a later test must use the *actual* body collision representation, world bounds and all movable entities, not simply this full visual rectangular proxy. No threshold is enough by itself to prove natural-feeling movement.

## 5. One bounded geometry reference probe actually executed
[Drive evidence archive — source program, exact JSON outputs, README, SHA manifest](https://drive.google.com/file/d/15RqJb_y1ezbCF5L8EFR-ojqmc1z-HPtN/view). **4345 bytes, SHA-256 `69b57fdf1f104e8d11185056dd9994b1c8346d33b35bed8629a9b10cef1da0ad`**, ZIP CRC PASS, three included SHA256 checks PASS; original uploaded file fetched back from Drive and returned exact same bytes/hash.

The Python program `skraun_level3_clearance_probe.py` uses an integer conservative AABB overlap test with independent obstacles and 4-neighbor flood fill (which is sufficient to establish route reachability without assuming diagonal corner tunneling). For each example it logs L1/L2/L3 goal reachability and whether every listed possible orb location can safely contain a full L3 body.

These THREE layouts were **intentionally invented test fixtures ONLY** (not the actual eight maps):
| Fake geometry fixture | L1 reach goal | L2 reach goal | L3 reach goal | Upgrade safe? |
|---|---:|---:|---:|---|
| SPARSE_OPEN_ONLY_SYNTHETIC — 3 small blocks, wide central travel | PASS | PASS | PASS | PASS |
| NARROW_DOOR_ONLY_SYNTHETIC — wall with 20-row passage | PASS | **FAIL** | **FAIL** | no pickup points tested |
| GROWTH_TRAP_ONLY_SYNTHETIC — block beside potential upgrade point | PASS | PASS | PASS | **FAIL at marked pickup** |

Observed reference flood fill accessible top-left positions from test spawn: open example **20,223 L1 / 15,766 L2 / 10,747 L3**. Narrow fixture **18,865 L1 / 7,975 L2 / 5,187 L3**, but goal unreachable at L2/L3. Growth-trap fixture **22,040 L1 / 18,512 L2 / 13,496 L3**; the checked grow-point is illegal at L3.

**What this proves:** a single narrow doorway or orb placed too close to an obstacle can create exact predictable Level3 navigation failures even when movement seems fine in Level1. These failures are detectable BEFORE ROM coding if real map geometry is supplied.
**What this does NOT prove:** 8 maps are complete, actual game collision works, diagonal sliding is implemented, every corner feels good, physical Atari shows these obstacles, or R3 full-scene/CPU constraints are resolved. No actual maps tested.

## 6. Future acceptance test contract
A later separately authorized layout/physics test MUST:
- Load each of the actual **eight fixed canonical map masks**, with recorded coordinate/scale and all solid components; no hand-waved mock rectangles.
- Test L1/L2/L3 with both visual P0 footprint and approved actual collision box, all start positions, all permitted orb placements, realistic enemy/in-flight-object placements and both 4-way and 8-way joystick traces; score start safety, route connectivity, growth legality, corner-slide and non-stuck escape.
- Check more than graph reachability: long narrow corridors, repeated forced turns, fight-space sufficiency, visual readability and alternatives to chokepoints. These may require in-game human feel testing; a flood fill alone is insufficient.
- Recheck the real full-game CPU budget and TIA layering separately; gameplay collision data must never depend on frame alternating obstacle visibility.
- Report individual map PASS/FAIL and worst movement failure traces, not just a percentage or composite green score.

## 7. MAIN II disposition / STOP
**ACCEPTED USER PLAYABILITY PRINCIPLE, not actual Level3 map implementation.** Level3 must be **larger and powerful AND easy to move**, no forced obstacle maze. Preliminary source-only checker and negative test fixtures completed, no production acceptance.
- Tracking [issue #23 – L3 NAVIGATION GATE](https://github.com/Odourman/the-skraun/issues/23) **OPEN**.
- Existing [visual gate #15](https://github.com/Odourman/the-skraun/issues/15) remains OPEN; [ART1 L3 defect #19](https://github.com/Odourman/the-skraun/issues/19) OPEN, independent P01 [#1](https://github.com/Odourman/the-skraun/issues/1) OPEN; R3 NO-GO.
- No new ROM implementation, B3c/R4, ART1 fix, map source replacements, gameplay behavior/code, renderer scheduling, new sprite, merging draft branches or independent VERIFICATION authorized by this report. Any such next step needs a separate specifically bounded order after the necessary source and resource review.
