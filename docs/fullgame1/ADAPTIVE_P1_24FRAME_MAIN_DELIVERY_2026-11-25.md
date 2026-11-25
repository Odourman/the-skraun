# THE SKRAUN - adaptive P1 scheduler / MAIN developer handoff (2026-11-25)

**Disposition:** DEVELOPER_OBSERVED_BOUNDED_PASS / THREE_SIMULTANEOUS_P1_SPRITES_NOT_SOLVED / MAIN_REVIEW_REQUIRED / NO_MERGE. Work was explicitly requested by user and isolated from FULLGAME-1 PR #51 and rejected sparse-PF PR #52.

## Exact source and build
- Base PR #51 HEAD 8ab2840c99785b499c3499b89a23246fca026fa9; frozen original 16KiB F6 ROM SHA256 146c6541c673b10d2dc44304627b67ce9a5e3788e39d087d73251cfd3f50767c.
- New source scripts/fullgame1_adaptive_p1_patch.py plugs into scripts/fullgame1_build.py. New F6 ROM is exactly **16,384 bytes**, SHA256 **d2a0a1b57ac9c78b2af14f77800f7c1ecf99aaa43f60e8c4216974f18aed2a0e**. Bank0 SHA256 6cc9102799dd01ad75316fce200c7a1dd1a914d67062d0d2426635107eb3b20b; banks1/2/3 byte-identical to original.
- AdaptiveSelect lives in bank0 at F A40, is invoked during blank-time game updates, and prioritizes active sword, 24f sword telegraph, Ranger draw/release, otherwise live actor round robin. A single dangerous actor gets 3 of every 4 frame slots; simultaneous knight warnings share 3/3/2 of every 8 slots with Ranger. Retains KnightCanHit no-off-slot damage gate. No visible-row register instructions changed.
- All four standard F6 banks are 4096 bytes each. Actual used content still has padding, so future extra space should fund real predecoded raster events, graphics and world content; filling it with meaningless bytes does not improve playability.

## Genuine native CI
- **SUCCESS** [GitHub Actions #45530532678](https://github.com/Odourman/the-skraun/actions/runs/45530532678): real DASM, exact candidate 16384 bytes and SHA, Stella 6.7.1 bootstrap, 17/17 selected physical NTSC final frames scanEnd=262 (including arrow_first, stage2_L3, gameover_restart). Artifact 14985380222 holds native ROM/build and Stella proof.
- Old 120 captured sequential states in that workflow still have 0/120 individually observed scanEnd values. Do not upgrade a missing measurement into PASS.

## Local Stella 24-consecutive-frame physical tests
- Real X11 Stella debugger, synthetic RAM fixtures then 24 individually stepped frames and GUI-entered prints of _scanEnd and DrawSlot each frame. 24 pixel screenshots each for same-Y and close-overlap tests. 8 separately preserved sessions total 192/192 observed completed-frame endpoints at 262 NTSC lines, one of these 8 was frozen baseline.
- Baseline K1+K2 24f warning same Y, x32/101/147: slots K1/K2/Ranger **8/8/8**.
- New K1+K2 same Y: **9/9/6**; isolated K1 warning **18/3/3**; isolated K2 warning **3/18/3**; Ranger bow draw **3/3/18**.
- New close-overlap with large Skraun P0, x77/85/92: **12/6/6**; wide X, x10/145/156: **12/6/6**; halo + arrow + orb stress: **18/0/6** but halo can kill K2, hence not a three-surviving-actor proof.
- Screenshots show a real, small visible blue sprite when selected, plus green Ranger; at P0 overlap, blue on-screen pixel counts on sampled visible-TV crop reduce from about 122–150 to 22–38. The warning can remain difficult to read despite P1 prioritization.

## What is still not proved
- Not three fully independent 8-bit P1 sprites in one physical frame; still one P1 slot selected each frame.
- Not 24 fully readable contiguous sword-warning frames for each knight under same-Y/P0 overlap; image occlusion remains serious.
- Not cycle-by-cycle worst-physical-scanline/beam deadline and RIOT/stack highwater proof or complete game playthrough.
- Not full circular X/Y halo or fine-grained visible arrow, which were outside this bounded change.

**Outcome:** Preserve as developer-tested draft PR #53, never merge blindly to main or mark FULLGAME-1 finished. Better immediate warning-priority gameplay is observed; the original physical three-enemy renderer challenge remains open.