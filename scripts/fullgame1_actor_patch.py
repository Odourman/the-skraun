"""FULLGAME-1 experimental F6 3-actor logic integration.
Core mandates independent K1/K2/Ranger; P1 shown by temporal slot only,
and Y remains visually fixed pending physically-budgeted renderer.
NOT release-ready. Source-only intent until real Stella gameplay proof.
"""
def once(s,a,b,name):
    n=s.count(a)
    if n!=1: raise ValueError(f"{name}: anchor count={n}")
    return s.replace(a,b,1)

def actors_bank2(s):
    s=once(s, "INPT4       = $3C", "AuxMode     = $EF\nINPT4       = $3C", "command mailbox")
    a=s.index("GameBankTick:\n")
    b=s.index("InitializeGame:\n",a)
    s=s[:a]+"""GameBankTick:
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
        jsr SetWorldColors
        jsr UpdateSound
        jmp GameBankReturn
StagePauseDone:
        lda Lives
        bne GameRunning
        jmp GameOver
GameRunning:
        lda Invulnerable
        beq InvulnDone
        dec Invulnerable
InvulnDone:
        lda #0
        sta AuxMode
        jsr ActorBankEnter ; true F6 bank0 independent actor AI
        jsr UpdateArrow
        jsr SetWorldColors
        jsr UpdateSound
        jmp GameBankReturn

"""+s[b:]
    # Perform both stage initialization calls (start and next visit)
    a="        jsr PlaceStageOrb\n        rts"
    b="""        jsr PlaceStageOrb
        lda #1
        sta AuxMode
        jsr ActorBankEnter
        rts"""
    if s.count(a)!=2:raise ValueError(f"stage-init call sites={s.count(a)}")
    s=s.replace(a,b)
    s=once(s,"        ORG $F700\n; GAMEPLAY-5 C:", """        ; F6 independent bank0 call. Following JMP fetched after switch
        ; at same PC in bank0 ($F6C3); bank2 owns the return RTS at $F6D3.
        ORG $F6C0
ActorBankEnter:
        lda $FFF6
        ORG $F6D3
ActorBankReturn:
        rts

        ORG $F700
; GAMEPLAY-5 C:""", "F6 hot/cold bank trampolines")
    return s

def actors_bank3(s):
    s=once(s,"        jsr CheckHaloHit\n", "        nop\n        nop\n        nop\n", "remove old sequential halo kill")
    s=once(s, """SelectEnemyArtImpl:
        lda StageKills
        clc
        adc #1
        cmp KillsNeed
        bne SelectKnightPose""", """SelectEnemyArtImpl:
        lda $E4             ; real 3-actor selected visual slot
        cmp #2
        bne SelectKnightPose""", "distinct Ranger identity")
    return s
