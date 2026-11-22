; GAMEPLAY-4 dynamic exact source pose tables + M1 two-row physical arrow trial.
; Zero-regression only after DASM/Stella evidence, never claim independent 3 actors.
; GAMEPLAY-3 PHYSICAL K1-T neutral/warning + R1 neutral; exact 8x16 source masks.
; WARNING: no K1 strike/R1 draw/release runtime table yet; those need diagnostic passes.
; GAMEPLAY-2 F8 bank1 - unchanged U1-LEG1 / PLAY1-H renderer, single-visit orb fix.
; GAMEPLAY-1 bank 1; exact original PLAY1-H bitmaps + bounded noncritical modifications.
; F8 8KiB prototype: PLAY1-H visible kernel retained; no new PF2 write.
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
ENAM1       = $1E
RESM1       = $13
HMM1        = $23
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
REFP1       = $0C       ; TIA native per-bit horizontal mirroring
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
ArrowRowPtr = $89   ; low/high dynamic physically visible M1 row pointer; old RowMapPtr unused
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
ArrowCool   = $9D       ; 0..180 actual release cooldown, unused GAMEPLAY-3 OrbTimer state
HaloFrames  = $9E       ; 30 NTSC frames when FIRE pressed
HaloRecover = $9F       ; 60/36/15 f cooldown AFTER halo ends
HaloRadius  = $A0       ; logical 360-degree square/Chebyshev radius
TargetAlive = $A1       ; one frozen original R3 knight P1 dummy
TargetFlash = $A2       ; death feedback countdown
ArrowDX     = $A3  ; -1/+1 when flying, 0 inactive
ArrowDY     = $A4  ; -1/0/+1 fixed at release
KnightDir   = $A5  ; attack facing locked at warning initiation, old unused HaloVisualMask   ; previous level-dependent contour bits
HaloRowPtr = $A6  ; dynamic level-baked ROM pointer
OrbRowPtr = $A8   ; BL shown/hidden pointer
; GAMEPLAY-1 F8 extension. Physical screen still PLAY1-H PARTIAL.
Stage       = $AA
StageDir    = $AB
Lives       = $AC
ScoreLo     = $AD
ScoreHi     = $AE
KnightX     = $AF
SwordWarn   = $B0
SwordStrike = $B1
SwordRest   = $B2
Invulnerable= $B3
StageKills  = $B4
KillsNeed   = $B5
EnemyRowPtr = $B6    ; low/high actual F8 ROM P1 scan table page
SoundFrames = $BF
ArrowX      = $B8  ; retired unused Ranger bookkeeping in sequential diagnostic
ArrowY      = $B9
OrbX        = $BA
OrbDirty    = $BB

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
        jsr SelectEnemyArt ; offscreen identity/pose, never after GRP1 beam deadline
        lda HaloFrames
        beq HaloPointerOff
        ldx Level
        lda PlayerY
        clc
        adc HaloBaseLo,x
        sta HaloRowPtr
        lda HaloBaseHi,x
        adc #0
        sta HaloRowPtr+1
        jmp HaloPointerReady
HaloPointerOff:
        lda #$01
        sta HaloRowPtr
        lda #$FF
        sta HaloRowPtr+1
HaloPointerReady:
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
        lda #0
        sta HMP1          ; stale previous-frame motion must not move P1
        sta HMBL          ; nor move BL on P0's HMOVE
        lda RenderX
        jsr PositionP0
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMP0          ; essential: second HMOVE must not move P0 again
        lda KnightX       ; one sequential P1 diagnostic actor, canon 3 independent OPEN
        jsr PositionP1
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMP1          ; clear after P1's own motion
        ; M1 independent TIA missile from P1, genuine per-frame X updates.
        ; Only move/position active missile; no BL or P0 object ownership stolen.
        lda ArrowDX
        beq NoMissilePosition
        lda ArrowX
        jsr PositionMissile1
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMM1
NoMissilePosition:
        ; Point M1's two enabled raster bytes at a *fixed screen Y*.
        ; Off pointer always full 193 zero bytes in preserved FF guard.
        lda ArrowDX
        beq MissileRowOff
        lda ArrowY
        cmp #48
        bcc MissileRowOff
        cmp #176
        bcs MissileRowOff
        clc
        adc #$90             ; $F890 + ArrowY (seed at $F940)
        sta ArrowRowPtr
        lda #$F8
        adc #0
        sta ArrowRowPtr+1
        jmp MissileRowReady
MissileRowOff:
        lda #$01
        sta ArrowRowPtr
        lda #$FF
        sta ArrowRowPtr+1
MissileRowReady:
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
        ; original static synthetic PF masks, PF0 is PF1 & $80.
        ; PF1 first and PF0 second saves 2c/row without altering bits.
        lda PlayPF1,x
        sta PF1
        and #$80
        sta PF0
        txa
        tay
        lda (HaloRowPtr),y
        sta PF2           ; c27, before left PF2 beam deadline
        ; P1 x125 and BL x96 are beyond these register write deadlines.
        lda (OrbRowPtr),y
        sta ENABL         ; original BL orb (independent, never used by arrow)
        lda (ArrowRowPtr),y
        sta ENAM1         ; real M1 vertical-gated arrow, two native scanlines
        ldy EnemyIndexScan,x
        lda (EnemyRowPtr),y
        sta GRP1          ; exact runtime 8x16 pose, 16B+zero mask via scan remap
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
        sta ENAM1
        sta PF0
        sta PF1
        sta PF2
        sta WSYNC
        lda #34             ; ~29 raster lines of overscan incl update work
        sta TIM64T
        jsr UpdateOrb
        jsr UpdateAttack
        jsr CheckHaloHit
        jsr GameBankEnter ; F8 gameplay tick in overscan ONLY
        lda OrbDirty
        beq OrbXPlaced
        lda OrbX
        jsr PositionBall
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMBL
        sta OrbDirty
OrbXPlaced:
        lda OrbMask
        beq SelectOrbZero
        lda #0
        sta OrbRowPtr
        lda #$FD
        sta OrbRowPtr+1
        jmp OrbSelected
SelectOrbZero:
        lda #$01
        sta OrbRowPtr
        lda #$FF
        sta OrbRowPtr+1
OrbSelected:
OverScanWait:
        lda INTIM
        bne OverScanWait
        sta WSYNC
        sta WSYNC          ; GAMEPLAY-2 measured frame 261 -> add one OVERSCAN line, target 262
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
        lda RectRAMLo,x  ; gameplay bank loads 16B collision rectangles for active layout
        sta RectPtr
        lda #0
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

; Old MapSmall/MapMedium/MapLarge row indirection was UNUSED since PLAY1-H,\n; real U1-LEG1 P0 is rendered from frozen PlayL1/L2/L3P0..P3 below.\n\n; Visible synthetic obstacles: top x=[12,28) reflected to [132,148)
; at arena y=[24,48); lower x=[24,44) reflected to [116,136)
; at arena y=[136,152). 4 solids, not final world map.
; This physical scanline map is indexed by X=192..1 in VisibleLoop.
        ORG $F398
; Visible sprite source in compact indexed ROM tables. Pixel-exact 16 rows.
; This replaces obsolete 193B standalone K1-warning profile (space for code).
SelectEnemyArtImpl:
        lda StageKills
        clc
        adc #1
        cmp KillsNeed
        bne SelectKnightPose
        ldx #3
        lda SwordWarn
        beq RangerNoDraw
        ldx #4
        jmp PoseChosen
RangerNoDraw:
        lda SwordStrike
        beq PoseChosen
        ldx #5
        jmp PoseChosen
SelectKnightPose:
        ldx #0
        lda SwordWarn
        beq KnightNoWarning
        ldx #1
        jmp PoseChosen
KnightNoWarning:
        lda SwordStrike
        beq PoseChosen
        ldx #2
PoseChosen:
        lda EnemyArtLo,x
        sta EnemyRowPtr
        lda EnemyArtHi,x
        sta EnemyRowPtr+1
        ; Knight visual facing locks during warning/strike,
        ; free chase and Ranger face toward player at other times.
        cpx #3
        bcs NormalEnemyFace
        lda SwordWarn
        ora SwordStrike
        beq NormalEnemyFace
        lda KnightDir
        sta REFP1
        rts
NormalEnemyFace:
        lda KnightX
        cmp PlayerX
        bcc FacingRight
        lda #8
        sta REFP1
        rts
FacingRight:
        lda #0
        sta REFP1
        rts
PositionMissile1:
        sta WSYNC
        sec
MissilePosLoop:
        sbc #15
        bcs MissilePosLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMM1
        sta RESM1
        rts

        ORG $F459
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
; Obsolete unused MapLow/MapHigh removed, no dynamic RowMapPtr reader.\nArtLo:
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
        beq OrbDone         ; exactly one orb per stage visit, never respawn after pickup
OrbCandidate:
        lda Level
        cmp #3
        bcs OrbDone       ; on L3 orb remains if it was already present
        ; candidate test against actual BL center x96, y112,
        ; source-sized full body +2 pixel touch margin.
        lda PlayerX
        sec
        sbc OrbX
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
        lda #0
        ; consumed orb stays absent for whole stage visit; old OrbTimer retired
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
        ; former HaloVisualMask scratch is now KnightDir; no visual read of this var
        jmp AttackRadius
AttackOff:
        lda #$86
        sta COLUPF       ; blue diagnostic world PF+orb when inactive
        lda #0
        ; retired unread HaloVisualMask storage, now used by KnightDir
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
        sbc KnightX
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
HaloBaseLo: dc.b 0,$B0,$C0,$D0
HaloBaseHi: dc.b 0,$F7,$FA,$FD

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
; Three runtime collision tables live at RIOT $C0/$D0/$E0.
; They are written only by offscreen bank0 game code on stage transitions.
RectRAMLo:
        dc.b 0,$C0,$D0,$E0
        ORG $F680
GameBankEnter:
        lda $FFF8         ; F8: switch to bank 0 on read
        jmp $F100         ; fetched from bank 0 after hotspot
        ORG $F690
GameBankReturn:
        lda $FFF9         ; F8: switch back to original graphics bank
        rts               ; fetched from bank 1 after hotspot
        ORG $F6A0
GameBankReset:
        lda $FFF9
        jmp $F000
        ORG $F6A8
SelectEnemyArt:
        jmp SelectEnemyArtImpl
        ; 12B pointer table in F6AB..F6B6, physically outside F7A8 halo guard
EnemyArtLo:
        dc.b <K1NeutralBytes,<K1WarningBytes,<K1StrikeBytes,<R1NeutralBytes,<R1DrawBytes,<R1ReleaseBytes
EnemyArtHi:
        dc.b >K1NeutralBytes,>K1WarningBytes,>K1StrikeBytes,>R1NeutralBytes,>R1DrawBytes,>R1ReleaseBytes
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
        ; L1 source-baked visible profile, with real signed Y shift
        ORG $F7A8
        ds 120,0
        ORG $F820
HaloL1Rows:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$03
        dc.b $03,$03,$00,$00,$00,$00,$00,$03,$03,$03,$00,$00
        dc.b $00,$00,$00,$03,$03,$03,$02,$02,$02,$02,$02,$02
        dc.b $02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02,$02
        dc.b $02,$02,$02,$03,$03,$03,$00,$00,$00,$00,$00,$03
        dc.b $03,$03,$00,$00,$00,$00,$00,$03,$03,$03,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00
        ds 31,0
        ORG $F900
ArrowSeedScan:
        ds 64,0
ArrowSeedCore:
        dc.b $02,$02         ; 2 physical M1 scanlines; real TIA ENAM1 bit1
        ds 127,0
        ds 63,0              ; F9C1..F9FF guard; never touched by arrow source
        ORG $FA00
PlayPF1:
        ds 25,0
        ds 16,$3E
        ds 88,0
        ds 24,$E0
        ds 40,0
        ; GAMEPLAY-4: 6 exact source masks x17B =102B in unused PF1 pad; PLAYPF1 only x<=192
K1NeutralBytes:
        dc.b $88,$D8,$A8,$A8,$70,$70,$78,$D8,$F8,$F8,$70,$D8,$D8,$88,$F8,$78,0  ; 17th zero = out-of-16-row lookup
K1WarningBytes:
        dc.b $88,$D8,$A8,$A8,$70,$70,$78,$D8,$FE,$FA,$72,$DA,$DA,$8A,$FA,$7A,0  ; 17th zero = out-of-16-row lookup
K1StrikeBytes:
        dc.b $88,$D8,$A8,$A8,$70,$70,$7F,$DF,$FC,$F8,$70,$D8,$D8,$88,$F8,$78,0  ; 17th zero = out-of-16-row lookup
R1NeutralBytes:
        dc.b $CC,$48,$50,$32,$31,$75,$7D,$71,$72,$70,$70,$30,$70,$50,$78,$38,0  ; 17th zero = out-of-16-row lookup
R1DrawBytes:
        dc.b $CC,$48,$48,$28,$32,$75,$79,$7F,$79,$75,$71,$32,$70,$50,$78,$38,0  ; 17th zero = out-of-16-row lookup
R1ReleaseBytes:
        dc.b $CC,$48,$48,$28,$32,$71,$71,$7F,$71,$71,$71,$32,$70,$50,$78,$38,0  ; 17th zero = out-of-16-row lookup
        ds 9,0  ; 111B original padding preserved in size
        ORG $FB30
HaloL2Rows:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$1F
        dc.b $1F,$1F,$00,$00,$00,$00,$00,$1F,$1F,$1F,$10,$10
        dc.b $10,$10,$10,$13,$13,$13,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$13,$13,$13,$10,$10,$10,$10,$10,$1F
        dc.b $1F,$1F,$00,$00,$00,$00,$00,$1F,$1F,$1F,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00
        ds 15,0
        ; At $FC00+X and $FD00+X all X=1..192 reads stay same page.
        ORG $FC00
EnemyIndexScan:          ; direct source byte index for 16 real native 8x16 rows
        ds 73,16          ; every non-sprite row points to 17th zero byte
        dc.b 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
        ds 104,16         ; source screenshot pixels remain bottom-first as frozen
        ORG $FD00
OrbScan:
        ds 63,0
        dc.b 2,2,2,2
        ds 126,0          ; index192 must be zero
        ds 63,0           ; guarantee FDC1..FDFF zeros for OFF pointer

        ; level3 Y-motion template with full two-sided guards in ROM
        ; Original last BL table extends to FDFF. FE00..FE3F is
        ; zero guard. L3 table starts FE40; FF01..FFFB is a
        ; permanent 251-byte zero profile for OFF halo and OFF BL.
        ORG $FE00
        ds 64,0
        ORG $FE40
HaloL3Rows:
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
        ds 251,0
        ORG $FFFC
        dc.w Reset
        dc.w Reset
