; THE SKRAUN - P02 EXPERIMENT A: P1 HALO (NTSC)
; Atari 2600 / MOS 6507, plain 4 KiB ROM, DASM 2.20.x.
; Scope: P01 movement + 360-degree P1 halo arcs, 3 scales, fire timing.
; DIAGNOSTIC ONLY. P1 is reserved for halo, so future enemy cost is severe.
; Controls: stick moves; SELECT changes level; FIRE triggers ~30-frame halo.
; All TIA/RIOT symbols are defined here; no external includes.

        processor 6502

VSYNC       = $00
VBLANK      = $01
WSYNC       = $02
NUSIZ0      = $04
NUSIZ1      = $05
COLUP0      = $06
COLUP1      = $07
COLUBK      = $09
RESP0       = $10
RESP1       = $11
GRP0        = $1B
GRP1        = $1C
HMP0        = $20
HMP1        = $21
HMOVE       = $2A
SWCHA       = $0280
SWCHB       = $0282
INPT4       = $3C

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
HaloTimer   = $8E
HaloCooldown= $8F
HaloX       = $90
HaloBottom  = $91
HaloHeight  = $92
HaloMapPtr  = $93          ; 2-byte pointer

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
        lda #$C8             ; dark green troll; black eye holes
        sta COLUP0
        lda #$2E             ; golden magical ring, separate P1 object
        sta COLUP1
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
        jsr UpdateAnimation
        sta WSYNC           ; 7
        jsr UpdateHaloState
        sta WSYNC           ; 8
        jsr UpdateHaloScale
        sta WSYNC           ; 9
        jsr UpdateHaloPosition
        sta WSYNC           ; 10
        lda PlayerX
        jsr PositionP0      ; 11 (routine owns WSYNC)
        sta WSYNC           ; 12
        lda HaloX
        jsr PositionP1      ; 13 (routine owns WSYNC)
        sta WSYNC           ; 14
        sta HMOVE           ; apply both fine-motion offsets in HBLANK
        lda #0
        sta GRP1            ; clear stale P1 graphics between halo activations

        ldx #23
VblankPad:
        sta WSYNC           ; lines 15..37
        dex
        bne VblankPad

        lda #0
        sta VBLANK
        ldx #192
VisibleLoop:
        sta WSYNC           ; one scanline per iteration
        ; Independent P02-A diagnostic kernel: when the halo is active,
        ; alternate which graphic object gets updated on each scanline.
        ; The other graphic register holds its previous line's pixels.
        ; This avoids a 76-cycle overrun but halves vertical update rate.
        lda HaloHeight
        beq DrawTroll
        txa
        and #1
        beq DrawTroll
DrawHalo:
        txa
        sec
        sbc HaloBottom
        bcc HideHalo
        cmp HaloHeight
        bcs HideHalo
        tay
        lda (HaloMapPtr),y
        tay
        lda HaloGfx,y
        sta GRP1
        jmp NextRow
HideHalo:
        lda #0
        sta GRP1
        jmp NextRow
DrawTroll:
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
        sta GRP1
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

; Alternate two back-leg silhouettes during movement only.
UpdateAnimation:
        lda JoyState
        and #$F0
        cmp #$F0
        beq UseIdle
        lda FrameCount
        and #$08
        beq UseIdle
        lda #<GfxWalking
        sta GfxPtr
        lda #>GfxWalking
        sta GfxPtr+1
        rts
UseIdle:
        lda #<GfxIdle
        sta GfxPtr
        lda #>GfxIdle
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

; Graphics are stored from bottom (two small legs) to top.
; Holes in two rows show the black background as eyes.
GfxIdle:
        dc.b %00100100
        dc.b %00100100
        dc.b %01100110
        dc.b %01100110
        dc.b %11111111
        dc.b %11111111
        dc.b %11011011
        dc.b %11011011
        dc.b %11111111
        dc.b %01111110
        dc.b %00111100
        dc.b %00011000

GfxWalking:
        dc.b %01000010
        dc.b %01100110
        dc.b %01100110
        dc.b %01100110
        dc.b %11111111
        dc.b %11111111
        dc.b %11011011
        dc.b %11011011
        dc.b %11111111
        dc.b %01111110
        dc.b %00111100
        dc.b %00011000

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

; A 30-frame active ring followed by fixed cooldown, held FIRE repeats.
; This logic is provisional P02 timing and does not change MAIN decisions.
UpdateHaloState:
        lda HaloTimer
        beq HaloInactive
        dec HaloTimer
        bne HaloDone
        lda Level
        cmp #1
        bne HaloCooldown2
        lda #60
        bne SetHaloCooldown
HaloCooldown2:
        cmp #2
        bne HaloCooldown3
        lda #36
        bne SetHaloCooldown
HaloCooldown3:
        lda #15
SetHaloCooldown:
        sta HaloCooldown
        rts
HaloInactive:
        lda HaloCooldown
        beq HaloCheckFire
        dec HaloCooldown
        rts
HaloCheckFire:
        lda INPT4
        bmi HaloDone
        lda #30
        sta HaloTimer
HaloDone:
        rts

; Width in the horizontal axis cannot exceed 32 logical pixels with P1.
; At level 3 this is NOT wider than the 32-pixel troll; deliberate stress.
UpdateHaloScale:
        lda HaloTimer
        beq HaloDisabled
        lda Level
        cmp #1
        bne HaloShape2
        lda #5
        sta NUSIZ1
        lda #20
        sta HaloHeight
        lda #<RingSmallMap
        sta HaloMapPtr
        lda #>RingSmallMap
        sta HaloMapPtr+1
        rts
HaloShape2:
        cmp #2
        bne HaloShape3
        lda #7
        sta NUSIZ1
        lda #32
        sta HaloHeight
        lda #<RingMediumMap
        sta HaloMapPtr
        lda #>RingMediumMap
        sta HaloMapPtr+1
        rts
HaloShape3:
        lda #7
        sta NUSIZ1
        lda #48
        sta HaloHeight
        lda #<RingLargeMap
        sta HaloMapPtr
        lda #>RingLargeMap
        sta HaloMapPtr+1
        rts
HaloDisabled:
        lda #0
        sta HaloHeight
        rts

UpdateHaloPosition:
        lda Level
        cmp #1
        bne HaloPos2
        lda PlayerX
        sec
        sbc #4
        sta HaloX
        lda PlayerY
        sec
        sbc #4
        sta HaloBottom
        rts
HaloPos2:
        cmp #2
        bne HaloPos3
        lda PlayerX
        sec
        sbc #8
        sta HaloX
        lda PlayerY
        sec
        sbc #4
        sta HaloBottom
        rts
HaloPos3:
        lda PlayerX
        sta HaloX
        lda PlayerY
        sec
        sbc #6
        sta HaloBottom
        rts

PositionP1:
        sta WSYNC
        sec
P1PositionLoop:
        sbc #15
        bcs P1PositionLoop
        eor #7
        asl
        asl
        asl
        asl
        sta HMP1
        sta RESP1
        rts

; The P1 raster ring is 8 bitmap columns stretched to 16/32 pixels.
; Its max width is fundamentally insufficient for a 32px-wide level-3 troll.
HaloGfx:
        dc.b %00011000
        dc.b %00100100
        dc.b %01100110
        dc.b %01000010
        dc.b %11000011
        dc.b %10000001
        dc.b %10000001
        dc.b %10000001
        dc.b %10000001
        dc.b %10000001
        dc.b %10000001
        dc.b %11000011
        dc.b %01000010
        dc.b %01100110
        dc.b %00100100
        dc.b %00011000
RingSmallMap:
        dc.b 0,0,1,2,3,4,5,6,7,7,8,8,9,10,11,12,13,14,15,15
RingMediumMap:
        dc.b 0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7
        dc.b 8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15
RingLargeMap:
        dc.b 0,0,0,1,1,1,2,2,2,3,3,3,4,4,4,5,5,5
        dc.b 6,6,6,7,7,7,8,8,8,9,9,9,10,10,10
        dc.b 11,11,11,12,12,12,13,13,13,14,14,14,15,15,15

        ORG $FFFC
        dc.w Reset
        dc.w Reset
