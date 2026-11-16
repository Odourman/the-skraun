; THE SKRAUN — P02-B1 playfield halo research ROM
; Mirrored 40-cell TIA playfield: 52-line static ring centered at x80.
; This diagnostic intentionally contains NO troll or dynamic movement.
; TIA P0/P1, missiles and ball remain unused in B1.
; NTSC 262 scanlines, plain 4 KiB cartridge, DASM.
        processor 6502

VSYNC   = $00
VBLANK  = $01
WSYNC   = $02
COLUPF  = $08
COLUBK  = $09
CTRLPF  = $0A
PF0     = $0D
PF1     = $0E
PF2     = $0F

        SEG Code
        ORG $F000

Reset:
        sei
        cld
        ldx #$FF
        txs
        lda #0
        ldx #$2C
ClearTIA:
        sta $00,x
        dex
        bpl ClearTIA
        lda #$01
        sta CTRLPF           ; reflect left playfield onto right
        lda #$2E
        sta COLUPF           ; golden ring
        lda #$00
        sta COLUBK

MainFrame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC

        ldx #37
VblankLines:
        sta WSYNC
        dex
        bne VblankLines

        lda #0
        sta VBLANK
        ldx #192
VisibleLoop:
        sta WSYNC
        txa
        sec
        sbc #77             ; active when X in [77,128]
        bcc ClearPF
        cmp #52
        bcs ClearPF
        tay
        lda RingPF0,y
        sta PF0
        lda RingPF1,y
        sta PF1
        lda RingPF2,y
        sta PF2
        jmp NextRow
ClearPF:
        lda #0
        sta PF0
        sta PF1
        sta PF2
NextRow:
        dex
        bne VisibleLoop

        lda #2
        sta VBLANK
        lda #0
        sta PF0
        sta PF1
        sta PF2
        ldx #30
OverscanLines:
        sta WSYNC
        dex
        bne OverscanLines
        jmp MainFrame

        ORG $F300
; 52 rows × 3 bytes in ROM; no 52×40 framebuffer in RAM.
; 20 left half cells, mapping PF0 bits 4..7, PF1 bits 7..0,
; PF2 bits 0..7. Reflection creates the other half.
RingPF0:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
RingPF1:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01
        dc.b $03,$03,$03,$03,$03,$06,$06,$06,$06,$06,$06,$06,$06
        dc.b $06,$06,$06,$06,$06,$06,$06,$06,$03,$03,$03,$03,$03
        dc.b $01,$01,$01,$01,$00,$00,$00,$00,$00,$00,$00,$00,$00
RingPF2:
        dc.b $C0,$F0,$F8,$FC,$FC,$FE,$3E,$0F,$0F,$07,$03,$03,$01
        dc.b $01,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$01
        dc.b $01,$03,$03,$07,$0F,$0F,$3E,$FE,$FC,$FC,$F8,$F0,$C0

        ORG $FFFC
        dc.w Reset
        dc.w Reset
