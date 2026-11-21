# THE SKRAUN – PLAY1 enarenaprototyp: PLAYTEST och teknisk reproduktion
**2026-11-21 | ROM DEVELOPMENT II | endast uttryckligt godkänt PLAY1 #34 | DEVELOPER_OBSERVED, inte independent Verification**

## Spela på Stella 6.7.1 eller motsvarande NTSC/4K-kompatibel Atari 2600-emulator
Ladda `experiments/play1_single_arena.bin` när den har byggts från källan. Det här är **EN syntetisk öppen fyrhindersarena**, inte en av de åtta slutbanorna. Inga P1-fiende-AI, svärd, ranger, pilar eller kommande N8/N9 finns.

**Kontroller:** joystick 8 riktningar: flytta Skraun. Hinder är solida, diagonala rörelser får glida längs den fria axeln enligt COL1 K0. FIRE: håll inne för att aktivera en cirka 30-frames magisk attack; Skraun kan fortsätta röra sig under attack. SELECT är kvar från COL1 som **explicit debuggerhjälp** för att pröva säker tillväxt; det är INTE riktig orbpickup och ska inte användas som bevis för det.

**Spelloop att prova:**
1. Från start x80/y88, level1, rör joystick höger cirka 16 rutor och ned cirka 24 rutor. Den lilla BL-orben finns omkring x96/y112 och **faktisk positionskontakt** uppgraderar level 1→2 efter fullstorlekssäker `CandidateValid`.
2. Stanna kvar kring orben. Den förbrukade orben återaktiveras på sin fasta position efter 90 NTSC-rutor; en ny verklig kontakt ger level2→3 när området är säkert. Ingen kan växa över level3. Orb kan senare ligga kvar synlig om spelaren redan är level3.
3. På level3 vid ca x96/y112, tryck FIRE. TEST B färgar hela arena-PF guld, orb delar `COLUPF`; en extra gul PF2-ring syns. Rör Skraun under attack. Den blå stationära R3-knight-dummyn vid x125/y96 träffas logiskt när Skraun är inom level3-radien, försvinner och ger en kort röd bakgrundsflash.
4. Starta om ROM om du vill upprepa den engångsövningen; det finns ingen fullspels-loop/fiendespawn.

**OBSERVERA EN VIKTIG KÄND VISUELL BRIST:** PF2-ringens faktiska geometri är i denna snabbprototyp fortfarande centrerad på den fasta arenapositionen x80/y112. Logisk 360-graders attack och guld-PF är kodade och aktiveras under rörelse, men **den synliga PF-konturen följer inte Skrauns X/Y**. Därför får denna ROM inte märkas fullt godkänd PLAY1, även om joystick/orb/target fungerar i Stella. PF2 på Atari är spegelgeometri och kräver annan dynamisk scheduling för en över hela arenan korrekt följsam 360-kontur. Inget sådant senare rendererarbete är auktoriserat genom detta PLAY1-resultat. Haloens ytterradie/tjocklek via `HaloVisualMask` växer i den **fasta** diagnostiska PF-konturen, men den följer inte logisk PlayerX/Y.

## Reproducera original-DASM-bygget
```sh
sudo apt-get install -y dasm stella xvfb xdotool scrot python3-pil
mkdir -p build/play1
dasm experiments/play1_single_arena.asm -f3 -obuild/play1/play1.bin -lbuild/play1/play1.lst -sbuild/play1/play1.sym
test "$(stat -c %s build/play1/play1.bin)" -eq 4096
sha256sum experiments/play1_single_arena.asm build/play1/play1.bin
```

Genuin Stella-raster och råa bildbevis:
```sh
bash scripts/play1_stella_capture.sh
/usr/bin/python3 tests/play1_image_audit.py build/play1
bash scripts/play1_gameplay_capture.sh
/usr/bin/python3 tests/play1_gameplay_audit.py build/play1
```
De sju skärmscenarierna styrs av **Stellas verkliga `joy0Right #0`, `joy0Down #0`, `joy0Fire #0`** via autoexec.script, inte direkta spel-RAM-uppdateringar: baseline, level1 FIRE, joystickpickup level2, level2 FIRE, orb återaktivering level3, level3 FIRE+P1-måldöd och level3 rörelse medan halo är ON. Själva skärmbilderna fångas från en levande Stella 6.7.1 Debugger-skärm, inte från en mockup. För pixel-/registerbevis, kontrollera artifacts till GitHub Actions-workflows `PLAY1 real NTSC DASM build + authentic Stella screen` och `PLAY1 real joystick, orb, L3, FIRE gameplay regression` på denna branch.

## Testkoder och återhämtningsintervall
- 30 NTSC-rutor aktiv halo; cooldown enligt exakta kodtabellen L1=60, L2=36, L3=15 frames efter attack. Inre kodflödet dekrementerar även på sista attackrutan, vilket kan ge en ruta mindre i observerad cooldown; inga exakt observerade FIRE-retriggersekvenser påstås.
- Logisk diagonaltäckande 360° halo via `max(abs(dx),abs(dy))` med målradie L1=18, L2=28, L3=40 TIA-positionsenheter. Det är en fyrkantig Chebyshev-räckviddskandidat, inte en godkänd exakt cirkel.
- PF världsblå testvärde `#$86`, PF guld testvärde `#$2E`, riddare ljusblå testvärde `#$9E` – **inga slutliga palettbeslut**.
- En synlig BL, samma `COLUPF`-domän som PF; inga M0/M1-pilar/svärd och ingen oberoende fienderendering.
- Ny ROM-källkod: `experiments/play1_single_arena.asm` från exakt fryst COL1-commit `90f89441b41a2e82408581b81d3743b1423e5cdb`.

## Status
**PLAY1: DEVELOPER_OBSERVED_PARTIAL** tills en korrekt, fysiskt synlig halo följer P0 i alla riktningar; inte ett N8/N9/fullspels-PASS. Se teknisk handoff i `docs/play1/ROMDEV_PLAY1_MAIN_HANDOFF_2026-11-21.md`.
