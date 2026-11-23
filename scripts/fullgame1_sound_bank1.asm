; FULLGAME-1 F6 bank1: two distinct TIA audio channels with 12f envelopes
; Channel0 gets event $10..$90; channel1 event $A0..$F0.
; Request $BF: highest event priority in frame; voice state $EE/$EF:
; upper nibble = sound ID, lower nibble = remaining frames.
; Both voice bytes are located below hardware stack $F0-$FF.
; $EE was WorldShift only during map setup, after which it is reusable.
; $EF was AuxMode; actor init mailbox moves to $EB.
        processor 6502
AUDC0     = $15
AUDC1     = $16
AUDF0     = $17
AUDF1     = $18
AUDV0     = $19
AUDV1     = $1A
SoundReq  = $BF
Voice0    = $EE
Voice1    = $EF
        SEG AudioCode
        ORG $F000
AudioCold:
        lda $FFF9
        jmp $F000
        ORG $F100
AudioEngine:
        lda SoundReq
        beq NoNewEvent
        cmp #$A0
        bcs QueueVoice1
QueueVoice0:
        lda Voice0
        and #$F0
        cmp SoundReq
        bcs ClearRequest
        lda SoundReq
        ora #$0C
        sta Voice0
        jmp ClearRequest
QueueVoice1:
        lda Voice1
        and #$F0
        cmp SoundReq
        bcs ClearRequest
        lda SoundReq
        ora #$0C
        sta Voice1
ClearRequest:
        lda #0
        sta SoundReq
NoNewEvent:
        lda Voice0
        and #$0F
        beq MuteVoice0
        tay
        dec Voice0
        lda Voice0
        and #$F0
        lsr
        lsr
        lsr
        lsr
        tax
        lda AudioTypes,x
        sta AUDC0
        tya
        lsr
        lsr
        clc
        adc AudioPitches,x
        and #$1F
        sta AUDF0
        lda AudioEnvelope,y
        sta AUDV0
        jmp TickVoice1
MuteVoice0:
        lda #0
        sta Voice0
        sta AUDV0
TickVoice1:
        lda Voice1
        and #$0F
        beq MuteVoice1
        tay
        dec Voice1
        lda Voice1
        and #$F0
        lsr
        lsr
        lsr
        lsr
        tax
        lda AudioTypes,x
        sta AUDC1
        tya
        lsr
        lsr
        clc
        adc AudioPitches,x
        and #$1F
        sta AUDF1
        lda AudioEnvelope,y
        cpx #11           ; sword warning: two separated urgent pulses
        bne VolumeVoice1
        cpy #7
        bcs VolumeVoice1
        cpy #4
        bcc VolumeVoice1
        lda #0
VolumeVoice1:
        sta AUDV1
        jmp AudioReturn
MuteVoice1:
        lda #0
        sta Voice1
        sta AUDV1
AudioReturn:
        jmp AudioBankReturn
AudioTypes:
        dc.b 0,4,4,6,8,12,6,1,12,8,12,1,8,12,6,4
AudioPitches:
        dc.b 0,24,20,15,18,16,24,29,12,27,10,10,8,5,16,12
AudioEnvelope:
        dc.b 0,1,2,3,4,5,6,7,8,8,9,10,10,10,10,10

        ORG $F6E3
AudioEntryTrampoline:
        jmp AudioEngine
        ORG $F6EA
AudioBankReturn:
        lda $FFF8       ; bank2 next fetch $F6ED is an RTS
        ORG $FFFC
        dc.w AudioCold
        dc.w AudioCold
