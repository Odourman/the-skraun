# FULLGAME-1 – SPARSE PF1/BL/M1 + EARLY GRP1 KERNEL – 2026-11-25

**Status:** `DEVELOPER_OBSERVED_BOUNDED / SOURCE_ONLY_CYCLE_LEDGER / NOT_RELEASE_READY`. Read [draft PR #52](https://github.com/Odourman/the-skraun/pull/52). This is a new **isolated implementation experiment**, authorized expressly by the user, and not a new full game or release approval.

## Exact base and code

- Branch `experiment/fullgame1-kernel-sparsepf-earlygrp-20261125` branches from FULLGAME-1 draft PR #51 HEAD `8ab2840c99785b499c3499b89a23246fca026fa9`. Neither PR #51, frozen GAMEPLAY-5 nor `main` were edited.
- Original actual 16,384-byte F6 ROM SHA256 `146c6541c673b10d2dc44304627b67ce9a5e3788e39d087d73251cfd3f50767c`.
- New assembled 16,384-byte F6 candidate SHA256 **`e5d027c35ae8bdbc0bac60a2ba41abbd5b2a777f7e32726cc9266499c02cb258`**; bank3 SHA256 `c65b3f9d2eb7fb940ffa5cd1dc35014c4ec6f8b259fb53d229f99e597b9e4c75`. Banks0-2 unchanged.
- A post-generation `scripts/fullgame1_sparse_kernel_patch.py` integrated into `scripts/fullgame1_build.py` modifies **both** normal and arrow visible kernel paths, without modifying original gameplay/score/movement/audio.

## What changed

- Physical PF1 and ENABL/ENAM1 enable are only written on **24 world-band boundary** lines instead of every **186 visible arena** scanlines. Encoded event WorldPFIndex is 0=no change, 1+band=updated band. Ordinary rows omit both enable and PF1 register writes; P1 GRP1 processing starts earlier there.
- Shifted world data by one sentinel byte and adjusted M1/BL seed pointers by -1 so event lookups need no extra DEY. Obsolete F01 diagnostic-only tables removed (56 bytes); actual live per-stage solid rectangles remain untouched.
- Both abandoned trial variants gave 264 and 263 NTSC lines respectively. The final event-index design observed 262 in selected Stella conditions.

## CPU accounting – carefully distinguish arithmetic and physical proof

| Item | Baseline | Candidate | Evidence |
|---|---:|---:|---|
| PF1 writes / arena image | 186 | 24 | SOURCE_ONLY exact active loop/event count |
| ENABL or ENAM1 writes / image | 186 | 24 | SOURCE_ONLY exact active loop/event count |
| Non-boundary lines | 162 | 162 | SOURCE_ONLY |
| PF/effect code per ordinary line | 20 CPU cycles | 7 | SOURCE_ONLY opcode sum |
| PF/effect code per boundary line | 20 CPU cycles | 22 | SOURCE_ONLY opcode sum |
| Arithmetic total difference for 186 scanlines | baseline | **-2058 cycles** | SOURCE_ONLY aggregate, **not** additional time on a particular critical scanline |

**Boundary lines cost 2 cycles MORE** than the original. An aggregate saving cannot prove 76-cycle safety, PF/GRP pixel deadlines or reliable three-actor draw in the same hardest raster line. Those are still OPEN.

## Verified source values and actual bounded emulator sampling

- Source oracle: **1,488** PF row comparisons across eight worlds + **372** BL comparisons + **32,736** M1 comparisons for 176 arrow Y states × 186 rows = **34,596 / 34,596** matching expected original register values. This is not physical time proof.
- Actual developer-run local DASM assembled candidate into exactly four 4096-byte banks; bank3 output reassembled byte-identical from the isolated post-generation transformer.
- Actual local Stella 6.7.1 single sampled frame each for start, real joystick/FIRE movement, and *diagnostically RAM-injected* N3 S1 adversarial scene was **262 NTSC scanlines** in old and candidate ROM; 281×201 TV crops showed **zero pixel differences in all three sample images**. The hardest injected state used Skraun L3 X80 Y78, K1 X32 Y78, K2 X101 Y78, Ranger X147 Y78, halo active, M1 arrow and BL orb.
- **Not** a 120-frame independent scanline campaign, actual per-physical-scanline worst-cycle trace, original console test, human playtest or independent Verification. Synthetic same-Y RAM setup may exercise the displayed one-slot P1 but does NOT prove three independent visible actor masks.

## Reproduction and open release gates

- Run `python3 scripts/fullgame1_build.py`, check exact SHA `e5d027c35ae8bdbc0bac60a2ba41abbd5b2a777f7e32726cc9266499c02cb258`.
- Isolated workflow `.github/workflows/fullgame1-sparsepf-earlygrp.yml` builds with real DASM and executes the native 17-scene Stella regression. Check actual [Actions run #45528298701](https://github.com/Odourman/the-skraun/actions/runs/45528298701) for its **completed** result; no claim CI pass while running.
- Local review bundle (supplied to user) includes the candidate ROM, generated bank3 source/listing/symbols, Python transformer, oracle, actual Stella screenshot pairs, debugger sessions and SHA256 manifest.
- Still unimplemented/unproven: three physical P1 enemy sprites simultaneously, visually correct circular X/Y halo, arrow fine-Y, continuous full game natural play, all worst beam deadlines, stack high-water, original hardware.

**Disposition:** preserve as `SPARSE_EVENT_KERNEL_DEVELOPER_CHECKPOINT / MAIN_REVIEW_REQUIRED / NO_MERGE`, and do not silently apply patch to existing PR #51. User explicitly authorized only this bounded kernel change.
