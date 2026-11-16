# THE SKRAUN — P01 Stella debugger NTSC timing evidence

**Date:** 2026-11-16
**Scope:** P01 only; not the final game or independent verification.
**ROM SHA-256:** `7f27eb778247afe7ae0f8445d2654bad080ba36aee257ecb78692d9191ba5455` (4,096 bytes).
**Emulator:** Stella 6.7.1 on Linux/Xvfb, software rendering, sound and multithreaded rendering disabled.

## Direct debugger observation

A real Stella Debugger screenshot from [diagnostic run 43864824100](https://github.com/Odourman/the-skraun/actions/runs/43864824100) shows:

- Frame counter = **20**.
- Scanline display reads **262** for the preceding frame.
- At the debugger command prompt, `print _scanEnd` returned **#262**.
- The program counter is in the expected P01 frame routine.
- The same ROM checksum as the original reproducible P01 build was recorded.

Screenshot archived in Drive:
https://drive.google.com/file/d/1HD69Ohn-dknw5Fku2QG_5GRaDqYfm37i/view?usp=drivesdk

Diagnostic artifact archived in Drive:
https://drive.google.com/file/d/1JY05J91bmJN4ToW8J5hskDOzkCMv5Dec/view?usp=drivesdk

## Test interpretation

**Observed PASS:** On at least one steady-state NTSC frame, Stella itself reported 262 scanlines. This is stronger evidence than the earlier task-specific 6502/WSYNC model.

**Limitations:** It is one recorded debugger observation, not a complete scanline-by-scanline or CPU-cycle budget audit. Original hardware and PAL were not tested. Independent verification remains pending.

The later attempts to automatically export debugger CLI sessions were not accepted as measurements: in one run the session file was empty, and in another the virtual Stella window was black/unavailable. These were **test harness failures** and do not overturn the successful direct debugger screenshot.

The GitHub debugger workflow is now restricted to manual diagnostics to prevent these transient failures from becoming misleading CI acceptance checks. Full independent acceptance is tracked in [P01 issue #1](https://github.com/Odourman/the-skraun/issues/1).

**Gate:** P01 remains OPEN until full direction/animation tests and independent NTSC verification are recorded.
