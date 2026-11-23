"""FULLGAME-1: collapse 3 x 16B level-expanded obstacle caches to 16B raw geometry.
TestLevel bbox is expanded mathematically, freeing D0..EF for actual actor state.
The original source/graphics remain frozen; no claim of 8 final maps.
"""
def one(s,a,b,name):
    n=s.count(a)
    if n!=1: raise ValueError(f"{name}: expected 1 anchor, found {n}")
    return s.replace(a,b,1)
def cache_bank2(s):
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
    return s

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
