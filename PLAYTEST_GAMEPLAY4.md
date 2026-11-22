# THE SKRAUN – GAMEPLAY-4 PLAYTEST (F8, NTSC, partial)
**2026-11-22 – ROM DEVELOPMENT III.** GAMEPLAY-4 is a bounded playable K1-T sword / R1 bow experiment; NOT a finished game and NOT a real independent three-enemy renderer.

## Best runnable ROM
- **Use** `experiments/gameplay4a_f8_ntsc.bin` only, genuine 8192-byte DASM-built Atari 2600 conventional F8 binary.
- SHA-256 `8bb19a9d58b6a4f608f1ab10adbb622b9e70d0f44b39e247c68feb3a974427bd` from `experiments/gameplay4a_SHA256SUMS.txt`.
- The exact built sources `experiments/gameplay4a_bank0.asm` and `gameplay4a_bank1.asm` are committed separately from unproven attempted M1 variant `experiments/gameplay4_bank0.asm` and `gameplay4_bank1.asm`.
- Do not run `gameplay4_bank0`+`gameplay4_bank1` as production: real Stella shows **360** raster lines / PAL* or inconsistent frame state with the M1 missile enabled. Arrow experiment is a negative timing test, NOT a working in-game projectile.

## Controls and genuine stage path
- Joystick all 8 directions. Move right ~25 NTSC frames then release to approach knight: after ~24-frame raised-sword warning, **actual native 8x16 K1-T strike pose** appears for 7 logical active frames, then recovery ~60 frames. His sword damages the player only in the active direction/range in current diagnostic rules (not body contact). No new full obstacle line-of-sight/collision hard proof.
- For orb L1→L2: joystick RIGHT ~16 frames, DOWN ~24 from reset position; original real BL orb is consumed once per stage visit.
- For sequential training targets / stage1 score: from this point hold FIRE, UP ~40 frames, RIGHT ~14 frames, continue movement/attack. Stage1 sequential 100+100+250-point training waves and Stage1→2 remain inherited from GAMEPLAY-2. During the Ranger's last slot, bow source masks are selected by 24-frame draw and 8-frame release and recover ~60 frames; **the supplied GAMEPLAY-4A ROM deliberately has NO arrow** because the physical M1 trial exceeded NTSC timing. No invisible projectile or damage is allowed.
- After 1→2, RIGHT ~8 and DOWN ~24 reaches stage2 orb for L2→L3. L3 joystick and held-FIRE movement were sampled in authentic Stella with 262 raster lines, native 64×36 P0 footprint 1200 source-dependent gray TIA pixels. Two world maps and full 8-arena art are NOT implemented.
- Physical FIRE also resets after GAME OVER, with inherited lives and scores; original Y-only visible halo remains PARTIAL without X/Y-follow redesign.

## Real test and reproduction
- [Genuine DASM/Stella full 8-scene checkpoint](https://github.com/Odourman/the-skraun/actions/runs/45032475262) – **all eight tested scenes _scanEnd=262** after hot P0 scanline optimization; P0 L1=98, L2=392, L3=1200 true gray pixels; K1-T native source masks in running cartridge L1 neutral116, raised warning134, active strike130, recovery neutral116 in actual 320×228 TIA crops.
- Ranger source mask timing needs precisely selected authentic joystick-frame screenshot; independent full on-hardware animation certification is NOT claimed. Graphics II six source masks unchanged, with earlier separately demonstrated real ROM masked 8×16 poses.
- [Original actual M1 arrow full attempt](https://github.com/Odourman/the-skraun/actions/runs/45032475336): 8192B F8 physically executed but 360 scanlines in key scenes, not accepted. The logical fixed-vector/cooldown/halo/wall/body code is only SOURCE_ONLY in this rejected variant; the desired visible moving, damaging arrow is **NOT IMPLEMENTED** in the best runnable game.

## Invariants and warnings
- Retains unchanged approved original 8×12 source Skraun U1-LEG1 A/B, P0, joystick, FIRE, original BL orb, 3 levels, lives, scores, stage transitions and conventional F8.
- One sequential P1 actor temporarily (two knight score slots then Ranger) **does NOT meet mandatory final two simultaneous knights + independent Ranger**; no new renderer attempted within this sprint.
- Exact 76-cycle worst-case with all page-cross penalties, TIA write-before-beam deadlines for all X, actual RIOT 128B stack highwater, beam-safe sprite near x31, all blocked obstacle arrow/sword cases, and all possible L3 joystick paths are **NOT VERIFIED**. 262 full frames are genuine bounded evidence, not a hardware-wide certification.
- No new N8/N9, mapper change, X/Y halo, graphics production, eight final arenas, or main merge.

Source report: `docs/gameplay4/ROMDEV_GAMEPLAY4_MAIN_IV_DELIVERY_2026-11-22.md`. One DRAFT PR #46; implementation STOP after delivery.
