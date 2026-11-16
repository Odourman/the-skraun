# THE SKRAUN — MAIN TO ROM DEVELOPMENT — P02-R3 DECISIVE SCENE / ENEMY SCHEDULING FEASIBILITY
**Authorized:** 2026-11-16 by MAIN. **Scope:** separate P02-R3 architecture experiment ONLY. **No B3c or production integration, no automatic R4, and no independent VERIFICATION.**

## 0. Evidence authority and frozen baseline

MAIN has reviewed and **accepted P02-R2 as completed bounded ROM DEVELOPMENT self-tests**, not as production renderer approval or independent verification. R2 was performed on `experiment/romdev-r2-two-line-scheduler`; reviewed draft PR [#13](https://github.com/Odourman/the-skraun/pull/13) head `2cb9eafa0f5964e89553f791ff18ea9d9362fe8e`, still **draft/unmerged**. The successful assembled/rendered ROM run [#43912037744](https://github.com/Odourman/the-skraun/actions/runs/43912037744) is commit `47c0309c4929df991a67ef1db3b218e8b0f67a42`; comparison to final PR head shows **only a workflow and report additions**, no changes to the tested 6502 source. [Direct Stella Debugger 16-state run #43911806707](https://github.com/Odourman/the-skraun/actions/runs/43911806707), [final validated package #43913077850](https://github.com/Odourman/the-skraun/actions/runs/43913077850).

Read the exact [R2 MAIN handoff](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r2-two-line-scheduler/docs/ROMDEV_P02_R2_RENDERER_SCHEDULING_MAIN_HANDOFF_2026-11-16.md), [R1 handoff](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r1-renderer-feasibility/docs/ROMDEV_P02_R1_RENDERER_FEASIBILITY_MAIN_HANDOFF_2026-11-16.md), [design decisions 01–60](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), visual authority, and [30-trick relevance audit](https://github.com/Odourman/the-skraun/blob/main/docs/R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md). Check CURRENT GitHub state before starting; these SHA values are provenance of completed R2, not a promise about the future HEAD.

Known facts from R2:
- Actual two-line PF + P0 + one P1: **68/76 worst physical scanline A; 67/76 B**, compared to R1 one-line + P1 **71/76**. Ring image IoU **0.907–0.915** versus baseline; vertical contour is changed.
- Actual P1 NUSIZ1=$04 + time-critical GRP1 rewrite produces two distinct green bitmap silhouettes at the *fixed* 64-color-clock horizontal spacing, with **76/76 worst line, zero margin**. That is NOT two freely positionable enemy sprites.
- Separate 16-row HUD zone demo works; arena worst **64/76 without P1**, NOT proof a loaded HUD+full arena works.
- Gold/blue line interlace is a LIMITED fallback at **74/76**, with exactly **50% gold ring rows** and striped appearance, NOT independent same-pixel layers.
- Hypothetical level-3 ring 48 clocks ×72 rows / four-clock thickness was **only a bounded proxy**. Right PF2 and full intended range remain unproved in an actual ROM.
- A single 262-scanline frame result does not prove worst-case TIA right-half-write deadlines or quality with moving independent enemies. CPU figures above are **static assembler-accounted**, not full measured integrated traces.
- No same-Y three-independent-opponent + arrow + orb + readable obstacles/halo has passed. R2 has **not proven that all possible TIA approaches are impossible**.

MAIN's design is unchanged: P0 gray overhead Skraun, level-3 halo larger/thicker than level-3 body, 2 knights + 1 green archer simultaneously, one arrow in flight, collectible orb, solid visible obstacles through which halo passes, and a readable score/lives HUD. Avoid constant distracting flicker. Gameplay collision truth must NOT be inferred from PF pixels or flicker.

## 1. Purpose of R3 (decisive bounded gate)

Test whether a realistic **original-compatible TIA/6507 architecture** can reconcile those scene requirements by **scheduled P1 reuse and carefully bounded visual compromises** instead of demanding all objects on one scanline in one unschedulable kernel.

Do NOT just further micro-optimize the 68-cycle line-pair kernel or repeat the known 76/76 fixed-distance dual-copy demonstration. R3's output must be a **clear go/no-go architecture decision for MAIN**, or a quantifiable hardware/design trade-off. A credible failing result is a successful research deliverable.

Build at most **2–3 targeted, real 4K NTSC diagnostics** (a separate research-only mapper comparison is permitted only if strictly necessary to prove data size, never claimed to add raster cycles). Work in a NEW dedicated experiment branch/draft PR, not `main`. Do not merge prior drafts.

## 2. R3-A: independently located enemy scheduling under real render load

Develop one bounded diagnostic with **three independent in-memory enemy positions and three distinct visible identities**, representing two knights and one archer, but **NO AI**. Provide deterministic selected test layouts with:
- different Y bands (easy vertical reuse),
- two enemies whose Y ranges partly overlap,
- all three overlapping in Y with **independent, non-fixed X positions**, including left/middle/right and P0 occlusion/reversal,
- independent player motion (at least retained horizontal diagnostic joystick test) and fixed playfield obstacles + visible ring in the same arena.

Attempt P1 scheduling/multiplex per Y zone when possible; for unavoidable same-Y conflict, evaluate **limited frame-to-frame rotation of the single P1 slot**, ideally only when overlap occurs. Keep each enemy's logical X/Y stable regardless of which frames draw it. Do NOT fake multiple independent actors by relying on NUSIZ's fixed 64-clock copies or changing actual AI/game design to force enemy rows apart.

Measure per-enemy on-screen visibility/duty cycle for every scenario (e.g. 60Hz when alone, perhaps 30Hz when two compete, 20Hz if three rotate), deterministic frame captures (not just one PNG), readability/outline/color persistence, visible tearing, and code/scheduler overhead. Do not silently call 20Hz or disturbing flicker production-acceptable: it is an explicit aesthetic **FAIL/RISK** that MAIN may reject. If a better original-TIA scheduling scheme exists, compare it with this transparent fallback.

Explicitly reserve time and object allocation for **one arrow** (M0/M1 if appropriate) and **one orb** (BL or another object) with correct TIA color sharing and priority. Attempt a real minimal static-symbol display of these if feasible, otherwise provide costed lower bounds and NOT TESTED, never assert actual coexistence.

## 3. R3-B: scene-preserving halo and ACTUAL level-3 reach

Create at least one real diagnostic of the larger level-3 P0 and a **genuinely wider/thicker level-3 ring** (the 48-clock×72-row proxy is a possible stress hypothesis, not binding final design) at center and near both horizontal extremes. The ring may follow the existing diagnostic SWCHA horizontal grid; **full B3c vertical/freely attack-triggered gameplay is explicitly excluded**.

- Exercise right PF2 if the ring extends past x120/128 and any other currently omitted PF group. Do not artificially constrain Skraun's permanent playable X to keep tests easy.
- Display at least two visible obstacles under/through the ring's occupied scanlines, without making the geometry of those solid obstacles ambiguous to a typical player where possible.
- Compare at most two concrete visualization approaches worth testing in R3: e.g. a scene-first PF with short-lived halo overlay/alternating frames, bounded two-line/color/pattern treatment, sparse PF writes, a genuinely budgeted missile/ball hybrid. Do not repeat R2's already-rejected striped 50%-gold technique as if it were new. Record which changes preserve distinct colors/contours and which cannot simultaneously represent ring and scenery at the same TIA PF pixel.
- If alternating-frame rendering is considered, capture a **consecutive-frame sequence** and report 30/20Hz duty, hue/brightness, skipped obstacles, line artifact and readability. An isolated screenshot cannot establish flicker acceptability.
- Maintain collision semantics independently of display: obstacles solid, magic passes through them; implementing collision/AI is outside R3.

If this cannot be done with usable legibility and safe raster time while P1 must support independently located enemies, **report a genuine architecture conflict**, including exactly which hardware resource cannot be shared. Do not weaken level-3 power/reach or decide on a visual redesign without MAIN.

## 4. R3-C: true worst-case timing and region-budget decision

Measure/calculate with explicit paths for the strongest 1–2 R3 candidates:
- Worst physical scanline cycle counts in unloaded vs same-Y P0+halo+obstacle+enemy(s), with page crossings, branch paths, frame-level scheduler costs in VBLANK/overscan, mandatory PF register deadlines including right PF2, and remaining cycles after minimal missile/ball draw.
- Actual Stella Debugger 262-line timing at center/edge/reversal and selected frame-alternation patterns, along with any direct cycle traces available. Distinguish **STATIC CALCULATED**, **DIRECT DEBUGGER OBSERVED**, and **NOT TESTED**.
- TIA resource ledger for P0, P1, M0/M1, BL and PF, dynamic display limits, realistic 128-byte RAM allocation for three enemy X/Y/state, Skraun, orb, projectile and priority scheduler (not just the original 10-byte diagnostic), ROM data growth for 8 distinct obstacle maps, all 3 troll/ring levels and candidate 4K/banked size requirements.
- Separate HUD region must be accounted for without claiming it frees cycles on overloaded arena scanlines.
- Keep specific measured frame-visibility duty, 1–2-frame joystick responsiveness and genuine alignment between ring and P0 in playfield units.

**Success criterion is NOT unconditional 60Hz simultaneous three independent enemy sprites on one physical row.** The criterion is a clearly documented, **visually acceptable** resource-scheduled approximation that keeps fixed mechanics and physical console compatibility, or precise failure evidence. Production visual acceptability is not finally decided by ROM DEVELOPMENT alone.

## 5. Stop conditions and MAIN decision

Use a bounded experiment count, then stop instead of starting an unending R4 optimization loop. The final handoff must answer:

1. Is there an architecture which demonstrably leaves a plausible CPU/TIA budget for **P0 + visible obstacles + moving level-3 halo + three independent enemy positions + one arrow + one orb + HUD** under worst overlap, using measured actual or openly identified approximate frame scheduling?
2. How often and how visibly must enemies, obstacles or halo flicker/alternate at NTSC 60Hz? Is this plausibly compatible with decision 59's readability goal, or must MAIN choose between gameplay legibility, cartridge hardware or adjusted visual presentation?
3. Which exact requirements remain **PASS (bounded) / FAIL / BLOCKED / NOT TESTED**, and which would need a separate production implementation step?

If R3 evidence says **NO credible path without a gameplay/visual/hardware change**, stop and elevate the concrete choice to MAIN, with 2–3 quantified alternatives. Do **not** self-authorize R4, B3c, DPC/ARM/cartridge cutover or a redesign.

No full game AI, real enemy pursuit, melee/projectile physics, 0.5s FIRE/cooldown, power-up gameplay, permanent world layouts, full score/health, PAL, mainline merge or independent VERIFICATION. R3 is **engineering proof of feasibility only**, not implementation of the full game. VERIFICATION remains dormant; continue developer DASM/Stella and source-snapshot self-tests.

## 6. Hand-off package required

At R3 completion submit one consolidated report to MAIN containing exact baseline/branch/commit, built ROMs SHA256, source+test commands, authentic Stella game frames and debugger evidence, worst cycle ledger, RAM/ROM ledger, per-enemy *measured on-screen duty/independent X/Y*, level-3 ring shape/visibility, projectile/orb reservations, rejected candidates, and an explicit recommendation for MAIN. Keep draft PR unmerged. No separate incremental report or independent verification requested.
