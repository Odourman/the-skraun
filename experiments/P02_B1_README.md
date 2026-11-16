# P02-B1: mirrored playfield halo diagnostic

**Not a full gameplay or halo implementation.** This research ROM contains one **static** golden ring centered horizontally (x=80 logical TIA pixels), drawn by mirrored playfield PF0/PF1/PF2. It does not contain P0 troll, movement, collisions, or obstacles.

The ROM builds as a plain 4 KiB NTSC cartridge:
`dasm experiments/p02_playfield_b1.asm -f3 -obuild/p02-playfield-b1.bin -lbuild/p02-playfield-b1.lst -sbuild/p02-playfield-b1.sym`.

The 84 scanline image uses 84×3=252 bytes of ROM table data, zero screen framebuffer bytes of RAM, and no player/missile/ball registers. `CTRLPF=1` reflects the 20 left playfield cells to the right. The nominal ring envelope is ~52×84 color clocks/scanlines, more than the level-3 32-clock-wide troll, but there is **no troll in this experiment**, so fitting both is not yet proven.

**Important limitation:** A static centered ring is substantially easier than a halo following a moving troll, particularly horizontally, and the same playfield hardware will also be wanted for scenery. Passing B1 only authorizes further testing, not selecting playfield for the final game.

B1 should be evaluated from a real Stella PNG: visible gold pixels, centered mirror symmetry, width >64 color clocks and frame timing. See GitHub Actions for actual results; no independent verification is implied.
