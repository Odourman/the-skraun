"""FULLGAME-1 experimental real M1 arrow. Developer-tested hypothesis only."""
def once(s, old, new, tag):
    n=s.count(old)
    if n!=1: raise ValueError(f"{tag}: expected one anchor, got {n}")
    return s.replace(old,new,1)

def patch_bank2(s):
    s=once(s,
       "        jsr SetWorldColors\n        jsr UpdateSound\n        jmp GameBankReturn",
       "        jsr UpdateArrow\n        jsr SetWorldColors\n        jsr UpdateSound\n        jmp GameBankReturn",
       "game tick moving arrow")
    s=once(s,
       "        lda #8\n        sta SwordStrike\n        ; CHECKPOINT A: no projectile, so no invisible damage ever\n        rts",
       "        lda #8\n        sta SwordStrike\n        jsr LaunchArrow      ; physical M1 shot on bow release\n        lda #9\n        sta SoundFrames\n        lda #12\n        sta AUDC0\n        lda #20\n        sta AUDF0\n        rts",
       "R1 release")
    s=once(s,
       "UpdateArrow:\n        lda ArrowCool",
       "UpdateArrow:\n        ; Temporary safety: no invisible arrow can hit during halo;\n        ; all arrows disappear when any halo is active (DESIGN DEVIATION).\n        lda HaloFrames\n        beq ArrowNoHaloCull\n        lda #0\n        sta ArrowDX\n        sta ArrowDY\nArrowNoHaloCull:\n        lda ArrowCool",
       "halo arrow safety")
    return s

ARROW_KERNEL = """
; Additional F6 bank3 visible loop: M1 takes place of PF2 halo for these frames.
; Pre-frame arrow/halo disjointness guaranteed by bank2 tick.
VisibleGate:
        ldx #192
        lda ArrowDX
        beq GateNormal
        lda HaloFrames
        bne GateNormal
        lda #0
        jmp VisibleArrow
GateNormal:
        lda #0
        jmp Visible

VisibleArrow:
        sta WSYNC
        sta GRP0
        lda PlayPF1,x
        sta PF1
        and #$80
        sta PF0
        txa
        tay
        lda (ArrowRowPtr),y
        sta ENAM1
        lda (OrbRowPtr),y
        sta ENABL
        ldy EnemyIndexScan,x
        lda (EnemyRowPtr),y
        sta GRP1
        txa
        sec
        sbc RenderBottom
        cmp SpriteHeight
        bcs ArrowNextSpriteBlank
        tay
        lda (GfxPtr),y
        dex
        bne VisibleArrow
        jmp VisibleDone
ArrowNextSpriteBlank:
        lda #0
        dex
        bne VisibleArrow
        jmp VisibleDone
"""

def patch_bank3(s):
    s=once(s,
       "        ldx #192\n        lda #0            ; preloaded GRP0 for first (empty) visible row\nVisible:",
       "        jmp VisibleGate  ; preframe physical M1 or gold halo path\nVisible:",
       "visible path gate")
    s=once(s, "        ORG $F459\nPF0Choices:", ARROW_KERNEL+"\n        ORG $F459\nPF0Choices:", "F401-F458 alternate loop")
    return s
