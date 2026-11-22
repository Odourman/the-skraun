# THE SKRAUN — GAMEPLAY-5 PLAYTEST
**ROM DEVELOPMENT III · 2026-11-22 · MAIN IV Issue #48 · DEVELOPER_OBSERVED**

## Körbar checkpoint
**Föredragen ROM: `experiments/gameplay5_f8_ntsc.bin`**. Verkligt DASM-byggd original-Atari 2600 NTSC F8-ROM på exakt 8192 byte. SHA-256:
`b31e508e8947052b88fa50fb173106dcbe8e7d5f416eb3740e5f29088526bdca`.

För att kontrollera: `sha256sum -c experiments/gameplay5_SHA256SUMS.txt`. Bygg även själv:
```bash
dasm experiments/gameplay5_bank0.asm -f3 -ob0.bin -lb0.lst -sb0.sym
dasm experiments/gameplay5_bank1.asm -f3 -ob1.bin -lb1.lst -sb1.sym
cat b0.bin b1.bin > the_skraun_gameplay5.bin
sha256sum the_skraun_gameplay5.bin
```
Föredragen källa och exakt enbank-/tvåbankproveniens ingår i det frysta commit:et. GAMEPLAY-4A-originalet förblir byte-identiskt som separat checkpoint.

## Så spelar du
Öppna `experiments/gameplay5_f8_ntsc.bin` i Stella, vanliga joystick 0. Alla åtta rörelseriktningar, väggglidning enligt befintlig K0-logik, FIRE för den ursprungliga återkommande halon, SELECT-debugcheat ingår fortfarande inte i normalt progressionflöde och GAME OVER: FIRE eller konsolens RESET för ny omgång.

Start: bana 1, Level 1, tre liv och noll poäng. Från start **HÖGER ~16 bildrutor, NER ~24** för att plocka banans TIA BL-orb och växa till Level 2. När en riddare är nära får han 24 bildrutors tydlig svärdsvarning, därefter ett 7-bildrutors aktivt svärdshugg och ~60 bildrutors återhämtning. Den nya skadekontrollen försöker stoppa svärd genom riktiga hinder. Låt inte riddaren träffa dig under hans aktiva hugg; fysisk fullständig hinder-/riktningstest saknas fortfarande.

För strid och banbyte: håll FIRE, gå **UPP ~40 bildrutor, HÖGER ~14**, och fortsätt FIRE/överlevnad. Nuvarande temporära synliga P1-fiender är fortfarande två riddarpoängplatser om 100 p + Ranger om 250 p **i följd**, inte tre samtidiga fiender; slutpoängen på bana 1 bör bli 450 p under lyckat test. Efter ~120 bildrutors övergång ger bana 2 en ny orb, **HÖGER ~8, NER ~24** från återspawnpunkten för Level 3; högsta nivån bevarar samma källbitmap och på skärmen en 64×36 TIA-bildyta i den provade PAL-nej NTSC-uppskalningen.

**Ingen Ranger-pil finns i denna säkra ROM.** R1 visar riktig neutral, dra, släpp med world-green källmask, men de avvisade fysiska M0- och tidigare M1-försöken får inte levereras som om de vore flygande pilar. Den visuella haloformen följer Y men inte X och är fortfarande PARTIAL.

## Äkta mätningar och reproduktion
[GAMEPLAY-5 faktisk 13-scen DASM/Stella-regression](https://github.com/Odourman/the-skraun/actions/runs/45046813014) kör `scripts/gameplay5_stella_regression.sh` utan debugger-RAM/PC-modifiering. Alla **13/13 _scanEnd = 262**, bland annat neutral 116, svärdsvarning 134, hugg 130 K1-T-blå bildpixlar; Skraun L1 98 grå, L2 392 och L3 1200; Ranger green-source draw/release samt omstart. Exakta autentiska skrivbordsskärmbilder, 320×228 TIA-crops och kommandologgar finns i workflow-artefakten. Detta är **DEVELOPER_OBSERVED BOUNDED**, inte full 76-cykel-/beamdeadline-verifiering.

[GAMEPLAY-5 33+2 overscan-timerexperiment](https://github.com/Odourman/the-skraun/actions/runs/45046548302): 262 för var och en av R1-faserna 18/21/24/27/30. Förändrat bank1 överscan 34→33, slutliga två WSYNC oförändrade. Frysta 4A hade 263 vid phase27. Att detta orsakssamband gäller alla frame- och motorvägar är INTE bevisat; första avvikande PC/instruktion har inte isolerats.

[GAMEPLAY-5 M0 tvåkantspil — fysisk FAIL](https://github.com/Odourman/the-skraun/actions/runs/45046341969): genuin DASM F8 och Stella, **286/286/287/287/286/286/286 rader** i 7 Ranger-faser, inte en 262-kompatibel körbar pil. Källor `experiments/gameplay5m0_bank0.asm` + `gameplay5m0_bank1.asm`; använd dem bara för reproducerbar misslyckad diagnostik.

[GAMEPLAY-5 H3 två nya fysiska tre-fienderförsök — FAIL](https://github.com/Odourman/the-skraun/actions/runs/45047010682): `experiments/gameplay5h3_bank0.asm` + separata same/sep-bank1. Same-Y-source-/paletteväxling 93/94 bildrader, separated Y med per-band P1 RESP1/COLUP1 277/287 rader. K2+Ranger X/Y i separata logiska RAM-register; **inte tre korrekta oberoende renderade fiender**. Dessa försök är diagnostik och ingen kanonisk kompromiss.

## Gränser
Fullständig 76-cyklersinstruktionsledger per faktisk rasterrad och TIA-colour-clock-skrivningsdeadlines: NOT VERIFIED; RIOT stack-highwater och alla nested call/interrupt-flöden: NOT VERIFIED. Svärd-hinder gate finns SOURCE_ONLY men block-/oblockpar med båda riktningar är NOT VERIFIED. Extra liv vid 2000 och kompletta 8-banpendeln är ärvda och inte omtestade i denna sprint. Full X/Y-halo är inte integrerad, eftersom fysisk M0/H3-överbelastning inte gav trovärdig plats för ännu en sen PF2-skrivning; ingen befintlig räckvidd reducerad.

Rapport: `docs/gameplay5/ROMDEV_GAMEPLAY5_MAIN_IV_DELIVERY_2026-11-22.md`. Draft PR #49, ingen main-merge. **STOP** för MAIN IV:s granskning.
