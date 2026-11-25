# THE SKRAUN – HEALTH-2 final technical report

Date: 2026-11-25  
Scope: MAIN V HEALTH-2, isolated experiment branch.  
Evidence classes used: SOURCE_ONLY, HEALTH_OBSERVED, DEVELOPER_OBSERVED. No MAIN_REVIEWED or INDEPENDENT_VERIFICATION evidence is claimed.

## Executive result

HEALTH-2 improved the test harness and exposed false intent/PASS conditions. The frozen F6 NTSC ROM rebuilt with DASM. Natural joystick runs captured full 128-byte RIOT RAM and selected game state. A separate Stage 2 / Level 2 transition assertion passed. The harness also measured 120 individual frame endpoints, each 262 raster lines.

This is not full engine qualification. Dynamic CPU counters were unavailable because Stella did not find the expected listing and symbol files in natural-scene sessions. There is no per-scanline CPU/deadline proof, stack high-water measurement, full RAM lifetime proof, complete halo, three-enemy renderer, collision matrix or full natural level loop.

## Provenance

- Frozen baseline branch: experiment/fullgame1-romdev-v-halo-rim-20261125 at a194d744be7bf521b661b4d5af41e0525b480559.
- Baseline ROM: 16,384 bytes, SHA-256 bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5.
- HEALTH-2 branch: experiment/health2-deep-debug-optimization-20261125.
- Resume HEAD: e69b65d230a4f66e8c352b12089a47e2d8d3c033.
- Final Actions run: #45672925822 at HEAD 2c4981f2cedf4ed55e152de9704a9fb5e7262591; artifact #15048879739, 1,412,969 bytes, digest f6073b8382931f86b66a6416b3284f2a936707097bf540b8ad3cebd8bd49d032. Workflow conclusion is failure because known assertions fail and the cycle parser correctly stops on missing debugger symbols. Artifact upload succeeded.
- Earlier runs: [#45670054471](https://github.com/Odourman/the-skraun/actions/runs/45670054471), [#45669092999](https://github.com/Odourman/the-skraun/actions/runs/45669092999). Rejected position experiment ROM SHA-256 cc65326332c1b53578e957420454e5efd711a481d99c17d8681d42b8cb32fa63.
- No active ROMDEV branch, main, mapper, canon, merge, release or independent verification was changed or initiated.

## State assertions and harness repair

Latest Actions state results: 9 PASS, 3 FAIL, 1 UNPROVEN. The scenarios save the actual RAM command output after natural joystick sequences; tests do not write RAM or PC. This is a final-state probe, not a per-frame trace.

| Assertion | Result | Observation |
|---|---|---|
| Start: Stage 1, Level 1, 3 lives | PASS | Expected state |
| Knight warning / strike / rest | PASS | Correct timers observed; strike sampled at adjusted frame 23 |
| Active arrow first / mid / later | PASS ×3 | Arrow active at capture |
| Ranger arrow phase samples | PASS | Five distinct arrow coordinates; endpoint samples only |
| Stage transition | PASS | Stage 2, Level 2; StageKills=0; KillsNeed=3 |
| ranger_draw | FAIL | RDraw=0; arrow already active |
| ranger_release | FAIL | RRelease=0 despite active arrow |
| Legacy stage2_L3 | FAIL | Actual state Stage 2, Level 2, not Level 3 |
| gameover_restart | UNPROVEN | Only final RAM saved, no GameOver checkpoint |

The separate transition sequence waited through StagePause and passed Stage 2 / Level 2; it did not prove Level 3 upgrade. Do not report the scenario name stage2_L3 as evidence of Level 3.

An earlier stress_120 autoexec path created empty session files and is excluded as evidence. The replacement interactive measurement executed 120 distinct frame #1 steps and captured 120/120 values equal to 262 scanlines. This is frame-length evidence only.

The full RAM table is used for gameplay state. Stella may label numeric RIOT addresses using overlapping TIA register names in print *$xx output, so those labels alone are ambiguous.

## CPU, raster, TIA

NTSC has 76 6507 cycles per physical scanline. Stella Debugger documents its scanline, cycle and frame counters; Atari Stella Programmer's Guide documents TIA timing and HMOVE constraints. Sources: [Stella Debugger](https://stella-emu.github.io/docs/debugger.html), [Atari Stella Programmer's Guide](https://web.atari.org/stellaes.pdf).

All 16 natural scene endpoints and the 120-frame probe read scanEnd=262. A 262-line frame does not establish 76-cycle compliance on every scanline, absence of late TIA writes, or worst-case deadlines.

The reusable cycle summary required fCycles, fWsyncCycles and fTimReadCycles. Natural sessions show Stella could not find the expected .lst/.sym files. Internal fields were absent and labels resolved to TIA registers; the parser stopped nonzero. This is a measured harness defect, not a CPU overrun. No dynamic CPU totals are reported. The remedy is to load verified absolute ROM/list/symbol paths and require ROM SHA, bank, expected symbol and PC before accepting counters.

A synthetic VisibleGate baseline-only fixture at PC $F406, bank 3 sampled scan=36, sCycles=13, fCycles=2744, fWsyncCycles=231/201, fTimReadCycles=770; P0/P1/M0/M1=64/33/52/122 and BL=40/107 across two phases. These are breakpoint samples, not per-line bounds or candidate equivalence. The candidate did not reach its expected session. No per-line worst case, branch/page-crossing enumeration, timer-margin proof or TIA beam-deadline test was completed.

### Fine-positioner patch

DASM built an isolated shared helper replacing five inline fine-position loops. SOURCE_ONLY path modeling over X=0..159: baseline mean 55.21875 cycles, candidate 60.53125, delta +5.3125; candidate slower at 105/160 X, equal at 15, faster at 40, range -8..+20. Modeled HMP byte matched across tested coordinates. Model includes the WSYNC instruction but excludes variable raster wait. Candidate Stella physical equivalence was not captured. The patch is rejected and not integrated.

## RAM, stack, banks

Static parsing of all four real DASM listings/symbols found 125 distinct addresses with declared RAM aliases and 150 literal TIA write sites. Listing occupancy and apparent $FF holes: bank 0 1,655/2,441; bank 1 503/3,593; bank 2 1,577/2,519; bank 3 3,974/122. Holes do not imply safe code space; ORGs, hotspots, vectors, tables and control flow still constrain placement.

No complete address lifetime/def-use graph, uninitialized read audit, all-bank return proof or dynamic stack high-water was completed. A final _sp=$FF sample is one post-pause value, not a peak. Suspected alias pairs EnemyBottom/ScratchIX, Voice0/WorldShift and Voice1/AuxMode require call-phase validation before they can be classified as safe or faulty.

## Halo, enemies, bugs and Atari techniques

No new full-ring halo candidate or three-full-enemy renderer was built. No visible-vs-logical halo/collision mask, simultaneous sprite pixel oracle, all-map traversability, collision matrix, natural complete stage loop, reproducible restart or long soak was completed. Current evidence does not prove those systems generally impossible; it does not qualify them either.

The original 30-trick Drive source and matrix were reviewed. The only new practical optimization attempt combined shared position code and fine-position reasoning; it regressed modeled cycles. The prior shared-HMOVE experiment with M1 moving 122 to 78 was not repeated. No Venetian-blinds, mid-scanline GRP/VDEL, NUSIZ, dynamic playfield halo or adaptive P0/P1 candidate was built and measured here. Such ideas remain hypotheses until checked with sprite/pixel evidence and actual deadlines.

## Finding register

| ID | HEALTH-2 state | Finding |
|---|---|---|
| HEALTH-001 | Not retested | Mirrored CTRLPF/REF pixel oracle needed |
| HEALTH-002 | Prior correction, not retested | BL width/collision/render alignment needs focused test |
| HEALTH-003 | Not retested | HUD PF2 / halo scratch overlap test needed |
| HEALTH-004 | Not retested | SELECT latch/audio alias test needed |
| HEALTH-005 | Not retested | RenderBottom/HUD lifetime test needed |
| HEALTH-006 | Open risk | INTIM/halo guard may preserve stale TIA values |
| HEALTH-007 | Open limitation | One full P1 silhouette despite three logical actors in tested renderer |
| HEALTH-008 | Unproven | No worst-case per-line 76-cycle / beam deadline proof |
| HEALTH-009 | Unproven | Stack high-water absent |
| HEALTH-010 | Unproven | Orb width versus collision radius matrix absent |
| HEALTH-011 | Observed | TIA labels in print *$xx can mislead about RIOT byte; full RAM dump is safer |
| HEALTH-012 | Observed | Legacy stage2_L3 state is Stage 2/Level 2; separate transition PASS |
| HEALTH-013 | Observed FAIL | Ranger draw/release timing misses sampled intended phase |
| HEALTH-014 | Unproven | No GameOver-to-restart checkpoint |
| HEALTH-015 | Harness repaired | Empty session test replaced by 120 explicit interactive steps |
| HEALTH-016 | SOURCE_ONLY rejected | Shared fine-positioner adds 5.31 mean cycles |
| HEALTH-017 | Harness defect | Candidate physical position session absent |
| HEALTH-018 | Harness defect | Natural sessions miss .sym/.lst; cycle counters absent |

## Repair recommendations

1. Fix Stella listing/symbol load using verified absolute paths. Require ROM SHA, bank, PC and expected symbol in every measurement session.
2. Retain RAM state probe. Add intermediate checkpoints for Ranger draw/release, Level 3, GameOver and restart; separate Stage 2 entry from level escalation.
3. Instrument the most expensive visible kernel and INTIM path for actual per-line cycle maxima, branch/page timing, TIA write positions and remaining timer margin.
4. Measure stack high-water with a documented sentinel build, then stress halo, two attacks, arrow, HUD, audio and stage transition together; quantify instrumentation overhead.
5. Build an address ownership/lifetime map and validate F6 hotspots and bank returns before reusing RAM or ROM holes.
6. Keep the /30 patch rejected. Require candidate ROM identity, physical TIA positions and pixel comparison before accepting future positioning optimizations.
7. Start bounded halo/enemy tests with pixel masks and actual simultaneous sprite silhouettes before designing full rendering architecture.

## Completion boundary

Delivered: repaired natural-state capture, explicit state assertions, separate Stage 2 transition, 120/120 frame endpoints, real DASM logs/listings/symbols/bank binaries/ROM, static RAM/TIA/ROM inventory, positioner patch/model, final Actions evidence package and checksums.

Not completed: CPU/raster deadline proof, dynamic CPU counters, stack high-water, full RAM lifetimes, positive tested repair/optimization, complete halo, three-enemy renderer, collision and map traversability matrices, full natural loop, restart, long soak and broad trick benchmarking. These remain explicitly open. The package is not MAIN review, independent verification or release approval.
