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
OrbTimer    = $9D
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
BonusCount  = $B6
SoundFrames = $B7
RangerX     = $B8
RangerY     = $B9

        SEG GameCode
        ORG $F000
        ds 256,0       ; explicit first-bank start for exact 4096 bytes
        ORG $F100
GameBankTick:
        lda Stage
        bne GameInitialized
        jsr InitializeGame
GameInitialized:
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
        jsr KnightAI
AfterKnight:
        jsr RangerFleeDiagnostic
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
        sta BonusCount
        sta SwordWarn
        sta SwordStrike
        sta SwordRest
        sta Invulnerable
        sta SoundFrames
        lda #125
        sta KnightX
        lda #145
        sta RangerX
        lda #64
        sta RangerY
        lda #2
        sta OrbMask
        lda #0
        sta OrbTimer
        lda #80
        sta PlayerX
        lda #88
        sta PlayerY
        jsr SetWaveTarget
        jsr InstallStageLayout
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
        ; One original P1 target physically killed by existing halo logic.
        ; 100 pts per diagnostic knight, ranger award NOT implemented.
        clc
        lda ScoreLo
        adc #100
        sta ScoreLo
        lda ScoreHi
        adc #0
        sta ScoreHi
        inc StageKills
        inc BonusCount
        lda BonusCount
        cmp #20
        bne NoBonus
        lda #0
        sta BonusCount
        inc Lives
NoBonus:
        lda #13
        sta SoundFrames
        lda #4
        sta AUDC0
        lda #16
        sta AUDF0
        lda StageKills
        cmp KillsNeed
        bcc MoreTargets
        jsr NextStage
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
        dec Stage
        jmp SetNewStage
StageForward:
        inc Stage
        jmp SetNewStage
StageReverse:
        lda Stage
        cmp #1
        bne StageBackOne
        lda #1
        sta StageDir
        inc Stage
        jmp SetNewStage
StageBackOne:
        dec Stage
SetNewStage:
        lda #0
        sta StageKills
        sta SwordWarn
        sta SwordStrike
        sta SwordRest
        sta OrbTimer
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
        lda #145
        sta RangerX
        lda #64
        sta RangerY
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
        rts

KnightAI:
        ; Single P1 training knight X chase; Y remains static at arena 96.
        ; Sword is logical, warning indicated by changing P1 color.
        lda SwordWarn
        beq NoWarning
        dec SwordWarn
        lda #$2E
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
        lda #$4E
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

RangerFleeDiagnostic:
        ; Position bookkeeping only: NO ranger sprite, arrow or damage.
        ; Not counted as physically realized ranger behavior.
        lda FrameCount
        and #7
        bne RangerDone
        lda RangerX
        cmp PlayerX
        bcs RangerRight
        cmp #18
        bcc RangerDone
        dec RangerX
        rts
RangerRight:
        cmp #142
        bcs RangerDone
        inc RangerX
RangerDone:
        rts

; Two *intentionally distinct provisional layouts* at stage boundaries.
; Unlike rejected PLAY1-H mirror hack, this is not an X-halo trick:
; we switch geometry together with its exact collision tables.
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
        bne GameOverStay
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
MirrorRects:
        dc.b 5,36,15,58,125,156,15,58,17,52,127,162,109,144,127,162
        dc.b 1,40,9,64,121,160,9,64,13,56,121,168,105,148,121,168
        dc.b 0,48,3,70,113,160,3,70,5,64,115,174,97,156,115,174
; Mirror bit off: right-side obstacle copies begin at x92 and x104.
RepeatRects:
        dc.b 5,36,15,58,85,116,15,58,17,52,127,162,97,132,127,162
        dc.b 1,40,9,64,81,120,9,64,13,56,121,168,93,136,121,168
        dc.b 0,48,3,70,73,128,3,70,5,64,115,174,85,144,115,174

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
