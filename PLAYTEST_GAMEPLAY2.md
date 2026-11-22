# THE SKRAUN GAMEPLAY-2 - F8/NTSC stage playtest (DEVELOPER_OBSERVED)

**Binding scope:** MAIN IV's 2026-11-22 GAMEPLAY-2 order. This is a separate experimental branch based on frozen GAMEPLAY-1 commit `7f289a536c375bf760428274280179cfe15a6a62`. Original `main`, PR #41 and U1-LEG1 must remain unchanged. F8 8 KiB only.

## Build and run
```bash
mkdir -p build/gameplay2
dasm experiments/gameplay2_bank0.asm -f3 -obuild/gameplay2/bank0.bin -lbuild/gameplay2/bank0.lst -sbuild/gameplay2/bank0.sym
dasm experiments/gameplay2_bank1.asm -f3 -obuild/gameplay2/bank1.bin -lbuild/gameplay2/bank1.lst -sbuild/gameplay2/bank1.sym
test "$(stat -c %s build/gameplay2/bank0.bin)" -eq 4096
test "$(stat -c %s build/gameplay2/bank1.bin)" -eq 4096
cat build/gameplay2/bank0.bin build/gameplay2/bank1.bin > build/gameplay2/gameplay2_f8.bin
test "$(stat -c %s build/gameplay2/gameplay2_f8.bin)" -eq 8192
sha256sum experiments/gameplay2_bank0.asm experiments/gameplay2_bank1.asm build/gameplay2/gameplay2_f8.bin
stella build/gameplay2/gameplay2_f8.bin
```
Also download the authentic, SHA-frozen `experiments/gameplay2_f8_ntsc.bin` once the one-shot freeze job has completed; never use GAMEPLAY-1's ROM SHA for GAMEPLAY-2.

## Controls and walkthrough

1. Start in stage 1, `Stage=$AA=1`, `Lives=$AC=3`, `Score=$AE:$AD=0000`. Joystick moves 8 directions. Solid mirror obstacles block Skraun by full-body rectangles. Use wall slide.
2. Move RIGHT 16 NTSC frames and DOWN 24 to pick up the original TIA BL orb near (96,112). Level `$82` changes 1 -> 2 and the orb is consumed (`$9C=0`).
3. Hold FIRE to activate 30-frame halo while moving UP 40 and RIGHT 14 to stay outside the fixed-Y sword attack band. Wait long enough for the single P1 dummy knight sequence to be cleared; two knight slots yield 100 each, last fleeing world-colored Ranger *proxy* yields 250. This is a diagnostic sequential P1 test, not approved production 2-knight+Ranger rendering.
4. After the third elimination the stage remains briefly cleared for a 24-frame transition. The next stage changes automatically to 2. Score totals 450, lives/level carry forward. Orb and enemies reset for each **new stage visit**, not when life is lost.
5. In stage2 after respawn at x80/y88, collect the new orb at x88/y112 with RIGHT 8, DOWN 24. This grants Level3 (not two upgrades for one orb). After cooldown ends, hold FIRE while moving diagonally RIGHT+UP; actual P0 expected size 64x36 on TV, using the exact U1-LEG1 source.
6. For damage test: from a fresh stage1, move RIGHT ~25, let the single knight chase, show 24-frame gold warning, active sword attack and life loss (L1 case); physical body contact alone does not deal damage. Continue to zero lives for GAME OVER, then press FIRE or console RESET to initialize a new game. The displayed game-over cue is provisional (background color), not final art.
7. At repeated 2,000-point threshold a new life is awarded; the most useful physical state values are cumulative `$AE:$AD`, bonus remainder `$BD:$BC`, lives `$AC`.

**Expected endpoint canon in source:** 1..8..8..7..1..1..2..; the endpoints must repeat on reversal. Only initial 1 -> 2 is physically audited here; the complete 16-visit loop remains separate test scope.

## Stella debugger map (hex RIOT, actual displayed RAM)

- Player x/y `$80/$81`, level `$82`, joystick `$83`; orb mask `$9C`; attack `$9E`, target alive `$A1`.
- Stage `$AA`, direction `$AB`, lives `$AC`; score low/high `$AD/$AE`; knight x `$AF`.
- Sword warning / strike / rest `$B0/$B1/$B2`; invulnerability `$B3`; wave kills `$B4`; wave target count `$B5`.
- Bonus remainder `$BC/$BD`, transition timer `$BE`.
- Collision rectangles `$C0..$EF`; stack nominal `$F0..$FF`. Runtime SP high-water not yet independently measured.
- Stella `print _scanEnd` in a **typed debugger session** yields physical scanline count. The original uncorrected GAMEPLAY-2 candidate read 261; one overscan WSYNC was added in `gameplay2_bank1.asm` to target the required 262. Do not accept NTSC* autodetection without matching physical measurements.

## Real repeatable developer tests
```bash
bash scripts/gameplay2_stella_scenes.sh
/usr/bin/python3 tests/gameplay2_audit.py
```
The GitHub Actions workflow `.github/workflows/gameplay2-real.yml` installs actual DASM, Stella 6.7.1, Xvfb and debugger GUI input to produce an 8192-byte ROM, 10+ genuine user-input scenes, 320x228 TIA crops, exact PNG hashes, textual typed `_scanEnd` sessions, input scripts and raw debugger screenshots. It fails closed on physical U1 L1/L2/L3 sprite sizes, P1 warning, gold L3 FIRE and 262 scanlines. Source-only code is not a replacement for these tests. It is developer self-check, not independent Verification.

## Known limits
- Still only ONE physical TIA P1 enemy at a time; Ranger proxy uses world color and original dummy bitmap, no real bow, arrow, 3-enemy renderer or approved K1_VISIR graphic. This is temporary diagnostic scope, **not a canon compromise**.
- Halo follows Y but **not X**. No GAMEPLAY-2 authorization for new halo renderer.
- Only TWO provisional obstacle PF layouts, no eight final maps or static dream spirals. UI has no numeric score/lives HUD; inspect debugger RAM.
- Full hardest-scene 76-cycle beam-deadline trace and runtime stack highwater are still open even if bounded frame length is 262.
- MAIN review and any independent Verification are not implied by green CI.
