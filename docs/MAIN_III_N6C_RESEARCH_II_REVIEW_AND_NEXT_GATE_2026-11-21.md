# THE SKRAUN – MAIN III granskning av RESEARCH II:s N6-C-leverans och nästa grind

**Datum:** 2026-11-21  
**Klass:** MAIN III granskningsbeslut, source-only; **ej** ny spelcanon, ej ROM/N7-arbetsorder, ej independent Verification.  
**Beslut:** `RESEARCH_II_N6C_BOUNDED_RESULTS_ACCEPTED_WITH_LIMITATIONS / FULL_RENDERER_NOT_PROVEN / N6_C_OPEN / N7_NOT_AUTHORIZED`.

## 1. Direkt kontrollerad leverans och auktoritet

- RESEARCH II [overlämning Issue #30, kommentar 7063415027](https://github.com/Odourman/the-skraun/issues/30#issuecomment-7063415027).
- Forskningsgren `research/n6c-p1-timing-sourceonly-20261121`, leveranstip `82788be294f4741e35d4c05811d2efea4a0a32b6` (GitHub fetch_commit). Jämförelse mot main visar **endast fyra nytillagda forskningsfiler**, ingen produktionskodeffekt. Gren divergerat eftersom main fortsatte separat; **merge inte utförd eller beställd**.
- [Rapport, Git blob `37f045b93ba40d9ee7d326ef390c138ea5801115`](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/RESEARCH_II_N6C_PHYSICAL_P1_DECISION.md).
- [Skript, Git blob `837876a0ada55c9a00c9feb520dbed877443da40`](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/N6C_COMPACT_SOURCE_REPLAY.py).
- [Fryst JSON, Git blob `1cc2c316b2866fde06870f2869ffad638ee7ce94`](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/N6C_SOURCE_COUNTEREXAMPLES.json) och [README](https://github.com/Odourman/the-skraun/blob/research/n6c-p1-timing-sourceonly-20261121/research/n6c_2026-11-21/README.md).
- Scriptet är en frusen källmodell med hårdkodade R3 8-rads fiendebitmappar och en valfri exakt blobkontroll. MAIN gjorde separat omräkning av rad-/gapvillkoren från de 24 källbyte som finns i skript/rapport: S1/S2-close/S3 trevägsradmodell ger **5 konfliktande av 16** ompositioneringar vardera i F2a; naiva bitmap-/color-write gap fail **S2-close 7/16, S3 3/16**. Dessa överensstämmer med rapportens JSON. Detta är **MAIN källgranskning, inte oberoende Verification**, och inget nytt TIA-hårdvaruprov.
- Användarens angivna ZIP, 9 filer, 21 274 bytes, SHA256 `9e992429cbaefe05655d0114e027d3f7ce0e2a712c7abd3309d10b17ce1e8732`, har **inte separat verifierats av MAIN från en ZIP-bytefil**; endast de faktiskt tillgängliga fyra versionshanterade forskningsfilerna granskades här.

## 2. MAIN:s beslut per arkitektur

| Variant | Källbaserad disposition | Viktig begränsning |
|---|---|---|
| F1 – P0-lån som enda tredje fienderesurs | **AVSLÅ som universell** | Skraun L3 upptar alla 16 same-Y-fienderader S1/S3. Opportunistiskt P0-lån i lediga andra band fortfarande möjligt |
| F2a – en reguljär P1-huvudkopia per fysisk rad, RESP1-preposition före nästa | **AVSLÅ inom modellens explicita villkor** | S2-close 5/16 right→left wrap behöver X67 reset innan den utgående R-X101-spriten ens visats. Exempel RESP klock130, Ranger första pixel klock171: reset 41 clocks tidigare. Modellen använder ungefärlig RESP-main delay, INTE cycle-perfect TIA-mätning |
| Naiv helinstruktions `GRP1/COLUP1` mellan tätt litna pixlar | **AVSLÅ som generell schemametod** | 7/16 naiva close-gap rows, 3/16 S3 rows, men förladdad tidigare instruktion med STORE-completion efter sista gamla pixel kan i vissa fall rymmas |
| F2b – `NUSIZ1/RESP1` reset-retrigger, GRP1/COLUP1 pipeline, VDEL | **FORTFARANDE ÖPPEN** | Kräver verkligt korrekt X-positionering, tre olika bitmaps/färger, P0-busy, PF-radmasker och 76cy per linje, inget source-only full-PASS |
| Alla sammanslagna P0/P1/PF/BL/M0/HUD, 128B | **EJ BEVISAD** | Forskarens 24-opcode pappersrad 58/76 eller 64/76 är ENDAST PF+P0+första P1; två ytterligare fria X/P1 och full objektägare/timing saknas. Inga skäl till N6-stängning |

**Särskilt MAIN-korrigering:** Påståendet att två 3-cykels STA måste förbruka 18 lediga pixelklockor INOM exakt mellanrum är **inte** ett generellt förbud. En registerskrivning kan påbörjas före gamla figurens sista tända pixel och *avslutas* efter, inom fönstrets TIA-fas. Skriftliga optimistiska källmodeller visar 0/16 sådana isolerade återstående STORE-completion-fails vid S2-close/S3, men de ger **inte** gratis positionsomladdning/GRP byte/NUSIZ/PF och är inte automatisk fysisk genomförbarhet.

## 3. Revisionskrav innan vi hävdar fysiskt GO

1. Den exakta `RESP1/NUSIZ1`-reset/retrigger- och VDEL-latchsemantiken måste observeras i **riktigt ASM-körande Atari 2600/NTSC-Stella**. Source-only-approximationen på `RESPnext = 68 + nextX -5` kan inte bära en generell hårdvaruslutsats.
2. En fullständig fysisk/opcode tidslinje måste senare täcka två/tre P1-fiender (inklusive Ranger annan färg), P0 L3, PF B/ON original X80/X84 mask bytes, BL/M0 och HUD utan antaganden om gratis mängd `STA` eller dolda ROM-banker.
3. `R3 state23B + P1Buf89B=112B` är gamla diagnostiska data, inte godkänd framtida buffert; ingen 128B RAM/stack-live proof levererad.
4. Svärdsvarningen i 24 NTSC-rutor är fortfarande **inte** byggd som R3-source bitmap; här måste en fryst/läsbar varningspose skapas/auktoriseras separat innan ett framtida spelrendering-PASS.

## 4. MAIN:s snäva N7-rekommendation (FÖRSLAG, ännu EJ AUKTORISERAT)

**När användaren ger ett nytt uttryckligt GO, först då** lämna till ROM DEVELOPMENT ett enda, minsta original-Atari-2600 NTSC mikro-ROM-test med en exklusiv hypotes: `F2b kan visa tre oberoende same-Y-fiender med korrekta bitmaps/X/färger under 76c när P0 är upptagen`.

Första prov:
- S2-close knights X67,X83 (symboliskt samma ljusblå `COLUP1`) + Ranger X101 (annan världs-kamouflerad `COLUP1`), 16 gemensamma fysiska fienderader, både permutations- och reverse-X stress, minst 12 sammanhängande renderade bildrutor; inga ersättnings-NUSIZ-identiska kopior som låtsas vara unika aktörer.
- S3 P0 U1-LEG1 L3 X104 samtidigt med knights X105/124 Ranger X147; P0 får inte tas bort eller oavsiktligt flyttas. Mät `RESP1/NUSIZ1/GRP1/COLUP1/HMOVE/VDEL` i Stella debugger, colorclock och complete write phase.
- PF B/ON X80/84 OR-komposit på omstridda källrad 98 → arena Y78/79 och en tydligt dokumenterad M0/BL-reservation; om de inte fysiskt renderas i det minimala provet får det inte upphöjas till fullscene-GO. Vid verklig integration är M0/BL, svärdsvarning, HUD, RAM/stack och AI fortfarande öppna.
- **STOP:** fienderna tappar självständig X, färg/bitmap fel, P0 försvinner, gränsskrivning för sen, visuell duty faller till R3 20Hz, eller 76c/rad överskrids. Redovisa ett konkret första fail, då inga fler generella löften om F2b.
- Leverans vid eventuell separat auktorisation: `.asm`, `.bin`, DASM-logg, Stella trace (scanline/cycle/RESP/NUSIZ/GRP1), 12 bildrutor med scenpositioner, SHA256 manifest, PLAYTEST. Endast självtester av ROM DEVELOPMENT; **VERIFICATION II ska sedan få separat oberoende order av MAIN**.

**Ingen ny ROM, assembler, konst, N7 eller independent Verification initierad genom detta beslut.** Efter ett eventuellt F2b mikroROM-negativ blir nästa steg ett användarval mellan kreativa kompromisser (RESEARCH II föreslog lokal fien­der-only row striping eller en väl signalerad visuell Y-offset), inte automatisk minskning av fiendeantalet.

## 5. Gällande estetiska/gameplaykrav skyddas

Tre samtidiga fiender, två ljusblå riddare med P1-integrerat svärd som designriktning, världskamouflerad ranger, ljusgrå U1-LEG1, större halo per level, färgmodell B (PF+BL värld när OFF/guld ON), åtta öppna hinderbanor och level3 framkomlighet behålls. Ingen slutlig färg- eller storlekskod bestämd. [Designbesluten](DESIGN_DECISIONS_01-60_2026-11-16.md) och [rörlighetsgrind #23](https://github.com/Odourman/the-skraun/issues/23) gäller fortfarande.

**Slutstatus:** `N6_C_RESEARCH_BOUNDED_RESULTS_ACCEPTED / N6_C_FULL_76C_BEAM_RIOT_GO_OPEN / N7_PENDING_USER_EXPLICIT_AUTHORIZATION`.
