# THE SKRAUN — VERIFICATION II, PR71/F1 independent final readout (2026-11-26)

**Result: INCONCLUSIVE_CRITICAL_GATE.** This is independent emulator testing, not a universal PASS or release authorization. No confirmed new F1 release-blocking ROM defect was reproduced. The exact bounded Pachinko bug has an independent negative control and F1 correction. Remaining critical TIA beam timing, worst-case stack/RAM, sprite collision pixel matrix and physical-console tests are not fully discharged.

## Frozen candidate
- PR #71, exact frozen commit: `3182809e161cfa3a3520b4de60638a3d1c661bfb` (open draft, unmerged).
- Original complete ZIP 23,622,499 bytes, SHA256 `3556df6c0ce21324efd56ccfbbb2a8e757a13bae3fc4c3a16eb5c3bdc5f42862`; original 852/852 manifest PASS.
- Independent real DASM 2.20.14.1 F6/NTSC rebuild = 16,384 bytes, SHA256 `f6677d53585f4e80be2cf5a435467406a0ad0d28c078d80375c2af44f9875a26`; frozen PR70 D rebuilt with SHA256 `50f105a3ccfb6cdcc6921c50b1ef2f042246d475d0ec33edee0a6dd893920f1a`. Only bank 2 differs. Five frozen GitHub source blobs also match.

## Independent executable evidence
- **Stella 6.7.1 actual debugger**: reproduction of former D 264-line interval (16x262, 1x264) versus F1 17x262, with audio deferred at frame12 and resumed frame13.
- Ten independent INTIM-budget synthetic fixtures, three different dual-audio fixtures and a native no-RAM-injection hold sequence: all native F1 sequences combined **674 measured 262-line intervals**, no new observed excess.
- Actual named TIA PC breakpoint sites included late **GRP1 cycle 47**, exceeding the previously summarized cycle40 sample maximum. This is not proven an illegal write because of VDELP1; exhaustive physical beam/deadline analysis remains unverified.
- Genuine stack mirror write instrumentation: 12,165 writes in natural hold and 896 in world8/L3; observed minimum SP `$F2`, but this does not establish worst-case stack bounds.
- Twelve U1-LEG1 A/B/facing/level P0 tables are byte-exact to frozen source; preserved 768 PF1 bytes hash `4c52651d7eca55e8e5c5158d33c90bec6bbd4f85e1732e65cf94321cd2b5334d`. This does not fully validate rendered multi-object pixels.
- **Stella 7** natural real joystick/audio: 9,000 consecutive frames / 150 sec, all eight levels, 22 stage transitions, 8,431 level3 frames; separate 2,100 frame sweep; natural life-loss + RESET (3->2->1->0, then 3). Real recorded stereo PCM, video; no source/ROM patches.
- Ranger: 36 newly generated **synthetic state injected** emulator comparisons across 4 worlds x 3 levels x 3 motion patterns; approach 28 vs knight24 straight, 24 vs20 diagonal, Ranger32 retreat. Not a proof of all Ranger escape edge-pairs, LOS or fully reachable native states.

## Remaining critical / not tested
- **INCONCLUSIVE**: full 76-cycle beamdeadline matrix including late GRP1/VDELP1, worst-case RIOT+stack and INTIM underflow, sound queue starvation limit, all same-Y and full on-screen object pixel oracles, complete Ranger edge/LOS scenarios, subjective play/audio.
- **NOT TESTED**: physical Atari 2600 / RetroN77, actual human play/ear tests, PAL.
- Source/design decision for MAIN V: candidate uses level display heights 12/20/30 versus earlier provisional 12/24/36, and bonus-life threshold 5,000 instead of old 2,000. Broad FULLGAME-1 developer delegation may cover experimentation; no final aesthetic approval implied.

## Package and reproducibility
- Complete new independent ZIP: [Google Drive](https://drive.google.com/file/d/1SPxVN-FYnH1O1emOJtl000Gv41dlpu9v/view?usp=drivesdk).
- Package: 3,422,647 bytes, SHA256 `ffa67307efeea90c6fafeb9139135f216b8d7a064901ff44d9b87ddb8fcb2c61`, 253 entries, 252 manifest SHA256 PASS, ZIP CRC PASS.
- Contains full Swedish report, test matrix, exact ROM+sources, DASM listings/symbols, independent scripts, raw native debugger commands/logs/screenshots, native traces and emulator gameplay video with WAV.
- Developer original delivery: [Issue #50](https://github.com/Odourman/the-skraun/issues/50), [PR71](https://github.com/Odourman/the-skraun/pull/71).

**Read-only verification:** no production code edits, no PR merge, no release, no prior negative evidence erased. MAIN V alone decides a tightly targeted closing gate and release authorization.