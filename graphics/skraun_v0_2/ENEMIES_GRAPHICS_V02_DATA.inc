; SKRAUN GRAPHICS V0.2 | P1 8x12 ART ONLY, UNAPPROVED, NOT STELLA
; Sword, bow and warning pose are art candidates; no P1 scheduler/CPU/RAM proof.

Enemy_knight_idle_TOP_FIRST:
    dc.b %00011000
    dc.b %00111100
    dc.b %00100100
    dc.b %00111100
    dc.b %01111101
    dc.b %11111111
    dc.b %11111100
    dc.b %00111100
    dc.b %00100100
    dc.b %01100110
    dc.b %01000010
    dc.b %11000011

Enemy_knight_idle_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000010
    dc.b %01100110
    dc.b %00100100
    dc.b %00111100
    dc.b %11111100
    dc.b %11111111
    dc.b %01111101
    dc.b %00111100
    dc.b %00100100
    dc.b %00111100
    dc.b %00011000

Enemy_knight_warning_TOP_FIRST:
    dc.b %00011001
    dc.b %00111101
    dc.b %00100101
    dc.b %00111101
    dc.b %01111101
    dc.b %11111111
    dc.b %11111100
    dc.b %00111100
    dc.b %00100100
    dc.b %01100110
    dc.b %01000010
    dc.b %11000011

Enemy_knight_warning_BOTTOM_FIRST:
    dc.b %11000011
    dc.b %01000010
    dc.b %01100110
    dc.b %00100100
    dc.b %00111100
    dc.b %11111100
    dc.b %11111111
    dc.b %01111101
    dc.b %00111101
    dc.b %00100101
    dc.b %00111101
    dc.b %00011001

Enemy_archer_idle_TOP_FIRST:
    dc.b %00011100
    dc.b %00111110
    dc.b %00101010
    dc.b %00011100
    dc.b %01011100
    dc.b %10111110
    dc.b %10111110
    dc.b %10111110
    dc.b %01011100
    dc.b %00010100
    dc.b %00100110
    dc.b %01100011

Enemy_archer_idle_BOTTOM_FIRST:
    dc.b %01100011
    dc.b %00100110
    dc.b %00010100
    dc.b %01011100
    dc.b %10111110
    dc.b %10111110
    dc.b %10111110
    dc.b %01011100
    dc.b %00011100
    dc.b %00101010
    dc.b %00111110
    dc.b %00011100

Enemy_archer_draw_TOP_FIRST:
    dc.b %00011100
    dc.b %00111110
    dc.b %00101010
    dc.b %00011100
    dc.b %01011100
    dc.b %10111110
    dc.b %11111111
    dc.b %10111110
    dc.b %01011100
    dc.b %00010100
    dc.b %00100110
    dc.b %01100011

Enemy_archer_draw_BOTTOM_FIRST:
    dc.b %01100011
    dc.b %00100110
    dc.b %00010100
    dc.b %01011100
    dc.b %10111110
    dc.b %11111111
    dc.b %10111110
    dc.b %01011100
    dc.b %00011100
    dc.b %00101010
    dc.b %00111110
    dc.b %00011100
