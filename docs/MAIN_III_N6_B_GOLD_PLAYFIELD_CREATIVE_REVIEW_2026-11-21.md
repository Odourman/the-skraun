# THE SKRAUN — MAIN III N6: användarvalt B-test (PF blir guld under halo), prioriterad kreativ omprövning

**Datum:** 2026-11-21. **Klass:** N6 SOURCE-ONLY/konceptuell design- och rasterprövning, **inte** en ny godkänd spelcanon, inte N7, ingen ROM, inget hårdvaru-/Stella-PASS.

## 0. Användarbeslut och auktoritet

I diskussionen om färgoptimering föreslog MAIN tre konkurrerande färgkontrakt: **A original:** halo guld, världsfärgat PF-hinder, guldorb; **B dynamiskt:** under inaktiv halo PF världsfärg, under aktiv halo HELA PF guld; **C en permanent världsfärg** för halo/hinder/orb. MAIN rekommenderade att pröva B först. Användaren svarade explicit **"Ok, vi testar det."**.

Detta är **godkännande att pröva B som N6-färg-/arkitekturkandidat**, inte att permanent införa den utan presentation av tekniska och visuella resultat, inte ett ROM-/N7-uppdrag. Kontrollalternativen A/C bevaras, all tidigare logik och [användarens rangercamouflage](MAIN_III_USER_DECISION_RANGER_WORLD_CAMOUFLAGE_2026-11-21.md) består.

## 1. Preliminär källanalys av alternativ B med verkliga frysta R3/N6-masker

Källa och reproducerbart underlag: [N6 source-only paketerat och omräknat](MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md), [Drive 14-file ZIP](https://drive.google.com/file/d/1enKWO-6h6gVdvnzAQfFQUnE9_QIR2vRL/view). Original R3 source blob SHA `3c9ed79078eee6a0c63100614a593f92e240b5e8`, 13 X-halopositioner x 176 fysiska R3-rader per position = 2 288 källbaserade radfall; dessa är **inte** 2 288 uppmätta CPU-instruktionsspår.

- **B/OFF:** `SCENERY_ONLY` i fryst N6 `N6_SUMMARY.json`: 2 496 minsta nödvändiga PF-registerbyteändringar per 2 288 radfall, världsfärg efter separat `COLUPF` setup.
- **B/ON:** `OR_MERGED_SINGLE_COLOR` i fryst N6: 4 400 minsta nödvändiga PF-registerbyteändringar på samma radfall, HALO-mask OR SCENERY-mask, ett guldvärde i `COLUPF` i arenazonen. 419/2 288 radfall kräver ännu **sex** PF-byteändringar. Siffran räknar ändrade bytes mellan frysta left/right PF-sekvenser, inte extra load/index/bank/beam/kerneltid.
- **Löst i princip:** B kräver ingen **guld-kontra-världsfärg COLUPF-midline-övergång** när hela arena-PF använder en enhetlig guldfärg under attacken, i motsats till N4:s kritiska fyra färggränser på X80/X84 source mask-row98 för två separata kulörer. Fortfarande behövs arenazonens inledande `COLUPF` setup; HUD/andra event och verkliga deadlines måste räknas.
- **Kvarstående synligt problem:** N6:s båda source-kategorier överlappar **104 fysikaliska PF-cell-instanspositioner** sammanlagt i denna 13X×176 sourcereplay. Vid samma guld kan endast EN lysande PF-cell synas där, ingen separat ring/hinderkontur. Dessutom kan närliggande guldfärgade celler visuellt sammanflyta trots att de inte har identiska koordinater. Logiken HALO-PASS genom hinder kontra SOLID-STOP måste fortsatt beräknas separat.
- **Värsta P1/CPU kvar:** B tar inte bort tre fiender på samma Y, GRP1/RESP1/HMOVE, P0 överlapp, BL-orb, M0 arrow, 128B RAM/stack, HUD/AI/timer. Även 6 minsta PF-byte-ändringar kan vara oförenliga med 76c och deadlines när allt annat körs.
- **Orb:** under OFF kan BL visa världsfärgen tillsammans med PF, under ON bli guld. Kontrast mot bakgrund, exakt BL-Y och möjlighet att hitta orben från banstart är öppna kvalifikationskrav. Byt inte orb till osynlig eller otillgänglig.
- **OBS:** Övergripande R3 maskgeometri inkluderar 13 halo X och statiska hinder. Ingen ny animerad ROM, inga alternativa slutgiltiga 8 banor eller PAL/NTSC-registernyanser testade här.

## 2. Vilka kreativa beslut bör prövas och i vilken ordning?

**Rangordna efter sannolik hårdvarunytta, bevarad spelidentitet, tydliga stoppvillkor.**

| Prioritet | Uttryckligt kandidatval att analysera, INTE automatiskt ny canon | Teknik/trick som gör det intressant | Krävd negativ kontroll / visuell kompromiss |
|---|---|---|---|
| P0 | **B: PF blir guld under aktiv halo, vanligt världsfärgat PF när inaktiv** | #12 rasterfärg, #24 sparse/predecode PF, #14 flera specialkernels | 104 cellöverlapp; full ring/kolliderande hinder kan visuellt bli en guldklump. P1+BL+M0+P0 worst scene oförändrad |
| P1 | **Halo 360° logiskt konstant men enklare *synlig* kant/segmentform** | #5 PF-bitmap-mask, #7 asym PF, #8 tvålinjekernel, #24 predecode | Får inte visuellt vilseleda om räckvidd; kvantifiera X80/X84, alla 13 lägen och eventlog samt 8/16/32 wide L1-L3 |
| P1 | **Hinderform och åtta layoutmönster förenklas i PF**, färre komplexa vänster-/högerändringar | #7 PF symmetry/asym, #14 regionkernel, #24 predecode; R3 daggade originalmönster | Inte förlora 8 olika banor, fri L3 manöver, väggars riktiga solid-kollision och halo-through-solid |
| P1 | **Fiendehöjd och antal sprite/attackpose-rader optimeras**, rangern kamoufleras fortfarande | #1 multiplex, #2 GRP midline, #3 lokal Venetian, #8 two-line / 3line, #9 VDEL, #14 flera kernel | 3 äkta fria X/Y kvar; 0.4s warning/faktiskt svärd måste ses; inga hopslagningar av unika figurer |
| P2 | **BL-orb liten och formstabil; kan växla world-color OFF/gold ON** samt öppen säker Y och kontrast | #17 Ball, #14 region, #24 predecode | Orb syns från början, går att nå, ligger kvar under L3, ingen gratis guld på sten-rader |
| P2 | **Likröda riddare, grå M0-pil, statiska drömspiraler, enkel effekt-animation och separat HUD** | #12 raster color, #14 multiple kernels, #17 M0/BL owner, #13 HUD | Färre COLUP1/P0-färgskiften, men oberoende X/GRP/beam krävs. Pil/vindup/invulnerability måste vara tydliga |
| P3/guarded | **Level3 kroppsmått och visuella storlekssteg** | #8 2line/3line P0 repetitive row schedule | Starkt användargodkänd U1-LEG1 8×12 mask och visuell skalning; rör endast efter faktiskt fastlagd blocker, med explicit spelardesignbeslut |
| P3/guarded | **Högst en aktiv knight plus Ranger; senare nya riddare i reserv** | #1 actor multiplex/P1 lower overlap | STOR gameplay-ändring jämfört med två samtidigt aktiva riddare; skydda totalantal/framkomst, kräver nytt användarbeslut |
| P3/guarded | **Aktiv attack signaleras med bakgrundspuls snarare än full ring, logisk 360° bibehållen** | #12 BK changes, #14 specialkernel | Ger inte gratis cirkulär räckviddsgrafik och kan bli orättvist/otydligt, allra sista visuella reserv |

### Var inte låsta vid krav som inte köper spelkänsla

- Undvik att ändra 8 öppna banor, Skraun upprätt U1-LEG1, 360-graders logisk attack, förutsägbar rangerpil, svärdsvärmning, högt level-3 power och kamouflage enbart för att göra en mikrotest enklare. De är spelets identitet.
- Däremot behöver inte haloexakt ringkontur, objektens sekundära färger, röda riddarnas olika shades, stenarnas mönsterrikedom, fiendernas antal fysikaliska bitmaprader eller orbens konstnärliga färg vara heliga om ett genomförbart alternativ skapar bättre helspel.
- Vid kreativa byte: definiera både synlig effekt (pixlar/läsbarhet) och spelarnas informationsbehov (vad kan träffa, var är fienden/obstacle/orb) med explicit user-val när canon ändras.

## 3. N6-C praktisk jämförelse och stoppvillkor

Pröva B som **förstahandskandidat** och A/C som kontroller, medan S0–S9 hålls identiska:

1. Kontrollera B OFF scenery och B ON halo OR scenery med exakta R3 X56..104 maskkällor och samma X/Y/fiendescenarier; utforma beam-deadline-laglig arena-`COLUPF` setup, 0/1/2/3/4/5/6 PF byte-delta och BL orb i både OFF/ON.
2. Pröva **minst två visuella haloformer** och två distinkta PF hinderlayout-strategier endast source/ritförhandsgranskning först. Presentera original och kandidat pixel-troget och mät kritiska per-rad skrivbehov, inga syntetiska 'PASS' utan faktisk genomförbarhet.
3. Fiendeskemat ska hantera fri X/Y/alla överlapp med P0-lending kontra lokalt Venetian, och framhäva 24f svärdsvärn. Korrigera eventuella extra `COLUP0/1` skiften från färgägarlån.
4. En enda integrerad schema-/kostnads-/RAM-tabell: samtliga register, deadline, 76cy per fysikrad, RIOT128 inkl stack, 262 frame, VBLANK/overscan logic. Stoppa vid första falsifierade kandidat med exakt motexempel.
5. Om B löser färgregistret men inte worst PF-data/fiender, välj separat kort revision av halo- eller hindergrafik. Om P1 three-way fortfarande inte går, analysera kortare fiender/enkla animationer innan att föreslå en aktiv riddare. Om väsentlig konst ändras behöver användaren godkänna valet.

**STATUS:** `N6_B_USER_APPROVED_FOR_COMPARATIVE_TESTING`, `N6_B_SOURCE_COLOUR_BOTTLENECK_RELIEF_NOT_ROM_PROVEN`, `N6_C_FULL_SCHEDULE_OPEN`, `N7_NOT_AUTHORIZED`, `NO_CANON_B_ADOPTION`.

Källor: [MAIN III N6](MAIN_III_N6_COLOR_OBJECT_ARCHITECTURE_DECISION_2026-11-21.md); [N3 S0-S9](MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md); [N4 exact PF negative](MAIN_III_N4_PF_G1_SOURCE_TIMING_REPORT_2026-11-17.md); [N5 36 genuine frames](MAIN_III_N5_P1_SAME_Y_FEASIBILITY_AND_GAME_DECISION_2026-11-17.md); [all30 tricks](MAIN_III_SECOND_PASS_ALL_30_ATARI_TRICKS_AND_COMBINATIONS_2026-11-17.md); [Let Me Out transfer](MAIN_III_THREE_PASS_LET_ME_OUT_TRANSFER_TO_THE_SKRAUN_2026-11-21.md).
