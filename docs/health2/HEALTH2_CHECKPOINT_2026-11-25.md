# THE SKRAUN – HEALTH-2 continuation checkpoint

**Status:** active, experimental only. No active ROM DEVELOPMENT branch, main, merge, release, or independent Verification was touched.

## Live provenance

- Repository: Odourman/the-skraun
- HEALTH-2 branch: experiment/health2-deep-debug-optimization-20261125
- Confirmed branch HEAD at resume: e69b65d230a4f66e8c352b12089a47e2d8d3c033
- HEAD message: HEALTH-2: sample transition before damage window
- Rebuilt F6/NTSC baseline candidate SHA-256: bb7db027779f96fc02cff5b92dc94113e8db6a4b4ecf20ad537a33e08db598a5, 16,384 bytes.
- Latest run: https://github.com/Odourman/the-skraun/actions/runs/45670054471, HEAD above, completed with expected state-assertion failure.
- Latest artifact: https://github.com/Odourman/the-skraun/actions/runs/45670054471/artifacts/15049232122, 1,408,384 bytes, digest sha256:8defe9dce99a7ddbcb39edd5852b57e43be6fd9076a418e7c56638eda58ff872.
- Prior run: https://github.com/Odourman/the-skraun/actions/runs/45669092999, commit 4b1ed971556daa7bb977c3c582d17474e9fb6c69.
- Prior artifact: https://github.com/Odourman/the-skraun/actions/runs/45669092999/artifacts/15048219538, 1,620,190 bytes, digest sha256:2a2b7602818e8ef50c440c783fdd1d41d4b56f86be2f3c966c7279883686b974.
- The 45670054471 artifact was downloaded and its local ZIP SHA-256 matched the GitHub artifact digest.

## Resumed findings

1. Latest natural joystick sequence reaches **Stage 2, Level 2**, not Level 3. The transition assertion now correctly passes only for Stage 2/Level 2; a separate legacy-named stage2_L3 capture fails the intended Level-3 assertion with actual Level 2. Do not call that test a Level-3 pass.
2. Latest scenario report: **9 pass, 3 fail, 1 unproven**. Failures are ranger draw, ranger release, and the Level-3 claim. Game-over followed by restart remains unproven because only the final state was saved.
3. All 16 captured scene endpoints report 262 scanlines. A separate 120-frame sequence records 262 scanlines in each of 120 consecutive frames. This proves frame-length stability in those sessions, not that each raster line stays within 76 CPU cycles or meets every TIA beam deadline.
4. The action's source inventory reports 125 RAM addresses, 150 static TIA write sites, and listing occupancy of 1,655 / 503 / 1,577 / 3,974 bytes in banks 0–3. Apparent unoccupied bytes are not automatically safe insertion space. The inventory explicitly does not prove RAM live ranges or stack safety.
5. Native stack high-water has **not** been measured. Existing _sp values are point-in-time debugger state only; no sentinel/high-water method was present in these captures.
6. The prior position-optimization Action did not produce a candidate Stella comparison: its comparison parser raised FileNotFoundError for ROMDEV_V_POSITIONS/phase_0/SESSION.txt. This is a harness/evidence failure, not position-equivalence evidence.
7. The proposed shared subtract-30 PositionFine routine is rejected on the available SOURCE_ONLY model: baseline mean 55.21875 cycles versus candidate 60.53125 (+5.3125); candidate is slower at 105 of 160 X coordinates, equal at 15, faster at 40, with a worst regression of 20 cycles. The separate physical test only showed two synthetic visible-gate cases before failing to preserve the candidate session.
8. The previous position test is explicitly a **synthetic debugger RAM fixture**, not a natural gameplay test. The 16 scenario state captures are **natural joystick sessions**.
9. Current HALO outer contour and three-enemy rendering remain incomplete: the tested ROM still has resource sharing among P0/P1/M0/M1/BL/PF, and a 262-line count does not establish correct source pixels or continuous halo coverage.

## Evidence downloaded into the resume workspace

- health2_artifact_45670054471.zip, extracted under health2_run_45670054471/
- health2_artifact_45669092999.zip, extracted under health2_run_45669092999/
- Exact branch sources fetched at the confirmed HEALTH-2 ref under health2_branch_snapshot/
- Project Sources 00–04 and the attached original HEALTH-2 order
- Google Drive's 30-trick review document; it supports practical combinations #03 Venetian, #05 dynamic PF, #08 two-line kernel, #09 VDEL, #12 raster colors, #14 specialized kernels, #17 missile/ball reuse, #21 timer scheduling, and #24 precomputed display data. It explicitly warns that Venetian Blinds adds no color plane or scanline cycles and that same-Y mobile enemies are unlike fixed chess pieces.

## Continue from here

- Preserve the baseline ROM and keep all changes on the HEALTH-2 branch.
- Add a reusable emitted-listing timing/beam-deadline analyzer and report its limits clearly.
- Repair the position-comparison harness only if the experiment is worth rerunning; the current speed model says this candidate should remain rejected.
- Add a real stack high-water instrumented diagnostic run, distinctly marked synthetic if it initializes RAM or changes control state.
- Continue targeted halo, enemy, collision, and navigation experiments only where actual builds and Stella evidence are achievable.
- Package the reports, source diffs, run logs, screenshots, ROMs, and failed experiments for MAIN V. Do not claim completion until measured evidence exists for each delivered item.
