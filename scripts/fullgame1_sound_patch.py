"""FULLGAME-1 two-voice SFX integration. All TIA audio writes offscreen.
$BF is highest-priority event request; $EE/$EF are packed voice states.
Source-only until measured in Stella with audio explicitly enabled.
"""
def exactly(s,old,new,tag):
    if s.count(old)!=1: raise ValueError(f"{tag}: source anchor {s.count(old)} not one")
    return s.replace(old,new,1)

def sound_bank2(s):
    a=s.index("InitializeGame:\n")
    b=s.index("SetWaveTarget:\n",a)
    start=s[a:b]
    start=exactly(start,"        jsr ActorBankEnter\n        rts",
        "        jsr ActorBankEnter\n        lda #$F0          ; restart cue after actor RAM clears\n        sta SoundFrames\n        rts","new game sound")
    s=s[:a]+start+s[b:]
    s=exactly(s, """        lda #24
        sta SoundFrames
        lda #12
        sta AUDF0
        lda #6
        sta AUDC0""", """        lda #$60          ; stage transition melody
        sta SoundFrames""","stage change cue")
    s=exactly(s,"""        jsr UpdateArrow
        jsr SetWorldColors""","""        jsr UpdateArrow
        ; New halo starts at frame=30 in bank3 overscan; one cue per
        ; activation, 3 levels with separate TIA distortion/pitch.
        lda HaloFrames
        cmp #30
        bne HaloSoundAlreadyPlayed
        lda Level
        asl
        asl
        asl
        asl
        cmp SoundFrames
        bcc HaloSoundAlreadyPlayed
        sta SoundFrames
HaloSoundAlreadyPlayed:
        jsr SetWorldColors""","halo start in roomy game bank")
    # All arrow impacts and exits get a low dry tick; never trigger an
    # invisible projectile since active arrow is always enabled in M1.
    s=exactly(s,"""ArrowDestroy:
        lda #0
        sta ArrowDX""","""ArrowDestroy:
        lda #$90          ; projectile hits world/halo/player/edge
        cmp SoundFrames
        bcc ArrowSoundHigherPriority
        sta SoundFrames
ArrowSoundHigherPriority:
        lda #0
        sta ArrowDX""","projectile destruction cue")
    # Legacy damage entry was an unprioritized continuous channel0 tone.
    s=exactly(s,"""        lda #16
        sta SoundFrames
        lda #2
        sta AUDC0
        lda #8
        sta AUDF0""","""        lda #$C0
        cmp SoundFrames
        bcc DamageAlreadyQueued
        sta SoundFrames
DamageAlreadyQueued:""","arrow-player damage cue")
    s=exactly(s,"""LoseLife:
        dec Lives
        lda #80
        sta PlayerX""","""LoseLife:
        dec Lives
        bne ExtraLifeStillHere
        lda #$E0
        sta SoundFrames
ExtraLifeStillHere:
        lda #80
        sta PlayerX""","player last life cue")
    a=s.index("UpdateSound:\n")
    b=s.index("GameOver:\n",a)
    s=s[:a]+"""UpdateSound:
        ; The entire F6 bank1 sound engine executes during overscan only.
        jmp SoundBankEnter

"""+s[b:]
    s=exactly(s, """        lda #0
        sta AUDV0
        lda SwitchState""","""        jsr UpdateSound   ; finish game-over envelope, then mute both voices
        lda SwitchState""","gameover sound")
    return s

def sound_bank3(s):
    s=exactly(s,"""        inc Level
        lda #0
        sta OrbMask""","""        inc Level
        lda #$50          ; chime only after actual successful growth
        sta SoundFrames
        lda #0
        sta OrbMask""","orb pickup cue")
    # Obsolete A=0 immediately before RTS had no consumer; its removal
    # gives the two missing bytes before the immutable F600 ROM bank3 page.
    s=exactly(s,"""        sta OrbMask
        lda #0
        ; consumed orb""","""        sta OrbMask
        ; consumed orb""","free two bytes of dead code")
    return s
