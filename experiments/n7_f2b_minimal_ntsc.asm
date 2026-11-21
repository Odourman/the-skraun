; THE SKRAUN - N7/F2b authorised, isolated physical diagnostic only.
; BASE: 4KiB NTSC, 6507 + true TIA. No mapper, full game or N8.
; P1 main and NUSIZ 3 close copies, one mid-line RESP1 re-trigger.
; This is a *falsification candidate*: a green DASM build is NOT a P1 PASS.
; S2 @ Scene=0, permuted S2 @ Scene=1, S3 P0 busy @ Scene=2.
; Source: MAIN III order / issue #31 (2026-11-21).
        processor 6502
VSYNC   = $00
VBLANK  = $01
WSYNC   = $02
NUSIZ0  = $04
NUSIZ1  = $05
COLUP0  = $06
COLUP1  = $07
COLUPF  = $08
COLUBK  = $09
CTRLPF  = $0A
REFP0   = $0B
REFP1   = $0C
PF0     = $0D
PF1     = $0E
PF2     = $0F
RESP0   = $10
RESP1   = $11
GRP0    = $1B
GRP1    = $1C
ENAM0   = $1D
ENABL   = $1F
HMP0    = $20
HMP1    = $21
VDELP1  = $26
HMOVE   = $2A
SWCHA   = $0280
SWCHB   = $0282
INTIM   = $0284
TIM64T  = $0296

Scene       = $80  ; debugger-settable after reset: 0=S2,1=permuted,2=S3
FrameNumber = $81
FirstColor  = $82
ThirdColor  = $83
P1RowA      = $90  ; $90..$9F, 16 double-rendered R3 source bytes
P1RowB      = $A0  ; $A0..$AF
P1RowC      = $B0  ; $B0..$BF

        SEG Code
        ORG $F000
Reset:
        sei
        cld
        ldx #$FF
        txs
        lda #0
        ldx #$7F
ZeroRAM:
        sta $80,x
        dex
        bpl ZeroRAM
        lda #0
        sta Scene
        sta PF0
        sta PF1
        sta PF2
        sta ENAM0
        sta ENABL
        sta COLUBK
        sta CTRLPF
        sta REFP0
        sta REFP1
        sta VDELP1
        sta HMP0
        sta HMP1
        lda #$07
        sta NUSIZ0
        lda #$03
        sta NUSIZ1

Frame:
        lda #2
        sta VBLANK
        sta VSYNC
        sta WSYNC
        sta WSYNC
        sta WSYNC
        lda #0
        sta VSYNC
        lda #43
        sta TIM64T
        inc FrameNumber
        jsr StageThree
        lda Scene
        cmp #2
        bcc P0Hidden
        lda #$0C
        bne P0Color
P0Hidden:
        lda #0
P0Color:
        sta COLUP0
        lda FirstColor
        sta COLUP1
        lda #0
        sta PF0
        sta PF1
        sta PF2
        sta COLUPF
        sta HMP1
        lda Scene
        cmp #2
        bcc NoP0Position
        lda #88    ; S3 Skraun centre X104, 32-colorclock-wide P0
        jsr PositionP0
NoP0Position:
        lda Scene
        cmp #2
        bcc S2P1Start
        lda #105
        bne P1StartReady
S2P1Start:
        lda #67
P1StartReady:
        jsr PositionP1
        sta WSYNC
        sta HMOVE
WaitVblank:
        lda INTIM
        bne WaitVblank
        sta WSYNC
        lda #0
        sta VBLANK
        ldy #16
HudBlank:
        sta WSYNC
        dey
        bne HudBlank

; 176 arena lines exactly: 78 preceding, 16 same-Y, 82 following.
        ldx #78
Top:
        sta WSYNC
        lda P0Top-1,x
        sta GRP0
        lda #0
        sta GRP1
        dex
        bne Top

; Critical *same-physical-line* attempt. One close-copy train (NUSIZ1=3)
; plus explicit RESP1 at cycle 53 (see static instruction schedule).
; The new main P1 position at end of previous line may disturb next line.
; No calls / RIOT RAM buffers in critical kernel. All three R3 8-row
; originals are re-used bit-exact with each source row replicated twice.
; First/second actor color same on normal S2/S3; Ranger has unique color.
; Forbidden to count fixed repeated bitmaps as individual actor PASS.
        ldx #16
P1Band:
        sta WSYNC
        lda P0Band-1,x
        sta GRP0
        lda P1RowA-1,x
        sta GRP1
        lda P1RowB-1,x
        ldy P1RowC-1,x
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        nop
        sta GRP1
        bit FrameNumber
        sta RESP1
        sty GRP1
        lda ThirdColor
        sta COLUP1
        lda FirstColor
        sta COLUP1
        dex
        bne P1Band

        ldx #82
Bottom:
        sta WSYNC
        lda P0Bottom-1,x
        sta GRP0
        lda #0
        sta GRP1
        dex
        bne Bottom

        lda #2
        sta VBLANK
        lda #0
        sta GRP0
        sta GRP1
        sta PF0
        sta PF1
        sta PF2
        ldx #30
Overscan:
        sta WSYNC
        dex
        bne Overscan
        jmp Frame

; Scene1 reverses R3 source first/last X placement; colors follow identity.
; Scene0 S2: K1@67, K2@83, Ranger@101.
; Scene1 permute: Ranger@67, K2@83, K1@101 (no Y shifting).
; Scene2 S3: K1@105, K2@124, Ranger@147, P0 L3 centre104.
; NUSIZ train alone is NOT free-X; the explicit RESP1 is intentionally tried.
StageThree:
        lda Scene
        cmp #1
        beq StagePermuted
        lda #$9E            ; light blue symbolic candidate, NOT final canon
        sta FirstColor
        lda #$C6            ; forest camouflage candidate, NOT final canon
        sta ThirdColor
        ldx #16
StageNormalLoop:
        lda R3K1Doubled-1,x
        sta P1RowA-1,x
        lda R3K2Doubled-1,x
        sta P1RowB-1,x
        lda R3RangerDoubled-1,x
        sta P1RowC-1,x
        dex
        bne StageNormalLoop
        rts
StagePermuted:
        lda #$C6
        sta FirstColor
        lda #$9E
        sta ThirdColor
        ldx #16
StagePermutedLoop:
        lda R3RangerDoubled-1,x
        sta P1RowA-1,x
        lda R3K2Doubled-1,x
        sta P1RowB-1,x
        lda R3K1Doubled-1,x
        sta P1RowC-1,x
        dex
        bne StagePermutedLoop
        rts

PositionP0:
        sta WSYNC
        sec
Pos0:
        sbc #15
        bcs Pos0
        eor #7
        asl
        asl
        asl
        asl
        sta HMP0
        sta RESP0
        rts
PositionP1:
        sta WSYNC
        sec
Pos1:
        sbc #15
        bcs Pos1
        eor #7
        asl
        asl
        asl
        asl
        sta HMP1
        sta RESP1
        rts

; Single chosen B/ON PF source masks retained as experiment REFERENCE DATA.
; After a deterministic P1 FAIL we must STOP, not silently claim P3 drawn.
; R3 row source98 -> arena y78/79, X80 and X84 respectively. Left PF0,1,2
; and right PF0,1,2 for each. This ROM DOES NOT emit these PF writes:
; P3 combined PF proof is explicitly untested unless P1 F2b first succeeds.
        ORG $F500
PF_B80_Left:   dc.b $00,$00,$0C
PF_B80_Right:  dc.b $40,$50,$00
PF_B84_Left:   dc.b $00,$00,$14
PF_B84_Right:  dc.b $40,$30,$00

        ORG $F700
P0Top:
; 78 entries, x=78..1, arena Y0..77
        dc.b $FE,$7C,$7C,$7C,$66,$66,$66,$5A,$5A,$5A,$7E,$7E
        dc.b $7E,$24,$24,$24
        ds 62,0
P0Band:
; 16 entries, x=16..1, arena Y78..93
        dc.b $C4,$C4,$64,$64,$64,$3C,$3C,$3C,$3C,$3C,$3C,$3D
        dc.b $3D,$3D,$FE,$FE
P0Bottom:
; 82 entries, x=82..1, arena Y94..175
        ds 78,0
        dc.b $06,$06,$06,$C4
        ORG $F800
R3K1Doubled:
        dc.b $42,$42,$66,$66,$24,$24,$5A,$5A,$DB,$DB,$7E,$7E
        dc.b $3C,$3C,$18,$18
R3K2Doubled:
        dc.b $81,$81,$66,$66,$3C,$3C,$7E,$7E,$DB,$DB,$5A,$5A
        dc.b $7E,$7E,$24,$24
R3RangerDoubled:
        dc.b $42,$42,$24,$24,$18,$18,$7E,$7E,$5A,$5A,$7E,$7E
        dc.b $3C,$3C,$18,$18
        ORG $FFFC
        dc.w Reset
        dc.w Reset
