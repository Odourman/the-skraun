# THE SKRAUN — MAIN authorization for ROM DEVELOPMENT (2026-11-16)

**Authority:** MAIN, based on the user's delegation to continue using recommended decisions within authorized scope.  
**Status:** AUTHORIZED DEVELOPMENT SCOPE, not a verification PASS.  
**Verification policy:** No independent VERIFICATION in this sprint. Bundle evidence for one later substantial milestone when MAIN requests it.  
**Source baseline:** `main` commit `1ff760024a5d1a7b2b6685eb6db97b7e7492721f` at the time of this authorization. Before work, check live repository state and any later authoritative MAIN decisions.  
**Design authority:** `docs/DESIGN_DECISIONS_01-60_2026-11-16.md` and later user-approved gray overhead Skraun direction in `docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md`.

## ROM DEVELOPMENT: one continuous, ordered technical assignment

You have permission to implement, revise, build, debug and retest **the following three connected tasks**, in this order, without asking MAIN after every correction. Use experimental branches and real Atari 2600/NTSC-compatible 6502/TIA code. Stop after completing this scope and report the findings before any larger expansion.

### A. Gray Skraun orientation and walk-animation engineering self-test

Base your work on:
- `experiment/gray-topdown-skraun` (two A/B poses, 3 sizes, eight joystick directions);
- `fix/p02-gray-halo-upright` (corrected sprite row ordering for the descending raster kernel);
- user sketch/reference in project Google Drive, including overhead camera, light gray, two short moving poses and horizontal-only facing.

Check actual Stella frames, not just bitmap table content. Capture A and B in each horizontal facing direction, movement in eight directions, the two upper limbs swinging and two lower legs changing pose, and all three sprite sizes. Ensure there is no unwanted vertical inversion in any newly combined kernel. Record whether 8×12 sprite is visually recognizable; do not declare final art approval on the user's behalf. Record direct Stella Debugger NTSC timing as available; label any unmeasured timing NOT TESTED.

### B. Hardware mirroring optimization, `REFP0`

Implement and compare a **separate test candidate** where REFP0 bit 3 controls horizontal direction and only two A/B source bitmaps are stored. Confirm four outcomes (A right, B right, A left, B left) in actual Stella, including direction changes during movement. Check code size, RAM and worst-case timing versus the current four-table version. `REFP0` solves **horizontal** reflection only and MUST NOT replace the row-order fix.

If hardware mirroring exhibits limitations, retain the working four-table strategy as fallback and document why. Do not sacrifice readability, input responsiveness, or other agreed gameplay features for a small ROM saving.

### C. P02-B3a narrow feasibility experiment: moving halo centers at three fixed X values

After A and B are technically self-tested, build a **separate diagnostic ROM** testing an asymmetric playfield ring centered at logical TIA color-clock x=56, 80, 104, selected with a diagnostic console control (e.g., SELECT). Fixed Y and one sprite power level (level 2) are sufficient. A true moving ring, joystick-following, FIRE cooldown, collisions, enemies and complete world backgrounds are **not part of this scope**.

The ring must keep the same readable outline and size at all three centers, and the left and right playfield halves must display appropriately even though they are no longer simply mirrored about x=80. Measure whether PF updates can coexist on the same scanlines as a P0 placeholder/gray Skraun without exceeding the 76-cycle CPU scanline budget. Preserve P1 for future enemies. Record ROM bytes, 128-byte RAM footprint, register writes, approximate/observed worst-case scanline cycles, measured Stella frame lines where practical, and any graphical discontinuities or clipping.

Prefer genuine Stella screenshots and debugger measurements over models. A model-only PASS must be labeled as such. Explicitly compare feasibility and resource costs against P02-A (P1 halo) and B1/B2 (centered mirrored PF), which are evidence-only experiments, not production renderers.

## Engineering authority and constraints

- You may independently iterate and fix code within A/B/C, including necessary tests, CI, visual diagnostics and documentation. Do not interrupt MAIN for small assembler or test-harness decisions.
- **Do not merge into `main`**, close historical P01/P02 verification issues, mark an experiment as production-ready, or modify design decisions 01–60 without a new MAIN decision.
- Do not silently introduce a new sprite design, new character facing up/down, altered combat rules, altered power levels, or changes to the eight-stage game loop.
- If B3a proves impossible within Atari 2600 timing/resources, conduct bounded comparisons and report the specific reason and alternatives; do not claim a solution on the basis of compilation alone.
- Do not start P02-B3b/B3c (free-following moving halo), combat engine, extra bank-switching architecture or world implementation under this authorization. Those are possible future scopes that MAIN will authorize separately.
- Existing independent VERIFICATION issues may remain open but must **not trigger a verification request** during this sprint. Development self-tests are mandatory; external verification is deferred until MAIN bundles a substantial milestone.

## Required consolidated handoff to MAIN

At the end of this assignment, deliver:
1. Exact branch(es), commits, changed file paths and build commands.
2. Compiled ROM(s) with file sizes and SHA-256, test instructions and current Google Drive/GitHub links.
3. Actual Stella screenshot evidence for A/B poses, left/right reflection, and 3 halo centers.
4. CPU cycles / scanlines / RAM / ROM measurements with explicit self-test versus independently measured distinctions.
5. PASS/FAIL/NOT TESTED and defects for each scope A, B and C.
6. Comparison of REFP0 versus four sprites; comparison of B3a asymmetric PF versus prior halo techniques.
7. Practical recommendation to MAIN for next step, with honest limitations and no request for premature independent verification.

**Scope completion ends at B3a feasibility evidence.** MAIN will decide the next authorization based on the report.
