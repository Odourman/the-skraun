; THE SKRAUN GRAPHICS v0.3 – Troll sprite masks
; DATA ONLY: NOT ROM, NOT actual Stella test.
; Each row bit7 to bit0 is image left-to-right, top-first logical.
; Descending-index R3-VFIX must be mapped to its 177-entry table separately.
; No changes to engine, code banks, P0/P1 scheduling, or PF renderer.

Q1_splayed_quad_A_R_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11111100
    dc.b %10111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %11011011
    dc.b %10000010

Q1_splayed_quad_A_R_BOTTOM:
    dc.b %10000010
    dc.b %11011011
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111111
    dc.b %11111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q1_splayed_quad_A_L_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %00111111
    dc.b %11111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %11011011
    dc.b %01000001

Q1_splayed_quad_A_L_BOTTOM:
    dc.b %01000001
    dc.b %11011011
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %11111101
    dc.b %00111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q1_splayed_quad_B_R_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %00111111
    dc.b %11111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %11011011
    dc.b %01000001

Q1_splayed_quad_B_R_BOTTOM:
    dc.b %01000001
    dc.b %11011011
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %11111101
    dc.b %00111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q1_splayed_quad_B_L_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11111100
    dc.b %10111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %11011011
    dc.b %10000010

Q1_splayed_quad_B_L_BOTTOM:
    dc.b %10000010
    dc.b %11011011
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111111
    dc.b %11111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q2_long_back_A_R_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11111111
    dc.b %10011001
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %01011010
    dc.b %11000011

Q2_long_back_A_R_BOTTOM:
    dc.b %11000011
    dc.b %01011010
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %10011001
    dc.b %11111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q2_long_back_A_L_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11111111
    dc.b %10011001
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %01011010
    dc.b %11000011

Q2_long_back_A_L_BOTTOM:
    dc.b %11000011
    dc.b %01011010
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %10011001
    dc.b %11111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q2_long_back_B_R_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %01000010

Q2_long_back_B_R_BOTTOM:
    dc.b %01000010
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Q2_long_back_B_L_TOP:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %10111101
    dc.b %11011011
    dc.b %01000010

Q2_long_back_B_L_BOTTOM:
    dc.b %01000010
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %10111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100
