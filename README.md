# The Skraun

**The Skraun** is an Atari 2600 top-down action game about a four-legged troll fighting knights and a green archer.

## Project status (2026-11-16)

**Design established; P01 builds and renders in Stella, with independent verification still pending.** Three sprite sizes and rightward joystick movement passed automated real-emulator screenshot checks. Stella debugger timing, complete control/animation test and real hardware remain unverified.

The project currently has 60 gameplay design decisions documented in the MAIN conversation and its exported design log. Those decisions govern implementation; this README is only an overview.

### Core design constraints

- Eight screens in four worlds: forest (1–2), mountains (3–4), dream (5–6), and dark night (7–8).
- One green archer per screen. Two knights can be active at once; additional knights arrive after earlier ones are defeated.
- A moving, 360-degree magic halo replaces a physical weapon. It destroys enemies and arrows, and passes through obstacles.
- The troll grows through levels 1–3 by collecting one orb per screen. A hit lowers its level; a hit at level 1 costs a life.
- **Level 3 must feel overpowered**; do not add difficulty scaling that nullifies player progression.
- When the eighth screen is cleared, the sequence reverses: 1→8, 8→1, 1→8, and so forth. Difficulty does not increase between loops.
- Simple, sparse solid obstacles stop arrows and sword attacks but not the troll's halo.
- Target authentic Atari 2600 hardware, with NTSC first and PAL examined separately.

## Development and verification

A working prototype must be reproducible from its 6502 source and a documented build procedure. Source changes, emulator screenshots, cycle/scanline measurements and a build log are not substitutes for independent verification.

Recommended gates:
1. **P01:** Display and move the troll; investigate three sizes and simple leg animation.
2. **P02:** Render a halo centered on the moving troll; separately establish collision logic.
3. **P03:** Stress-test sprite reuse for the troll, two knights and the archer, with projectile and orb.
4. **P04:** Implement a small combat arena and the agreed rules.
5. **P05:** Integrate progression, scoring, level transitions, and world order.

Each gate requires a testable artifact and explicit statement of what was actually verified. Do not treat design or feasibility research as successful implementation.

See [the first prototype gate](docs/PROTOTYPE_01_PLAN.md).

## License

No license has been selected yet. Do not assume permission to reuse this project's original assets or code.


## Design, research and CI

- [MAIN design decisions 01–60](docs/DESIGN_DECISIONS_01-60_2026-11-16.md) — the gameplay rules to preserve, including the level-3 overpowered design and reversed world order.
- [Atari 2600 comparison, decisions 01–60](docs/ATARI2600_COMPARISON_01-60_2026-11-16.md) — advisory research and engineering risks; not implementation proof.
- [P01 prototype plan](docs/PROTOTYPE_01_PLAN.md) — source implemented; independent runtime approval pending.
- [P01 source code](src/main.asm) — 6502 / DASM movement, three sizes and two leg poses.
- [P01 build report](docs/P01_BUILD_REPORT_2026-11-16.md) — CI evidence, SHA-256 and still-open tests.
- [P01 Stella screenshot evidence](docs/P01_STELLA_VISUAL_EVIDENCE_2026-11-16.md) — actual emulator PNGs, three sizes, rightward motion and test limitations.
- [GitHub Actions CI](.github/workflows/ci.yml) — checks document completeness on pushes and pull requests. With `src/main.asm` present, also assembles a 4 KiB NTSC prototype with DASM and publishes its ROM, listing, symbols and SHA-256 as a workflow artifact.

Regular CI verifies assembly and model-based logic. Separate Stella visual CI verifies three sprite sizes and one movement direction. **Neither is independent verification or proof of original-hardware timing.**

Google Drive retains a separate project folder named **THE SKRAUN - Atari 2600**, including historic decisions 01–19 and exported decisions 01–60. GitHub provides the tracked code, CI and revisioned engineering documents.
