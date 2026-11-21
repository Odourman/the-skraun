# THE SKRAUN – MAIN III N6: accepterad riktning för jämförande grafik-/närstridsstudie

**Datum:** 2026-11-21. **Auktoritet:** användarens meddelande "Ja, bra. Följ dina rekommendationer. Det låter bra!" efter MAIN:s åttapunktsgenomgång av melee, färg, orb, halo och skala. **Avgränsning:** N6 source-only designanalys och teknisk prövning. **Ingen ny ROM, ny grafikfil, assemblerändring, cartridgeformat, N7, merge eller independent Verification.**

## 1. Vad som får betraktas som användarbekräftad riktning

1. Pröva den **tekniskt billigaste tydliga halokonturen** i stället för att låsa en rund cirkel: rasterblockjusterad kantig/åttakantig/kvadratisk mot original. Logisk 360° attack, genomträngning av hinder, tre level-steg och cirka 0,5 s aktiv tid kvarstår. Ingen form är redan vald som slutgiltig.
2. **Tre fiender samtidigt** – två riddare och en miljökamouflerad ranger – **bevaras** under N6:s första lösningsförsök. R3 20Hz same-Y är ett negativt *arkitekturprov*, inte ett generellt bevis för att tre fiender är omöjliga. Ingen speländring till en riddare auktoriserad.
3. **Ljusblå riddarrustning är den nya föredragna färgriktningen**, i stället för två röda shades eller tidigare föreslagen gemensam röd. Använd exakt samma ljusblå TIA färgbyte för båda som testkandidat, jämför kontrast mot ljusgrå Skraun, världens bakgrund, hinder, natt och ranger; exakt NTSC-kod och PAL-översättning ej låsta. En och samma ljusblå färg för två riddare har samma COLUP1-switchkostnad som en och samma röd färg. 
4. **Svärden ska primärt testas som del av själva riddarens P1-grafik**: STILL/varningspose med höjt svärd/aktiv slagpose/återhämtning. Software-hitbox beräknas separat; svärd stoppas av hinder, skada endast under aktivt huggfönster och attackriktning låst vid varningsstart. Minst cirka 0,4 s läsbar varning. **M1 som kompletterande synlig svärdslinje** är ett reservspår när 8-bitars P1-silhuetten inte räcker, inte ett gratis andra player-objekt.
5. **Orb:** liten och enkel Ball-kandidat, får världens PF-färg i HALO-OFF och guld i HALO-ON, med valfri avsiktlig blink-/puls-effekt endast om den behåller synlighet och detta ger vettig faktisk renderer-/kontrastbudget. Från början synlig, nåbar och kvarliggande efter L3 enligt spelets regler.
6. **Miljö:** håll PF-hinderformer enklare och banor öppna, utan att överge åtta distinkta banor; drömspiraler är statiska.
7. **Skrauns storlek:** godkänd original U1-LEG1 8x12 A/B för L1 ändras inte utan särskilt konstbeslut. Jämför fysikaliska visningshöjder L2/L3: originalplan L1 8x12, L2 16x24, L3 32x36 kontra kandidat L1 8x12, L2 16x20, L3 32x30 med olika replikering av samma 12 source-rader. Detta är **endast kandidattest**, inte godkänt ändrat spelmått eller ändrade konstpixlar.
8. **Valt N6 färgexperiment B:** PF hinder har världsfärg under halo-OFF, hela arena-PF blir guld vid halo-ON; jämför historisk A (två olika samtidiga PF-färger) och enklare C (en färg alla lägen). Orb delar PF/BL COLUPF. Ingen slutförd 76-cykelkernel är visad.

## 2. N6 prövningsordning med lägst intrång först

| Etapp | Kandidater | En verifierbar source-only output | Negativ/stopp-villkor |
|---|---|---|---|
| T1 PF och halo | A/B/C med alla 13 R3-X, exakt samma ursprungliga spelmasker; kantig/stepped/kvadratisk mask som jämförelse först efter verklig källmaskgenerering | Per fysisk radar, PF0/PF1/PF2 byte-delta 0..6, COLUPF events, antal verkliga täckta källceller, klock-deadlines X80/84 och gräns X56/104 | Ingen ny enkel form får sägas vara billigare för att den har färre hörn. Förkastad om verklig beamdeadline eller attackläsbarhet kräver omöjlig färg-/bildsekvens |
| T2 P1 och svärd | Två identiskt ljusblå riddare med P1-integrerad svärdspose, världskamo Ranger, tre fria X/Y, alternativa local 2/3-way Venetian och tillfälligt P0-lån | Minst källa/positioneringshändelser för P1/GRP1/RESP1/HMOVE och färg; 12-/24-frame läsbarhetskrav, aktiv 8-bitars grafikbredd/varning; P0 ska bevaras i S3 | STOP för koncept som bara ger tre via fasta NUSIZ-kopior eller R3 20Hz helframeblink; svärd får inte reduceras till oförståelig pose |
| T3 reservsvärd M1 | Jämför S1 P1 in-sprite mot M1 kort separat linje när P1 bredd inte räcker | ENAM1/RESM1/NUSIZ1/COLUP1 schema samt samtidiga 2 Knight svärdsvillkor | Inget påstående att M1 kan rita två oberoende svärd/egen färg utan ytterligare ägarplan |
| T4 P0 scale | Godkänd 8x12 U1 källa, kända 16x24/32x36 kontra visningsförslag 16x20/32x30 | Fysisk maskjämförelse och antal P0-Y-overlap rader på S0–S9, bibehållen källinformation, horisontell x1/x2/x4 med L3 rörlighet | Inga nya proportioner permanent utan användarens visuella val. Minskad P0-höjd löser inte 3 same-Y P1 automatiskt |
| T5 BL orb & map | Enkelt BL world OFF/gold ON, PF-hinder i åtta tänkta open maps; stilla spiral | Under OFF/ON BL synlighets- och raster-HUE-fall, hårdvaruobjektens gemensamma registerägarbok | Ingen förlorad orb vid L3 eller försvinnande på nattbakgrund; inga färgbyten som överskrider COLUPF-deadlines |
| T6 EN gemensam N6-C | T1+T2+T3+T4+T5 på N3 S0–S9, minst två verkligt olika kernels | Per-rad COLU/GRP/PF/BL/Mx/RESP/HMOVE händelse och 76 CPU cycles, 128B RIOT inkl stack, VBLANK/Overscan, ROM; konkret första motexempel om fail | Inga isolerade microtest blir fullscene-GO; om blockering kvarstår, erbjud **specifik** grafisk/gameplaykompromiss, inte tyst sänkning av fiendeantal |

## 3. Hårdvarufakta och tidigare observerad status att inte misstolka

- TIA har P0/P1 som två oberoende player-objekt; M0 delar COLUP0, M1 delar COLUP1, BL delar COLUPF med PF. Ingen extra färg uppstår av att välja en blå nyans framför röd.
- R3 faktiskt observerad three-same-Y 20Hz per fiende var FAIL under dess **testade** schema. Source-only N6 visar att framtida 3-way Venetian kan bevara 6/5/5 av åtta källrader vid dubbel-höjd (inte alla tre fullt renderade) men visar **inte** en positionerings- och färg-korrekt fysisk kernel.
- N6 B-on tidigare källberäknad 4 400 minsta PF-byteändringar över 13 X×176 R3-radfall, 419 svåra fall med sex förändringar. Även enfärgad PF ger inte en ny sprite eller garanterade CPU-cykler.
- Källprov och designutvärdering får fortsätta under N6. En **ny ROM, DASM/Stella-implementation eller N7** kräver specifik separat order. **Verification ska vara oberoende** av ROM DEVELOPMENT.

## 4. Beviskällor

- [Användarens punktvisa preferenser och tekniska meleekällor](MAIN_III_N6_USER_FEEDBACK_MELEE_SWORD_REFERENCE_AND_CREATIVE_TEST_MATRIX_2026-11-21.md)
- [N6 integrerat färg-/objektkontrakt](MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md)
- [N6 source-model color B och prioriterade creative fallbacks](MAIN_III_N6_B_GOLD_PLAYFIELD_CREATIVE_REVIEW_2026-11-21.md)
- [Bindande designbeslut 01–60](DESIGN_DECISIONS_01-60_2026-11-16.md)
- [Godkänd U1-LEG1 figur](SKRAUN_VISUAL_DIRECTION_2026-11-16.md)
- [Worst-scene S0–S9](MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md)
- [N5 P1 same-Y autentiska negativbevis](MAIN_III_N5_P1_SAME_Y_FEASIBILITY_AND_GAME_DECISION_2026-11-17.md)
