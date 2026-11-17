# PF-REP1 — real R3 register and colour representability SOURCE study

**2026-11-17 | RESEARCH, NOT ROM / NOT STELLA / NOT FINAL GAME.**

**Why:** New [RESEARCH v1](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_RESEARCH_HANDOFF_V1_RECEIPT_AND_PF_SOURCE_TRIAGE_2026-11-17.md) recommends exploring Steven Hugg's sparse PF register streams and multikernels before a new all-in renderer. User does not want another beautiful isolated demo; goal is same-Y 3 enemies + gold 360° halo + obstacles + approved U1-LEG1 + easy L3 movement in a real game.

**Authoritative frozen original R3 code:** [romdev_r3_overlap.asm](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm), Git blob `3c9ed79078eee6a0c63100614a593f92e240b5e8`. `R3_SOURCE_EXACT_MASKS.json` stores exact **byte-alias-resolved `M_halo` and `M_scenery` five-field, 19-row source masks** at every X=56..104 step 4, and the 177-entry source `RingRowMap`. Original source was directly loaded through GitHub connector, not invented. Source example is **NOT** the user's eight actual maps, or a new validated R3 ROM.

To reproduce with only Python stdlib:
```sh
python3 PF_REP1_REPRODUCE.py
```
The script creates `PF_REP1_RESULTS.json` with 13 per-X source transition and PF-colour mask reports. It validates source length, asserts all original 13 positions retain >1 transitions per two-line group, tests PF0/PF1/PF2 bit order and catches coactive halo/obstacle rows.

Actual findings: across 88 executed R3 `R3Pair` iterations (x176,174,...2), all 13 positions have **6–12 two-line groups with >1 individual source PF field transition**. 16 pairs per X have *both* original-mode halo and synthetic scenery PF bits lit, and they occur within the same half-screen, so a single frame with plain single-colour `COLUPF` cannot make both gold and blue *as distinct PF colours* on those scanlines. At overlapping exact PF pixel cells, a priority choice is required (and NOT presently user-authorised). Two alternative priority colour-transition lower-bound histograms are recorded; neither proves real TIA timing.

The script also counts the **minimum zero-page stores to change actual PF register values** in the reference left→right and two-line phases, setting up a critical distinction: "few changes between consecutive scanline shape rows" does **not** remove *required horizontal asymmetric PF0/PF1/PF2 rewrites within the same scanline*. This is theoretical register-state accounting, not a cycle-exact executable TIA schedule, and does not establish actual write deadlines.

**Rejected:** direct substitution of Hugg's simple 1-register-per-2-lines sparse PF stream into the original R3 halo + synthesised scenery artwork. **Not rejected:** a more flexible multiwrite kernel, altered resource ownership, a separate coloured drawing resource, or three-stream after exact RAM and deadline proof. R3 full-scene NO-GO and #15/#19/#23/#24 OPEN remain.

**STOP:** PF-REP1 is SOURCE ONLY; no real ROM, 6507 cycles, Stella screenshots, merger, palette or locked U1-LEG1 sprite change. [PF-REP1 issue #25](https://github.com/Odourman/the-skraun/issues/25).