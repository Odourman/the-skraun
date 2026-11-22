#!/usr/bin/env python3
"""GAMEPLAY-4 checkpoint A: real K1-T neutral/warning/strike + R1 neutral/draw/release.
No arrow in this checkpoint, not a fake/invisible projectile. Original bank sources
remain unchanged, both generated assembler sources are preserved in artifacts.
"""
from pathlib import Path
r=Path("build/gameplay4/checkpoint_A")
r.mkdir(parents=True,exist_ok=True)
a=Path("experiments/gameplay4_bank0.asm").read_text()
b=Path("experiments/gameplay4_bank1.asm").read_text()
old="""        sta SwordStrike
        jsr LaunchArrow
        rts"""
new="""        sta SwordStrike
        ; CHECKPOINT A: no projectile, so no invisible damage ever
        rts"""
assert old in a
a=a.replace(old,new)
missile="""        lda (ArrowRowPtr),y
        sta ENAM1         ; real M1 vertical-gated arrow, two native scanlines
"""
assert missile in b
b=b.replace(missile,"        ; CHECKPOINT A: no M1 visible writes; no invisible projectile logic\n")
# No arrow launch means ArrowDX stays zero; its VBLANK position block is unreachable.
assert "jsr LaunchArrow" not in a
(r/"bank0.asm").write_text(a)
(r/"bank1.asm").write_text(b)
print("CHECKPOINT_A_SOURCE_GENERATED; exact six live pose tables; no hidden arrow.")
