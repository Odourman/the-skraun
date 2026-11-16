# THE SKRAUN — Grå Skraun sedd uppifrån: första ROM-testet

Datum: 2026-11-16
**Status: lyckad byggning och begränsat Stella-egenprov; fortfarande experimentell grafik.**
Spelreglerna 01–60 ändras inte. P01:s äldre gröna test-ROM och `src/main.asm` lämnas orörda.
GitHub-gren: `experiment/gray-topdown-skraun`.
Källkod: `experiments/p01_skraun_gray_topdown.asm`.

## Designreferens

Användarens egen teckning från 2026-11-16 är primär referens för trollformen, men spelets kamera är **rakt uppifrån**. De två upplyfta armarna i skissen tolkas som framben/främre lemmar som viftar medan bakbenen går. Spegelvänd höger/vänster; ingen separat upp- eller nedvändning. Två korta gångposer A/B. Ljusgrå kropp, mörka hål för ögon/ansiktsmarkeringar. Första ROM-bitmappen är en tolkning, inte en slutgodkänd form.

Originalfoto (endast i Drive): https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view
Visuell riktning på GitHub: https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md

## Reproducerbar ROM

- Byggkommando: `dasm experiments/p01_skraun_gray_topdown.asm -f3 -obuild/skraun-gray-overhead.bin -lbuild/skraun-gray-overhead.lst -sbuild/skraun-gray-overhead.sym`
- Kompilerad ROM: 4 096 byte, 4K NTSC.
- SHA-256: `387ad9dd3fc3cbceeaca61122963de5b79ecc482dc0e17d22a4c6827b756fd99`.
- Källversion för testet: `55d30421bb1843f2d158598b27aae176e9e5973a` (innehåller den senaste grå figuren, testskript och workflow).
- GitHub Actions-run: https://github.com/Odourman/the-skraun/actions/runs/43882932038
- Testet byggde 4K ROM, körde Stella 6.7.1 och sparade verkliga PNG-skärmbilder.
- Testmodul: `tests/check_gray_skraun.py`.

## Observerat i Stella

| Fall | Pixelmått i Stella-bild, horisontellt dubblerat | Resultat |
|---|---|---|
| Level 1 | 16 × 12 | Pass |
| Level 2 | 32 × 24 | Pass |
| Level 3 | 64 × 36 | Pass |
| Riktning åt höger | b-box x174–237, y92–127 | Synlig rörelse |
| Riktning åt vänster | b-box x164–227, y92–127 | Synlig rörelse |

`tests/check_gray_skraun.py` läste dessutom källkoden och bekräftade fyra bitmaptabeller, 12 rader vardera, två olika gångposer och **exakt bitvis spegling** av både A och B. `COLUP0=$0C` gav synlig neutralgrå silhuett på svart bakgrund. Det här är en utvecklaregenkontroll, inte oberoende verifiering.

Skärmbilder, ROM, assemblerlistning, symboler, bygglogg och kontrollsumma finns i Drive:
https://drive.google.com/drive/folders/1udBPud9jpVzvMevcgKL8duib94GyV_yJ

## Kvarstående risker och avgränsningar

- 8×12-pixelmotivet är kraftigt förenklat. Om huvud, horn, armar och fyra lemmar uppfattas rätt i **ovanifrånperspektiv** måste bedömas visuellt; denna CI kan inte avgöra bildspråket.
- Att båda poses finns och speglas i ROM-källan bevisar inte i sig att varje pose syns korrekt i Stella vid rätt tidpunkt. Separata frame-stepped animationstester behövs.
- Utan horisontellt joystickutslag bevarar ROM-koden senaste vänster/högerorientering vid rörelse uppåt/nedåt; den regeln är en teknisk implementeringsdetalj som kan justeras utan nytt spelmekanikbeslut.
- En frame från själva Stella Debugger med 262 scanlines för just denna ROM har **inte** bifogats. P01:s tidigare NTSC-mätning kan inte automatiskt överföras till ny kod.
- Kontrast i skog/berg/dröm/natt är ännu oprövad eftersom den här ROM:en har svart testbakgrund.
- Koden är inte integrerad i P02-B2:s playfield-ring; P02-B3 rörlig ring är ännu ej programmerad.
- Ingen oberoende verifiering har godkänt grafiken. P01-gate: https://github.com/Odourman/the-skraun/issues/1

## Rekommenderad fortsättning

1. Gör animations-/riktningsverifiering med Stella skärmdumpar och 262-line-mätningar för den nya grå ROM:en.
2. Låt användaren granska den **verkliga** ROM-grafiken, särskilt overhead-känslan, innan vi ersätter P01 på huvudgrenen.
3. Fortsätt separat P02-B3a-förstudie med asymmetrisk playfield, utan att blanda ihop sprite-design och rörlig haloteknik.
4. Efter separat verifiering kan sprite ersättas i spelprototypen och kontrasttestas på riktiga nivåbakgrunder.

**Slutsats:** Grå Skraun är nu en verklig spelbar Atari 2600-test-ROM, med tydligt avgränsad status. Slutgrafiken är inte godkänd.
