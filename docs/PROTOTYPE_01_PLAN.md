# Prototype 01 — Troll display and movement

**Status:** Implemented and built successfully with DASM on GitHub Actions (2026-11-16). Stella visuals, original hardware, and independent verification remain pending.
**Target:** Stock Atari 2600 / NTSC, initially via an ordinary 4 KiB cartridge image unless a documented constraint forces a different mapping.
**Design authority:** The Skraun MAIN design decisions 01–60 (2026-11-16).

Build evidence: [P01 build report](P01_BUILD_REPORT_2026-11-16.md). Download the ROM from the linked GitHub Actions run or the project's Google Drive folder.

## Objective

Produce a small reproducible `.bin` that displays and moves the troll in a single uncluttered arena. This is a feasibility experiment, not the finished game.

## Minimum scope

1. Start on original-compatible Atari 2600 NTSC timing.
2. Draw a recognizable, symmetrical single-colour troll viewed from directly overhead.
3. Move with the joystick in all eight directions. Diagonal movement must not produce an unreasonable speed advantage.
4. Draw and exercise three distinct sprite-size concepts. They may be switched by a temporary debug control, not yet by an orb.
5. Investigate whether two little legs can animate affordably without stealing time needed by the eventual halo and enemy kernel.
6. Keep the image stable and the player visible at the screen edges; never write past allocated RAM.

## Explicitly out of scope

No knight AI, archer AI, projectile, score, orb pickup, halo attack, obstacles, world transitions or sound. No claim that four simultaneous characters will already fit.

## Required evidence before approval

- Complete assembler source, chosen assembler and exact build command.
- Output ROM with size and SHA-256.
- A clean build log and test instructions.
- NTSC scanline count and any timer/overrun observations from Stella Debugger.
- Three-size visual captures and notes on sprite identity/readability.
- Self-test findings, including reproducible issues.
- **Separate independent verification** before reporting this prototype as approved.

## Engineering questions to record

- Exact pixel dimensions, colour choice and per-scanline TIA register use for each size.
- Whether sprite scaling uses TIA NUSIZ replication or authored multiscale shapes; large figures may need more than simple replication.
- RAM budget and timing margin for a future halo and sprite multiplexing.
- Frame-stepped movement consistency and diagonal normalization without expensive floating-point arithmetic.
- Hardware differences or constraints discovered that must be tested under PAL later.

## Gate decision

P01 passes only if the ROM can be reproduced and the visible/movement behaviour matches the agreed design on a measured NTSC frame. An attractive screenshot by itself is not sufficient.

Research suggestions are advisory. New gameplay changes must be marked as proposed, rather than silently replacing established decisions.
