# THE SKRAUN – Atari 2600 sprite row-order audit and upright fix

Date: 2026-11-16
Review owner: MAIN
Status: **Technical defect found and fixed on an isolated experimental branch; verified by developer self-tests only.** Stable main implementation and independent gate remain unchanged.

## Why the monster appeared upside down

The Atari 2600 TIA generates a frame top-to-bottom. The register `GRP0` holds just one **horizontal** 8-bit player row and is overwritten by the 6507 as the display beam advances through scanlines. `WSYNC` synchronizes execution to the next scanline.

In the static combined prototype `experiments/p02_gray_static_halo.asm`, the visible routine starts `LDX #192` and for each output line executes `DEX`, `TAY`, `LDA (TrollPtr),Y`, `STA GRP0`. Consequently **the first visible line reads ROM table index 191 and the last reads index 0**.

The older combined ROM erroneously stored Troll1/2/3 data with the **topmost bitmap row in the lower addresses**. The decrementing index read the **feet first and the head last**, vertically flipping the sprite. The previous CI checked bounding boxes, colors and ring containment but did **not** check head/feet orientation. Thus its green status was incomplete, not proof of correct design. A static symmetrical golden playfield ring hid the error in the ring itself.

This does NOT mean that 2600 sprites universally must be authored upside-down. It means stored row order must match the kernel's memory access order. A kernel that indexes upwards requires the opposite order.

## Research verification

- Original Atari `Stella Programmer's Guide`, Steve Wright, 3 December 1979: TIA displays the television image top-to-bottom, one scanline at a time; 262-line NTSC frame (3 VSYNC, 37 VBLANK, 192 picture, 30 overscan), 76 processor cycles per scanline. Source: https://www.atariage.com/2600/programming/2600_101/docs/stella.html
- Andrew Davie, *Atari 2600 Programming for Newbies*, Session 23: deliberately decrementing the line counter changes the ordering when reading per-line graphics; tables must match the direction. Source: https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-23.html
- Stella Debugger documentation: visual inspection, stepping and trace, TIA and register displays, debugger script and frame/scanline advance. Source: https://stella-emu.github.io/docs/debugger.html
- User-supplied historical package `THE_SKRAUN_KOMPLETT_CHATTPAKET_TILL_MAIN_2026-11-16(1).zip`: 31 entries; ZIP consistency check passed; 30 manifest SHA-256 entries verified. Historical design decisions 01–19 and top-down artwork direction align with latest graphics brief. This archive is **historical research/handoff**, superseded for decisions by current main `DESIGN_DECISIONS_01-60` and the user's later visual corrections.

## Fix

Branch: `fix/p02-gray-halo-upright`
Code: `experiments/p02_gray_static_halo.asm`
Test: `tests/check_gray_static_halo.py`
Workflow: `.github/workflows/p02-gray-static.yml` on fix branch.

Only the 192-byte `Troll1`, `Troll2`, `Troll3` bitmap tables were reversed in row order. `Ring1/2/3` playfield tables and the fixed raster kernel were not functionally changed. Assembly comments now explain the memory/scanline contract.

The new regression checks **both stored table order** and **actual rendered Stella pixels at levels 1, 2, 3**, using the 12-row approved-source prototype bitmap as a reference:
- Top row `00100100` (head/ears)
- Bottom row `11000010` (legs/feet)
- Vertical replication 1/2/3 for levels 1/2/3; horizontal pixel expansion from TIA NUSIZ 1×/2×/4×.

## Evidence

- Actual GitHub Actions run: https://github.com/Odourman/the-skraun/actions/runs/43885132056
- DASM: PASS, 4,096-byte NTSC ROM; SHA-256 `7dda240f58656277e5508ad444368b2c33cad0ee9c9a5c259b27e0a7eda44bed`.
- Stella version 6.7.1, X11 software rendering: actual screenshots for 3 levels, all passed.
- Gray bounds: level 1 16×12, level 2 32×24, level 3 64×36 display pixels.
- Ring bounds: level 1 48×42, level 2 80×62, level 3 96×84 display pixels.
- All three `UPRIGHT PASS` pixel-by-pixel checks passed, and halo still encircles the gray troll.
- Evidence package: GitHub Actions artifact `the-skraun-gray-upright-stella-evidence`, with source/ROM listing, PNGs, checksums and log.

## Effect on other prototypes

The original `experiment/p02-playfield-b2` also uses a descending visible line counter and pre-generated 192-row sprite tables that need explicit orientation review. Its earlier successful visual tests checked sizes and enclosure, **not head/feet orientation**. Do not treat those old screenshots as proof of correct sprite orientation. A later B2 production integration must use the corrected bottom-first storage convention, or an explicitly different correct lookup kernel.

The standalone gray P01 prototype `experiment/gray-topdown-skraun` has a different indexed bitmap routine and independently authored bottom-first data; the source order alone should not be changed blindly. Its visuals and animation still need independent review.

## Gates not passed

- Complete independently checked sprite animation/8-way movement in real Stella.
- Measured NTSC cycle/scanline timing for the corrected combined ROM.
- Player's visual acceptance of the actual tiny overhead sprite at level 1.
- P01 independent verification issue #1.
- Dynamic P02-B3 halo implementation and battle scene.

## Recommended team separation

- **MAIN:** current conversation: decisions, scope, authority, repository/Drive state, acceptance coordination.
- **ROM DEVELOPMENT:** separately scoped source changes and self-tests.
- **VERIFICATION:** separate source checkout, independent rebuilding, Stella/Debugger comparisons and PASS/FAIL, without modifying the candidate implementation.

Start prompts: `handoff/ROM_DEVELOPMENT_START.md` and `handoff/VERIFICATION_START.md`.
