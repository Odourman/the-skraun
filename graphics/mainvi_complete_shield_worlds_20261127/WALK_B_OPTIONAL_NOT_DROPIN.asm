; OPTIONAL SOURCE_ONLY TWO-STEP WALK, NOT DIRECT DROP-IN: requires selector + data relocation.
; Original six 17-byte mask rows + 9 bytes unused in F7A8..F820; new 17-byte mask does not fit.
CShieldContourWalkB:
    dc.b $68,$2C,$25,$35,$5D,$DF,$DE,$DE,$DE,$FC,$7C,$38,$7C,$44,$7C,$38,$00
CShieldSolidWalkB:
    dc.b $68,$2C,$25,$35,$5D,$DF,$FE,$FE,$FE,$FC,$7C,$38,$7C,$44,$7C,$38,$00
