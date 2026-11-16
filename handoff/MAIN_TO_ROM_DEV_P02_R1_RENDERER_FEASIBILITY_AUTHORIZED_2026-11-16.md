# THE SKRAUN — MAIN AUTHORIZED SCOPE: P02-R1 RENDERER ARCHITECTURE FEASIBILITY
**Date:** 2026-11-16
**Authority:** MAIN
**Status:** New bounded ROM DEVELOPMENT research/implementation assignment. **Not B3c. No main merge. No independent VERIFICATION at this milestone.**

## 1. Why MAIN authorizes R1

MAIN accepts P02-B3b as a **completed limited developer self-test** after examining the submitted branch, technical handoff and green Stella/Debugger workflows. This is not approval for production integration.

Verified deliverable references:
- B3b branch: `experiment/romdev-b3b-horizontal-follow`; reviewed head `67cb3ef368b460b9062d3d965aa8e25a0a276c3c`.
- [Draft PR #11](https://github.com/Odourman/the-skraun/pull/11), targeting B3a experiment, not `main`.
- [B3b full technical report](https://github.com/Odourman/the-skraun/blob/experiment/romdev-b3b-horizontal-follow/docs/ROMDEV_B3B_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md).
- [Final Stella image regression](https://github.com/Odourman/the-skraun/actions/runs/43901341243) and [live-joystick Stella Debugger timing](https://github.com/Odourman/the-skraun/actions/runs/43900278446): completed/success at time of MAIN review.
- [B3b Google Drive evidence](https://drive.google.com/drive/folders/1fn4RTvPreT6dsVQD5HUaLYIRPfLffz8h).
- Baseline B3b ROM hashes, both 4096-byte NTSC: dynamic `7d96bcb71532643307922f62814900b09a1525ede06795c17417607634efd060`; precombined obstacle `31b859d711bb08228b03015f9039b1df97c77628ab3637f754ad3df77b599bbe`.

### Confirmed bounded findings, and what remains unproved
- Real SWCHA joystick input chooses **13 four-color-clock horizontal centers**, `56..104`; P0 and ring stay aligned. However, one step only happens **every 16 NTSC frames**, up to ~250 ms first-response latency; this is NOT playable-final control responsiveness.
- Static worst-case raster accounting from DASM data: **63/76 cycles** including the next WSYNC, leaving **13 cycles** before full scenery/enemies/HUD. This is a **calculated** limit, not directly profiled per-instruction in the eventual integrated game.
- 262-line NTSC frames were **observed directly in Stella Debugger** in four motion states, not a proof of spare CPU headroom.
- Synthetic PF scenery is **precomposed into the ROM** by OR and shares one PF color with the halo; intersecting or player-occluded pixels become visually indistinguishable.
- Runtime OR with arbitrary scenery requires at least ~16 further cycles for four dynamic byte reads (before OR overhead), exceeding 76 cycles in this unchanged kernel; this architecture is **NOT** approved for flexible full-game backdrops.
- P1 is unused in the diagnostic, but there is **no proven rendering of two knights + one archer + one arrow + HUD** with this kernel.
- `main` is unchanged by B3b. A/B/C and B3b are developer experiments, not independently verified.

**MAIN technical decision:** Do not start B3c by simply adding vertical movement, FIRE and scales to the same 63-cycle kernel. First compare whether a realistic scene-capable architecture exists.

## 2. Authorized work: P02-R1, an independent renderer feasibility package

ROM DEVELOPMENT may implement, revise, optimize and self-test **one bounded renderer study** in a new experimental branch, with necessary alternatives and tests, without requesting MAIN approval for ordinary debugging.

### R1-A: improve horizontal input response in diagnostic ROM
- Replace the artificial 16-frame joystick movement gate with a responsive test control method (target first response <=2 NTSC frames; target update every 1–4 frames while held, documenting speed and quantized accuracy). This is a **diagnostic control test only**, not the complete movement rule.
- Retain 13 calibrated horizontal centers as a reproducible test grid. Do not introduce permanent gameplay edge restrictions.
- Keep P0+halo aligned, correct upright Skraun orientation, stable 262 NTSC scanlines in typical and reversal states.
- Record actual response latency and held-direction speed with deterministic input/frame tests; don't call it playable-final based only on fixed frame count.

### R1-B: compare renderer architectures for visible halo AND independently meaningful scenery
Implement small diagnostic variants where practical, or give bounded cycle/ROM/RAM analysis if hardware makes a proposed variant impossible:
1. **Optimized asymmetric PF**: reduce register writes/table fetches, reuse masks, shift expensive work to VBLANK/overscan or encode/compress scenery+ring masks without full 13-position × 8-stage duplication. Test obstacles overlapping ring rows in Stella.
2. **Layering/scheduling alternatives**: investigate time-multiplexed/color-timed PF display, bounded row partitioning or other TIA tricks. Distinguish true independent colors/layers from a same-color OR. Quantify tearing, flicker, scoremode/color artifacts and scanline deadlines. A visual effect is not acceptable if it destroys obstacle visibility or game readability.
3. **Hybrid object/PF**: study playfield reserved for environment while parts of halo use player/missile/ball resources or carefully budgeted multiplex. **Account explicitly for P1's future enemy duty**. Using P1 for the ring is not automatically acceptable: P02-A showed width and resource drawbacks.
These are options to test/compare, NOT a requirement to force all three into fully runnable ROMs. Prioritize the few best technically justified experiments.

Maintain level-3 design constraint: the eventually projected ring must be larger and more powerful than the level-3 sprite; a level-2-only feasibility ROM is not proof. Do not weaken the gameplay to accommodate a renderer.

### R1-C: credible worst-case object/HUD headroom
- Construct a **synthetic timing/resource load** modelling the register writes, per-scanline cycles and object slots required for **P0 Skraun + two knights + one archer + one arrow + orb + HUD** on overlapping rows. This is a feasibility harness, NOT authorized full enemy behavior or AI.
- Count cycles using real assembled symbols and all relevant page crossings, especially mid-line right-half PF handoffs. Prefer additionally obtaining direct Stella Debugger instruction/scanline traces for the limiting paths. A 262-line frame **without objects rendered** is insufficient proof.
- Explicitly budget sprite allocation/multiplex and missile/ball use, RAM, ROM and possible costs of obstacle collision geometry (collision truth independent from visual PF bits). If a full multi-actor synthetic runtime kernel is not feasible, document precise hard costs and show feasible alternatives rather than fabricating a PASS.
- Optional *research-only* ROM-size comparisons (4K vs a documented banked 8K/16K candidate) are allowed IF useful. **Do not choose or integrate a production bankswitch scheme as part of this scope.** Extra ROM storage is not extra 6507 scanline CPU time.

## 3. Minimum evidence and decision gates
- Build real original-compatible Atari 2600 NTSC ROMs with DASM. Save exact source/commit, 4096/8192/etc actual sizes, SHA-256, listing/symbols and test commands; use a new dedicated research branch/PR, not `main`.
- Capture **actual Stella 6.7.1 screenshots** of multiple consecutive joystick inputs, reversals and ring+obstacle overlaps; labels must distinguish illustration versus authentic emulator images.
- Test worst-case PF right-half timing deadlines and ordinary frame count. Check 262-line frames with Stella Debugger on meaningful paths. State **STATIC CALCULATION** versus **DIRECT DEBUGGER MEASUREMENT** clearly.
- Give a compact, quantitatively comparable table for each serious candidate: available PF colors/layers, P1 availability, maximum raster cycles, remaining CPU margin, RAM use, ROM mask growth per scene/position, obstacle visibility, level-3 promise, flicker risk, and object/HUD headroom.
- Explicit **PASS / FAIL / BLOCKED / NOT TESTED** for responsive control, visual differentiation, raster cycle capacity, and combined resource feasibility. Do not declare a fully playable game.
- Deliver one consolidated research+ROM report with reproducible evidence and recommendation: pursue renderer X for future B3c, redesign again, or elevate a concrete unavoidable design/hardware choice to MAIN.

## 4. Hard exclusions
- **No B3c** vertical/diagonal free following, 3 dynamic scales, 30-frame FIRE/cooldown.
- **No B3d** finished multiple-actor animation/AI; only synthetic timing/slot estimates.
- **No B3e** combat/collision implementation; only separate collision-budget analysis.
- No permanent eight-world scenery, HUD implementation, enemy behavior, new gameplay rules or final graphics sign-off.
- No production branch merge, no unilateral permanent bank scheme or final halo render choice, no closure of independent verification tickets.
- **No independent VERIFICATION this round.** MAIN has explicitly chosen milestone-batched verification. ROM DEVELOPMENT must keep automated and manual engineering self-tests.
- If no approach supports ring+visible scenery+credible enemy capacity, clearly stop and report rejection evidence; do not hide constraints by narrowing the permanent playfield, reducing level-3 range or assuming impossible free P1 slots.

## 5. End of authorization
This authorization is **P02-R1 only**. Upon completing its bounded comparisons, ROM DEVELOPMENT returns a single report to MAIN. MAIN alone decides whether to authorize B3c or another design/engineering step. Implementing one R1 diagnostic does not authorize the rest of the game's renderer.
