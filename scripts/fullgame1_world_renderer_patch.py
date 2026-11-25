"""FULLGAME-1 original-compatible F6 eight-world, live-Y sprite experiment.
Actual 8 x 24 PF1 band layouts and 8 world solidity sets. Renderer still
cycles P1 temporally among actors; does not prove 3 physical P1 sprites.
"""
WORLDS=[
[24,60,126,24,24,24,0,0,0,0,0,0,0,0,0,0,0,0,24,24,126,60,24,0],
[16,56,124,254,16,124,56,0,0,0,0,0,0,0,0,0,0,56,124,16,254,124,56,16],
[129,195,231,255,102,36,0,0,0,0,0,0,0,0,0,0,0,36,102,255,231,195,129],
[36,102,231,255,195,129,0,0,0,0,0,0,0,0,0,0,129,195,231,255,102,36,66,0],
[17,51,119,255,238,204,136,0,0,0,0,0,0,0,0,0,0,136,204,238,255,119,51,17],
[128,192,224,240,120,60,30,0,0,0,0,0,0,0,0,0,0,30,60,120,240,224,192,128],
[1,128,0,16,4,0,32,0,0,0,0,0,0,0,0,0,0,1,0,128,8,2,64,0],
[56,124,240,224,192,128,0,0,0,0,0,0,0,0,0,0,0,8,16,32,124,254,124,56]]
WORLDS=[w+[0]*(24-len(w)) for w in WORLDS]
SOLIDS=[
[(10,31,24,50),(128,151,24,50),(14,39,135,161),(122,148,135,161)],
[(10,34,28,61),(123,148,20,49),(15,42,134,158),(124,151,137,162)],
[(8,36,21,55),(127,153,26,58),(10,39,135,165),(127,152,138,164)],
[(9,34,25,59),(124,153,26,63),(11,35,131,165),(127,153,136,160)],
[(9,30,22,55),(129,151,27,61),(12,37,135,165),(123,151,138,165)],
[(10,39,24,59),(125,153,22,54),(10,33,138,161),(128,152,135,162)],
[(9,35,24,62),(128,151,22,56),(12,39,135,165),(127,151,135,165)],
[(10,35,29,55),(130,153,25,61),(15,40,136,165),(122,148,132,162)]]
assert len(WORLDS)==len(SOLIDS)==8
assert all(len(w)==24 for w in WORLDS) and all(len(r)==4 for r in SOLIDS)

def asc(a):
    return ",".join("$"+format(v,"02X") for v in a)

def patch_bank0(s):
    if s.count("ScratchIX = $E8")!=1:raise ValueError("bank0 scratch")
    s=s.replace("ScratchIX = $E8","EnemyBottom = $E8\nScratchIX = $E8")
    for tag,var in (("ChooseK1:","K1Y"),("ChooseK2:","K2Y"),("ChooseRanger:","RY")):
        a=s.index(tag+"\n")
        b=s.index("        rts\n",a)
        s=s[:b]+"        lda #169\n        sec\n        sbc "+var+"\n        sta EnemyBottom\n"+s[b:]
    a=s.index("InstallWorldMap:\n")
    b=s.index("        ORG $FFFC\n",a)
    code="""InstallWorldMap:
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
        dc.b $00,$00,$18,$30,$48,$60,$78,$90,$A8
WorldPFHi:
        dc.b $FA,$FA,$FA,$FA,$FA,$FA,$FA,$FA,$FA
WorldRects:
"""
    for i,rect in enumerate(SOLIDS):
        code+="        dc.b "+asc([v for r in rect for v in r])+" ; world "+str(i+1)+"\n"
    s=s[:a]+code+s[b:]
    # A knight may only hurt the player if it occupied the visible P1
    # slot for the just-rendered frame; P1 can display only one actor.
    s=s.replace("KnightCanHit:\n        lda Invuln\n","""KnightCanHit:
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
""")
    # Prevent same-frame invisible hits after arrow creation in overscan:
    # ArrowCool is no longer used as a 180-frame cooldown (RCool is).
    a="ArrowCooldownSet:\n        ldx Stage\n"
    if s.count(a)!=1:raise ValueError("arrow freshness source")
    s=s.replace(a,"ArrowCooldownSet:\n        lda #2\n        sta $9D\n        ldx Stage\n")
    return s

def patch_bank3(s):
    if s.count("EnemyRowPtr = $B6")!=1:raise ValueError("bank3 sprite symbol")
    s=s.replace("EnemyRowPtr = $B6","EnemyBottom = $E8\nEnemyRowPtr = $B6")
    before="""        txa
        tay
        lda (WorldPFPtr),y
        sta PF1"""
    after="""        ldy WorldPFIndex,x
        lda (WorldPFPtr),y
        sta PF1"""
    if s.count(before)!=2:raise ValueError("PF1 pointer changes="+str(s.count(before)))
    s=s.replace(before,after)
    old="""        ldy EnemyIndexScan,x
        lda (EnemyRowPtr),y
        sta GRP1"""
    neu="""        txa
        sec
        sbc EnemyBottom
        cmp #16
        bcs DynamicEnemyBlank
        tay
        lda (EnemyRowPtr),y
        jmp DynamicEnemyWrite
DynamicEnemyBlank:
        lda #0
DynamicEnemyWrite:
        sta GRP1"""
    if s.count(old)!=2:raise ValueError("P1 source changes="+str(s.count(old)))
    s=s.replace(old,neu,1)
    s=s.replace(old,neu.replace("DynamicEnemyBlank","DynamicArrowEnemyBlank").replace("DynamicEnemyWrite","DynamicArrowEnemyWrite"),1)
    halo="""        lda (HaloRowPtr),y
        sta PF2           ; c27, before left PF2 beam deadline
"""
    if s.count(halo)!=1:raise ValueError("halo source")
    s=s.replace(halo,"")
    a=s.index("VisibleArrow:\n");b=s.index("ArrowNextSpriteBlank:",a)
    section=s[a:b]
    if section.count("        lda (OrbRowPtr),y\n        sta ENABL\n")!=1:
        raise ValueError("M1/BL resource conflict")
    section=section.replace("        lda (OrbRowPtr),y\n        sta ENABL\n","")
    s=s[:a]+section+s[b:]
    # FA00..FAC0: 8 x 24 bytes + sentinel, preserve original FAC1 enemy art.
    world="PlayPF1:\n"
    for i,w in enumerate(WORLDS):
        world+="; World "+str(i+1)+" 24 raster bands\n"
        world+="        dc.b "+asc(list(reversed(w)))+"\n"
    world+="        dc.b 0\n"
    a=s.index("PlayPF1:\n");b=s.index("K1NeutralBytes:\n",a)
    s=s[:a]+world+s[b:]
    a=s.index("EnemyIndexScan:");b=s.index("        ORG $FD00\n",a)
    lut="WorldPFIndex:\n"+"".join("        ds 8,"+str(i)+"\n" for i in range(24))+"        ds 1,23\n"
    s=s[:a]+lut+s[b:]
    # TIA M1 shares player-1 color. Give it a contrast-safe physical
    # color even when the world-camouflaged Ranger was selected.
    gate="""VisibleGate:
        ldx #192
        lda ArrowDX
        beq GateNormal
"""
    if s.count(gate)!=1:raise ValueError("M1 gating source")
    s=s.replace(gate,gate+"""        lda #$9E
        sta COLUP1
""")
    # Reuse the *same* precomputed 8-line metatile index for M1 and BL.
    # This avoids 4 new cycles in the over-budget physical hot raster.
    # Visual projectile/BL snap to 8-raster-line bands; logical collision
    # remains exact X/Y and the 2-frame projectile freshness gate.
    orig="""        lda ArrowY
        cmp #48
        bcc MissileRowOff
        cmp #176
        bcs MissileRowOff
        clc
        adc #$90             ; $F890 + ArrowY (seed at $F940)
        sta ArrowRowPtr
        lda #$F8
        adc #0
        sta ArrowRowPtr+1"""
    repl="""        ; Only active arrows reach here; overscan logic validates bounds.
        ; Low seed pointer = $F92A + ceil(ArrowY / 8).
        ; Metatile Y = floor((176-ArrowY) / 8), so seed $F940
        ; enables one real 8-line missile band without per-line cost.
        lda ArrowY
        clc
        adc #7
        lsr
        lsr
        lsr
        clc
        adc #$2A
        sta ArrowRowPtr
        lda #$F9
        sta ArrowRowPtr+1"""
    if s.count(orig)!=1:raise ValueError("metatile M1 preframe source changed")
    s=s.replace(orig,repl)
    orig="""        lda #0
        sta OrbRowPtr
        lda #$FD
        sta OrbRowPtr+1"""
    repl="""        lda #$38    ; FD3F seed at metatile band 7 (BL orb)
        sta OrbRowPtr
        lda #$FD
        sta OrbRowPtr+1"""
    if s.count(orig)!=1:raise ValueError("metatile BL pointer source changed")
    s=s.replace(orig,repl)
    orig="""        dc.b $02,$02         ; 2 physical M1 scanlines; real TIA ENAM1 bit1"""
    repl="""        dc.b $02,$00         ; 8 physical scanlines per one visible M1 band"""
    if s.count(orig)!=1:raise ValueError("one-band M1 seed source changed")
    s=s.replace(orig,repl)
    return s

def patch_bank2(s):
    # Renderer companion: tracking P0 light/gold is X/Y-physical and
    # replaces the old rectangular PF2 ring. Logical radius unchanged.
    a="""SetWorldColors:
        ; Eight provisional color identities, but ONE common obstacle map.
        ; World PF must become gold under active halo (PLAY1-H test B).
        ldx Stage
"""
    b="""SetWorldColors:
        ; Animated gold player silhouette follows real P0 X/Y.
        lda HaloFrames
        beq P0AuraInactive
        lda #$2E
        sta $06
        jmp P0AuraReady
P0AuraInactive:
        lda #$0E
        sta $06
P0AuraReady:
        ldx Stage
"""
    if s.count(a)!=1:raise ValueError("P0 aura source")
    s=s.replace(a,b)
    a="TestArrowBody:\n        lda Invulnerable\n"
    if s.count(a)!=1:raise ValueError("arrow damage gate")
    s=s.replace(a,"TestArrowBody:\n        lda ArrowCool\n        bne TestArrowWalls\n        lda Invulnerable\n")
    return s
