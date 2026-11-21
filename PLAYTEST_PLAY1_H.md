# PLAY1-H – PLAYTEST, faktisk Atari 2600-ROM (2026-11-21)

**Status: PLAY1_H_PARTIAL (DEVELOPER_OBSERVED).** Fryst PLAY1 bas SHA 8247a3ba2b723c88336b63d5666503bed72cf2af. Exakt auktorisation i GitHub Issue #36 samt MAIN III:s bindande PLAY1-H-order. Inte oberoende Verification.

## Spela
Bygg och starta i Stella:
    dasm experiments/play1_h_single_arena.asm -f3 -obuild/play1h/play1h.bin -lbuild/play1h/play1h.lst -sbuild/play1h/play1h.sym
Styr Skraun med joystick i åtta riktningar, glid längs de fyra fasta syntetiska hindren. Flytta höger cirka 16 rutor och ned cirka 24 från x80/y88 till BL-orben x96/y112; verklig positionskontakt ger L1→L2. Efter 90 bildrutor kan orben återkomma och ge L2→L3. SELECT är en kvarvarande debughjälp, INTE orbersättning. Håll FIRE för 30-rutors halo, rör dig under aktiv attack och besegra den enda stationära R3 P1-träningsriddaren på level3. Ingen fiende-AI, Ranger eller slutgiltig värld.

**Begränsning:** Den synliga nivåberoende guld-PF2-konturen flyttar sig i Y med PlayerY och uppdateras per frame, men förblir fixerad i X. Den logiska attacken följer i båda axlarna. Därför är PLAY1-H inte fullständigt godkänd.

## Reproducera riktiga screenshots
    sudo apt-get install -y dasm stella xvfb xdotool scrot python3-pil python3-numpy
    mkdir -p build/play1h
    dasm experiments/play1_h_single_arena.asm -f3 -obuild/play1h/play1h.bin -lbuild/play1h/play1h.lst -sbuild/play1h/play1h.sym
    bash scripts/play1h_stella_abc.sh
    /usr/bin/python3 tests/play1h_pixels.py

Åtta verkliga Stella 6.7.1-lägen fångas med riktiga debuggerjoystickkommandon, inga PlayerX/Y-/level-/halo-RAM-injektioner: baseline, pickup_L2_off, L1_on, L2_on, A_L3_on, B_L3_right8, C_L3_right8_up8, D_L3_right8_down8. Varje scenario ger 1400x1000 GUI- och 320x228 TIA RGB-fångst, faktisk skärm-/formatlogg och spelkontrollscript. X-rörelse måste skilja ringen från P0-ocklusion; Y-effekt måste jämföras utanför P0/P1. En faktisk 262-raders NTSC-frame bör granskas från skärmlogg/debugger med verkliga scanlineindex (ej hävdad full per-instruktionstrace).

## Gränser och negativ kontroll
Den frivilligt testade X-kandidaten ändrade TIA:s CTRLPF mirror/repeat vid PlayerX>=100. Dess riktiga Stella-bilder visade 64 ändrade guldpixlar på en fast övre hinder-rad, P0 level2 32x34 i stället för 32x24 och P1 144 i stället för exakt 120 blå pixlar. **X-försöket förkastades och reverterades** till varianten som följer Y och bevarar testarenan. Det är ett lokalt teknik-Fail, inte universell omöjlighet. Tidigare B3b:s 16-framesuppdatering har inte använts.

PLAY1:s fyra solida hinder, U1-LEG1 original A/B, nivå1 8x12, nivå2 16x24, nivå3 32x36, orben och FIRE samt en P1 R3 knight finns som exakt avgränsad prototype. RIOT statisk variabelallokering $80..$A9 (42 bytes) plus härledd return-stack upp till4 bytes; fysisk highwater EJ MÄTT. Synliga kerneln får inte bedömas beam-säker för alla positioner enbart på grön CI; indirekta Y-korsningar kan förbruka extra 6507-cykler. L3-hinder, orbbindning och P1 kräver bilderna, inte pappersantaganden.

## Stopp
Leverans till MAIN III via Issue #36, separat draft PR, ingen main-merge. Inget N8/N9, mapperbyte, ny grafik eller vidare automatiskt steg.