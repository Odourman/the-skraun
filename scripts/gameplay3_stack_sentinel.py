#!/usr/bin/env python3
"""Create a separate (NOT main playable) GAMEPLAY-3 RIOT stack sentinel ROM.
F0..FF are initialized with unique canaries AFTER ClrRAM and BEFORE any JSR.
No injection with Stella debugger; instrumented startup code is auditable.
"""
from pathlib import Path
s=Path("experiments/gameplay3_bank1.asm").read_text()
a="        bpl ClrRAM\n        ldx #$2C"
b="""        bpl ClrRAM
        ldx #$0F
StackSentinelInit:
        txa
        eor #$A5
        sta $F0,x
        dex
        bpl StackSentinelInit
        lda #0
        ldx #$2C"""
assert a in s
s=s.replace(a,b,1)
Path("build/gameplay3/stack_sentinel_bank1.asm").write_text(s)
print("INSTRUMENTED_TEST_ONLY: patterned RIOT $F0..$FF canaries, original game main bank unchanged")
