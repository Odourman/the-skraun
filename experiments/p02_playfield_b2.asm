; THE SKRAUN — P02-B2 static centered playfield ring + P0 troll
; 3 sizes cycled by console SELECT, no halo FIRE or movement yet.
; Ring uses only PF2 because its x extents stay near screen center.
; Two TIA player objects are NOT consumed by ring, only P0 for troll.
; Separate 4 KiB NTSC research ROM. Never interpret this as final renderer.
        processor 6502
VSYNC       = $00
VBLANK      = $01
WSYNC       = $02
NUSIZ0      = $04
COLUP0      = $06
COLUPF      = $08
COLUBK      = $09
CTRLPF      = $0A
PF0         = $0D
PF1         = $0E
PF2         = $0F
RESP0       = $10
GRP0        = $1B
HMP0        = $20
HMOVE       = $2A
SWCHB       = $0282

Level       = $80
PrevSelect  = $81
SwitchState = $82
PlayerX     = $83
RingPtr     = $84           ; 2 zero-page bytes
TrollPtr    = $86           ; 2 zero-page bytes

        SEG Code
        ORG $F000
Reset:
        sei
        cld
        ldx #$FF
        txs
        lda #0
        ldx #$7F
ClearRAM:
        sta $80,x
        dex
        bpl ClearRAM
        ldx #$2C
ClearTIA:
        sta $00,x
        dex
        bpl ClearTIA
        lda #1
        sta Level
        sta CTRLPF         ; reflect playfield about x=80
        lda #$C8
        sta COLUP0         ; green troll
        lda #$2E
        sta COLUPF         ; golden ring
        lda #0
        sta COLUBK
        sta PF0
        sta PF1

MainFrame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC

; VBLANK: exactly 37 scanlines, including one positioning WSYNC.
        lda SWCHB
        sta SwitchState
        sta WSYNC             ; 1
        jsr UpdateLevel
        sta WSYNC             ; 2
        jsr SelectPointers
        sta WSYNC             ; 3
        lda PlayerX
        jsr PositionP0        ; 4, routine owns WSYNC
        sta WSYNC             ; 5
        sta HMOVE
        ldx #32
VBlankPad:
        sta WSYNC             ; 6..37
        dex
        bne VBlankPad

        lda #0
        sta VBLANK
        ldx #192
VisibleLoop:
        sta WSYNC             ; one scanline
        dex                   ; X: 191..0, index bottom-to-top ROM tables
        txa
        tay
        lda (RingPtr),y
        sta PF2
        lda (TrollPtr),y
        sta GRP0
        txa
        bne VisibleLoop

        lda #2
        sta VBLANK
        lda #0
        sta PF2
        sta GRP0
        ldx #30
OverScan:
        sta WSYNC
        dex
        bne OverScan
        jmp MainFrame         ; 3 + 37 + 192 + 30 = 262

UpdateLevel:
        lda SwitchState
        and #2
        bne SelectReleased
        lda PrevSelect
        bne SelectDone
        lda #1
        sta PrevSelect
        inc Level
        lda Level
        cmp #4
        bne SelectDone
        lda #1
        sta Level
SelectDone:
        rts
SelectReleased:
        lda #0
        sta PrevSelect
        rts

SelectPointers:
        lda Level
        cmp #1
        bne SetLevelTwo
        lda #64
        sta PlayerX
        lda #0
        sta NUSIZ0
        lda #<Ring1
        sta RingPtr
        lda #>Ring1
        sta RingPtr+1
        lda #<Troll1
        sta TrollPtr
        lda #>Troll1
        sta TrollPtr+1
        rts
SetLevelTwo:
        cmp #2
        bne SetLevelThree
        lda #59
        sta PlayerX
        lda #5
        sta NUSIZ0
        lda #<Ring2
        sta RingPtr
        lda #>Ring2
        sta RingPtr+1
        lda #<Troll2
        sta TrollPtr
        lda #>Troll2
        sta TrollPtr+1
        rts
SetLevelThree:
        lda #51
        sta PlayerX
        lda #7
        sta NUSIZ0
        lda #<Ring3
        sta RingPtr
        lda #>Ring3
        sta RingPtr+1
        lda #<Troll3
        sta TrollPtr
        lda #>Troll3
        sta TrollPtr+1
        rts

PositionP0:
        sta WSYNC
        sec
PositionLoop:
        sbc #15
        bcs PositionLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP0
        sta RESP0
        rts

        ORG $F600
; 6×192 ROM bytes, zero additional raster framebuffer RAM.
; Y index is reversed from visible scanline: 191=top, 0=bottom.
Ring1:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$80,$80,$C0,$C0,$C0,$40,$60,$60,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$60,$60,$40,$C0,$C0,$C0,$80,$80,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
Ring2:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$80,$C0,$C0,$C0,$E0,$E0,$60
        dc.b $60,$20,$30,$30,$30,$10,$10,$10,$10,$10,$18,$18
        dc.b $18,$18,$18,$08,$08,$08,$08,$08,$08,$08,$08,$08
        dc.b $08,$08,$08,$08,$08,$08,$08,$08,$08,$18,$18,$18
        dc.b $18,$18,$10,$10,$10,$10,$10,$30,$30,$30,$20,$60
        dc.b $60,$E0,$E0,$C0,$C0,$C0,$80,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
Ring3:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$80,$C0,$C0,$E0,$E0,$E0
        dc.b $E0,$70,$70,$30,$30,$30,$18,$18,$18,$18,$18,$08
        dc.b $08,$08,$0C,$0C,$0C,$0C,$0C,$0C,$0C,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04,$04
        dc.b $04,$04,$04,$0C,$0C,$0C,$0C,$0C,$0C,$0C,$08,$08
        dc.b $08,$18,$18,$18,$18,$18,$30,$30,$30,$70,$70,$E0
        dc.b $E0,$E0,$E0,$C0,$C0,$80,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
Troll1:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$24,$24,$66,$66,$FF,$FF
        dc.b $DB,$DB,$FF,$7E,$3C,$18,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
Troll2:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $24,$24,$24,$24,$66,$66,$66,$66,$FF,$FF,$FF,$FF
        dc.b $DB,$DB,$DB,$DB,$FF,$FF,$7E,$7E,$3C,$3C,$18,$18
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
Troll3:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$24,$24,$24,$24,$24,$24
        dc.b $66,$66,$66,$66,$66,$66,$FF,$FF,$FF,$FF,$FF,$FF
        dc.b $DB,$DB,$DB,$DB,$DB,$DB,$FF,$FF,$FF,$7E,$7E,$7E
        dc.b $3C,$3C,$3C,$18,$18,$18,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00

        ORG $FFFC
        dc.w Reset
        dc.w Reset
