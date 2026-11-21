# RESEARCH II — N6-C source-only reproducible handoff
**2026-11-21. Advisory only. Issue #30 remains OPEN.**
- [Full technical decision brief](RESEARCH_II_N6C_PHYSICAL_P1_DECISION.md)
- [Python 3 stdlib replay](N6C_COMPACT_SOURCE_REPLAY.py)
- [Frozen source-only result JSON](N6C_SOURCE_COUNTEREXAMPLES.json)

Run in a local checkout of this branch:
```sh
cd research/n6c_2026-11-21
python3 N6C_COMPACT_SOURCE_REPLAY.py
```
Optionally provide the **exact frozen R3 assembler** as an argument. It checks the raw historical Git blob SHA1 and all 24 enemy bitmap bytes:
```sh
python3 N6C_COMPACT_SOURCE_REPLAY.py /path/to/romdev_r3_overlap.asm
```
Output: `P1_R3_ROW_COLOR_BITMAP_BOUNDS.csv`, `P1_NEXT_LINE_MAIN_RESP_CONFLICT.csv`, `N6C_SOURCE_COUNTEREXAMPLES.json`. The generated JSON must match the frozen JSON file. Use a clean copy or compare before overwriting.

No ROM, no DASM, no new Stella run, no independent Verification. No production changes, mapper change, sprites, merge, N7 start, or implicit gameplay compromise. The example partial 64-cycle PF/P0/first-P1 opcode row in the report is **NOT an integrated engine proof**. The `RESP1` main-copy next-line and TIA write completion models are bounded by their stated assumptions, not cycle-perfect TIA simulation.

Sources: [original R3 code](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm) / blob `3c9ed79078eee6a0c63100614a593f92e240b5e8`; [MAIN III N6-C handoff](https://github.com/Odourman/the-skraun/blob/main/handoff/RESEARCH_II_N6C_P1_TIMING_AND_INTEGRATED_KERNEL_SOURCE_ONLY_2026-11-21.md); [N3 fixture](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_FIXTURES_2026-11-17.json); [MAIN's N6-C source-only interim](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N6C_SOURCE_ONLY_PHYSICAL_FEASIBILITY_INTERIM_2026-11-21.md).
