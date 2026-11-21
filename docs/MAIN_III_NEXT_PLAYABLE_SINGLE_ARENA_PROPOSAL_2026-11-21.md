# THE SKRAUN – MAIN III: nästa snabbaste väg till en faktiskt spelbar enarenaprototyp

**Datum:** 2026-11-21. **Klass:** MAIN:s faktagranskade ARBETSFÖRSLAG, inte ROM-auktorisation och INTE start på N8, N9 eller någon ny cutover family. **Syfte:** prioritera närmsta spelbara upplevelse, minska återkommande diagnos-/verifieringsloopar.

## 1. Bunden sanningskedja

- [Live MAIN-state](CURRENT_MAIN_STATE_2026-11-17.md): användaren har uttryckligen prioriterat snabb, modig spelbar utveckling och selektiv riskbaserad verifiering.
- [P01-COL1 verklig ROM-rapport](MAIN_II_P01_COL1_REAL_ROM_COLLISION_DIAGNOSTIC_RECEIPT_2026-11-17.md), [MAIN III konservativ CPU/RAM-review](MAIN_III_P01_COL1_N2_WORST_CASE_CPU_RIOT_STACK_AUDIT_2026-11-17.md), [PR #27](https://github.com/Odourman/the-skraun/pull/27), [Issue #24](https://github.com/Odourman/the-skraun/issues/24). Fryst 4,096B ROM SHA256 `f36217f9ae96a1e927795ca639b9d6b6cca68ad3e8e4f296afadcdb52d6a6ad2`, experimentgren `experiment/p01-col1-single-arena-collision-20261117`. Verkliga Stella-bilder stöder P0 U1-LEG1 A/B, tre visningsstorlekar, en syntetisk öppen arena och rörelseeffekter. Kollisionsrutin har exakta kompilatormodelltester, och MAIN:s konservativa käll-cykelberäkning visar max 60 cykler aktiva synliga COL1 kernel-instruktioner + WSYNC, men en fullständig actual-Stella gameplay/AI profilerad kernel är EJ bevisad.
- [N7/F2b MAIN negativ-granskning](MAIN_III_N7_F2B_DEVELOPER_DELIVERY_REVIEW_2026-11-21.md), [Issue #31](https://github.com/Odourman/the-skraun/issues/31), [draft PR #32](https://github.com/Odourman/the-skraun/pull/32): två specifika tre-P1-S2 retrigger-varianter FAIL som källkorrekt same-Y rendering. Detta falsifierar INTE alla 3-fiender-lösningar och är INTE grund att skriva om spelbesluten.
- [Issue #33](https://github.com/Odourman/the-skraun/issues/33): EN separat read-only independent Verification är auktoriserad, inga leveranskommentarer på issue vid ny MAIN-kontroll. Detta får inte bli en serie nya verifieringsloopar.
- [N6 B och spelcanon](MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md), [designbeslut 01–60](DESIGN_DECISIONS_01-60_2026-11-16.md), [L3-rörlighetsgrind #23](https://github.com/Odourman/the-skraun/issues/23).

## 2. MAIN:s val av NÄSTA MENINGSFULLA prototypinriktning

**Bevara en ensam spelbar arena och bygg en sammanhängande minimal loop på den redan fungerande COL1-rörelsekärnan.** Det här ska ge verklig joystickrespons och något som känns som att spela, i stället för ännu en PF-/P1-kerneldiagnos.

**Rekommenderat MINIMALT nästa implementeringsscope, ENDAST efter ny, uttrycklig separat auktorisation:**
1. **Återanvänd COL1 P0-, frusen U1-LEG1 A/B-, kollision- och 8-vägsrörelse** i en NY separat experimentgren baserad på identifierad, bytefäst COL1-bas, utan att mergea PR #27 eller #32 i main.
2. En enda SYNTHETISK öppen träningsarena, högst de befintliga få hindren. Ingen kanonisering av åtta färdiga banor. Verifiera kroppslig fri rörelse även när Skraun når L3, med marginal för realistisk kollisionskropp och utan väggfällor.
3. En **liten aktiv orb**, helst BL, synlig från start. Plockas upp genom verklig kollisionskontroll, ökar level L1→L2→L3 om rörelseutrymme finns. Bort med reliance på COL1:s debug-SELECT som "spelmässig" nivåökning, men separat dokumenterade debuginjektioner kan finnas för testreproduktion.
4. **FIRE aktiverar logisk 360° halo i cirka 30 NTSC-frames** och låter P0 röra sig under spell. L1 1s/ L2 .6s/ L3 .25s cooldown-kandidater enligt canon, gradvis större radie och tjockare ring, utan krav att låsa slutliga radievärden eller att den ska vara perfekt rund. **B färgtest:** ringmask OR hindermask som guld-PF under ON; OFF världsfärg PF. OR-ringen ska ha verkligt urskiljbar räckvidd; ENBART att färga alla befintliga hinder guld är inte ett synligt halo-prov.
5. **Ett stillastående måltavleobjekt** – använder befintlig R3-knight bitmap på P1 och preliminär ljusblå färg – som kan träffas av halons logiska radie och ge ett tydligt ljud/färg/poängliknande feedback. Det är en **TEKNISK SPELBARHETSDUMMY**, inte en ersättning för de två riddarna + Ranger, ingen AI eller svärdsattack påstås. Inga nya spritepixelmasker och inga tysta gameplaybegränsningar.
6. Bygg först en 4KiB normal NTSC ROM; om kod-/RAM-budget inte ryms eller TIA timing/beam deadlines faller, rapportera det exakt och STOPPA i stället för implicit mapperbyte, osynlig förlust av rörelse/halo/objekt eller överdrivna verifieringsloopar.

**Varför detta:** COL1 har redan P0-movement/Scale/solid proof; ett lokalt, fokuserat P1 *en aktör*-test är billigare än tre-fritt-X-same-Y och ger ändå ett första gameplay-kretslopp (rör dig → ta orb → attackera → träffa). Den fulla 3-fiender-kernel-frågan och huvudattackens konsekvenser kvarstår som ÖPPNA separata tekniska acceptansgrindar.

## 3. Vad MAIN ska kräva av en enda framtida developer-leverans

- Körbar ROM, ASM, separat tydlig branch/commit, DASM build-logg, SHA för kod/binär, PLA YTEST-instruktioner och minst en uppmätt Stella-capture av rörelse, orb-interaktion, halo aktiv/inaktiv och synligt målträff.
- Faktiska 6507/TIA scanline-/cycle-mått för angränsande P0/P1/PF/BL-rader, 262 NTSC-rad framing, RIOT/stack och tydlig FÖRSTA missade deadline om FAIL. Göm inte eventuella tvåfärgs-PF eller P0-sprite-artefakter.
- En snabb praktisk spelbarhetsbedömning: L3 kan röra sig utan att fastna på fyra hinder, halon rör sig med Skraun och dess nivåökning blir tydlig, ett mål kan besegras med FIRE.
- Bara **DEVELOPER_OBSERVED + MAIN_REVIEWED** krävs för ett preliminärt litet designbeslut; separat VERIFICATION endast om ett avgörande nytt och tvistigt påstående faktiskt uppkommer. Ändra inte Issue #33:s redan frysta uppdrag.
- Ingen fullscene-PASS och ingen godkänd slutlig spelbalans från denna micro-playtest. Fortsatt tredjefiender-krav, riktig riddarnärstrid, världskamouflerad Ranger, hela åttabanorsspelet, HUD och ljud återstår.

## 4. Auktorisation och STOP

Denna MAIN-review **väljer en rekommenderad riktning**. Den återskapar **inte** en N7-order och startar **inte N8/N9, ROM DEVELOPMENT, ny grafikproduktion, mapperbyte, main merge eller nya Verification-serier**. Nästa faktisk ROM-kodorder kräver ett **nytt explicit användargodkännande av det beskrivna begränsade träningsarena-spelet**, med en bestämd stage-identitet innan ROM DEVELOPMENT II aktiveras. Detta gäller även om N7/Issue #33 avslutas framgångsrikt eller negativt.

**Slutstatus:** `MAIN_NEXT_PLAYABLE_VERTICAL_SLICE_SELECTED_AS_PROPOSAL / EXISTING_COL1_ROM_ANCHORED / N8_N9_NEW_ROM_NOT_AUTHORIZED / N6C_3_ENEMY_KERNEL_OPEN / VERIFY_33_ONE_SHOT_PENDING`.
