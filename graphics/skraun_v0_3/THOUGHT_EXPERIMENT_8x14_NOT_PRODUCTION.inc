; THE SKRAUN GRAPHICS v0.3 – Dimension experiment, NOT approved
; DATA ONLY: NOT ROM, NOT actual Stella test.
; Each row bit7 to bit0 is image left-to-right, top-first logical.
; Descending-index R3-VFIX must be mapped to its 177-entry table separately.
; No changes to engine, code banks, P0/P1 scheduling, or PF renderer.

Unapproved8x14_A_R_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %11111111
    dc.b %10011001
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %01011010
    dc.b %11000011

Unapproved8x14_A_R_BOTTOM:
    dc.b %11000011
    dc.b %01011010
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %10011001
    dc.b %11111111
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Unapproved8x14_A_L_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %11111111
    dc.b %10011001
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %01011010
    dc.b %11000011

Unapproved8x14_A_L_BOTTOM:
    dc.b %11000011
    dc.b %01011010
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %10011001
    dc.b %11111111
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Unapproved8x14_B_R_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %01000010

Unapproved8x14_B_R_BOTTOM:
    dc.b %01000010
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Unapproved8x14_B_L_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %01000010

Unapproved8x14_B_L_BOTTOM:
    dc.b %01000010
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100
