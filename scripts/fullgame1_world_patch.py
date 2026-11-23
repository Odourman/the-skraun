"""FULLGAME-1 stage-dependent physical playfield source, 8 offset/shape variants.
Hot raster loop is leaner: PF0=0, PF1 from selected ROM pointer.
This changes old decorative leftmost PF0 bit; collision cache remains solid.
DASM/Stella evidence required for actual 262 and pixel safety.
"""
def world_bank3(s):
    n=s.count("ArrowRowPtr = $89")
    if n!=1: raise ValueError("ArrowRowPtr source symbol missing")
    s=s.replace("ArrowRowPtr = $89", "ArrowRowPtr = $89\nWorldPFPtr = $EC", 1)
    old="""        sta WSYNC
        sta GRP0
        lda PlayPF1,x
        sta PF1
        and #$80
        sta PF0
        txa
        tay
"""
    new="""        sta WSYNC
        sta GRP0
        txa
        tay
        lda (WorldPFPtr),y
        sta PF1
"""
    n=s.count(old)
    if n!=2: raise ValueError(f"normal+arrow raster loop anchors={n}")
    return s.replace(old,new)
