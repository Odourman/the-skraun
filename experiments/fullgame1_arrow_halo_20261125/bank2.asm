; GAMEPLAY-5 A+C checkpoint: less overscan work, safe sword ray, invuln & stage pause.
; GAMEPLAY-4 integrated K1-T strike / R1 draw-release and M1 arrow trial.
; RIOT byte reuse documented; ROM/raster pass depends on actual Stella build.
; GAMEPLAY-3 K1-T/R1 experimental native P1, preserving GAMEPLAY-2 sequential playable loop.
; Warning/strike knight armor remains light blue; mask switching in bank1.
; GAMEPLAY-2: F8 bank0 stage-cycle/score/lives executable, from frozen GAMEPLAY-1
; GAMEPLAY-1 experimental F8 BANK 0. New gameplay state, no production claim.
; F8 bank 1 is the exact PLAY1-H visible kernel lineage.
; THIS IS NOT A THREE-VISIBLE-ENEMY RENDERER OR 8 FINAL ARENAS.
        processor 6502
COLUP1      = $07
COLUPF      = $08
COLUBK      = $09
CTRLPF      = $0A
AUDC0       = $15
AUDF0       = $17
AUDV0       = $19
AUDV1       = $1A
PlayerX     = $80
PlayerY     = $81
Level       = $82
FrameCount  = $8D
ScoreTop    = $84
SWCHB       = $0282
OrbMask     = $9C
ArrowCool   = $9D      ; legitimate reuse: consumed OrbTimer never read GAMEPLAY-3
HaloFrames  = $9E
AttackState = $9F      ; bit 7 waits at start
ArrowMajor= $A1     ; bit 7 selects Y as the major axis
ArrowMinor= $A2     ; magnitude of the minor axis
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
ArrowDX     = $A3      ; unused old CheckDX byte, 0 or +/-1
ArrowDY     = $A4      ; unused old CheckDY byte, 0 or +/-1
KnightDir   = $A5      ; unused old HaloVisualMask storage, 0 right/8 left
HalfW       = $98
HalfH       = $99
HaloRadius  = $A0
ArrowX      = $B8
ArrowY      = $B9
EnemyRowPtr = $B6 ; $B6/B7 F8 bank1 dynamic ROM sprite table pointer
WorldPFPtr  = $EC
SoundFrames = $BF ; unused former BonusCount moved, preserving all collision bytes
; $B8,$B9 reused for in-flight arrow, obsolete unrendered RangerX/Y bookkeeping removed
OrbX        = $BA
OrbDirty    = $BB
BonusLo     = $BC  ; points since last 2,000-point extra life
BonusHi     = $BD
StagePause  = $BE  ; 24f real transition delay on stage clear
ScratchY    = $EB
INPT4       = $3C

        SEG GameCode
        ORG $F000
; Active RESET uses Phase bit7, sampled only on a physical press edge.
; Phase bit6 (manual FIRE latch) and low gait bits are preserved.
ResetGate:
        lda SWCHB
        lsr
        bcc ResetPressed
        lda $86
        bpl ResetCheckStage
        and #$7F
        sta $86
        jmp ResetCheckStage
ResetPressed:
        lda $86
        bmi ResetCheckStage
        ora #$80
        sta $86
        lda #0
        sta Stage
ResetCheckStage:
        lda Stage
        bne ResetRunning
        jmp GameStartNew
ResetRunning:
        jmp GameInitialized
BudgetedSound:
        ; Multi-award, growth and projectile work can consume the last
        ; overscan lines. Leave TIA audio and both queued requests intact
        ; when there is too little time for both envelopes and the return.
        bit $0285
        bmi DeferSound
        lda $0284
        cmp #6
        bcc DeferSound
        ; TIM64T starts at 33. A higher value means TIMINT changed
        ; before the INTIM read, which can acknowledge the timeout.
        cmp #34
        bcs RearmExpiredSoundTimer
        jmp SoundBankEnter
RearmExpiredSoundTimer:
        ; Restore timeout for OverScanWait on the next timer clock.
        lda #0
        sta $0294
DeferSound:
        rts

        ds $F100-*,0
        ORG $F100
GameBankTick:
        jmp ResetGate
        nop
GameStartNew:
        jsr InitializeGame
        ; Stage-0 reset/initialization already performs two bank changes
        ; and map/actor setup. Avoid running all combat/sound work again
        ; inside the same overscan frame.
        jmp GameBankReturn
GameInitialized:
        bit AttackState
        bpl GameStarted
        jmp GameBankReturn
GameStarted:
        lda StagePause
        beq StagePauseDone
        dec StagePause
        bne GamePauseOnly
        jsr NextStage
        ; Finish this frame: first new-stage audio tick occurs next frame.
        jmp GameBankReturn
GamePauseOnly:
        ; Completed wave: no stationary projectile during the two-second clear pause.
        lda #0
        sta ArrowDX
        sta ArrowDY
        jsr SetWorldColors
        jsr UpdateSound
        jmp GameBankReturn
StagePauseDone:
        lda Lives
        bne GameRunning
        jmp GameOver
GameRunning:
        lda Invulnerable
        bmi RunRespawnFrame
        beq InvulnDone
        dec Invulnerable
InvulnDone:
        lda #0
        sta ScratchY
        jsr ActorBankEnter ; true F6 bank0 independent actor AI
        jsr UpdateArrow
        jsr SetWorldColors
        jsr UpdateSound
        jmp GameBankReturn

RunRespawnFrame:
        ; A life was lost in the preceding overscan. Reset only the
        ; surviving opponents; no AI or queued projectile can run here.
        lda #60
        sta Invulnerable
        lda #0
        sta ArrowDX
        sta ArrowDY
        sta ArrowCool
        lda #2
        sta ScratchY
        jsr ActorBankEnter
        jsr SetWorldColors
        jsr UpdateSound
        jmp GameBankReturn

InitializeGame:
        lda #1
        sta Stage
        sta StageDir
        sta Level
        lda #3
        sta Lives
        lda #0
        sta ScoreLo
        sta ScoreHi
        sta ScoreTop
        sta StageKills
        sta EnemyRowPtr
        sta EnemyRowPtr+1
        sta BonusLo
        sta BonusHi
        sta SwordWarn
        sta SwordStrike
        sta ArrowError
        sta Invulnerable
        sta SoundFrames
        sta $85
        sta StagePause
        sta HaloFrames
        sta AUDV0
        sta AUDV1
        lda #$80
        sta AttackState   ; return to FIRE prompt on cold start and RESET
        lda $86
        and #$C3          ; preserve sampled FIRE through RESET
        sta $86
        lda #0
        sta ArrowCool
        sta ArrowDX
        sta ArrowDY
        sta KnightDir
        sta ArrowX
        sta ArrowY
        lda #125
        sta KnightX
        lda #2
        sta OrbMask
        lda #0
        sta ArrowCool
        sta ArrowDX
        sta ArrowDY
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        jsr SetWaveTarget
        jsr InstallStageLayout
        jsr PlaceStageOrb
        lda #1
        sta ScratchY
        jsr ActorBankEnter
        lda #$F0          ; restart cue after actor RAM clears
        sta SoundFrames
        rts

SetWaveTarget:
        ; Diagnostic sequential dummy count = knights + ranger slot.
        ; Does NOT mean multiple physical enemies are implemented.
        lda Stage
        cmp #5
        bcc BeforeDream
        cmp #7
        bcc DreamCount
        lda #5
        sta KillsNeed
        rts
BeforeDream:
        lda #3
        sta KillsNeed
        rts
DreamCount:
        lda #4
        sta KillsNeed
        rts

TargetEliminated:
        lda ArrowMinor
        bne TargetDeadWait
        ; Two sequential 100-point P1 knight proxies, final ranger
        ; proxy of each stage awards 250. Not simultaneous opponents.
        lda StageKills
        clc
        adc #1
        cmp KillsNeed
        beq AwardRanger
        ldx #100
        jmp AwardReady
AwardRanger:
        ldx #250
AwardReady:
        txa
        clc
        adc ScoreLo
        sta ScoreLo
        lda ScoreHi
        adc #0
        sta ScoreHi
        txa
        clc
        adc BonusLo
        sta BonusLo
        lda BonusHi
        adc #0
        sta BonusHi
        lda BonusHi
        cmp #$07
        bcc NoBonus
        bne BonusEarned
        lda BonusLo
        cmp #$D0
        bcc NoBonus
BonusEarned:
        sec
        lda BonusLo
        sbc #$D0
        sta BonusLo
        lda BonusHi
        sbc #$07
        sta BonusHi
        inc Lives
NoBonus:
        inc StageKills
        lda #13
        sta SoundFrames
        lda #4
        sta AUDC0
        lda #16
        sta AUDF0
        lda StageKills
        cmp KillsNeed
        bcc MoreTargets
        lda #120         ; GAMEPLAY-5 C: ~2s stage visit transition
        sta StagePause       ; no respawn before stage clear
        jmp TargetDeadWait
MoreTargets:
        lda #1
        lda #125
        sta KnightX
        lda #0
        sta SwordWarn
        sta SwordStrike
        sta ArrowError
        lda #$9E
        sta COLUP1
TargetDeadWait:
        rts

NextStage:
        ; Pendulum 1..8..1, no difficulty escalation by cycle.
        lda StageDir
        bmi StageReverse
        lda Stage
        cmp #8
        bne StageForward
        lda #$FF
        sta StageDir
        jmp SetNewStage    ; duplicate endpoint 8, then reverse
StageForward:
        inc Stage
        jmp SetNewStage
StageReverse:
        lda Stage
        cmp #1
        bne StageBackOne
        lda #1
        sta StageDir
        jmp SetNewStage    ; duplicate endpoint 1, then forward
StageBackOne:
        dec Stage
SetNewStage:
        lda #0
        sta StageKills
        sta SwordWarn
        sta SwordStrike
        sta ArrowError
        sta ArrowCool
        sta ArrowDX
        sta ArrowDY
        sta KnightDir
        sta StagePause
        lda #2
        sta OrbMask
        lda #1
        lda #125
        sta KnightX
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        lda #$9E
        sta COLUP1
        lda #$60          ; stage transition melody
        sta SoundFrames
        jsr SetWaveTarget
        jsr InstallStageLayout
        jsr PlaceStageOrb
        lda #1
        sta ScratchY
        jsr ActorBankEnter
        rts

RangerProxyAI:
        jmp RangerCombat     ; real Ranger draw/release/arrow offscreen logic, sequential P1

KnightAI:
        ; Single P1 training knight X chase; Y remains static at arena 96.
        ; Sword is logical, warning indicated by changing P1 color.
        lda SwordWarn
        beq NoWarning
        dec SwordWarn
        lda #$9E
        sta COLUP1
        lda SwordWarn
        bne KnightDone
        lda #7
        sta SwordStrike
        jmp KnightDone
NoWarning:
        lda SwordStrike
        beq NoStrike
        dec SwordStrike
        lda #$9E
        sta COLUP1
        jsr CloseForSword
        beq StrikeFinished
        lda Invulnerable
        bne StrikeFinished
        jsr ApplySwordDamage
StrikeFinished:
        lda SwordStrike
        bne KnightDone
        lda #60
        sta ArrowError
        jmp KnightDone
NoStrike:
        lda ArrowError
        beq ReadyKnight
        dec ArrowError
        lda #$9E
        sta COLUP1
        jmp KnightDone
ReadyKnight:
        lda #$9E
        sta COLUP1
        jsr CloseForSword
        beq ChaseKnight
        lda #24
        sta SwordWarn
        ; Hold facing for entire warning and active strike, prevent mid-swing flip.
        lda KnightX
        cmp PlayerX
        bcc LockSwordRight
        lda #8
        sta KnightDir
        jmp KnightDone
LockSwordRight:
        lda #0
        sta KnightDir
        jmp KnightDone
ChaseKnight:
        lda FrameCount
        and #3
        bne KnightDone
        lda KnightX
        cmp PlayerX
        beq KnightDone
        bcc KnightChaseRight
        cmp #31
        bcc KnightDone
        dec KnightX
        jmp KnightDone
KnightChaseRight:
        cmp #145
        bcs KnightDone
        inc KnightX
KnightDone:
        rts

CloseForSword:
        lda PlayerX
        sec
        sbc KnightX
        bcs SwordAbsX
        eor #$FF
        clc
        adc #1
SwordAbsX:
        cmp #14
        bcs SwordNotClose
        lda PlayerY
        sec
        sbc #96
        bcs SwordAbsY
        eor #$FF
        clc
        adc #1
SwordAbsY:
        cmp #20
        bcs SwordNotClose
        ; Only active strike has a directional hitbox.
        lda SwordStrike
        beq SwordCloseOK  ; warning trigger only, never deals damage
        lda KnightDir
        bne CheckSwordLeft
        lda PlayerX
        cmp KnightX
        bcc SwordNotClose
        jmp SwordCloseOK
CheckSwordLeft:
        lda PlayerX
        cmp KnightX
        bcs SwordNotClose
SwordCloseOK:
        ; GAMEPLAY-5 C: no sword THROUGH any real solid rectangle.
        ; Warning remains proximity-only; damage only active strike + unobstructed.
        lda SwordStrike
        beq SwordClear
        jsr SwordLineClear
        beq SwordNotClose
SwordClear:
        lda #1
        rts
SwordNotClose:
        lda #0
        rts

ApplySwordDamage:
        ; Never hurt player from knight body contact.
        lda #60          ; GAMEPLAY-5 C: ~1s real invulnerability
        sta Invulnerable
        lda #$C0
        cmp $85
        bcc DamageAlreadyQueued
        sta $85
DamageAlreadyQueued:
        lda Level
        cmp #1
        beq LoseLife
        dec Level
        rts
LoseLife:
        dec Lives
        bne ExtraLifeStillHere
        lda #$E0
        sta $85
ExtraLifeStillHere:
        lda #$BC
        sta Invulnerable
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        rts

; The old unrendered RangerFleeDiagnostic was removed: B8/B9 are now
; independently positioned projectile X/Y; actual Ranger stays on P1 KnightX.

; Two *intentionally distinct provisional layouts* at stage boundaries.
; Unlike rejected PLAY1-H mirror hack, this is not an X-halo trick:
; we switch geometry together with its exact collision tables.
PlaceStageOrb:
        ldx Stage
        ; Fold visit time and score so regular pendulum play is not
        ; tied to one low-order frame-clock bit.
        lda FrameCount
        lsr
        lsr
        eor FrameCount
        eor ScoreHi
        eor ScoreLo
        eor StageDir
        and #1
        beq OrbPlaceLeft
        lda StageOrbRightX,x
        bne OrbPlaceChosen
OrbPlaceLeft:
        lda StageOrbX,x
OrbPlaceChosen:
        sta OrbX
        lda #1
        sta OrbDirty     ; ball repositioned once OFFSCREEN by bank1
        rts

InstallStageLayout:
        lda Stage
        and #1
        beq InstallRepeat
        ldx #15
CopyMirror:
        lda MirrorRects,x
        sta $C0,x
        dex
        bpl CopyMirror
        lda #$11
        sta CTRLPF       ; mirrored obstacle layout, original PLAY1-H
        rts
InstallRepeat:
        ldx #15
CopyRepeat:
        lda RepeatRects,x
        sta $C0,x
        dex
        bpl CopyRepeat
        lda #$10
        sta CTRLPF       ; repeated obstacle layout, changed at stage boundary
        rts

SetWorldColors:
        ; HEALTH-001: persist 1-based Stage REF when updating ball size.
        ; HEALTH-002 CORRECTED: D4/D5 = 00:1, 10:2, 20:4, 30:8 clocks.
        lda Stage
        and #1
        ora #$10
        sta CTRLPF
        ldx Stage
        lda WorldPFColors,x
        sta COLUPF
ColorHaloActive:
        lda WorldBGColors,x
        sta COLUBK
ColorKeepFlash:
        rts

UpdateSound:
        jmp BudgetedSound

GameOver:
        jmp GameOverImpl

WorldPFColors:
        dc.b $00,$C6,$C8,$86,$88,$66,$68,$82,$84
WorldBGColors:
        dc.b $00,$00,$00,$02,$02,$00,$00,$00,$00
HaloBLWidths:
        dc.b $00,$10,$20,$30 ; index 0 unused, L1=2 L2=4 L3=8 color clocks

; Full-body collision expanded rectangles. 3 levels, four solids, 4 bytes each.
; Mirrored copies are frozen original F01Diag_L1/L2/L3 values.
StageOrbX:
        dc.b 0,22,22,22,22,22,22,22,22
StageOrbRightX:
        dc.b 0,138,138,138,138,138,138,138,138

MirrorRects:
        dc.b 9,32,21,52,129,152,21,52,21,48,133,156,113,140,133,156
RepeatRects:
        dc.b 9,32,21,52,89,112,21,52,21,48,133,156,101,128,133,156

        ORG $F480
; GAMEPLAY-4 actual R1 draw/release phases, not three-enemy kernel.
RangerCombat:
        ldx Stage
        lda WorldPFColors,x
        sta COLUP1          ; world-green Ranger, distinct from blue K1-T
        lda SwordWarn
        beq RangerNotDrawing
        dec SwordWarn
        bne RangerCombatDone
        lda #8
        sta SwordStrike
        jsr LaunchArrow      ; physical M1 shot on bow release
        lda #9
        sta SoundFrames
        lda #12
        sta AUDC0
        lda #20
        sta AUDF0
        rts
RangerNotDrawing:
        lda SwordStrike
        beq RangerNotReleased
        dec SwordStrike
        bne RangerCombatDone
        lda #60
        sta ArrowError
        rts
RangerNotReleased:
        lda ArrowError
        beq RangerReady
        dec ArrowError
        rts
RangerReady:
        lda ArrowCool
        bne RangerFlee
        lda ArrowDX
        bne RangerFlee
        lda #24            ; 0.4s draw, exact R1 draw source mask
        sta SwordWarn
        rts
RangerFlee:
        lda FrameCount
        and #7
        bne RangerCombatDone
        lda KnightX
        cmp PlayerX
        bcs RangerFleeRight
        cmp #26
        bcc RangerCombatDone
        dec KnightX
        rts
RangerFleeRight:
        cmp #134
        bcs RangerCombatDone
        inc KnightX
RangerCombatDone:
        rts

; Sample player X/Y ONCE on bow release. Arrow has fixed 8-way direction.
LaunchArrow:
        lda ArrowDX
        bne NoArrowSpawn    ; invariant: one M1 arrow maximum
        lda KnightX
        sta ArrowX
        lda #96
        sta ArrowY
        lda PlayerX
        cmp KnightX
        bcc LaunchLeft
        lda #1
        sta ArrowDX
        jmp LaunchVertical
LaunchLeft:
        lda #$FF
        sta ArrowDX
LaunchVertical:
        lda #0
        sta ArrowDY
        lda PlayerY
        cmp #91
        bcc LaunchUp
        cmp #101
        bcc LaunchReady
        lda #1
        sta ArrowDY
        jmp LaunchReady
LaunchUp:
        lda #$FF
        sta ArrowDY
LaunchReady:
        lda #180
        sta ArrowCool     ; cooldown begins at actual release, not at draw
NoArrowSpawn:
        rts

; Active projectile update in overscan, never retargets after firing.
UpdateArrow:
        lda ArrowCool
        beq ArrowCooldownDone
        dec ArrowCool
ArrowCooldownDone:
        lda ArrowDX
        bne ArrowIsActive
        rts
ArrowIsActive:
        lda $86
        and #3
        bne ArrowMoveThisFrame
        rts
ArrowMoveThisFrame:
        jsr StepArrow
        lda ArrowX
        cmp #10
        bcs ArrowMinXOK
        jmp ArrowDestroy
ArrowMinXOK:
        cmp #151
        bcc ArrowMaxXOK
ArrowBoundaryDestroy:
        jmp ArrowDestroy
ArrowMaxXOK:
        lda ArrowY
        cmp #6  ; upper arena margin, within the M1 row table guard
        bcc ArrowBoundaryDestroy
        cmp #176
        bcs ArrowBoundaryDestroy
        ; Halo intercepts projectile even through solids; checked first.
        lda HaloFrames
        beq TestArrowBody
        lda ArrowX
        sec
        sbc PlayerX
        bcs ArrowHaloAbsX
        eor #$FF
        clc
        adc #1
ArrowHaloAbsX:
        sta $E9
        lda ArrowY
        sec
        sbc PlayerY
        bcs ArrowHaloAbsY
        eor #$FF
        clc
        adc #1
ArrowHaloAbsY:
        tay
        lda $E9
        jsr OctagonOutside
        bcc ArrowDestroy
TestArrowBody:
        lda ArrowCool
        bne TestArrowWalls
        lda Invulnerable
        bne TestArrowWalls
        lda ArrowX
        sec
        sbc PlayerX
        bcs ArrowBodyAbsX
        eor #$FF
        clc
        adc #1
ArrowBodyAbsX:
        ldy Level
        cmp ArrowCoreHalfW,y
        bcs TestArrowWalls
        lda ArrowY
        sec
        sbc PlayerY
        bcs ArrowBodyAbsY
        eor #$FF
        clc
        adc #1
ArrowBodyAbsY:
        cmp ArrowCoreHalfH,y
        bcs TestArrowWalls
AcceptArrowDamage:
        jsr ApplySwordDamage  ; shared level-down / lose-life / i-frames
        jmp ArrowDestroy
TestArrowWalls:
        ; Two nonoverlapping vertical bands, with independent horizontal pairs.
        ldx #0
        lda ArrowY
        cmp $C2
        bcc ArrowDone
        cmp $C3
        bcc ArrowWallBand
        cmp $CA
        bcc ArrowDone
        cmp $CB
        bcs ArrowDone
        ldx #8
ArrowWallBand:
        lda ArrowX
        cmp $C0,x
        bcc ArrowDone
        cmp $C1,x
        bcc ArrowDestroy
        cmp $C4,x
        bcc ArrowDone
        cmp $C5,x
        bcc ArrowDestroy
ArrowDone:
        rts
ArrowDestroy:
        lda #$90          ; projectile hits world/halo/player/edge
        cmp SoundFrames
        bcc ArrowSoundHigherPriority
        sta SoundFrames
ArrowSoundHigherPriority:
        lda #0
        sta ArrowDX
        sta ArrowDY
        rts

        ; Solid central torso, independent of the full movement box.
ArrowCoreHalfW:
        dc.b 0,4,7,13
ArrowCoreHalfH:
        dc.b 0,6,9,13

        ; Exact corresponding shared-address bank trampolines.
        ORG $F680
GameBankEnter:
        lda $FFF8
        jmp GameBankTick
        ORG $F690
GameBankReturn:
        lda $FFF9
        rts
        ORG $F6A0
GameBankReset:
        lda $FFF9
        jmp $F000

        ; F6 independent bank0 call. Following JMP fetched after switch
        ; at same PC in bank0 ($F6C3); bank2 owns the return RTS at $F6D3.
        ORG $F6C0
ActorBankEnter:
        lda $FFF6
        ORG $F6D3
ActorBankReturn:
        rts

        ORG $F6E0
SoundBankEnter:
        lda $FFF7
        ORG $F6ED
SoundBankReturn:
        rts
        ORG $F700
; GAMEPLAY-5 C: exact 48-byte RIOT per-level rectangle gate.
; With current sequential training P1 Y=96 most obstacles do not cross its
; row, but the logic is directional and handles future art/actor Y properly.
; Source truth: only this physical stage's expanded solid cache is inspected.
; Live-range: TryX $90 (min endpoint), TryY $91 (max endpoint) are safe
; after visible frame VBLANK movement has finished, never during CandidateValid.
SwordLineClear:
        lda KnightX
        cmp PlayerX
        bcc SwordOrderA
        sta $91
        lda PlayerX
        sta $90
        jmp SwordStartRects
SwordOrderA:
        sta $90
        lda PlayerX
        sta $91
SwordStartRects:
        ldx #0
SwordRectLoop:
        lda #96          ; frozen current diagnostic P1 centre Y
        cmp $C2,x        ; rect min Y inclusive
        bcc SwordNextRect
        cmp $C3,x        ; rect max Y exclusive
        bcs SwordNextRect
        lda $90          ; min(KnightX, PlayerX)
        cmp $C1,x        ; rect max X exclusive
        bcs SwordNextRect
        lda $91          ; max(KnightX, PlayerX)
        cmp $C0,x        ; rect min X inclusive
        bcc SwordNextRect
        lda #0          ; real solid wall intersects the sword ray
        rts
SwordNextRect:
        txa
        and #$0F
        cmp #12
        beq SwordRayOpen
        inx
        inx
        inx
        inx
        jmp SwordRectLoop
SwordRayOpen:
        lda #1
        rts


; Shared octagonal radial metric: maximum of |dx|,|dy| + half minimum.
; Input A=unsigned |dx| and Y=unsigned |dy|. Output Carry=1 OUTSIDE,
; Carry=0 INSIDE. X is preserved; scratch E9/EA lives only during call.
OctagonOutside:
        sta $E9
        tya
        ldy Level
        cmp AuraHitHalfH,y
        bcs AuraHitOutside
        clc
        adc AuraHitOffset,y
        tay
        lda $E9
        cmp AuraHitWidths,y
        rts
AuraHitOutside:
        sec
        rts
        ORG $F780
GameOverImpl:
        lda #0
        sta HaloFrames
        sta AttackState
        sta ArrowDX
        sta OrbMask
        lda #200
        sta $E8          ; suppress stale P1 even before the dedicated screen
        lda #$10
        sta $05          ; do not keep a pair or duplicated missile
        sta CTRLPF       ; no mirror for the END banner
        lda #$0E
        sta COLUPF
        lda #0
        sta COLUBK
        jsr UpdateSound
        jmp GameBankReturn

        ORG $F840
StepArrow:
        lda ArrowMajor
        and #$7F
        sta $EB            ; actor-bank mailbox is dead after ActorBankEnter
        lda ArrowError
        clc
        adc ArrowMinor
        cmp $EB
        bcc ArrowMajorOnly
        sbc $EB
        sta ArrowError
        lda ArrowY
        clc
        adc ArrowDY
        sta ArrowY
        jmp AdvanceArrowX
ArrowMajorOnly:
        sta ArrowError
        bit ArrowMajor
        bpl AdvanceArrowX
        lda ArrowY
        clc
        adc ArrowDY
        sta ArrowY
        rts
AdvanceArrowX:
        lda ArrowX
        clc
        adc ArrowDX
        sta ArrowX
        rts

AuraHitHalfH: dc.b 0,12,20,30
AuraHitOffset: dc.b 0,0,12,32
AuraHitWidths:
        dc.b $08,$08,$08,$08,$08,$08,$06,$06,$06,$06,$04,$04,$10,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$10,$0C,$0C,$0C,$0C,$0C,$0C,$08,$08,$04,$04
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$1C,$1C,$1C,$1C,$1C,$1C
        dc.b $1C,$1C,$18,$18,$18,$18,$14,$14,$10,$10,$0C,$0C,$08,$08

        ORG $FFFC
        dc.w GameBankReset
        dc.w GameBankReset
