# THE SKRAUN — P02-R3 DECISIVE FEASIBILITY: MAIN HANDOFF
**Datum: 2026-11-16. ROM DEVELOPMENT. Utvecklaregenkontroll, ingen oberoende VERIFICATION.**

**Bindande scope:** https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_ROM_DEV_P02_R3_DECISIVE_SCENE_SCHEDULER_AUTHORIZED_2026-11-16.md

**Isolerad experimentgren:** experiment/romdev-r3-decisive-scene-scheduler, skapad från R2:s frysta commit 2cb9eafa0f5964e89553f791ff18ea9d9362fe8e. **Draft PR #14** https://github.com/Odourman/the-skraun/pull/14 mot R2:s experimentgren, INTE main. Ej mergad, ingen B3c/R4 eller AI.

## 1. Beslut till MAIN: NO-GO för direkt B3c

Tre oberoende fiende-X/Y och tre distinkta P1-bitmappar kan produceras inom riktig original-TIA, men **vid tre fiender på samma Y visas varje fiende bara 20Hz (4 av12 frames)**. Vid två överlappande och en tredje i separat band: 30/30/60Hz. Vid tre separata Y-band: 60Hz per fiende. Spelreglerna garanterar INTE sådan permanent Y-separation. Att tvinga detta vore en obehörig gameplayändring.

En verkligt större nivå3-guldhalo syns tillsammans med syntetiska hinder endast med två oacceptabla kompromisser i dessa kernels: antingen **guldhalo 30Hz och blå hinder 30Hz på ALTERNERANDE hela frames**, eller både halo och hinder 60Hz i samma guldfärg i en enda PF-bitmap, där hindergränser och halo smälter ihop på overlap. Det är INTE två samtidigt individuellt färgade grafiklager på samma scanline. Värsta 6502 rasterlinjerna har bara **2–4 cykler marginal av76** före riktig pil/orb/AI/collision. Alltså inget produktions-GO.

## 2. Riktigt DASM-byggda originalkompatibla 4K ROMs

Samtliga **3×4096 byte**, riktiga 6507/TIA ASM, ingen bankswitch eller AI, har byggts med DASM -f3, -o BIN, -l LISTING och -s SYMBOLS. Källorna ligger under experiments på grenen:

| Variant | Source | Verifierad BIN SHA-256 |
|---|---|---|
| Full same-Y overlap | romdev_r3_overlap.asm | f25c8622c115f85717b1fd51ff2a30cfb6fa293e95aceb228257c0655067775c |
| Delvis overlap + separat archer | romdev_r3_partial.asm | 411f7ce389e0853f071011e0ab2be34ad90c47f352ea524f1ad39e98891d501c |
| Tre oberoende Y-band | romdev_r3_stagger.asm | 94ae477a944a042a6e605b6046b4e833b0cf3387bc62906e75491e47a649f226 |

## 3. Tre fienders synlighet och faktiska koordinater

Varje av fiende1, fiende2, bågskytt har X/Y i separata RAM bytes EnemyX0..2 och EnemyY0..2, oberoende av R2:s fasta NUSIZ-avstånd. Fiendegrafik är två distinkta röda riddarbilder och en grön bågskyttmask. 89-byte RIOT P1 row-buffer fylls i VBLANK; P1 repositioneras mellan Y-band i tomma 4-linjers rasterluckor. Bilderna är faktiska Stella-snapshots tagna via Debugger frame #1 + saveSnap, med pixelräkning i tests/romdev_r3_frames.py, inte asynkrona GUI-snapshots.

| Scenario | Fiendernas X,Y i diagnostisk TIA/RAM | Verklig synlighet i tolv konsekutiva 60Hz frames |
|---|---|---|
| overlap | (32,78), (101,78), (147,78) | **4/12 per fiende =20Hz** |
| partial | (36,75), (105,82), (149,141) | **6/12,6/12,12/12 =30/30/60Hz** |
| stagger | (28,20), (111,80), (149,141) | **12/12,12/12,12/12 =60Hz vardera** |

20Hz innebär ~16,7ms synlig, därefter ~33,3ms helt osynlig. 30Hz innebär en frame synlig, nästa frame helt osynlig. Om störande kontinuerligt blink accepteras är ett visuellt MAIN-/användarbeslut. Inget sådant godkännande har givits.

**Extra observation:** På partial med P0 vid x104 skymdes **128 av136** av den andre riddarens röda pixels, d.v.s. **94,1%** trots oförändrat fiende-X/Y. Skuggning/prioritet kan alltså i sig dölja en fiende nära spelaren även på en frame då hans slot är aktiv.

## 4. Verklig nivå3-halo + samma-Y hinder

P0 är light-gray overhead, 4×8bit NUSIZ0 = **32 TIA-color-clocks /64 original PNG-pixels bred**, och **36 fysiska scanlines hög**. Den större nya nivå3-halon är prekomponerad asymmetrisk PF med nominell **48-color-clock ytterbredd, 72 scanlines höjd och 4-clock tjockare kant**, jämfört med R2:s mindre cirka40×64 level2-halo. Faktisk 4-clock PF-quantisering ger observerad ring-bbox cirka**104 original PNG-pixlar =52 TIA-clocks**, cirka 2 clocks centeravvikelse från P0. Level3-art och gameplay attackradie är INTE officiellt godkända eller implementerade.

Höger PF2 måste skrivas för större level3-halo vid x104. Den faktiska ROM-tabellen R2_104 är icke-noll och Stella visar gold till **PNG x256–263**. Vid x56,80,104 och riktningsbyte finns inga klippta pixlar inom den diagnostiska gridden; en permanent gameplay-screen edge har INTE beslutats. SWCHA håller 4-clock X-step med två frame-gate; ingen B3c 8-vägs kontroll.

Tre fasta syntetiska hinderkolumner i overlap Y vid TIA x56,88,108 kan visas blått utan halo eller tillsammans som samma guld-PF. I tolvcaptures visar två färglager **6/12 guld och 6/12 blå frames**, aldrig separata lager samtidigt. Stagger visar gold+scene på varje frame, men med sammansmälta guldbitar. Inga riktiga kollisions-/solidity data eller magiska träffar är modellerade. Magic-goes-through-obstacles och hinder-soliditet måste ha oberoende framtida collision-sanning.

## 5. CPU-/rasterbudget och vad som faktiskt mättes

**STATIC beräknat utifrån faktiska DASM-symboler och adresser**, tests/romdev_r3_static.py, 13 center och full A/B branch/page-crossing enumeration:

| ROM | Physical A max /76 | Physical B max /76 | Min marginal | Right PF0 latest | PF1 | PF2 |
|---|---:|---:|---:|---:|---:|---:|
| overlap | 63 | 72 | 4 | 42 | 50 | 58 |
| partial | 63 | 73 | 3 | 42 | 50 | 58 |
| stagger | 63 | 74 | 2 | 42 | 50 | 58 |

Beräknade right PF beam-deadlines: PF0 cirka49,33 CPUcycles; PF1 cirka54,67; PF2 cirka65,33. Alla tre registeruppdateringarna klarar dessa deadlines i den statiska modellen. En fysisk NTSC-line har 76 CPU-cykler, även i tvålinjerskernel.

**DIRECT observerat i Stella Debugger 6.7.1:** Alla tre färdiga ROMs har **262 NTSC scanlines**, 19 direkt testade states per ROM och totalt **57 äkta original-Stella PNGs**, där 36 är 12 konsekutiva frame-captures per ROM. Den verkliga Mode-sekvensen vid center, edge och reverse är **6,12,12,0,0,6,7**. Sista 7 är korrekt 4-clock steg efter ytterligare en right-hold frame, inget testfel i ROM. Direct debugger frame-längd är INTE en per-instruction 6507 trace.

P1Buf nollställs i VBLANK (89 bytes, runt **893 statiskt uppskattade CPU-cykler**), och 1–3 fiendebitmappar×8 rader komponeras (cirka151 loopcykler per bild före JSR/setup). HUD: verklig blå/cyan **16-scanline placeholderregion**, arena 176 rows, ingen riktig score/lives logik och ingen avlastning för hard same-Y rows.

**Pil/orb är inte verkligt implementerade i R3.** Minsta LDA immediate + STA ENAM0/ENABL är **5 nya cykler per reg** utan positions-/fysik-/collisionwork. Worst overlap skulle redan bli77/76, partial78/76, stagger79/76 för bara en ny enable på samma rad. Att placera en sådan write på annan tom rad är en obekräftad framtida schedulerhypotes. M0 delar P0-grått, M1 P1-rött/grönt, BL PF-guld/blått. Dessa ger inte godtyckligt fri egenobjektfärg.

## 6. Exakt RIOT och ROM-kompakthet

128-byte RIOT RAM: **23 bytes state på $80..$96** (10 byte PF pointers, Mode, Frames, Slot, ShapePtr, ActiveX, EnemyX/Y, RasterSave), plus **89-byte P1Buf på $A0..$F8**, totalt **112/128 använda**. Återstående16 omfattar stackregionen **$F9..$FF** för SP=$FF. Därmed bara **9 bytes $97..$9F direkt säkert oanvända** innan stackdjupsanalys. Verklig AI, collision, score/lives, audio, arrow/orb saknas.

Faktiska DASM listing emitterade adresser (inte antal nonzero-rombytes, och ORG-hål räknade som fria):

| Kandidat | Emitterad kod/data i 4K | Lediga ORG-byte | Största sammanhängande hål |
|---|---:|---:|---:|
| overlap | 2102 | 1994 | 1124 |
| partial | 2226 | 1870 | 1124 |
| stagger | 2214 | 1882 | 1105 |

Mask-deduplikation: overlap/partial 40 unika×19-byte PF masktabellblock =760 ROM bytes, stagger 41×19=779 bytes. Naiv åttafaldig duplicering av 760-byte masks i åtta oberoende banor kostar **6080 bytes före sprites/3 levels/AI/audio/HUD**. Detta är illustrativ scaling-risk, INTE optimal nedre ROM-komprimeringsgräns. En bankad ROM kan spara mer data men ökar inte antal fysiska PF-lager, sprites eller 76cycles.

## 7. Ärliga misslyckanden och korrigeringar

1. SDL/Xdotool BadWindow vid första debugger-HUD-fönstret: testharness-fel, fix genom att återupptäcka aktuell synlig Stella window.
2. Initialt **260 NTSC scanlines = FAIL**. Timer 44/43/43 för overlap/partial/stagger efter debugger-undersökningar av 263 och261 mellanrevisioner gav slutligen 262. Äldre ROM SHA är INTE frysta.
3. Stagger midframe HMOVE skiftade P0 oavsiktligt då HMP0 låg kvar. Fix: skriv HMP0=0 innan varje senare P1-HMOVE. Original PNG testar rätt x56/80/104.
4. Gammal HUD PF-data gav färgbleed på första arenaraden. Fix: PF0/PF1/PF2 nollas efter HUD.
5. En extra right-held debugger-frame efter reversering ger korrekt Mode7 efter Mode6. Testförväntan korrigerades, ingen ROM rörelsebugg.
6. Kandidaternas absoluta scen-y-start kan skilja 1–2 scanlines på grund av VBLANK/regiontimer; i en ROM behålls samma grå 64×36 P0-form och ringens relativa placering.
7. **Olösta verkliga hinder:** 20Hz enemy, 30Hz halo/hinder, same-color PF merging, 94% P0-occlusion vid partiellt overlapp och 2–4 CPU-cykler headroom. Inget av dessa får rapporteras som full game feasibility PASS.

## 8. PASS/FAIL/BLOCKED OCH MAIN-ALTERNATIV

| R3-grind | Resultat |
|---|---|
| Tre individuella EnemyX/Y och tre distinkta sprites | PASS, diagnostik |
| Tre skilda höjdband alla60Hz | PASS begränsat |
| Två fiender same-Y 30Hz var + separat archer60Hz | PASS teknik med FLICKER |
| Tre fiender same-Y 20Hz var | PASS tidsdelningskod men VISUAL FAIL/RISK |
| Level3 större halo, grå P0, right PF2 och x56/80/104 | PASS inom diagnostisk range |
| Samtidigt oberoende tydlig halo + hinder på samma frame/rasterrad | FAIL i testad enda PF-plan |
| 3 fria same-Y fiender + pil/orb + färgseparerad halo + riktig HUD | BLOCKED i dessa 3 kernels |
| 262 NTSC och statiskt PF registerdeadline test | PASS utvecklaregenkontroll |
| AI, collisions, arrow/orb sprites, 8 banor, riktiga lives/score, ljud, B3c 8-way, PAL/hårdvarukonsol | NOT TESTED / ej auktoriserat |
| B3c, R4, main merge, independent VERIFICATION | NOT STARTED |

**Alternativ A:** MAIN/användaren godkänner explicit svårt 20/30Hz-flimmer och oavklarad pil/orb-CPU-budget. ROM DEVELOPMENT avråder under läsbarhetsbeslut59.
**Alternativ B:** MAIN auktoriserar ett nytt snävt TIA-arkitekturförsök. Staggered 60Hz är bara fast path, och att tvinga riktiga fiender att aldrig ha samma Y vore ändrad gameplay. Inget löfte att annan original-TIA-kernel klarar det.
**Alternativ C:** MAIN gör ett uttryckligt grafiskt eller hårdvarumässigt plattformsval. F6/F8 bankning löser ROM-data, inte TIA-PF-färg och actor-scanlinebudget. DPC/ARM ställer nya kompatibilitets-/distributionskrav och skapar inte automatiskt ny TIA-plan. Ingen migrering utförd.

**Slutlig rekommendation: avsluta R3 och stoppa automatisk B3c. MAIN beslutar nästa uttryckliga scope.**

## 9. Färdiga ursprungsbevis

- [Sista riktiga 4K DASM/ROM build, symboler/listningsfiler, path-CSV och SHA: GitHub Actions #43919399638](https://github.com/Odourman/the-skraun/actions/runs/43919399638).
- [Slutligt GREEN direkt Stella Debugger 262-lines, 57 original bilder, uppmätt 20/30/60Hz och pixel regression: GitHub Actions #43919941150](https://github.com/Odourman/the-skraun/actions/runs/43919941150).
- [Draft PR #14, INTE merged](https://github.com/Odourman/the-skraun/pull/14).
- [Google Drive: R3 originalbevis](https://drive.google.com/drive/folders/1lxeqjTpPM3hhTz3Xm-YX_zf6AifV1ME3).
- Fullständigt MAIN ZIP med 3 ROM, source/list/sym, 57 autentiska Stella PNG, debugger-sessioner och beräknade CSV samt SHA manifest publiceras som separat slutpaket.

**Ingen B3c, R4, AI, collision, main-merge eller oberoende VERIFICATION.**
