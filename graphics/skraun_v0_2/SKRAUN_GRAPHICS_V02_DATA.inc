; SKRAUN GRAPHICS V0.2 2026-11-16 | 8x12 BITMAP DATA ONLY
; AUTHORING: TOP ROW FIRST, bit7 is LEFTMOST, bit0 RIGHTMOST
; FULL 177-ENTRY R3-VFIX raster tables cannot be patched by copying 12 bytes.
; R3 descending kernel must map row order independently before any ROM integration.
; NO ROM OR STELLA TEST PERFORMED.

Skraun_v01_C_baseline_A_R_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %11111110
    dc.b %10011011
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000100
    dc.b %11000011

Skraun_v01_C_baseline_A_R_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %11000100
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %10011011
    dc.b %11111110
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_v01_C_baseline_A_L_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %01111111
    dc.b %11011001
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %00100011
    dc.b %11000011

Skraun_v01_C_baseline_A_L_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %00100011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %11011001
    dc.b %01111111
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_v01_C_baseline_B_R_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %01111111
    dc.b %11011001
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %00100011
    dc.b %11000011

Skraun_v01_C_baseline_B_R_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %00100011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %11011001
    dc.b %01111111
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_v01_C_baseline_B_L_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %11111110
    dc.b %10011011
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000100
    dc.b %11000011

Skraun_v01_C_baseline_B_L_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %11000100
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %10011011
    dc.b %11111110
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_C_refined_A_R_TOP_FIRST:
    dc.b %00100110
    dc.b %01111110
    dc.b %01011010
    dc.b %00111110
    dc.b %00111100
    dc.b %11111100
    dc.b %10111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %11000110
    dc.b %10000011

Skraun_C_refined_A_R_BOTTOM_FIRST:
    dc.b %10000011
    dc.b %11000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111111
    dc.b %11111100
    dc.b %00111100
    dc.b %00111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100110

Skraun_C_refined_A_L_TOP_FIRST:
    dc.b %01100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111100
    dc.b %00111100
    dc.b %00111111
    dc.b %11111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100011
    dc.b %11000001

Skraun_C_refined_A_L_BOTTOM_FIRST:
    dc.b %11000001
    dc.b %01100011
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %11111101
    dc.b %00111111
    dc.b %00111100
    dc.b %01111100
    dc.b %01011010
    dc.b %01111110
    dc.b %01100100

Skraun_C_refined_B_R_TOP_FIRST:
    dc.b %00100110
    dc.b %01111110
    dc.b %01011010
    dc.b %00111110
    dc.b %00111100
    dc.b %00111111
    dc.b %11111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %11000011

Skraun_C_refined_B_R_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %11111101
    dc.b %00111111
    dc.b %00111100
    dc.b %00111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100110

Skraun_C_refined_B_L_TOP_FIRST:
    dc.b %01100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111100
    dc.b %00111100
    dc.b %11111100
    dc.b %10111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000011

Skraun_C_refined_B_L_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111111
    dc.b %11111100
    dc.b %00111100
    dc.b %01111100
    dc.b %01011010
    dc.b %01111110
    dc.b %01100100

Skraun_C_overhead_A_R_TOP_FIRST:
    dc.b %00100100
    dc.b %01111100
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %10011101
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %01000110
    dc.b %11000011

Skraun_C_overhead_A_R_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %10011101
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111100
    dc.b %00100100

Skraun_C_overhead_A_L_TOP_FIRST:
    dc.b %00100100
    dc.b %00111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11011011
    dc.b %10111001
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %01100010
    dc.b %11000011

Skraun_C_overhead_A_L_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111001
    dc.b %11011011
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %00111110
    dc.b %00100100

Skraun_C_overhead_B_R_TOP_FIRST:
    dc.b %00100100
    dc.b %01111100
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %11111001
    dc.b %10111111
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %01100010
    dc.b %11000011

Skraun_C_overhead_B_R_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111111
    dc.b %11111001
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %01111100
    dc.b %00100100

Skraun_C_overhead_B_L_TOP_FIRST:
    dc.b %00100100
    dc.b %00111110
    dc.b %01011010
    dc.b %00111100
    dc.b %00111100
    dc.b %10011111
    dc.b %11111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01111110
    dc.b %01000110
    dc.b %11000011

Skraun_C_overhead_B_L_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01111110
    dc.b %00111100
    dc.b %00111100
    dc.b %11111101
    dc.b %10011111
    dc.b %00111100
    dc.b %00111100
    dc.b %01011010
    dc.b %00111110
    dc.b %00100100
