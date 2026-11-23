"""FULLGAME-1 stage-dependent physical playfield source, 8 offset/shape variants.
Hot raster loop is leaner: PF0=0, PF1 from selected ROM pointer.
This changes old decorative leftmost PF0 bit; collision cache remains solid.
DASM/Stella evidence required for actual 262 and pixel safety.
"""
def world_bank3(s):
    n=s.count("ArrowRowPtr = $89")
    if n!=1: raise ValueError("ArrowRowPtr source symbol missing")
    s=s.replace("ArrowRowPtr = $89", "ArrowRowPtr = $89\nWorldPFPtr = $EC", 1)
    replacement="""        sta WSYNC
        sta GRP0
        txa
        tay
        lda (WorldPFPtr),y
        sta PF1
"""
    for label, successor in (("Visible:\n","        lda (HaloRowPtr),y"),("VisibleArrow:\n","        lda (ArrowRowPtr),y")):
        a=s.index(label)
        b=s.index(successor,a)
        s=s[:a]+label+replacement+s[b:]
    return s
