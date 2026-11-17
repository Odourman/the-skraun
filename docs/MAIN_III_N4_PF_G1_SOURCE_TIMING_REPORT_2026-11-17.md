# THE SKRAUN – MAIN III N4: PF-halo/hinder, verkliga källmasker, färgdeadlines och registerlivslängd

**Datum 2026-11-17. Status: SOURCE-ONLY RESEARCH / MAIN:s källgranskning. N4 utförd, med NEGATIVT resultat för direkt R3-färglösning och kvarstående arkitekturfråga. Ingen ny DASM/ROM, inga nya Stella-bilder, ingen oberoende VERIFICATION, ingen ny designcanon, ingen kart- eller mapperändring.**

## 1. Exakt källbas och varför den är giltig

- GitHub `main` observerad före arbetet: `5b8dc848fe051c288d58dc7316891c18d178769a`. Gällande [MAIN III N3-testkontrakt](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md), [design 01–60 och senare visuell/L3-korrigering](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md).
- **Original R3 assembler** `experiments/romdev_r3_overlap.asm`, fryst experimentgren `experiment/romdev-r3-decisive-scene-scheduler`, Git blob **`3c9ed79078eee6a0c63100614a593f92e240b5e8`**, faktiskt hämtad och läst med GitHub-anslutningen. [R3 negativ rapport](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md).
- **Verkliga R3 PF-masker** i separat verifierat och återhämtat [PF-REP1 original ZIP](https://drive.google.com/file/d/1AvRZt2oy496uWSYDhJubmepXOqm-SO5X/view): 13 X-värden **56,60,...,104**, ursprungliga 26 halo/scenery-källmaskgrupper 5×19 byte och 177 byte `RingRowMap`. ZIP 7603 byte, omräknad SHA256 **`d1c409ece3254833e6199c665bb8a8e2ca3d43a77d7cc222dc310f7f69a8da99`**, CRC OK. Den arkiverade originalblob-referensen stämmer med direkt GitHub-källan.
- **PF-REP1B original villkorlig scheduler** från [Drive-arkiv](https://drive.google.com/file/d/1mEpLUB6jMd5UyUyav1gRlVK63fjQ4IVd/view): 17537 byte, omräknad SHA256 **`af7b6e75ccef34392f10e92ba857b24532a2f8db4ec9b15fede15e65e0504b27`**, 9 filer och CRC OK. Samma source-CSV/JSON, kod och tidigare förenklade 3/5-cykelmodell är kopierade i N4-leveransen.
- [RESEARCH II G1/HYP-C2-rapport](https://drive.google.com/file/d/1MtA0edh0hCOa-OoIBDNITml7k18FYvJD/view), [PF-REP1C negativa resursägartester](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_SOURCE_AUDIT_2026-11-17.md), och N3:s S4/S5/S6 används som jämförelseregel.
- Hårdvarukällor: [Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) 228 colorclocks/fysisk linje, 68 HBLANK, 160 aktiva colorclocks, 76 CPU-cykler; [Andrew Davie Sessions 17–18](https://www.randomterrain.com/atari-2600-memories-tutorial-andrew-davie-17.html) om vänster/höger PF-fönster; [8Blit S04E01](https://8blit.com/s04e01/) med **ungefärliga konservativa PF registerfönster**; [Stella Debugger](https://stella-emu.github.io/docs/debugger.html) om CPU-radcykler och pixelposition. Dessa källor är INTE en ny autentisk Skraun-TIA-körning.

## 2. Vad som faktiskt kördes

En ny separat reproducerbar Python 3 source-only-gång, **inte ROM-kod**, genererade mask-, färg-, registerlivslängds- och timingtabeller direkt från fryst maskdata. Ingen av maskerna eller original-R3-filerna ändrades.

1. `N4_G1_SOURCE_REPLAY.py`: skapar `N4_ALL_SOURCE_MIXED_LINES.csv` (**832 poster = 416 fysikaliska rader × två hypotetiska H/S-ritprioriteter**), `N4_COLOR_WRITE_EVENTS.csv` (alla nödvändiga färggränser), `N4_R3_REGISTER_LIVENESS.csv` och `N4_RESULTS.json`. Det återger EXAKT den gamla PF-REP1B modellens resultat, men skiljer dessutom mellan permissiva heltalsavslut och en explicit **CPU/TIA 3-färgklocksfasmodell**.
2. `N4_PHASE_SENSITIVITY.py`: jämför explicit tre olika teoretiska offset-faser 0, 1 och 2 colorclocks mellan CPU store completion och TIA pixelvärdering. Det är en **känslighetsstudie**, inte en uppmätt verklig hårdvarufas.
3. `N4_REGRESSION.py`: kontrollerar originalmaskens Git blob, föregående PF-REP1B:s exakta 416-utfall, alla nya profiler, X80/X84 gränshändelser, positivia/negativa kontroller samt oberoende beräkning igen. PASS vid sista körningen.
4. `README.md`, `SHA256SUMS.txt`, scripts, resultaten och original-PF-data levereras i ett självständigt källpaket; varje datafil går att återskapa. Inga falska 6507-uppmätta timestamps finns.

**Viktig scenklassificering:** R3:s `M_halo` och `M_scenery` var ursprungligen två ALTERNATIVA lägen, inte två samtidiga färgplan i en fungerande R3-ROM. N4 använder den tidigare PF-REP1B:s *hypotetiska sammanläggning* för att visa vad en framtida fullspelsscen skulle behöva. H/S är **ännu inte beslutade användarprioriteter** för identiska PF-pixlar.

## 3. Omräkning från R3:s index till faktisk rasterposition

I originalassemblern `R3Pair` startar X=176 och kör X=176,174,...,2 i **88 par med två fysiska rader per par**. `RingRowMap,X` används sedan som källindex. En annan Y-världsdefinition i COL1 får INTE förväxlas med det här.

**Den ökända "row98" är X=98 i R3:s käll-loop, inte den absoluta TV-linjen 98.** För X=98 är antalet föregående arenarader `176−98=78`, så paret ligger på arena-rad **78 och 79**. Med R3:s **16 HUD-rader** före arenan blir det nominellt synligt regionindex **94 och 95**. Om första synliga TV-raden verkligen vore efter 3+37 sync/blank, vore nominell absolut TV-linje **134/135** (0-index). R3:s egen timer/start kan förskjuta faktiskt TV-läge; **den sista absoluta kopplingen är inte observerad i Stella och får inte användas som uppmätt värde**. Inom en *fysisk* linje gäller däremot den explicita 68 +160-klockorsmodellen för skrivfönstret.

PF0/1/2 är 20 celler per skärmhalva, vardera 4 TIA-colorclocks. PF1/PF2:s vänster->höger-omskrivningar måste ligga före den aktuella cellens bildstråle. De antagna källreferensfönstren i denna studie (CPU-cykelnummer inom raden) är vänster PF0 senast18, PF1 senast24, PF2 senast34; höger PF0 25–45, PF1 35–50, PF2 46–61. **De här tiderna är konservativa undervisningsfönster, inte uppmätta TIA-signalriktiga deadlines på Skraun.**

## 4. Exakt problemrad – originalmasker, inte illustrerade godtyckliga pixlar

De sex R3-maskregistren är `[L0,L1,L2,R0,R1,R2]`, med vänster PF0=0 i dessa syntetiska prov. Vid källmaskrad X=98, första av de två fysiska arenaraderna:

| R3 halo X | Sex bytes halo | Sex bytes scenery | OR-geometri i PF | Nödvändiga färgbyten mellan tända celler |
|---|---|---|---|---|
| 56 | `00 04 80 00 00 00` | `00 00 04 40 10 00` | `00 04 84 40 10 00` | 9→14, 14→19, 19→22 (3) |
| **80** | **`00 00 08 00 40 00`** | **`00 00 04 40 10 00`** | **`00 00 0C 40 50 00`** | **14→15, 15→22, 22→25, 25→27 (4)** |
| **84** | **`00 00 10 00 20 00`** | **`00 00 04 40 10 00`** | **`00 00 14 40 30 00`** | **14→16, 16→22, 22→26, 26→27 (4)** |
| 104 | `00 00 00 20 01 00` | `00 00 04 40 10 00` | `00 00 04 60 11 00` | 14→21, 21→22, 27→31 (3) |

**På just X80/X84 source row98 finns INGEN dubbelbokad exakt PF-cell** mellan halo och hinder; alltså kvarstår **FYRA färgdeadlines även när pixelprioritetskonflikten tillfälligt inte finns.** Vid andra X/rader finns verkliga cellöverlapp; de är en **separat** fråga som inte kan lösas med fler cykler.

För X80 källceller 14→15 ligger tänkt färggräns vid `68 + 4×15 = 128 colorclocks` in på fysisk rasterrad, dvs **128/3 ≈42,667 CPU-cykler**. Under den ***specifika*** modellantagelsen att TIA-färgbyte sker precis på CPU-avslut vid colorclock 3×cykeltalet med fas0 finns ingen **heltalscykel** som avslutas exakt på 128: lägsta är 43, högsta 42. X84 cell 26→27 ligger på `68+4×27=176`, vilket analogt blir 58,667; samma falsifiering för fas0. Detta säger INTE att verklig TIA har fas0, en viss registerlatens, eller att en 1–2 colorclocks synlig skarv skulle vara en otillåten användarkompromiss. Det säger att 3-cykels *source toy PASS* inte kan räknas som exakt bildsignal-bevis.

## 5. Full 416-fallsjämförelse per hypotetisk prioritet

Varje kolumn nedan har **416 fysiska source-baserade kombinationsrader** (13 X ×16 blandade tvålinjepar ×2 linjer). `PASS` betyder **endast att den angivna optimistiska abstrakta skrivjobbschemaläggaren** hittade ett schema. Det är INTE en assemblerad TIA-kernel eller ett spel.

| Modell / prioritet | H-guld PASS/416 | S-hinder PASS/416 | Källbaserad slutsats |
|---|---:|---:|---|
| Gammal liberal avrundning, **3 cycles/store** | 416 | 416 | Falsk trygghet om man tolkar det som en riktig kernel |
| Gammal liberal avrundning, **5 cycles/event** | 360 | 356 | Avslår 56/60 jobbscenarier; reproducerat exakt |
| Ny modell: **fas0 exakt 4-clock-cell, 3 cycles/store** | **316** | **312** | 100/104 fall blockerade under strikt phase0-fönster |
| Ny modell: **fas0 exakt 4-clock-cell, 5 cycles/event** | **288** | **284** | 128/132 fall blockerade under samma antaganden |

Separat fas-känslighet, fortfarande **3 cycles/store-ideal**:

| Antagen color-clock-fas för CPU-skrivning | H PASS/416 | S PASS/416 |
|---:|---:|---:|
| 0 | 316 | 312 |
| 1 | 260 | 252 |
| 2 | 288 | 276 |

**Tolkning:** Ingen av tre prövade fasta faser ger full 416/416 i denna strikta pixel-exakt + underladdad jobs-modell. Men faserna är teoretiska, tidsfönstren konservativa och vi har **inte** simulerat TIA-färgregisterlatens, A/X/Y-preservation, pipelining över föregående skanningsrad eller alternativa färg-/maskägare. Ett sådant modell-FAIL begränsar denna **specificerade kandidatklass**, inte original-Atari 2600:s generella möjlighet att göra ett nytt färgschema. Undvik både att kalla 316/416 ett faktiska pixels-pass och att kalla 100/416 ett hårdvaruomöjlighetsbevis.

Fas0 har 220 H respektive 236 S färgövergångar mellan *omedelbart intilliggande* upplysta PF-celler genom de 416 raderna, varav 128 respektive 136 inte sammanfaller med modellens heltalscykelgräns. Det är antal *händelser*, inte unika rader, och får inte läggas rakt till ovanstående fail-antal.

## 6. Verklig R3 X/Y-livslängd – direkt drop-in motbevisat

Läs original-ASM [rader 161–198](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm#L161-L198):

- `LDX #176`, `R3Pair`, `LDA Troll3,X`, `LDY RingRowMap,X`, `DEX` kräver **X som aktuell rasterrad, två gånger per loop**. Att förladda `X=#gold` permanent skulle förstöra radindex för sprite, PF och loop. Att återladda X efter `STX COLUPF` kostar minst en verklig extra instruktion/dataåtkomst och ett nytt tillstånd.
- `LDY RingRowMap,X` matar **fem `LDA (PFptr),Y`** med R3:s original L1/L2/R0/R1/R2-maskevent. På B-raden återanvänds Y till `LDY SpriteRowMap,X` + `LDA P1Buf,Y` + `STA GRP1`. Att förladda `Y=#stone` permanent skulle förstöra både PF- och fiendeindex. Y måste då återskapas eller alla data-åtkomster skrivas om.
- **A** bär omedelbart hämtade PF-maskbytes inför `STA PF*`; en förberedande `LDA #color` som används upprepade gånger kan skriva över nästa PF-data och kräva mer minnes-/registerarbete.
- De ursprungliga **R3 diagnostiska** worst-bildraderna beräknades i projektet till 72/73/74 av 76 cykler och inkluderade ännu inte verklig pil/orb/AI/HUD. Även fyra idealiserade `STX/STY COLUPF` per X80/X84-rad kräver 12 ytterligare CPU-cykler **UTAN** initiering, PF-indexändringar, P1, oscillator-fas eller projektil. Därför är **direkt införande av fler stores i oförändrade R3 B-linjer NO-GO på källnivå**. Det betyder inte att en **ombyggd** sparse-/specialkernel saknar möjlighet.

**HYP-C2:s egentliga resultat:** `STX COLUPF` och `STY COLUPF` är verkliga trecykelstores för zeropage TIA-register, men **permanent X+Y som färger i samma R3Pair-loop är registermässigt inkompatibelt med frysta R3-instruktioner**. I nuläget finns **ingen komplett legal registerlivslängds-/CPU-beam-tidslinje** för att uppfylla alla åtta PF+COLUPF write-jobbs och P0/P1 samtidigt. Detta är en användbar falsifierad *drop-in-kandidat*, inte en universell fysisk NO-GO.

## 7. S5 och S6: ändlägen, andra färgägare, kvarvarande risker

- **S5 ändlägen X56/X104:** På källmaskrad98 krävs tre färgövergångar, färre än X80/X84:s fyra. Det är inte legitimt att testa enbart X56/X104 och därifrån dra slutsatsen att 13 X-varianter fungerar. Den nya CSV-filen innehåller alla X och båda fysiska raden i varje 16 gemensamma källpar.
- **S6 objektägande:** `P0+M0` delar `COLUP0`, `P1+M1` delar `COLUP1`, `PF+BL` delar `COLUPF`, resten `COLUBK`. En Ball kan inte stå för en oberoende gul ring med blå PF-hinder. Om M0 ritar pil kan den ärva grå Skraun-färg, om M1 används är den bunden till riddare/bågskyttens röd/gröna färg. Ett alternativt ägarupplägg är ingen verifierad lösning förrän färg, geometri och projektil/orb-beteende för samma fysiska rad är budgeterade.
- **Identisk PF-cell:** på vissa andra positioner (sex X totalt: 64,68,76,80,84,88) begär halo och scenery samma fyra colorclocks. En enda fysisk pixel kan inte ha både blått och guld. Den hypotetiska H/S-ritprioriteten är inte ett användargodkänt stilbeslut, och spelets LOGISKA halo-through-obstacle och solid-body/sword/arrow-blocker får inte ändras på grund av ritprioritet.
- **Bakgrund som haloring:** `COLUBK` färgar alla lediga pixlar i sin horisontella färgzon; den skapar inte på egen hand en ringformad mask. Alternativet behöver lika strikt mask-/färg-/beam- och resursmodell, inte bara ett nytt register.
- **3-raders-/displaylist- och specialkernel-alternativ:** De kan ge ny *arbetsfördelning*, men inte två färger i samma pixel, ett gratis P1, en gratis pil/orb eller fler än 76 cykler per fysisk rad. Sådana andra arkitekturer är **ännu inte falsifierade** av direkt-R3-negativet.

## 8. N4 disposition och nästa beslut

**N4 källgranskningen är KLAR**, och gränserna är tydliga:

| Hypotes/underfråga | Utfallet | Beslutsstatus |
|---|---|---|
| Ursprungliga R3 masker, alla 13 X, 16×2 blandade rader | Omräknade/reproducerade från originalblob; CSV/JSON & SHA | **SOURCE-DATA PASS** |
| Gammal PF-REP1B 416/416 för 3-cykel-only | Reproducerat som abstrakt modell; bristfälligt full-kernelbevis | **SOURCE REPLAY PASS; ENGINE GO EJ VISAT** |
| Exakt CPU color-clock lattice under phase0/1/2, endast store-jobs | Varje prövad fas ger minst ett FAIL; känslig för fas och pixel-latch-antaganden | **MODEL-CONDITIONAL NEGATIVE** |
| HYP-C2 `STX/STY` direkt i original R3 utan ombyggnad | X/Y redan nödvändiga som rad-/källindex; R3 ~72–74/76 före nya stores | **DIRECT DROP-IN NO-GO** |
| Ombyggd sparse PF + lookahead + ny registerlayout | Något nytt komplett schemakontrakt har ej bevisats | **OPEN / INTE MOTBEVISAT** |
| Gold/stone exact-overlap ritprioritet | Fysiskt entydigt val krävs när samma cell begär två färger | **ÖPPET VISUELLT BESLUT, INGET ÄNDRAT** |
| G2 ny DASM/Stella färg-mikro-ROM | Saknar tillräckligt avgränsad överlevande källsekvens | **INTE AUKTORISERAD/INTE STARTAD** |

**MAIN rekommenderar:** **beställ INTE G2/färgmikro-ROM eller R4/B3c från den nuvarande X/Y-preload-hypotesen.** Dokumentera detta som en avfärdad direkt drop-in och behåll [#25](https://github.com/Odourman/the-skraun/issues/25) öppen. Nästa rimliga research inom PF-spåret vore en särskild **N4B source-only register- och lookahead-arkitektur** med en verklig kandidat som visar att PF-left-data kan förberedas föregående fysisk rad, att hela X/Y/A-ägarskapet hålls och att real 6507 write-tider kan genereras utan full P1/arrow/orb-stöld. Om sådan inte går att få fram, lämna explicit NO-GO för *den* kandidaten innan ROM.

**Parallell väg enligt MAIN:s tiostegsplan:** N5 **source-only samma-Y P1-fiendekernel** kan prövas oberoende medan PF #25 är öppet. Undvik att ett ofullständigt färgprov blockerar alla andra forskningsspår. Ingen automatisk implementation eller godkänd fullspelsteknik följer av den här analysen.

**Alla källposter, beräkningsresultat, 832 scenrader, enskilda tidsjobb, registertabell, tre fasprov och regression finns i levererad ZIP och GitHub-/Drive-rapport.** Reproducerad som source-only CPU-/färgmodell; inga riktiga Skraun-TIA-cykler eller nya Stella-fotografier genererades.
