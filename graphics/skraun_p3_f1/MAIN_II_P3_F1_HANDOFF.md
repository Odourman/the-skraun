# THE SKRAUN – GRAPHICS P3-F1 / MAIN II – SLUTRAPPORT

**2026-11-16 | Avgränsat designuppdrag | Designförhandsvisningar, INTE Stella | Inget estetiskt godkännande**

## Slutresultat

**KÄLLDATA: PASS. IDENTITET VID NIVÅ 1: EJ BEVISAD. HÖGER/VÄNSTER I FAKTISK NIVÅ-1-STORLEK: EJ BEVISAD.**

De två nya U1-baserade förslagen förbättrar de **permanenta, geometriska** höger/vänster-signalerna. Däremot kan jag inte påstå att de nu **liknar användarens originaltroll betydligt mer** eller att människor särskiljer deras två riktningar på en normal Atari-TV. Den omärkta jämförelsen har producerats för MAIN/användaren men **ingen mänsklig blindstudie** har utförts. Det vore ett felaktigt PASS att använda enbart ökade bitavstånd som estetisk acceptans.

MAIN II:s senare rättelse är bindande: **SPELBILDEN** ses ovanifrån, medan **trollet STÅR UPPRÄTT** med horn och huvud uppåt, armar åt sidorna och två ben under kroppen. Ett stiliserat synligt ansikte är tillåtet. Den tidigare P1/P2-anatomins liggande djur är en negativ historisk referens, inte en möjlig P3-F1-kandidat.

## Källor genomgångna

- [Bindande, uppdaterad MAIN II-order](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_II_TO_GRAPHICS_P3_F1_UPRIGHT_FACING_READABILITY_AUTHORIZED_2026-11-16.md), [ärende #21](https://github.com/Odourman/the-skraun/issues/21), inklusive användarens **"U1 är lite åt rätt håll"**. Detta betyder inte att U1 är nära att godkännas.
- [MAIN II:s P3-beslut](https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md), [designbeslut 01–60 och senare rättelse](https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md), [aktuell visuell riktning](https://github.com/Odourman/the-skraun/blob/main/docs/SKRAUN_VISUAL_DIRECTION_2026-11-16.md).
- [Fryst P3-U1-källfil](https://github.com/Odourman/the-skraun/blob/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead/P3_SOURCE_BITMAPS.json), dess granskade tidigare PNG/GIF i Drive, och MAIN II:s källkontroll.
- Privat [originalteckning i Google Drive](https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view) granskad enbart som **privat referens**: två korta horn, stora ögon, öppen mun, två långa viftande armar och tydliga ben/stora fötter. **Originalfotot finns INTE i ZIP eller GitHub.**

## D1 – Face/Ear Signature

- **Exakt 8×12, två gångposer och bit-exakt vänsterspegling.** Två horn, nu placerade asymmetriskt vid överkanten, större fullbordad huvudkontur åt höger, två negativa ögonhål och **2×2 mörka ansiktsceller** som munöppning. Huvudet (rader 0–4) är identiskt mellan gångposerna så att riktningen inte är beroende av gångsteget. Armar och ben växlar oberoende.
- **Fördel:** Munnens mörka öppning omfattar fler bildceller än tidigare U1:s två. Ursprungliga Skrauns uttrycksfulla ansikte och horn får högst prioritet. Den markerade högra käken kan ge ett riktningstecken som består även under stegväxling.
- **Nackdel:** Stora mörka munhålet kan uppfattas som ett tekniskt tomrum eller ett groteskt ansikte på en frontal liten figur. Två ögon och en mun i 8×12 syns inte nödvändigtvis som ett personligt ansikte i nivå 1. Det går inte att beskriva detta som en säker identitetsförbättring.

## D2 – Shoulder/Arm Signature

- **Exakt 8×12, två gångposer och bit-exakt vänsterspegling.** Behåller U1:s båda horn, ögon och ursprungliga mörka munanvisning i huvudet. Stabil förstoring av högra käk-/axel-/överkroppskonturen (rader 4, 7 och 8), medan armarna viftar diagonalt och fötterna tar två steg.
- **Fördel:** Mer skev, distinkt kroppsform och ett riktningsankare i överkroppen som inte byter sida av gångsteget. U1:s ansikte är mindre omritat.
- **Nackdel:** Tunn kropp och utskjutande armar riskerar fortfarande att se ut som en generisk människa/robot. Öppen mun förblir en liten U1-lik öppning. Den asymmetriska axeln kan misstas för en armrörelse.

## Jämförelse med fryst U1: mätdata, inte estetisk poäng

**Exakt antal skilda av 96 källbitar**. A-R = pose A höger; B-L = pose B vänster.

| Par | U1 fryst | D1 Face/Ear | D2 Shoulder/Arm |
|---|---:|---:|---:|
| A-R mot A-L | 10 | 22 | 24 |
| B-R mot B-L | 12 | 20 | 22 |
| A-R mot B-R (gångsteg) | 7 | 9 | 7 |
| A-R mot B-L (korsförväxling) | 5 | 17 | 23 |
| A-L mot B-R (korsförväxling) | 5 | 17 | 23 |
| Skillnad D1/D2 mot gamla U1, A respektive B | 0/0 | 10/8 | 9/13 |

U1:s 5/96 korsavstånd är en konkret källa till förväxlingsrisk. D1/D2 ökar dessa avstånd, men **en bilaga med biträkning ersätter inte den användarstyrda oetiketterade nivå-1-granskningen**. `HAMMING_AUDIT.json` visar fullständig 4×4-matris inklusive huvudregionens riktningsavstånd. `audit_hamming.py` räknar om varje värde oberoende av en manuellt ifylld tabell.

## Granskningsordning – visa blind bild först

1. **`00_BLIND_L1_UNLABELED.png`**: 12 omkastade, omärkta nivå-1-utsnitt med nummer 01–12, inga riktningstips. Samma 240×164-utsnitt i den faktiska 640×480-TV-approximationens skala; ingen extra zoom. Utvärdera själv innan facit öppnas.
2. **`01_BLIND_ANSWER_KEY.md`**: separat facit. Detta är **inte** en utförd mänsklig läsbarhetsstudie.
3. **`02_L1_LABELED_SAME_SCALE.png`**, `03_L1_NATIVE_160x192.png`, `04_L1_FULL_4_3_SCREEN.png`: identifierade, direkt jämförbara scener utan extra spritepixlar.
4. **`05_EXACT_8x12_GRIDS_ALL_STATES.png`**, `06_BLACK_WHITE_SILHOUETTES_ZOOMED.png`, `08_GAIT_HIGHLIGHTS_SOURCE_ONLY.png`, `09_STABLE_FACING_CUES.png`: förstorade källdata och analytiska markeringar, **inte faktisk spelstorlek**.
5. **`07_L1_L2_L3_CONCEPTUAL.png`**, `10_FOREST_NIGHT_FLAT_CONTEXT.png`: endast illustrativ skalförstoring och enfärgade bakgrunder; inte full TIA-renderer.
6. **`GIF_U1_*.gif`, `GIF_D1_*.gif`, `GIF_D2_*.gif`**: två animerade posebilder vid exakt samma bildfrekvens, både höger och vänster.

De tre konceptuella nivåerna är L1 = 8cc×12 linjer, L2 = 16×24 och L3 = 32×36. Alla bildfiler är **DESIGN PREVIEW – NOT STELLA**. Ingen teknisk ART1-nivå-3-reparation har gjorts; #19 är oförändrat.

## Stopp och rekommendation

**Rekommendation till MAIN II: bedöm D1 före D2 vid faktiskt nivå-1-avstånd på den blinda sidan, eftersom identitet prioriteras över enbart spegelskillnad.** D2 kan jämföras separat som axelbaserat riktningsförsök. Ingen sprite är slutgodkänd.

Källans format/mirror/poses är automatiskt kontrollerbara, men **full identitet + avläst höger/vänster är fortfarande EJ PROVEN**. Om de nya nivå-1-bilderna ser ut som generiska små figurer är detta ett negativt identitetsresultat och P3-F1 ska stanna utan P3-F2/P4/v0.4. Ingen ROM, Stella, ny dimension, ny värld/halo/fiende/HUD, ändring av spelregler, merge, oberoende Verification, art-gate #15-stängning eller ART1-fix #19 har utförts.
