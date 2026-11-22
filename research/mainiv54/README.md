# THE SKRAUN / MAIN IV / RESEARCH II — ALL 54, SOURCE_ONLY

**Datestamp:** 2026-11-22. **Authority:** [binding MAIN IV handoff](../../handoff/MAIN_IV_TO_RESEARCH_II_ALL_54_PROBLEMS_GLOBAL_SOLUTION_SEARCH_2026-11-22.md), [Issue #47](https://github.com/Odourman/the-skraun/issues/47). Research-only; no ROM or change to existing canon/mapper/game source/main. Branch based on MAIN IV's frozen docs branch `a1c554b7b6734ebb726428a651634c288d9dab4f`.

## Files
- [00_MAIN_DECISION_BRIEF.md](00_MAIN_DECISION_BRIEF.md): ranked MAIN IV decision + evidence/limits
- [01_ALL_54_ISSUES_MATRIX.csv](01_ALL_54_ISSUES_MATRIX.csv): exactly 54 ID rows with status, source, previous negative, primary/backup solutions, risk and test
- [02_TOP_TECHNICAL_CANDIDATES.md](02_TOP_TECHNICAL_CANDIDATES.md): eight practical 6507/TIA candidate architectures and first falsification
- [03_GLOBAL_SOURCE_REGISTER.md](03_GLOBAL_SOURCE_REGISTER.md): original source links, multilingual search coverage, new vs recycled findings, provenance/reuse conditions
- [04_SOURCE_ONLY_REPLAY.py](04_SOURCE_ONLY_REPLAY.py): standard-library coverage/status/arithmetic replay

```sh
cd research/mainiv54
python3 04_SOURCE_ONLY_REPLAY.py
```

The **complete locally reproduced** source-only archive (including an expanded replay, results, manifest) was uploaded to connected Drive with source SHA256 `a4705b0294f2367fdd0a14b237bb727a9ff1166bab3ee5e7fc96374fab88a2f0`:
[Full source-only ZIP](https://drive.google.com/file/d/1q9YstOPtN-d1yB5saqhIJyceXsg7v77B/view?usp=drivesdk).
The four primary GitHub files were independently read back and their Git blob SHA1 equals the locally prepared text bytes. Source-only arithmetic/replay is **not independent technical verification** of any physical ROM.

**Frozen actual game anchor:** [PR #46](https://github.com/Odourman/the-skraun/pull/46), GAMEPLAY-4A commit `bc2ef9249b4e13701647850d89cb631c43190c65`, ROM reportedly 8192B/F8 SHA256 `8bb19a9d58b6a4f608f1ab10adbb622b9e70d0f44b39e247c68feb3a974427bd`. We read actual source blobs but did **not** re-download/rebuild the original ROM or run a fresh emulator.

**STOP:** MAIN IV must explicitly authorize any new developer test after this research. No N8/N9/GAMEPLAY-5, sprite, cart mapper change, canon alteration, main merge or independent Verification is implied.
