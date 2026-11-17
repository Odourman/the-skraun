# THE SKRAUN – MAIN III N5: tre fiender på samma Y och är hela spelet realistiskt på original-Atari 2600?

**Datum 2026-11-17. Klass:** MAIN III:s källgranskning och självständig kontroll av *redan existerande autentiska* Stella-bildrutor samt source-only motexempel. **Ingen ny ROM, inga nya Stella-exekveringar, inga spel-/grafikbeslut, ingen oberoende VERIFICATION.**

## Kort beslutsbesked

**Grundspelet: realistiskt som Atari 2600-spel. Den nuvarande *exakta, samtidiga, lågflimrande fullscenen*: hög risk och sannolikt inte möjlig med den redan testade standard-TIA-arkitekturen utan synliga kompromisser.** Det går inte att bevisa en generell omöjlighet för ALLA ännu outforskade 6507-kernels; lika lite går det att lova att en specialkernel löser den. Att bygga ett fullständigt spel på basis av R3, PF-REP1B och COL1 nu vore tekniskt oförsvarligt. **GO för EN sista avgränsad N6 SOURCE-ONLY gemensam arkitektur-/STOP-granskning. NO-GO för fullscens-ROM, automatisk R4/B3c och produktionsimplementation.**

Detta är en riskbedömning baserad på verkliga maskinresultat, inte en numeriskt kalibrerad sannolikhetsprognos. Det svåra är inte åtta banor eller spelets regler i sig. Det svåra är att samtidigt visa upprätt stor grå Skraun, tre separata same-Y fiender (två distinkta riddare och en grön archer) med synlig ~0,4s svärdsvarning, rörlig guldhalo och annorlunda färgade solida hinder på samma raster, pil, orb, HUD och ännu tillräcklig 6507 CPU-/RAM-budget.

## 1. Käll-/autoritetsspårning och nytt objektivt underlag

- [Bindande designbeslut 01–60 samt senare användarkorrigeringar](DESIGN_DECISIONS_01-60_2026-11-16.md); [visuellt fastställd U1-LEG1 och storleksregel](SKRAUN_VISUAL_DIRECTION_2026-11-16.md); [MAIN III N3 S0–S9 testkontrakt](MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md).
- Fryst R3 originallokal ASM motsvarar exakt GitHub blob SHA `3c9ed79078eee6a0c63100614a593f92e240b5e8`: [original faktisk R3-overlap ASM](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/experiments/romdev_r3_overlap.asm) och [färdig ROM DEVELOPMENT R3-rapport](https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md). PR #14 är DRAFT/unmerged.
- **Äkta gammalt Stella-material hämtat på nytt i denna N5-session från projektets Drive:** [R3 ORIGINAL COMPLETE MAIN DELIVERY wrapper](https://drive.google.com/file/d/144hABkr1rC0blhz5kGsolrzFwLb6_RtG/view), 304132 bytes; dess inre fullständiga 184-filars ZIP hade SHA256 `ac71c5aef26f3c66ba18dac042d89ecc7fb150aab926d526d37fa625d5330e96`, matchade `PACKAGE_SHA256.txt` och klarade ZIP CRC. Tre verkliga 4K DASM/NTSC-frysta ROM-filer source + genuine Stella 6.7.1 PNGs och originalkontrollskript ingår. N5-kopian bevarar endast **36 oförändrade äkta Stella seq_00..11 PNGs** (12 av vardera overlap, partial och stagger), original tre ASM, det nya reproduktionsskriptet och beräknade CSV/JSON-data. **Dessa är äldre Stella-captures, INTE en ny original-Stella exekvering i N5.**
- Kompletterande verifierade tidigare tekniska utfall: [N2 COL1 isolerad 6507 kollisionsbudget](MAIN_III_P01_COL1_N2_WORST_CASE_CPU_RIOT_STACK_AUDIT_2026-11-17.md); [N4 negativa PF/COLUPF-källtestet](MAIN_III_N4_PF_G1_SOURCE_TIMING_REPORT_2026-11-17.md). Båda är *snäva*, kan inte bevisa full scen.
- Hårdvara: [Ataris ursprungliga Stella Programmer's Guide](https://www.atariage.com/2600/programming/2600_101/docs/stella.html) bekräftar 76 6507-cykler/fysisk scanline, endast P0 och P1 som två oberoende åttabits sprites, två missiles och Ball, fixed-spacing NUSIZ copies, WSYNC/HMOVE, och 128 byte RIOT RAM. [Steven Huggs moderna 2025 three-stream-förstudie](https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html) visar lovande *kandidattekniker* men med **max tre valda registeruppdateringar per scanline i hans exempel**, 32B/display-list och en olöst display-list-rebuild varje frame; det är inte ett bevis på tre olikfärgade same-Y fiender plus tvåfärgat PF/halo i just The Skraun.

## 2. N5 – ny oberoende pixelomräkning av verkliga R3-Stella-bilder

Original P1-representation: `EnemyX0..2`, `EnemyY0..2`; två **olika** röda R3-riddarbitmappar och färger `$44`/`$48`, en **grön** archerbitmap och färg `$C6`; NUSIZ1=0 ger en P1 8-clocks bred (ingen gratis tredubbling). `Slot` väljs om varje frame. `ClearSpriteBuffer` nollställer 89B, `DrawSpriteIntoBuffer` matar BARA den valda figuren, `SelectP1` väljer dess X och färg. P1 har därmed en **aktör per 60Hz frame på samma Y** enligt originalkoden; det är källbestämt.

Det nya `N5_SOURCE_AND_STELLA_REPLAY.py` öppnar varje fryst 320×228 PNG, läser exakt RGB per pixel och räknar alla färgdomäner utan att återanvända gamla publicerade sammanfattningssiffror. Kontroll: grå P0 1320 pixlar och HUD placeholder 1968 pixlar per frame; nedan observerat **12 ÄKTA original-Stella frames**, inte simulerad utdata:

| R3 originalfall | Riddare 1 | Riddare 2 | Bågskytt | Halo guld | Hinder blå | Vad det BEVISAR |
|---|---:|---:|---:|---:|---:|---|
| **Samma Y**: (32,78), (101,78), (147,78) | **4/12** | **4/12** | **4/12** | 6/12 | 6/12 | Tre individuella positioner, men 20Hz/figur och separat 30Hz PF-färg per HEL frame; INTE full tydlig simultan grafik |
| **Två Y överlapp**: (36,75), (105,82), (149,141) | **6/12** | **6/12** | **12/12** | 6/12 | 6/12 | 30/30/60Hz fungerar i just denna Y-arrangering, men R3 har observerad ~94% P0-skymning av en röd riddare i visst läge |
| **Tre skilda Y-zoner**: (28,20), (111,80), (149,141) | **12/12** | **12/12** | **12/12** | 12/12 | 0/12 | 60Hz tre actor-delar när Y-mönstret är glest; skogen/hindren saknar då självständig blå färg |

För den **riktiga same-Y R3** är varje fiendes cykliska sekvens `100100100100`, `010010010010` respektive `001001001001`; längsta obrutna bortavaro **två frames** varje gång (ca33 ms vid nominella NTSC60). En ~0,4s sword windup motsvarar nominellt 24 frames. **Om den observerade 12-frame schemaläggningen upprepas oförändrad** blir riddaren synlig på **8/24** och frånvarande på **16/24**; detta är en **MATEMATISK 24-frame PROJEKTION, inte observerade 24 Stella-bilder**. En förvarningsgest har inte implementerats i R3, alltså är den gestens faktiska läsbarhet OPRÖVAD, inte ett uppmätt FAIL. En annan separat PF-varning kan teoretiskt hjälpa men den krockar med redan blockerad halo+hinderyta och kräver separat bevis.

## 3. Test mot S1–S3: vad olika multiplexeringsidéer faktiskt kräver

### A: En hel och unikt formad P1-aktör per fysisk BILDRUTA (exakt R3 same-Y-klass)
På **12** bildrutor finns precis **12 P1 aktör-frame-platser**. Tre fiender på 20Hz kräver sammanlagt 3×4=12 platser, och R3 uppnår just det. Men tre på minst 30Hz skulle kräva 3×6=**18 platser**, minst40Hz 24 och60Hz 36. **Matematiskt OMÖJLIGT i just klassen 'högst en P1-fiende per 60Hz frame'**; gäller oavsett hur smart innehållet roteras. Det är **inte** en sats om varje tänkbar 2600-kernel; för bättre samtidig bild måste den klassen överges och mer än en aktör/scanline eller en ny blandad representationsklass byggas.

Ett särskilt prioriterat P1-slot för riddarens sword cue under ~24 frames kan synliggöra honom oftare, men då försvinner i stället de andra aktörerna oftare. Det är en designkompromiss och INGET användarbeslut har tagits om tillåtna frame-duties.

### B: En unikt formad P1 per fysisk RASTERAD (Venetian/striping)
Antag 16 fysiska bildrader per tvålinjers 8-source-row-fiende, tre fullt samtidigt aktiva exakt same-Y fiender. Tre fullständiga silhuetter kräver 3×16=**48 aktör-rad-platser**; med bara **en unikt formad P1-aktör per fysisk scanline** finns bara16. Högsta sammanlagda fullradstäckning =16/48=**33,3% per aktör i genomsnitt**. Att rotera de spridda raderna mellan frames kan få ALLA tre att vara delvis synliga varje frame, men skapar tre vertikalt sönderskivade former och kräver extra P1 färg/X-byte mellan rasterrader. Ingen verklig Stella- eller cycle-/RAM-budget har provats för denna omritade klass, och den bevisar inte att den ser bra ut. **PF-sparsifiering kan inte kompensera saknade P1-radslots.** Det är en användbar forskningskandidat, inte en spelmotor.

### C: Hårdvarans NUSIZ 2-/3-kopior
NUSIZ-kopior har bestämda inbördes avstånd och samma Player-bitmap vid en given linje, utan fria oberoende färger; det är **INTE** två olika röda svärdsriddare + grön bågskytt med full fri fiende-X. Kan bara bli aktörtroget med ytterligare verkligt tidssatta intra-line GRP1/COLUP1/positionsskrivningar, vilket är en ANNAN kandidat, inte gratis tredje sprite.

### D: Snabb P1-uppdatering INOM samma rasterrad
En grov naiv metod försöker göra `STA GRP1` + `STA COLUP1` efter att första fiendens 8-clocksbredsvita slutar men före nästa identiska 8-clocksrasterstart. Två zero-page TIA stores **minst 3+3 CPU-cykler = 18 TIA färgklockor** – *före* någon självständig `RESP1`/`HMP1` positionering, laddning och extra PF/P0-kod.

| Syntetisk adversarial scen från N3 | Sorted enemy-X | Fria clocks mellan 8-clock-sprites | Räcker 18 clocks för BARA två stores? |
|---|---|---|---|
| S1 ursprunglig full overlap | 32, 101, 147 | 61, 38 | JA som naken två-store-avståndsgräns; **hel kernel fortfarande obevisad** |
| S2 permutation | 40, 80, 120 | 32, 32 | JA som isolerad förenklad avståndsgräns |
| **S2 nära** | 67, 83, 101 | **8, 10** | **NEJ** |
| **S3 nära P0** | 105, 124, 147 | **11, 15** | **NEJ** |

Denna **begränsade** negativa kontroll antar ingen förtida färg-/bitmapskrivning som förvränger den föregående aktören, ingen automatiserad NUSIZ-kloning, och att de två nödvändiga värdena skall bli giltiga mellan aktörerna. En helt annan TIA latch-ordning, föregripande skrivningar eller interline representation kan kringgå just denna enkla modell; att bevisa det kräver riktigt instruktion/rasterarbete och ny separat MAIN-auktorisation. En RESP1-strobe kan även ha effekter på följande scanlines. **Vi har INTE bevisat att tre på samma rad är universellt omöjliga på original-TIA.**

### E: Vertikala zoner, two-/three-line eller Hugg three-stream
Samma Y-problemet försvinner om fienderna *redan ligger i skilda Y-zoner*. Men AI får enligt canon röra sig fritt och användaren har INTE auktoriserat att tvinga fiender att aldrig överlappa. Att dra nytta av separation när den uppstår är korrekt; att anta den permanent i hårdvarubudgeten är fel. Hugg visade smart display-list sharing, men demonstrationen med tre valda registerwrites per scanline, extra RAM för listor och svår listplanering per frame utgör INTE ett konkret S1/S2/S3 PASS, särskilt inte samtidigt med guld/sten PF-färgscheman och P0 vid L3.

## 4. Varför dessa problem multipliceras, inte adderas

- **Samma rasterrad**: original R3 worst B=72/76 (overlap),73/76 (partial),74/76 (stagger), kvar bara4/3/2 statiskt; en ny GRP1/COLUP1/RESP1 eller `ENAM0/ENABL` kan inte läggas till utan att byta kernel/arbete och dataförberedelse. R3 har INGEN riktig pil/orb/svärd/AI/fysik/HUD (16-rads HUD är färgblock).
- **Färglager**: original P0/`COLUP0` binder M0:s färg, P1/`COLUP1` binder M1:s, PF/`COLUPF` binder Ball; `COLUBK` är övergripande bakgrund. Att 'låna M0/BL som halo eller pil' är inte en oberoende färgkanal. N4 prövade X80/X84 med flera PF/COLUPF färgövergångar och direkt R3-drop-in NO-GO; ny source-/real-kernel krävs även om N5 får P1 att fungera.
- **RAM**: R3:s 23 byte state + 89B P1Buf = **112 av 128 byte RIOT**, 9 bytes tydligt oanvända `$97..$9F` om resten av högminnet måste stå emot stack. N2 COL1 använder 28B *i sin egen diagnostik*. Naiv R3 112+COL1 28=**140>128** redan före fiende-AI, actionstater, orb, pilar, poäng. De kan inte bara länkas ihop. Optimering, borttagning eller ömsesidigt exklusiv byte-liveness måste visas; inga extra RAM-byte uppstår via ROM-bankning.
- **Källsilhuett**: användaren godkände exakt U1-LEG1 A/B med upprätt troll och samma form skalad L1/L2/L3, inte 'P0 får bli ett enklare fyrbent streck'. L3:s ca32×36 verklig P0-bild är separat diagnostiskt visad; större P0 kan också skymma fiender. R3 partial hade en återgiven situation med **128/136=94,1% av en röd riddars pixels dolda**, även då den var aktiv på sin P1-slot.
- **Scen och gameplay**: en cirkulär halo som logiskt passerar solida hinder kan implementeras som SEPARAT mjukvarufysik, men den visuellt självständiga guld-ringen på samma rad som kontrastfärgade stenar är det olösta kravet. Solid kropp/svärd/pil måste använda logisk kollision, inte lita på utbytta PF färgbitar.
- **Åtta banor**: sannolikt hanterbart med statiska hinderdata/ROM-bankning och source-only K0 utgör grund; de åtta framtagna geometrierna är *icke kanoniska utkast*, inte åtta faktiska spelbara banor. Fyra världar och HUD/score är inga enskilda omöjliga kravnoder, men alla kostar ROM/RAM/CPU och TIA.

## 5. Sannolik genomförbarhet per krav – saklig teknisk värdering

| Del av Skraun | Bedömning NU | Det som saknas för ordentlig GO |
|---|---|---|
| 8-vägs joystick och smidig level3-kollision i EN öppen arena | **TROLIGEN GENOMFÖRBART**; P01-COL1 har riktiga Stella-prover och N2 konservativt timingbevis inom isolerat P0-scope | Samma input/collision tillsammans med AI/halo/fiender och oförstörd 6507 frame-budget |
| U1-LEG1 A/B och tre större storlekar | **TROLIGEN GENOMFÖRBART TEKNISKT** i isolerat P0, exakta visuella slutgrindar öppna | Full bildmask/sprite-överlapp, L3 ART1 #19 och fysisk läsbarhet med P1 |
| Åtta öppna banor och fyra världar | **TROLIGEN GENOMFÖRBART** med ROM-data/bankning, inte åtta fulltestade banor | Framkomliga slutkartor, RAM/ROM-ledger, väl fungerande ritkernel och spelintegration |
| Fiende-AI för två riddare + en flyende archer; skador/orb/timer/score/ljud | **LOGISKT MÖJLIGT; genomförbarhet med full renderer OPRÖVAD** | VBLANK/overscan maxcykel, RAM-liveness och verklig en-ROM-scene |
| Tre olika same-Y fiender med pålitlig läsbar sword cue | **KRITISK HÖG RISK; R3 nuvarande lösning visuellt otillräcklig** | Ny same-Y P1 fysisk kernel/mönster som klarar S1–S3, 12/24 råframes och worst timing utan att ta P0 |
| Separat gul halo och annorlunda färgade solida hinder i SAMMA frame/raster | **KRITISK HÖG RISK; direkt R3/N4 negativ** | Source-programmerbar percell/perregister deadline, bevisad COLUPF/PF fysisk maskkonflikt inklusive user-priority |
| Pil + orb + HUD tillsammans med ovanstående och all logik | **HÖG RISK; inte gemensamt testat** | En enda gemensam fysisk register-/RAM-/cykelägartabell och 262-line echte Stella-prototyp |
| Full arkadupplevelse helt utan synliga kompromisser på stock 2600 | **LÅG BEVISAD GENOMFÖRBARHET; skulle INTE lova leverans** | Minst två separata kritiska source-GO och verklig integrerad ROM; risk att kompromisser eller annan plattform behövs |

Ett påstått "bevis" som visar spriteflimmer i separat ROM, halo i en annan och collision i en tredje är **inte sammansatt bevis** och kan inte godkänna hela spelet. Det finns ingen hederlig numerisk procentsats att härleda ur dessa resultat för att beskriva sannolikheten att en framtida helt ny specialkernel lyckas.

## 6. Vägarna framåt och en rimlig STOP-regel för att inte piska en död häst

**A – Original Atari 2600 som oförändrad målhårdvara: ett sista avgränsat tekniskt försök, sedan svart på vitt.** N6 måste inledas source-only med en ENDA gemensam värstascen och verkligt föreslagen register-/färgägarfördelning samt cycle- och 128B byte-liveness per sprite/halo/HUD/pil/orb/AI. Kräv minst S1 same-Y, S2 close och S4/S5 PF-mask samtidigt och läsbar ~24-frame sword cue. En ny kärna får varken baseras på 20Hz full-figur-flicker som "godkänd" eller anta tre permanenta separata Y-banden. **Om N6 inte kan presentera en sammanhängande kandidat med faktisk realistisk tids-/RAM-redovisning: STOP för oförändrad fullscen på stock 2600.** Rekommendera då explicit nytt användarbeslut i stället för planlös fler-rapport-ackumulering. En source-only plausibel kandidat kan ge en separat av MAIN avgränsad riktig DASM/Stella mikro-ROM innan full engine; ett source-PASS är inte en maskin-PASS.

**B – Troget SPEL på original Atari 2600 med uttalade visuella kompromisser:** behåll overhead, upprätt U1-LEG1, tre storlekar och attack/magi/8 arenor, men användaren skulle då behöva uttryckligen godkänna någon konkret kombination av (i) tidsmultiplexerad fiendesynlighet och en extra säker tydlig varningsmetod, (ii) mindre exakt visuellt separat PF-guld/solid-färg, eller (iii) färre aktiva fiender än två riddare+archer. Alternativ (iii) ändrar FASTSTÄLLD spelcanon och är därför inte auktoriserat utan användaren. Nya farliga svärdsvarningar får aldrig döljas som osynliga attacker. Dessa är **alternativ, inte beslut**. Om provresultatet blir otydligt eller störande ska vi inte lansera det som "fungerande" bara för att ROM körs.

**C – Behåll fullständig visuell ambition men ändra teknisk plattform:** Atari 7800 eller en annan sprite-kapablare maskin skulle underlätta flera av de specifika TIA-begränsningarna, men ändrar hela projektets plattformsmål och kräver explicit beslut. Ett 2600-superchip/DPC+/ARM-assisterat cartridgelager kan hjälpa RAM, logik och ROM-strömning men **lägger inte automatiskt till en tredje TIA Player eller ett andra individuellt färgat PF-lager**; kan inte antas bota S1/S4 utan realbevis. Inga sådana hardware cutovers auktoriseras av detta dokument.

## 7. N5-beslut, konkret nästa avgränsning

**N5 SOURCE-ONLY inklusive självständig kontroll av frysta autentiska R3 Stella 36 bilder: COMPLETE.** 
- Bekräftat exakt 4/12 same-Y per fiende, 6/12 partial två riddare +12/12 archer, 12/12 stagger; inte ny ROM/Stella och ingen riktig sword telegraph än.
- Bevisad otillräcklighet för R3-klassen **högst en oberoende P1-aktör per fysisk frame** om tre fiender ska visas med högre frequency; **inte** bevis på universell hårdvaruomöjlighet.
- Bevisad otillräcklighet för *en P1-rad per fysisk scanline utan midline reuse* att visa tre kompletta same-Y fiendebitmappar varje frame; Venetian row striping är en potentiell men otestad kompromiss.
- Fyra av åtta artificiella close-pair gaps mindre än 18 färgklockor med två minima zero-page stores under strikta inga-tearing-villkor; begränsat motexempel, inte universell real-TIA theorem.
- **N6: SOURCE-ONLY arkitekturbeslut/STOP. Inte automatiskt G2, R4, B3c, ny ROM, sprite, mapper, ban-canon, main-merge eller oberoende Verification.** R3 NO-GO, PF issue #25 och P01-COL1 #24 samt #1/#15/#19/#23 kvarstår oförändrade.

## 8. Reproduktion

Paketet har `N5_SOURCE_AND_STELLA_REPLAY.py` och 36 **frysta originalbilder** + tre **exakta original-ASM-filer**, `N5_REAL_STELLA_12_FRAME_PIXEL_AUDIT.csv`, `N5_INTRALINE_GAP_MODEL.csv` och `N5_RESULTS.json`. Kör `python3 N5_SOURCE_AND_STELLA_REPLAY.py` med Python 3 och Pillow. Scriptet fastslår original R3 Git blob, unika source enemy bitmaps/colours, pixelräknar alla 36 bilder och prövar explicita N3 adversarial gaps. **24-frame-data och Venetian/intraline-kontroller är matematiska source-only-modeller, inte nya 24-frame Stella eller riktiga 6507 timing.** Nya hashkontroller finns i `SHA256SUMS.txt` och paketeringslogg.
