# THE SKRAUN — P02-B2 Centered playfield halo + troll

Date: 2026-11-16
Status: **PASS, bounded Stella visual developer self-test**. Not a production halo, independent verification or completed P02 gate.
Experimental branch: `experiment/p02-playfield-b2`.
Original P01 `src/main.asm` and approved gameplay design decisions 01–60 are unchanged.

## Source and reproducible build

- Experimental assembler: `experiments/p02_playfield_b2.asm`
- Command: `dasm experiments/p02_playfield_b2.asm -f3 -obuild/p02-playfield-b2.bin -lbuild/p02-playfield-b2.lst -sbuild/p02-playfield-b2.sym`
- Format: plain Atari 2600 NTSC 4 KiB cartridge, **4,096 bytes**
- SHA-256: `59b94620c64f57e8847d096cc58d1bda216fd52e8a8f1ca15fd46a7241cf74a1`
- Source calibration commit: `1dfab2748faba8d5b15cf29ec02343cd4188f1bd`
- Passed CI: https://github.com/Odourman/the-skraun/actions/runs/43871863825
- Visual regression: `tests/p02_b2_stella_check.py`

## Real Stella screenshot evidence

Stella 6.7.1 Linux/Xvfb, screenshot output 320×228. Horizontal display pixels are 2× TIA color clocks.

| Level | P0 green troll bbox (x1,y1,x2,y2) | P0 width×height | PF gold ring bbox | Ring width×height |
| --- | --- | --- | --- | --- |
| 1 | (152,105,167,116) | 16×12 | (136,90,183,131) | 48×42 |
| 2 | (148,99,179,122) | 32×24 | (120,80,199,141) | 80×62 |
| 3 | (126,93,189,128) | 64×36 | (112,69,207,152) | 96×84 |

Automatic assertions passed: all three distinct sprite sizes, increasing halo diameters, ring envelope extending beyond the troll on every side, and sufficient alignment between green player and gold playfield center. The first attempts with incorrectly calibrated RESP0 placement **failed** the test and were corrected based on their measured screenshot bounding boxes.

## Technical resource budget

- P0 (first normal player sprite) is used for the troll, using NUSIZ0=0/5/7 for 1×/2×/4× width.
- The **halo uses PF2** with `CTRLPF=1` reflection, which is possible because the ring remains fixed at x80.
- P1, both missiles and the ball remain unused, **in this test only**.
- Six precomputed 192-row tables (three ring + three troll) use **1,152 bytes of cartridge ROM**, and no screen framebuffer in the 128-byte internal RAM.
- Each visible line performs a ROM lookup for PF2 and GRP0. This is a modest kernel, but **a direct 6502/Stella Debugger worst-case cycle measurement for B2 has not been completed**.

## What this does NOT prove

The ring is permanently visible; FIRE duration, cooldown and blinking are not implemented here. Neither ring nor troll can move in B2. A mirrored playfield is fixed about x80, so it cannot simply follow a moving player horizontally. It is **not demonstrated** that six asymmetric PF writes per scanline, moving sprites, scenery and enemies will all fit. Collisions, arrow destruction, the one-orb rule, obstacles and full stages are also absent.

P02-A's P1-halo solution had an insufficient maximum width on level 3. B2 demonstrates an alternative way to preserve P1 **while stationary**, not a complete dynamic solution.

## Recommended next bounded experiment — B3a

Prove a non-mirrored playfield ring at three discrete horizontal centers (e.g., x56, x80, x104) using left/right half-row rewrites and actual Stella screenshots. Only if that passes under cycle limits should dynamic joystick following, vertically moving ring, FIRE timing, collision model or simultaneous enemies be introduced.

P01 independent verification remains open at https://github.com/Odourman/the-skraun/issues/1. No experimental renderer has been merged into the stable game source.
