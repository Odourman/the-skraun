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
        lda #$50          ; ascending orb chime
        cmp SoundFrames
        bcc OrbChimeAlreadyQueued
        sta SoundFrames
OrbChimeAlreadyQueued:
        lda #0
        sta OrbMask""","orb pickup cue")
    s=exactly(s,"""        lda #30
        sta HaloFrames
AttackColor:""","""        lda #30
        sta HaloFrames
        lda Level
        asl
        asl
        asl
        asl               ; $10/$20/$30: 3 halo power sounds
        cmp SoundFrames
        bcc HaloCueAlreadyQueued
        sta SoundFrames
HaloCueAlreadyQueued:
AttackColor:""","halo activation cue")
    return s
