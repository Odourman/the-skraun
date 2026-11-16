# THE SKRAUN – Grå Skraun + statisk playfield-ring, kombinerad ROM

Datum: 2026-11-16
**Status:** Godkänt avgränsat utvecklartest i Stella; inte färdig spelmotor eller oberoende verifiering.
Egen experimentgren: `experiment/p02-gray-halo-static`.
Källkod: `experiments/p02_gray_static_halo.asm`. Huvudgrenens P01-ROM är orörd.

## Syfte

Förenar den grå ovanifrån-tolkningen av användarens trollskiss med P02-B2:s gula playfield-ring utan att förbruka TIA:s andra spelarsprite (P1). Grå P0-silhuett, gul PF2-ring i tre nivåer. Denna kombinations-ROM är **statisk**; det finns ingen rörelse, ingen FIRE-knapp eller fiender i experimentet.

## Byggresultat

- DASM 6502: `dasm experiments/p02_gray_static_halo.asm -f3 -obuild/gray-static-halo.bin -lbuild/gray-static-halo.lst -sbuild/gray-static-halo.sym`
- ROM: 4 096 byte, NTSC/4K.
- SHA-256: `932d868d47ab99993c31126749e493cac9ca0837fbe0e1b3d2792aa66c0c6719`.
- GitHub Actions: https://github.com/Odourman/the-skraun/actions/runs/43883757257
- Automatisk pixeltest: `tests/check_gray_static_halo.py` – pass.
- Full evidence, ROM och PNG: https://drive.google.com/drive/folders/1TGzGo8KMUgUdqoKHUAdaCo3vNTZkPhSW

## Direkt uppmätt ur riktiga Stella-bilder

| Nivå | Grå Skraun | Gyllene PF-ring | Resultat |
|---|---|---|---|
| Level 1 | 16×12 bildpixlar | 48×42 bildpixlar | Ringen omsluter figuren |
| Level 2 | 32×24 | 80×62 | Ringen omsluter figuren |
| Level 3 | 64×36 | 96×84 | Ringen omsluter figuren |

Horisontellt använder Stellas skärmbild dubblerade bildpixlar relativt TIA:s färgklockor. Både mått och position uppmättes från emulatorns verkliga PNG-bilder.

## Vad är fortfarande öppet?

- **Rörlig haloring:** ej implementerad. P02-B3a måste visa ospeglad playfieldgrafik i tre X-lägen, därefter joystickföljning och cykelbudget.
- **Gånganimation i kombinations-ROM:** ej implementerad. De två A/B-gångposerna är i separat `experiment/gray-topdown-skraun` och behöver senare kombineras först efter kontroll av tid och flimmer.
- **Fiender, hinder, skog/berg/dröm/natt, riktig poängräkning och kollisioner:** saknas.
- **Läsbarhet och utseende:** grå figuren har inte fått oberoende grafiskt godkännande; skissen är visuellt rättesnöre, men 8-bitars TIA-gränsen ger en mycket förenklad form.
- **Stella Debugger-kontroll:** full 262-scanline- och värstafallscykelbudget för denna ROM är inte dokumenterad.
- **Oberoende VERIFICATION:** fortfarande öppen (P01 issue #1).

Detta test får därför **inte** beskrivas som att den rörliga ringen är löst eller att den grå spritefiguren är slutgodkänd. Inga av MAIN:s 60 spelbeslut ändras.
