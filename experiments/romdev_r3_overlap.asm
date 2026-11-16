; R3 overlap: rotate3; PF alternate. Two-line vertical P1 graphics; 60/30/20Hz measured in Stella not assumed.
; THE SKRAUN P02-R3 REAL 6507/TIA 4K NTSC DIAGNOSTIC; NO B3c/AI/PRODUCTION.
; R3: in-RIOT 89-byte per-frame P1 raster buffer, 3 independent enemy X/Y RAM,
; VDELP1 2-physical-line sprite preloading and independent horizontal positioning.
; P0 actual 4x width/36 physical rows, gold level3 48-clock/72-row ellipse,
; three fixed synthetic obstacle columns. 13 genuine SWCHA 4-clock centers.
        processor 6502
VSYNC      = $00
VBLANK     = $01
WSYNC      = $02
NUSIZ0     = $04
NUSIZ1     = $05
COLUP0     = $06
COLUP1     = $07
COLUPF     = $08
COLUBK     = $09
CTRLPF     = $0A
PF0        = $0D
PF1        = $0E
PF2        = $0F
RESP0      = $10
RESP1      = $11
GRP0       = $1B
GRP1       = $1C
HMP0       = $20
HMP1       = $21
VDELP1     = $26
HMOVE      = $2A
SWCHA      = $0280
INTIM      = $0284
TIM64T     = $0296
Mode       = $80
Frames     = $81
L1Ptr      = $82
L2Ptr      = $84
R0Ptr      = $86
R1Ptr      = $88
R2Ptr      = $8A
Slot       = $8C
ShapePtr   = $8D
ActiveX    = $8F
EnemyX0    = $90
EnemyX1    = $91
EnemyX2    = $92
EnemyY0    = $93
EnemyY1    = $94
EnemyY2    = $95
RasterSave = $96
P1Buf      = $A0       ; 89B $A0..$F8; 7 bytes free at $F9..$FF
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
        lda #6
        sta Mode
        lda #$0C
        sta COLUP0
        lda #$2E
        sta COLUPF
        lda #7
        sta NUSIZ0
        lda #0
        sta NUSIZ1
        lda #1
        sta VDELP1
        lda #$20
        sta EnemyX0
        lda #$65
        sta EnemyX1
        lda #$93
        sta EnemyX2
        lda #$4E
        sta EnemyY0
        lda #$4E
        sta EnemyY1
        lda #$4E
        sta EnemyY2
Frame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC
        lda #44
        sta TIM64T
        jsr UpdateMotion
        inc Slot
        lda Slot
        cmp #3
        bcc SlotOK
        lda #0
        sta Slot
SlotOK:
        jsr SelectPtrs
        jsr ClearSpriteBuffer
        jsr DrawSpriteIntoBuffer
        jsr SelectP1
        ldx Mode
        lda P0XTable,x
        jsr PositionP0
        sta WSYNC
        lda ActiveX
        jsr PositionP1
        sta WSYNC
        sta HMOVE
VBlankWait:
        lda INTIM
        bne VBlankWait
        sta WSYNC
        lda #0
        sta VBLANK
        ldy #16
HUD:
        sta WSYNC
        lda #$9C
        sta COLUPF
        lda #$F0
        sta PF0
        sta PF1
        lda #0
        sta PF2
        dey
        bne HUD
        lda Frames
        and #1
        bne PFBlue
        lda #$2E
        bne PFColorDone
PFBlue:
        lda #$86
PFColorDone:
        sta COLUPF
        lda #0
        sta PF0
        sta PF1
        sta PF2
        lda P1Buf
        sta GRP1
        ldx #176
R3Pair:
        sta WSYNC             ; line A, PF right-PF2 explicitly scheduled
        lda Troll3,x
        sta GRP0
        ldy RingRowMap,x
        lda #0
        sta PF0
        lda (L1Ptr),y
        sta PF1
        lda (L2Ptr),y
        sta PF2
        lda (R0Ptr),y
        sta PF0
        lda (R1Ptr),y
        sta PF1
        lda (R2Ptr),y
        sta PF2
        dex
        sta WSYNC             ; line B, Y reused, P1 next pair buffered after beam
        lda Troll3,x
        sta GRP0
        lda #0
        sta PF0
        lda (L1Ptr),y
        sta PF1
        lda (L2Ptr),y
        sta PF2
        lda (R0Ptr),y
        sta PF0
        lda (R1Ptr),y
        sta PF1
        lda (R2Ptr),y
        sta PF2
        ldy SpriteRowMap,x
        lda P1Buf,y
        sta GRP1
        dex
        bne R3Pair
        sta WSYNC
        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        sta GRP1
        sta PF0
        sta PF1
        sta PF2
        ldx #29
Overscan:
        sta WSYNC
        dex
        bne Overscan
        jmp Frame
UpdateMotion:
        inc Frames
        lda Frames
        and #1
        bne MotionDone
        lda SWCHA
        and #$C0
        cmp #$40
        beq MoveRight
        cmp #$80
        beq MoveLeft
MotionDone:
        rts
MoveRight:
        lda Mode
        cmp #12
        bcs MotionDone
        inc Mode
        rts
MoveLeft:
        lda Mode
        beq MotionDone
        dec Mode
        rts
SelectPtrs:
        ldx Mode
SelectPhase:
        lda Frames
        and #1
        beq SelectRing
        txa
        clc
        adc #13
        tax
SelectRing:
        lda L1Lo,x
        sta L1Ptr
        lda L1Hi,x
        sta L1Ptr+1
        lda L2Lo,x
        sta L2Ptr
        lda L2Hi,x
        sta L2Ptr+1
        lda R0Lo,x
        sta R0Ptr
        lda R0Hi,x
        sta R0Ptr+1
        lda R1Lo,x
        sta R1Ptr
        lda R1Hi,x
        sta R1Ptr+1
        lda R2Lo,x
        sta R2Ptr
        lda R2Hi,x
        sta R2Ptr+1
        rts
ClearSpriteBuffer:
        lda #0
        ldy #88
ZeroP1:
        sta P1Buf,y
        dey
        bpl ZeroP1
        rts
DrawSpriteIntoBuffer:
        ldx Slot
        lda EnemyY0,x
        lsr
        tax
        ldy Slot
        lda EnemyArtLo,y
        sta ShapePtr
        lda EnemyArtHi,y
        sta ShapePtr+1
        ldy #0
DrawOneRow:
        lda (ShapePtr),y
        sta P1Buf,x
        inx
        iny
        cpy #8
        bne DrawOneRow
        rts
SelectP1:
        ldx Slot
        lda EnemyX0,x
        sta ActiveX
        lda EnemyColor,x
        sta COLUP1
        rts
PositionP0:
        sta WSYNC
        sec
Position0Loop:
        sbc #15
        bcs Position0Loop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP0
        sta RESP0
        rts
PositionP1:
        sta WSYNC
        sec
Position1Loop:
        sbc #15
        bcs Position1Loop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP1
        sta RESP1
        rts

        ORG $F500
L1Lo:
        dc.b <M_halo_L1_56,<M_halo_L1_60,<M_halo_L1_64,<M_halo_L1_68,<M_halo_L1_72,<M_halo_L1_76,<M_halo_L1_80,<M_halo_L1_84,<M_halo_L1_88,<M_halo_L1_92,<M_halo_L1_96,<M_halo_L1_100,<M_halo_L1_104,<M_scenery_L1_56,<M_scenery_L1_60,<M_scenery_L1_64,<M_scenery_L1_68,<M_scenery_L1_72,<M_scenery_L1_76,<M_scenery_L1_80,<M_scenery_L1_84,<M_scenery_L1_88,<M_scenery_L1_92,<M_scenery_L1_96,<M_scenery_L1_100,<M_scenery_L1_104
L1Hi:
        dc.b >M_halo_L1_56,>M_halo_L1_60,>M_halo_L1_64,>M_halo_L1_68,>M_halo_L1_72,>M_halo_L1_76,>M_halo_L1_80,>M_halo_L1_84,>M_halo_L1_88,>M_halo_L1_92,>M_halo_L1_96,>M_halo_L1_100,>M_halo_L1_104,>M_scenery_L1_56,>M_scenery_L1_60,>M_scenery_L1_64,>M_scenery_L1_68,>M_scenery_L1_72,>M_scenery_L1_76,>M_scenery_L1_80,>M_scenery_L1_84,>M_scenery_L1_88,>M_scenery_L1_92,>M_scenery_L1_96,>M_scenery_L1_100,>M_scenery_L1_104
L2Lo:
        dc.b <M_halo_L2_56,<M_halo_L2_60,<M_halo_L2_64,<M_halo_L2_68,<M_halo_L2_72,<M_halo_L2_76,<M_halo_L2_80,<M_halo_L2_84,<M_halo_L2_88,<M_halo_L2_92,<M_halo_L2_96,<M_halo_L2_100,<M_halo_L2_104,<M_scenery_L2_56,<M_scenery_L2_60,<M_scenery_L2_64,<M_scenery_L2_68,<M_scenery_L2_72,<M_scenery_L2_76,<M_scenery_L2_80,<M_scenery_L2_84,<M_scenery_L2_88,<M_scenery_L2_92,<M_scenery_L2_96,<M_scenery_L2_100,<M_scenery_L2_104
L2Hi:
        dc.b >M_halo_L2_56,>M_halo_L2_60,>M_halo_L2_64,>M_halo_L2_68,>M_halo_L2_72,>M_halo_L2_76,>M_halo_L2_80,>M_halo_L2_84,>M_halo_L2_88,>M_halo_L2_92,>M_halo_L2_96,>M_halo_L2_100,>M_halo_L2_104,>M_scenery_L2_56,>M_scenery_L2_60,>M_scenery_L2_64,>M_scenery_L2_68,>M_scenery_L2_72,>M_scenery_L2_76,>M_scenery_L2_80,>M_scenery_L2_84,>M_scenery_L2_88,>M_scenery_L2_92,>M_scenery_L2_96,>M_scenery_L2_100,>M_scenery_L2_104
R0Lo:
        dc.b <M_halo_R0_56,<M_halo_R0_60,<M_halo_R0_64,<M_halo_R0_68,<M_halo_R0_72,<M_halo_R0_76,<M_halo_R0_80,<M_halo_R0_84,<M_halo_R0_88,<M_halo_R0_92,<M_halo_R0_96,<M_halo_R0_100,<M_halo_R0_104,<M_scenery_R0_56,<M_scenery_R0_60,<M_scenery_R0_64,<M_scenery_R0_68,<M_scenery_R0_72,<M_scenery_R0_76,<M_scenery_R0_80,<M_scenery_R0_84,<M_scenery_R0_88,<M_scenery_R0_92,<M_scenery_R0_96,<M_scenery_R0_100,<M_scenery_R0_104
R0Hi:
        dc.b >M_halo_R0_56,>M_halo_R0_60,>M_halo_R0_64,>M_halo_R0_68,>M_halo_R0_72,>M_halo_R0_76,>M_halo_R0_80,>M_halo_R0_84,>M_halo_R0_88,>M_halo_R0_92,>M_halo_R0_96,>M_halo_R0_100,>M_halo_R0_104,>M_scenery_R0_56,>M_scenery_R0_60,>M_scenery_R0_64,>M_scenery_R0_68,>M_scenery_R0_72,>M_scenery_R0_76,>M_scenery_R0_80,>M_scenery_R0_84,>M_scenery_R0_88,>M_scenery_R0_92,>M_scenery_R0_96,>M_scenery_R0_100,>M_scenery_R0_104
R1Lo:
        dc.b <M_halo_R1_56,<M_halo_R1_60,<M_halo_R1_64,<M_halo_R1_68,<M_halo_R1_72,<M_halo_R1_76,<M_halo_R1_80,<M_halo_R1_84,<M_halo_R1_88,<M_halo_R1_92,<M_halo_R1_96,<M_halo_R1_100,<M_halo_R1_104,<M_scenery_R1_56,<M_scenery_R1_60,<M_scenery_R1_64,<M_scenery_R1_68,<M_scenery_R1_72,<M_scenery_R1_76,<M_scenery_R1_80,<M_scenery_R1_84,<M_scenery_R1_88,<M_scenery_R1_92,<M_scenery_R1_96,<M_scenery_R1_100,<M_scenery_R1_104
R1Hi:
        dc.b >M_halo_R1_56,>M_halo_R1_60,>M_halo_R1_64,>M_halo_R1_68,>M_halo_R1_72,>M_halo_R1_76,>M_halo_R1_80,>M_halo_R1_84,>M_halo_R1_88,>M_halo_R1_92,>M_halo_R1_96,>M_halo_R1_100,>M_halo_R1_104,>M_scenery_R1_56,>M_scenery_R1_60,>M_scenery_R1_64,>M_scenery_R1_68,>M_scenery_R1_72,>M_scenery_R1_76,>M_scenery_R1_80,>M_scenery_R1_84,>M_scenery_R1_88,>M_scenery_R1_92,>M_scenery_R1_96,>M_scenery_R1_100,>M_scenery_R1_104
R2Lo:
        dc.b <M_halo_R2_56,<M_halo_R2_60,<M_halo_R2_64,<M_halo_R2_68,<M_halo_R2_72,<M_halo_R2_76,<M_halo_R2_80,<M_halo_R2_84,<M_halo_R2_88,<M_halo_R2_92,<M_halo_R2_96,<M_halo_R2_100,<M_halo_R2_104,<M_scenery_R2_56,<M_scenery_R2_60,<M_scenery_R2_64,<M_scenery_R2_68,<M_scenery_R2_72,<M_scenery_R2_76,<M_scenery_R2_80,<M_scenery_R2_84,<M_scenery_R2_88,<M_scenery_R2_92,<M_scenery_R2_96,<M_scenery_R2_100,<M_scenery_R2_104
R2Hi:
        dc.b >M_halo_R2_56,>M_halo_R2_60,>M_halo_R2_64,>M_halo_R2_68,>M_halo_R2_72,>M_halo_R2_76,>M_halo_R2_80,>M_halo_R2_84,>M_halo_R2_88,>M_halo_R2_92,>M_halo_R2_96,>M_halo_R2_100,>M_halo_R2_104,>M_scenery_R2_56,>M_scenery_R2_60,>M_scenery_R2_64,>M_scenery_R2_68,>M_scenery_R2_72,>M_scenery_R2_76,>M_scenery_R2_80,>M_scenery_R2_84,>M_scenery_R2_88,>M_scenery_R2_92,>M_scenery_R2_96,>M_scenery_R2_100,>M_scenery_R2_104
P0XTable:
        dc.b $2A,$2E,$32,$36,$3A,$3E,$42,$46,$4A,$4E,$52,$56
        dc.b $5A
EnemyArtLo:
        dc.b <EnemyArt0,<EnemyArt1,<EnemyArt2
EnemyArtHi:
        dc.b >EnemyArt0,>EnemyArt1,>EnemyArt2
EnemyColor:
        dc.b $44,$48,$C6
EnemyArt0:
        dc.b $18,$3C,$7E,$DB,$5A,$24,$66,$42
EnemyArt1:
        dc.b $24,$7E,$5A,$DB,$7E,$3C,$66,$81
EnemyArt2:
        dc.b $18,$3C,$7E,$5A,$7E,$18,$24,$42
        ORG $F650
RingRowMap:
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$00
        dc.b $00,$01,$01,$02,$02,$03,$03,$04,$04,$05,$05,$06
        dc.b $06,$07,$07,$08,$08,$09,$09,$0A,$0A,$0B,$0B,$0C
        dc.b $0C,$0D,$0D,$0E,$0E,$0F,$0F,$10,$10,$11,$11,$11
        dc.b $11,$10,$10,$0F,$0F,$0E,$0E,$0D,$0D,$0C,$0C,$0B
        dc.b $0B,$0A,$0A,$09,$09,$08,$08,$07,$07,$06,$06,$05
        dc.b $05,$04,$04,$03,$03,$02,$02,$01,$01,$00,$00,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12
SpriteRowMap:
        dc.b $58,$58,$57,$57,$56,$56,$55,$55,$54,$54,$53,$53
        dc.b $52,$52,$51,$51,$50,$50,$4F,$4F,$4E,$4E,$4D,$4D
        dc.b $4C,$4C,$4B,$4B,$4A,$4A,$49,$49,$48,$48,$47,$47
        dc.b $46,$46,$45,$45,$44,$44,$43,$43,$42,$42,$41,$41
        dc.b $40,$40,$3F,$3F,$3E,$3E,$3D,$3D,$3C,$3C,$3B,$3B
        dc.b $3A,$3A,$39,$39,$38,$38,$37,$37,$36,$36,$35,$35
        dc.b $34,$34,$33,$33,$32,$32,$31,$31,$30,$30,$2F,$2F
        dc.b $2E,$2E,$2D,$2D,$2C,$2C,$2B,$2B,$2A,$2A,$29,$29
        dc.b $28,$28,$27,$27,$26,$26,$25,$25,$24,$24,$23,$23
        dc.b $22,$22,$21,$21,$20,$20,$1F,$1F,$1E,$1E,$1D,$1D
        dc.b $1C,$1C,$1B,$1B,$1A,$1A,$19,$19,$18,$18,$17,$17
        dc.b $16,$16,$15,$15,$14,$14,$13,$13,$12,$12,$11,$11
        dc.b $10,$10,$0F,$0F,$0E,$0E,$0D,$0D,$0C,$0C,$0B,$0B
        dc.b $0A,$0A,$09,$09,$08,$08,$07,$07,$06,$06,$05,$05
        dc.b $04,$04,$03,$03,$02,$02,$01,$01,$00
Troll3:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$24,$24,$24,$7E,$7E,$7E
        dc.b $7E,$7E,$7E,$5A,$5A,$5A,$7E,$7E,$7E,$FD,$FD,$FD
        dc.b $9D,$9D,$9D,$3C,$3C,$3C,$7E,$7E,$7E,$64,$64,$64
        dc.b $46,$46,$46,$C2,$C2,$C2,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00
        ORG $F880
M_halo_L1_56:
        dc.b $00,$00,$00,$01,$01,$02,$02,$02,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$08,$00
M_halo_L2_56:
        dc.b $04,$1F,$1F,$31,$20,$60,$40,$40,$C0,$80,$80,$80
        dc.b $80,$80,$80,$80,$80,$80,$00
M_halo_R0_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$10,$00
M_halo_R1_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R2_56 = M_halo_R1_56
M_halo_L1_60:
        dc.b $00,$00,$00,$00,$00,$01,$01,$01,$02,$02,$02,$02
        dc.b $02,$02,$02,$02,$02,$04,$00
M_halo_L2_60:
        dc.b $08,$3E,$3E,$63,$41,$C0,$80,$80,$80,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
        ORG $F900
M_halo_R0_60:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$10,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$30,$00
M_halo_R1_60 = M_halo_R1_56
M_halo_R2_60 = M_halo_R1_56
M_halo_L1_64:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01
        dc.b $01,$01,$01,$01,$01,$02,$00
M_halo_L2_64:
        dc.b $10,$7C,$7C,$C6,$82,$81,$01,$01,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R0_64:
        dc.b $00,$00,$00,$00,$00,$10,$10,$10,$30,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$60,$00
M_halo_R1_64 = M_halo_R1_56
M_halo_R2_64 = M_halo_R1_56
M_halo_L1_68:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$01,$00
M_halo_L2_68:
        dc.b $20,$F8,$F8,$8C,$04,$02,$02,$02,$01,$01,$01,$01
        dc.b $01,$01,$01,$01,$01,$00,$00
M_halo_R0_68:
        dc.b $00,$00,$00,$10,$10,$30,$20,$20,$60,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$C0,$00
M_halo_R1_68 = M_halo_R1_56
M_halo_R2_68 = M_halo_R1_56
M_halo_L1_72 = M_halo_R1_56
M_halo_L2_72:
        dc.b $40,$F0,$F0,$18,$08,$04,$04,$04,$02,$02,$02,$02
        dc.b $02,$02,$02,$02,$02,$01,$00
M_halo_R0_72:
        dc.b $00,$10,$10,$30,$20,$60,$40,$40,$C0,$80,$80,$80
        dc.b $80,$80,$80,$80,$80,$80,$00
M_halo_R1_72:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$80,$00
M_halo_R2_72 = M_halo_R1_56
M_halo_L1_76 = M_halo_R1_56
M_halo_L2_76:
        dc.b $80,$E0,$E0,$30,$10,$08,$08,$08,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$02,$00
M_halo_R0_76:
        dc.b $00,$30,$30,$60,$40,$C0,$80,$80,$80,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R1_76:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80
        dc.b $80,$80,$80,$80,$80,$C0,$00
M_halo_R2_76 = M_halo_R1_56
M_halo_L1_80 = M_halo_R1_56
        ORG $FA00
M_halo_L2_80:
        dc.b $00,$C0,$C0,$60,$20,$10,$10,$10,$08,$08,$08,$08
        dc.b $08,$08,$08,$08,$08,$04,$00
M_halo_R0_80:
        dc.b $10,$70,$70,$C0,$80,$80,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R1_80:
        dc.b $00,$00,$00,$00,$00,$80,$80,$80,$C0,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$60,$00
M_halo_R2_80 = M_halo_R1_56
M_halo_L1_84 = M_halo_R1_56
M_halo_L2_84:
        dc.b $00,$80,$80,$C0,$40,$20,$20,$20,$10,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$08,$00
M_halo_R0_84:
        dc.b $20,$F0,$F0,$80,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R1_84:
        dc.b $00,$00,$00,$80,$80,$C0,$40,$40,$60,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$30,$00
M_halo_R2_84 = M_halo_R1_56
M_halo_L1_88 = M_halo_R1_56
M_halo_L2_88:
        dc.b $00,$00,$00,$80,$80,$40,$40,$40,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$10,$00
M_halo_R0_88:
        dc.b $40,$F0,$F0,$10,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R1_88:
        dc.b $00,$80,$80,$C0,$40,$60,$20,$20,$30,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$18,$00
M_halo_R2_88 = M_halo_R1_56
M_halo_L1_92 = M_halo_R1_56
M_halo_L2_92:
        dc.b $00,$00,$00,$00,$00,$80,$80,$80,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$20,$00
M_halo_R0_92:
        dc.b $80,$E0,$E0,$30,$10,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R1_92:
        dc.b $00,$C0,$C0,$60,$20,$30,$10,$10,$18,$08,$08,$08
        dc.b $08,$08,$08,$08,$08,$0C,$00
M_halo_R2_92 = M_halo_R1_56
M_halo_L1_96 = M_halo_R1_56
M_halo_L2_96:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80
        dc.b $80,$80,$80,$80,$80,$40,$00
        ORG $FB00
M_halo_R0_96:
        dc.b $00,$C0,$C0,$60,$20,$10,$10,$10,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00
M_halo_R1_96:
        dc.b $80,$E0,$E0,$30,$10,$18,$08,$08,$0C,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$06,$00
M_halo_R2_96 = M_halo_R1_56
M_halo_L1_100 = M_halo_R1_56
M_halo_L2_100 = M_halo_R1_72
M_halo_R0_100:
        dc.b $00,$80,$80,$C0,$40,$20,$20,$20,$10,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$00,$00
M_halo_R1_100:
        dc.b $40,$F0,$F0,$18,$08,$0C,$04,$04,$06,$02,$02,$02
        dc.b $02,$02,$02,$02,$02,$03,$00
M_halo_R2_100 = M_halo_R1_56
M_halo_L1_104 = M_halo_R1_56
M_halo_L2_104 = M_halo_R1_56
M_halo_R0_104 = M_halo_L2_88
M_halo_R1_104:
        dc.b $20,$F8,$F8,$8C,$04,$06,$02,$02,$03,$01,$01,$01
        dc.b $01,$01,$01,$01,$01,$01,$00
M_halo_R2_104 = M_halo_L1_68
M_scenery_L1_56 = M_halo_R1_56
M_scenery_L2_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$04,$04
        dc.b $04,$04,$04,$04,$04,$04,$00
M_scenery_R0_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$00
M_scenery_R1_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$10,$10
        dc.b $10,$10,$10,$10,$10,$10,$00
M_scenery_R2_56 = M_halo_R1_56
M_scenery_L1_60 = M_halo_R1_56
M_scenery_L2_60 = M_scenery_L2_56
M_scenery_R0_60 = M_scenery_R0_56
M_scenery_R1_60 = M_scenery_R1_56
M_scenery_R2_60 = M_halo_R1_56
M_scenery_L1_64 = M_halo_R1_56
M_scenery_L2_64 = M_scenery_L2_56
M_scenery_R0_64 = M_scenery_R0_56
M_scenery_R1_64 = M_scenery_R1_56
M_scenery_R2_64 = M_halo_R1_56
M_scenery_L1_68 = M_halo_R1_56
M_scenery_L2_68 = M_scenery_L2_56
M_scenery_R0_68 = M_scenery_R0_56
M_scenery_R1_68 = M_scenery_R1_56
M_scenery_R2_68 = M_halo_R1_56
M_scenery_L1_72 = M_halo_R1_56
M_scenery_L2_72 = M_scenery_L2_56
M_scenery_R0_72 = M_scenery_R0_56
M_scenery_R1_72 = M_scenery_R1_56
M_scenery_R2_72 = M_halo_R1_56
M_scenery_L1_76 = M_halo_R1_56
M_scenery_L2_76 = M_scenery_L2_56
M_scenery_R0_76 = M_scenery_R0_56
M_scenery_R1_76 = M_scenery_R1_56
M_scenery_R2_76 = M_halo_R1_56
M_scenery_L1_80 = M_halo_R1_56
M_scenery_L2_80 = M_scenery_L2_56
M_scenery_R0_80 = M_scenery_R0_56
M_scenery_R1_80 = M_scenery_R1_56
M_scenery_R2_80 = M_halo_R1_56
M_scenery_L1_84 = M_halo_R1_56
M_scenery_L2_84 = M_scenery_L2_56
M_scenery_R0_84 = M_scenery_R0_56
M_scenery_R1_84 = M_scenery_R1_56
M_scenery_R2_84 = M_halo_R1_56
M_scenery_L1_88 = M_halo_R1_56
M_scenery_L2_88 = M_scenery_L2_56
M_scenery_R0_88 = M_scenery_R0_56
M_scenery_R1_88 = M_scenery_R1_56
M_scenery_R2_88 = M_halo_R1_56
M_scenery_L1_92 = M_halo_R1_56
M_scenery_L2_92 = M_scenery_L2_56
M_scenery_R0_92 = M_scenery_R0_56
M_scenery_R1_92 = M_scenery_R1_56
M_scenery_R2_92 = M_halo_R1_56
M_scenery_L1_96 = M_halo_R1_56
M_scenery_L2_96 = M_scenery_L2_56
M_scenery_R0_96 = M_scenery_R0_56
M_scenery_R1_96 = M_scenery_R1_56
M_scenery_R2_96 = M_halo_R1_56
M_scenery_L1_100 = M_halo_R1_56
M_scenery_L2_100 = M_scenery_L2_56
M_scenery_R0_100 = M_scenery_R0_56
M_scenery_R1_100 = M_scenery_R1_56
M_scenery_R2_100 = M_halo_R1_56
M_scenery_L1_104 = M_halo_R1_56
M_scenery_L2_104 = M_scenery_L2_56
M_scenery_R0_104 = M_scenery_R0_56
M_scenery_R1_104 = M_scenery_R1_56
M_scenery_R2_104 = M_halo_R1_56
        ORG $FFFC
        dc.w Reset
        dc.w Reset
