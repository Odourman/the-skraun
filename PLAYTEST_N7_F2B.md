# THE SKRAUN – N7/F2b PLAYTEST
**2026-11-21 | ROM DEVELOPMENT II egenkontroll | faktisk 6507/DASM/Stella 6.7.1**

## Auktoritet och STOP
Enbart [MAIN III N7/F2b-arbetsordern](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_III_TO_ROM_DEVELOPMENT_II_N7_F2B_MINIMAL_NTSC_DIAGNOSTIC_AUTHORIZED_2026-11-21.md), [issue #31](https://github.com/Odourman/the-skraun/issues/31). **F2b_FAIL_FOR_TESTED_SCENE.** Efter en (1) avgränsad justering stoppade utvecklingen. Inga N8- eller gameplaytillägg.

## Reproducerbart bygge
Kör från repo-rot i Linux med DASM 2.20.14.1:

```sh
dasm experiments/n7_f2b_minimal_ntsc.asm -f3 -oexperiments/n7_f2b_minimal_ntsc.bin -lexperiments/n7_f2b_minimal_ntsc.lst -sexperiments/n7_f2b_minimal_ntsc.sym
test "$(stat -c %s experiments/n7_f2b_minimal_ntsc.bin)" -eq 4096
sha256sum -c experiments/n7_f2b_SHA256SUMS.txt
```

Fryst slut-ROM SHA256: `d15c4805b06c562cb76369dfe3efff3a8c9537f28de4945196d198957fc5368f`.
Fryst ASM SHA256: `a4d95c17ecad953605c7be8a9e0792c6779bf6af8990f420ff8a517233e25a22`.
Den första, opatchade ROM-versionen (föräldra-commit, inte slut-ROM) hade SHA256 `45b8fa0045383438f5b3bcc9d09b2cfac3f91a9b9822d0d5a7124e71c44ad361`.

## Återskapa autentiska skärmbilder
Förutsätter installerade `stella`, `xvfb-run`, `xdotool`, `scrot` och `python3-pil`. GitHub Actions [körning #44911307187](https://github.com/Odourman/the-skraun/actions/runs/44911307187) utförde just detta och sparade originaldata.

```sh
mkdir -p build/n7
dasm experiments/n7_f2b_minimal_ntsc.asm -f3 -obuild/n7/n7-f2b-ntsc.bin -lbuild/n7/n7-f2b-ntsc.lst -sbuild/n7/n7-f2b-ntsc.sym
bash scripts/n7_f2b_stella_capture.sh
/usr/bin/python3 tests/n7_f2b_analyse.py build/n7
/usr/bin/python3 tests/n7_f2b_source_pixel_oracle.py build/n7/stella-s2-12
```

Stella Debugger kör `frame #10` och därefter tolv på varandra följande `frame #1`. **FRAME_001..FRAME_012** är faktiskt tagna Stella-fönsterbilder; **TIA_001..012** är pixel-exakta utsnitt från samma skärmdumpar, inga renderade förhandsbilder. Råa filer, emulator-logg och skärmbilder finns i [Drive-arkivet](https://drive.google.com/file/d/1k_G4Fff_2ed3d_HiBX7ZzB9LdGQ7O7Mq/view).

## Kontrollera registertider i Stella
```sh
bash scripts/n7_f2b_debugger_trace.sh
```

Fryst korrigerad PC-spårning: [körning #44911486185](https://github.com/Odourman/the-skraun/actions/runs/44911486185), [Drive-bevis](https://drive.google.com/file/d/19ojDhXYTOqKQUnMVeajwHZLgTKgOw4ld/view). Efter en enda NOP reducerades `STA RESP1` på fysisk scanline 131 från CPU-cykel 50–53 till **48–51**. Den efterföljande P1Band-iterationens motsvarande PC kommer ändå först på fysisk scanline 133, inte 132. Se `TRACE_03.png`, `TRACE_04.png`, `TRACE_10.png`.

## Regler för tolkning
- **DASM SUCCESS**: korrekt maskinbyggd fil, inte F2b-renderingsgodkännande.
- **Stella SUCCESS**: verklig emulator startade och 12 konsekutiva, färgade ramar sparades; *alla tre individuella R3-maskar på de begärda X-positionerna* är ändå **FAIL**.
- Scene-variabeln i RIOT `$80`: 0 = S2-close (den faktiskt provade), 1 = omvänd ordning och 2 = S3 med P0 L3 (finns som källalternativ, men **ingen dokumenterad faktisk Stella-PASS/FAIL för dem**).
- PF B/ON-maskar X80/X84 finns som data i ROM men ritas **inte** fysiskt. M0/BL/HUD/svärd/AI är inte byggda.
- Justeringstak uppnått: endast en NOP togs bort, ingen mer ny arkitekturforskning eller gameplaykompromiss.
- För själva resultatets begränsningar, läs `docs/n7_f2b/ROMDEV_N7_F2B_HANDOFF.md`.

## Manuellt playtest
Öppna `experiments/n7_f2b_minimal_ntsc.bin` i Stella 6.7.1, NTSC. Inspektera S2:s 16 fienderader kring arena Y78. Två riddare är avsedda att ha samma ljusblå test-TIA-byte och ranger en separat grön test-TIA-byte; originalbitmapparna finns i koden. Visuell existens av blå/gröna pixlar är **inte** liktydigt med att tre fria X och fulla originalmasker fungerar.
