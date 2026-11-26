# THE SKRAUN — VERIFICATION II / FINAL CRITICAL GATE CLOSURE (2026-11-26)

**FINAL: `INCONCLUSIVE_CRITICAL_GATE`.** Frozen PR71/F1 still open, draft, unmerged, original code commit `3182809e161cfa3a3520b4de60638a3d1c661bfb`. This branch is **verification documentation only**; no code edits or release.

**Frozen ROM:** actual fresh DASM 2.20.14.1 F6/NTSC rebuild, 16,384 bytes, byte-identical to reference, SHA-256 `f6677d53585f4e80be2cf5a435467406a0ad0d28c078d80375c2af44f9875a26`. Original developer ZIP and prior independent evidence preserved.

## Gate A: `PASS_BOUNDED_NATIVE_STELLA`
Independent Stella6.7.1 debugger, world8/L3 dual-load + three actors same-Y mixed poses + X-edge scenes. Each scene 2,208 second-line GRP1 PC events, total 6,624; `STA GRP1` at bank3 `F181`, measured completed cycles 40–47. VDELP1 activated in Reset, visible P1 delayed latch is consumed by next pair's GRP0 at cycle3. **Min observed 32 cycles =96 colorclocks** to next GRP0 transfer; independent conservative indexed/pagecross upper bound cycle50 -> 29 cycles/87 colorclocks. First/second-row GRP0 cycle3; ENAM1 cycle15; ENAM0 cycle23, earliest permitted halo M0 x>=4. Special PF1 color line reaches cycle28 exactly at first PF1 cell but source blank path and sampled Stella pixels did not show leakage. Six new native P1 K1-neutral screenshots exact 116/116 mask pixels; four prior developer L3-left screenshots independently rescored 4/4, explicitly not new captures. Other per-object matrix is NOT FULLY TESTED.

## Gate B: `PASS_BOUNDED_STATIC_AND_NATIVE`
Independent all-branch, F6 hotspot aware 6507 callgraph on frozen compiled banks: 15,200 states, max seven JSR nesting, no reachable unbalanced returns/recursion in model; `SP=$FF-14=$F1` bound. Actual independent Stella RIOT stack mirror `$01F0–$01FF` instrumentation observed min SP `$F2`; stack-reserved `F0–FF` retains 2 unused bytes at static bound, voice bytes `EE/EF` not overwritten by stack in modeled paths. Synthetic fixtures do not prove natural state reachability.

## Gate C: `INCONCLUSIVE_CRITICAL_GATE` — timer read-order race
- Independent bank1 audio control-flow overbound across 320 path combinations: at most **249 CPU cycles** in AudioEngine `F100–F1B7` (pessimistic indexed crossing).
- Native Stella `INTIM=6` frame12 sample: CMP `2:F031` scan252/cycle57; bank1 AudioEngine `1:F100` scan252/cycle69 → `1:F1B7` scan255/cycle65 (224 cycles); `2:F6ED` scan255/cycle72 (243 cycles from CMP to return); resulting NTSC 262-raster interval.
- Eight consecutive **synthetic** sound deferrals, frames19–26, each 262 lines, no TIA audio writes or voice `EE/EF` changes while deferred; frame27 resumes AudioEngine with six real TIA AUD register writes. Legitimate event priority and SoundFrames `BF` updates continue, so no unconditional queue retention or starvation bound claimed.
- **New reproducible synthetic RIOT timer phase finding:** original bank2 `BIT TIMINT; BMI Defer; LDA INTIM; CMP #6; BCC Defer; JMP SoundBankEnter` can select SoundBankEnter if TIMINT is read just before underflow but INTIM afterward. Genuine Stella with frozen ROM and debugger-injected `TIM1T=2` at PC `2:F027`: flag N=1 at `2:F02A`, branch to Defer `2:F036`. With `TIM1T=7`: N=0 at `2:F02A`, later `INTIM=$FD` at `2:F02F`, takes `2:F033` to real AudioEngine `1:F100` after timer underflow. **This test changes RIOT timer midframe**, so its anomalous 249/252-line frames are **not** natural game failures. Natural reachability of this race is **NOT PROVEN**. But a valid physical timing phase is unguarded, hence no unrestricted emulator PASS.

**Recommended MAIN V decision:** Do not issue an unqualified PASS for frozen F1. Either explicitly accept bounded timer phase risk with recorded caveat, or separately authorize ROM DEVELOPMENT for a **single surgical control-order fix**: read/compare INTIM first, then recheck TIMINT immediately before entry into audio; run only targeted underflow + INTIM6 + eight-defer + SHA regression. No new broad Pachinko campaign. No implementation is authorized to VERIFICATION.

**NOT TESTED:** full remaining P0/P1/missile/orb/HUD pixel matrix, all Ranger LOS/edge pairs, physical original Atari 2600/RetroN77, PAL, human subjective play and listening.

## Evidence

**Full Swedish report, actual debugger logs/screens, independently rebuilt ROM+source+symbol/listings, complete scripts, fixtures, ZIP manifest:** [Google Drive verified ZIP](https://drive.google.com/file/d/1pmuh-XVLOi9Ac7VcwdXVKp49n-fQTF9_/view?usp=drivesdk).
- ZIP 608,154 bytes, SHA-256 `531f80f897f1efa94ad3a3b6b9fbf885a636bfc002c449f0e5773b48185d9726`.
- 118 ZIP entries, 117 SHA256 manifest lines, all PASS, ZIP CRC PASS.
- Reference: [PR71](https://github.com/Odourman/the-skraun/pull/71), [Issue50](https://github.com/Odourman/the-skraun/issues/50), [earlier independent readout](https://github.com/Odourman/the-skraun/blob/verification/pr71-f1-independent-20261126/verification/PR71_F1_INDEPENDENT_READOUT_2026-11-26.md).

**STOP:** no product modifications, main merge, external release, or unilateral approval. MAIN V receives final decision authority.