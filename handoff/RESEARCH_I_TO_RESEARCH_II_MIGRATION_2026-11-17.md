# THE SKRAUN - RESEARCH I -> RESEARCH II: kontrollerad migration
Datum: 2026-11-17
Klassning: RESEARCH/HANDOFF, RADGIVANDE. Inte designcanon, ROM-order, verifiering eller merge-auktorisation.

## Syfte
Den tidigare researchchattens uppdrag, bevis och arbetsgränser ska vara fullt återhämtningsbara för en ny, ren och självgående RESEARCH II-chatt. Detta dokument dokumenterar inte ett byte av MAIN eller någon godkänd ny fullspelsarkitektur. Ny chatt ska aldrig anta att dess minne innehåller senaste projektstatus.

## Roller och ansvar
- Användaren fastställer slutliga spel- och visuella beslut.
- MAIN II leder projektet, prioriterar och ger separat avgränsad ROM-/grafikauktorisation.
- ROM DEVELOPMENT gör riktig DASM/6507/TIA-kod och sina egna Stella-kontroller inom existerande scope.
- VERIFICATION granskar oberoende en tillräckligt fryst leverans när MAIN beställer den.
- RESEARCH II söker, analyserar, förklarar, prövar källbaserade hypoteser och levererar rådgivande handoff. Får inte ändra spelkod, sprites eller fastställda spelregler, starta R4/B3c eller själv utropa oberoende PASS.

## Källauktoritet
1. Ny uttrycklig användarinstruktion och bekräftade designval.
2. Senaste relevanta MAIN-beslut/aktuell Project Status på GitHub main och dess verkliga handoffs, inklusive bindande scope och stoppvillkor.
3. Aktuell originalkod, frysta artefakter, verklig Stella-/DASM-evidens, Issues/PR; skillnad mellan en gren och main är viktig.
4. Google Drive originalpaket och historiska handoffs som evidens.
5. Tidigare RESEARCH v1 är rådgivande jämförelsematerial, aldrig en överordnad eller aktuell implementeringsauktoritet.

Källor att börja med:
- Repo: https://github.com/Odourman/the-skraun
- Design: https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md
- Visuell riktning: https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md
- Status: https://github.com/Odourman/the-skraun/blob/main/docs/PROJECT_STATUS_2026-11-16.md
- PF-REP1C senast kontrollerat: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_SOURCE_AUDIT_2026-11-17.md
- PF-REP1 ärende: https://github.com/Odourman/the-skraun/issues/25
- PF-REP1 research-PR: https://github.com/Odourman/the-skraun/pull/26
- Kollision P01-COL1: https://github.com/Odourman/the-skraun/issues/24 och https://github.com/Odourman/the-skraun/pull/27
- R3 NO-GO: https://github.com/Odourman/the-skraun/blob/experiment/romdev-r3-decisive-scene-scheduler/docs/ROMDEV_P02_R3_DECISIVE_SCENE_SCHEDULER_MAIN_HANDOFF_2026-11-16.md
- K0: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_COLLISION_K0_RESEARCH_30_TRICKS_AND_NEXT_ROM_GATE_2026-11-16.md
- Research v1 arkiv hos Drive: https://drive.google.com/file/d/1k1AExfpgNrFFr_c3py3LYK4Byw6adQnS/view?usp=drivesdk
- Research-migrationsmapp i Drive: https://drive.google.com/drive/folders/1gK6qVyiE-g4uK1DbxQiFGD9LGfhTsMFx

## Fryst överlämningsstatus vid läsning 2026-11-17
- Det godkända källutseendet för Skraun är U1-LEG1, upprätt hornat ljusgrått troll med två A/B-poser och tidigare korrigerad semantisk visuell höger/vänster. Samma pixelgrundmask används för nivå 1/2/3. Åtta banor i fyra världar, två samtidiga riddare och grön bågskytt, orb, pil, 360-graders guldhalo som passerar solida hinder; level 3 måste vara kraftfullt och lättstyrt i rymliga arenor. Detta får inte förenklas i smyg.
- R3 same-Y-tre-fiender uppmättes till 20 Hz per fiende; PF halo/hinder gav 30/30 Hz växling eller samma färg; kritiska linjer hade 2-4 statiskt beräknade cykler kvar av 76. Nästan hela specifika RAM-layouten upptagen. Pil/orb/full AI/kollision/HUD ej integrerade. R3 NO-GO gäller testad arkitektur, inte all möjlig Atari 2600-kod.
- Research v1 levererade avhandling, 30-trickmatris, källregister, kodstudier och söklogg. Förstahandshypotes: specialiserade multikernels + selektiva PF-registeruppdateringar. Inte bevisad eller godkänd motor.
- MAIN har redan bedömt föreslagen enkel Hugg one-register-per-two-line-substitution mot R3:s verkliga mask och funnit att den INTE kan återge exakta masker. PF-REP1 fortsatte.
- PF-REP1C (source-only) avvisar enkel Missile/Ball-färgplaneomfördelning, enkel NUSIZ-kopiering och naiv Venetian som exakt scene-resurslösning under testade villkor. Det betyder inte att alla specialkernels, tidsbestämda horisontella färgbyten eller nya algoritmer är motbevisade. Ärende #25 fortsatt öppet vid kontroll.
- PF-REP1B rapporterade 5-cykelkonflikter i villkorad färg-/PF-schemaläggning på X80/X84 vid givna deadlines. Detta var analytisk källa, inte riktig kernel/ROM.
- P01-COL1 (#24) är redan separat auktoriserad. PR #27 är draft med source-oracle tester, inte bevis på färdig byggd och Stella-granskad ROM. Det får inte dupliceras av RESEARCH II.
- Öppna kvalitetsgrindar vid kontroll: #1 P01 oberoende, #15 visuell, #19 ART1 level3 första felrad, #23 L3 navigation, #24 kollision och #25 PF-REP1. Fånga ALLTID senare status direkt.
- PR #26 och #27 är draft, omergade vid kontroll. Inga forskningsrekommendationer får ensamma starta implementation, merge eller oberoende Verification.

## Återstående egentliga researchfråga
Identifiera nya, faktiska, tekniskt falsifierbara sätt att samtidigt göra:
P0 U1-LEG1 i alla tre storlekar; två riddare och en grön bågskytt vid oberoende X och samma Y, läsbar attackförvarning; 360-graders tydligt gul halo och tydligt separat solida hinder i SAMMA fysiska frames; pil, orb och HUD med ägarskap P0/P1/M0/M1/BL/PF, ROM/RAM/stack och riktiga CPU-deadlines samt VBLANK/overscan-spellogik.

Prioritera återstående evidensluckor efter PF-REP1C: full physical TIA write-deadline med horisontell färgseparation; ompositionering av P1/same-Y via tidsstyrda grafiska skrivningar utan att förstöra fixed U1-LEG1 och PF; verklig generell kontra specialiserad kernel; alternativ till blandad PF-resurs som inte tyst ändrar halo-funktion. Sök primärkod och bevis för faktiska spel, andra språk och dokumenterade negativa fall. Inga generiska 30-tricklistor som substitut för register-/cykel-/RAM-bevis.

## Vad den nya chatten ska göra först
1. Kontrollera fungerande anslutningar till GitHub/Drive, läs de styrande live-källorna och PR/Issue-status. Redovisa kort status och om något i denna snapshot har ändrats.
2. Läs hela v1-forskningspaketet i Drive, inklusive dess fem researchfiler och manifestet i ZIP. Bekräfta vilka delar som var historiskt underlag och vilka hypoteser senare PF-REP1B/C redan har motsagt.
3. Läs PF-REP1C:s faktiska källpaket, källfilerna bakom det och återstående falsifierbara register-/färgfrågor.
4. Fortsätt självständig teknisk forskning och leverera EN uppdaterad, reproducerbar, källgraderad RESEARCH II-rekommendation till MAIN, med exakt pass/fail-kriterium och minsta nya uppdrag som MAIN KAN besluta om. Ingen ny ROM förrän separat uttrycklig order.
5. Använd tydlig evidensklass på varje centralt påstående: historiskt dokumenterat, direkt observerat i Skraun-ROM, source-only härlett, beräknad uppskattning, otestad hypotes, eller motsagt av faktiskt resultat.

## Verifierings- och publiceringsdisciplin
- Rapportera aldrig emulatorbyggd men okontrollerad ROM som Stella PASS.
- Ange exakt branch/commit, källversion, SHA-256 för levererade artefakter och villkor för tester.
- Sökverktyg/Drive/GitHub-plugins används när de fungerar. Läs verkliga filer och nämn konkret om åtkomst saknas.
- Om projektet ändras senare är denna migrationsrapport en HISTORISK SNAPSHOT. Senare auktoritativ status vinner.
- Slutrapport till MAIN ska visa vad vi vet, vad som motsagts, bästa återstående vägar, worst-case-kostnad, samt tydliga stoppvillkor. RESEARCH II beslutar inte själv att gå vidare till implementation.

## Startprompt för ny chat
Se separat fil i denna branch: handoff/NEW_RESEARCH_CHAT_STARTPROMPT_2026-11-17.md.
