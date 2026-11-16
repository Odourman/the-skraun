# THE SKRAUN — MAIN implementation authorization: P02-B3b (2026-11-16)

**Issued by:** MAIN (this project's main coordination chat)  
**Decision:** A, B and C accepted as **completed developer self-tests**, not independently verified, not merged into `main`.  
**ROM DEVELOPMENT next authorized scope:** one bounded P02-B3b research/implementation experiment, including playfield-resource coexistence diagnostics and measured resource budgets.  
**No independent VERIFICATION now.** MAIN deliberately defers independent verification until a substantial cohesive system is ready; ordinary DASM/Stella self-tests remain mandatory.

## 1. Checked entry state and authority

At issuance, GitHub `main` was `1c399a47674303d9c461acd0d7acdb33af124fa1`. Before proceeding, inspect the **actual** main head and experiments; this SHA is only a dated starting-point record.

Read:
- `docs/DESIGN_DECISIONS_01-60_2026-11-16.md` and later MAIN-approved `docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md`.
- [Full A/B/C ROM DEVELOPMENT handoff](https://github.com/Odourman/the-skraun/blob/experiment/romdev-c-b3a/docs/ROMDEV_ABC_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md).
- [A sprite/animation PR #8](https://github.com/Odourman/the-skraun/pull/8), commit `c5928c348f4892d34102657b4dfa8683c70ab896`.
- [B REFP0 PR #9](https://github.com/Odourman/the-skraun/pull/9), commit `c0af705d3947b3da8f4527bfc4e8c23501a66b5c`.
- [C asymmetric 3-position PF PR #10](https://github.com/Odourman/the-skraun/pull/10), latest observed branch head `c9e6b1ab0bdeffe83442960d8895441d5daa81da`.
- `docs/P02_B3_DYNAMIC_RING_GATE.md` in `experiment/p02-playfield-b2`, as **technical test plan**, not authorization to implement every later stage.

Reference C ROM SHA-256 `31dfcb8034ed7c37d89918df8c0600bfa1159d94830189122240d225cb817479` (4,096 bytes NTSC). Its directly observed Stella Debugger result is 262 scanlines at a sampled frame; its max 64/76 cycle visible-line estimate is **static instruction accounting**, not a full measured worst-case integrated profile. C renders three *precomputed* centers `x=56/80/104`, not joystick-following.

A/B/C were rebuilt in [GitHub Actions run #43892290269](https://github.com/Odourman/the-skraun/actions/runs/43892290269). Evidence folder: https://drive.google.com/drive/folders/1MyI-ZuVqSj_MwQRebn7C0emfxlU5jdeX.

## 2. Authorized task B3b: ring genuinely follows horizontal joystick

Build and repeatedly test a **new isolated real 6502/TIA NTSC ROM** that moves a level-2 Skraun position marker or gray P0 sprite **and** the asymmetric playfield magic ring together horizontally, based on real SWCHA joystick input rather than SELECT-based mode switching.

Required research result:
- Demonstrate continuous *logical* horizontal follow in quantized 4-TIA-color-clock steps, ideally all 13 centers `56,60,64,68,72,76,80,84,88,92,96,100,104` (or document a precise justified limitation). Show multiple consecutive direction changes rather than only separate fixed states.
- Hold vertical center constant and keep level 2 for this stage. Eight-direction movement, full vertical follow, three halo scales, FIRE, cooldown, collisions and combat are **not yet requested**.
- Center ring and P0 stay aligned within feasible 4-clock PF quantization (target <=2 TIA color clocks), with a clear measured policy for response latency and no screen clipping on the tested range.
- One or more runtime approaches may be investigated: compact ROM data, compressed row masks, PF register manipulation, efficient table indices or safe VBLANK/overscan precomputation. Avoid relying on 13 copies of 192-row full-screen bitmap tables or a framebuffer exceeding the 128-byte RAM capacity.
- Keep P1 available for future enemies. Use `REFP0` if it helps the P0 character; do not confuse horizontal reflect with vertical row order. Apply the corrected upright bitmap convention if using the B2/C descending scanline index.
- First attempt a clean 4K experiment. If a larger ROM mapping appears necessary, you may build a **separate research-only** size comparison, clearly labelled as such; do not commit to a production bankswitching format without MAIN approval.
- Fix ordinary regressions autonomously within this research task, recording instructive causes rather than asking MAIN after every iteration.

## 3. Mandatory feasibility probe: ring versus playfield scenery

The same TIA PF0/PF1/PF2 registers are also needed for future trees, stones and world layouts, and the current static C kernel reportedly uses up to 64 of 76 cycles per visible line.

As part of B3b, perform a **bounded coexistence experiment or conservative resource comparison** with a few synthetic obstacle playfield pixels/rows and a moving ring:
- Test/quantify what happens on rows occupied by both a ring and an obstacle. The collision truth is independent of this PF visualization.
- Determine whether clear simultaneous display is possible by masked composition or another bounded approach without losing critical gameplay visibility.
- Measure or conservatively estimate register-write count, additional compute time, available HBLANK/raster cycles, storage cost and visual tradeoffs. Compare the future headroom for P0, two knights, one archer, one arrow and HUD. This is an *engineering reservation*, **not** a request to implement enemy AI, full scenery, collisions or multiplexing now.
- If the PF architecture proves to be unsuitable, identify precise rejection reasons and compare credible alternatives (hybrid PF/object render, more compact mask design, different raster scheduling etc.) instead of making a cosmetic demo look production-ready.
- Do not sacrifice level-3 ring reach, future obstacles or enemy resources merely to pass a level-2 demo.

## 4. Tests, evidence and transparent status

For each relevant implementation candidate:
1. Commit exact source, test scripts, build command, ROM size and SHA-256 to a dedicated experiment branch, and preserve the tested artifact.
2. Show **actual** Stella 6.7.1 frames or a deterministic sequence of frames for sustained left movement, right movement, reversal, and representative centers. Distinguish these images from illustrations or AI-generated concept art.
3. Test ring contour/width, alignment, fixed Y, absence of unintended reflections and pixel clipping, and P0 orientation. Use fail-closed tests whenever a missing screenshot or blank debugger capture occurs.
4. Measure real NTSC frame lengths with Stella Debugger at multiple motion states, and calculate/measure the worst-case 6502 cycles for each used kernel path. Label calculated cycle bounds separately from *directly measured* debugger results. Carefully account for branching and page crosses.
5. Report RAM bytes, used/free ROM bytes, PF register usage, P1 availability, PF scenery competition, and expected limitations when added objects enter overlapping scanlines.
6. Compare against A/B/C static test artifacts and document whether the technical approach appears extensible or needs redesign.
7. Give **PASS / FAIL / BLOCKED / NOT TESTED** for B3b free horizontal follow and the separate scenery headroom probe. Do not claim complete P02 or production readiness from this narrow test.

## 5. Hard boundaries and stop conditions

- This authorization **ends after B3b and the bounded scenery-resource diagnostic**. Do not start B3c vertical/diagonal follow, 30-frame FIRE, 3-scale dynamic ring, full B3d enemy load, B3e collision implementation, backgrounds or mainline integration without a **new MAIN authorization**.
- Do not merge experimental branches to `main`, rewrite decisions 01–60, close P01 or any independent verification tickets, or claim independent verification.
- Do not establish a permanent artificial horizontal screen boundary because an early diagnostic used restricted edges; report workarounds and their consequences.
- Halt and report a material blocker if genuine motion cannot be sustained in a 262-line frame, PF resource conflicts make scenery impracticable, or a realistic timing estimate leaves too little room for the future game. Conduct bounded alternate-method analysis before declaring full impossibility.
- Independent VERIFICATION stays dormant. Repeated self-tests and CI are expected; MAIN will package larger completed systems later.

## 6. Delivery to MAIN

Deliver **one combined handoff**, not a report after every microiteration:
- Branch/commit(s), exact assembler sources, built ROM(s), SHA-256, test logs, Stella frames and debugger evidence linked in GitHub and Drive.
- Tested range and motion quality, centering error, worst-case per-line cycles (measured vs calculated), resource ledger, result of obstacle visibility conflict probe.
- Important findings, failed candidates and reproducible limitations.
- Recommendation whether MAIN should later authorize B3c, redesign the halo renderer, or conduct a different feasibility study.
- Explicit statement that work is a developer self-test with **no independent VERIFICATION**.

**Work autonomously within this authorized scope. Do not interrupt MAIN for routine coding, self-test or bug-fix choices; stop only when the scope is complete or an actual MAIN-level design/hardware tradeoff requires a new decision.**
