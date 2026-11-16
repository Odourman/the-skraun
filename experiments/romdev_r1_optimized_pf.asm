; P02-R1 optimized asymmetric PF with PRECOMPOSED fixed-obstacle masks.
; Deduplicates 16 of 52 blocks (528 bytes ROM saved) by DASM aliases;
; preserves every original 33-byte mask pixel-exact. Independent color
; for ring and scenery is NOT created by this optimization.
; R1 scope only. This is NOT a fixed 8-level layout architecture.
; THE SKRAUN ROM DEVELOPMENT P02-B3b - independent joystick-follow prototype.
; Level 2 only. Genuine SWCHA horizontal motion; 13 centers in 4-color-clock increments.
; No SELECT-driven position changes. One step every 2 NTSC frames; R1-A responsive joystick diagnostic. Last horizontal
; position is bounded to diagnostic x=56..104 only; NOT a game-play screen limit.
; Y is fixed. P1 unused. CTRLPF=0. 6 PF register writes per scanline.
; Ring is a hollow ellipse (~40 TIA-clock wide, ~63 scanlines high).
; Display storage: 13 positions * 4 PF tables * 33 rows = 1716 ROM bytes;
; plus 192 row-map, 192 P0 sprite, 104 pointer bytes; no framebuffer.
; Obstacle variant: three fixed scenery columns x56,88,108 on y82..109 combined by OR in ROM masks; not collision logic.
; Same playfield color for ring and synthetic scenery: overlap merges visually.
        processor 6502
VSYNC       = $00
VBLANK      = $01
WSYNC       = $02
NUSIZ0      = $04
COLUP0      = $06
COLUPF      = $08
COLUBK      = $09
CTRLPF      = $0A
PF0         = $0D
PF1         = $0E
PF2         = $0F
RESP0       = $10
GRP0        = $1B
HMP0        = $20
HMOVE       = $2A
SWCHA       = $0280

Mode        = $80         ; 0..12, initial 6 -> TIA x=80
Frames      = $81         ; low bit gates 2-frame joystick response
L1Ptr       = $82
L2Ptr       = $84
R0Ptr       = $86
R1Ptr       = $88
; RAM $80..$89 = 10 bytes. No framebuffer.

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
        lda #6
        sta Mode
        lda #$0C
        sta COLUP0
        lda #$2E
        sta COLUPF
        lda #0
        sta CTRLPF
        sta COLUBK
        sta PF0
        sta PF1
        sta PF2
        lda #5
        sta NUSIZ0

Frame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC
        sta WSYNC                ; VBLANK scanline 1
        jsr UpdateMotion
        sta WSYNC                ; VBLANK scanline 2
        jsr SelectPtrs           ; 71 cycles, in one VBLANK scanline
        sta WSYNC                ; VBLANK scanline 3; prevent 87-cycle path overflow
        ldx Mode
        lda P0XTable,x
        jsr PositionP0           ; VBLANK scanline 4 (inside routine)
        sta WSYNC                ; VBLANK scanline 5
        sta HMOVE
        ldx #32
VBlankPad:
        sta WSYNC                ; VBLANK scanlines 6..37
        dex
        bne VBlankPad
        lda #0
        sta VBLANK

        ldx #192
Visible:
        sta WSYNC
        lda Troll2,x
        sta GRP0
        ldy RingRowMap,x
        lda #0
        sta PF0                 ; left PF0 unused
        lda (L1Ptr),y
        sta PF1
        lda (L2Ptr),y
        sta PF2
        lda (R0Ptr),y
        sta PF0                 ; right PF0 before right playfield begins
        lda (R1Ptr),y
        sta PF1
        lda #0
        sta PF2                 ; right PF2 unused
        dex
        bne Visible

        sta WSYNC               ; first overscan line (prevents 263-line frame)
        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        sta PF0
        sta PF1
        sta PF2
        ldx #29
Overscan:
        sta WSYNC               ; overscan lines 2..30
        dex
        bne Overscan
        jmp Frame

; SWCHA bit 7=0 right, bit 6=0 left. Both pressed -> no motion.
; Update 1 out of 2 frames at most; P0 and all 4 ring pointers update
; in the same VBLANK immediately before visible scanlines.
UpdateMotion:
        inc Frames
        lda Frames
        and #$01
        bne MoveDone
        lda SWCHA
        and #$C0
        cmp #$40
        beq MoveRight
        cmp #$80
        beq MoveLeft
MoveDone:
        rts
MoveRight:
        lda Mode
        cmp #12
        bcs MoveDone
        inc Mode
        rts
MoveLeft:
        lda Mode
        beq MoveDone
        dec Mode
        rts

; 8 lookup tables (13 positions each) stay within one ROM page;
; max fixed 71 cycles including JSR and RTS (no indexed page crossing).
SelectPtrs:
        ldx Mode
        lda L1Lo,x
        sta L1Ptr
        lda L1Hi,x
        sta L1Ptr+1
        lda L2Lo,x
        sta L2Ptr
        lda L2Hi,x
        sta L2Ptr+1
        lda R0Lo,x
        sta R0Ptr
        lda R0Hi,x
        sta R0Ptr+1
        lda R1Lo,x
        sta R1Ptr
        lda R1Hi,x
        sta R1Ptr+1
        rts

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

        ORG $F300
; Pointer low/high tables intentionally reside in one page.
L1Lo:
        dc.b <L1_56,<L1_60,<L1_64,<L1_68,<L1_72,<L1_76,<L1_80,<L1_84,<L1_88,<L1_92,<L1_96,<L1_100,<L1_104
L1Hi:
        dc.b >L1_56,>L1_60,>L1_64,>L1_68,>L1_72,>L1_76,>L1_80,>L1_84,>L1_88,>L1_92,>L1_96,>L1_100,>L1_104
L2Lo:
        dc.b <L2_56,<L2_60,<L2_64,<L2_68,<L2_72,<L2_76,<L2_80,<L2_84,<L2_88,<L2_92,<L2_96,<L2_100,<L2_104
L2Hi:
        dc.b >L2_56,>L2_60,>L2_64,>L2_68,>L2_72,>L2_76,>L2_80,>L2_84,>L2_88,>L2_92,>L2_96,>L2_100,>L2_104
R0Lo:
        dc.b <R0_56,<R0_60,<R0_64,<R0_68,<R0_72,<R0_76,<R0_80,<R0_84,<R0_88,<R0_92,<R0_96,<R0_100,<R0_104
R0Hi:
        dc.b >R0_56,>R0_60,>R0_64,>R0_68,>R0_72,>R0_76,>R0_80,>R0_84,>R0_88,>R0_92,>R0_96,>R0_100,>R0_104
R1Lo:
        dc.b <R1_56,<R1_60,<R1_64,<R1_68,<R1_72,<R1_76,<R1_80,<R1_84,<R1_88,<R1_92,<R1_96,<R1_100,<R1_104
R1Hi:
        dc.b >R1_56,>R1_60,>R1_64,>R1_68,>R1_72,>R1_76,>R1_80,>R1_84,>R1_88,>R1_92,>R1_96,>R1_100,>R1_104
P0XTable:
        dc.b $32,$36,$3A,$3E,$42,$46,$4A,$4E,$52,$56,$5A,$5E,$62

        ORG $F400
; Indexed by descending scanline X (191..0); outside ring points to
; row 32 of each compact 33-byte table. Within ring, mirrored about Y=95.5.
RingRowMap:
        dc.b $20              ; unreachable x=0 padding for 192..1 countdown
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$00,$01,$02,$03,$04,$05,$06,$07
        dc.b $08,$09,$0A,$0B,$0C,$0D,$0E,$0F,$10,$11,$12,$13
        dc.b $14,$15,$16,$17,$18,$19,$1A,$1B,$1C,$1D,$1E,$1F
        dc.b $1F,$1E,$1D,$1C,$1B,$1A,$19,$18,$17,$16,$15,$14
        dc.b $13,$12,$11,$10,$0F,$0E,$0D,$0C,$0B,$0A,$09,$08
        dc.b $07,$06,$05,$04,$03,$02,$01,$00,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
        dc.b $20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20,$20
Troll2:
        dc.b $00              ; unreachable x=0 padding for 192..1 countdown
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $C2,$C2,$46,$46,$64,$64,$7E,$7E,$3C,$3C,$9D,$9D
        dc.b $FD,$FD,$7E,$7E,$5A,$5A,$7E,$7E,$7E,$7E,$24,$24
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
L1_56:
        dc.b $00,$00,$00,$00,$01,$01,$01,$01,$03,$02,$02,$02
        dc.b $02,$02,$02,$04,$04,$04,$04,$04,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$00,$00,$00,$00
L2_56:
        dc.b $06,$06,$0F,$0F,$1F,$19,$10,$10,$30,$20,$20,$20
        dc.b $20,$20,$20,$40,$40,$40,$44,$44,$44,$44,$44,$44
        dc.b $44,$44,$44,$44,$44,$04,$04,$04,$00
R0_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_56:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$10,$10,$10,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$10,$10,$10,$00
L1_60:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$01,$01,$01,$01
        dc.b $01,$01,$01,$02,$02,$02,$02,$02,$02,$02,$02,$02
        dc.b $02,$02,$02,$02,$02,$00,$00,$00,$00
L2_60:
        dc.b $0C,$0C,$1E,$1E,$3F,$33,$21,$21,$61,$40,$40,$40
        dc.b $40,$40,$40,$80,$80,$80,$84,$84,$84,$84,$84,$84
        dc.b $84,$84,$84,$84,$84,$04,$04,$04,$00
R0_60 = R0_56    ; identical 33-byte mask reused without runtime cost
R1_60 = R1_56    ; identical 33-byte mask reused without runtime cost
L1_64:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$01,$01,$01,$01,$01,$01,$01,$01,$01
        dc.b $01,$01,$01,$01,$01,$00,$00,$00,$00
L2_64:
        dc.b $18,$18,$3C,$3C,$7E,$66,$42,$42,$C3,$81,$81,$81
        dc.b $81,$81,$81,$00,$00,$00,$04,$04,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$04,$04,$04,$00
R0_64:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$10,$10,$10,$50,$50,$50,$50,$50,$50
        dc.b $50,$50,$50,$50,$50,$40,$40,$40,$00
R1_64 = R1_56    ; identical 33-byte mask reused without runtime cost
L1_68:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00
L2_68:
        dc.b $30,$30,$78,$78,$FC,$CC,$84,$84,$86,$02,$02,$02
        dc.b $02,$02,$02,$01,$01,$01,$05,$05,$05,$05,$05,$05
        dc.b $05,$05,$05,$05,$05,$04,$04,$04,$00
R0_68:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$10,$10,$10,$10
        dc.b $10,$10,$10,$20,$20,$20,$60,$60,$60,$60,$60,$60
        dc.b $60,$60,$60,$60,$60,$40,$40,$40,$00
R1_68 = R1_56    ; identical 33-byte mask reused without runtime cost
L1_72 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_72:
        dc.b $60,$60,$F0,$F0,$F8,$98,$08,$08,$0C,$04,$04,$04
        dc.b $04,$04,$04,$02,$02,$02,$06,$06,$06,$06,$06,$06
        dc.b $06,$06,$06,$06,$06,$04,$04,$04,$00
R0_72:
        dc.b $00,$00,$00,$00,$10,$10,$10,$10,$30,$20,$20,$20
        dc.b $20,$20,$20,$40,$40,$40,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_72 = R1_56    ; identical 33-byte mask reused without runtime cost
L1_76 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_76:
        dc.b $C0,$C0,$E0,$E0,$F0,$30,$10,$10,$18,$08,$08,$08
        dc.b $08,$08,$08,$04,$04,$04,$04,$04,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$04,$04,$04,$00
R0_76:
        dc.b $00,$00,$10,$10,$30,$30,$20,$20,$60,$40,$40,$40
        dc.b $40,$40,$40,$80,$80,$80,$C0,$C0,$C0,$C0,$C0,$C0
        dc.b $C0,$C0,$C0,$C0,$C0,$40,$40,$40,$00
R1_76 = R1_56    ; identical 33-byte mask reused without runtime cost
L1_80 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_80:
        dc.b $80,$80,$C0,$C0,$E0,$60,$20,$20,$30,$10,$10,$10
        dc.b $10,$10,$10,$08,$08,$08,$0C,$0C,$0C,$0C,$0C,$0C
        dc.b $0C,$0C,$0C,$0C,$0C,$04,$04,$04,$00
R0_80:
        dc.b $10,$10,$30,$30,$70,$60,$40,$40,$C0,$80,$80,$80
        dc.b $80,$80,$80,$00,$00,$00,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_80:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$80,$80,$80,$90,$90,$90,$90,$90,$90
        dc.b $90,$90,$90,$90,$90,$10,$10,$10,$00
L1_84 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_84:
        dc.b $00,$00,$80,$80,$C0,$C0,$40,$40,$60,$20,$20,$20
        dc.b $20,$20,$20,$10,$10,$10,$14,$14,$14,$14,$14,$14
        dc.b $14,$14,$14,$14,$14,$04,$04,$04,$00
R0_84:
        dc.b $30,$30,$70,$70,$F0,$C0,$80,$80,$80,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_84:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80
        dc.b $80,$80,$80,$40,$40,$40,$50,$50,$50,$50,$50,$50
        dc.b $50,$50,$50,$50,$50,$10,$10,$10,$00
L1_88 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_88:
        dc.b $00,$00,$00,$00,$80,$80,$80,$80,$C0,$40,$40,$40
        dc.b $40,$40,$40,$20,$20,$20,$24,$24,$24,$24,$24,$24
        dc.b $24,$24,$24,$24,$24,$04,$04,$04,$00
R0_88:
        dc.b $60,$60,$F0,$F0,$F0,$90,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_88:
        dc.b $00,$00,$00,$00,$80,$80,$80,$80,$C0,$40,$40,$40
        dc.b $40,$40,$40,$20,$20,$20,$30,$30,$30,$30,$30,$30
        dc.b $30,$30,$30,$30,$30,$10,$10,$10,$00
L1_92 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_92:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$80,$80,$80,$80
        dc.b $80,$80,$80,$40,$40,$40,$44,$44,$44,$44,$44,$44
        dc.b $44,$44,$44,$44,$44,$04,$04,$04,$00
R0_92:
        dc.b $C0,$C0,$E0,$E0,$F0,$30,$10,$10,$10,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_92:
        dc.b $00,$00,$80,$80,$C0,$C0,$40,$40,$60,$20,$20,$20
        dc.b $20,$20,$20,$10,$10,$10,$10,$10,$10,$10,$10,$10
        dc.b $10,$10,$10,$10,$10,$10,$10,$10,$00
L1_96 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_96:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$80,$80,$80,$84,$84,$84,$84,$84,$84
        dc.b $84,$84,$84,$84,$84,$04,$04,$04,$00
R0_96:
        dc.b $80,$80,$C0,$C0,$E0,$60,$20,$20,$30,$10,$10,$10
        dc.b $10,$10,$10,$00,$00,$00,$40,$40,$40,$40,$40,$40
        dc.b $40,$40,$40,$40,$40,$40,$40,$40,$00
R1_96:
        dc.b $80,$80,$C0,$C0,$E0,$60,$20,$20,$30,$10,$10,$10
        dc.b $10,$10,$10,$08,$08,$08,$18,$18,$18,$18,$18,$18
        dc.b $18,$18,$18,$18,$18,$10,$10,$10,$00
L1_100 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_100:
        dc.b $00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00,$00
        dc.b $00,$00,$00,$00,$00,$00,$04,$04,$04,$04,$04,$04
        dc.b $04,$04,$04,$04,$04,$04,$04,$04,$00
R0_100:
        dc.b $00,$00,$80,$80,$C0,$C0,$40,$40,$60,$20,$20,$20
        dc.b $20,$20,$20,$10,$10,$10,$50,$50,$50,$50,$50,$50
        dc.b $50,$50,$50,$50,$50,$40,$40,$40,$00
R1_100:
        dc.b $C0,$C0,$E0,$E0,$F0,$30,$10,$10,$18,$08,$08,$08
        dc.b $08,$08,$08,$04,$04,$04,$14,$14,$14,$14,$14,$14
        dc.b $14,$14,$14,$14,$14,$10,$10,$10,$00
L1_104 = L1_68    ; identical 33-byte mask reused without runtime cost
L2_104 = L2_100    ; identical 33-byte mask reused without runtime cost
R0_104:
        dc.b $00,$00,$00,$00,$80,$80,$80,$80,$C0,$40,$40,$40
        dc.b $40,$40,$40,$20,$20,$20,$60,$60,$60,$60,$60,$60
        dc.b $60,$60,$60,$60,$60,$40,$40,$40,$00
R1_104:
        dc.b $60,$60,$F0,$F0,$F8,$98,$08,$08,$0C,$04,$04,$04
        dc.b $04,$04,$04,$02,$02,$02,$12,$12,$12,$12,$12,$12
        dc.b $12,$12,$12,$12,$12,$10,$10,$10,$00

        ORG $FFFC
        dc.w Reset
        dc.w Reset
