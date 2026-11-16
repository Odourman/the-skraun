# THE SKRAUN — P02-B dynamic playfield halo feasibility plan

**Date:** 2026-11-16
**Status:** Proposed research and bounded technical experiments; **not implemented or verified**.
**Authority:** MAIN design decisions 01–60; P02 general feasibility plan.
**Predecessor:** P02-A P1 experiment, results: https://github.com/Odourman/the-skraun/pull/2 (draft; not for merge).
**P01 independent gate:** https://github.com/Odourman/the-skraun/issues/1 remains OPEN.

## Objective
Test whether a 360-degree halo that moves with the player can use Atari 2600's **playfield** instead of occupying a full player sprite. At level 3, the visible halo must be wider than the 32-logical-pixel troll.

Unlike P02-A, this is a research plan, not a claim of a running solution.

## Confirmed hardware facts vs hypotheses

- TIA playfield uses 20 independently programmable coarse columns in each screen half, **40 columns total** at 4 color clocks per column.
- PF0, PF1 and PF2 encode one half; with asymmetric rendering the right-hand half needs register changes during the scanline. There is no framebuffer.
- Each NTSC scanline allows 76 CPU cycles. In the same time interval the kernel must handle P0 troll and eventually multiple enemy graphics.
- Player0 and player1 remain separate hardware objects if the ring uses the playfield, **but** future obstacle art also depends on PF bandwidth.
- A complete 40-bit-wide by 48-line-high buffer costs 240 bytes before other state: more than the internal 128-byte RAM. This is why an on-the-fly, table-driven or smaller-row-buffer approach should be investigated.

## Test ladder, smallest useful experiments first

| Step | Test | Pass criterion |
| --- | --- | --- |
| B1 | Static 40-cell symmetrical PF ring at one location, no troll | 360-degree outline visibly complete, real Stella NTSC frame remains 262 lines |
| B2 | Center ring of 3 sizes on one P0 troll | Level-3 ring visibly extends beyond the 32px troll on all four sides; no severe missing PF half |
| B3 | Quantized horizontal follow | Halo moves with player; <=2 logical pixel center misalignment due to 4px PF granularity where possible |
| B4 | Vertical follow and FIRE | Ring lasts about 30 frames, follows joystick diagonals, and respects intended cooldowns |
| B5 | Placeholder future gameplay workload | Reserve sprite/object time for two knights, green archer, arrow and simple solid obstacles without misrepresenting flicker |
| B6 | Separate collision model | Eight radial bearing checks plus tests just inside/outside each ring radius, independent of visibility and PF sprites |

## Implementation strategies to compare

1. **Symmetrical PF:** First validate a ring centered at screen x=80 using the playfield's reflection mode. It is insufficient for unrestricted x movement, but serves as a baseline.
2. **Asymmetric PF rewriting:** Dynamically write both PF halves at the correct beam positions, with player X quantized to 4px cells. Measure the cost of six PF register writes and P0 graphical work each active line.
3. **ROM row-mask tables:** Precompute ring outline masks or horizontal spans for radius/row combinations; evaluate ROM and bank mapping rather than allocating a whole screen or a 240-byte row-buffer in 128-byte RAM.
4. **Hybrid PF/object render:** If pure PF cannot coexist with obstacles, compare a hybrid that reserves PF for solid scenery and borrows object raster slots only on the rows carrying halo arcs.

These are experimental directions, not approved final implementation choices.

## Mandatory evidence
- Commit-specific assembler source and exact DASM command, ROM SHA-256 and 4096/8192/16384 byte mapping *as actually used*.
- Actual Stella PNG screenshots at levels 1, 2, 3, near left/right boundaries, and under diagonal movement.
- Measured scanline counts and scanline CPU cycle load in Stella Debugger (not just model outputs).
- A resource table: TIA registers/objects used, RAM bytes, ROM bytes, and approximate highest-cost scanline.
- Explicit comparison against P02-A, including the 32px width and P1 occupancy failures.
- Independent VERIFICATION before promotion into any stable game implementation.

## Stop conditions
- Ring cannot exceed 32px around the level-3 troll at a readable quality.
- Ring and obstacles cannot be drawn in the same scene without unacceptable loss of gameplay.
- Stable NTSC timing or future multiple-actor sprite budget cannot be maintained.
- Implementation requires increasing difficulty to offset level-3 power (disallowed design change).

**Next engineering action:** implement B1 only, in its own experimental branch, while keeping P01 source and ROM unchanged. Escalate to B2+ only on concrete B1 results. Research cannot be used to claim B1 has passed.
