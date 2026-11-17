# THE SKRAUN – KONTROLLERAD MIGRATION MAIN II → MAIN III
**Datum:** 2026-11-17. **Roll:** ny ren permanent huvudchatt MAIN III, inte ny ROM/GRAPHICS/RESEARCH/VERIFICATION-chatt. **Formellt läge:** överlämningsunderlag, inte ny implementation eller fullspels-GO.

## A. Varför migrationen görs
Användaren vill lämna den långa MAIN II-chatten utan att förlora beslut, tekniskt statusläge, arbetsfördelning eller bevis. MAIN III ska kunna ta upp **självständig teknisk projektledning** direkt genom att verifiera aktuella GitHub- och Google Drive-källor, och inte be användaren upprepa tidigare beslut. Den här texten är en indexerad handoff för en ny chatt, inte auktoritet över färskare användarbeslut eller verifierade repoändringar.

## B. Källordning / start
1. Direkta användarbeslut, särskilt senare korrigeringar. Gällande designbeslut på https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md och visuell https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md.
2. Kontrollera live GitHub https://github.com/Odourman/the-skraun, `main`, open drafts, issues, commits, build/Debugger-jobb och faktiska källfiler. Pre-migration main HEAD från kontroll 2026-11-17 var `8e3cc8f2d3f0a93adfd4dc9d72142b58fd8ba10b`; den blir historisk så snart migrationen skrivs.
3. [Projektstatus på GitHub](https://github.com/Odourman/the-skraun/blob/main/docs/PROJECT_STATUS_2026-11-16.md) och [Google Drive aktuellt projektstatusdokument](https://docs.google.com/document/d/1K_89EdAIFPOsftgYI32ULHZG5w_gvzFulMzTp-nqjLo/edit), Drive-mapp https://drive.google.com/drive/folders/1tSipzf7bucrqFOwHBEH61fKvyl0z7D1z.
4. Separata konkreta `handoff/`-arbetsorder och frozen PR-källor styr scope för varje experiment; READ authority vs results vs unapproved proposals.
5. Research (inklusive 30 tricks) är rådgivning, inte tillstånd att ändra canon eller att deklarera ett ROM-PASS. Tester på andra Atari-projekt får inte översättas till Skraun-resultat. Chattminne är aldrig repo-sanning.

## C. Användarens fasta mål
The Skraun: originalkompatibel Atari 2600, snabbt och roligt topdown arkadspel. Världen ovanifrån, Skraun själv upprätt. Exakt samma ljusgrå, hornade, getbensgångande godkända **U1-LEG1 8×12** source A/B på L1/L2/L3, skillnad ENDAST storlek. Båda sidofacings EXAKT horisontellt speglade: FRAMTIDA VISUELL HÖGER använder ursprungliga LEG1 `LEFT`, VISUELL VÄNSTER ursprungliga `RIGHT`. L1 visuellt positivt godkänd på designnivå, inte fullt Stella/Rom-PASS; nivå2 16×24 och nivå3 32×36 är tekniska koncept, 4x bredd/3x höjd på L3 kan förvränga proportioner. #19 L3 översta rasterrad-defekt OPEN. Ingen extra spelerpelskedetalj på högre nivå.

Åtta distinkta fasta arenor / fyra världar (skog 1–2, berg 3–4, dröm 5–6, mörk natt 7–8), **glesa hinder med mycket fri förflyttning även på L3, aldrig fastna när man växer L2→L3**. Alla åtta geometriska DRAFT-utkast är endast design/research, ej kanoniska kartor. K0 ROM-tabellmodell och 1-clock small-step hörnglidning source-only lovande; riktiga kollisioner ej full-godkända i Stella. Två riddare med synligt svärd, en grön flyende bågskytt per arena, en orb, stor guldhalo som passerar hinder; pilar/svärd stoppas av hinder, poäng/liv; läsbart stridsflimmer. L1 svårt, L2 medel, L3 stark/OP, inte klumpig. En mer rymlig layout får inte avskaffa fiender/mekanik/hinder.

## D. Faktisk nyaste källstatus vid 2026-11-17 live-kontroll
**GitHub `main`:** `src/main.asm` fortfarande enkel P01-prototyp, inte färdigt spel och inga integrerade 8 banor/P1-fiender/halomotor. Draft-PR:er omersatta. Återkontrollera HEAD före åtgärd.

**ROM DEVELOPMENT / P01-COL1:** BINDANDE separat avgränsad order https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_ROM_DEV_P01_COL1_ONE_ARENA_COLLISION_DIAGNOSTIC_AUTHORIZED_2026-11-16.md ; issue [#24](https://github.com/Odourman/the-skraun/issues/24) OPEN. **Det finns redan riktig påbörjad kod:** draft [PR #27](https://github.com/Odourman/the-skraun/pull/27), branch `experiment/p01-col1-single-arena-collision-20261117`, kontroll-HEAD `d970c4ccf5fe23123ace5486a37b72825f193fa5`; `experiments/p01_col1_single_arena.asm`, `tests/col1_source_oracle.py`, `tests/col1_cpu_runtime.py`, `.github/workflows/p01-col1-stella.yml`. GitHub [Action run 44073915789](https://github.com/Odourman/the-skraun/actions/runs/44073915789) utfördes 2026-11-17:
- Käll-oracle PASS.
- DASM installerades och assemblerade en riktig **4096-byte NTSC ROM**, list/symbol/sha sparad som CI artifact.
- Kompilerad ROM körd i developer **6502/RIOT/WSYNC CPU-modell: PASS**.
- Autentisk **Stella screenshot/Debugger-art proof INTE PASS**. Jobbsteg FAIL, jobblogg rad: `line 19: pid: unbound variable`. Workflow använder en enkelciterad `bash -c '...'` med kommentar innehållande en apostrof `Stella's own Linux FAQ`; denna sannolika Bash-quote-split är i första hand ett test-automationsfel. Verifiera med direkt shell-/jobblogg innan korrigering, ändra bara arbetsflödet inom gällande P01-COL1 och låt ROM DEVELOPMENT utföra. Första praktiska prioritet; bygg inte duplikat.
- Senaste vanliga `The Skraun CI` på samma commit [run 44073915808](https://github.com/Odourman/the-skraun/actions/runs/44073915808) SUCCESS, men den **ersätter inte** verklig Stella pixel-/rasterverifiering.
- I projekt-Drive-root ligger även flera P01-COL1 source-draft text/ASM/CPU-modellfiler från 2026-11-17. De är INTE automatiskt kanoniska framför GitHub PR#27; jämför exakta bytes och testkedja innan återbruk.

**Renderer-huvudblockeraren P02-R3:** redan verkliga DASM/Stella-diagnoser för original-TIA med same-Y 3 oberoende fiender som roterar 20Hz var, guldhalo/hinder 30/30Hz eller hopslagen PF-färg, statiskt ~2–4 av 76 cykler kvar per värsta rasterrad före pil/orb/AI/collision och 89B P1-buffer; NEGATIVT tekniskt R3 NO-GO för testad arkitektur, inte matematisk omöjlighet för alla alternativ. Inga produktions-B3c/R4 eller extra mapper/ARM beslut.

**RESEARCH PF-REP1 #25:** [issue #25](https://github.com/Odourman/the-skraun/issues/25) OPEN och research-only [PR #26](https://github.com/Odourman/the-skraun/pull/26) unmerged. [research v1 receipt](../docs/MAIN_II_RESEARCH_HANDOFF_V1_RECEIPT_AND_PF_SOURCE_TRIAGE_2026-11-17.md) noterar att uppgivet större sjufilspaket från extern research då INTE verifierats fullt; två research-filer lästes. [PF-REP1](../docs/MAIN_II_PF_REP1_SOURCE_SCREEN_AND_NEXT_DECISION_2026-11-17.md) faktiskt reproducerad source-only 13 X-lägen/88 tvålinjegrupper; Hugg enkel 1 PF-write/2-linjer FAIL för oförändrad R3, selektiva skriver kräver mer bevis. [PF-REP1B](../docs/MAIN_II_PF_REP1B_CONDITIONAL_TIA_WRITE_WINDOWS_2026-11-17.md) villkorad tidsanalys med negativa deadlinefall X80/X84. [PF-REP1C](../docs/MAIN_II_PF_REP1C_RESOURCE_OWNER_AND_VENETIAN_SOURCE_AUDIT_2026-11-17.md) source-only utesluter enkla Ball/Missile-trick och pixel-exakt Venetian. Full verifierad [Drive PF-REP1C ZIP](https://drive.google.com/file/d/1-MN_WleLizpnzK8u_2xaoAAsIgjJIWxM/view) 16690 bytes SHA256 `9b707a24395bb0f0597f1dbf4e5367d767b2a1fa8372003d7f93c1dc8a6959a7`, 7/7 manifest PASS, clean-build 9/9 bytes PASS. INTE ROM/Stella fullrenderer-PASS. #25 OPEN.

**8 arena-DRAFT:** [full source-only report](../docs/MAIN_II_EIGHT_ROOMY_LEVEL3_MAP_DRAFT_REVIEW_AND_STOP_2026-11-16.md), Google Drive [ZIP](https://drive.google.com/file/d/1MePHLlCFKRD07kibk9qoUKmw8Ea9jTQC/view), branch `design/l3-eight-open-arena-drafts-20261116` unmerged. Ännu INTE slutförda riktiga banor.

**K0 kollisionsmodell:** [källrapport](../docs/MAIN_II_COLLISION_K0_RESEARCH_30_TRICKS_AND_NEXT_ROM_GATE_2026-11-16.md), [Drive](https://drive.google.com/file/d/174OGOSl7eHkAqAtB53oFWTTrVlclTcre/view) source-only 24 tabelluppsättningar/384 candidate ROM bytes, 675840 exakta jämförelser, 768864/768864 enhetssteg PASS i source-modell. Samlat 4-unit sweep kunde ge 39348 skillnader mot små steg. Detta betyder INTE 6502 runtime PASS och P01-COL1 #27 är verklig nästa testgrind.

**Grafik och verification:** #15 visuell full-gate OPEN trots godkänt L1 designutseende; #19 ART1 L3 första rad OPEN; #23 nivå3 rörelse/mappar OPEN; #24 COL1 OPEN; #25 PF-REP1 OPEN; #1 oberoende P01 Verification OPEN. R3 bildriktning i separat VFIX har utvecklaregenkontroll, inte overall sprite-canon/PROD PASS.

## E. Roller
**MAIN III:** prioriterar, läser, fastställer tech scope, gör auktorisering och oberoende mottagningsgranskning av developer self-tests utan att kalla den formella Verification. **ROM DEVELOPMENT:** ensam ansvarig för assemblerkällkod, DASM, Stella, Debugger, CI, verkliga ROM-experiment, och egna tester enligt snävt uppdrag. **GRAPHICS:** bara nya separat auktoriserade designbehov, bevara låst U1-LEG1. **RESEARCH:** rådgivande primärkällor, 30 tricks, alternativ/negativa analyser, får inte implementera som Work. **VERIFICATION:** formellt oberoende granskning av färdig FRYST leverans och får aldrig själv fixa koden under granskning. Dokumentera PR/branch/SHA/build/exakta loggar samt Drive-evidens.

## F. Instruktion till MAIN III
1. Börja med live GitHub/Drive-mottagning, verifiera P01-COL1 PR #27 och exakt CI-fel samt P01-COL1 Drive-utkast; PF-REP1 #25, PR #26 och senaste forskning; kontrollera att inga av frågorna har hunnit förändras efter denna snapshot.
2. Skapa en kort MAIN III mottagningsrapport och rättvis PASS/FAIL/NOT TESTED-matris, uppdatera projektstatus i båda systemen efter faktiskt nytt underlag.
3. Få ROM DEVELOPMENT att inom befintlig P01-COL1-order reparera det avgränsade Stella-workflowfelet (efter bevisad rotorsak), utföra riktig Stella och inte duplicera den redan påbörjade 4K-ROM:en. MAIN granskar leveransen.
4. Bevara separat problem med halo/hinder/fiender: #25 research source-only, R3 NO-GO, ingen automatisk R4/B3c. Ge en snäv senare kernel-authorization först efter ett tydligt plan/acceptanskontrakt.
5. Fortsätt självständigt, men bara medan den aktiva chatten faktiskt kör verktyg. Ingen utlovad asynkron vidareutveckling utan automation. Be endast användaren om en betydande olöst prioriteringsfråga eller gameplay/visuell kompromiss. Håll användaren informerad med dokumenterad verklig progress.

## G. Exakt startprompt
Filen [handoff/MAIN_III_STARTPROMPT_2026-11-17.md](MAIN_III_STARTPROMPT_2026-11-17.md) innehåller starttexten att kopiera i en REN NY MAIN III-chatt. Den kan klistras in med kompletterande Drive och GitHub-länkar, men själva den nya konversationen måste skapas av användaren; publicering av dessa filer flyttar inte en ChatGPT-konversation automatiskt.

## H. Om något verkar motsägelsefullt
- Tidigare MAIN II-status nämner P01-COL1 "READY, NOT BUILT" — **supersederas som status av PR#27 och körning 44073915789 där DASM/CPU-modell körts**, utan att den gamla orderns auktorisationsscope ändras.
- "Source-oracle PASS" säger inget om autonomt Stella-PASS.
- "U1-LEG1 visuellt godkänd" avser design/pose L1; ingen automatiskt godkänd L2/L3 eller hel spelscen.
- "24 kartor/kollisionstabeller" är åtta *kandidater* × tre storlekar, inte 24 faktiska färdiga banor.
- PF-REP1-källteoretisk NO-GO har smalt specificerad modell; inget generellt förbud mot hela spelet.
- Titta alltid på nyaste live data, inte på detta dokument som en fryst framtidsprognos.

**Migreringen är ett dokumenterat MAIN-ansvarsskifte, inte beslut om ny kod, merge, full engine eller oberoende Verification.**