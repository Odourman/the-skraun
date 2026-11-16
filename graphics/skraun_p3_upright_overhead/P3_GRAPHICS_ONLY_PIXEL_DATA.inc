; THE SKRAUN GRAPHICS P3 -- pixel source ONLY (NOT ROM / NOT STELLA)
; 8 bits per row, 12 rows. No processor instructions, bank changes, or raster kernel.
; TOP_FIRST: screen top row to bottom. BOTTOM_FIRST: reverse the 12 rows only.
; LEFT: exact horizontal flip of each row. NEVER use P1 prone anatomical orientation as current.
; 8-way joystick gameplay DOES NOT create up/down sprite assets.

SkraunP3_Control_Q1_prior_best_upright_A_RIGHT_TOP_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_A_RIGHT_BOTTOM_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_A_LEFT_TOP_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_A_LEFT_BOTTOM_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_B_RIGHT_TOP_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_B_RIGHT_BOTTOM_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_B_LEFT_TOP_FIRST:
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

SkraunP3_Control_Q1_prior_best_upright_B_LEFT_BOTTOM_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_A_RIGHT_TOP_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_A_RIGHT_BOTTOM_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_A_LEFT_TOP_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_A_LEFT_BOTTOM_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_B_RIGHT_TOP_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_B_RIGHT_BOTTOM_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_B_LEFT_TOP_FIRST:
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

SkraunP3_Control_P1_A_negative_prone_B_LEFT_BOTTOM_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_A_RIGHT_TOP_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_A_RIGHT_BOTTOM_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_A_LEFT_TOP_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_A_LEFT_BOTTOM_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_B_RIGHT_TOP_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_B_RIGHT_BOTTOM_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_B_LEFT_TOP_FIRST:
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

SkraunP3_Candidate_U1_upright_face_priority_B_LEFT_BOTTOM_FIRST:
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

SkraunP3_Candidate_U2_upright_body_priority_A_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %00111110
    dc.b %00110110
    dc.b %00011110
    dc.b %00111100
    dc.b %11111111
    dc.b %10011001
    dc.b %01111110
    dc.b %00111100
    dc.b %00100100
    dc.b %01100110
    dc.b %11000011

SkraunP3_Candidate_U2_upright_body_priority_A_RIGHT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100110
    dc.b %00100100
    dc.b %00111100
    dc.b %01111110
    dc.b %10011001
    dc.b %11111111
    dc.b %00111100
    dc.b %00011110
    dc.b %00110110
    dc.b %00111110
    dc.b %00100100

SkraunP3_Candidate_U2_upright_body_priority_A_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111100
    dc.b %01101100
    dc.b %01111000
    dc.b %00111100
    dc.b %11111111
    dc.b %10011001
    dc.b %01111110
    dc.b %00111100
    dc.b %00100100
    dc.b %01100110
    dc.b %11000011

SkraunP3_Candidate_U2_upright_body_priority_A_LEFT_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01100110
    dc.b %00100100
    dc.b %00111100
    dc.b %01111110
    dc.b %10011001
    dc.b %11111111
    dc.b %00111100
    dc.b %01111000
    dc.b %01101100
    dc.b %01111100
    dc.b %00100100

SkraunP3_Candidate_U2_upright_body_priority_B_RIGHT_TOP_FIRST:
    dc.b %00100100
    dc.b %00111110
    dc.b %00110110
    dc.b %00011110
    dc.b %00111100
    dc.b %01111111
    dc.b %10011011
    dc.b %11111100
    dc.b %00111100
    dc.b %00100100
    dc.b %01001110
    dc.b %10000111

SkraunP3_Candidate_U2_upright_body_priority_B_RIGHT_BOTTOM_FIRST:
    dc.b %10000111
    dc.b %01001110
    dc.b %00100100
    dc.b %00111100
    dc.b %11111100
    dc.b %10011011
    dc.b %01111111
    dc.b %00111100
    dc.b %00011110
    dc.b %00110110
    dc.b %00111110
    dc.b %00100100

SkraunP3_Candidate_U2_upright_body_priority_B_LEFT_TOP_FIRST:
    dc.b %00100100
    dc.b %01111100
    dc.b %01101100
    dc.b %01111000
    dc.b %00111100
    dc.b %11111110
    dc.b %11011001
    dc.b %00111111
    dc.b %00111100
    dc.b %00100100
    dc.b %01110010
    dc.b %11100001

SkraunP3_Candidate_U2_upright_body_priority_B_LEFT_BOTTOM_FIRST:
    dc.b %11100001
    dc.b %01110010
    dc.b %00100100
    dc.b %00111100
    dc.b %00111111
    dc.b %11011001
    dc.b %11111110
    dc.b %00111100
    dc.b %01111000
    dc.b %01101100
    dc.b %01111100
    dc.b %00100100
