"""FULLGAME-1: collapse 3 x 16B level-expanded obstacle caches to 16B raw geometry.
TestLevel bbox is expanded mathematically, freeing D0..EF for actual actor state.
The original source/graphics remain frozen; no claim of 8 final maps.
"""
def one(s,a,b,name):
    n=s.count(a)
    if n!=1: raise ValueError(f"{name}: expected 1 anchor, found {n}")
    return s.replace(a,b,1)
def cache_bank2(s):
    s=one(s,"StageOrbX:\n        dc.b 0,96,88,80,104,92,84,100,76",
          "StageOrbX:\n        dc.b 0,96,88,80,80,92,84,88,76",
          "safe 8-world level3 orb locations")
    s=one(s,"        ldx #47\nCopyMirror:", "        ldx #15\nCopyMirror:", "mirror 16 byte cache")
    s=one(s,"        ldx #47\nCopyRepeat:", "        ldx #15\nCopyRepeat:", "repeat 16 byte cache")
    a=s.index("MirrorRects:\n")
    b=s.index("\n        ORG $F480",a)
    s=s[:a]+"""MirrorRects:
        ; 4 unexpanded solids x0,x1,y0,y1, collision grow follows Level
        dc.b 9,32,21,52,129,152,21,52,21,48,133,156,113,140,133,156
RepeatRects:
        dc.b 9,32,21,52,89,112,21,52,21,48,133,156,101,128,133,156
"""+s[b:]
    s=one(s,"""        lda Level
        sec
        sbc #1
        asl
        asl
        asl
        asl
        tax
SwordRectLoop:""","""        ldx #0
SwordRectLoop:""","sword unexpanded LOS")
    assert_safe_level3_orbs(s)
    return s

def assert_safe_level3_orbs(s):
    """Static geometry gate: a player standing ON each BL orb can grow to L3.
    Confirms all eight compiled orb centers against the actual four solid
    rectangles loaded by the F6 world-layout code. Does not replace Stella.
    """
    import re
    def read_row(label):
        m=re.search(r"^"+label+r":\\s*\\n\\s*dc\\.b\\s+([0-9,]+)",s,re.M)
        if not m: raise ValueError("missing geometry row "+label)
        return [int(v) for v in m.group(1).split(",")]
    orbs=read_row("StageOrbX")
    mirror=read_row("MirrorRects")
    repeat=read_row("RepeatRects")
    offsets=[0,0,0,6,6,12,12,18,18]
    if len(orbs)!=9 or len(mirror)!=16 or len(repeat)!=16:
        raise ValueError("unexpected world geometry dimensions")
    for stage in range(1,9):
        rects=mirror if stage%2 else repeat
        x=orbs[stage]
        for i in range(0,16,4):
            x0,x1,y0,y1=rects[i:i+4]
            y0-=offsets[stage]
            y1-=offsets[stage]
            if x+16>x0 and x-16<x1 and 112+18>y0 and 112-18<y1:
                raise ValueError(f"stage {stage} orb center x={x} blocks L3 growth at rect {i//4}")
    
def cache_bank3(s):
    a=s.index("CandidateValid:\n")
    b=s.index("\nUpdateScale:",a)
    s=s[:a]+"""CandidateValid:
        ldx TestLevel
        lda TryX
        cmp MinCX,x
        bcc Invalid
        cmp MaxCX,x
        bcs Invalid
        lda TryY
        cmp MinCY,x
        bcc Invalid
        cmp MaxCY,x
        bcs Invalid
        lda WidthHalf,x
        sta RectPtr
        lda HeightHalf,x
        sta RectPtr+1
        ldx #0
RectLoop:
        ; Center bounding box intersects raw rectangle if the two axes
        ; overlap. The raw four rectangles live at C0..CF for all levels.
        lda TryX
        clc
        adc RectPtr
        cmp $C0,x
        bcc NextRect
        lda TryX
        sec
        sbc RectPtr
        cmp $C1,x
        bcs NextRect
        lda TryY
        clc
        adc RectPtr+1
        cmp $C2,x
        bcc NextRect
        lda TryY
        sec
        sbc RectPtr+1
        cmp $C3,x
        bcc Invalid
NextRect:
        txa
        clc
        adc #4
        tax
        cpx #16
        bcc RectLoop
        lda #1
        rts
Invalid:
        lda #0
        rts
"""+s[b:]
    return s
