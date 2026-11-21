; PLAY1-H DRAFT | Y-follow PF2 physical renderer diagnostic; strict bounded source copy of frozen PLAY1
; Derived exactly from frozen COL1 PR27 commit 90f89441b41a2e82408581b81d3743b1423e5cdb
; 4 KiB NTSC original 6507/TIA. One stationary P1 TRAINING dummy only; NO production enemy architecture.
; Original U1-LEG1 rows are frozen, top-first human input -> bottom-first ROM.
        processor 6502
VSYNC       = $00
VBLANK      = $01
WSYNC       = $02
NUSIZ0      = $04
NUSIZ1      = $05
COLUP0      = $06
COLUP1      = $07
COLUPF      = $08
COLUBK      = $09
CTRLPF      = $0A
PF0         = $0D
PF1         = $0E
PF2         = $0F
RESP0       = $10
RESP1       = $11
RESBL       = $14
GRP0        = $1B
GRP1        = $1C
ENABL       = $1F
HMP0        = $20
HMP1        = $21
HMBL        = $24
HMOVE       = $2A
INPT4       = $3C
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
BaseX       = $9B       ; original X for strict diagonal Y-projection
OrbMask     = $9C       ; 2 = BL visible, 0 = consumed temporarily
OrbTimer    = $9D       ; bounded 90f return for L3 demonstration
HaloFrames  = $9E       ; 30 NTSC frames when FIRE pressed
HaloRecover = $9F       ; 60/36/15 f cooldown AFTER halo ends
HaloRadius  = $A0       ; logical 360-degree square/Chebyshev radius
TargetAlive = $A1       ; one frozen original R3 knight P1 dummy
TargetFlash = $A2       ; death feedback countdown
CheckDX     = $A3
CheckDY     = $A4
HaloVisualMask = $A5   ; previous level-dependent contour bits
HaloRowPtr = $A6         ; 16-bit ROM row pointer shifted by real PlayerY, computed in VBLANK

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
        lda #$11
        sta CTRLPF      ; original 4 mirrored obstacles; 2x BL orb
        lda #$9E
        sta COLUP1      ; light-blue diagnostic knight byte, NOT final palette
        lda #2
        sta OrbMask
        lda #1
        sta TargetAlive
        lda #125
        jsr PositionP1
        lda #96
        jsr PositionBall
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMP1
        sta HMBL

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
        lda PlayerX
        sta BaseX
        lda #0
        sta MotionDid
        jsr MoveX
        jsr MoveY
        jsr DebugLevel
        jsr UpdateScale
        jsr UpdateGait
        ; Real signed dynamic Y shift without source bitmap modification.
        ; HaloPF2Rows begins at FE80; FE80 + (PlayerY-112) = FE10+PlayerY.
        ; Safe pointer range FE1A..FEB7; X 1..192 reads FE1B..FF77.
        lda PlayerY
        clc
        adc #$10
        sta HaloRowPtr
        lda #$FE
        sta HaloRowPtr+1
        lda PlayerX
        sec
        sbc HalfW
        sta RenderX
        lda #177            ; pre-offset P0 bottom; remove SBC #1 in scanline
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
        lda #0            ; preloaded GRP0 for first (empty) visible row
Visible:
        sta WSYNC
        sta GRP0          ; P0 first, frozen U1-LEG1 (cycle3 after WSYNC)
        ; PF byte writes FIRST, before left PF cell deadlines.
        lda PlayPF0,x
        sta PF0           ; c10, before visible left PF0
        lda PlayPF1,x
        sta PF1           ; c17, before visible left PF1
        txa
        tay
        lda (HaloRowPtr),y
        and HaloVisualMask
        sta PF2           ; c27, before left PF2 beam deadline
        ; P1 x125 and BL x96 are beyond these register write deadlines.
        lda DummyScan,x
        sta GRP1          ; c34, original R3 knight on P1, one dummy
        lda OrbScan,x
        and OrbMask
        sta ENABL         ; c44, BL original TIA ball
        ; Fixed-centre PF2 ring trial (arena x80/y112), NOT P0-following.
        ; PREPARE GRP0 for the NEXT visible scanline, x-1.
        ; Deliberately after PF writes; accumulator persists through
        ; DEX/BNE and WSYNC so next line writes GRP0 at CPU cycle ~3.
        txa
        sec
        sbc RenderBottom
        bcc NextSpriteBlank
        cmp SpriteHeight
        bcs NextSpriteBlank
        tay
        lda (GfxPtr),y
        jmp NextLine
NextSpriteBlank:
        lda #0
NextLine:
        dex
        bne Visible
        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        sta GRP1
        sta ENABL
        sta PF0
        sta PF1
        sta PF2
        sta WSYNC
        lda #34             ; ~29 raster lines of overscan incl update work
        sta TIM64T
        jsr UpdateOrb
        jsr UpdateAttack
        jsr CheckHaloHit
OverScanWait:
        lda INTIM
        bne OverScanWait
        sta WSYNC
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

; Strict K0 corner policy: X and Y projections from ORIGINAL position
; must both be clear before diagonal; then diagonal target must be clear.
; If only X clears, slide X; if only Y clears, slide Y.
; X preference on ambiguous corners is diagnostic, not final feel canon.
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
        lda Level
        sta TestLevel
        ; If horizontal input was also pressed, require Y-only projection
        ; from original centre to be legal before trying diagonal goal.
        lda JoyState
        and #$C0
        cmp #$C0
        beq YGoalCheck
        lda BaseX
        sta TryX
        jsr CandidateValid
        beq MoveYDone
YGoalCheck:
        lda PlayerX
        sta TryX
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
        ; P0 now has bit-exact pre-expanded ROM bitmap per level/pose;
        ; original source rows unchanged; no RowMapPtr lookup in scanline.
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
        lda Level
        sec
        sbc #1
        asl
        asl
        clc
        adc RectIndex
        tax
        lda PlayArtLo,x
        sta GfxPtr
        lda PlayArtHi,x
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

        ; PLAY1 code/data inserted below

; ---- PLAY1 frame-independent gameplay: OVERSCAN, not critical scanlines ----
UpdateOrb:
        lda OrbMask
        bne OrbCandidate
        lda OrbTimer
        beq OrbReappear
        dec OrbTimer
        rts
OrbReappear:
        lda #2
        sta OrbMask
        rts
OrbCandidate:
        lda Level
        cmp #3
        bcs OrbDone       ; on L3 orb remains if it was already present
        ; candidate test against actual BL center x96, y112,
        ; source-sized full body +2 pixel touch margin.
        lda PlayerX
        sec
        sbc #96
        bcs OrbAbsX
        eor #$FF
        clc
        adc #1
OrbAbsX:
        ldx Level
        cmp OrbTolX,x
        bcs OrbDone
        lda PlayerY
        sec
        sbc #112
        bcs OrbAbsY
        eor #$FF
        clc
        adc #1
OrbAbsY:
        cmp OrbTolY,x
        bcs OrbDone
        lda Level
        clc
        adc #1
        sta TestLevel
        lda PlayerX
        sta TryX
        lda PlayerY
        sta TryY
        jsr CandidateValid     ; real COL1 full-size collision K0
        beq OrbDone
        inc Level
        lda #0
        sta OrbMask
        lda #90
        sta OrbTimer           ; same fixed, reachable BL after 90f
OrbDone:
        rts

UpdateAttack:
        lda TargetFlash
        beq NoFlash
        dec TargetFlash
        bne NoFlash
        lda #0
        sta COLUBK
NoFlash:
        lda HaloFrames
        beq AttackInactive
        dec HaloFrames
        bne AttackColor
        ldx Level
        lda RecoverTable,x
        sta HaloRecover
AttackInactive:
        lda HaloRecover
        beq TryFire
        dec HaloRecover
        bne AttackColor
TryFire:
        lda INPT4          ; Fire active-low, bit7
        bmi AttackColor
        lda HaloFrames
        bne AttackColor
        lda #30
        sta HaloFrames
AttackColor:
        lda HaloFrames
        beq AttackOff
        lda #$2E
        sta COLUPF       ; TEST B: full arena PF + BL GOLD while active
        ldx Level
        lda HaloMaskTable,x
        sta HaloVisualMask
        jmp AttackRadius
AttackOff:
        lda #$86
        sta COLUPF       ; blue diagnostic world PF+orb when inactive
        lda #0
        sta HaloVisualMask
AttackRadius:
        ldx Level
        lda RadiusTable,x
        sta HaloRadius
        rts

CheckHaloHit:
        lda HaloFrames
        beq NoTargetHit
        lda TargetAlive
        beq NoTargetHit
        lda PlayerX
        sec
        sbc #125
        bcs HitAbsX
        eor #$FF
        clc
        adc #1
HitAbsX:
        cmp HaloRadius
        bcs NoTargetHit
        lda PlayerY
        sec
        sbc #96
        bcs HitAbsY
        eor #$FF
        clc
        adc #1
HitAbsY:
        cmp HaloRadius
        bcs NoTargetHit
        lda #0
        sta TargetAlive
        sta COLUP1
        lda #$42
        sta COLUBK             ; transient kill feedback
        lda #20
        sta TargetFlash
NoTargetHit:
        rts

PositionP1:
        sta WSYNC
        sec
P1PosLoop:
        sbc #15
        bcs P1PosLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP1
        sta RESP1
        rts

PositionBall:
        sta WSYNC
        sec
BallPosLoop:
        sbc #15
        bcs BallPosLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMBL
        sta RESBL
        rts

OrbTolX:
        dc.b 0,7,11,19
OrbTolY:
        dc.b 0,9,15,21
RadiusTable:
        dc.b 0,18,28,40
RecoverTable:
        dc.b 0,60,36,15
HaloMaskTable:
        dc.b 0,$03,$1F,$FF

; Source original R3 K1 exact eight bytes $18,$3C,$7E,$DB,$5A,$24,$66,$42,
; each displayed twice, in decreasing scanline X index order.
; Real TIA object line tables are relocated to aligned F-page ROM
; to guarantee no ABS,X page-crossing beyond 76c raster budget.

PlayL1P0:
        dc.b $06,$C4,$64,$3C,$3C,$3D,$FE,$7C,$66,$5A,$7E,$24
PlayL1P1:
        dc.b $60,$23,$26,$3C,$3C,$BE,$FE,$7C,$66,$5A,$7E,$24
PlayL1P2:
        dc.b $60,$23,$26,$3C,$3C,$BC,$7F,$3E,$66,$5A,$7E,$24
PlayL1P3:
        dc.b $06,$C4,$64,$3C,$3C,$7D,$7F,$3E,$66,$5A,$7E,$24
PlayL2P0:
        dc.b $06,$06,$C4,$C4,$64,$64,$3C,$3C,$3C,$3C,$3D,$3D
        dc.b $FE,$FE,$7C,$7C,$66,$66,$5A,$5A,$7E,$7E,$24,$24
PlayL2P1:
        dc.b $60,$60,$23,$23,$26,$26,$3C,$3C,$3C,$3C,$BE,$BE
        dc.b $FE,$FE,$7C,$7C,$66,$66,$5A,$5A,$7E,$7E,$24,$24
PlayL2P2:
        dc.b $60,$60,$23,$23,$26,$26,$3C,$3C,$3C,$3C,$BC,$BC
        dc.b $7F,$7F,$3E,$3E,$66,$66,$5A,$5A,$7E,$7E,$24,$24
PlayL2P3:
        dc.b $06,$06,$C4,$C4,$64,$64,$3C,$3C,$3C,$3C,$7D,$7D
        dc.b $7F,$7F,$3E,$3E,$66,$66,$5A,$5A,$7E,$7E,$24,$24
        ORG $F700    ; all four x36 L3 bitmaps fit one ROM page
PlayL3P0:
        dc.b $06,$06,$06,$C4,$C4,$C4,$64,$64,$64,$3C,$3C,$3C
        dc.b $3C,$3C,$3C,$3D,$3D,$3D,$FE,$FE,$FE,$7C,$7C,$7C
        dc.b $66,$66,$66,$5A,$5A,$5A,$7E,$7E,$7E,$24,$24,$24
PlayL3P1:
        dc.b $60,$60,$60,$23,$23,$23,$26,$26,$26,$3C,$3C,$3C
        dc.b $3C,$3C,$3C,$BE,$BE,$BE,$FE,$FE,$FE,$7C,$7C,$7C
        dc.b $66,$66,$66,$5A,$5A,$5A,$7E,$7E,$7E,$24,$24,$24
PlayL3P2:
        dc.b $60,$60,$60,$23,$23,$23,$26,$26,$26,$3C,$3C,$3C
        dc.b $3C,$3C,$3C,$BC,$BC,$BC,$7F,$7F,$7F,$3E,$3E,$3E
        dc.b $66,$66,$66,$5A,$5A,$5A,$7E,$7E,$7E,$24,$24,$24
PlayL3P3:
        dc.b $06,$06,$06,$C4,$C4,$C4,$64,$64,$64,$3C,$3C,$3C
        dc.b $3C,$3C,$3C,$7D,$7D,$7D,$7F,$7F,$7F,$3E,$3E,$3E
        dc.b $66,$66,$66,$5A,$5A,$5A,$7E,$7E,$7E,$24,$24,$24

PlayArtLo:
        dc.b <PlayL1P0,<PlayL1P1,<PlayL1P2,<PlayL1P3,<PlayL2P0,<PlayL2P1,<PlayL2P2,<PlayL2P3,<PlayL3P0,<PlayL3P1,<PlayL3P2,<PlayL3P3
PlayArtHi:
        dc.b >PlayL1P0,>PlayL1P1,>PlayL1P2,>PlayL1P3,>PlayL2P0,>PlayL2P1,>PlayL2P2,>PlayL2P3,>PlayL3P0,>PlayL3P1,>PlayL3P2,>PlayL3P3


        ; PLAY1 combined original asymmetric PF obstacle source (mirror enabled)
        ; Halo is a *first visible centered static contour experiment*,
        ; NOT full P0-following sprite or full-scene claim.
        ORG $F900
PlayPF0:
        ds 129,0
        ds 24,$80
        ds 40,0
        ORG $FA00
PlayPF1:
        ds 25,0
        ds 16,$3E
        ds 88,0
        ds 24,$E0
        ds 40,0
        ; At $FC00+X and $FD00+X all X=1..192 reads stay same page.
        ORG $FC00
DummyScan:
        ds 73,0
        dc.b $42,$42,$66,$66,$24,$24,$5A,$5A
        dc.b $DB,$DB,$7E,$7E,$3C,$3C,$18,$18
        ds 104,0          ; index192 read by first of 192 visible lines MUST be zero
        ORG $FD00
OrbScan:
        ds 63,0
        dc.b 2,2,2,2
        ds 126,0          ; index192 must be zero, never $FF ORG padding

        ; 128-byte zero left guard + 193-row halo + right guard:
        ; PlayerY signed pointer shifts never read unrelated PF/dummy/BL data.
        ORG $FE00
        ds 128,0
HaloPF2Rows:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF
        dc.b $FF,$FF,$80,$80,$80,$80,$80,$9F,$9F,$9F,$90,$90
        dc.b $90,$90,$90,$93,$93,$93,$92,$92,$92,$92,$92,$92
        dc.b $92,$92,$92,$92,$92,$92,$92,$92,$92,$92,$92,$92
        dc.b $92,$92,$92,$93,$93,$93,$90,$90,$90,$90,$90,$9F
        dc.b $9F,$9F,$80,$80,$80,$80,$80,$FF,$FF,$FF,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00


        ORG $FFFC
        dc.w Reset
        dc.w Reset
