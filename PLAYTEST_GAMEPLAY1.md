# THE SKRAUN - GAMEPLAY-1 - EXPERIMENTAL F8/NTSC PLAYTEST

**Status:** DEVELOPMENT PARTIAL. This is a playable experiment, not production-canon approval.
**Base:** frozen PLAY1-H commit `79b9739e77741c74ae5228f3c63d64449af7bc9f`; its original source tables remain intact.
**Branch:** `experiment/gameplay1-accelerated-full-prototype-20261122`.
**No main merge.** Source-only / developer-observed evidence must not be called independent VERIFICATION.

## Run on Stella / original cartridge-compatible F8 mapper
Open `experiments/gameplay1_f8_ntsc.bin` once the CI freeze has committed it, or download `build/gameplay1/gameplay1_f8.bin` from the matching GitHub Actions artifact.
ROM is 8192 bytes of conventional F8 (two 4 KiB banks; bank 0 then bank 1). It is not suitable for a fixed 4 KiB-only cartridge. Stella labels `F8*` by automatic detection. **NTSC is the target**, not PAL; verify physical scanlines before a hardware compatibility claim.

## Controls (one-player Atari joystick)
- Joystick: all 8 directions; wall slides and large character collision reuse PLAY1-H.
- FIRE: starts a ~30 NTSC-frame attack. Holding FIRE reactivates after level-dependent recovery; Skraun moves during the attack.
- Walk into BL orb: raise level L1 -> L2 -> L3 when the next full body fits. Stage visit displays one BL orb; restart on later stage visits.
- Console SELECT: inherited experimental level-selection/debug control from PLAY1-H; not canonical game control and **not yet physically shown to work in the tested GAMEPLAY-1 SELECT sequences**.
- Console RESET after GAME OVER: initializes a new game.

## What you can actually test
- Move the gray upright original U1-LEG1 level1 player through two provisional obstacle pattern types (some stage handling is source-only so far).
- Collect an orb and try a larger body; move and cast FIRE, which changes the arena PF color to gold.
- Approach the blue knight: physical P1 flashes gold during a ~24-frame sword warning, then a logical damage window; mere body contact does not hurt.
- Attack the P1 target with FIRE; sequential target-wave logic is in source.
- The last single-P1 slot in every wave acts as **world-colored fleeing Ranger proxy** (not Ranger sprite, no arrow).
- 8 stage counters have distinct test-color / orb-X settings and an odd/even alternate obstacle type; this is **NOT eight production maps**.
- Score in memory: 100 points per sequential knight proxy, 250 per Ranger proxy. Lives start at 3. Automatic life at each new 2,000-point threshold is implemented in source; visual HUD not done.
- Stage order in source is 1..8..7..1..2; stage transitions, scoring and lives require further physical playtest.

## Known critical limitations
1. **ONE** P1 enemy drawn at once. The 2-knight+1-Ranger simultaneously-rendered canon is *OPEN*. Sequential proxy is NOT a gameplay concession.
2. PLAY1-H gold PF halo follows Y but not X. Global PF recoloring under FIRE is not sufficient evidence of a 360 degree geometric ring.
3. No arrow or real Ranger sprite; knight sword warning uses temporary P1 color, not an approved sword animation pose.
4. Only TWO provisional PF obstacle geometries, alternating. Obstacles/halo/collision for all eight distinct final maps not verified.
5. No physical HUD text, authentic world sprites, dream spirals, full sound design or finished GAME OVER display.
6. Level3 SELECT test did not yield the expected L3 physical sprite in initial screenshots. L3 current combined runtime remains NOT VERIFIED.
7. Full NTSC 262 physical scanline and TIA register-write deadline/worstcase proof remains open. The old PLAY1-H static kernel has a possible ~77/76 cycle source-only path. 8 KiB banked ROM does not add CPU cycles.
8. All dynamic score/ranger/bonus/arena logic is developer-authored and source-reviewed until each relevant gameplay sequence is captured; a green build is not a full gameplay PASS.

## Reproduce real assembly
```sh
mkdir -p build/gameplay1
dasm experiments/gameplay1_bank0.asm -f3 -obuild/gameplay1/bank0.bin -lbuild/gameplay1/bank0.lst -sbuild/gameplay1/bank0.sym
dasm experiments/gameplay1_bank1.asm -f3 -obuild/gameplay1/bank1.bin -lbuild/gameplay1/bank1.lst -sbuild/gameplay1/bank1.sym
test "$(stat -c %s build/gameplay1/bank0.bin)" -eq 4096
test "$(stat -c %s build/gameplay1/bank1.bin)" -eq 4096
cat build/gameplay1/bank0.bin build/gameplay1/bank1.bin > build/gameplay1/gameplay1_f8.bin
test "$(stat -c %s build/gameplay1/gameplay1_f8.bin)" -eq 8192
sha256sum experiments/gameplay1_bank0.asm experiments/gameplay1_bank1.asm build/gameplay1/gameplay1_f8.bin
```

## Reproduce bounded real-Stella developer captures
The Ubuntu GitHub Actions workflow `.github/workflows/gameplay1-real.yml` installs DASM/Stella 6.7.1/Xvfb and executes `scripts/gameplay1_stella_scenes.sh`. It saves debugger desktop screenshots, actual TIA crops, per-scene real joystick/FIRE scripts, Stella logs and the executable 8KiB F8 ROM. `tests/gameplay1_pixels.py` rejects specific physical pixel regressions of U1-L1/L2, P1 original 120 bits, FIRE gold and warning. Those bounded checks are **DEVELOPER_OBSERVED**, not a full-frame trace or independent verification. Check logs / SHA in the exact matching CI run; partial screenshots do not prove all mechanics.
