; THE SKRAUN – GRAPHICS P1 – DESIGN DATA ONLY, NO ROM IMPLEMENTATION
; Both candidates RIGHT head toward bit0 (right), rump toward bit7 (left).
; TOP_FIRST: logical screen top-to-bottom, no assumption about CPU kernel memory order.
; BOTTOM_FIRST supplied as explicit alternative for future independently authorized ROM work.
; LEFT source is bitwise horizontal mirror of RIGHT per row; do NOT invert vertical order by accident.
; THESE 12-BYTE ART TABLES CANNOT BE DIRECTLY PATCHED INTO R3-VFIX 177-ENTRY TABLES.

SkraunP1_A_rounded_back_A_RIGHT_TOP_FIRST:
    dc.b %01000100
    dc.b %11001100
    dc.b %01001100
    dc.b %01111110
    dc.b %01111111
    dc.b %11111101
    dc.b %11111111
    dc.b %01111101
    dc.b %01111110
    dc.b %01001100
    dc.b %11001100
    dc.b %01000100

SkraunP1_A_rounded_back_A_RIGHT_BOTTOM_FIRST:
    dc.b %01000100
    dc.b %11001100
    dc.b %01001100
    dc.b %01111110
    dc.b %01111101
    dc.b %11111111
    dc.b %11111101
    dc.b %01111111
    dc.b %01111110
    dc.b %01001100
    dc.b %11001100
    dc.b %01000100

SkraunP1_A_rounded_back_A_LEFT_TOP_FIRST:
    dc.b %00100010
    dc.b %00110011
    dc.b %00110010
    dc.b %01111110
    dc.b %11111110
    dc.b %10111111
    dc.b %11111111
    dc.b %10111110
    dc.b %01111110
    dc.b %00110010
    dc.b %00110011
    dc.b %00100010

SkraunP1_A_rounded_back_A_LEFT_BOTTOM_FIRST:
    dc.b %00100010
    dc.b %00110011
    dc.b %00110010
    dc.b %01111110
    dc.b %10111110
    dc.b %11111111
    dc.b %10111111
    dc.b %11111110
    dc.b %01111110
    dc.b %00110010
    dc.b %00110011
    dc.b %00100010

SkraunP1_A_rounded_back_B_RIGHT_TOP_FIRST:
    dc.b %00101000
    dc.b %01101100
    dc.b %01001100
    dc.b %01111110
    dc.b %01111111
    dc.b %11111101
    dc.b %11111111
    dc.b %01111101
    dc.b %01111110
    dc.b %01001100
    dc.b %11000110
    dc.b %10000010

SkraunP1_A_rounded_back_B_RIGHT_BOTTOM_FIRST:
    dc.b %10000010
    dc.b %11000110
    dc.b %01001100
    dc.b %01111110
    dc.b %01111101
    dc.b %11111111
    dc.b %11111101
    dc.b %01111111
    dc.b %01111110
    dc.b %01001100
    dc.b %01101100
    dc.b %00101000

SkraunP1_A_rounded_back_B_LEFT_TOP_FIRST:
    dc.b %00010100
    dc.b %00110110
    dc.b %00110010
    dc.b %01111110
    dc.b %11111110
    dc.b %10111111
    dc.b %11111111
    dc.b %10111110
    dc.b %01111110
    dc.b %00110010
    dc.b %01100011
    dc.b %01000001

SkraunP1_A_rounded_back_B_LEFT_BOTTOM_FIRST:
    dc.b %01000001
    dc.b %01100011
    dc.b %00110010
    dc.b %01111110
    dc.b %10111110
    dc.b %11111111
    dc.b %10111111
    dc.b %11111110
    dc.b %01111110
    dc.b %00110010
    dc.b %00110110
    dc.b %00010100

SkraunP1_B_low_long_back_A_RIGHT_TOP_FIRST:
    dc.b %00000000
    dc.b %01000100
    dc.b %11000110
    dc.b %01000100
    dc.b %01111110
    dc.b %11111101
    dc.b %11111111
    dc.b %11111101
    dc.b %01111110
    dc.b %01000100
    dc.b %11000110
    dc.b %01000100

SkraunP1_B_low_long_back_A_RIGHT_BOTTOM_FIRST:
    dc.b %01000100
    dc.b %11000110
    dc.b %01000100
    dc.b %01111110
    dc.b %11111101
    dc.b %11111111
    dc.b %11111101
    dc.b %01111110
    dc.b %01000100
    dc.b %11000110
    dc.b %01000100
    dc.b %00000000

SkraunP1_B_low_long_back_A_LEFT_TOP_FIRST:
    dc.b %00000000
    dc.b %00100010
    dc.b %01100011
    dc.b %00100010
    dc.b %01111110
    dc.b %10111111
    dc.b %11111111
    dc.b %10111111
    dc.b %01111110
    dc.b %00100010
    dc.b %01100011
    dc.b %00100010

SkraunP1_B_low_long_back_A_LEFT_BOTTOM_FIRST:
    dc.b %00100010
    dc.b %01100011
    dc.b %00100010
    dc.b %01111110
    dc.b %10111111
    dc.b %11111111
    dc.b %10111111
    dc.b %01111110
    dc.b %00100010
    dc.b %01100011
    dc.b %00100010
    dc.b %00000000

SkraunP1_B_low_long_back_B_RIGHT_TOP_FIRST:
    dc.b %00000000
    dc.b %00101000
    dc.b %01101100
    dc.b %01000100
    dc.b %01111110
    dc.b %11111101
    dc.b %11111111
    dc.b %11111101
    dc.b %01111110
    dc.b %01000100
    dc.b %11000110
    dc.b %10000010

SkraunP1_B_low_long_back_B_RIGHT_BOTTOM_FIRST:
    dc.b %10000010
    dc.b %11000110
    dc.b %01000100
    dc.b %01111110
    dc.b %11111101
    dc.b %11111111
    dc.b %11111101
    dc.b %01111110
    dc.b %01000100
    dc.b %01101100
    dc.b %00101000
    dc.b %00000000

SkraunP1_B_low_long_back_B_LEFT_TOP_FIRST:
    dc.b %00000000
    dc.b %00010100
    dc.b %00110110
    dc.b %00100010
    dc.b %01111110
    dc.b %10111111
    dc.b %11111111
    dc.b %10111111
    dc.b %01111110
    dc.b %00100010
    dc.b %01100011
    dc.b %01000001

SkraunP1_B_low_long_back_B_LEFT_BOTTOM_FIRST:
    dc.b %01000001
    dc.b %01100011
    dc.b %00100010
    dc.b %01111110
    dc.b %10111111
    dc.b %11111111
    dc.b %10111111
    dc.b %01111110
    dc.b %00100010
    dc.b %00110110
    dc.b %00010100
    dc.b %00000000

