# THE SKRAUN – Aktuellt projektläge, 16 november 2026

**MAIN sammanfattning efter kontroll av GitHub och Google Drive.**

## Käll- och implementationsgräns

1. Beslut 01–60 på `main` definierar spelets regler. Användarens nya handritade referens och uttryckliga bekräftelse av ljusgrått, ovanifrånperspektiv, två poser och enbart horisontell spegling är aktuell visuell riktning.
2. Experimenten `experiment/p02-halo-p1`, `experiment/p02-playfield-b2` och `experiment/gray-topdown-skraun` är **separata grenar**. Ingen har slagits ihop med den stabila källkoden.
3. Tester som byggningen, automatisk PNG-analys och ett isolerat Stella-prov är **egenkontroller**, inte oberoende VERIFICATION.

## Kontrollerad kod- och teststatus

| Del | Status | Evidens |
|---|---|---|
| Speldesign 01–60 | Dokumenterad | `docs/DESIGN_DECISIONS_01-60_2026-11-16.md` |
| P01 grundprototyp | Körbar 4K NTSC; tre storlekar, grundrörelse | `src/main.asm`; ordinarie CI godkänd |
| P01 oberoende verifiering | **Öppen, ej godkänd** | https://github.com/Odourman/the-skraun/issues/1 |
| P02-A P1-haloring | ROM och Stella-bilder; otillräcklig level-3-bredd och blockerar P1 | https://github.com/Odourman/the-skraun/pull/2 |
| P02-B1 statisk playfield-ring | Bounded Stella test PASS, ring 96×84 bildpixlar | `docs/P02_B1_PLAYFIELD_RESULT_2026-11-16.md` |
| P02-B2 statisk halo med P0-troll | Bounded Stella test PASS, tre storlekar | https://github.com/Odourman/the-skraun/pull/3 |
| P02-B3 dynamisk ring | Plan och testgrind dokumenterade, **ingen ROM ännu** | `docs/P02_B3_DYNAMIC_RING_GATE.md` i B2-grenen |
| Ny grå overhead-Skraun | ROM byggd, 3 storlekar och grundrörelse i Stella; grafiken är fortfarande preliminär | https://github.com/Odourman/the-skraun/pull/4 |
| Skog/berg/dröm/natt, riddare, grön bågskytt, kollisioner, poäng och ljud | **Inte implementerade** i de testade prototyperna | Återstår |

## Nytt visuell implementationstest

- Användarens handritade ursprungsform, privata foto i projektets Drive: https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view
- Godkänd visuell riktning: ljusgrått, ovanifrån, 2 korta gångposer med arm- och benrörelser, vänster = exakt bitvis spegling av höger. Ingen ny vy uppåt/nedåt.
- Grå experimentkällkod: `experiments/p01_skraun_gray_topdown.asm` i PR #4.
- Godkänd DASM- och Stella-egenkontroll: https://github.com/Odourman/the-skraun/actions/runs/43882932038
- ROM SHA-256: `387ad9dd3fc3cbceeaca61122963de5b79ecc482dc0e17d22a4c6827b756fd99`, storlek 4 096 byte.
- Skärmbilder: 16×12, 32×24, 64×36 pixlar i Stella-bilder; motsvarar horisontellt 8/16/32 TIA-color-clocks. Den grå figuren behöver estetisk overhead-kontroll, timing och oberoende test.
- Google Drive-evidens: https://drive.google.com/drive/folders/1udBPud9jpVzvMevcgKL8duib94GyV_yJ

## Prioriterad fortsättning

1. Kontrollera att A/B-animationerna faktiskt syns i Stella och testa grå P01:s scanline-/cykelbudget, inte bara spelarspritens bildmått.
2. Gör den minsta grå figuren visuellt igenkännlig ovanifrån, baserat på originalteckningen. Beakta kontrast mot framtida skog/berg/dröm/natt, särskilt grå sten.
3. Utred P02-B3a (flyttbar ospeglad playfield-ring i tre X-lägen) i **ny separat experimentgren** med bildtest, timing och tydlig riskredovisning. P02-B2 är fortfarande statisk.
4. Integrera inte grå figur eller ny ring på `main` förrän aktuella scope och mätningar håller. P01-oberoende verifiering ska inte antas passerad.

**Övergripande slutsats:** Speldesignen är långt gången, men spelet är fortfarande i hårdvaru- och kärngrafikprototypstadiet. Det finns ingen färdig spelbar kampbana och inga riktiga bakgrundsvärldar i ROM ännu.
