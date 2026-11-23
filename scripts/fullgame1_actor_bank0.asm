; FULLGAME-1 F6 bank0: independent logical K1/K2/Ranger for experimental play.
; THIS IS A DEVELOPMENT CANDIDATE. All three share a phase-multiplexed P1
; and currently display on one fixed Y-band. No claim of full game/3 sprites.
        processor 6502
COLUP1    = $07
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
TargetAlive=$A1
ArrowDX   = $A3
ArrowDY   = $A4
KnightDir = $A5
Stage     = $AA
Lives     = $AC
ScoreLo   = $AD
ScoreHi   = $AE
KnightX   = $AF
SwordWarn = $B0
SwordStrike=$B1
SwordRest = $B2
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
ScratchIX = $E8
ScratchMin=$E9
ScratchMax=$EA
ScratchY  = $EB
AuxMode   = $EF
        SEG GameAux
        ORG $F000
ColdBoot:
        lda $FFF9
        jmp $F000
        ORG $F100
ActorEntry:
        lda AuxMode
        beq ActorsRunning
        jsr ActorInitialize
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
        lda #81
        sta RX
        lda #96
        sta RY
        lda #1
        sta RAlive
        lda KillsNeed
        sec
        sbc #3
        sta Reserves
        lda #0
        sta NextSlot
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
        lda #7
        sta K1Strike,x
KnightReturn:
        rts
KnightTryStrike:
        lda K1Strike,x
        beq KnightTryRest
        dec K1Strike,x
        jsr KnightCanHit
        beq NoKnightHit
        jsr DamagePlayer
NoKnightHit:
        lda K1Strike,x
        bne KnightReturn
        lda #60
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
        lda #24
        sta K1Warn,x
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
        lda FrameCount
        and #3
        bne KnightReturn
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
        lda K1Y,x
        cmp PlayerY
        beq KnightReturn
        bcc KnightMoveDown
        cmp #34
        bcc KnightReturn
        dec K1Y,x
        rts
KnightMoveDown:
        cmp #155
        bcs KnightReturn
        inc K1Y,x
        rts

KnightInRange:
        lda PlayerX
        sec
        sbc K1X,x
        bcs KnightAbsX
        eor #$FF
        clc
        adc #1
KnightAbsX:
        cmp #15
        bcs KnightOut
        lda PlayerY
        sec
        sbc K1Y,x
        bcs KnightAbsY
        eor #$FF
        clc
        adc #1
KnightAbsY:
        cmp #21
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
        cmp HaloRadius
        bcs KnightOut
        lda PlayerY
        sec
        sbc K1Y,x
        bcs HaloKnightYAbs
        eor #$FF
        clc
        adc #1
HaloKnightYAbs:
        cmp HaloRadius
        bcs KnightOut
        lda #1
        rts

KnightCanHit:
        lda Invuln
        bne KnightOut
        jsr KnightInRange
        beq KnightOut
        lda K1Facing,x
        bne SwordFacesLeft
        lda PlayerX
        cmp K1X,x
        bcc KnightOut
        jmp SwordTestObstacles
SwordFacesLeft:
        lda PlayerX
        cmp K1X,x
        bcs KnightOut
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
        lda #15
        sta SoundFrames
        lda #2
        sta AUDC0
        lda #8
        sta AUDF0
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
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        rts

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
        bne RangerExists
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
        cmp HaloRadius
        bcs RangerTimers
        lda PlayerY
        sec
        sbc RY
        bcs RangerAbsY
        eor #$FF
        clc
        adc #1
RangerAbsY:
        cmp HaloRadius
        bcs RangerTimers
        lda #0
        sta RAlive
        jmp AwardRanger
RangerTimers:
        lda RDraw
        beq RangerTryRelease
        dec RDraw
        bne RangerDone
        jsr SpawnArrow
        lda #8
        sta RRelease
RangerDone:
        rts
RangerTryRelease:
        lda RRelease
        beq RangerTryCool
        dec RRelease
        rts
RangerTryCool:
        lda RCool
        beq RangerReady
        dec RCool
        jmp RangerFlee
RangerReady:
        lda ArrowDX
        bne RangerFlee
        lda #24
        sta RDraw
        rts
RangerFlee:
        lda FrameCount
        and #7
        bne RangerDone
        lda RX
        cmp PlayerX
        bcs RangerStepRight
        cmp #23
        bcc RangerDone
        dec RX
        jmp RangerStepY
RangerStepRight:
        cmp #145
        bcs RangerStepY
        inc RX
RangerStepY:
        lda RY
        cmp PlayerY
        bcs RangerStepUp
        cmp #145
        bcs RangerDone
        inc RY
        rts
RangerStepUp:
        cmp #35
        bcc RangerDone
        dec RY
        rts

SpawnArrow:
        lda ArrowDX
        bne SpawnDone
        lda RX
        sta ArrowX
        lda RY
        sta ArrowY
        lda PlayerX
        cmp RX
        bcc ArrowLeft
        lda #1
        sta ArrowDX
        jmp ArrowYVector
ArrowLeft:
        lda #$FF
        sta ArrowDX
ArrowYVector:
        lda #0
        sta ArrowDY
        lda PlayerY
        cmp RY
        beq ArrowCooldownSet
        bcc ArrowUp
        lda #1
        sta ArrowDY
        jmp ArrowCooldownSet
ArrowUp:
        lda #$FF
        sta ArrowDY
ArrowCooldownSet:
        ldx Stage
        lda RangerCooldowns,x
        sta RCool
        lda #9
        sta SoundFrames
        lda #12
        sta AUDC0
        lda #20
        sta AUDF0
SpawnDone:
        rts

ReserveTick:
        lda Reserves
        beq ReserveDone
        lda ResWait
        beq ReserveEligible
        dec ResWait
        rts
ReserveEligible:
        lda K1Alive
        beq Respawn1
        lda K2Alive
        bne ReserveDone
        lda #1
        sta K2Alive
        lda #145
        sta K2X
        lda #86
        sta K2Y
        lda #0
        sta K2Warn
        sta K2Strike
        sta K2Rest
        jmp ReserveCreated
Respawn1:
        lda #1
        sta K1Alive
        lda #20
        sta K1X
        lda #108
        sta K1Y
        lda #0
        sta K1Warn
        sta K1Strike
        sta K1Rest
ReserveCreated:
        dec Reserves
        lda #120
        sta ResWait
ReserveDone:
        rts

ChooseP1:
        lda NextSlot
        clc
        adc #1
        cmp #3
        bcc SelectedIndex
        lda #0
SelectedIndex:
        sta NextSlot
        sta DrawSlot
        cmp #1
        beq ChooseK2
        cmp #2
        beq ChooseRanger
ChooseK1:
        lda K1X
        sta KnightX
        lda K1Alive
        sta TargetAlive
        lda K1Warn
        sta SwordWarn
        lda K1Strike
        sta SwordStrike
        lda K1Rest
        sta SwordRest
        lda K1Facing
        sta KnightDir
        lda #$9E
        sta COLUP1
        rts
ChooseK2:
        lda K2X
        sta KnightX
        lda K2Alive
        sta TargetAlive
        lda K2Warn
        sta SwordWarn
        lda K2Strike
        sta SwordStrike
        lda K2Rest
        sta SwordRest
        lda K2Facing
        sta KnightDir
        lda #$9E
        sta COLUP1
        rts
ChooseRanger:
        lda RX
        sta KnightX
        lda RAlive
        sta TargetAlive
        lda RDraw
        sta SwordWarn
        lda RRelease
        sta SwordStrike
        lda RCool
        sta SwordRest
        lda #0
        sta KnightDir
        ldx Stage
        lda RangerColors,x
        sta COLUP1
        rts

AwardKnight:
        ldx #100
        jmp AwardAny
AwardRanger:
        ldx #250
AwardAny:
        stx ScratchIX
        txa
        clc
        adc ScoreLo
        sta ScoreLo
        lda ScoreHi
        adc #0
        sta ScoreHi
        lda ScratchIX
        clc
        adc BonusLo
        sta BonusLo
        lda BonusHi
        adc #0
        sta BonusHi
        lda BonusHi
        cmp #$07
        bcc NoExtraLife
        bne ExtraLife
        lda BonusLo
        cmp #$D0
        bcc NoExtraLife
ExtraLife:
        sec
        lda BonusLo
        sbc #$D0
        sta BonusLo
        lda BonusHi
        sbc #$07
        sta BonusHi
        lda Lives
        cmp #9
        bcs NoExtraLife
        inc Lives
NoExtraLife:
        inc StageKills
        lda #13
        sta SoundFrames
        lda #4
        sta AUDC0
        lda #16
        sta AUDF0
        lda StageKills
        cmp KillsNeed
        bcc AwardDone
        lda #120
        sta StagePause
AwardDone:
        rts

RangerColors:
        dc.b $00,$C6,$C8,$36,$38,$56,$58,$06,$08
RangerCooldowns:
        dc.b 0,180,180,150,150,120,120,90,90
        ORG $FFFC
        dc.w ColdBoot
        dc.w ColdBoot
