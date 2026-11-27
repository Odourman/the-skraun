; THE SKRAUN MAIN VI / GRAPHICS II : SOURCE_ONLY P1 REPLACEMENT, NOT BUILT
; Only replace 3 K1 17-byte data rows within the existing F7A8 block.
; Data order is bottom-first for ROM: index 0 is physical bottom. Index 16 is zero guard.
; Do not change Ranger R1 rows, pointer tables, REFP1, VDEL, or code.
K1NeutralBytes:
    dc.b $C6,$6C,$6C,$28,$39,$39,$3C,$7C,$FE,$7E,$3C,$76,$76,$42,$7E,$3C,$00
K1WarningBytes:
    dc.b $C6,$6C,$6C,$28,$38,$39,$3D,$7D,$FE,$7E,$3D,$77,$77,$43,$7E,$3D,$00
K1StrikeBytes:
    dc.b $C6,$6C,$6C,$28,$38,$38,$3F,$7F,$FE,$7E,$3C,$76,$76,$42,$7E,$3C,$00
