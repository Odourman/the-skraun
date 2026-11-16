# THE SKRAUN — P02-B1 Playfield Halo experiment result

Date: 2026-11-16
Status: **PASS, bounded visual self-test only**; NOT the final halo or independent P02 acceptance.
Repo branch: `experiment/p02-playfield-b1`.
Source: `experiments/p02_playfield_b1.asm`.
Reproducible DASM build: `dasm experiments/p02_playfield_b1.asm -f3 -obuild/p02-playfield-b1.bin -lbuild/p02-playfield-b1.lst -sbuild/p02-playfield-b1.sym`.

## Verified artifact

- NTSC 4 KiB ROM (4,096 bytes).
- SHA-256: `68e68b3484c952a11cfcaf3e4b706feb400be7efc07d418b0d57fe75b824b68a`.
- Actual Stella screenshot (320×228): golden playfield pixels bound x112..207, y69..152.
- Visible golden ring width: **96 screenshot px = 48 TIA color clocks**; height: **84 scanlines**.
- Horizontal pixel reflection correspondence: 100%; screen aspect ratio width/height 1.143.
- Real Stella image analysis: PASS, hollow, centered and not overly flattened.
- GitHub Actions run: https://github.com/Odourman/the-skraun/actions/runs/43870826690.
- Google Drive evidence: https://drive.google.com/drive/folders/10z4TcTyd04dms9PNpFrDGZtHFkNWvWKc.

## TIA design and resource use

- Use `CTRLPF=1` to mirror the 20 left-side 4-color-clock playfield cells about the screen center.
- Three 84-row ROM tables (PF0, PF1, PF2) together use 252 ROM bytes. In the successful centered ring, PF0 and PF1 are all zero and only PF2 contains nonzero masks.
- No RAM framebuffer. P0, P1, missiles and ball are not used in this B1 ROM, so they remain free **in this isolated test**.
- One PF2 register is updated per visible scanline. The full dynamic-ring and scenery budget is **not** established by this static demonstration.

## Rejected earlier artwork

The initial B1 geometry produced a screenshot bounding box of 176×52 pixels (aspect 3.38), much too flat. That test passed a width check but did not pass a satisfactory appearance assessment. The revised geometry passes a stronger circularity check, and the earlier screenshot remains historical evidence.

## Explicit limits and next gate

B1 contains **no troll, no FIRE, no movement, no collisions, no obstacles and no enemies**. A good static ring does not establish that it can move freely without using additional playfield registers or CPU time. It also does not establish coexistence with obstacles, which compete for the same PF resources. Full Stella Debugger cycle and scanline evidence, original hardware and independent verification remain open.

The next bounded experiment is **P02-B2**, overlaying the P0 troll with three centered ring sizes. It does not attempt unrestricted x/y movement yet.

MAIN's 60 gameplay design decisions remain unchanged. P01 independent verification issue remains open: https://github.com/Odourman/the-skraun/issues/1.
