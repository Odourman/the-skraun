; FULLGAME-1 F6 bank0: independent logical K1/K2/Ranger for experimental play.
; THIS IS A DEVELOPMENT CANDIDATE. All three share a phase-multiplexed P1
; and currently display on one fixed Y-band. No claim of full game/3 sprites.
        processor 6502
COLUP1    = $07
NUSIZ1    = $05
AUDC0     = $15
AUDF0     = $17
AUDV0     = $19
PlayerX   = $80
PlayerY   = $81
Level     = $82
FrameCount= $8D
HalfW     = $98
HalfH     = $99
HaloFrames= $9E
HaloRadius= $A0
ArrowMajor= $A1     ; bit 7 selects Y as the major axis
ArrowMinor= $A2
ArrowDX   = $A3
ArrowDY   = $A4
KnightDir = $A5
Stage     = $AA
Lives     = $AC
ScoreLo   = $AD
ScoreHi   = $AE
ScoreTop  = $84      ; high decimal digit as five-row glyph offset
KnightX   = $AF
SwordWarn = $B0
SwordStrike=$B1
ArrowError= $B2     ; projectile error accumulator
Invuln    = $B3
StageKills= $B4
KillsNeed = $B5
ArrowX    = $B8
ArrowY    = $B9
BonusLo   = $BC
BonusHi   = $BD
StagePause= $BE
SoundFrames=$BF
K1X       = $D0
K1Y       = $D1
K1Warn    = $D2
K1Strike  = $D3
K1Rest    = $D4
K1Alive   = $D5
K1Facing  = $D6
K2X       = $D7
K2Y       = $D8
K2Warn    = $D9
K2Strike  = $DA
K2Rest    = $DB
K2Alive   = $DC
K2Facing  = $DD
RX        = $DE
RY        = $DF
RDraw     = $E0
RRelease  = $E1
RCool     = $E2
RAlive    = $E3
DrawSlot  = $E4
Reserves  = $E5
ResWait   = $E6
NextSlot  = $E7
EnemyBottom = $E8
ScratchIX = $E8
ScratchMin=$E9
ScratchMax=$EA
ScratchY  = $EB
WorldPFPtr= $EC
WorldShift= $EE
AuxMode   = $EF
        SEG GameAux
        ORG $F000
ColdBoot:
        lda $FFF9
        jmp $F000
; Bounded two-segment refinement of the conservative LOS (old fast path first).
; ScratchMin/Max = x bounds; ScratchIX/Y = y bounds. No new RAM.
RangerLaneRefined:
        jsr RangerHasClearLane
        beq LaneRefine
        rts
LaneRefine:
        lda RX
        cmp PlayerX
        bne RefineXDiff
        lda #0
        rts
RefineXDiff:
        lda RY
        cmp PlayerY
        bne RefineYDiff
        lda #0
        rts
RefineYDiff:
        lda RX
        cmp PlayerX
        bcs Half0XHigh
        sta ScratchMin
        clc
        adc PlayerX
        ror
        adc #0
        sta ScratchMax
        jmp Half0XDone
Half0XHigh:
        sta ScratchMax
        clc
        adc PlayerX
        ror
        sta ScratchMin
Half0XDone:
        lda RY
        cmp PlayerY
        bcs Half0YHigh
        sta ScratchIX
        clc
        adc PlayerY
        ror
        adc #0
        sta ScratchY
        jmp Half0YDone
Half0YHigh:
        sta ScratchY
        clc
        adc PlayerY
        ror
        sta ScratchIX
Half0YDone:
        jsr LaneHalfBox
        beq RefineBlocked
        lda PlayerX
        cmp RX
        bcs Half1XHigh
        sta ScratchMin
        clc
        adc RX
        ror
        adc #0
        sta ScratchMax
        jmp Half1XDone
Half1XHigh:
        sta ScratchMax
        clc
        adc RX
        ror
        sta ScratchMin
Half1XDone:
        lda PlayerY
        cmp RY
        bcs Half1YHigh
        sta ScratchIX
        clc
        adc RY
        ror
        adc #0
        sta ScratchY
        jmp Half1YDone
Half1YHigh:
        sta ScratchY
        clc
        adc RY
        ror
        sta ScratchIX
Half1YDone:
        jmp LaneHalfBox
RefineBlocked:
        lda #0
        rts
LaneHalfBox:
        ldx #0
LaneBand:
        lda ScratchY
        cmp $C2,x
        bcc LaneNextBand
        lda ScratchIX
        cmp $C3,x
        bcs LaneNextBand
        lda ScratchMax
        cmp $C0,x
        bcc LaneNextBand
        lda ScratchMin
        cmp $C1,x
        bcc RefineBlocked
        lda ScratchMax
        cmp $C4,x
        bcc LaneNextBand
        lda ScratchMin
        cmp $C5,x
        bcc RefineBlocked
LaneNextBand:
        cpx #8
        beq RefineClear
        ldx #8
        bne LaneBand
RefineClear:
        lda #1
        rts

        ORG $F100
ActorEntry:
        lda ScratchY
        beq ActorsRunning
        cmp #2
        beq ActorsRespawning
        jsr ActorInitialize
        jmp AuxiliaryReturn
ActorsRespawning:
        jsr RepositionSurvivors
        jsr ChooseP1
        jmp AuxiliaryReturn
ActorsRunning:
        jsr Knight1Tick
        jsr Knight2Tick
        jsr RangerTick
        jsr ReserveTick
        jsr ChooseP1
        jmp AuxiliaryReturn

ActorInitialize:
        ldx #$1F
        lda #0
ClearActorRAM:
        sta $D0,x
        dex
        bpl ClearActorRAM
        lda #122
        sta K1X
        lda #96
        sta K1Y
        lda #1
        sta K1Alive
        lda #43
        sta K2X
        lda #96
        sta K2Y
        lda #1
        sta K2Alive
        lda #140       ; Ranger enters away from P0, no point-blank arrow
        sta RX
        lda #88        ; accessible open center-right corridor in all 8 worlds
        sta RY
        lda #1
        sta RAlive
        lda #36
        sta RCool
        lda KillsNeed
        sec
        sbc #3
        sta Reserves
        lda #0
        sta NextSlot
        jsr InstallWorldMap
        jsr ChooseP1
        rts

Knight1Tick:
        ldx #0
        jmp KnightTick
Knight2Tick:
        ldx #7
KnightTick:
        lda K1Alive,x
        bne KnightExists
        rts
KnightExists:
        lda HaloFrames
        beq KnightTimer
        jsr KnightWithinHalo
        beq KnightTimer
        lda #0
        sta K1Alive,x
        jmp AwardKnight
KnightTimer:
        lda K1Warn,x
        beq KnightTryStrike
        dec K1Warn,x
        bne KnightReturn
        jsr SwordAdvance
        lda #9
        sta K1Strike,x
        ; Audible sword hit-window cue. Strike outranks prior warning.
        lda #$A0
        jsr QueueSound
KnightReturn:
        rts
KnightTryStrike:
        lda K1Strike,x
        beq KnightTryRest
        dec K1Strike,x
        jsr KnightCanHit
        beq NoKnightHit
AcceptKnightDamage:
        jsr DamagePlayer
NoKnightHit:
        lda K1Strike,x
        bne KnightReturn
        lda #24
        sta K1Rest,x
        rts
KnightTryRest:
        lda K1Rest,x
        beq KnightReady
        dec K1Rest,x
        rts
KnightReady:
        jsr KnightInRange
        beq KnightChase
        lda #16
        sta K1Warn,x
        ; Short telegraph cue: never interrupt an existing sound event.
        lda #$B0
        jsr QueueSound
        lda K1X,x
        cmp PlayerX
        bcc FaceRight
        lda #8
        sta K1Facing,x
        rts
FaceRight:
        lda #0
        sta K1Facing,x
        rts
KnightChase:
        ; Keep actual K1/K2 collision rectangles consistent with the world.
        ; All three trials run offscreen in F6 bank0, not in the 76c kernel.
        txa
        eor FrameCount
        and #7
        beq KnightReturn
        cmp #4
        beq KnightReturn
        cmp #1
        bne KnightMoveStart
        lda K1X,x
        cmp PlayerX
        beq KnightMoveStart
        lda K1Y,x
        cmp PlayerY
        bne KnightReturn
KnightMoveStart:
        lda K1X,x
        sta ScratchMin
        lda K1Y,x
        sta ScratchMax
        lda K1X,x
        cmp PlayerX
        beq KnightStepY
        bcc KnightMoveRight
        cmp #24
        bcc KnightStepY
        dec K1X,x
        jmp KnightStepY
KnightMoveRight:
        cmp #143
        bcs KnightStepY
        inc K1X,x
KnightStepY:
        lda PlayerY
        cpx #0
        beq KnightTargetReady
        clc
        adc #5               ; second knight cuts across the lower shoulder
KnightTargetReady:
        cmp K1Y,x
        beq KnightMovementCheck
        bcs KnightMoveDown
        lda K1Y,x
        cmp #34
        bcc KnightMovementCheck
        dec K1Y,x
        jmp KnightMovementCheck
KnightMoveDown:
        lda K1Y,x
        cmp #155
        bcs KnightMovementCheck
        inc K1Y,x
KnightMovementCheck:
        ; Prefer full diagonal step; else X-only; else Y-only.
        ; These are actual logical actor positions used by combat and shots.
        jsr KnightBlocked
        beq KnightMovementDone
        lda K1Y,x
        cmp ScratchMax
        beq KnightRejectX
        sta ScratchY
        lda ScratchMax
        sta K1Y,x
        lda K1X,x
        cmp ScratchMin
        beq KnightMovementDone
        jsr KnightBlocked
        beq KnightMovementDone
        lda ScratchMin
        sta K1X,x
        lda ScratchY
        sta K1Y,x
        jsr KnightBlocked
        beq KnightMovementDone
        lda ScratchMax
        sta K1Y,x
KnightMovementDone:
        rts
KnightRejectX:
        lda ScratchMin
        sta K1X,x
        rts

KnightBlocked:
        ; Select the vertical band first; stage 5 has different X ranges.
        ; Normal actor movement and spawns keep Y in 33..155 inclusive:
        ; y+8 is always >= top min; y-8 is always < bottom max.
        ldy #0
        lda K1Y,x
        sec
        sbc #8
        cmp $C3
        bcc KnightCheckX
        adc #15
        cmp $CA
        bcc KnightNotBlocked
        ldy #8
KnightCheckX:
        lda K1X,x
        clc
        adc #4
        cmp $C0,y
        bcc KnightNotBlocked
        cmp $C4,y
        bcc KnightCheckLeft
        sbc #8
        cmp $C5,y
        bcc KnightBlockedYes
        bcs KnightNotBlocked
KnightCheckLeft:
        sbc #7
        cmp $C1,y
        bcc KnightBlockedYes
KnightNotBlocked:
        lda #0
        rts
KnightBlockedYes:
        lda #1
        rts
        ds $F2AF-*,0

KnightInRange:
        lda PlayerX
        sec
        sbc K1X,x
        bcs KnightAbsX
        eor #$FF
        clc
        adc #1
KnightAbsX:
        ldy Level
        cmp SwordWarnX,y
        bcs KnightOut
        lda PlayerY
        sec
        sbc K1Y,x
        bcs KnightAbsY
        eor #$FF
        clc
        adc #1
KnightAbsY:
        cmp SwordWarnY,y
        bcs KnightOut
        lda #1
        rts
KnightOut:
        lda #0
        rts
KnightWithinHalo:
        lda PlayerX
        sec
        sbc K1X,x
        bcs HaloKnightXAbs
        eor #$FF
        clc
        adc #1
HaloKnightXAbs:
        sta $E9
        lda PlayerY
        sec
        sbc K1Y,x
        bcs HaloKnightYAbs
        eor #$FF
        clc
        adc #1
HaloKnightYAbs:
        tay
        lda $E9
        jsr OctagonOutside
        bcs KnightOut
        lda #1
        rts

KnightCanHit:
        cpx #0
        bne KnightCheck2Visible
        lda DrawSlot
        beq KnightIsVisible
        jmp KnightIsHidden
KnightCheck2Visible:
        lda DrawSlot
        cmp #1
        beq KnightIsVisible
KnightIsHidden:
        lda #0
        rts
KnightIsVisible:
        lda SwordStrike    ; snapshot drawn during the current visible frame
        beq KnightOut
        lda Invuln
        bne KnightOut
        jsr SwordOverlapsBody
        beq KnightOut
SwordTestObstacles:
        ; Physical solids $C0-$CF are now unexpanded 4 x 4B.
        ; Test horizontal cast from attackerY through each rectangle.
        stx ScratchIX
        lda K1X,x
        cmp PlayerX
        bcc OrderKnightFirst
        sta ScratchMax
        lda PlayerX
        sta ScratchMin
        jmp SwordOrderDone
OrderKnightFirst:
        sta ScratchMin
        lda PlayerX
        sta ScratchMax
SwordOrderDone:
        lda K1Y,x
        sta ScratchY
        ldx #0
SwordObstacleLoop:
        lda ScratchY
        cmp $C2,x
        bcc SwordNextObstacle
        cmp $C3,x
        bcs SwordNextObstacle
        lda ScratchMin
        cmp $C1,x
        bcs SwordNextObstacle
        lda ScratchMax
        cmp $C0,x
        bcc SwordNextObstacle
        ldx ScratchIX
        lda #0
        rts
SwordNextObstacle:
        txa
        clc
        adc #4
        tax
        cpx #16
        bcc SwordObstacleLoop
        ldx ScratchIX
        lda #1
        rts

DamagePlayer:
        lda Invuln
        bne DamageDone
        lda #60
        sta Invuln
        lda #$C0
        jsr QueueSound
        lda Level
        cmp #1
        beq DamageLife
        dec Level
DamageDone:
        rts
DamageLife:
        lda Lives
        beq DamageDone
        dec Lives
        bne LifeRemains
        lda #$E0
        jsr QueueSound
LifeRemains:
        lda #$BC          ; respawn flag plus 60 frame protection
        sta Invuln
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        rts

        ORG $F400
; Exact neutral dual-knight copies. Only when Y, facing, neutral art and
; spacing match the hardware. Never enable duplicates with an active M1.
; Ranger scheduling remains intact; it is never replaced with a copy.
ExactNeutralPair:
        pha
        lda #$10
        sta NUSIZ1
        pla
        cmp #2
        bcs PairReturn
        pha
        lda ArrowDX
        bne PairReject
        lda K1Alive
        and K2Alive
        beq PairReject
        lda K1Warn
        ora K1Strike
        ora K2Warn
        ora K2Strike
        bne PairReject
        lda K1Y
        cmp K2Y
        bne PairReject
        ; Neutral REFP1 is derived from relative player X; require same side.
        lda K1X
        cmp PlayerX
        lda #0
        rol
        sta ScratchMin
        lda K2X
        cmp PlayerX
        lda #0
        rol
        cmp ScratchMin
        bne PairReject
        ldx #0
        lda K2X
        sec
        sbc K1X
        bcs PairGap
        eor #$FF
        clc
        adc #1
        inx
PairGap:
        ldy #$11
        cmp #16
        beq PairAccept
        ldy #$12
        cmp #32
        beq PairAccept
        ldy #$14
        cmp #64
        bne PairReject
PairAccept:
        sty NUSIZ1
        pla
        txa
PairReturn:
        rts
PairReject:
        pla
        rts

        ORG $F500
; Forward blade and inflated player body overlap. The 8-clock P1
; strike mask extends only a few clocks beyond the centre of the knight.
SwordOverlapsBody:
        lda K1Facing,x
        bne SwordLeftDelta
        lda PlayerX
        sec
        sbc K1X,x
        jmp SwordForwardDelta
SwordLeftDelta:
        lda K1X,x
        sec
        sbc PlayerX
SwordForwardDelta:
        bcc SwordMiss
        ldy Level
        cmp SwordBodyX,y
        bcs SwordMiss
SwordCheckY:
        lda PlayerY
        sec
        sbc K1Y,x
        bcs SwordAbsY
        eor #$FF
        clc
        adc #1
SwordAbsY:
        cmp SwordBodyY,y
        bcs SwordMiss
SwordBodyHit:
        lda #1
        rts
SwordMiss:
        lda #0
        rts

SwordBodyX:
        dc.b 0,9,13,19
SwordBodyY:
        dc.b 0,7,10,13
SwordAdvance:
        cpx #7
        beq SwordLongStep
        lda Stage
        cmp #8
        bcc SwordAdvanceDone  ; the last arena adds the lead knight.s step
        lda #1
        bne SwordSetStep
SwordLongStep:
        lda #2
SwordSetStep:
        sta ScratchY
        lda K1X,x
        sta ScratchMin
        ldy K1Facing,x
        bne SwordAdvanceLeft
        clc
        adc ScratchY
        cmp #151
        bcs SwordAdvanceDone
        bcc SwordTryAdvance
SwordAdvanceLeft:
        sec
        sbc ScratchY
        cmp #10
        bcc SwordAdvanceDone
SwordTryAdvance:
        sta K1X,x
        jsr KnightBlocked
        beq SwordAdvanceDone
        lda ScratchMin
        sta K1X,x
SwordAdvanceDone:
        rts
SwordWarnX:
        dc.b 0,12,15,22
SwordWarnY:
        dc.b 0,9,13,18

        ORG $F6C3
; Entered immediately after LDA $FFF6 in bank2 at the same physical PC.
AuxiliaryEntryTrampoline:
        jmp ActorEntry
        ORG $F6D0
AuxiliaryReturn:
        lda $FFF8
; The RTS after this address MUST be fetched from F6 bank2 at $F6D3.
        ORG $F700

RangerTick:
        lda RAlive
        beq RangerDoneEarly
        and #1
        bne RangerExists
        jmp RangerAway
RangerDoneEarly:
        rts
RangerExists:
        lda HaloFrames
        beq RangerTimers
        lda PlayerX
        sec
        sbc RX
        bcs RangerAbsX
        eor #$FF
        clc
        adc #1
RangerAbsX:
        sta $E9
        lda PlayerY
        sec
        sbc RY
        bcs RangerAbsY
        eor #$FF
        clc
        adc #1
RangerAbsY:
        tay
        lda $E9
        jsr OctagonOutside
        bcs RangerTimers
        lda #0
        sta RAlive
        jmp AwardRanger
RangerTimers:
        jmp RangerTactics
RangerDone:
        rts
RangerMovementCheck:
        ; On a blocked diagonal try ONE alternate axis per tick, alternating
        ; on bit2. This bounds the collision cost and still slides along walls.
        ldx #14
        jsr RangerBlocked
        beq RangerMovementDone
        lda FrameCount
        and #4
        bne RangerFallbackY
        lda RY
        sta ScratchY
        lda ScratchMax
        sta RY
        lda RX
        cmp ScratchMin
        bne RangerFallbackCheck
        ; X did not change; try Y only instead.
        lda ScratchY
        sta RY
        jmp RangerFallbackCheck
RangerFallbackY:
        lda RX
        sta ScratchY
        lda ScratchMin
        sta RX
        lda RY
        cmp ScratchMax
        bne RangerFallbackCheck
        lda ScratchY
        sta RX
RangerFallbackCheck:
        jsr RangerBlocked
        beq RangerMovementDone
        lda ScratchMin
        sta RX
        lda ScratchMax
        sta RY
RangerMovementDone:
        rts

SpawnArrow:
        lda ArrowDX
        bne SpawnDone
        lda RX
        sta ArrowX
        lda RY
        sta ArrowY
        jsr InitializeAim
ArrowCooldownSet:
        lda #2
        sta $9D
        ldx Stage
        lda RangerCooldowns,x
        sta RCool
        lda #$80
        jsr QueueSound
SpawnDone:
        rts

ReserveTick:
        lda Reserves
        beq ReserveDone
        ; Reserve appears ~72 NTSC frames *after* a knight slot
        ; becomes vacant. A full wave never respawns already killed
        ; knights: Reserves is the exact remaining unseen quota.
        lda K1Alive
        beq ReserveSlotOpen
        lda K2Alive
        bne ReserveOccupied
ReserveSlotOpen:
        lda ResWait
        bne ReserveCountdown
        lda #72
        sta ResWait
        rts
ReserveCountdown:
        dec ResWait
        bne ReserveDone
        ldx #0
        lda K1Alive
        beq ReservePoint
        ldx #7
ReservePoint:
        lda #24
        ldy PlayerX
        cpy #80
        bcs ReserveFarSide
        lda #136
ReserveFarSide:
        sta K1X,x
        lda #88
        sta K1Y,x
        lda #0
        sta K1Warn,x
        sta K1Strike,x
        sta K1Rest,x
        lda #1
        sta K1Alive,x
        dec Reserves
        lda #0
        sta ResWait
        rts
ReserveOccupied:
        ; Clear a countdown if the free slot was somehow filled.
        lda #0
        sta ResWait
ReserveDone:
        rts

ChooseP1:
        lda RAlive
        and #1
        ora K1Alive
        ora K2Alive
        bne ChooseLiveP1
        ; No phantom knight during stage-clear pause.
        lda #200          ; x=1..186 minus 200 never selects 0..15
        sta EnemyBottom
        lda #$10
        sta NUSIZ1
        rts
ChooseLiveP1:
        jsr AdaptiveSelect
        jsr ExactNeutralPair
        sta DrawSlot
        cmp #1
        beq ChooseK2
        cmp #2
        beq ChooseRanger
ChooseK1:
        lda K1X
        sta KnightX
        lda K1Alive
        lda K1Warn
        sta SwordWarn
        lda K1Strike
        sta SwordStrike
        lda K1Facing
        sta KnightDir
        lda K1Strike
        beq K1WarnTint
        lda #$46       ; warm bright strike cue while dangerous
        bne K1ColorDone
K1WarnTint:
        lda K1Warn
        beq K1NeutralTint
        lda #$2E       ; stable golden 24f sword telegraph
        bne K1ColorDone
K1NeutralTint:
        lda #$9E       ; original light-blue armour
K1ColorDone:
        sta COLUP1
        lda #170          ; preload P1 for next physical row via VDELP1
        sec
        sbc K1Y
        sta EnemyBottom
        rts
ChooseK2:
        lda K2X
        sta KnightX
        lda K2Alive
        lda K2Warn
        sta SwordWarn
        lda K2Strike
        sta SwordStrike
        lda K2Facing
        sta KnightDir
        lda K2Strike
        beq K2WarnTint
        lda #$46       ; warm bright strike cue while dangerous
        bne K2ColorDone
K2WarnTint:
        lda K2Warn
        beq K2NeutralTint
        lda #$2E       ; stable golden 24f sword telegraph
        bne K2ColorDone
K2NeutralTint:
        lda #$9E       ; original light-blue armour
K2ColorDone:
        sta COLUP1
        lda #170          ; preload P1 for next physical row via VDELP1
        sec
        sbc K2Y
        sta EnemyBottom
        rts
ChooseRanger:
        lda RX
        sta KnightX
        lda RAlive
        lda RDraw
        sta SwordWarn
        lda RRelease
        sta SwordStrike
        lda RAlive
        and #8
        sta KnightDir
        ldx Stage
        lda RangerColors,x
        sta COLUP1
        lda #170          ; preload P1 for next physical row via VDELP1
        sec
        sbc RY
        sta EnemyBottom
        rts

AwardKnight:
        ldx #100
        lda #$40
        jsr QueueSound
        jmp AwardAny
AwardRanger:
        ldx #250
        lda #$50
        jsr QueueSound
AwardAny:
        stx ScratchIX
        ; Two packed BCD bytes plus the high digit; +100 or +250.
        cpx #100
        bne ScoreAdd250
        sed
        clc
        lda ScoreHi
        adc #$01
        sta ScoreHi
        jmp ScoreCarry
ScoreAdd250:
        sed
        clc
        lda ScoreLo
        adc #$50
        sta ScoreLo
        lda ScoreHi
        adc #$02
        sta ScoreHi
ScoreCarry:
        cld
        bcc ScoreIncreaseDone
        lda ScoreTop
        cmp #45
        bcs ScoreSaturated
        adc #5             ; CMP cleared carry for a nonterminal glyph
        sta ScoreTop
        bcc ScoreIncreaseDone
ScoreSaturated:
        lda #$99          ; terminal five-digit display is 99999
        sta ScoreHi
        sta ScoreLo
ScoreIncreaseDone:
        lda ScratchIX
        clc
        adc BonusLo
        sta BonusLo
        lda BonusHi
        adc #0
        sta BonusHi
        lda BonusHi
        cmp #$13
        bcc NoExtraLife
        bne ExtraLife
        lda BonusLo
        cmp #$88
        bcc NoExtraLife
ExtraLife:
        sec
        lda BonusLo
        sbc #$88
        sta BonusLo
        lda BonusHi
        sbc #$13
        sta BonusHi
        lda Lives
        cmp #9
        bcs NoExtraLife
        inc Lives
        lda #$D0
        jsr QueueSound
NoExtraLife:
        inc StageKills
        lda StageKills
        cmp KillsNeed
        bcc AwardDone
        lda #90
        sta StagePause
        lda #$60
        jsr QueueSound
AwardDone:
        rts

; Highest-priority event mailbox, preserve X/Y for actor logic.
QueueSound:
        ; Halo/orb/arrow on channel0, warning/sword/damage on channel1.
        cmp #$A0
        bcs QueuePriorityVoice1
        cmp SoundFrames
        bcc SoundReqLower
        sta SoundFrames
SoundReqLower:
        rts
QueuePriorityVoice1:
        cmp $85
        bcc SoundReqLower
        sta $85
        rts

RangerColors:
        dc.b $00,$C6,$C8,$86,$88,$66,$68,$82,$84
RangerCooldowns:
        dc.b 0,176,176,150,150,126,126,102,102

; Eight physically different map layouts: 4 vertical shifts x mirror/repeat
; of the established collision/visual source. No claim of final world art.
; World PF pointer is set once per stage and *read without extra hotspots*
; in the F6 bank3 visible raster kernel. Source FA00, guard F9C1..F9FF=0.
InstallWorldMap:
        ldy Stage
        lda WorldPFLo,y
        sta WorldPFPtr
        lda WorldPFHi,y
        sta WorldPFPtr+1
        dey
        tya
        asl
        asl
        asl
        asl
        tax
        ldy #0
CopyStageSolids:
        lda WorldRects,x
        sta $C0,y
        inx
        iny
        cpy #16
        bcc CopyStageSolids
        lda #0
        sta WorldShift
        rts
WorldPFLo:
        dc.b $00,$00,$60,$C0,$20,$80,$E0,$40,$A0
WorldPFHi:
        dc.b $FA,$FA,$FA,$FA,$FB,$FB,$FB,$FC,$FC
WorldRects:
        dc.b $10,$30,$06,$30,$70,$90,$06,$30,$10,$30,$78,$A4,$70,$90,$78,$A4 ; Revision 3 stage 1, internal Y = arena Y - 9
        dc.b $14,$30,$08,$34,$64,$80,$08,$34,$14,$30,$76,$A0,$64,$80,$76,$A0 ; HEALTH-3 swapped stage 2 motif rectangles
        dc.b $10,$30,$0A,$2C,$70,$90,$0A,$2C,$10,$30,$7E,$9E,$70,$90,$7E,$9E ; Revision 3 stage 3, internal Y = arena Y - 9
        dc.b $14,$30,$0E,$2E,$64,$80,$0E,$2E,$14,$30,$7A,$9C,$64,$80,$7A,$9C ; HEALTH-3 swapped stage 4 motif rectangles
        dc.b $10,$2C,$06,$30,$74,$90,$06,$30,$10,$30,$7A,$A2,$70,$90,$7A,$A2 ; Revision 3 stage 5, internal Y = arena Y - 9
        dc.b $14,$30,$0A,$32,$64,$80,$0A,$32,$14,$30,$76,$A0,$64,$80,$76,$A0 ; HEALTH-3 swapped stage 6 motif rectangles
        dc.b $10,$30,$08,$30,$70,$90,$08,$30,$10,$30,$7A,$A0,$70,$90,$7A,$A0 ; Revision 3 stage 7, internal Y = arena Y - 9
        dc.b $14,$30,$0A,$30,$64,$80,$0A,$30,$14,$30,$78,$A0,$64,$80,$78,$A0 ; HEALTH-3 swapped stage 8 motif rectangles

        ORG $FA80
; Display only. Single urgent threat gets two frames in each three.
; Equal threats use the same cyclic live-actor cursor as peaceful frames.
; Damage still checks the previously displayed active strike.
AdaptiveSelect:
        lda K1Alive
        beq ASCheckK2Strike
        lda K1Strike
        beq ASCheckK2Strike
        lda K2Alive
        beq ASPickK1
        lda K2Strike
        bne ASBoth
        jmp ASPickK1
ASCheckK2Strike:
        lda K2Alive
        beq ASCheckK1Warn
        lda K2Strike
        bne ASPickK2
ASCheckK1Warn:
        lda K1Alive
        beq ASCheckK2Warn
        lda K1Warn
        beq ASCheckK2Warn
        lda K2Alive
        beq ASPickK1
        lda K2Warn
        bne ASBoth
        jmp ASPickK1
ASCheckK2Warn:
        lda K2Alive
        beq ASCheckRanger
        lda K2Warn
        bne ASPickK2
ASCheckRanger:
        lda RAlive
        and #1
        beq ASRoundRobin
        lda RDraw
        ora RRelease
        beq ASRoundRobin
ASPickRanger:
        ldx #2
        jmp ASMajority
ASPickK1:
        ldx #0
        jmp ASMajority
ASPickK2:
        ldx #1
        jmp ASMajority
ASBoth:
        jmp ASRoundRobin
ASMajority:
        lda $86           ; two of three frames prioritize the active attack
        and #3
        bne ASReturnHigh
        ; On every third frame deliberately give an *other* living
        ; character the turn, so a 24-frame telegraph has >=16 frames
        ; with the warning knight without indefinitely hiding the Ranger.
        jsr ASRoundRobin
        sta DrawSlot
        txa
        cmp DrawSlot
        bne ASReturnAlternative
        jsr ASRoundRobin
        rts
ASReturnAlternative:
        lda DrawSlot
        rts
ASReturnHigh:
        txa
        rts
ASRoundRobin:
        ldy #3
ASRRLoop:
        lda NextSlot
        clc
        adc #1
        cmp #3
        bcc ASRRValue
        lda #0
ASRRValue:
        sta NextSlot
        cmp #1
        beq ASRRK2
        cmp #2
        beq ASRRRanger
        lda K1Alive
        bne ASRRK1Good
        beq ASRRNext
ASRRK1Good:
        lda #0
        rts
ASRRK2:
        lda K2Alive
        beq ASRRNext
        lda #1
        rts
ASRRRanger:
        lda RAlive
        and #1
        beq ASRRNext
        lda #2
        rts
ASRRNext:
        dey
        bne ASRRLoop
        lda #0
        rts

; Shared octagonal radial metric: maximum of |dx|,|dy| + half minimum.
; Input A=unsigned |dx| and Y=unsigned |dy|. Output Carry=1 OUTSIDE,
; Carry=0 INSIDE. X is preserved; scratch E9/EA lives only during call.
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

        ORG $FC00
RepositionSurvivors:
        ; Preserve alive flags, reserves, kills, score and the current orb.
        lda #0
        sta K1Warn
        sta K1Strike
        sta K1Rest
        sta K2Warn
        sta K2Strike
        sta K2Rest
        lda K1Alive
        beq RespawnCheckK2
        lda #122
        sta K1X
        lda #96
        sta K1Y
RespawnCheckK2:
        lda K2Alive
        beq RespawnCheckRanger
        lda #43
        sta K2X
        lda #96
        sta K2Y
RespawnCheckRanger:
        lda RAlive
        and #1
        beq RespawnActorsDone
        lda RAlive
        and #3
        sta RAlive
        lda #0
        sta RDraw
        sta RRelease
        lda #90
        sta RCool
        lda #140
        sta RX
        lda #88
        sta RY
RespawnActorsDone:
        rts

InitializeAim:
        ; Bresenham ratio measured at release, never read the target again.
        ldy #1
        lda PlayerX
        sec
        sbc RX
        bcs ArrowAimX
        eor #$FF
        adc #1
        ldy #$FF
ArrowAimX:
        sty ArrowDX
        sta ArrowMajor
        ldy #1
        lda PlayerY
        sec
        sbc RY
        bcs ArrowAimY
        eor #$FF
        adc #1
        ldy #$FF
ArrowAimY:
        sty ArrowDY
        ; A = |dy|, ArrowMajor currently |dx|. Normalize only long rays
        ; to make the major magnitude fit a byte with a free axis bit.
        ldy #0
        cmp ArrowMajor
        bcc AimXMajor
        ldx ArrowMajor
        stx ArrowMinor
        ldy #$80
        bne NormalizeAim
AimXMajor:
        sta ArrowMinor
        lda ArrowMajor
NormalizeAim:
        cmp #0
        bne NonZeroAim
        lda #1
NonZeroAim:
        bpl SaveAim
        lsr
        lsr ArrowMinor
SaveAim:
        sta ArrowMajor
        lsr
        sta ArrowError
        tya
        ora ArrowMajor
        sta ArrowMajor
        rts

RangerHasClearLane:
        ; Reject any solid intersecting the bounding rectangle of the shot.
        ; This is conservative on diagonals, where the ray can miss a box
        ; that the rectangle meets. The Ranger then keeps moving.
        ldx #0
CheckLaneRectangle:
        lda RX
        cmp $C0,x
        bcs CheckLaneRight
        lda PlayerX
        cmp $C0,x
        bcc NextLaneRectangle
CheckLaneRight:
        lda RX
        cmp $C1,x
        bcc CheckLaneTop
        lda PlayerX
        cmp $C1,x
        bcs NextLaneRectangle
CheckLaneTop:
        lda RY
        cmp $C2,x
        bcs CheckLaneBottom
        lda PlayerY
        cmp $C2,x
        bcc NextLaneRectangle
CheckLaneBottom:
        lda RY
        cmp $C3,x
        bcc LaneBlocked
        lda PlayerY
        cmp $C3,x
        bcc LaneBlocked
NextLaneRectangle:
        inx
        inx
        inx
        inx
        cpx #16
        bcc CheckLaneRectangle
        lda #1
        rts
LaneBlocked:
        lda #0
        rts

; RAlive bit0 present, bit1 escape used; $10/$20/$30/$40 = committed exit (present).
; $02 = away; RCool=150 half-rate ticks; RRelease=exit index while away.
; Scratch E8/E9/EA/EB transient, no new persistent RAM.
RangerTactics:
        lda RAlive
        cmp #$10
        bcc RangerNormal
        jmp RangerExitMove
RangerNormal:
        lda RDraw
        beq RangerReleaseTick
        dec RDraw
        bne RangerDoneNear
        jsr RangerDistance
        cmp #30
        bcc RangerAbort
        cmp #45
        bcs RangerAbort
        lda ArrowDX
        bne RangerAbort
        jsr RangerLaneRefined
        beq RangerAbort
        jsr SpawnArrow
        lda #8
        sta RRelease
RangerDoneNear:
        rts
RangerAbort:
        lda #36
        sta RCool
        rts
RangerReleaseTick:
        lda RRelease
        beq RangerCoolTick
        dec RRelease
        rts
RangerCoolTick:
        lda RCool
        beq RangerRate
        dec RCool
RangerRate:
        lda FrameCount
        and #3
        beq RangerRateTick
        cmp #3
        bne RangerDoneNear
RangerRateTick:
        jsr RangerDistance
        tay
        lda RAlive
        and #4
        beq RangerBand
        cpy #32
        bcs RangerInwardClear
        jmp RangerInward
RangerInwardClear:
        lda RAlive
        and #$FB
        sta RAlive
RangerBand:
        tya
        cmp #28
        bcc RangerThreat
        ldx Stage
        lda RCool
        cmp RetreatThreshold,x
        bcs RangerRetreat
        tya
        cmp #45
        bcs RangerApproach
        lda RCool
        bne RangerDoneNear
        tya
        cmp #36
        bcc RangerRetreat
        lda ArrowDX
        bne RangerDoneNear
        jsr RangerLaneRefined
        beq RangerApproach
        lda #30
        sta RDraw
        lda #$70
        jmp QueueSound
RangerThreat:
        lda RAlive
        and #3
        cmp #1
        bne RangerRetreat
        lda StageKills
        clc
        adc #1
        cmp KillsNeed
        bcs RangerRetreat  ; do not begin a five-second empty-arena escape
        lda RX
        cmp #38
        bcc RangerPickLeft
        cmp #122
        bcs RangerPickRight
        lda RY
        cmp #58
        bcc RangerPickTop
        cmp #118
        bcs RangerPickBottom
        bcc RangerRetreat
RangerPickLeft:
        lda #$11
        bne RangerCommitExit
RangerPickRight:
        lda #$21
        bne RangerCommitExit
RangerPickTop:
        lda #$31
        bne RangerCommitExit
RangerPickBottom:
        lda #$41
RangerCommitExit:
        sta RAlive
        rts
RangerApproach:
        lda PlayerX
        sta ScratchIX
        lda PlayerY
        sta ScratchY
        jmp RangerMoveTarget
RangerRetreat:
        ; Reflect the target toward a distant lane, avoiding permanent wall pressure.
        lda RX
        cmp PlayerX
        bcc RetreatLeft
        lda #152
        bne RetreatX
RetreatLeft:
        lda #8
RetreatX:
        sta ScratchIX
        lda RY
        cmp PlayerY
        bcc RetreatUp
        lda #158
        bne RetreatY
RetreatUp:
        lda #12
RetreatY:
        sta ScratchY
        ; Used escape: at a closed corner, commit to an inward slide until
        ; the distance is >=32. Not a teleport or a second escape.
        cmp RY
        bne RetreatMove
        lda ScratchIX
        cmp RX
        bne RetreatMove
        lda RAlive
        ora #4
        sta RAlive
RangerInward:
        lda #80
        sta ScratchIX
        lda #88
        sta ScratchY
RetreatMove:
        jmp RangerMoveTarget
RangerExitMove:
        lda FrameCount
        and #3
        beq ExitMoveTick
        cmp #3
        bne ExitDone
ExitMoveTick:
        lda RAlive
        lsr
        lsr
        lsr
        lsr
        tay
        dey
        lda EdgeX,y
        cmp RX
        bne ExitTarget
        lda EdgeY,y
        cmp RY
        beq RangerDepart
ExitTarget:
        lda EdgeX,y
        sta ScratchIX
        lda EdgeY,y
        sta ScratchY
        jmp RangerMoveTarget
RangerDepart:
        ; Abort only before crossing the edge if already the last enemy.
        lda StageKills
        clc
        adc #1
        cmp KillsNeed
        bcc RangerDepartAllowed
        lda #1
        sta RAlive
        rts
RangerDepartAllowed:
        sty RRelease
        lda #150
        sta RCool
        lda #2
        sta RAlive
        rts
ExitDone:
        rts
RangerAway:
        lda FrameCount
        and #1
        bne AwayDone
        dec RCool
        bne AwayDone
        ; Select a different edge with frame/player/stage variation, try all three.
        lda FrameCount
        lsr
        lsr
        eor FrameCount
        eor ScoreLo
        eor ScoreHi
        eor PlayerX
        eor PlayerY
        eor Stage
        and #3
        tay
        ldx #4
ReturnTry:
        cpy RRelease
        beq ReturnNext
        lda EdgeX,y
        sta RX
        lda EdgeY,y
        sta RY
        ; A candidate farther than 36 in either axis is safe even for L3.
        lda PlayerX
        sec
        sbc RX
        bcs ReturnAbsX
        eor #$FF
        adc #1
ReturnAbsX:
        cmp #36
        bcs RangerReturn
        lda PlayerY
        sec
        sbc RY
        bcs ReturnAbsY
        eor #$FF
        adc #1
ReturnAbsY:
        cmp #36
        bcs RangerReturn
ReturnNext:
        iny
        tya
        and #3
        tay
        dex
        bne ReturnTry
        ; Geometrically unreachable: at least two edge points are >36 away.
        lda #1
        sta RCool
AwayDone:
        rts
RangerReturn:
        lda #3
        sta RAlive
        lda #0
        sta RDraw
        sta RRelease
        lda #30
        sta RCool
        rts
EdgeX: dc.b 8,152,80,80
EdgeY: dc.b 88,88,12,158
RetreatThreshold: dc.b 0,128,128,102,102,78,78,54,54
RangerDistance:
        lda RX
        sec
        sbc PlayerX
        bcs DistX
        eor #$FF
        adc #1
DistX:
        sta ScratchMin
        lda RY
        sec
        sbc PlayerY
        bcs DistY
        eor #$FF
        adc #1
DistY:
        cmp ScratchMin
        bcc DistXMax
        sta ScratchMax
        lda ScratchMin
        lsr
        clc
        adc ScratchMax
        rts
DistXMax:
        lsr
        clc
        adc ScratchMin
        rts
RangerMoveTarget:
        lda RX
        cmp ScratchIX
        beq RangerRateOK
        lda RY
        cmp ScratchY
        beq RangerRateOK
        lda FrameCount
        and #7
        bne RangerRateOK
        rts
RangerRateOK:
        lda RX
        sta ScratchMin
        lda RY
        sta ScratchMax
        lda RX
        cmp ScratchIX
        beq RangerMoveY
        bcc RangerMoveRight
        cmp #8
        bcc RangerMoveY
        beq RangerMoveY
        dec RX
        lda RAlive
        ora #8
        sta RAlive
        jmp RangerMoveY
RangerMoveRight:
        cmp #152
        bcs RangerMoveY
        inc RX
        lda RAlive
        and #$F7
        sta RAlive
RangerMoveY:
        lda RY
        cmp ScratchY
        beq RangerMoved
        bcc RangerMoveDown
        cmp #13
        bcc RangerMoved
        dec RY
        jmp RangerMoved
RangerMoveDown:
        cmp #158
        bcs RangerMoved
        inc RY
RangerMoved:
        jmp RangerMovementCheck

RangerBlocked:
        ; All eight immutable maps have open side strips and central corridor.
        lda RX
        cmp #12
        bcc RangerFree
        cmp #148
        bcs RangerFree
        cmp #52
        bcc RangerCheckY
        cmp #96
        bcc RangerFree
RangerCheckY:
        lda RY
        clc
        adc #8
        cmp $C2
        bcc RangerFree
        lda RY
        sec
        sbc #8
        cmp $CB
        bcs RangerFree
        jmp KnightBlocked
RangerFree:
        lda #0
        rts
        ORG $FFFC
        dc.w ColdBoot
        dc.w ColdBoot
