; P01-COL1 DRAFT | single synthetic 4-solid arena, P0 U1-LEG1 only
; 4 KiB NTSC standard mapper; no P1/halo/enemy/score. Not a product ROM.
; Original U1-LEG1 rows are frozen, top-first human input -> bottom-first ROM.
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
SWCHA       = $0280
SWCHB       = $0282
INTIM       = $0284
TIM64T      = $0296

PlayerX     = $80   ; CENTRE x in TIA colour clocks, 0..159
PlayerY     = $81   ; CENTRE y in 176-line arena, 0 at top
Level       = $82   ; 1,2,3
JoyState    = $83
SwitchState = $84
PrevSelect  = $85
Phase       = $86
DiagonalSkip= $87
SpriteHeight= $88
RowMapPtr   = $89   ; 2 bytes
GfxPtr      = $8B   ; 2 bytes
FrameCount  = $8D
Facing      = $8E   ; 0 future RIGHT = source old LEFT, 1 future LEFT = source old RIGHT
MotionDid   = $8F
TryX        = $90
TryY        = $91
TestLevel   = $92
RectPtr     = $93   ; 2 bytes
RectIndex   = $95
RenderX     = $96
RenderBottom= $97
HalfW       = $98
HalfH       = $99
GrowthBlocked = $9A

        SEG Code
        ORG $F000
Reset:
        sei
        cld
        ldx #$FF
        txs
        lda #0
        ldx #$7F
ClrRAM:
        sta $80,x
        dex
        bpl ClrRAM
        ldx #$2C
ClrTIA:
        sta $00,x
        dex
        bpl ClrTIA
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        lda #1
        sta Level
        lda #$0C
        sta COLUP0
        lda #$86
        sta COLUPF
        lda #$00
        sta COLUBK
        lda #1
        sta CTRLPF      ; horizontal reflect: four symmetric synthetic solids

Frame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC
        lda #43          ; 43*64 cycles; 37-line NTSC blank target
        sta TIM64T
        lda SWCHA
        sta JoyState
        lda SWCHB
        sta SwitchState
        inc FrameCount
        inc Phase
        lda Phase
        cmp #3
        bne PhaseGood
        lda #0
        sta Phase
PhaseGood:
        jsr DetectDiagonal
        lda #0
        sta MotionDid
        jsr MoveX
        jsr MoveY
        jsr DebugLevel
        jsr UpdateScale
        jsr UpdateGait
        lda PlayerX
        sec
        sbc HalfW
        sta RenderX
        lda #176
        sec
        sbc PlayerY
        sec
        sbc HalfH
        sta RenderBottom
        lda RenderX
        jsr PositionP0
        sta WSYNC
        sta HMOVE
BlankWait:
        lda INTIM
        bne BlankWait
        sta WSYNC
        lda #0
        sta VBLANK
        lda #0
        sta PF2
        ldx #192
Visible:
        sta WSYNC
        ldy PFCode,x
        lda PF0Choices,y
        sta PF0
        lda PF1Choices,y
        sta PF1
        txa
        sec
        sbc RenderBottom
        bcc BlankP0
        cmp SpriteHeight
        bcs BlankP0
        tay
        lda (RowMapPtr),y
        tay
        lda (GfxPtr),y
        sta GRP0
        jmp NextLine
BlankP0:
        lda #0
        sta GRP0
NextLine:
        dex
        bne Visible
        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        sta PF0
        sta PF1
        sta PF2
        ldx #30
OverScan:
        sta WSYNC
        dex
        bne OverScan
        jmp Frame

; 8 directions; two of each three diagonal frame updates, like P01.
DetectDiagonal:
        lda #0
        sta DiagonalSkip
        lda JoyState
        and #$C0
        cmp #$C0
        beq NoDiag
        lda JoyState
        and #$30
        cmp #$30
        beq NoDiag
        lda Phase
        cmp #2
        bne NoDiag
        lda #1
        sta DiagonalSkip
NoDiag:
        rts

; X-first, then Y. An axis is allowed only when the full expanded body
; is legal. Diagonal never jumps through a blocked corner. X priority
; on ambiguous corner slides is diagnostic, NOT final approved game feel.
MoveX:
        lda DiagonalSkip
        bne MoveXDone
        lda JoyState
        and #$40
        beq WantLeft
        lda JoyState
        and #$80
        bne MoveXDone
        lda #0
        sta Facing
        lda PlayerX
        clc
        adc #1
        sta TryX
        jmp CheckMoveX
WantLeft:
        lda #1
        sta Facing
        lda PlayerX
        sec
        sbc #1
        sta TryX
CheckMoveX:
        lda PlayerY
        sta TryY
        lda Level
        sta TestLevel
        jsr CandidateValid
        beq MoveXDone
        lda TryX
        sta PlayerX
        lda #1
        sta MotionDid
MoveXDone:
        rts
MoveY:
        lda DiagonalSkip
        bne MoveYDone
        lda JoyState
        and #$10
        beq WantUp
        lda JoyState
        and #$20
        bne MoveYDone
        lda PlayerY
        clc
        adc #1
        sta TryY
        jmp CheckMoveY
WantUp:
        lda PlayerY
        sec
        sbc #1
        sta TryY
CheckMoveY:
        lda PlayerX
        sta TryX
        lda Level
        sta TestLevel
        jsr CandidateValid
        beq MoveYDone
        lda TryY
        sta PlayerY
        lda #1
        sta MotionDid
MoveYDone:
        rts

; SELECT cycles L1->L2->L3->L1 only when proposed larger size is clear.
; A blocked grow lights the background red, never embeds body in solids.
DebugLevel:
        lda SwitchState
        and #2
        bne SelectUp
        lda PrevSelect
        bne DebugDone
        lda #1
        sta PrevSelect
        lda Level
        cmp #3
        bne TryGrow
        lda #1
        sta Level
        jmp GrowthOK
TryGrow:
        clc
        adc #1
        sta TestLevel
        lda PlayerX
        sta TryX
        lda PlayerY
        sta TryY
        jsr CandidateValid
        beq GrowthFail
        inc Level
GrowthOK:
        lda #0
        sta GrowthBlocked
        sta COLUBK
        rts
GrowthFail:
        lda #1
        sta GrowthBlocked
        lda #$42
        sta COLUBK
        rts
SelectUp:
        lda #0
        sta PrevSelect
DebugDone:
        rts

; For each candidate (TryX,TryY,TestLevel), K0 expanded rectangle
; tables: xmin inclusive, xmax exclusive, ymin inclusive, ymax exclusive.
; One source-only F01-inspired reflection-friendly scene, NOT canonical.
CandidateValid:
        ldx TestLevel
        lda TryX
        cmp MinCX,x
        bcc Invalid
        cmp MaxCX,x
        bcs Invalid
        lda TryY
        cmp MinCY,x
        bcc Invalid
        cmp MaxCY,x
        bcs Invalid
        lda RectLo,x
        sta RectPtr
        lda RectHi,x
        sta RectPtr+1
        lda #0
        sta RectIndex
RectLoop:
        ldy RectIndex
        lda TryX
        cmp (RectPtr),y
        bcc NextRect
        iny
        lda TryX
        cmp (RectPtr),y
        bcs NextRect
        iny
        lda TryY
        cmp (RectPtr),y
        bcc NextRect
        iny
        lda TryY
        cmp (RectPtr),y
        bcc Invalid
NextRect:
        lda RectIndex
        clc
        adc #4
        sta RectIndex
        cmp #16
        bcc RectLoop
        lda #1
        rts
Invalid:
        lda #0
        rts

UpdateScale:
        ldx Level
        lda WidthHalf,x
        sta HalfW
        lda HeightHalf,x
        sta HalfH
        lda SpriteHeights,x
        sta SpriteHeight
        lda PlayerSizes,x
        sta NUSIZ0
        lda MapLow,x
        sta RowMapPtr
        lda MapHigh,x
        sta RowMapPtr+1
        rts

UpdateGait:
        lda #0
        sta RectIndex ; reused scratch: graphics index 0 A-right,1 B-right,2 A-left,3 B-left
        lda Facing
        beq FaceReady
        lda #2
        sta RectIndex
FaceReady:
        lda MotionDid
        beq GaitReady
        lda FrameCount
        and #8
        beq GaitReady
        inc RectIndex
GaitReady:
        ldx RectIndex
        lda ArtLo,x
        sta GfxPtr
        lda ArtHi,x
        sta GfxPtr+1
        rts

PositionP0:
        sta WSYNC
        sec
P0Loop:
        sbc #15
        bcs P0Loop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP0
        sta RESP0
        rts

; All four user-approved bitmap tables are TOP_FIRST in source and
; reversed for the decreasing X visible kernel. RIGHT label uses the
; ORIGINAL U1-LEG1 LEFT source bitmap, and vice versa. Frozen bit-exact.
A_VISUAL_RIGHT:
        dc.b %00000110,%11000100,%01100100,%00111100
        dc.b %00111100,%00111101,%11111110,%01111100
        dc.b %01100110,%01011010,%01111110,%00100100
B_VISUAL_RIGHT:
        dc.b %01100000,%00100011,%00100110,%00111100
        dc.b %00111100,%10111110,%11111110,%01111100
        dc.b %01100110,%01011010,%01111110,%00100100
A_VISUAL_LEFT:
        dc.b %01100000,%00100011,%00100110,%00111100
        dc.b %00111100,%10111100,%01111111,%00111110
        dc.b %01100110,%01011010,%01111110,%00100100
B_VISUAL_LEFT:
        dc.b %00000110,%11000100,%01100100,%00111100
        dc.b %00111100,%01111101,%01111111,%00111110
        dc.b %01100110,%01011010,%01111110,%00100100

MapSmall:
        dc.b 0,1,2,3,4,5,6,7,8,9,10,11
MapMedium:
        dc.b 0,0,1,1,2,2,3,3,4,4,5,5
        dc.b 6,6,7,7,8,8,9,9,10,10,11,11
MapLarge:
        dc.b 0,0,0,1,1,1,2,2,2,3,3,3
        dc.b 4,4,4,5,5,5,6,6,6,7,7,7
        dc.b 8,8,8,9,9,9,10,10,10,11,11,11

; Visible synthetic obstacles: top x=[12,28) reflected to [132,148)
; at arena y=[24,48); lower x=[24,44) reflected to [116,136)
; at arena y=[136,152). 4 solids, not final world map.
; This physical scanline map is indexed by X=192..1 in VisibleLoop.
PFCode:
        ds 25,0           ; X=0..24 => no PF
        ds 16,2           ; X=25..40 => lower mirror pair
        ds 88,0           ; X=41..128 => empty
        ds 24,1           ; X=129..152 => upper mirror pair
        ds 40,0           ; X=153..192 => empty
PF0Choices:
        dc.b 0,$80,0
PF1Choices:
        dc.b 0,$E0,$3E
MinCX:  dc.b 0,8,12,20
MaxCX:  dc.b 0,153,149,141
MinCY:  dc.b 0,10,16,22
MaxCY:  dc.b 0,167,161,155
WidthHalf:
        dc.b 0,4,8,16
HeightHalf:
        dc.b 0,6,12,18
SpriteHeights:
        dc.b 0,12,24,36
PlayerSizes:
        dc.b 0,0,5,7
MapLow:
        dc.b 0,<MapSmall,<MapMedium,<MapLarge
MapHigh:
        dc.b 0,>MapSmall,>MapMedium,>MapLarge
ArtLo:
        dc.b <A_VISUAL_RIGHT,<B_VISUAL_RIGHT,<A_VISUAL_LEFT,<B_VISUAL_LEFT
ArtHi:
        dc.b >A_VISUAL_RIGHT,>B_VISUAL_RIGHT,>A_VISUAL_LEFT,>B_VISUAL_LEFT
RectLo:
        dc.b 0,<F01Diag_L1,<F01Diag_L2,<F01Diag_L3
RectHi:
        dc.b 0,>F01Diag_L1,>F01Diag_L2,>F01Diag_L3
; K0 source formula: full body +4 margin per side (x & y), half-open.
F01Diag_L1:
        dc.b 5,36,15,58
        dc.b 125,156,15,58
        dc.b 17,52,127,162
        dc.b 109,144,127,162
F01Diag_L2:
        dc.b 1,40,9,64
        dc.b 121,160,9,64
        dc.b 13,56,121,168
        dc.b 105,148,121,168
F01Diag_L3:
        dc.b 0,48,3,70
        dc.b 113,160,3,70
        dc.b 5,64,115,174
        dc.b 97,156,115,174

        ORG $FFFC
        dc.w Reset
        dc.w Reset
