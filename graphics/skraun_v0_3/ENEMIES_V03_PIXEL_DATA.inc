; THE SKRAUN GRAPHICS v0.3 – Enemy sprite masks
; DATA ONLY: NOT ROM, NOT actual Stella test.
; Each row bit7 to bit0 is image left-to-right, top-first logical.
; Descending-index R3-VFIX must be mapped to its 177-entry table separately.
; No changes to engine, code banks, P0/P1 scheduling, or PF renderer.

Knight_A_R_TOP:
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
    dc.b %00011000
    dc.b %11011110
    dc.b %10011101
    dc.b %11111111
    dc.b %01011110
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Knight_A_R_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %01011110
    dc.b %11111111
    dc.b %10011101
    dc.b %11011110
    dc.b %00011000
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100

Knight_A_L_TOP:
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
    dc.b %00011000
    dc.b %01111011
    dc.b %10111001
    dc.b %11111111
    dc.b %01111010
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Knight_A_L_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %01111010
    dc.b %11111111
    dc.b %10111001
    dc.b %01111011
    dc.b %00011000
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100

Knight_B_R_TOP:
    dc.b %00111111
    dc.b %01100101
    dc.b %01100111
    dc.b %00111101
    dc.b %00011101
    dc.b %11011110
    dc.b %10011100
    dc.b %11111100
    dc.b %01011100
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Knight_B_R_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %01011100
    dc.b %11111100
    dc.b %10011100
    dc.b %11011110
    dc.b %00011101
    dc.b %00111101
    dc.b %01100111
    dc.b %01100101
    dc.b %00111111

Knight_B_L_TOP:
    dc.b %11111100
    dc.b %10100110
    dc.b %11100110
    dc.b %10111100
    dc.b %10111000
    dc.b %01111011
    dc.b %00111001
    dc.b %00111111
    dc.b %00111010
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Knight_B_L_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %00111010
    dc.b %00111111
    dc.b %00111001
    dc.b %01111011
    dc.b %10111000
    dc.b %10111100
    dc.b %11100110
    dc.b %10100110
    dc.b %11111100

Archer_A_R_TOP:
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
    dc.b %10011000
    dc.b %11011100
    dc.b %10111110
    dc.b %10011110
    dc.b %10011100
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Archer_A_R_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %10011100
    dc.b %10011110
    dc.b %10111110
    dc.b %11011100
    dc.b %10011000
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100

Archer_A_L_TOP:
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
    dc.b %00011001
    dc.b %00111011
    dc.b %01111101
    dc.b %01111001
    dc.b %00111001
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Archer_A_L_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %00111001
    dc.b %01111001
    dc.b %01111101
    dc.b %00111011
    dc.b %00011001
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100

Archer_B_R_TOP:
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
    dc.b %01011000
    dc.b %11111100
    dc.b %11011111
    dc.b %11111100
    dc.b %01011100
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Archer_B_R_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %01011100
    dc.b %11111100
    dc.b %11011111
    dc.b %11111100
    dc.b %01011000
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100

Archer_B_L_TOP:
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
    dc.b %00011010
    dc.b %00111111
    dc.b %11111011
    dc.b %00111111
    dc.b %00111010
    dc.b %00011000
    dc.b %01100110
    dc.b %11000011

Archer_B_L_BOTTOM:
    dc.b %11000011
    dc.b %01100110
    dc.b %00011000
    dc.b %00111010
    dc.b %00111111
    dc.b %11111011
    dc.b %00111111
    dc.b %00011010
    dc.b %00111100
    dc.b %01100110
    dc.b %01100110
    dc.b %00111100
