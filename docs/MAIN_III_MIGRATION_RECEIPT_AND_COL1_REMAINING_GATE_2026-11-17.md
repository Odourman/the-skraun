# THE SKRAUN — MAIN III migration receipt and remaining COL1 acceptance gate
**2026-11-17 | MAIN project coordination; evidence receipt, not implementation, independent verification or full-game approval**

## Source-of-truth and authority
MAIN III has directly inspected the connected GitHub repository, main/current branches, migration in GitHub and Google Drive, design decisions 01–60 plus later visual/Level3 user constraints, current project status, the full existing P01-COL1 work order, PR #27 + #26, issues #24/#25, actual Actions job steps/logs and relevant PF-REP1/B/C and two all-30-trick audits. This note supersedes **older status claims** in the original migration snapshot, **not** the original work-order authority or game design.

- Main HEAD observed before this receipt: `0d0a107f728ada825ad43b589fc2507e6b2522b4`.
- Existing ROM DEVELOPMENT P01-COL1 draft PR #27: https://github.com/Odourman/the-skraun/pull/27
- Existing isolated branch: `experiment/p01-col1-single-arena-collision-20261117` at observed HEAD `3ac5799edc8adf5e63a901229bfb31ad2681402e`.
- Binding scope: https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_ROM_DEV_P01_COL1_ONE_ARENA_COLLISION_DIAGNOSTIC_AUTHORIZED_2026-11-16.md
- MAIN III directed the **remaining work inside this same authorization** by comment https://github.com/Odourman/the-skraun/pull/27#issuecomment-6947066982 ; no new ROM, duplicate branch or renderer authorization.

## PASS / FAIL / NOT TESTED, based on live evidence
| Subject | Disposition | Specific evidence and limits |
|---|---|---|
| K0 geometry / user-accepted U1-LEG1 exact source | Developer source-model PASS | 332,232 legal 8-direction cases, 48 ROM collision table bytes; one synthetic four-solid arena, not eight canonical maps |
| Genuine DASM NTSC ROM | PASS build, not integrated game | 4,096 bytes, SHA-256 `f36217f9ae96a1e927795ca639b9d6b6cca68ad3e8e4f296afadcdb52d6a6ad2`, actual Actions [44075138086](https://github.com/Odourman/the-skraun/actions/runs/44075138086) |
| Compiled ROM 6502/RIOT/WSYNC subset model | Developer self-test PASS | Eight joystick directions, corner-slide, synthetic obstacle contact, growth permitted/refused, model 262 nominal lines; *not* genuine TIA/Stella state proof |
| Authentic Stella 6.7.1 sprite pixels | Bounded developer PASS | [44075138086](https://github.com/Odourman/the-skraun/actions/runs/44075138086), L1/L2/L3 8x12 /16x24 /32x36 logical A pixel masks; visual LEFT A+B samples, movement RIGHT, no L3 excess/clipped row in **this diagnostic** |
| Genuine Stella frame readout | Partial / insufficient for final full timing | [44074822309](https://github.com/Odourman/the-skraun/actions/runs/44074822309) shows `_scanEnd #261` on zero-indexed counter and `_fCount #10`, consistent with 262. Later [44075138084](https://github.com/Odourman/the-skraun/actions/runs/44075138084) completed but `saveSes` text is empty, logs include X11 BadWindow warnings; no machine-readable comprehensive debugger cycle trace |
| Controlled genuine Stella blocked corner / obstacle sides / L2→L3 refusal | NOT YET PROVEN | Present compiler subset model and source oracle do not satisfy actual Stella state acceptance |
| Complete 6507 worst-case VBLANK/overscan, page-cross, stack and frame timing | NOT YET PROVEN | No actual conservative full-path and run-time budget accepted |
| Original R3 full-scene (P0 + independent same-Y enemies + gold halo + distinct obstacles) | NO-GO for R3 tested methods | ~20Hz P1 enemy visibility, 30/30 halo/PF interlace or merged colour; worst visible lines ~2–4 static cycles spare even before remaining objects |
| Formal independent VERIFICATION | NOT RUN | Developer / MAIN tests never count as the separate Verification role |

The earlier run [44073915789](https://github.com/Odourman/the-skraun/actions/runs/44073915789) failed `pid: unbound variable` due to shell quoting. This is **superseded** by later successful runs; it is neither a pending fix nor evidence of defective game ASM.

Original MAIN II frozen Drive ROM/Stella evidence: https://drive.google.com/file/d/1Gl15LKcIGIQhMTPJf0G3tZ2hKOYgQshR/view (35-file ZIP, previously checked SHA256 `a409c36aaaa651096cd686ad93238b50d47d276fe34ad7d7931f6064089b9487`). No claim that MAIN III re-downloaded and rehashed this ZIP independently in the present session; current verdict primarily uses live Actions logs and source.

## PF-REP1 research remains separate
- [Issue #25](https://github.com/Odourman/the-skraun/issues/25) OPEN and [draft PR #26](https://github.com/Odourman/the-skraun/pull/26) unmerged; PF-REP1/B/C source data and replay reports reviewed.
- Simple unchanged Hugg one-PF-register-per-two-line scheme FAIL for original R3 mask transitions at all 13 X. Idealized sparse stores and 3-cycle hypothetical window success do **not** prove a 6507 full renderer.
- PF-REP1B naive conditional five-cycle schedules FAIL for 56/60 of 416 mixed lines under hypothetical halo/scenery priorities; two-cycle window sensitivity means **not a universal NO-GO**.
- PF-REP1C shows single unrepositioned Missile/NUSIZ fixed-copy cannot represent three separated synthetic obstacle strips, and Venetian alternation keeps 150/184 halo and 48/96 scenery source cell-lines; does **not** establish real visibility/TV perception or universal TIA impossibility.
- Independent gold halo vs obstacle colour ownership, exact register deadlines, same-Y P1 three-enemy visibility, 128B RIOT/stack and real 6507 cycle plan remain OPEN. No R4/B3c/fullrenderer or mapper migration is authorized.

## Prioritization and STOP
1. **Complete already-authorized #24** in existing PR #27: real Stella/Debugger state-controlled obstacle/corner tests, allowed/blocked growth and level-3 movement, 262-frame proof under workload, conservative complete 6507 path/stack ledger. Read the scoped developer instruction in the PR comment linked above. If tooling blocks proof, report precise negative evidence instead of a false PASS.
2. MAIN III reviews the actual frozen next evidence, does not replace ROM DEVELOPMENT and does not prematurely activate independent Verification.
3. Maintain PF-REP1 #25 as advisory source-only; delay any new full-scene kernel authorization until a concrete physical resource/deadline hypothesis survives hard same-Y tests. Do not silently reduce knights, archer, halo visual identity, sparse solid obstacles, or approved sprite.
4. Preserve open quality gates [#1](https://github.com/Odourman/the-skraun/issues/1), [#15](https://github.com/Odourman/the-skraun/issues/15), [#19](https://github.com/Odourman/the-skraun/issues/19), [#23](https://github.com/Odourman/the-skraun/issues/23), [#24](https://github.com/Odourman/the-skraun/issues/24), [#25](https://github.com/Odourman/the-skraun/issues/25).

**No user-level gameplay or art decision changed. No implemented ROM or production merge was made by MAIN III in this receipt.**
