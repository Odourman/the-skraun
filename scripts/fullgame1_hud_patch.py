"""FULLGAME-1 4-decimal-digit score/lives HUD in original-compatible 16KiB F6.
Bank1 precomputes 5 rows of playfield digits from packed BCD after movement,
bank3 renders them in five real top arena raster rows plus separator.
Not a claim of all-frame beam/cycle verification. Fullgame1 source patch.
"""
def once(s,old,new,tag):
    if s.count(old)!=1:raise ValueError(f"HUD {tag}: got {s.count(old)} anchors")
    return s.replace(old,new,1)

def bank0(s):
    old="""        stx ScratchIX
        txa
        clc
        adc ScoreLo
        sta ScoreLo
        lda ScoreHi
        adc #0
        sta ScoreHi
        lda ScratchIX"""
    new="""        stx ScratchIX
        ; Packed BCD scoreboard 0000..9999; knight +100, Ranger +250.
        cpx #100
        bne ScoreAdd250
        sed
        clc
        lda ScoreHi
        adc #$01
        sta ScoreHi
        cld
        jmp ScoreIncreaseDone
ScoreAdd250:
        sed
        clc
        lda ScoreLo
        adc #$50
        sta ScoreLo
        lda ScoreHi
        adc #$02
        sta ScoreHi
        cld
ScoreIncreaseDone:
        lda ScratchIX"""
    return once(s,old,new,"BCD award")

GLYPHS=(
("111","101","101","101","111"),
("010","110","010","010","111"),
("111","001","111","100","111"),
("111","001","111","001","111"),
("101","101","111","001","001"),
("111","100","111","001","111"),
("111","100","111","101","111"),
("111","001","001","001","001"),
("111","101","111","101","111"),
("111","101","111","001","111"),
)

def bank1(s):
    s=once(s,"Voice1    = $EF\n        SEG AudioCode",
           "Voice1    = $EF\nScoreHi   = $AE\nScoreLo   = $AD\n        SEG AudioCode","bank1 aliases")
    glyph="HudFont:\n"
    for d,rows in enumerate(GLYPHS):
        out=[]
        for row in rows:
            v=int(row,2)
            reverse=int(row[::-1],2)
            out.append((v<<4)|reverse)
        glyph+="        dc.b "+",".join("$"+format(v,"02X") for v in out)+" ; "+str(d)+"\n"
    glyph+="HudBase:\n        dc.b "+",".join("$"+format(5*d,"02X") for d in range(10))+"\n"
    hud="""        ORG $F300
HudPrepare:
        ldy #0
HudPrepareRow:
        lda ScoreHi
        lsr
        lsr
        lsr
        lsr
        tax
        tya
        clc
        adc HudBase,x
        tax
        lda HudFont,x
        and #$70
        asl
        sta $0090,y
        lda ScoreHi
        and #$0F
        tax
        tya
        clc
        adc HudBase,x
        tax
        lda HudFont,x
        and #$70
        lsr
        lsr
        lsr
        ora $0090,y
        sta $0090,y
        lda ScoreLo
        and #$0F
        tax
        tya
        clc
        adc HudBase,x
        tax
        lda HudFont,x
        and #$07
        asl
        asl
        asl
        asl
        sta $95
        lda ScoreLo
        lsr
        lsr
        lsr
        lsr
        tax
        tya
        clc
        adc HudBase,x
        tax
        lda HudFont,x
        and #$07
        ora $95
        cpy #3
        bcs HudStorePF2Tail
        sta $00E9,y
        jmp HudNextRow
HudStorePF2Tail:
        sta $0097,y
HudNextRow:
        iny
        cpy #5
        bcc HudPrepareRow
        jmp HudExitToGraphics
"""+glyph+"""
        ORG $F6BB
HudEntryFromGraphics:
        jmp HudPrepare
        ORG $F6C0
HudExitToGraphics:
        lda $FFF9
"""
    s=once(s,"        ORG $F6E3\nAudioEntryTrampoline:",hud+"\n        ORG $F6E3\nAudioEntryTrampoline:","bank1 HUD code")
    return s

def bank3(s):
    s=once(s,"        jsr SelectEnemyArt ; offscreen identity/pose, never after GRP1 beam deadline\n",
           "        jsr SelectEnemyArt ; offscreen identity/pose, never after GRP1 beam deadline\n        jsr HudBankEnter    ; prepare current score and lives after motion\n","HUD vblank")
    s=once(s,"VisibleGate:\n        ldx #192\n",
           "VisibleGate:\n        jsr HudDraw        ; five scoreboard scanlines + blank separator\n        ldx #186\n",
           "192 scanline preservation")
    code="""        ORG $F6B8
HudBankEnter:
        lda $FFF7
        ORG $F6C3
HudBankReturn:
        rts
        ORG $F6C4
HudDraw:
        ldy Lives
        lda HudLifeMasks,y
        sta PF0
        ldx #0
HudDrawRow:
        sta WSYNC
        lda $90,x
        sta PF1
        cpx #3
        bcs HudPF2Tail
        lda $E9,x
        jmp HudPF2Write
HudPF2Tail:
        lda $97,x
HudPF2Write:
        sta PF2
        inx
        cpx #5
        bne HudDrawRow
        sta WSYNC
        lda #0
        sta PF0
        sta PF1
        sta PF2
        rts
HudLifeMasks:
        dc.b 0,$10,$30,$70,$F0,$F0,$F0,$F0,$F0,$F0

"""
    s=once(s,
           "        ORG $F700    ; all four x36 L3 bitmaps fit one ROM page",
           code+"        ORG $F700    ; all four x36 L3 bitmaps fit one ROM page",
           "HUD bank 3 trampoline")
    return s
