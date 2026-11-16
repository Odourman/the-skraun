# P02-B2: static playfield halo around troll (three scales)

**Experimental, no gameplay implementation.** Builds a plain 4 KiB NTSC ROM using mirrored playfield PF2 to make a static ring around a **P0 troll**. SELECT cycles three levels: level 1 (8×12 sprite), level 2 (16×24), level 3 (32×36); each also changes the golden ring diameter. Neither troll nor ring moves horizontally or vertically in B2.

Source `experiments/p02_playfield_b2.asm`; build command:
`dasm experiments/p02_playfield_b2.asm -f3 -obuild/p02-playfield-b2.bin -lbuild/p02-playfield-b2.lst -sbuild/p02-playfield-b2.sym`

The ring is hard-coded at screen center x80 and uses PF2 only, reflected through CTRLPF. Ring/troll scanline tables contain **1,152 bytes in ROM** (six 192-byte arrays), controlled through four zero-page pointer bytes. There is **no full-screen frame buffer** in the Atari's 128-byte RAM.

One TIA player is consumed by the troll, P1 and both missile objects and the ball remain unused. The centered ring does **not** prove a moving ring is cheap: moving it horizontally will demand non-centered PF register patterns and possibly mid-scanline rewrites. Obstacle visuals and multi-actor multiplexing are untested.

This is B2 only. On an actual Stella capture verify all three sprite sizes, increasing halo widths and that level 3 visibly clears the troll. Preserve P01 independent gate and all 60 game design decisions.
