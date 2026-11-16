; THE SKRAUN P3-F1 | ART DATA ONLY / NOT ROM / NOT STELLA
; 8x12 monochrome, TOP_FIRST row0 head, row11 feet; BOTTOM_FIRST row order reversed
; LEFT = exact per-row 8bit reversal of RIGHT. Two walking poses; no UP/DOWN graphic.
; NOT drop-in kernel or 177 scanline indexing; not integrated.

SkraunP3F1_U1_frozen_A_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01100111
    dc.b %00111110
    dc.b %11111110
    dc.b %10111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000011

SkraunP3F1_U1_frozen_A_RIGHT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111100
    dc.b %11111110
    dc.b %00111110
    dc.b %01100111
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_U1_frozen_A_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %11100110
    dc.b %01111100
    dc.b %01111111
    dc.b %00111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %11000011

SkraunP3F1_U1_frozen_A_LEFT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %00111101
    dc.b %01111111
    dc.b %01111100
    dc.b %11100110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_U1_frozen_B_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01100111
    dc.b %00111110
    dc.b %01111111
    dc.b %00111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %11000001

SkraunP3F1_U1_frozen_B_RIGHT_BOTTOM_FIRST:
    dc.b %11000001
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %00111101
    dc.b %01111111
    dc.b %00111110
    dc.b %01100111
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_U1_frozen_B_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %11100110
    dc.b %01111100
    dc.b %11111110
    dc.b %10111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %10000011

SkraunP3F1_U1_frozen_B_LEFT_BOTTOM_FIRST:
    dc.b %10000011
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111100
    dc.b %11111110
    dc.b %01111100
    dc.b %11100110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_D1_face_ear_permanent_A_RIGHT_TOP_FIRST:
    dc.b %00100010
    dc.b %01111111
    dc.b %01011011
    dc.b %01100111
    dc.b %00100110
    dc.b %11011111
    dc.b %10011110
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000011

SkraunP3F1_D1_face_ear_permanent_A_RIGHT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %10011110
    dc.b %11011111
    dc.b %00100110
    dc.b %01100111
    dc.b %01011011
    dc.b %01111111
    dc.b %00100010

SkraunP3F1_D1_face_ear_permanent_A_LEFT_TOP_FIRST:
    dc.b %01000100
    dc.b %11111110
    dc.b %11011010
    dc.b %11100110
    dc.b %01100100
    dc.b %11111011
    dc.b %01111001
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %11000011

SkraunP3F1_D1_face_ear_permanent_A_LEFT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %01111001
    dc.b %11111011
    dc.b %01100100
    dc.b %11100110
    dc.b %11011010
    dc.b %11111110
    dc.b %01000100

SkraunP3F1_D1_face_ear_permanent_B_RIGHT_TOP_FIRST:
    dc.b %00100010
    dc.b %01111111
    dc.b %01011011
    dc.b %01100111
    dc.b %00100110
    dc.b %01111111
    dc.b %00111101
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01100010
    dc.b %10000011

SkraunP3F1_D1_face_ear_permanent_B_RIGHT_BOTTOM_FIRST:
    dc.b %10000011
    dc.b %01100010
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %00111101
    dc.b %01111111
    dc.b %00100110
    dc.b %01100111
    dc.b %01011011
    dc.b %01111111
    dc.b %00100010

SkraunP3F1_D1_face_ear_permanent_B_LEFT_TOP_FIRST:
    dc.b %01000100
    dc.b %11111110
    dc.b %11011010
    dc.b %11100110
    dc.b %01100100
    dc.b %11111110
    dc.b %10111100
    dc.b %00111100
    dc.b %00111100
    dc.b %01100110
    dc.b %01000110
    dc.b %11000001

SkraunP3F1_D1_face_ear_permanent_B_LEFT_BOTTOM_FIRST:
    dc.b %11000001
    dc.b %01000110
    dc.b %01100110
    dc.b %00111100
    dc.b %00111100
    dc.b %10111100
    dc.b %11111110
    dc.b %01100100
    dc.b %11100110
    dc.b %11011010
    dc.b %11111110
    dc.b %01000100

SkraunP3F1_D2_shoulder_arm_permanent_A_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01100111
    dc.b %00111111
    dc.b %11011111
    dc.b %10011110
    dc.b %00111111
    dc.b %00111110
    dc.b %01100110
    dc.b %01000100
    dc.b %11000011

SkraunP3F1_D2_shoulder_arm_permanent_A_RIGHT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000100
    dc.b %01100110
    dc.b %00111110
    dc.b %00111111
    dc.b %10011110
    dc.b %11011111
    dc.b %00111111
    dc.b %01100111
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_D2_shoulder_arm_permanent_A_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %11100110
    dc.b %11111100
    dc.b %11111011
    dc.b %01111001
    dc.b %11111100
    dc.b %01111100
    dc.b %01100110
    dc.b %00100010
    dc.b %11000011

SkraunP3F1_D2_shoulder_arm_permanent_A_LEFT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %00100010
    dc.b %01100110
    dc.b %01111100
    dc.b %11111100
    dc.b %01111001
    dc.b %11111011
    dc.b %11111100
    dc.b %11100110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_D2_shoulder_arm_permanent_B_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %01100111
    dc.b %00111111
    dc.b %01111111
    dc.b %11011110
    dc.b %00111111
    dc.b %00111110
    dc.b %01100110
    dc.b %01100110
    dc.b %10000111

SkraunP3F1_D2_shoulder_arm_permanent_B_RIGHT_BOTTOM_FIRST:
    dc.b %10000111
    dc.b %01100110
    dc.b %01100110
    dc.b %00111110
    dc.b %00111111
    dc.b %11011110
    dc.b %01111111
    dc.b %00111111
    dc.b %01100111
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

SkraunP3F1_D2_shoulder_arm_permanent_B_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111110
    dc.b %01011010
    dc.b %11100110
    dc.b %11111100
    dc.b %11111110
    dc.b %01111011
    dc.b %11111100
    dc.b %01111100
    dc.b %01100110
    dc.b %01100110
    dc.b %11100001

SkraunP3F1_D2_shoulder_arm_permanent_B_LEFT_BOTTOM_FIRST:
    dc.b %11100001
    dc.b %01100110
    dc.b %01100110
    dc.b %01111100
    dc.b %11111100
    dc.b %01111011
    dc.b %11111110
    dc.b %11111100
    dc.b %11100110
    dc.b %01011010
    dc.b %01111110
    dc.b %00100100

