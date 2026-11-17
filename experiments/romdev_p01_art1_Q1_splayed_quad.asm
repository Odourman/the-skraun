; THE SKRAUN — MAIN-authorized P01-ART1 P0 ONLY / TRUE STELLA READOUT
; No enemies, halo, PF objects, HUD, gameplay, new graphics, mapper, or production code.
; Exact historical 8x12 logical bitmap rows from P1/Q1, bottom-first ROM for
; descending visible X. TOP-FIRST expected rows protected by pixel tests.
; Automatic test stage each 48 NTSC frames: L1R,L1L,L2R,L2L,L3R,L3L;
; Diagnostic gait A/B each 8 frames, not joystick/gameplay movement.
        processor 6502
VSYNC      = $00
VBLANK     = $01
WSYNC      = $02
NUSIZ0     = $04
COLUP0     = $06
COLUBK     = $09
PF0        = $0D
PF1        = $0E
PF2        = $0F
RESP0      = $10
GRP0       = $1B
HMP0       = $20
HMOVE      = $2A
REFP0      = $0B
Stage      = $80     ; 0..5, two facings at each of three levels
StageFrame = $81     ; 0..47, 8-frame pose cadence
Level      = $82
PlayerX    = $83
PlayerY    = $84
SpriteH    = $85
Facing     = $86
Pose       = $87
MapPtr     = $88     ; 2 bytes
GfxPtr     = $8A     ; 2 bytes
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
        lda #$FF
        sta StageFrame
        lda #$0C
        sta COLUP0
        lda #$00
        sta COLUBK
        sta PF0
        sta PF1
        sta PF2
        sta REFP0     ; no hardware mirror; true source left mask in ROM
Frame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC
        sta WSYNC      ; VBLANK 1
        jsr UpdateStage
        sta WSYNC      ; VBLANK 2
        jsr UpdateScale
        sta WSYNC      ; VBLANK 3
        jsr UpdateFacing
        sta WSYNC      ; VBLANK 4
        jsr UpdatePose
        sta WSYNC      ; VBLANK 5
        lda PlayerX
        jsr PositionP0 ; VBLANK 6, owns WSYNC
        sta WSYNC      ; VBLANK 7
        sta HMOVE
        ldx #30
VBlankPad:
        sta WSYNC      ; VBLANK 8..37
        dex
        bne VBlankPad
        lda #0
        sta VBLANK
        ldx #192
Visible:
        sta WSYNC      ; one real NTSC scanline per output row
        txa
        sec
        sbc PlayerY    ; X decreases top-to-bottom
        bcc Blank
        cmp SpriteH
        bcs Blank
        tay
        lda (MapPtr),y
        tay
        lda (GfxPtr),y
        sta GRP0
        jmp Next
Blank:
        lda #0
        sta GRP0
Next:
        dex
        bne Visible
        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        ldx #30
OverScan:
        sta WSYNC
        dex
        bne OverScan
        jmp Frame       ; 3 VSYNC+37 VBLANK+192 visible+30 overscan=262
UpdateStage:
        inc StageFrame
        lda StageFrame
        cmp #48
        bne StageDone
        lda #0
        sta StageFrame
        inc Stage
        lda Stage
        cmp #6
        bne StageDone
        lda #0
        sta Stage
StageDone:
        rts
UpdateScale:
        lda Stage
        lsr
        clc
        adc #1
        sta Level
        cmp #1
        bne ScaleMedium
        lda #12
        sta SpriteH
        lda #90
        sta PlayerY
        lda #76
        sta PlayerX
        lda #0
        sta NUSIZ0
        lda #<MapSmall
        sta MapPtr
        lda #>MapSmall
        sta MapPtr+1
        rts
ScaleMedium:
        cmp #2
        bne ScaleLarge
        lda #24
        sta SpriteH
        lda #84
        sta PlayerY
        lda #72
        sta PlayerX
        lda #5
        sta NUSIZ0
        lda #<MapMedium
        sta MapPtr
        lda #>MapMedium
        sta MapPtr+1
        rts
ScaleLarge:
        lda #36
        sta SpriteH
        lda #78
        sta PlayerY
        lda #64
        sta PlayerX
        lda #7
        sta NUSIZ0
        lda #<MapLarge
        sta MapPtr
        lda #>MapLarge
        sta MapPtr+1
        rts
UpdateFacing:
        lda Stage
        and #1
        sta Facing
        rts
UpdatePose:
        lda StageFrame
        and #$08
        beq PoseA
        lda #1
        bne PoseSelected
PoseA:
        lda #0
PoseSelected:
        sta Pose
        lda Facing
        asl
        ora Pose
        asl
        tax
        lda PosePointerTable,x
        sta GfxPtr
        lda PosePointerTable+1,x
        sta GfxPtr+1
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
PosePointerTable:
        dc.w GfxRightA,GfxRightB,GfxLeftA,GfxLeftB
; SOURCE candidate Q1_splayed_quad, EXACT 8x12 rows, source Q1, NO ART EDITS.
GfxRightA:
        dc.b %10000010
        dc.b %11011011
        dc.b %01111110
        dc.b %00111100
        dc.b %00111100
        dc.b %10111111
        dc.b %11111100
        dc.b %00111100
        dc.b %00111100
        dc.b %01011010
        dc.b %01111110
        dc.b %00100100
GfxRightB:
        dc.b %01000001
        dc.b %11011011
        dc.b %01111110
        dc.b %00111100
        dc.b %00111100
        dc.b %11111101
        dc.b %00111111
        dc.b %00111100
        dc.b %00111100
        dc.b %01011010
        dc.b %01111110
        dc.b %00100100
GfxLeftA:
        dc.b %01000001
        dc.b %11011011
        dc.b %01111110
        dc.b %00111100
        dc.b %00111100
        dc.b %11111101
        dc.b %00111111
        dc.b %00111100
        dc.b %00111100
        dc.b %01011010
        dc.b %01111110
        dc.b %00100100
GfxLeftB:
        dc.b %10000010
        dc.b %11011011
        dc.b %01111110
        dc.b %00111100
        dc.b %00111100
        dc.b %10111111
        dc.b %11111100
        dc.b %00111100
        dc.b %00111100
        dc.b %01011010
        dc.b %01111110
        dc.b %00100100
MapSmall:
        dc.b 0,1,2,3,4,5,6,7,8,9,10,11
MapMedium:
        dc.b 0,0,1,1,2,2,3,3,4,4,5,5
        dc.b 6,6,7,7,8,8,9,9,10,10,11,11
MapLarge:
        dc.b 0,0,0,1,1,1,2,2,2,3,3,3
        dc.b 4,4,4,5,5,5,6,6,6,7,7,7
        dc.b 8,8,8,9,9,9,10,10,10,11,11
        ORG $FFFC
        dc.w Reset
        dc.w Reset
