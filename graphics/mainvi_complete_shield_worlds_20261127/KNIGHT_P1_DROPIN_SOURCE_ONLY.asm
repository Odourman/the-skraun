; THE SKRAUN MAIN VI / GRAPHICS II : SOURCE_ONLY P1 REPLACEMENT, NOT BUILT
; Only replace 3 K1 17-byte data rows within the existing F7A8 block.
; Data order is bottom-first for ROM: index 0 is physical bottom. Index 16 is zero guard.
; Do not change Ranger R1 rows, pointer tables, REFP1, VDEL, or code.
K1NeutralBytes:
    dc.b $4C,$64,$25,$35,$5D,$DF,$DE,$DE,$DE,$FC,$7C,$38,$7C,$44,$7C,$38,$00
K1WarningBytes:
    dc.b $4C,$64,$24,$34,$5C,$DC,$DC,$DC,$DE,$FF,$7D,$39,$7D,$45,$7D,$39,$00
K1StrikeBytes:
    dc.b $4C,$64,$24,$34,$5C,$DC,$DF,$DF,$DC,$FC,$7C,$38,$7C,$44,$7C,$38,$00
