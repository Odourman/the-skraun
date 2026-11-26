; FULLGAME-1 F6 bank1: two distinct TIA audio channels with 12f envelopes
; Channel0 gets event $10..$90; channel1 event $A0..$F0.
; Request $BF: highest event priority in frame; voice state $EE/$EF:
; upper nibble = sound ID, lower nibble = remaining frames.
; Both voice bytes are located below hardware stack $F0-$FF.
; $EE was WorldShift only during map setup, after which it is reusable.
; $EF was AuxMode; actor init mailbox moves to $EB.
        processor 6502
AUDC0     = $15
AUDC1     = $16
AUDF0     = $17
AUDF1     = $18
AUDV0     = $19
AUDV1     = $1A
SoundReq  = $BF
SoundReq1 = $85  ; former SELECT cheat byte, independent audio queue
Voice0    = $EE
Voice1    = $EF
ScoreHi   = $AE
ScoreLo   = $AD
        SEG AudioCode
        ORG $F000
AudioCold:
        lda $FFF9
        jmp $F000
        ORG $F100
AudioEngine:
        ; Channel0 and channel1 can accept different simultaneous events
        ; in a single physical frame. Neither starves the other queue.
        lda SoundReq
        beq NoNewEvent0
        lda Voice0
        and #$F0
        cmp SoundReq
        bcc AcceptVoice0
        bne NoNewEvent0
AcceptVoice0:
        lda SoundReq
        lsr
        lsr
        lsr
        lsr
        tax
        lda AudioLengths,x
        ora SoundReq
        sta Voice0
NoNewEvent0:
        lda #0
        sta SoundReq
        lda SoundReq1
        beq NoNewEvent1
        lda Voice1
        and #$F0
        cmp SoundReq1
        bcc AcceptVoice1
        bne NoNewEvent1
AcceptVoice1:
        lda SoundReq1
        lsr
        lsr
        lsr
        lsr
        tax
        lda AudioLengths,x
        ora SoundReq1
        sta Voice1
NoNewEvent1:
        lda #0
        sta SoundReq1
NoNewEvent:
        lda Voice0
        and #$0F
        beq MuteVoice0
        tay
        dec Voice0
        lda Voice0
        and #$F0
        lsr
        lsr
        lsr
        lsr
        tax
        lda AudioTypes,x
        sta AUDC0
        cpx #6
        bne Voice0Sweep
        lda AudioMelody,y   ; three ascending notes at the end of a wave
        bne Voice0Pitch
Voice0Sweep:
        tya
        lsr
        lsr
        clc
        adc AudioPitches,x
        and #$1F
Voice0Pitch:
        sta AUDF0
        lda AudioEnvelope,y
        sta AUDV0
        jmp TickVoice1
MuteVoice0:
        lda #0
        sta Voice0
        sta AUDV0
TickVoice1:
        lda Voice1
        and #$0F
        beq MuteVoice1
        tay
        dec Voice1
        lda Voice1
        and #$F0
        lsr
        lsr
        lsr
        lsr
        tax
        lda AudioTypes,x
        sta AUDC1
        tya
        lsr
        lsr
        clc
        adc AudioPitches,x
        and #$1F
        sta AUDF1
        lda AudioEnvelope,y
        cpx #11           ; sword warning: two separated urgent pulses
        bne VolumeVoice1
        cpy #7
        bcs VolumeVoice1
        cpy #4
        bcc VolumeVoice1
        lda #0
VolumeVoice1:
        sta AUDV1
        jmp AudioReturn
MuteVoice1:
        lda #0
        sta Voice1
        sta AUDV1
AudioReturn:
        jmp AudioBankReturn
AudioTypes:
        dc.b 0,4,12,4,8,4,4,1,8,8,8,1,8,4,12,4
AudioPitches:
        dc.b 0,26,18,11,14,15,8,26,8,24,13,26,7,5,24,14
AudioLengths:
        dc.b 0,9,10,11,7,12,15,6,5,4,6,11,10,14,15,10
AudioEnvelope:
        dc.b 0,1,2,2,3,4,5,5,6,7,8,9,10,10,10,10
AudioMelody:
        dc.b 12,12,12,12,12,12,15,15,15,15,15,19,19,19,19,19

        ORG $F300
        MAC HudCombineRow
        lda {1} + {3} * 10,x
        ora {2} + {3} * 10,y
        sta {4}
        ENDM

HudPrepare:
        ; Split each packed BCD score byte once. Row tables already have
        ; the glyph bits in PF1/PF2 order, so rendering needs no bit shifts.
        lda ScoreHi
        and #$0F
        tay
        lda ScoreHi
        lsr
        lsr
        lsr
        lsr
        tax
        HudCombineRow HudPF1High,HudPF1Low,0,$90
        HudCombineRow HudPF1High,HudPF1Low,1,$91
        HudCombineRow HudPF1High,HudPF1Low,2,$92
        HudCombineRow HudPF1High,HudPF1Low,3,$93
        HudCombineRow HudPF1High,HudPF1Low,4,$94
        lda ScoreLo
        and #$0F
        tay
        lda ScoreLo
        lsr
        lsr
        lsr
        lsr
        tax
        HudCombineRow HudPF2High,HudPF2Low,0,$E9
        HudCombineRow HudPF2High,HudPF2Low,1,$EA
        HudCombineRow HudPF2High,HudPF2Low,2,$EB
        HudCombineRow HudPF2High,HudPF2Low,3,$9A
        HudCombineRow HudPF2High,HudPF2Low,4,$9B
        jmp PrepareHaloColor

        ORG $F400
PrepareHaloColor:
        lda #0
        sta $0B
        lda $9E
        beq PlayerSilver
        lda #$2E
        bne SelectPlayerShade
PlayerSilver:
        lda #$0E
SelectPlayerShade:
        ldx $B3
        beq WritePlayerColor
        tay
        lda $8D
        and #4
        beq FullPlayerShade
        tya
        and #$F8
        bne WritePlayerColor
FullPlayerShade:
        tya
WritePlayerColor:
        sta $06
        jmp HudExitToGraphics

        ORG $F500
; Five rows per table. Each row is indexed by BCD digit 0 through 9.
; Preserve the original score font and the TIA's opposite PF bit orders.
HudPF1High:
        dc.b $E0,$40,$E0,$E0,$A0,$E0,$E0,$E0,$E0,$E0
        dc.b $A0,$C0,$20,$20,$A0,$80,$80,$20,$A0,$A0
        dc.b $A0,$40,$E0,$E0,$E0,$E0,$E0,$20,$E0,$E0
        dc.b $A0,$40,$80,$20,$20,$20,$A0,$20,$A0,$20
        dc.b $E0,$E0,$E0,$E0,$20,$E0,$E0,$20,$E0,$E0
HudPF1Low:
        dc.b $0E,$04,$0E,$0E,$0A,$0E,$0E,$0E,$0E,$0E
        dc.b $0A,$0C,$02,$02,$0A,$08,$08,$02,$0A,$0A
        dc.b $0A,$04,$0E,$0E,$0E,$0E,$0E,$02,$0E,$0E
        dc.b $0A,$04,$08,$02,$02,$02,$0A,$02,$0A,$02
        dc.b $0E,$0E,$0E,$0E,$02,$0E,$0E,$02,$0E,$0E
HudPF2High:
        dc.b $07,$02,$07,$07,$05,$07,$07,$07,$07,$07
        dc.b $05,$03,$04,$04,$05,$01,$01,$04,$05,$05
        dc.b $05,$02,$07,$07,$07,$07,$07,$04,$07,$07
        dc.b $05,$02,$01,$04,$04,$04,$05,$04,$05,$04
        dc.b $07,$07,$07,$07,$04,$07,$07,$04,$07,$07
HudPF2Low:
        dc.b $70,$20,$70,$70,$50,$70,$70,$70,$70,$70
        dc.b $50,$30,$40,$40,$50,$10,$10,$40,$50,$50
        dc.b $50,$20,$70,$70,$70,$70,$70,$40,$70,$70
        dc.b $50,$20,$10,$40,$40,$40,$50,$40,$50,$40
        dc.b $70,$70,$70,$70,$40,$70,$70,$40,$70,$70

        ORG $F6BB
HudEntryFromGraphics:
        jmp HudPrepare
        ORG $F6C0
HudExitToGraphics:
        lda $FFF9

        ORG $F6E3
AudioEntryTrampoline:
        jmp AudioEngine
        ORG $F6EA
AudioBankReturn:
        lda $FFF8       ; bank2 next fetch $F6ED is an RTS
        ORG $FFFC
        dc.w AudioCold
        dc.w AudioCold
