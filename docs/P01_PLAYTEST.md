# THE SKRAUN — P01 MANUAL PLAYTEST (NTSC)

**Status:** Manual test protocol, not proof that the tests have passed.
**ROM SHA-256:** `7f27eb778247afe7ae0f8445d2654bad080ba36aee257ecb78692d9191ba5455`
**Source:** `src/main.asm`
**GitHub Actions:** https://github.com/Odourman/the-skraun/actions/runs/43861600791

## Loading
1. Download the 4,096-byte `the-skraun-p01.bin` from the GitHub Actions artifact or The Skraun's Google Drive folder.
2. Open the file with Stella. Cartridge mapping should be `4K` and TV mode `NTSC`.
3. The screen should show one small, one-colour, symmetrical creature with two eye holes and two small back legs on a black background.
4. No enemies, halos, obstacles, scores or sounds are present yet.

## Controls
- Joystick port 0: up, down, left, right and diagonal movement (Stella defaults to arrow keys).
- Console SELECT: cycle through level 1 (8×12), level 2 (16×24) and level 3 (32×36). Default Stella key: F1. Release and press again to advance one additional level.
- Level changes are diagnostic only. They do **not** represent the final orb-based progression.

## Check visually
1. Boot at level 1. Confirm troll appears and remains stationary when no direction is pressed.
2. Test all eight directions. Diagonal speed should not be noticeably faster than straight movement.
3. Test edges of the screen for clipping or disappearing graphics.
4. Observe alternating little back legs during movement. At rest, they should stay still.
5. Use SELECT to test all three sizes. Confirm size changes without changing player movement speed.
6. Capture Stella screenshots at all three levels (default shortcut F12).
7. Use Stella Debugger to examine scanline count, `VSYNC`, `VBLANK`, `WSYNC`, and any timing overruns. Stable frames are intended to have 262 NTSC scanlines.

## Report defects
For each issue record: ROM SHA-256, Stella version, NTSC/PAL setting, scale level, joystick input, reproduction steps, screenshot and debugger observation.

## Explicitly NOT verified
Successful DASM assembly and a custom 6502/WSYNC model do not prove accurate Stella rendering or compatibility with original hardware. Separate independent verification is still required for P01 approval.
