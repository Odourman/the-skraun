; THE SKRAUN - GRAY OVERHEAD ART EXPERIMENT (P01-based NTSC)
; Atari 2600 / MOS 6507, plain 4 KiB ROM, DASM 2.20.x.
; Scope: overhead light-gray monster, 2 poses, mirrored left/right; 3 sizes.
; NOT a replacement for P01; separate experiment pending visual and independent testing.
; Controls: joystick port 0 moves, console SELECT cycles levels.
; All TIA/RIOT symbols are defined here; no external includes.

        processor 6502

VSYNC       = $00
VBLANK      = $01
WSYNC       = $02
NUSIZ0      = $04
COLUP0      = $06
COLUBK      = $09
RESP0       = $10
GRP0        = $1B
HMP0        = $20
HMOVE       = $2A
SWCHA       = $0280
SWCHB       = $0282

PlayerX     = $80           ; coarse left edge, clamped for 32px sprite
PlayerY     = $81           ; bottom row in reversed visible-line index
Level       = $82           ; 1..3 (SELECT button; test-only)
JoyState    = $83
SwitchState = $84
PrevSelect  = $85           ; press-edge latch
Phase       = $86           ; 0,1,2; skips one of 3 diagonal updates
DiagonalSkip= $87
SpriteHeight= $88           ; 12,24,36 scanlines
RowMapPtr   = $89           ; 2-byte zero-page pointer
GfxPtr      = $8B           ; 2-byte zero-page pointer
FrameCount  = $8D
Facing      = $8E           ; 0 right, 1 left, persists on up/down inputs

        SEG Code
        ORG $F000

Reset:
        sei
        cld
        ldx #$FF
        txs
        lda #0
        ldx #$7F
ClearRAM:
        sta $80,x
        dex
        bpl ClearRAM

        ldx #$2C
ClearTIA:
        sta $00,x
        dex
        bpl ClearTIA

        lda #64
        sta PlayerX
        lda #80
        sta PlayerY
        lda #1
        sta Level
        lda #$0C             ; NTSC neutral light gray; black eye holes
        sta COLUP0
        lda #$00
        sta COLUBK

MainFrame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC           ; exactly 3 VSYNC scanlines
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC

; VBLANK, exactly 37 WSYNC lines.
; Every bounded routine has its own line; avoid accidental line spills.
        lda SWCHA
        sta JoyState
        lda SWCHB
        sta SwitchState
        inc FrameCount
        inc Phase
        lda Phase
        cmp #3
        bne PhaseReady
        lda #0
        sta Phase
PhaseReady:
        sta WSYNC           ; VBLANK line 1

        jsr DetectDiagonal
        sta WSYNC           ; 2
        jsr MoveHorizontal
        sta WSYNC           ; 3
        jsr MoveVertical
        sta WSYNC           ; 4
        jsr UpdateLevel
        sta WSYNC           ; 5
        jsr UpdateScale
        sta WSYNC           ; 6
        jsr UpdateFacing
        sta WSYNC           ; 7
        jsr UpdateAnimation
        sta WSYNC           ; 8
        lda PlayerX
        jsr PositionP0      ; 9 (routine owns WSYNC)
        sta WSYNC           ; 10
        sta HMOVE           ; apply fine motion in HBLANK

        ldx #27
VblankPad:
        sta WSYNC           ; lines 11..37
        dex
        bne VblankPad

        lda #0
        sta VBLANK
        ldx #192
VisibleLoop:
        sta WSYNC           ; one scanline per iteration
        txa
        sec
        sbc PlayerY
        bcc HideSprite
        cmp SpriteHeight
        bcs HideSprite
        tay
        lda (RowMapPtr),y
        tay
        lda (GfxPtr),y
        sta GRP0
        jmp NextRow
HideSprite:
        lda #0
        sta GRP0
NextRow:
        dex
        bne VisibleLoop

        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        ldx #30
Overscan:
        sta WSYNC           ; exactly 30 overscan scanlines
        dex
        bne Overscan
        jmp MainFrame       ; 3 + 37 + 192 + 30 = 262 NTSC

; Avoid diagonal speed bonus: when BOTH axes are held,
; move on two of three frames. Speed = ~0.943 of axial.
DetectDiagonal:
        lda #0
        sta DiagonalSkip
        lda JoyState
        and #$C0
        cmp #$C0
        beq NoDiagonal
        lda JoyState
        and #$30
        cmp #$30
        beq NoDiagonal
        lda Phase
        cmp #2
        bne NoDiagonal
        lda #1
        sta DiagonalSkip
NoDiagonal:
        rts

; SWCHA port 0: bit 7 right, 6 left, 5 down, 4 up, active low.
MoveHorizontal:
        lda DiagonalSkip
        bne HorizontalDone
        lda JoyState
        and #$40
        beq GoLeft
        lda JoyState
        and #$80
        bne HorizontalDone
        lda PlayerX
        cmp #118
        bcs HorizontalDone
        inc PlayerX
        rts
GoLeft:
        lda PlayerX
        cmp #12
        bcc HorizontalDone
        beq HorizontalDone
        dec PlayerX
HorizontalDone:
        rts

MoveVertical:
        lda DiagonalSkip
        bne VerticalDone
        lda JoyState
        and #$10
        beq GoUp
        lda JoyState
        and #$20
        bne VerticalDone
        lda PlayerY
        cmp #10
        bcc VerticalDone
        beq VerticalDone
        dec PlayerY
        rts
GoUp:
        lda PlayerY
        cmp #150
        bcs VerticalDone
        inc PlayerY
VerticalDone:
        rts

; SWCHB bit 1 is the console SELECT switch, active low.
UpdateLevel:
        lda SwitchState
        and #2
        bne SelectReleased
        lda PrevSelect
        bne SelectDone
        lda #1
        sta PrevSelect
        inc Level
        lda Level
        cmp #4
        bne SelectDone
        lda #1
        sta Level
SelectDone:
        rts
SelectReleased:
        lda #0
        sta PrevSelect
        rts

; NUSIZ0 0=8-pixel, 5=16-pixel, 7=32-pixel player.
; Vertical size uses explicit 12-row repetition tables.
UpdateScale:
        lda Level
        cmp #1
        bne ScaleTwoOrThree
        lda #12
        sta SpriteHeight
        lda #0
        sta NUSIZ0
        lda #<MapSmall
        sta RowMapPtr
        lda #>MapSmall
        sta RowMapPtr+1
        rts
ScaleTwoOrThree:
        cmp #2
        bne ScaleThree
        lda #24
        sta SpriteHeight
        lda #5
        sta NUSIZ0
        lda #<MapMedium
        sta RowMapPtr
        lda #>MapMedium
        sta RowMapPtr+1
        rts
ScaleThree:
        lda #36
        sta SpriteHeight
        lda #7
        sta NUSIZ0
        lda #<MapLarge
        sta RowMapPtr
        lda #>MapLarge
        sta RowMapPtr+1
        rts

; No separate up/down facing. Last left/right state persists on vertical
; movement. Both upper arms and hind legs cycle through two poses.
; Joystick left and right are active-low SWCHA bits 6 and 7.
UpdateFacing:
        lda JoyState
        and #$40
        bne CheckRightFacing
        lda #1
        sta Facing
        rts
CheckRightFacing:
        lda JoyState
        and #$80
        bne FacingUnchanged
        lda #0
        sta Facing
FacingUnchanged:
        rts

; Select one of four frames via a ROM pointer table.
; Facing=0/1 (right/left), pose=0/1 (A/B when moving).
; Vertical movement animates but does not select a new orientation.
UpdateAnimation:
        lda JoyState
        and #$F0
        cmp #$F0
        beq StationaryPose
        lda FrameCount
        and #$08
        beq StationaryPose
        lda #1
        bne PoseChosen
StationaryPose:
        lda #0
PoseChosen:
        sta GfxPtr
        lda Facing
        asl
        ora GfxPtr
        asl
        tax
        lda PosePointerTable,x
        sta GfxPtr
        lda PosePointerTable+1,x
        sta GfxPtr+1
        rts

; Standard coarse/fine TIA positioning (15-color-clock groups).
; Caller applies HMOVE after the next WSYNC, during HBLANK.
PositionP0:
        sta WSYNC
        sec
PositionLoop:
        sbc #15
        bcs PositionLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP0
        sta RESP0
        rts

; Authoring source (top to bottom) is the project visual sprite spec.
; Sprite data below is stored bottom to top for the P01 visible kernel.
; P0 8-bit TIA player is scaled by NUSIZ0 for levels 1-3.
; No P1 usage. The two face holes are the dark background.
PosePointerTable:
        dc.w GfxRightA, GfxRightB, GfxLeftA, GfxLeftB
GfxRightA:
        dc.b %11000010
        dc.b %01000110
        dc.b %01100100
        dc.b %01111110
        dc.b %00111100
        dc.b %10011101
        dc.b %11111101
        dc.b %01111110
        dc.b %01011010
        dc.b %01111110
        dc.b %01111110
        dc.b %00100100

GfxRightB:
        dc.b %10000011
        dc.b %01100010
        dc.b %00100110
        dc.b %01111110
        dc.b %10111101
        dc.b %00111101
        dc.b %10111011
        dc.b %11111111
        dc.b %01011010
        dc.b %01111110
        dc.b %01111110
        dc.b %00100100

GfxLeftA:
        dc.b %01000011
        dc.b %01100010
        dc.b %00100110
        dc.b %01111110
        dc.b %00111100
        dc.b %10111001
        dc.b %10111111
        dc.b %01111110
        dc.b %01011010
        dc.b %01111110
        dc.b %01111110
        dc.b %00100100

GfxLeftB:
        dc.b %11000001
        dc.b %01000110
        dc.b %01100100
        dc.b %01111110
        dc.b %10111101
        dc.b %10111100
        dc.b %11011101
        dc.b %11111111
        dc.b %01011010
        dc.b %01111110
        dc.b %01111110
        dc.b %00100100
; Sub-index mapping: 1x, 2x or 3x vertical replication.
MapSmall:
        dc.b 0,1,2,3,4,5,6,7,8,9,10,11
MapMedium:
        dc.b 0,0,1,1,2,2,3,3,4,4,5,5
        dc.b 6,6,7,7,8,8,9,9,10,10,11,11
MapLarge:
        dc.b 0,0,0,1,1,1,2,2,2,3,3,3
        dc.b 4,4,4,5,5,5,6,6,6,7,7,7
        dc.b 8,8,8,9,9,9,10,10,10,11,11,11

        ORG $FFFC
        dc.w Reset
        dc.w Reset
