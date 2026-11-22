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
PlayerX     = $80
PlayerY     = $81
Level       = $82
FrameCount  = $8D
SwitchState = $84
OrbMask     = $9C
ArrowCool   = $9D      ; legitimate reuse: consumed OrbTimer never read GAMEPLAY-3
HaloFrames  = $9E
TargetAlive = $A1
TargetFlash = $A2
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
ArrowDX     = $A3      ; unused old CheckDX byte, 0 or +/-1
ArrowDY     = $A4      ; unused old CheckDY byte, 0 or +/-1
KnightDir   = $A5      ; unused old HaloVisualMask storage, 0 right/8 left
HalfW       = $98
HalfH       = $99
HaloRadius  = $A0
ArrowX      = $B8
ArrowY      = $B9
EnemyRowPtr = $B6 ; $B6/B7 F8 bank1 dynamic ROM sprite table pointer
SoundFrames = $BF ; unused former BonusCount moved, preserving all collision bytes
; $B8,$B9 reused for in-flight arrow, obsolete unrendered RangerX/Y bookkeeping removed
OrbX        = $BA
OrbDirty    = $BB
BonusLo     = $BC  ; points since last 2,000-point extra life
BonusHi     = $BD
StagePause  = $BE  ; 24f real transition delay on stage clear
INPT4       = $3C

        SEG GameCode
        ORG $F000
        ds 256,0       ; explicit first-bank start for exact 4096 bytes
        ORG $F100
GameBankTick:
        lda Stage
        bne GameInitialized
        jsr InitializeGame
GameInitialized:
        lda StagePause
        beq StagePauseDone
        dec StagePause
        bne GamePauseOnly
        jsr NextStage
GamePauseOnly:
        jmp GameBankReturn
StagePauseDone:
        lda Lives
        bne Running
        jmp GameOver
Running:
        lda Invulnerable
        beq InvulnDone
        dec Invulnerable
InvulnDone:
        lda TargetAlive
        bne KnightAlive
        jsr TargetEliminated
        jmp AfterKnight
KnightAlive:
        lda StageKills
        clc
        adc #1
        cmp KillsNeed
        bne KnightOnly
        jsr RangerProxyAI
        jmp AfterKnight
KnightOnly:
        jsr KnightAI
AfterKnight:
        jsr UpdateArrow
        jsr SetWorldColors
        jsr UpdateSound
        jmp GameBankReturn

InitializeGame:
        lda #1
        sta Stage
        sta StageDir
        sta TargetAlive
        sta Level
        lda #3
        sta Lives
        lda #0
        sta ScoreLo
        sta ScoreHi
        sta StageKills
        sta EnemyRowPtr
        sta EnemyRowPtr+1
        sta BonusLo
        sta BonusHi
        sta SwordWarn
        sta SwordStrike
        sta SwordRest
        sta Invulnerable
        sta SoundFrames
        sta StagePause
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
        lda TargetFlash
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
        lda #24
        sta StagePause       ; no respawn before stage clear
        jmp TargetDeadWait
MoreTargets:
        lda #1
        sta TargetAlive
        lda #125
        sta KnightX
        lda #0
        sta SwordWarn
        sta SwordStrike
        sta SwordRest
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
        sta SwordRest
        sta ArrowCool
        sta ArrowDX
        sta ArrowDY
        sta KnightDir
        sta StagePause
        lda #2
        sta OrbMask
        lda #1
        sta TargetAlive
        lda #125
        sta KnightX
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        lda #$9E
        sta COLUP1
        lda #24
        sta SoundFrames
        lda #12
        sta AUDF0
        lda #6
        sta AUDC0
        jsr SetWaveTarget
        jsr InstallStageLayout
        jsr PlaceStageOrb
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
        sta SwordRest
        jmp KnightDone
NoStrike:
        lda SwordRest
        beq ReadyKnight
        dec SwordRest
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
        lda #1
        rts
SwordNotClose:
        lda #0
        rts

ApplySwordDamage:
        ; Never hurt player from knight body contact.
        lda #45
        sta Invulnerable
        lda #16
        sta SoundFrames
        lda #2
        sta AUDC0
        lda #8
        sta AUDF0
        lda Level
        cmp #1
        beq LoseLife
        dec Level
        rts
LoseLife:
        dec Lives
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
        lda StageOrbX,x
        sta OrbX
        lda #1
        sta OrbDirty     ; ball repositioned once OFFSCREEN by bank1
        rts

InstallStageLayout:
        lda Stage
        and #1
        beq InstallRepeat
        ldx #47
CopyMirror:
        lda MirrorRects,x
        sta $C0,x
        dex
        bpl CopyMirror
        lda #$11
        sta CTRLPF       ; mirrored obstacle layout, original PLAY1-H
        rts
InstallRepeat:
        ldx #47
CopyRepeat:
        lda RepeatRects,x
        sta $C0,x
        dex
        bpl CopyRepeat
        lda #$10
        sta CTRLPF       ; repeated obstacle layout, changed at stage boundary
        rts

SetWorldColors:
        ; Eight provisional color identities, but ONE common obstacle map.
        ; World PF must become gold under active halo (PLAY1-H test B).
        ldx Stage
        lda HaloFrames
        bne ColorHaloActive
        lda WorldPFColors,x
        sta COLUPF
ColorHaloActive:
        lda TargetFlash
        bne ColorKeepFlash
        lda WorldBGColors,x
        sta COLUBK
ColorKeepFlash:
        rts

UpdateSound:
        lda SoundFrames
        beq SoundMute
        dec SoundFrames
        lda #7
        sta AUDV0
        rts
SoundMute:
        lda #0
        sta AUDV0
        rts

GameOver:
        lda #$42
        sta COLUBK
        lda #0
        sta AUDV0
        lda SwitchState
        and #1           ; physical console RESET switch, active low
        beq RestartGame
        lda INPT4        ; physical FIRE to restart too, active low bit 7
        bmi GameOverStay
RestartGame:
        lda #0
        sta Stage        ; next tick initializes new game
GameOverStay:
        jmp GameBankReturn

WorldPFColors:
        dc.b $00,$C6,$C8,$36,$38,$56,$58,$06,$08
WorldBGColors:
        dc.b $00,$00,$00,$02,$02,$04,$04,$00,$00

; Full-body collision expanded rectangles. 3 levels, four solids, 4 bytes each.
; Mirrored copies are frozen original F01Diag_L1/L2/L3 values.
StageOrbX:
        dc.b 0,96,88,80,104,92,84,100,76

MirrorRects:
        dc.b 5,36,15,58,125,156,15,58,17,52,127,162,109,144,127,162
        dc.b 1,40,9,64,121,160,9,64,13,56,121,168,105,148,121,168
        dc.b 0,48,3,70,113,160,3,70,5,64,115,174,97,156,115,174
; Mirror bit off: right-side obstacle copies begin at x92 and x104.
RepeatRects:
        dc.b 5,36,15,58,85,116,15,58,17,52,127,162,97,132,127,162
        dc.b 1,40,9,64,81,120,9,64,13,56,121,168,93,136,121,168
        dc.b 0,48,3,70,73,128,3,70,5,64,115,174,85,144,115,174

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
        jsr LaunchArrow
        rts
RangerNotDrawing:
        lda SwordStrike
        beq RangerNotReleased
        dec SwordStrike
        bne RangerCombatDone
        lda #60
        sta SwordRest
        rts
RangerNotReleased:
        lda SwordRest
        beq RangerReady
        dec SwordRest
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
        beq ArrowDone
        lda FrameCount
        and #1
        bne ArrowDone
        lda ArrowX
        clc
        adc ArrowDX
        sta ArrowX
        cmp #10
        bcc ArrowDestroy
        cmp #151
        bcs ArrowDestroy
        lda ArrowY
        clc
        adc ArrowDY
        sta ArrowY
        cmp #48
        bcc ArrowDestroy
        cmp #176
        bcs ArrowDestroy
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
        cmp HaloRadius
        bcs TestArrowBody
        lda ArrowY
        sec
        sbc PlayerY
        bcs ArrowHaloAbsY
        eor #$FF
        clc
        adc #1
ArrowHaloAbsY:
        cmp HaloRadius
        bcc ArrowDestroy
TestArrowBody:
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
        sec
        sbc HalfW
        bcs TestArrowWalls
        lda ArrowY
        sec
        sbc PlayerY
        bcs ArrowBodyAbsY
        eor #$FF
        clc
        adc #1
ArrowBodyAbsY:
        sec
        sbc HalfH
        bcs TestArrowWalls
        jsr ApplySwordDamage  ; shared level-down / lose-life / i-frames
        jmp ArrowDestroy
TestArrowWalls:
        ; Conservative physical-world collision: actual 4 collision
        ; rectangles in $C0-$CF, L1 expanded padding. No fake pass for
        ; pixel-perfect PF wall edge; no collision-table or stack overlap.
        ldx #0
ArrowWallLoop:
        lda ArrowX
        cmp $C0,x
        bcc NextArrowWall
        cmp $C1,x
        bcs NextArrowWall
        lda ArrowY
        cmp $C2,x
        bcc NextArrowWall
        cmp $C3,x
        bcc ArrowDestroy
NextArrowWall:
        inx
        inx
        inx
        inx
        cpx #16
        bcc ArrowWallLoop
ArrowDone:
        rts
ArrowDestroy:
        lda #0
        sta ArrowDX
        sta ArrowDY
        rts

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
        ORG $FFFC
        dc.w GameBankReset
        dc.w GameBankReset
