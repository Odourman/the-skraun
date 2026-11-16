; THE SKRAUN GRAPHICS v0.1 - NO ROM CODE CHANGES
; 8x12 row order always logical TOP -> BOTTOM; physical kernel index mapping must be verified
; Art candidates only, not MAIN approved or Stella validated

Skraun_A_A_Right_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %11111100
    dc.b %11011110
    dc.b %00111110
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_A_A_Right_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111110
    dc.b %11011110
    dc.b %11111100
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_A_A_Left_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %00111111
    dc.b %01111011
    dc.b %01111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_A_A_Left_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %01111100
    dc.b %01111011
    dc.b %00111111
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_A_B_Right_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %00111111
    dc.b %01111011
    dc.b %01111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_A_B_Right_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %01111100
    dc.b %01111011
    dc.b %00111111
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_A_B_Left_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %11111100
    dc.b %11011110
    dc.b %00111110
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_A_B_Left_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111110
    dc.b %11011110
    dc.b %11111100
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_B_A_Right_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %10111111
    dc.b %11100110
    dc.b %01100100
    dc.b %01100110
    dc.b %01000110
    dc.b %01000100
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_B_A_Right_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000100
    dc.b %01000110
    dc.b %01100110
    dc.b %01100100
    dc.b %11100110
    dc.b %10111111
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_B_A_Left_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %11111101
    dc.b %01100111
    dc.b %00100110
    dc.b %01100110
    dc.b %01100010
    dc.b %00100010
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_B_A_Left_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %00100010
    dc.b %01100010
    dc.b %01100110
    dc.b %00100110
    dc.b %01100111
    dc.b %11111101
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_B_B_Right_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %11111101
    dc.b %01100111
    dc.b %00100110
    dc.b %01100110
    dc.b %01100010
    dc.b %00100010
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_B_B_Right_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %00100010
    dc.b %01100010
    dc.b %01100110
    dc.b %00100110
    dc.b %01100111
    dc.b %11111101
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_B_B_Left_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00111100
    dc.b %10111111
    dc.b %11100110
    dc.b %01100100
    dc.b %01100110
    dc.b %01000110
    dc.b %01000100
    dc.b %11000011

; Bottom-first variant; descending-index kernels only:
Skraun_B_B_Left_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000100
    dc.b %01000110
    dc.b %01100110
    dc.b %01100100
    dc.b %11100110
    dc.b %10111111
    dc.b %00111100
    dc.b %01111110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

Skraun_C_A_Right_TOP_FIRST:
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

; Bottom-first variant; descending-index kernels only:
Skraun_C_A_Right_BOTTOM_FIRST:
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

Skraun_C_A_Left_TOP_FIRST:
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

; Bottom-first variant; descending-index kernels only:
Skraun_C_A_Left_BOTTOM_FIRST:
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

Skraun_C_B_Right_TOP_FIRST:
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

; Bottom-first variant; descending-index kernels only:
Skraun_C_B_Right_BOTTOM_FIRST:
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

Skraun_C_B_Left_TOP_FIRST:
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

; Bottom-first variant; descending-index kernels only:
Skraun_C_B_Left_BOTTOM_FIRST:
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
