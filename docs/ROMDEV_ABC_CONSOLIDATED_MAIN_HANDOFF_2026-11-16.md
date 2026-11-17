# THE SKRAUN – ROM DEVELOPMENT A/B/C, samlad överlämning till MAIN
Datum: 2026-11-16
Status: Genomfört avgränsat **utvecklaregenkontroll**-uppdrag A→B→C. **Ingen oberoende VERIFICATION**, ingen ändring på `main`, ingen B3b eller senare implementation.

## Auktorisation och källor
- MAIN-scope: [MAIN_TO_ROM_DEV_AUTHORIZED_SCOPE_2026-11-16.md](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_AUTHORIZED_SCOPE_2026-11-16.md).
- Gällande design: `docs/DESIGN_DECISIONS_01-60_2026-11-16.md`; grå, rakt-ovanifrån Skraun: `docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md`.
- Originalhandritning på Google Drive används endast som visuell referens; estetisk slutacceptans för pixelversionen har inte utfärdats.
- Alla ändringar ligger i **separata experimentgrenar**; tidigare P01-issue #1 för oberoende verifiering lämnas öppen.

## Sammanfattning
| Del | Resultat | Verkliga tester | Ej visat |
|---|---|---|---|
| A – grå sprite, radorientering, animation | **PASS (utvecklaregenkontroll)** | Stella 6.7.1, två A/B-poser i båda horisontella riktningarna, tre nivåer, åtta rörelseriktningar, 262-line frame via Debugger | Slutgiltig level-1 estetik, verklig konsol, hela framtida spelmotorn |
| B – REFP0 hårdvaruspegling | **PASS (utvecklaregenkontroll)** | Riktiga Stella-pixlar matchar A/B × höger/vänster; 262-line frame i Debugger; identiska rörelser | Full CPU- och pixeltimingaudit för framtida stridsmotor |
| C – P02-B3a tre fasta PF-ringlägen | **PASS (endast avgränsad B3a)** | Verklig Stella: x=56/80/104; identiska ringar, rätt centrering, ingen klippning; 262-line frame i Debugger | B3b fri joystickföljning, FIRE, kollision, hinder, flersprite-konkurrens, oberoende verifiering |

## Källkod, gren, byggkommandon och faktisk ROM
| Del | Experimentgren / källfil | Byggkommando | ROM SHA-256 |
|---|---|---|---|
| A | [experiment/romdev-a-gray-stella](https://github.com/Odourman/the-skraun/tree/experiment/romdev-a-gray-stella), `experiments/p01_skraun_gray_topdown.asm` | `dasm experiments/p01_skraun_gray_topdown.asm -f3 -obuild/romdev-a.bin -lbuild/romdev-a.lst -sbuild/romdev-a.sym` | `d1ef550504a97ebdadcd5c695752859400e103eb0812eb1bbacf46f4b1b61700` |
| B | [experiment/romdev-b-refp0](https://github.com/Odourman/the-skraun/tree/experiment/romdev-b-refp0), `experiments/romdev_b_refp0.asm` | `dasm experiments/romdev_b_refp0.asm -f3 -obuild/romdev-b.bin -lbuild/romdev-b.lst -sbuild/romdev-b.sym` | `2af7b2092c6bebf06bbe6211bbb0602988c19551b4d63a04eab1a6d303334b2b` |
| C | [experiment/romdev-c-b3a](https://github.com/Odourman/the-skraun/tree/experiment/romdev-c-b3a), `experiments/romdev_c_b3a.asm` | `dasm experiments/romdev_c_b3a.asm -f3 -obuild/romdev-c-b3a.bin -lbuild/romdev-c-b3a.lst -sbuild/romdev-c-b3a.sym` | `31dfcb8034ed7c37d89918df8c0600bfa1159d94830189122240d225cb817479` |

Var och en är **4 096 byte**, NTSC, 4K utan bankswitching. Samlad GitHub Actions-ombyggnad av *alla tre* källorna reproducerar exakt dessa SHA-256-värden: [ROMDEV ABC reproducible source and ROM handoff](https://github.com/Odourman/the-skraun/actions/runs/43892290269). Där ingår källkod, ROM, DASM-listningar, symbolfiler och testkod. Source commits vid den körningen:
- A `c5928c348f4892d34102657b4dfa8683c70ab896`
- B `c0af705d3947b3da8f4527bfc4e8c23501a66b5c`
- C `fa502523b4f85d5fdaa06f0d1edd60b0c416506a` (före denna rapportfil)

## A – resultat och defekter
- Riktig Stella, [visuell/movement PASS](https://github.com/Odourman/the-skraun/actions/runs/43890394322). `tests/romdev_a_stella_check.py` kontrollerar faktiskt renderade 8×12 bitmaprader (inte bara assembler-data), A och B i höger/vänster, NUSIZ-bredder och alla åtta joystickriktningar.
- Bildmått: level 1 **16×12** bildpixlar, level 2 **32×24**, level 3 **64×36** (dubbel horisontell skärmbildsskala relativt TIA).
- Direkta [Stella Debugger-bilden](https://github.com/Odourman/the-skraun/actions/runs/43891429587) visar **262 scanlines** på den slutliga A-kandidatens ROM; full värstafallscykelprofil är **NOT TESTED**.
- I den ursprungliga P01-liknande grafikkerneln kunde några vänsterrader klippas eftersom `GRP0` skrivs efter att strålen passerat sprites läge. A-experimentets minsta `PlayerX` höjdes från 12 till 30 som en **diagnostisk begränsning**. Detta är INTE en beslutade slutlig spelplansgräns eller reparerad generell kernel.
- Figursilhuetten har ett synligt huvud/öron, ögon och ben, men **8×12 är för litet för säker estetisk igenkänning på all framtida scenbakgrund**. Användarens slutgodkännande av faktiskt spelsprite saknas.

## B – REFP0-jämförelse
- `REFP0` TIA write-register `$0B`, bit 3 `#$08` gör horisontell P0-reflektion. Endast `GfxRightA` och `GfxRightB` lagras i ROM; vänster bild produceras i hårdvaran. Vertikal tabellordning är **oförändrat korrekt** och hör inte ihop med REFP0.
- [Stella-realtids-PNG- och åttariktningstest PASS](https://github.com/Odourman/the-skraun/actions/runs/43890695350); [B:s direktuppmätta 262 scanlines](https://github.com/Odourman/the-skraun/actions/runs/43892252607) från debuggerbild, inte CPU-modelldata.
- Fyra källbitmaptabeller A/B höger/vänster → två. Sparar **24 ROM-byte** i aktuell källkod, bekräftat av DASM-symbolernas MapLarge-placering `$F22C` vs `$F214`; fysisk cartridge-fil fortsatt 4096 byte.
- Både A och B använder nollsidans `$80..$8E`: **15 RAM-byte**. Synlig display-loop är i huvudsak samma; extra REFP0-skrivning sker under VBLANK. Exakt värstafallscykelavvikelse är **NOT TESTED** i debuggerprofil; befintliga frame-observationer visar ingen ökad bildrutelängd.
- Fyrtabellsversionen behålls som fallback om en senare kernel behöver andra kompromisser.

## C – B3a: endast tre förberäknade X-lägen
- Riktig Stella 6.7.1: [slutlig pixel-/konturkontroll PASS](https://github.com/Odourman/the-skraun/actions/runs/43891515354) och [sista ombyggnad med konservativ cykelberäkning PASS](https://github.com/Odourman/the-skraun/actions/runs/43891960779).
- `CTRLPF=0` (asymmetrisk). En P0-grå platsmarkör och olika playfield-byte för vänster/höger per synlig scanline; P1 reserverad.
- Ringens faktiska Stella-mått: **80×63 bildpixlar** i alla tre lägena, 1120 guldfärgade bildpunkter per ring. Bounding boxes x=[72,152), [120,200), [168,248), alla y=[80,143). P0 x=[96,128), [144,176), [192,224), y=[99,123). Bildförskjutningen är exakt 48 bildpixlar när centrum flyttas 24 TIA color-clocks; hela masken översätts pixelidentiskt.
- En äldre C-kandidat hade felcentrerad P0 och sedan **263 scanlines**; båda defekterna rättades. Den korrigerade [Stella Debugger-bilden](https://github.com/Odourman/the-skraun/actions/runs/43891882783) visar `_scanEnd = 262` vid frame 80. En tidigare automatiserad debuggerkörning gav en helt svart bild trots grön Actions-status; efter fail-closed-kontroll och omkörning har en läsbar, autentisk debuggerbild granskats.
- **128-byte RAM:** 12 byte används i denna isolerade C-testmotor (`$80..$8B`), 116 lediga inom endast detta experiment; framtida AI/HUD/bakgrunder ingår inte.
- **ROM:** sju 192-byte icke-noll PF-tabeller + en 192-byte nolltabell + en 192-byte trolltabell = **1728 byte data**. 4096 byte total ROM, ingen framebuffer och ingen bankswitching.
- **TIA:** sex PF-registerskrivningar (PF0/PF1/PF2 per vänster och höger halva), ett `GRP0` och `WSYNC` per synlig scanline. En konservativ statisk 6502-instruktionsräkning med sidkorsningar ger högst **64 av 76 cykler** för den löpande synliga rastervägen inklusive WSYNC, marginal **12 cykler**. **Värstafallscykler per scanline är inte direkt uppmätta i debugger**, och 262-line observerad frame i tre valda lägen ersätter inte en fullskalig dynamisk kernelprofil.
- Ringens bild och position ändras **bara vid SELECT** mellan tre förberäknade ROM-datamasker; det finns ingen frirörlig halo. FIRE/cooldown, kollision genom hinder, riddare, bågskytt och scenbakgrunder är medvetet **inte implementerade**.

## Teknikjämförelse: tidigare lösningar
| Teknik | Avgränsat belagt | Allvarlig begränsning |
|---|---|---|
| P02-A, P1-halo | P1 halo synlig i Stella | Max 32 TIA-color-clocks bredd på nivå 3 och upptar P1 som behövs för fiender |
| P02-B1/B2 speglad PF-halo | Statisk ring kring skärmmitt och troll på tre storlekar | Reflekterad PF låst vid x=80; ingen fritt flyttbar ring; omöjligt att avläsa kapacitet för miljöhinder från det statiska testet |
| P02-B3a, detta uppdrag | Samma asymmetriska ring vid x=56/80/104 och 262-line frame, P1 fri | Fler PF-skrivningar och mer maskdata, ingen frirörlig halo eller testad miljökonkurrens |

## Vad MAIN inte bör tolka som färdigspelat
- A/B/C är **utvecklaregenkontroller**, aldrig extern oberoende VERIFICATION.
- Ingen av delarna är produktionsklar, ingen är implementerad på `main`.
- Inte testat: PAL, originalhårdvara, verklig stridsscen, hinder och playfield-konkurrens, projektildetektion, nivåloop, ljud, full worst-case CPU-profiler eller slutlig estetisk acceptans.
- **B3b och senare är inte påbörjade.** Detta uppdrag ger en teknisk genomförbarhetsindikation, inte något MAIN-beslut om slutlig renderermetod.

## Levererat evidensmaterial och nästa rekommendation
- Samlad [Drive-evidensmapp](https://drive.google.com/drive/folders/1MyI-ZuVqSj_MwQRebn7C0emfxlU5jdeX) med A/B/C-ROM/PNG/loggar/debuggerbilder, källkod + ombyggnadsartefakt och bildmontage. Individuella GitHub Actions-länkar ovan identifierar alla testkörningar.
- Källkod, testkod, ROM, DASM-listor och SHA-filer i [exakt reproducerat käll-/ROM-paket](https://drive.google.com/file/d/1Bb3kKPHXC6gu8HvySSyOFrZNNHRlw5G2/view?usp=drivesdk).
- Original 8×12 sprite behöver fortsatt visuell granskning vid realistiska bakgrundskontraster; P0 vänsterkantsmarginal och full display-kernel resursbudget måste lösas före produktionsintegration.
- **Rekommendation till MAIN:** bevara A/B som dokumenterade grafikreferenser; prioritera en uttryckligt separat auktoriserad nästa feasibility-scope som kan testa verklig förflyttning och samtidig PF-scenkonkurrens innan slutligt renderingsval. Håll P1 ledig där möjligt. Under detta uppdrag lämnas B3b och alla senare steg orörda.
