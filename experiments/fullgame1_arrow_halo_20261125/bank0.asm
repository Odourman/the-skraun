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
        ORG $F100
ActorEntry:
        lda ScratchY
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
        lda #140       ; Ranger enters away from P0, no point-blank arrow
        sta RX
        lda #88        ; accessible open center-right corridor in all 8 worlds
        sta RY
        lda #1
        sta RAlive
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
        lda #7
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
        lda FrameCount
        and #3
        bne KnightReturn
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
        lda K1Y,x
        cmp PlayerY
        beq KnightMovementCheck
        bcc KnightMoveDown
        cmp #34
        bcc KnightMovementCheck
        dec K1Y,x
        jmp KnightMovementCheck
KnightMoveDown:
        cmp #155
        bcs KnightMovementCheck
        inc K1Y,x
KnightMovementCheck:
        ; Prefer full diagonal step; else X-only; else Y-only.
        ; These are actual logical actor positions used by combat and shots.
        jsr KnightBlocked
        beq KnightMovementDone
        lda K1Y,x
        sta ScratchY
        lda ScratchMax
        sta K1Y,x
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

KnightBlocked:
        ; Test a conservatively bounded 8x16 real P1 sprite against the
        ; current four *unexpanded* world rectangles C0..CF. X is actor
        ; record offset (0 for K1, 7 for K2); Y scans obstacle records.
        ldy #0
KnightBlockRect:
        lda K1X,x
        clc
        adc #4
        cmp $C0,y
        bcc KnightBlockNext
        lda K1X,x
        sec
        sbc #4
        cmp $C1,y
        bcs KnightBlockNext
        lda K1Y,x
        clc
        adc #8
        cmp $C2,y
        bcc KnightBlockNext
        lda K1Y,x
        sec
        sbc #8
        cmp $C3,y
        bcs KnightBlockNext
        lda #1
        rts
KnightBlockNext:
        tya
        clc
        adc #4
        tay
        cpy #16
        bcc KnightBlockRect
        lda #0
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
        lda #$70
        jsr QueueSound
        rts
RangerFlee:
        lda FrameCount
        and #7
        bne RangerDone
        lda RX
        sta ScratchMin
        lda RY
        sta ScratchMax
        lda RX
        cmp PlayerX
        bcs RangerStepRight
        cmp #23
        bcc RangerStepY
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
        bcs RangerMovementCheck
        inc RY
        jmp RangerMovementCheck
RangerStepUp:
        cmp #35
        bcc RangerMovementCheck
        dec RY
RangerMovementCheck:
        ; Ranger center occupies the same bounded 8x16 sprite as
        ; knights. Reuse the real four-rectangle solid tester at +14.
        ldx #14
        jsr KnightBlocked
        beq RangerMovementDone
        lda RY
        sta ScratchY
        lda ScratchMax
        sta RY
        jsr KnightBlocked
        beq RangerMovementDone
        lda ScratchMin
        sta RX
        lda ScratchY
        sta RY
        jsr KnightBlocked
        beq RangerMovementDone
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
        ; Reserve appears ~120 NTSC frames *after* a knight slot
        ; becomes vacant. A full wave never respawns already killed
        ; knights: Reserves is the exact remaining unseen quota.
        lda K1Alive
        beq ReserveSlotOpen
        lda K2Alive
        bne ReserveOccupied
ReserveSlotOpen:
        lda ResWait
        bne ReserveCountdown
        lda #120
        sta ResWait
        rts
ReserveCountdown:
        dec ResWait
        bne ReserveDone
        lda K1Alive
        beq Respawn1
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
        jsr AdaptiveSelect
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
        lda #169
        sec
        sbc K1Y
        sta EnemyBottom
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
        lda #169
        sec
        sbc K2Y
        sta EnemyBottom
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
        lda #169
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
        ; Packed BCD scoreboard 0000..9999; knight +100, Ranger +250.
        cpx #100
        bne ScoreAdd250
        sed
        clc
        lda ScoreHi
        adc #$01
        sta ScoreHi
        cld
        jmp ScoreIncreaseDone
ScoreAdd250:
        sed
        clc
        lda ScoreLo
        adc #$50
        sta ScoreLo
        lda ScoreHi
        adc #$02
        sta ScoreHi
        cld
ScoreIncreaseDone:
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
        lda #$D0
        jsr QueueSound
NoExtraLife:
        inc StageKills
        lda StageKills
        cmp KillsNeed
        bcc AwardDone
        lda #120
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
        dc.b $00,$C6,$C8,$36,$38,$56,$58,$06,$08
RangerCooldowns:
        dc.b 0,180,180,150,150,120,120,90,90

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
        dc.b $0A,$1F,$18,$32,$80,$97,$18,$32,$0E,$27,$87,$A1,$7A,$94,$87,$A1 ; world 1
        dc.b $0A,$22,$1C,$3D,$7B,$94,$14,$31,$0F,$2A,$86,$9E,$7C,$97,$89,$A2 ; world 2
        dc.b $08,$24,$15,$37,$7F,$99,$1A,$3A,$0A,$27,$87,$A5,$7F,$98,$8A,$A4 ; world 3
        dc.b $09,$22,$19,$3B,$7C,$99,$1A,$3F,$0B,$23,$83,$A5,$7F,$99,$88,$A0 ; world 4
        dc.b $09,$1E,$16,$37,$81,$97,$1B,$3D,$0C,$25,$87,$A5,$7B,$97,$8A,$A5 ; world 5
        dc.b $0A,$27,$18,$3B,$7D,$99,$16,$36,$0A,$21,$8A,$A1,$80,$98,$87,$A2 ; world 6
        dc.b $09,$23,$18,$3E,$80,$97,$16,$38,$0C,$27,$87,$A5,$7F,$97,$87,$A5 ; world 7
        dc.b $0A,$23,$1D,$37,$82,$99,$19,$3D,$0F,$28,$88,$A5,$7A,$94,$84,$A2 ; world 8

        ORG $FA40
; Adaptive display-only scheduler. Runs once per game frame in blanking.
; Priority: active sword > 24f telegraph > Ranger bow pose > live actors.
; Fast 3/4-frame lock for a single threat, 1/4 fair other actors.
; Dual sword priorities alternate K1/K2; every fourth frame selects a
; live Ranger, avoiding complete bow starvation during 24-frame warnings. The attack hit guard checks the previously
; displayed DrawSlot; invisible sword hits remain blocked.
; No extra per-line TIA work, no three-physical-P1-sprite claim.
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
        lda FrameCount
        and #3
        cmp #3
        bne ASBothKnight
        lda RAlive
        bne ASPickRanger
ASBothKnight:
        lda FrameCount
        and #1
        rts
ASMajority:
        lda FrameCount
        and #3
        bne ASReturnHigh
        ; On every fourth frame deliberately give an *other* living
        ; character the turn, so a 24-frame telegraph has >=18 frames
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

        ORG $FFFC
        dc.w ColdBoot
        dc.w ColdBoot
