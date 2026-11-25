"""FULLGAME-1 16KiB F6: bounded adaptive P1 actor presentation.

One physical P1 display slot per frame remains. Favors visible sword warning,
strike and bow draw; does NOT prove three same-Y independent sprites.
"""
OLD = '''ChooseP1:
        lda NextSlot
        clc
        adc #1
        cmp #3
        bcc SelectedIndex
        lda #0
SelectedIndex:
        sta NextSlot
        sta DrawSlot
        cmp #1
'''
NEW = '''ChooseP1:
        jsr AdaptiveSelect
        sta DrawSlot
        cmp #1
'''
CODE = '''
        ORG $FA40
; Adaptive display-only scheduler. Runs once per game frame in blanking.
; Active strike > 24f sword telegraph > Ranger bow > live round robin.
; One threat gets 3/4 frames, other actors share remaining 1/4.
; Dual warnings: K1/K2 alternated; Ranger every fourth frame if alive.
; Existing KnightCanHit guard checks previous DrawSlot, preventing
; off-slot sword damage. Actual physical occlusion remains unproven.
AdaptiveSelect:
        lda K1Alive
        beq ASCheckK2Strike
        lda K1Strike
        beq ASCheckK2Strike
        lda K2Alive
        beq ASPickK1
        lda K2Strike
        bne ASBoth
        jmp ASPickK1
ASCheckK2Strike:
        lda K2Alive
        beq ASCheckK1Warn
        lda K2Strike
        bne ASPickK2
ASCheckK1Warn:
        lda K1Alive
        beq ASCheckK2Warn
        lda K1Warn
        beq ASCheckK2Warn
        lda K2Alive
        beq ASPickK1
        lda K2Warn
        bne ASBoth
        jmp ASPickK1
ASCheckK2Warn:
        lda K2Alive
        beq ASCheckRanger
        lda K2Warn
        bne ASPickK2
ASCheckRanger:
        lda RAlive
        beq ASRoundRobin
        lda RDraw
        ora RRelease
        beq ASRoundRobin
ASPickRanger:
        ldx #2
        jmp ASMajority
ASPickK1:
        ldx #0
        jmp ASMajority
ASPickK2:
        ldx #1
        jmp ASMajority
ASBoth:
        lda FrameCount
        and #3
        cmp #3
        bne ASBothKnight
        lda RAlive
        bne ASPickRanger
ASBothKnight:
        lda FrameCount
        and #1
        rts
ASMajority:
        lda FrameCount
        and #3
        bne ASReturnHigh
        jsr ASRoundRobin
        sta DrawSlot
        txa
        cmp DrawSlot
        bne ASReturnAlternative
        jsr ASRoundRobin
        rts
ASReturnAlternative:
        lda DrawSlot
        rts
ASReturnHigh:
        txa
        rts
ASRoundRobin:
        ldy #3
ASRRLoop:
        lda NextSlot
        clc
        adc #1
        cmp #3
        bcc ASRRValue
        lda #0
ASRRValue:
        sta NextSlot
        cmp #1
        beq ASRRK2
        cmp #2
        beq ASRRRanger
        lda K1Alive
        bne ASRRK1Good
        beq ASRRNext
ASRRK1Good:
        lda #0
        rts
ASRRK2:
        lda K2Alive
        beq ASRRNext
        lda #1
        rts
ASRRRanger:
        lda RAlive
        beq ASRRNext
        lda #2
        rts
ASRRNext:
        dey
        bne ASRRLoop
        lda #0
        rts
'''

def adaptive_bank0(source: str) -> str:
    if source.count(OLD) != 1:
        raise ValueError("Original ChooseP1 anchor drift")
    source = source.replace(OLD, NEW, 1)
    assert source.count("        ORG $FFFC\n") == 1
    return source.replace("        ORG $FFFC\n", CODE + "        ORG $FFFC\n", 1)
