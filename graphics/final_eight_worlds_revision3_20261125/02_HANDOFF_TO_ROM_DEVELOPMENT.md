# THE SKRAUN / MAIN V → ROM DEVELOPMENT — GRAPHICS REVISION 3

**Advisory handoff, not an implementation authorization.** R3 is SOURCE_ONLY and pending aesthetic sign-off by MAIN V and user.

Baseline: draft PR [#60](https://github.com/Odourman/the-skraun/pull/60), immutable source commit `2af9855fbe8d3edbe6d01609d3e539547b744aef` (current draft HEAD at source review); bank3 blob `62e88de692df80024db8342e0990640a5310f620`.

After separate explicit MAIN approval, replace **only** the original 768-byte `PlayPF1` region between `ORG $FA00` and `ORG $FD00` in `experiments/fullgame1_arrow_halo_20261125/bank3.asm` with `03_PLAYFIELD_DATA.asm`. R3 PF1 SHA256 `c879daa4b5bcc1bb19aa71ee632c48996b0885963bd102dd8e76bd50761354d4`.

R3 retains 8×96 bytes, `WorldPFIndex` (two rasterlines per byte, reversed table read), `WorldPFPtr`, `Visible`, `VisibleArrow`, `CTRLPF`, original world palette and halo behavior. No new visible TIA writes, RAM or kernel. Exactly 32 bytes differ from frozen R2; all other 13 motifs are unchanged.

WorldRects: **Do not apply a collision change automatically**. The R2 conservative envelopes still cover the R3 outer bounds exactly, all 32 proposed AABBs preserved. AABB encloses holes of portals and spirals; physical game colliders/diagonal L3 movement must be tested independently of this source-only model.

Complete reproducible 123-file package includes `04_WORLD_GRAPHICS.json`, `05_COLLISION_RECOMMENDATIONS.json`, all screenshots, 16 motifs, a byte-exact Python generator, reference images and SHA manifest. PR60 original ROM and SHA must not be mislabeled as R3 ROM.

If separately authorized for implementation: native DASM build; Stella physical PF1 pixels for each world, mirrored/repeated stage 2/4 center clearance, NTSC 262 rasterlines and beam deadlines; collision, L3 free navigation, orb growth, enemy simultaneity and halo effect. These tests are **NOT** part of GRAPHICS II's work.

**No ROM implementation, no new verification and no merge.**