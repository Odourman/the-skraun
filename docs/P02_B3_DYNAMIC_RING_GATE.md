# The Skraun — P02-B3 dynamic playfield halo engineering gate

Status: **proposal only**, no B3 ROM or verified implementation.
Depends on: P02-B2 combined static troll+playfield evidence; keep P01 independent verification open.
Design authority: The Skraun MAIN decisions 01–60, especially 01–04, 11–12, 35 and 47–50.

## The real difficulty that B1 and B2 deliberately avoid

B1 and B2 set `CTRLPF=1`, which mirrors the left half about the **fixed screen center**, x=80 TIA color clocks. The ring's center therefore cannot follow a troll moving left/right just by changing its center coordinate: the reflected playfield itself always remains symmetric around x=80.

For a truly moving halo, we must draw arbitrary 40-column bit patterns in both halves. The kernel needs timely PF0/PF1/PF2 writes for the left side, and a second set of writes during the scanline for the right side (when using asymmetric mode). These writes compete with GRP0 updates for the troll, eventual sprite multiplexing for knights and archer, obstacles, and scanline CPU time.

## B3 smallest credible test

1. **B3a: single level, three horizontal ring positions only**. Freeze Y and level 2; move circle center to x=56, 80, 104 color clocks using a debug SELECT button. Proof must show both halves of a continuous ring, at identical size, without forcing 2× frame flicker. Use independent ROM mask data for each position as a first isolated feasibility test; do not yet claim a dynamic transformation algorithm.
2. **B3b: per-four-clock horizontal joystick movement**. Replace three precomputed positions with an efficient 4-clock stepping method. Quantify RAM usage and nonzero PF register writes per scanline.
3. **B3c: diagonal movement and three scales**. Add moving troll, 30-frame FIRE, width/height scaling with level. The ring must follow at the same speed with no significant lag.
4. **B3d: synthetic multiple-actor load**. Reserve enough headroom for two knights, one archer and one arrow, test sprites at overlapping Y ranges and annotate flicker.
5. **B3e: independent collision field**. Keep halo damage radius in game logic, never use the PF visual bitmaps as collision truth.

## Measurable pass conditions

- Three B3a center positions are proven with **actual Stella screenshots**, maintaining the same color/shape and no clipped PF half.
- Level-3 width remains larger than the 32-color-clock-wide troll, in all sampled X/Y positions.
- Screenshots include a nonzero-width ring at left, center and right; test script detects missing halves.
- NTSC frame is consistently 262 lines in real Stella Debugger across X shifts and overlap stress cases; document worst-case 6502 cycle use before claim.
- No unbounded PF buffer is allocated: 128-byte RAM is insufficient for a full 40-bit × 84-row bitmap.
- No final rendering decision or new bank scheme is made without comparative evidence against P02-A.

## Rejection triggers

- Right and left halves cannot both be updated without missing pixels or exceeding the 76-cycle scanline limit.
- Ring requires unacceptable PF scenery removal or locks sprite resources reserved for future enemies.
- Shift cost or bank-size requirements cannot be reconciled with authentic Atari 2600 performance.

The goal is a *technically defensible choice*, not an attractive isolated ring at the expense of the full game. B3 is NOT authorized as a production kernel by this plan.
