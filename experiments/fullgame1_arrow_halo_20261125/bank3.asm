; GAMEPLAY-5 A+C exact frozen source mask / visible kernel, unchanged for causal NTSC diff.
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
ENAM0       = $1D
ENAM1       = $1E
RESM0       = $12
RESM1       = $13
HMM0        = $22
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
VDELP1      = $26
RESMP0      = $28
HMOVE       = $2A
INPT4       = $3C
SWCHA       = $0280
SWCHB       = $0282
INTIM       = $0284
TIMINT      = $0285
TIM64T      = $0296

PlayerX     = $80   ; CENTRE x in TIA colour clocks, 0..159
PlayerY     = $81   ; CENTRE y in 176-line arena, 0 at top
Level       = $82   ; 1,2,3
JoyState    = $83
ScoreTop    = $84
HudLifePtr  = $95
Phase       = $86       ; gait bits 0..1, held FIRE bit 6, RESET bit 7
DiagonalSkip= $87
SpriteHeight= $88
ArrowRowPtr = $89
WorldPFPtr = $EC   ; low/high dynamic physically visible M1 row pointer; old RowMapPtr unused
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
BaseX       = $9B       ; original X for strict diagonal Y-projection
OrbMask     = $9C       ; 2 = BL visible, 0 = consumed temporarily
ArrowCool   = $9D       ; 0..180 actual release cooldown, unused GAMEPLAY-3 OrbTimer state
HaloFrames  = $9E       ; 12 NTSC frames when FIRE pressed
HaloRecover = $9F       ; 84/60/36 f cooldown AFTER halo ends
HaloRadius  = $A0       ; logical 360-degree octagon radius
ArrowMajor= $A1     ; bit 7 selects Y as the major axis
ArrowMinor= $A2     ; magnitude of the minor axis
ArrowDX     = $A3  ; -1/+1 when flying, 0 inactive
ArrowDY     = $A4  ; -1/0/+1 fixed at release
KnightDir   = $A5  ; attack facing locked at warning initiation, old unused HaloVisualMask   ; previous level-dependent contour bits
HaloRowPtr = $A6  ; M0 side-arc FF guarded 2-scanline ROM pointer
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
ArrowError= $B2     ; projectile error accumulator
Invulnerable= $B3
StageKills  = $B4
KillsNeed   = $B5
EnemyBottom = $E8
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
        sta VDELP1       ; GRP0 at next WSYNC transfers previous GRP1 to delayed latch
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
        lda #$10
        sta NUSIZ1      ; 2-pixel physical M1, while P1 stays 1x
        lda #2
        sta OrbMask
        lda #1
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
        inc FrameCount
        inc Phase
        lda Phase
        and #$03
        cmp #3
        bne PhaseGood
        lda Phase
        and #$C0          ; preserve physical RESET and FIRE latches
        sta Phase
PhaseGood:
        lda Lives
        beq MotionSkipDead
        jsr DetectDiagonal
        lda PlayerX
        sta BaseX
        lda #0
        sta MotionDid
        jsr MoveX
        jsr MoveY
MotionSkipDead:
        jsr UpdateScale
        jsr UpdateGait
        jsr SelectEnemyArt ; offscreen identity/pose, never after GRP1 beam deadline
        jsr HudBankEnter    ; prepare current score and lives after motion
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
        ; Each object RESP and fine-HM register is set on its own WSYNC.
        ; One shared HMOVE after all three positions preserves the same
        ; physical X, while recovering 1-2 precious VBLANK scanlines.
        lda #0
        sta HMP0
        sta HMP1
        sta HMM1
        sta HMBL
        lda RenderX
        jsr PositionP0
        lda KnightX
        jsr PositionP1
        lda ArrowDX
        beq NoMissilePosition
        lda ArrowX
        jsr PositionMissile1
NoMissilePosition:
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMP0
        sta HMM1
        sta HMBL
        ; Let P1 motion clocks finish before clearing its fine motion latch.
        ldx #3
P1MotionWait:
        dex
        bne P1MotionWait
        sta HMP1
        jsr RestoreOrbIfVisible
        jsr NewHaloSetup
        jsr SetBallWidth
        ; Point M1's two enabled raster bytes at a *fixed screen Y*.
        ; Off pointer always full 193 zero bytes in preserved FF guard.
        lda ArrowDX
        beq MissileRowOff
        ; Only active arrows reach here; overscan logic validates bounds.
        ; Low seed pointer = $F92A + ceil(ArrowY / 8).
        ; Metatile Y = floor((176-ArrowY) / 8), so seed $F940
        ; enables one real 8-line missile band without per-line cost.
        ; 2-scanline render index independently of 8-line PF metatiles.
        ; Ypair = 88-ceil(ArrowY/2), so pointer = F8E8+ceil(Y/2).
        lda ArrowY
        clc
        adc #1
        lsr
        clc
        adc #$E8
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
        lda $96
        sta DiagonalSkip    ; movement is complete until next frame
        jsr PrepareHudLife
BlankWait:
        bit TIMINT
        bmi BlankWaitDone
        lda INTIM
        bne BlankWait
BlankWaitDone:
        sta WSYNC
        lda #0
        sta VBLANK
        lda #0
        sta PF2
        jmp GateDispatch ; gameover has dedicated no-sprite kernel
; Paired raster kernel: PF1 and BL change once per pair, M1 and M0
; on the second physical row. P0 stays full one-line, P1 uses VDEL
; and its native doubled bitmap rows. Color changes only on two blank rows.
Visible:
        sta WSYNC
        sta GRP0
        ldy WorldPFIndex,x
        bmi PairColorLine
        lda (WorldPFPtr),y
        sta PF1
        lda (OrbRowPtr),y
        sta ENABL
        jmp PairNextP0
PairColorLine:
        cpy #$A7
        bne PairColorRestore
        lda $96
        bne PairColorWrite
PairColorRestore:
        lda $8F
PairColorWrite:
        sta COLUPF
        lda #0
        sta PF1
        sta ENABL
PairNextP0:
        txa
        sec
        sbc RenderBottom
        cmp SpriteHeight
        bcs PairFirstBlank
        tay
        lda (GfxPtr),y
        dex
        jmp PairSecond
PairFirstBlank:
        lda #0
        dex
PairSecond:
        sta WSYNC
        sta GRP0
        ldy WorldPFIndex,x
        lda (ArrowRowPtr),y
        sta ENAM1
        lda (HaloRowPtr),y
        sta ENAM0
        txa
        sec
        sbc EnemyBottom
        cmp #16
        bcs PairEnemyBlank
        tay
        lda (EnemyRowPtr),y
        jmp PairEnemyWrite
PairEnemyBlank:
        lda #0
PairEnemyWrite:
        sta GRP1
        txa
        sec
        sbc RenderBottom
        cmp SpriteHeight
        bcs PairSecondBlank
        tay
        lda (GfxPtr),y
        dex
        bne Visible
        jmp VisibleDone
PairSecondBlank:
        lda #0
        dex
        bne Visible
VisibleDone:
        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        sta GRP1
        sta GRP0          ; flush P1 delayed latch before HUD / next frame
        sta ENABL
        sta ENAM1
        sta ENAM0
        sta PF0
        sta PF1
        sta PF2
        sta WSYNC
        lda #33             ; GAMEPLAY-5 A 5/5 real Ranger 262: timer33 + original 2 WSYNC
        sta TIM64T
        jsr UpdateOrb
        jsr UpdateAttack
        jsr GameBankEnter ; F8 gameplay tick in overscan ONLY
OrbXPlaced:
        lda OrbMask
        beq SelectOrbZero
        lda FrameCount
        clc
        adc #1
        and #2
        bne SelectOrbZero
        lda #$0D    ; FD0D + pairs 57..60 selects the eight orb scanlines
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
        bit TIMINT
        bmi OverScanWaitDone
        lda INTIM
        bne OverScanWait
OverScanWaitDone:
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
        and #$03
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

SetBallWidth:
        ; BL belongs only to the orb. Its width and world reflection
        ; never depend on the player level or halo phase.
        lda Stage
        and #1
        ora #$10
        sta CTRLPF
        ldx Stage
        lda RasterWorldColors,x
        sta $8F
        ldx HaloFrames
        beq OrbColorReady
        lda #$2E
OrbColorReady:
        sta $96
        rts
RasterWorldColors:
        dc.b $00,$C6,$C8,$86,$88,$66,$68,$82,$84
; Life digit font (PF0 D4 first). Three pixels x five raster rows.
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
        lda WidthHalf,x
        sta RectPtr
        lda HeightHalf,x
        sta RectPtr+1
        ldx #0
RectLoop:
        ; Center bounding box intersects raw rectangle if the two axes
        ; overlap. The raw four rectangles live at C0..CF for all levels.
        lda TryX
        clc
        adc RectPtr
        cmp $C0,x
        bcc NextRect
        lda TryX
        sec
        sbc RectPtr
        cmp $C1,x
        bcs NextRect
        lda TryY
        clc
        adc RectPtr+1
        cmp $C2,x
        bcc NextRect
        lda TryY
        sec
        sbc RectPtr+1
        cmp $C3,x
        bcc Invalid
NextRect:
        txa
        clc
        adc #4
        tax
        cpx #16
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
        ORG $F36D
EdgeMask2:
        dc.b $33,$12,$14,$0C,$0C,$1D,$1F,$1C,$1C,$1C,$1C,$0C,$1C,$14,$1E,$0E
EdgeMask4:
        dc.b $0C,$04,$05,$03,$03,$07,$07,$07,$07,$07,$07,$03,$07,$05,$07,$03
EdgeMask6:
        dc.b $03,$01,$01,$00,$00,$01,$01,$01,$01,$01,$01,$00,$01,$01,$01,$00
        ORG $F3A0
; Visible sprite source in compact indexed ROM tables. Pixel-exact 16 rows.
; This replaces obsolete 193B standalone K1-warning profile (space for code).
SelectEnemyArtImpl:
        lda $E4             ; real 3-actor selected visual slot
        cmp #2
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
        bcs RangerFace
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
FacingLeft:
        lda #8
        sta REFP1
        rts
FacingRight:
        lda #0
        sta REFP1
        rts
RangerFace:
        cpx #4
        beq NormalEnemyFace ; bow draw faces its target
        bcc RangerFleeFace
        lda ArrowDX         ; after release keep the projectile's fixed facing
        beq NormalEnemyFace
        bmi FacingLeft
        bpl FacingRight
RangerFleeFace:
        lda KnightDir
        sta REFP1
        jmp EdgeArt
; Additional F6 bank3 visible loop: M1 takes place of PF2 halo for these frames.
; Pre-frame arrow/halo disjointness guaranteed by bank2 tick.
VisibleGate:
        jsr HudDraw
        lda DiagonalSkip    ; room/orb color overlaps HUD pointer for seven rows
        sta $96
        lda $8F             ; restore world color before the first arena row
        sta COLUPF
        ldx Stage
        lda ArenaBackground,x
        sta COLUBK
        ldx #184          ; seven HUD rows use two blank top-margin lines
        lda #0
        jmp Visible
HudLifeDigits:
        dc.b $70,$50,$50,$50,$70
        dc.b $20,$30,$20,$20,$70
        dc.b $70,$40,$70,$10,$70
        dc.b $70,$40,$70,$40,$70
        dc.b $50,$50,$70,$40,$40
        dc.b $70,$10,$70,$40,$70
        dc.b $70,$10,$70,$50,$70
        dc.b $70,$40,$40,$40,$40
        dc.b $70,$50,$70,$50,$70
        dc.b $70,$50,$70,$40,$70

        ORG $F459
PF0Choices:
        dc.b 0,$80,0
PF1Choices:
        dc.b 0,$E0,$3E
MinCX:  dc.b 0,8,12,20
MaxCX:  dc.b 0,153,149,141
MinCY:  dc.b 0,10,14,19
MaxCY:  dc.b 0,167,163,158
WidthHalf:
        dc.b 0,4,8,16
HeightHalf:
        dc.b 0,6,10,15
SpriteHeights:
        dc.b 0,12,20,30
PlayerSizes:
        dc.b 0,$10,$25,$37 ; M0 gold halo side thickness L1=2px, L2=4px, L3=8px
RestoreOrbIfVisible:
        lda OrbDirty
        beq OrbRestoreDone
        lda OrbRowPtr+1
        cmp #$FD
        bne OrbRestoreDone
        lda INTIM
        cmp #8
        bcc OrbRestoreSkip
        lda OrbX
        clc
        adc #3               ; convert gameplay center to this RESPBL loop's input
        jsr PositionBall
        sta WSYNC
        sta HMOVE
        ; Allow the TIA motion clocks to finish before clearing HMBL.
        ldx #6
OrbMotionWait:
        dex
        bne OrbMotionWait
        lda #0
        sta HMBL
        sta OrbDirty
OrbRestoreDone:
        rts
OrbRestoreSkip:
        lda #1
        sta OrbRowPtr
        lda #$FF
        sta OrbRowPtr+1
        rts
; ---- PLAY1 frame-independent gameplay: OVERSCAN, not critical scanlines ----
UpdateOrb:
        lda OrbMask
        beq OrbDone         ; exactly one orb per stage visit, never respawn after pickup
OrbCandidate:
        lda Level
        cmp #3
        bcs OrbDone       ; on L3 orb remains if it was already present
        ; candidate test against actual BL center OrbX, y68,
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
        sbc #68
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
        lda #$50          ; chime only after actual successful growth
        sta SoundFrames
        lda #0
        sta OrbMask
        ; consumed orb stays absent for whole stage visit; old OrbTimer retired
OrbDone:
        rts

GateDispatch:
        lda Lives
        bne GateAlive
        lda #0
        sta $0D
        sta COLUBK
        sta CTRLPF
        sta GRP0
        sta GRP1
        sta ENAM0
        sta ENAM1
        sta ENABL
        lda #$0E
        sta COLUPF
        jsr HudDraw
        ldx #185
DeadScreenLine:
        sta WSYNC
        dex
        bne DeadScreenLine
        jmp VisibleDone
GateAlive:
        jmp VisibleGate

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
        dc.b 0,10,17,23
RecoverTable:
        dc.b 0,70,46,29
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
PrepareHudLife:
        lda #0
        sta COLUBK         ; the HUD is black even in the dark blue arenas
        lda #$21          ; duplicate after rows 0 and 5 of seven physical rows
        sta JoyState       ; movement input is dead until the next frame
        ldy Lives
        bne HudLivePointer
        lda #1
        sta HudLifePtr
        lda #$FF
        sta HudLifePtr+1
        bne HudIndices
HudLivePointer:
        lda HudLifeOffsets,y
        clc
        adc #<HudLifeDigits
        sec
        sbc ScoreTop
        sta HudLifePtr
        lda #>HudLifeDigits
        sbc #0
        sta HudLifePtr+1
HudIndices:
        ldy ScoreTop
        ldx #0
        rts
HudLifeOffsets:
        dc.b 0,5,10,15,20,25,30,35,40,45
ArenaBackground:
        dc.b 0,0,0,2,2,0,0,0,0

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


        ORG $F600     ; GAMEPLAY-5 A: page-align L2 24-row bank1 P0 table.
                      ; A5 causal trial: old $F5FE crosses page for 22/24 rows.
PlayL2P0:
        dc.b $06,$06,$C4,$64,$64,$3C,$3C,$3C,$3D,$3D,$FE,$FE
        dc.b $7C,$66,$66,$5A,$5A,$7E,$24,$24
PlayL2P1:
        dc.b $60,$60,$23,$26,$26,$3C,$3C,$3C,$BE,$BE,$FE,$FE
        dc.b $7C,$66,$66,$5A,$5A,$7E,$24,$24
PlayL2P2:
        dc.b $60,$60,$23,$26,$26,$3C,$3C,$3C,$BC,$BC,$7F,$7F
        dc.b $3E,$66,$66,$5A,$5A,$7E,$24,$24
PlayL2P3:
        dc.b $06,$06,$C4,$64,$64,$3C,$3C,$3C,$7D,$7D,$7F,$7F
        dc.b $3E,$66,$66,$5A,$5A,$7E,$24,$24
; Three runtime collision tables live at RIOT $C0/$D0/$E0.
; They are written only by offscreen bank0 game code on stage transitions.
RectRAMLo:
        dc.b 0,$C0,$D0,$E0
        ORG $F654
EdgeBottomMask:
        dc.b $CC,$48,$50,$32,$31,$75,$7D,$71,$72,$70,$70,$30,$70,$50,$78,$38
        ds 16,0
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
        ORG $F6B8
HudBankEnter:
        lda $FFF7
        ORG $F6C3
HudBankReturn:
        rts
        ORG $F6C4
EdgeArt:
        lda $E3
        cmp #$10
        bcc EdgeArtDone
        and #$F0
        cmp #$40
        beq EdgeArtBottom
        cmp #$30
        beq EdgeArtDone
        ; Outward facing for left, right; inward entry uses same physical
        ; clipped pixels until clear of the edge (avoids opposite-side wrap).
        ldx #0
        cmp #$20
        beq EdgeArtFacing
        ldx #8
EdgeArtFacing:
        stx REFP1
        lda $E1
        beq EdgeArtDone
        asl
        asl
        asl
        clc
        adc #<EdgeMask2-16
        sta EnemyRowPtr
        lda #>EdgeMask2
        sta EnemyRowPtr+1
        rts
EdgeArtBottom:
        lda $E1
        clc
        adc #<EdgeBottomMask
        sta EnemyRowPtr
        lda #>EdgeBottomMask
        sta EnemyRowPtr+1
EdgeArtDone:
        rts
        ORG $F700    ; all four x36 L3 bitmaps fit one ROM page
PlayL3P0:
        dc.b $06,$06,$C4,$C4,$C4,$64,$64,$3C,$3C,$3C,$3C,$3C
        dc.b $3D,$3D,$3D,$FE,$FE,$7C,$7C,$7C,$66,$66,$5A,$5A
        dc.b $5A,$7E,$7E,$24,$24,$24
PlayL3P1:
        dc.b $60,$60,$23,$23,$23,$26,$26,$3C,$3C,$3C,$3C,$3C
        dc.b $BE,$BE,$BE,$FE,$FE,$7C,$7C,$7C,$66,$66,$5A,$5A
        dc.b $5A,$7E,$7E,$24,$24,$24
PlayL3P2:
        dc.b $60,$60,$23,$23,$23,$26,$26,$3C,$3C,$3C,$3C,$3C
        dc.b $BC,$BC,$BC,$7F,$7F,$3E,$3E,$3E,$66,$66,$5A,$5A
        dc.b $5A,$7E,$7E,$24,$24,$24
PlayL3P3:
        dc.b $06,$06,$C4,$C4,$C4,$64,$64,$3C,$3C,$3C,$3C,$3C
        dc.b $7D,$7D,$7D,$7F,$7F,$3E,$3E,$3E,$66,$66,$5A,$5A
        dc.b $5A,$7E,$7E,$24,$24,$24

PlayArtLo:
        dc.b <PlayL1P0,<PlayL1P1,<PlayL1P2,<PlayL1P3,<PlayL2P0,<PlayL2P1,<PlayL2P2,<PlayL2P3,<PlayL3P0,<PlayL3P1,<PlayL3P2,<PlayL3P3
PlayArtHi:
        dc.b >PlayL1P0,>PlayL1P1,>PlayL1P2,>PlayL1P3,>PlayL2P0,>PlayL2P1,>PlayL2P2,>PlayL2P3,>PlayL3P0,>PlayL3P1,>PlayL3P2,>PlayL3P3


        ; PLAY1 combined original asymmetric PF obstacle source (mirror enabled)
        ; Halo is a *first visible centered static contour experiment*,
        ; NOT full P0-following sprite or full-scene claim.
        ; L1 source-baked visible profile, with real signed Y shift
        ORG $F7A8
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
        ORG $F820
WorldPFIndex:
        ds 2,0
        ds 2,1
        ds 2,2
        ds 2,3
        ds 2,4
        ds 2,5
        ds 2,6
        ds 2,7
        ds 2,8
        ds 2,9
        ds 2,10
        ds 2,11
        ds 2,12
        ds 2,13
        ds 2,14
        ds 2,15
        ds 2,16
        ds 2,17
        ds 2,18
        ds 2,19
        ds 2,20
        ds 2,21
        ds 2,22
        ds 2,23
        ds 2,24
        ds 2,25
        ds 2,26
        ds 2,27
        ds 2,28
        ds 2,29
        ds 2,30
        ds 2,31
        ds 2,32
        ds 2,33
        ds 2,34
        ds 2,35
        ds 2,36
        ds 2,37
        ds 2,38
        ds 2,39
        ds 2,40
        ds 2,41
        ds 2,42
        ds 2,43
        ds 2,44
        ds 2,45
        ds 2,46
        ds 2,47
        ds 2,48
        ds 2,49
        ds 2,50
        ds 2,51
        ds 2,52
        ds 2,53
        ds 2,54
        ds 2,55
        dc.b $A2,56
        ds 2,57
        ds 2,58
        ds 2,59
        ds 2,60
        dc.b $A7,61
        ds 2,62
        ds 2,63
        ds 2,64
        ds 2,65
        ds 2,66
        ds 2,67
        ds 2,68
        ds 2,69
        ds 2,70
        ds 2,71
        ds 2,72
        ds 2,73
        ds 2,74
        ds 2,75
        ds 2,76
        ds 2,77
        ds 2,78
        ds 2,79
        ds 2,80
        ds 2,81
        ds 2,82
        ds 2,83
        ds 2,84
        ds 2,85
        ds 2,86
        ds 2,87
        ds 2,88
        ds 2,89
        ds 2,90
        ds 2,91
        ds 2,92
        ds 2,93
        ds 2,94
        ds 2,95
        ds 1,95
OctagonOutside:
        sta $E9
        tya
        cmp $E9
        bcc OctagonXMax
        sta $EA
        lda $E9
        lsr
        clc
        adc $EA
        cmp HaloRadius
        rts
OctagonXMax:
        lsr
        clc
        adc $E9
        cmp HaloRadius
        rts
        ORG $F900
ArrowSeedScan:
        ds 64,0
ArrowSeedCore:
        dc.b $02,$00         ; original banded M1 display, physically partial
        ds 94,0           ; F942..F99F required M1 arrow ROM guard
        ORG $F9A0
PositionMissile0:
        sta WSYNC
        sec
M0PositionLoop:
        sbc #15
        bcs M0PositionLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMM0
        sta RESM0
        rts
        ORG $F9B2
UpdateAttack:
        ; Update the physical latch even when no attack is allowed.
        ldy #0
        lda INPT4
        bpl FirePressed
        lda Phase
        and #$BF
        sta Phase
        jmp AttackTimers
FirePressed:
        bit Phase
        bvs AttackTimers
        lda Phase
        ora #$40
        sta Phase
        iny
AttackTimers:
        lda Lives
        beq AttackColor
        lda HaloFrames
        beq AttackInactive
        dec HaloFrames
        bne AttackColor
        ldx Level
        lda RecoverTable,x
        sta HaloRecover
        bne AttackColor
AttackInactive:
        lda HaloRecover
        beq TryFire
        dec HaloRecover
        bne AttackColor
TryFire:
        tya
        beq AttackColor
        lda $BE             ; a press during the stage transition is consumed
        bne AttackColor
        lda Invulnerable
        bmi AttackColor     ; no trigger on the respawn frame
        lda #12
        sta HaloFrames
AttackColor:
AttackRadius:
        ldx Level
        lda RadiusTable,x
        sta HaloRadius
        rts

        ORG $FA00
PlayPF1:
        dc.b $00,$00,$00,$00,$00,$00,$00,$18,$18,$18,$18,$18,$18,$18,$18,$3C
        dc.b $7E,$7E,$7E,$FF,$FF,$FF,$FF,$7E,$7E,$7E,$3C,$3C,$18,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$18,$18,$18,$18,$18,$18,$18,$7E,$FF,$FF,$FF,$7E,$7E,$7E,$7E
        dc.b $3C,$3C,$3C,$18,$18,$18,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$18,$18,$18,$18,$18,$18,$7F
        dc.b $7F,$7F,$7E,$7E,$7E,$38,$7C,$7C,$7C,$38,$38,$38,$10,$10,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$18
        dc.b $18,$18,$18,$18,$18,$18,$18,$3C,$7E,$7E,$7E,$7F,$7F,$7F,$7F,$7E
        dc.b $7E,$7E,$3C,$3C,$18,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$FF,$FF,$FF,$FF
        dc.b $FF,$FF,$FF,$7E,$7E,$7E,$7E,$3C,$3C,$3C,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$7E,$7E,$7E,$7E,$3C,$3C
        dc.b $3C,$18,$18,$18,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$7F,$7F,$7F,$7F,$7F
        dc.b $7E,$7E,$7E,$3E,$3E,$3E,$3E,$1C,$1C,$1C,$08,$08,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$3E,$3E,$3E
        dc.b $1C,$1C,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$C3,$C3,$C3,$C3,$C3,$C3,$C3,$C3
        dc.b $C3,$E7,$E7,$FF,$FF,$FF,$7E,$7E,$7E,$3C,$3C,$3C,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$FE,$FE,$FE,$82,$82,$82,$BA,$BA,$BA,$8A,$8A,$8A,$FA,$FA,$FA
        dc.b $02,$02,$02,$FE,$FE,$FE,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$7E,$7E,$7E,$42,$42,$42,$5E
        dc.b $5E,$5E,$52,$52,$52,$5E,$5E,$5E,$40,$40,$40,$7F,$7F,$7F,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $43,$43,$43,$43,$43,$43,$43,$43,$43,$7F,$7F,$7F,$7E,$7E,$7E,$3C
        dc.b $3C,$3C,$18,$18,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$FF,$FF,$FF,$FF,$FF,$FF,$FF
        dc.b $FF,$FF,$EF,$EF,$EF,$E7,$E7,$E7,$C7,$C7,$C7,$C7,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF,$FF
        dc.b $DB,$DB,$DB,$DB,$DB,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$7F,$7F,$7F,$7F,$7F,$7F,$7F
        dc.b $7F,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$35,$35,$35,$35,$35,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$7F,$7F,$7F,$7F,$7F,$7F,$7F,$6F,$6F,$6F,$67,$67,$67,$63,$63
        dc.b $63,$61,$61,$61,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
; End at $FD00 (exclusive), eight*96 bytes.
        ORG $FD00
OrbScan:
        ds 70,0
        ds 4,2      ; compact eight physical lines around the orb collision center
        ds 86,0    ; separate cap table at $FDA0
HaloCapRows:
        dc.b 2,2
        ds $FE00-*,0      ; all indexed cap reads remain in zero-padded FD
        ORG $FE00
NewHaloSetup:
        ; Attach M0 until it has a valid, current-frame halo position.
        lda #2
        sta RESMP0
        lda #1
        sta HaloRowPtr
        lda #$FF
        sta HaloRowPtr+1
        lda HaloFrames
        bne HaloCheckBudget
        rts
HaloCheckBudget:
        bit TIMINT
        bmi HaloSetupDone
        lda INTIM
        bmi HaloSetupDone
        cmp #12
        bcc HaloSetupDone
        lda FrameCount
        and #1
        bne HaloCap
        lda PlayerY
        lsr
        adc #$28           ; ceil(PlayerY/2) + side-band seed
        sta HaloRowPtr
        lda FrameCount
        and #2
        bne HaloAtRight
        lda PlayerX
        sec
        sbc HaloRadius
        cmp #5
        bcc HaloSetupDone
        cmp #160
        bcs HaloSetupDone
        bcc HaloPosition
HaloAtRight:
        lda PlayerX
        clc
        adc HaloRadius
        cmp #159
        bcs HaloSetupDone
        ldx Level
        sbc HaloRightInset,x ; carry is clear, includes one-clock origin correction
        jmp HaloPosition
HaloCap:
        lda FrameCount
        and #2
        bne HaloCapBottom
        lda PlayerY
        sec
        sbc HaloRadius
        bcc HaloSetupDone
        bcs HaloCapY
HaloCapBottom:
        lda PlayerY
        clc
        adc HaloRadius
HaloCapY:
        cmp #6
        bcc HaloSetupDone
        cmp #171
        bcs HaloSetupDone
        lsr
        adc #$48           ; HaloCapRows - 88 with ceil(Y/2)
        sta HaloRowPtr
        lda #$FD
        sta HaloRowPtr+1
        ldx Level
        lda HaloCapSizes,x
        sta NUSIZ0
        lda PlayerX
        sec
        sbc HaloCapInset,x
HaloPosition:
        ldx #0
        stx RESMP0
        jsr PositionMissile0
        sta WSYNC
        sta HMOVE
        lda #0
        sta HMM0
HaloSetupDone:
        rts
HaloRightInset:
        dc.b 0,2,4,8
HaloCapInset:
        dc.b 0,4,6,6
HaloCapSizes:
        dc.b 0,$20,$35,$37
HudDraw:
        lda #$0E
        sta COLUPF
        lda #$10            ; repeat order, left half score, right half lives
        sta CTRLPF
HudDrawRow:
        sta WSYNC
        lda HudLifeDigits,y
        sta PF0
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
        lda #0
        sta PF0
        nop
        nop
        nop
        sta PF1             ; after all left PF1 pixels
        lda (HudLifePtr),y
        nop
        nop
        sta PF2             ; after left PF2, before right PF2 at X128
        lsr JoyState
        bcs HudDrawRow      ; repeat first and last glyph rows
HudAdvance:
        iny
        inx
        cpx #5
        bne HudDrawRow
        sta WSYNC
        lda #0
        sta PF0
        sta PF2
        lda Stage
        and #1
        ora #$10
        sta CTRLPF
        rts

        ORG $FF01
        ds 124,0   ; FF01..FF7C: OFF M1/BL/M0 zero guard
HaloSideRim:
        ds 7,2     ; FF7D..FF83: 14-line cardinal arc
        ds 120,0   ; FF84..FFFB: zero guard
        ORG $FFFC
        dc.w Reset
        dc.w Reset

