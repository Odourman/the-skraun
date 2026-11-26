# Beslutade utvecklarval

| Val | Inlagt i ROM | Alternativ eller reserv |
| --- | --- | --- |
| R01 Halo | Fyra M0-faser med ordinarie P0-mask, BL-orb och separat M1. 48 styrda logiska gränsfall. | PR65:s markörer behölls som godkänd bas. Full diagonal skärmgeometri och fler fysiska segment har egen kvarvarande risk. |
| R02 Kompakt storlek | 8×12 / 16×20 / 32×30. Samma tolv källrader, 40 färre sprite-tabellbyte. Förskjutning och kollisionshöjd är 6/10/15. | PR65 16×24/32×36 kvar som separat byggbar fallback. Maskprovet hittade lika många exakta bilder för båda versionerna. |
| R03 Schemaläggning | Cykla när två riddare delar högsta hotgrad, behåll prioritering för ensamt hot och statiskt kvalificerad NUSIZ-kopia. | PR65:s särskilda dubbelfas. I samma 24-bildersfixtur gav PR65 antal/längsta lucka 8/3, 7/3, 9/2. Produktionen jämförs i MEASUREMENTS.json. |
| R04 Poäng/liv | BCD-display mättas vid 9 999, extraliv fortsätter utifrån faktiskt intjänade poäng och tak vid nio. Överskjutande bonus vid fullt livstak kvitteras direkt. | Sex siffror skulle kräva nytt HUD-utrymme. Ingen rullande poäng. |
| R05 HUD | Ljus konstant kontrast över alla färgpaletter. Miljöfärg återställs före arena. PR65:s vänsterfält med fem rader behållet. | En högre font inom samma rasterbudget är ej kvalificerad. Svart förlust med ensam poäng behåller läget. |
| R06 Ljud | Två TIA-röster, 15 ID, envelope, pitch och längd per ID, tvåpulsvarning, tretonig banjingle. | Tidigare enhetlig 12-bilders längd. Styrd PCM visar isolerade och samtidiga händelser samt tystnad. Mänsklig mixgranskning återstår. |
| Fast pilvektor | Heltalsackumulator sparar huvudaxel/lutning vid avfyrning. Konservativt hindertest vid både sikte och släpp. | PR65:s ±1/0/1-beroende 45-gradersväg. Exakt fri diagonal runt varje hinder kräver mer arbete. |
| Livsförlust | Högbiten i osårbarhetsvärdet markerar återplacering i nästa overscan. Bara överlevare flyttas. | Tidigare återställd spelare med kvarstående fiender intill spawn. |

## Resurser

- Mapper standard F6, fyra fysiska banker på exakt 4 096 byte. DASM-listningar visar ORG, fasta banktrampoliner och hotspot-/vektorgränser. PF1 768 byte och visuella områdestabeller är frysta.
- Inga nya fysiska RIOT-byte. `$A1/$A2/$B2` är projektilens huvudaxel, biaxel och felackumulator. `$EB` är bankbrevlåda före aktörsanrop och projektilscratch efter återkomst. `$B3` är osårbarhet/återplaceringsflagga. `$BF/$85` är ljudköer, `$EE/$EF` rösttillstånd. Ingen röstdel får antas leva kvar efter initiering som skriver aktörs-RAM.
- VBLANK-, synlig- och overscan-markörer, WSYNC, GRP0/1, COLUPx, PF-latch och positionsspår ligger i EVIDENCE. Loggarna ger raster och lokal beamfas. Exakta jämförbara CPU-max/medel på alla bankvägar är UNKNOWN. Global stack- och beamvärstagräns är UNKNOWN.
- Spelvideo är autentisk Stella 7.0. Tidigare Live SDL-video räknade presentationsramar medan tangentinput ibland inte nådde spelet. Libretro fångar bild/ljud och spelar joystickmanus på samma emulatorsteg. Rått planeringsprov i Stella 6.7.1 och oberoende binär-identitet mellan emulatorer framgår i bevisen.

## Kvarvarande användarbeslut

Inget nytt användarbeslut krävs för de implementerade slutvalen. Full produktkvalificering har tekniska och praktiska öppna punkter enligt MAIN_HANDOFF.
