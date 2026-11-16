# THE SKRAUN - P01 implementation / build report

Date: 2026-11-16
Scope: NTSC 4 KiB 6502 technical prototype; troll silhouette, joystick movement, 3 scale choices, leg animation.
Status: source compiled; real Stella 6.7.1 has now rendered all three sizes and moved the level-3 troll right in automated screenshot checks. Independent verification and hardware timing are still OPEN. No next prototype gate is approved by this report.

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
2. [SELF-TEST PASS] Three sizes render visibly in Stella 6.7.1, with two black eyes and legs. Independent aesthetic acceptance is still pending.
3. [PARTIAL PASS] SELECT selects all three sizes and rightward joystick movement works in Stella. Full real-emulator all-direction, diagonal, edge and animation checks remain.
4. In Stella Debugger, check stable 262-line NTSC frames, no VSYNC/VBLANK or kernel overruns, and note total CPU cycles per scanline.
5. Check original-hardware behavior where possible, especially HMOVE left-edge effects and line stability.
6. Ask a separate verifier to repeat these checks and record a distinct verdict.

## Non-scope

No halo, obstacles, enemies, or collision engine has been implemented. P02, P03, P04 and P05 remain separate later gates. The 60 design decisions are unchanged.

## Follow-up automatic checks

- `tests/p01_cpu_smoke.py` was added to GitHub and integrated into the regular CI build. It uses a limited 6502/WSYNC execution model and checks joystick motion, a two-out-of-three-frame diagonal update, one SELECT activation per press, and stable 262-line modeled frames. CI is a self-test, not independent acceptance.
- Ubuntu Stella 6.7.1's `-rominfo` recognized the ROM as NTSC and 4K.
- Early Xvfb Stella attempts produced either no PNG or an all-black desktop with no X11 window. They were **test-harness failures**. A later run succeeded after setting `-audio.enabled 0 -threads 0 -vsync 0`; these historical failures do not describe the ROM rendering.
- Stella visual diagnostic workflow: https://github.com/Odourman/the-skraun/blob/main/.github/workflows/stella-smoke.yml
- Manual test guide: https://github.com/Odourman/the-skraun/blob/main/docs/P01_PLAYTEST.md

**P01 gate: NOT YET APPROVED**. Assembly, 3-size actual Stella rendering, SELECT and rightward joystick motion passed self-tests; full Stella timing/control testing and separate independent verification remain outstanding.

## Actual Stella 6.7.1 visual and movement self-test (2026-11-16)

- CI run: https://github.com/Odourman/the-skraun/actions/runs/43863924388 — **success**.
- Primary evidence: https://github.com/Odourman/the-skraun/blob/main/docs/P01_STELLA_VISUAL_EVIDENCE_2026-11-16.md
- Captured TIA sprite dimensions (native logical): level 1 = 8×12; level 2 = 16×24; level 3 = 32×36. Each level was captured and pixel-measured in real Stella 6.7.1 screenshots.
- Screenshot sizes (2× horizontal scale): level 1 = 16×12; level 2 = 32×24; level 3 = 64×36.
- Level 3 rightward movement: capture x=124→210 (86 screenshot pixels) without vertical movement or scale change.
- `tests/check_stella_images.py` is now the mandatory automated visual check. It prevents all-black screenshots and dimension regressions from being reported as a pass.
- Full screenshots and GitHub Actions logs are archived in Drive under `P01 - Stella evidence - 2026-11-16`.
