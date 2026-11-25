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
        tax
        lda Voice0
        and #$F0
        cmp SoundReq
        bcs NoNewEvent0
        txa
        ora #$0C
        sta Voice0
NoNewEvent0:
        lda #0
        sta SoundReq
        lda SoundReq1
        beq NoNewEvent1
        tax
        lda Voice1
        and #$F0
        cmp SoundReq1
        bcs NoNewEvent1
        txa
        ora #$0C
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
        tya
        lsr
        lsr
        clc
        adc AudioPitches,x
        and #$1F
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
        dc.b 0,4,4,6,8,12,6,1,12,8,12,1,8,12,6,4
AudioPitches:
        dc.b 0,24,20,15,18,16,24,29,12,27,10,10,8,5,16,12
AudioEnvelope:
        dc.b 0,1,2,3,4,5,6,7,8,8,9,10,10,10,10,10

        ORG $F300
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
        ; Independent five-row threat status. The $95 scratch holds a
        ; completed score digit until this point; free thereafter.
        lda #0
        ldx $D5           ; K1 alive
        beq HudNoKnight1
        ora #$80
HudNoKnight1:
        ldx $DC           ; K2 alive
        beq HudNoKnight2
        ora #$40
HudNoKnight2:
        ldx $E3           ; Ranger alive
        beq HudNoRanger
        ora #$20
HudNoRanger:
        ; A fourth, independent HUD indicator warns of ANY imminent hit.
        ; It is not tied to the currently selected P1 display slot.
        ldx $D2          ; K1 sword telegraph
        bne HudDangerActive
        ldx $D9          ; K2 sword telegraph
        bne HudDangerActive
        ldx $D3          ; K1 active strike
        bne HudDangerActive
        ldx $DA          ; K2 active strike
        bne HudDangerActive
        ldx $E0          ; Ranger bow draw
        bne HudDangerActive
        ldx $A3          ; Ranger projectile still in flight
        beq HudDangerDone
HudDangerActive:
        ora #$10
HudDangerDone:
        sta $95
        jmp HaloVisualSelect
HudFont:
        dc.b $77,$55,$55,$55,$77 ; 0
        dc.b $22,$63,$22,$22,$77 ; 1
        dc.b $77,$14,$77,$41,$77 ; 2
        dc.b $77,$14,$77,$14,$77 ; 3
        dc.b $55,$55,$77,$14,$14 ; 4
        dc.b $77,$41,$77,$14,$77 ; 5
        dc.b $77,$41,$77,$55,$77 ; 6
        dc.b $77,$14,$14,$14,$14 ; 7
        dc.b $77,$55,$77,$55,$77 ; 8
        dc.b $77,$55,$77,$14,$77 ; 9
HudBase:
        dc.b $00,$05,$0A,$0F,$14,$19,$1E,$23,$28,$2D

        ORG $F400
; P0 stays exact U1-LEG1 in normal play. Active halo expands visual
; source to a precomputed frozen A-pose with 3+2 gold tips on each side;
; player can continue moving, but walking pose freezes for 30f.
HaloVisualSelect:
        lda $99           ; real HalfH remains untouched for collision
        sta $87           ; safe after movement (was DiagonalSkip)
        lda #0
        sta $0B           ; REFP0, normal sprite already physically flipped in ROM
        lda $9E           ; HaloFrames
        beq HaloRimOff
        lda $A0           ; HaloRadius (18/28/38)
        sta $87
        ldx $82           ; Level
        lda HaloRuneLo,x
        sta $8B           ; GfxPtr low
        lda HaloRuneHi,x
        sta $8C           ; GfxPtr high
        lda HaloRuneHeight,x
        sta $88           ; SpriteHeight (37/57/77)
        lda $8E           ; Facing (0=right,1=left)
        beq HaloRimPrepare
        lda #8
        sta $0B           ; hardware pixel-exact horizontal mirror
HaloRimPrepare:
        ; Three contour bands, phased by the 0..2 gait counter. Keep the
        ; logical radius untouched. Y offsets are in two-line table units.
        lda $86
        and #3
        asl
        asl
        ora $82
        tax
        lda HaloRimReach,x
        sta $8F           ; MotionDid is dead after UpdateGait, until next Frame
        lda $81
        clc
        adc #1
        lsr
        clc
        adc HaloRimYSeed,x
        sta $A6
        lda #$FF
        sta $A7
        jmp HudExitToGraphics
HaloRimOff:
        lda #1
        sta $A6
        lda #$FF
        sta $A7
        jmp HudExitToGraphics
HaloRimReach:
        dc.b 0,18,28,38, 0,14,21,29, 0,14,21,29
HaloRimYSeed:
        dc.b $28,$28,$28,$28, $28,$2D,$2F,$32, $28,$23,$21,$1E
HaloRuneLo:
        dc.b 0,$92,$B7,$B2
HaloRuneHi:
        dc.b 0,$FD,$FD,$F9
HaloRuneHeight:
        dc.b 0,37,57,77
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
