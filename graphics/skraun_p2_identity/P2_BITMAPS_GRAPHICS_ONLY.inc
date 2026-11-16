; THE SKRAUN - GRAPHICS P2 IDENTITY SILHOUETTE PROOF
; ART DATA ONLY. Not source code for a game, not Stella-tested. Not production accepted.
; Every label: 8 rows? NO: exact 12 logical rows, 8 bits per row.
; TOP_FIRST is picture row0..row11. BOTTOM_FIRST reverses these same rows.
; RIGHT face head is on bitmap right. LEFT is exact horizontal row-wise bit reversal.
; No GPU/kernel schedule/actual REFP0 mapping is implied by these sources.

SkraunP2_FrozenP1A_A_RIGHT_TOP_FIRST:
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

SkraunP2_FrozenP1A_A_RIGHT_BOTTOM_FIRST:
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

SkraunP2_FrozenP1A_A_LEFT_TOP_FIRST:
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

SkraunP2_FrozenP1A_A_LEFT_BOTTOM_FIRST:
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

SkraunP2_FrozenP1A_B_RIGHT_TOP_FIRST:
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

SkraunP2_FrozenP1A_B_RIGHT_BOTTOM_FIRST:
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

SkraunP2_FrozenP1A_B_LEFT_TOP_FIRST:
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

SkraunP2_FrozenP1A_B_LEFT_BOTTOM_FIRST:
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

SkraunP2_I1_head_signature_A_RIGHT_TOP_FIRST:
    dc.b %01001000
    dc.b %11001000
    dc.b %01001100
    dc.b %01101111
    dc.b %01111011
    dc.b %11111110
    dc.b %11111110
    dc.b %01111011
    dc.b %01101111
    dc.b %01001100
    dc.b %11001000
    dc.b %01001000

SkraunP2_I1_head_signature_A_RIGHT_BOTTOM_FIRST:
    dc.b %01001000
    dc.b %11001000
    dc.b %01001100
    dc.b %01101111
    dc.b %01111011
    dc.b %11111110
    dc.b %11111110
    dc.b %01111011
    dc.b %01101111
    dc.b %01001100
    dc.b %11001000
    dc.b %01001000

SkraunP2_I1_head_signature_A_LEFT_TOP_FIRST:
    dc.b %00010010
    dc.b %00010011
    dc.b %00110010
    dc.b %11110110
    dc.b %11011110
    dc.b %01111111
    dc.b %01111111
    dc.b %11011110
    dc.b %11110110
    dc.b %00110010
    dc.b %00010011
    dc.b %00010010

SkraunP2_I1_head_signature_A_LEFT_BOTTOM_FIRST:
    dc.b %00010010
    dc.b %00010011
    dc.b %00110010
    dc.b %11110110
    dc.b %11011110
    dc.b %01111111
    dc.b %01111111
    dc.b %11011110
    dc.b %11110110
    dc.b %00110010
    dc.b %00010011
    dc.b %00010010

SkraunP2_I1_head_signature_B_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %01100100
    dc.b %01001100
    dc.b %01101111
    dc.b %01111011
    dc.b %11111110
    dc.b %11111110
    dc.b %01111011
    dc.b %01101111
    dc.b %01001100
    dc.b %01100100
    dc.b %00100100

SkraunP2_I1_head_signature_B_RIGHT_BOTTOM_FIRST:
    dc.b %00100100
    dc.b %01100100
    dc.b %01001100
    dc.b %01101111
    dc.b %01111011
    dc.b %11111110
    dc.b %11111110
    dc.b %01111011
    dc.b %01101111
    dc.b %01001100
    dc.b %01100100
    dc.b %00100100

SkraunP2_I1_head_signature_B_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %00100110
    dc.b %00110010
    dc.b %11110110
    dc.b %11011110
    dc.b %01111111
    dc.b %01111111
    dc.b %11011110
    dc.b %11110110
    dc.b %00110010
    dc.b %00100110
    dc.b %00100100

SkraunP2_I1_head_signature_B_LEFT_BOTTOM_FIRST:
    dc.b %00100100
    dc.b %00100110
    dc.b %00110010
    dc.b %11110110
    dc.b %11011110
    dc.b %01111111
    dc.b %01111111
    dc.b %11011110
    dc.b %11110110
    dc.b %00110010
    dc.b %00100110
    dc.b %00100100

SkraunP2_I2_limb_signature_A_RIGHT_TOP_FIRST:
    dc.b %00001100
    dc.b %10011000
    dc.b %11001000
    dc.b %01001110
    dc.b %00111111
    dc.b %11111101
    dc.b %11111111
    dc.b %01111101
    dc.b %01001110
    dc.b %11001000
    dc.b %10011000
    dc.b %00001100

SkraunP2_I2_limb_signature_A_RIGHT_BOTTOM_FIRST:
    dc.b %00001100
    dc.b %10011000
    dc.b %11001000
    dc.b %01001110
    dc.b %01111101
    dc.b %11111111
    dc.b %11111101
    dc.b %00111111
    dc.b %01001110
    dc.b %11001000
    dc.b %10011000
    dc.b %00001100

SkraunP2_I2_limb_signature_A_LEFT_TOP_FIRST:
    dc.b %00110000
    dc.b %00011001
    dc.b %00010011
    dc.b %01110010
    dc.b %11111100
    dc.b %10111111
    dc.b %11111111
    dc.b %10111110
    dc.b %01110010
    dc.b %00010011
    dc.b %00011001
    dc.b %00110000

SkraunP2_I2_limb_signature_A_LEFT_BOTTOM_FIRST:
    dc.b %00110000
    dc.b %00011001
    dc.b %00010011
    dc.b %01110010
    dc.b %10111110
    dc.b %11111111
    dc.b %10111111
    dc.b %11111100
    dc.b %01110010
    dc.b %00010011
    dc.b %00011001
    dc.b %00110000

SkraunP2_I2_limb_signature_B_RIGHT_TOP_FIRST:
    dc.b %00011000
    dc.b %01011000
    dc.b %11010000
    dc.b %01001110
    dc.b %00111111
    dc.b %11111101
    dc.b %11111111
    dc.b %01111101
    dc.b %01001110
    dc.b %11010000
    dc.b %01011000
    dc.b %00011000

SkraunP2_I2_limb_signature_B_RIGHT_BOTTOM_FIRST:
    dc.b %00011000
    dc.b %01011000
    dc.b %11010000
    dc.b %01001110
    dc.b %01111101
    dc.b %11111111
    dc.b %11111101
    dc.b %00111111
    dc.b %01001110
    dc.b %11010000
    dc.b %01011000
    dc.b %00011000

SkraunP2_I2_limb_signature_B_LEFT_TOP_FIRST:
    dc.b %00011000
    dc.b %00011010
    dc.b %00001011
    dc.b %01110010
    dc.b %11111100
    dc.b %10111111
    dc.b %11111111
    dc.b %10111110
    dc.b %01110010
    dc.b %00001011
    dc.b %00011010
    dc.b %00011000

SkraunP2_I2_limb_signature_B_LEFT_BOTTOM_FIRST:
    dc.b %00011000
    dc.b %00011010
    dc.b %00001011
    dc.b %01110010
    dc.b %10111110
    dc.b %11111111
    dc.b %10111111
    dc.b %11111100
    dc.b %01110010
    dc.b %00001011
    dc.b %00011010
    dc.b %00011000

