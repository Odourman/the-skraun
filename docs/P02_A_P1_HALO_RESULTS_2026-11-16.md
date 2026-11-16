# THE SKRAUN — P02-A P1 halo experiment: measured findings

**Date:** 2026-11-16
**Scope:** Technical experiment only. No MAIN gameplay decisions 01–60 changed.
**State:** Executable / Stella visual self-test PASS; **not a viable final halo implementation**, not independently verified.
**Isolation:** `experiment/p02-halo-p1` branch; P01 `src/main.asm` and original P01 ROM are untouched.

## Reproducible output

- Source: `experiments/p02_halo_p1.asm` (DASM / 6502).
- Build: `dasm experiments/p02_halo_p1.asm -f3 -obuild/p02-halo-p1.bin -lbuild/p02-halo-p1.lst -sbuild/p02-halo-p1.sym`.
- Cartridge: 4 KiB NTSC.
- ROM SHA-256: `4b7812aeeea01a9bfd67e72efd07f69288d840440bc792463fabf9caa8b61eb8`.
- Full CI evidence: https://github.com/Odourman/the-skraun/actions/runs/43869068782
- CPU model: `experiments/p02_cpu_budget.py`, running automatically in CI.
- Screenshots from actual Stella 6.7.1 under Linux/Xvfb, not simulated paintings.

## Purpose and design constraints

A gold 360-degree ring overlays the green troll, with a provisional 30 NTSC-frame duration (~0.5 s) and level-dependent cooldown (60, 36, or 15 frames). Level changes through diagnostic console SELECT; FIRE triggers the ring and held FIRE repeats after cooldown. This experiment implements **graphics and trigger timing only**; it does not implement enemy hits, arrow destruction, obstacles, or gameplay progression.

The P1 player object is stretched via `NUSIZ1=5` (16 logical color clocks) for level 1 and `NUSIZ1=7` (32 clocks) for levels 2 and 3. The P0 troll retains the P01 three size concepts.

## Observed Stella screenshots (320×228, horizontal display pixels double logical TIA pixels)

| Scenario | Troll green x-range | Halo gold x-range | Halo gold y-range | Finding |
|---|---:|---:|---:|---|
| Level 1 fire | 122–137 | 106–137 | 112–131 | Visible but not horizontally centered |
| Level 2 fire | 124–155 | 104–167 | 100–131 | Visible and almost centered; left margin 20 pixels, right margin 12 |
| Level 3 fire | 124–187 | 108–171 | 86–133 | Does **not** enclose the full 32-logical-pixel-wide troll |
| Level 3 FIRE + RIGHT | 152–215 | 136–199 | 86–133 | Player and halo both move +28 captured pixels horizontally |

Actual screenshot files and full ASM listing are stored in the GitHub Actions artifact. The screenshot test checks all three SELECT stages and nonblank fire graphics.

## Timing findings

1. The initial naive two-sprite scanline kernel exceeded the 76-cycle budget when both graphics overlapped. A task-specific 6502/WSYNC model measured 274 lines at level 1 FIRE and 286 at level 2 FIRE. **FAIL**.
2. The revised kernel updates P0 and P1 on alternate scanlines while the halo is active, reducing workload. The same model subsequently measured **262 steady-state scanlines at level 1 and level 2 with FIRE active**. **MODEL PASS**.
3. Actual Stella displayed all sprites and input; however, **a full direct Stella Debugger timing/cycle audit during active halo has not been completed**, so the 262 model result must not be presented as definitive hardware timing proof.
4. The alternating-row technique reduces vertical bitmap update resolution while the ring is active. This is a design/visual risk even when scanline counts fit.

## Final suitability: REJECT as production approach in its present form

- P1 is one of Atari 2600's only two full player objects. Dedicating it to a halo prevents uncomplicated display of two knights and one archer; multiplexing or special drawing would still be required.
- A single stretched P1 tops out at 32 logical pixels wide. The level-3 troll itself is 32 logical pixels wide, leaving **no horizontal clearance** for a genuinely enclosing level-3 ring.
- Raster interleaving degrades vertical update precision and may produce flicker or pose inaccuracies under future enemy load.
- The level-1 ring is still visibly off-center, confirming that horizontal positioning needs better calibration.
- Halo blinking, hit radius, projectile collisions, obstacle-through-halo behavior, enemy stress, and independent verification are unfinished.

This is a **negative technical feasibility result with a successful executable demonstrator**. It is not a gameplay-design rejection and it does not weaken the agreed level-3 overpowered goal.

## Recommended next experiment: P02-B dynamic playfield ring

Investigate a 40-column coarse playfield overlay to free P1 for enemies. It must show a moving ring with >32 logical pixel width at level 3, avoid flash-strobing, fit a 262-line NTSC frame, and keep collision logic separate. Evaluate ROM table size, 128-byte RAM, midscanline PF rewrites, visual coarseness at 4-pixel resolution and placeholder enemy sprites. Do not make any P02-B technology or bank-size decision until actual ROM tests support it.

## Acceptance and project boundaries

P01 separate independent verification remains open: https://github.com/Odourman/the-skraun/issues/1 . This P02-A report is developer self-evaluation; it does not independently approve P01 or P02. The original 60 gameplay rules remain unchanged.
