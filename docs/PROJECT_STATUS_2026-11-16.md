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
| Grå Skraun med statisk haloring | 4K ROM och tre Stella-bilder godkända i begränsad egenkontroll, men **ingen rörlig halo** | https://github.com/Odourman/the-skraun/pull/5 |
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

## KORRIGERING AV SPRITEORIENTERING – 2026-11-16

Efter användarens observation verifierades att den tidigare kombinerade P02-grå-RING-ROM:en ritade trollet upp och ned. Rasterloopen läste bitmaptabeller via nedräknande index 191→0, men figurtabellerna lagrades i fel vertikal ordning. Samma metod förekommer i det tidiga B2-experimentet; dess gröna screenshot-test bevisar bara storlek/ring, inte rättvänd sprite.

**Fix:** [draft PR #6](https://github.com/Odourman/the-skraun/pull/6) i grenen `fix/p02-gray-halo-upright`, separat från `main`. Riktig Stella 6.7.1 bekräftar korrekt radorientering pixel för pixel på nivå 1–3, 4K NTSC ROM SHA-256 `7dda240f58656277e5508ad444368b2c33cad0ee9c9a5c259b27e0a7eda44bed`. Full audit i `docs/ATARI2600_SPRITE_ROW_ORDER_AUDIT_2026-11-16.md`, evidenspaket på Google Drive. P01/hela P02 är **inte oberoende verifierade**.

Roller: MAIN = den här huvudchatten; ROM DEVELOPMENT = separat implementation/självtest; VERIFICATION = separat oberoende granskning. Startprompter finns i `handoff/ROM_DEVELOPMENT_START.md` och `handoff/VERIFICATION_START.md`.

## MAIN uppdatering – A/B/C accepterade som egenkontroller, P02-B3b auktoriserad (2026-11-16)

Efter jämförelse med faktiska GitHub PR #8–#10, byggkörningar och samlad rapport har MAIN **accepterat A, B och C som klara avgränsade utvecklaregenkontroller**. Ingen gren har slagits ihop med `main` och inget oberoende VERIFICATION har genomförts.

- A: två riktiga gångposer, vänster/höger, tre storlekar och 8-riktningsrörelse i Stella. Den diagnostiska vänsterkantsmarginalen är inte en generell kernellösning eller färdig banagräns.
- B: `REFP0` hårdvaruspegling genomförd och utvecklartestad. Fyra bitmaptabeller reduceras till två och **24 ROM-byte** sparas; integrerad timing ej slutligt mätt.
- C: P02-B3a visar asymmetrisk ring i tre fasta X-centra 56/80/104 och grå P0. Debugger visar 262 scanlines vid provat läge. Beräknat högst **64 av 76 CPU-cykler/scanline** för synlig rutin (statisk kalkyl, **inte** full värstafallsmätning). Ingen fri joystickföljning, hinder eller fiender.
- Jämförbar originalrapport: https://github.com/Odourman/the-skraun/blob/experiment/romdev-c-b3a/docs/ROMDEV_ABC_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md . Samlat evidens: https://drive.google.com/drive/folders/1MyI-ZuVqSj_MwQRebn7C0emfxlU5jdeX .
- **Nytt uttryckligt MAIN-uppdrag:** https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_B3B_AUTHORIZED_SCOPE_2026-11-16.md – B3b, faktisk horisontell joystickföljning i 4-TIA-klocksteg och begränsat PF-hindrars/processorbudget-test. Ingen B3c, fiendekod eller produktionsintegration nu.
- **VERIFICATION vilande**, eftersom oberoende kontroll ska samlas för senare större leveranspaket. Öppna historiska verifieringsärenden stängs inte av detta beslut.

Tidigare statusuppgifter längre upp på sidan visar dåtidens läge; **denna sektion är senare och ersätter formuleringen att B3a inte var byggd**.

## Senaste MAIN-beslut: B3b accepterad som egenkontroll; P02-R1 auktoriserad (16 november 2026)

Detta är senaste lägesuppdateringen och ersätter äldre framtidsformuleringar ovan som beskrev B3b som ännu inte genomförd.

- ROM DEVELOPMENTs B3b utvecklartest [PR #11](https://github.com/Odourman/the-skraun/pull/11) visar 13 joystickstyrda 4-TIA-klockslägen och synkroniserad asymmetrisk PF-ring/P0. Realtidsbilder i [grön Stella-körning](https://github.com/Odourman/the-skraun/actions/runs/43901341243) och fyra verkliga joysticklägen med 262 scanlines i [Stella Debugger](https://github.com/Odourman/the-skraun/actions/runs/43900278446). Detta är **egenkontroller**, inte oberoende verifiering.
- Två 4K-ROM-varianter: dynamisk SHA-256 `7d96bcb71532643307922f62814900b09a1525ede06795c17417607634efd060`; prekomponerade syntetiska hinder SHA-256 `31b859d711bb08228b03015f9039b1df97c77628ab3637f754ad3df77b599bbe`.
- **Allvarliga begränsningar:** Endast 1 horisontellt steg per 16 NTSC-bildrutor (~267 ms), enbart 13 testpositioner, 63/76 cykler värstafall **statiskt beräknat** (13 cyklers marginal). Generell runtime-hinderkomposition i oförändrad kernel behöver minst ~79/76 cykler och saknar visuell separation mellan ring och hinder. Två riddare + bågskytt + pil + orb + HUD har inte testats i gemensam kernel.
- Full leveransrapport: https://github.com/Odourman/the-skraun/blob/experiment/romdev-b3b-horizontal-follow/docs/ROMDEV_B3B_CONSOLIDATED_MAIN_HANDOFF_2026-11-16.md . Evidensmapp: https://drive.google.com/drive/folders/1fn4RTvPreT6dsVQD5HUaLYIRPfLffz8h .
- **MAIN:s enda nya implementationsauktorisation:** [P02-R1 renderer architecture feasibility](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R1_RENDERER_FEASIBILITY_AUTHORIZED_2026-11-16.md) – diagnostiskt förbättrad respons, jämförelse av PF/hybrid/hinderrendering, konservativ budget för framtida fiender och HUD. Ingen B3c, ingen färdig stridsmotor, ingen produktionsmerge.
- **VERIFICATION fortfarande vilande** fram till en senare större sammanhängande milstolpe. Ingen oberoende PASS har utfärdats.
