# THE SKRAUN – MAIN:s beslut efter GRAPHICS v0.3 (2026-11-16)

**Typ:** Avslutad grafikgranskning och bindande statusbeslut, **inte** ny implementation.  
**Resultat:** v0.3:s grafiska arbetsleverans är **mottagen och accepterad som reproducerbara källkandidater**. Ingen spelarsprite, fiendesprite, världslayout eller spelattack är slutgodkänd för produktions-ROM. Uttryckligt beslut: **NO-GO för att låsa 8×12-Skraun som slutlig fyrbent topdown-identitet nu.**  
**Inget nytt GRAPHICS v0.4, R4, B3c, ROM-step, mapper-byte eller oberoende VERIFICATION är auktoriserat i detta beslut.**

## 1. Kontroll av exakt leverans och källor

- Original ZIP i projektets visuella Google Drive-mapp: https://drive.google.com/file/d/1-nlqRBYSmFJG0xRm90DpDBFYud7tgCPh/view
- Namn: `THE_SKRAUN_GRAPHICS_V0_3_2026-11-16.zip`. Hämtat och kontrollerat av MAIN, **386 046 byte**, **27 arkivposter**, `ZipFile.testzip()=None`, **26/26 poster i SHA256SUMS.txt matchar**, lokal `verify_graphics_v03.py` **PASS**. Beräknad extern ZIP SHA256: `e74757e9877d7f7ea6837721a30633b0d224c13ac4ff189d1fb12aca6a797e26` (= GRAPHICS uppgivet).
- Publicerade textkällor: https://github.com/Odourman/the-skraun/tree/graphics/skraun-v0-3-final-readability-20261116/graphics/skraun_v0_3 ; kontrollerad gren-HEAD `a98764192e352711370239727775701f8d8336c9`.
- MAIN har visuellt granskat **original-PNG:er**, animationsdata, bitmappar i `SKRAUN_V03.json`, `ENEMIES_V03.json`, `WORLDS_V03.json`, `HALO_V03.json`, `ART_METRICS_V03.json`, `MAIN_DECISION_V03.md` och användarens privata originalteckning.
- Styrande källor: `docs/DESIGN_DECISIONS_01-60_2026-11-16.md`, `docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md`, föregående [MAIN v0.3-scope](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_V0_3_OVERHEAD_READABILITY_FINAL_DESIGN_GATE_2026-11-16.md). Det ursprungliga privata teckningsfotot har inte publicerats av MAIN.

### Bevisnivåer
Detta är **källdata-, ZIP-, bild- och estetisk granskning**. Allt i v0.3 är **designmockup**, INTE DASM-byggda Atari-ROM-skärmbilder, CRT-observationer, produktionssprites eller oberoende VERIFICATION. Den tidigare R3:s hårdvaru-NO-GO påverkas inte av grön bitmapvalidering.

## 2. MAIN:s estetiska beslut

### Skraun – Q1 endast provisorisk testreferens, INTE final
- Q1 (`Q1_splayed_quad`) är tydligast av de nyproducerade **8×12-kandidaterna**. A/B skiljer **10 pixelceller**, inklusive främre och bakre lemrader. Q2 (`Q2_long_back`) skiljer **12 celler** men saknar tydlig fyrbent identitet i litet format. Speglade vänster/höger-källrader är korrekta, huvud-logik överst, bakben nederst. 
- Efter granskning av de autentiska 8×12-tavlorna är **huvudfelet inte i första hand otillräckliga två rader**: samma frontalansikte med två ögon, horisontella armrader och två nedre ben gör karaktären visuellt humanoid. Användarens originalteckning har en frontalt läsbar anatomi; **den bindande spelkameran är rakt ovanifrån**. Varken Q1, Q2 eller det separata 8×14-tankeexperimentet löser denna spänning på ett estetiskt övertygande sätt i de levererade förhandsvisningarna.
- **Ingen slutlig acceptans** av Q1, Q2 eller 8×14. Q1 kan användas som *explicit märkt placeholder i en senare separat auktoriserad ROM-konstdiagnostik*, aldrig som ett färdigt grafiskt designbeslut.
- **Ingen automatisk utökning till 8×14.** +2/+4/+6 skannlinjer på nivå1/2/3 och eventuellt ökad RAM-/ROM- och timingbelastning behöver kvantifieras separat om MAIN senare väljer att pröva ett nytt format. 8×14-förslaget har ännu inte tillräcklig estetisk nytta för att motivera den förändringen.
- Detta är **NO-GO för nuvarande grafikvarianter**, inte en matematisk omöjlighetsförklaring för alla möjliga 8×12-silhuetter. En framtida revidering bör i första hand utgå från en genuint *uppifrånläst rygg/kropp + fyra sidoankrade tassar* och minska frontansiktets grafiska dominans, med originalteckningens kännetecken bevarade. Ändring i fastställd visuell identitet, body axis eller kamera kräver ett nytt tydligt MAIN-beslut, inte automatisk GRAPHICS v0.4.

### Fiender – förbättrade animationer som arbetskandidater
- `knight_idle`→`knight_warning` **12 pixelcellsbyten** (mot v0.2:s 4). `archer_idle`→`archer_draw` **11 byten** (mot 2). Skillnaden är synligare i full bitmap och GIF, och den gröna bågskytten skiljer sig från riddaren.
- Ingen av dem är ännu **slutligt godkänd som igenkännbar svärdsriddare/bågskytt ovanifrån vid TV-storlek i faktisk rörelse**. Bågens och svärdets visuella förvarning måste bedömas med verklig färg och eventuell multiplex/flicker. Antal ändrade pixlar är inte ett kvalitetsmått i sig.

### Världarna – tematisk riktning accepterad som designreferens
- **Skog:** större krona/stubbar. **Berg:** stegade klippor. **Dröm:** öppna brutna spiraler/ruiner. **Natt:** skadade murar/tinnar. Två 40×24 speglade PF-layoutkandidater per värld, där formerna syns tydligare i *de verkliga monokroma montagen* än i v0.2.
- MAIN **behåller dessa fyra formspråk som lovande designriktning**. Exakta åtta PF-kartor, RGB-färger, kollisionskartor och TIA-register är INTE slutgodkända och inte funktionstestade tillsammans med spelobjekten.

### Guldhalo – formkoncept väljs, inte attackgeometri
- Nya separata familjen: nivå1 **40cc ×64 linjer** ratio 1,000; nivå2 **56cc ×80 linjer** ratio 1,120; nivå3 **72cc ×112 linjer** ratio 1,029 för den angivna approximerade 4:3-modellen `1 cc≈1.6 scanlinehögheter`.
- **MAIN väljer denna familj som VISUELL PROPORTIONSREFERENS** framför tidigare för hög nivå3 `88×176` och tidigare för breda alternativ. Alla tre är inom överenskomna ±15 % och ser mer runda ut i korrekt likformigt förhandsvisad TV-modell.
- **Inte** slutligt godkänd spelfunktion/räckvidd, tidslängd, kollisionsradie, playfield-implementation eller kompatibilitet med färgade hinder. Simulerad nivå3-kantklippning: ca **40,32 %** vid sidokanter och **41,94 %** vid övre/nedre kant för testade centrumpositioner – tydligt öppet visuellt problem.

## 3. Hårdvaru- och projektgrind

R3:s tidigare negativa tekniska genomförbarhetsbedömning gäller fortfarande: vid tre fiender på samma vertikala nivå cirka **20Hz per fiende** vid sekventiell delning av P1, halo mot hinder cirka **30/30Hz** eller gemensam PF-färg, och värsta vägar **2–4 statiskt beräknade lediga CPU-cykler** innan full pil/orb/HUD. V0.3:s bilder löser inte TIA-resurser, 128 RAM-byte, CPU, färg- och flickerbehov.

**MAIN:s aktuella sekvens:**
1. **Avsluta och frys v0.3** som reproducerbart grafikunderlag. GRAPHICS stannar enligt sin tidigare order. Issue #15 **förblir öppen** för slutligt visuellt godkännande.
2. **Ingen ny v0.4 eller ny design-loop på samma anatomiska tolkning.** Inte heller automatiskt 8×14. Det krävs först ett medvetet grafiskt vägval om hur originalteckningens frontala kännetecken ska uttryckas i äkta topdown-pixlar, och om en första nivå1 kan vara mer stiliserad.
3. När riktningen valts kan MAIN **separat auktorisera** ett mycket smalt Stella-sprite-test med 1 spelarsprite och 1 fiende i taget/1 motiv per värld, för **läsbarhet och visuell acceptans**. Detta är inte lösningen på R3:s fullspelsarkitektur och får inte självstartas.
4. Den stora **renderer-/hårdvaruavvägningen** med tre fiender, pil/orb och självständig halo/scen måste senare tas som ett eget MAIN-beslut. Varken större ROM/bankswitching eller grafiska mockups tillför automatiskt TIA-sprites eller 6507-cykler.

**Ej auktoriserat:** någon ny R4, B3c, AI, ROM-sammanslagning, permanent spriteformat-/designändring, 8×14-kernel, `main`-merge av grafikgrenen, eller oberoende VERIFICATION. Nästa stora beslut kvar hos MAIN/användaren.
