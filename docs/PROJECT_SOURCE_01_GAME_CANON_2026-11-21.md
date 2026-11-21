# THE SKRAUN – PROJECT SOURCE 01: SPELCANON OCH VISUELLA RIKTLINJER

**Snapshot:** 2026-11-21. **Denna fil beskriver och länkar till äldre och senare bindande användarbeslut; den uppfinner inga nya.** Vid konflikt kontrollera [bindande designbeslut](DESIGN_DECISIONS_01-60_2026-11-16.md) och [faktisk godkänd konst](SKRAUN_VISUAL_DIRECTION_2026-11-16.md). En föreslagen teknik är inte samma sak som godkänd konst/canon.

## 1. Kärnspel och nivåer

- Snabbt Atari 2600-arkadspel uppifrån; **Skraun står upprätt i bilden**, har horn/ögon/mun, utåtsträckta armar, getlika ben. Ej liggande fyrfotad kropp eller äldre P1 horisontell referens.
- 8 fasta, åtskilda banor med få solida hinder: skog 1–2, berg 3–4, dröm 5–6, natt 7–8. Fria manöverytor även för **största Skraun**, ingen tillväxtfälla vid orb, åtta joystickriktningar och glid längs fria hinderkanter.
- Skrauns nivå 1 är svår, nivå 2 medelsvår, nivå 3 ska kännas övermäktigt stark. Hastigheten ska inte bli trög p.g.a. kroppsstorlek. Level består mellan banor; poäng och liv följer tidigare regler.
- Två riddare och **en Ranger** ska vara aktiva samtidigt när scenen kräver det. Totalt per bana: skog 2 riddare, berg 2, dröm 3, natt 4 (reserver kommer senare); 1 Ranger per bana. Minska inte samtidiga fiender som teknisk genväg utan nytt uttryckligt beslut.
- Riddare jagar och träffar bara med **svärd**, inte kroppskontakt. Tydlig ~0,4s varning med riktningen låst, kort aktiv slagfas, ungefär 1s återhämtning. Svärdsposer **inbyggda i P1** är det föredragna N6-forskningsspåret; M1 separat linje endast reservtest. Ingen ny svärdskonst är redan godkänd.
- Ranger flyr, använder hinder och skjuter högst en aktiv pil. Pilens riktning låses vid avfyrning. Halon kan förstöra pilen; pil/svärd blockeras av verkligt solida hinder.

## 2. Spelarfigur och tre storlekar

- Exakt **U1-LEG1** ljusgrå nivå-1-källmask 8×12, två A/B gångposer och spegelvänd vänster/höger, användargodkänd. Källa: [U1-LEG1 A/B](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json). Den visuella HÖGER-riktningen motsvarar tidigare LEG1 LEFT-källdata; visuell VÄNSTER motsvarar tidigare RIGHT.
- Nivå 2 och 3 bygger på **samma källa**, inga nya detaljer eller posevarianter. Preliminär visningsplan L1=8×12, L2=16×24, L3=32×36. Alternativ L2=16×20/L3=32×30 **enbart källbaserade försökskandidater**, inte valda slutmått. Att sänka L3 från 36 till 30 rader löste inte den svåraste tre-fiender-samma-Y-konflikten i N6-C.
- Användaren har på nytt betonat **smidig L3-rörelse och inte alltför stor kropp**. Åtta öppna banor och mindre central kollisionsyta kan övervägas men en ny hitbox kräver synlig, rättvis designkontroll, inte osynlig genomfart genom väggar.

## 3. Magisk halo, orb och färger

- Skraun angriper med **360° halo**, som passerar genom solida hinder och omsluter kroppen. Halo aktiv ungefär 0,5s, blir **tjockare och får större yttre räckvidd** på stigande level; exakt radie, kontur, bytevärden och visuell genomförbarhet ej låsta. Rörelse under aktiv attack tillåten.
- *Valt jämförelsetest B, inte permanent slutgiltig palett:* arena-PF har **världens hinderfärg när halon är AV**, och **hela arena-PF blir guld när den är PÅ** (hinder+halo OR-mask). Det minskar särskilt tvåfärgs-COLUPF konflikter men kan få hinder och ring att flyta ihop.
- **Orb:** en liten enkel Ball-kandidat, synlig från banstart, säkert nåbar. Föredragen N6-provkandidat: samma världsfärg som PF när halo är AV och guld när PÅ. Får ha diskret avsiktligt flimmer om den förblir läsbar. Finns kvar vid level3 om ej tagen. Behandla inte en färgtestriktning som maskinverifierad ROM.
- **Riddare:** två med **samma ljusblå TIA-färg** i första fortsatta test, hellre än R3:s två olika röda. Exakt nyanskod ej låst; kontrast i natt- och bergsvärld måste provas. **Ranger är världskamouflerad**: grön i skogen, lila i drömvärlden, miljöanpassad i berg och natt; inte generellt alltid grön.
- Drömvärldens spiraler är **statiska**. Miljöformer ska hållas sparsamma, tydliga och hårdvarutrogna utan att lova åtta redan testade kartor.
- Källa till denna kandidatstatus: [N6 user-accepted comparative scope](MAIN_III_N6_USER_ACCEPTED_COMPARATIVE_DESIGN_SCOPE_2026-11-21.md) och [N6-B halo/objektanalys](MAIN_III_N6_B_GOLD_PLAYFIELD_CREATIVE_REVIEW_2026-11-21.md).

## 4. Särskilt *inte* slutgiltiga beslut

- Exakt ljusblå färgbyte / fyra rangerfärger; exakt haloform eller halostorlek; kroppsstorleksändringar L2/L3; separat M1-svärd; slutlig fysisk collision hitbox; acceptabla per-aktör duty-cycle-/flickervärden.
- Färger/figurer i äldre R3-kod är **historiska diagnostikkällor**, inte aktuellt konstgodkännande.
- Denna Project Source är bara en komprimerad ingång. Vid osäkerhet följ originalet, inte denna sammanfattning.
