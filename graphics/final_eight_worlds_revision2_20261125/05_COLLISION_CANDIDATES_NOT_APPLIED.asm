; SOURCE_ONLY collisions. NOT applied to bank0 WorldRects or game ROM.
; [x0,x1,y0,y1] exclusive max bounds, 16 B per stage.
; Requires separate MAIN scope and runtime validation.
ProposedWorldRects:
; Stage 1: Skog
        dc.b $10,$30,$0F,$39,$70,$90,$0F,$39,$10,$30,$81,$AD,$70,$90,$81,$AD
; Stage 2: Skog
        dc.b $14,$30,$0F,$39,$64,$80,$0F,$39,$14,$30,$81,$AD,$64,$80,$81,$AD
; Stage 3: Berg
        dc.b $10,$30,$13,$35,$70,$90,$13,$35,$10,$30,$87,$A7,$70,$90,$87,$A7
; Stage 4: Berg
        dc.b $14,$30,$13,$35,$64,$80,$13,$35,$14,$30,$87,$A7,$64,$80,$87,$A7
; Stage 5: Dröm
        dc.b $10,$2C,$0F,$39,$74,$90,$0F,$39,$10,$30,$83,$AB,$70,$90,$83,$AB
; Stage 6: Dröm
        dc.b $14,$30,$0F,$39,$64,$80,$0F,$39,$14,$30,$83,$AB,$64,$80,$83,$AB
; Stage 7: Natt
        dc.b $10,$30,$11,$39,$70,$90,$11,$39,$10,$30,$83,$A9,$70,$90,$83,$A9
; Stage 8: Natt
        dc.b $14,$30,$11,$39,$64,$80,$11,$39,$14,$30,$83,$A9,$64,$80,$83,$A9
