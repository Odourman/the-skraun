# THE SKRAUN — P01 Stella visual smoke test (2026-11-16)

## Scope and provenance
- ROM: `the-skraun-p01.bin`, 4,096 bytes, SHA-256 `7f27eb778247afe7ae0f8445d2654bad080ba36aee257ecb78692d9191ba5455`.
- Source: `src/main.asm` (unchanged during this round), DASM / 4 KiB NTSC.
- Emulator: **Stella 6.7.1**, SDL 2.30.0, Linux X11 via Xvfb, software rendering, sound off, threaded rendering off.
- CI run: https://github.com/Odourman/the-skraun/actions/runs/43863924388
- Screenshot checks: `tests/check_stella_images.py` (actual Stella PNG pixel analysis).
- Full artifact: https://github.com/Odourman/the-skraun/actions/runs/43863924388 (artifact `p01-stella-visual-diagnostic`).
- Drive evidence folder: https://drive.google.com/drive/folders/1-0YyUkR_6w0-nby3et2KoP8CiMdyQ_gM

## Observed results

| Frame | Green sprite bounding box in Stella's 320×228 snapshot | Screenshot dimensions | Logical TIA sprite dimensions |
| --- | --- | --- | --- |
| Level 1 | x=122..137, y=116..127 | 16×12 | 8×12 |
| Level 2 | x=124..155, y=104..127 | 32×24 | 16×24 |
| Level 3 | x=124..187, y=92..127 | 64×36 | 32×36 |
| Level 3 after right input | x=210..273, y=92..127 | 64×36 | 32×36 |

At level 3, held rightward joystick input moved the sprite **+86 captured pixels (+43 logical TIA horizontal pixels)** while leaving its vertical bounding box and sprite dimensions unchanged.

The green silhouette, two black eye gaps and rear legs are visible in the level-1 and level-3 screenshots. The images are directly from the Stella emulator, not generated artwork.

### Automated test conclusions
**PASS (self-test):**
- A real Stella emulator rendered three visible, nonblank sprites with dimensions matching the three source-defined levels.
- SELECT changed the displayed level twice as intended.
- Rightward joystick input moved the level-3 sprite without vertical drift.
- The main CI assembled the original ROM to 4,096 bytes and passed the model-based movement and boundary regression tests.
- Stella identified NTSC / 4K cartridge mapping.

**NOT YET VERIFIED:**
- All eight joystick directions and diagonals in real Stella (CPU-model-only coverage exists).
- Correct animation phase transitions while moving, and movement/animation during size changes.
- TIA scanline and cycle budgets read directly from Stella Debugger; 262-frame timing is currently demonstrated by a task-specific CPU model, not by debugger screenshots/logs.
- NTSC operation on real hardware, PAL compatibility, and independent verification.

## Engineering findings

The earlier completely black CI desktop capture was caused by Stella failing to create an X11 window with the original automated launch settings. Running with `-audio.enabled 0 -threads 0 -vsync 0` now yields a normal emulator window and actual F12 PNG screenshots. The CI rejects blank captures and checks sprite dimensions; a green build no longer relies solely on the executable starting.

**Status:** P01 visual and single-axis movement smoke tests passed. P01 as a whole is **not independently accepted**. No gameplay rule, sprite artwork or ROM code changed in this diagnostic round.

## Recommended next action

Use an independent VERIFICATION pass to inspect all directions, actual Stella frame/cycle timing and the visual appearance of every size. Do not merge future halo experiments into P01's baseline ROM before those results are recorded.
