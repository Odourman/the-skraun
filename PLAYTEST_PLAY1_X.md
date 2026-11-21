# THE SKRAUN — PLAYTEST PLAY1-X
**2026-11-21 | ROM DEVELOPMENT II | PLAY1-X authorized Issue #38 | expected FAIL for this physical implementation**

## Start ROM
This is an actual original Atari 2600 4 KiB NTSC-targeting diagnostic, but **NOT a correctly playable NTSC game**. It is supplied to reproduce the documented beam overrun and distorted player sprites. For playable movement/orb/halo-Y, keep the separately frozen PLAY1-H ROM as the comparison.

Build with DASM:
```sh
mkdir -p build/play1x
dasm experiments/play1_x_single_arena.asm -f3 -obuild/play1x/play1x.bin -lbuild/play1x/play1x.lst -sbuild/play1x/play1x.sym
test "$(wc -c <build/play1x/play1x.bin)" -eq 4096
sha256sum -c experiments/play1_x_SHA256SUMS.txt
```
For the manifest, use the checked-in `experiments/play1_x_single_arena.bin`, not `build/play1x/play1x.bin`.

## Real Stella gameplay input / negative render test
```sh
sudo apt-get install -y dasm stella xvfb xdotool scrot python3-pil python3-numpy
bash scripts/play1x_stella_capture.sh
/usr/bin/python3 tests/play1x_pixels.py
```
The final pixel test MUST exit nonzero: the candidate is intentionally frozen with measured failures. Use the actual `PLAY1X-authentic-DASM-Stella-ABC` Actions evidence ZIP from run #44936786678, not a source-only screenshot mockup. Nine authentic Stella 6.7.1 debugger/input scenes include baseline, L1 FIRE, actual joystick BL pickup to L2, L2 FIRE, supposed L3 FIRE A x96, B x104, C x112 and D up8, plus L3 collision attempt. Script sends `joy0Right #0`, `joy0Down #0`, `joy0Up #0`, `joy0Fire #0` and saves raw desktop/320x228 TIA crops, inputs, emulator logs. No gameplay RAM injection.

**Failure:** The second `STA PF2` write with precomputed right-half X mask and unchanged CTRLPF causes physical scanline spill in sprite-active rows. After a -3cy adjustment, actual Stella Debugger shows **273 lines L1, 285 L2, 297 L3**, rather than 262. Visible P0 BBOX heights: L1 **23** vs 12, L2 **47** vs 24, L3 **71** vs 36. Baseline R3 blue pixels **168** rather than exact 120; L2 blue **144**. All are actual emulator RGB/Debugger readouts, not a simulator. The pre-adjustment alternative was even worse: `Display Format: PAL*`. The final candidate gets `NTSC*` as format label but still has invalid line counts: the label is not a physical PASS.

Gold-pixel changes between A x96 and B x104 are observable, but the player/beam/level state is corrupted; these changes do NOT prove a valid moving 360° halo. B x104 to C x112 shows **0** non-occluded changes, because only one coarse precomputed right-half X bucket exists. Upper static obstacle row comparison changes **0** pixels in sampled scene, unlike the earlier rejected CTRLPF mirror trick. This does NOT rescue the kernel.

Only one bounded X-asymmetric right-half PF strategy was tested with a 3-cycle timing microfix. **Do not** change sprite masks, accept 297 scanlines or swap mapper to force a PASS. MAIN III decides any future separately authorized scope; ROM DEVELOPMENT II STOP after delivery. No N8/N9 or three-fiender engine.
