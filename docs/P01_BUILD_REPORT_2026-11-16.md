# THE SKRAUN - P01 implementation / build report

Date: 2026-11-16
Scope: NTSC 4 KiB 6502 technical prototype; troll silhouette, joystick movement, 3 scale choices, leg animation.
Status: source implemented and compiled; hardware rendering not yet independently verified. No next prototype gate is approved by this report.

## Source

- GitHub: https://github.com/Odourman/the-skraun/blob/main/src/main.asm
- Source commit: cac57dc0226cf383465a9ba9f4f5b1e7f69e3b7a
- Exact build (GitHub Actions): `dasm src/main.asm -f3 -obuild/the-skraun-p01.bin -lbuild/the-skraun-p01.lst -sbuild/the-skraun-p01.sym`
- CI run: https://github.com/Odourman/the-skraun/actions/runs/43861600791
- CI conclusion: success. Workflow created ROM, assembler listing, symbol map, checksum file.

## Reproducibility

- Output ROM: 4096 bytes (plain 4 KiB Atari 2600 NTSC cartridge).
- SHA-256: `7f27eb778247afe7ae0f8445d2654bad080ba36aee257ecb78692d9191ba5455`
- RESET vector: `$F000`. IRQ/BRK vector: `$F000`.
- Diagnostic gameplay test: movement in 8 directions; diagonal moves on 2 of 3 frames; three sprite concepts 8x12, 16x24, 32x36 pixels; rear leg alternating graphic; SELECT cycles sizes (edge triggered).
- Display loop design: 3 VSYNC, 37 VBLANK, 192 visible, 30 overscan = 262 WSYNC-delimited lines, assuming bounded sections complete within each line.

## Self-test evidence (not independent verification)

- GitHub Actions DASM assembly: PASS.
- File length, reset vectors and SHA-256: PASS.
- A locally written, task-specific 6502/WSYNC *model* (not a full TIA emulator) executed multiple frames. After the first startup frame, modeled VSYNC intervals were 19,912 CPU cycles = 262 scanlines each.
- Modeled movement: idle 64/80; right 78/80; up 64/94; diagonal right/up 73/89 after 14 completed frame updates. SELECT held activated level 2 just once.
- The model is not a substitute for Stella's debugger, TIA beam timing, scanline measurements or real-device testing; the first startup interval was 261 modeled scanlines.

## Open P01 verification tasks

1. Load `the-skraun-p01.bin` in Stella in Atari 2600 NTSC mode.
2. Confirm visible silhouette is readable in all three scale settings and the eye holes and legs look correct.
3. Verify joystick controls across directions, diagonals, edges, and SELECT press/release; compare at least one static and moving picture at each size.
4. In Stella Debugger, check stable 262-line NTSC frames, no VSYNC/VBLANK or kernel overruns, and note total CPU cycles per scanline.
5. Check original-hardware behavior where possible, especially HMOVE left-edge effects and line stability.
6. Ask a separate verifier to repeat these checks and record a distinct verdict.

## Non-scope

No halo, obstacles, enemies, or collision engine has been implemented. P02, P03, P04 and P05 remain separate later gates. The 60 design decisions are unchanged.