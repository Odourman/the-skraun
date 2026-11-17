# THE SKRAUN – MAIN III omgranskning av alla 30 Atari 2600-trick, 17 november 2026

KLASS: SOURCE-ONLY RESEARCH och N6-förberedelse. INGEN ny implementation, ROM, spelcanon, grafik, mapper, merge eller självständig Verification. N6 är INTE slutförd.

## Källauktoritet och kända begränsningar

- Ursprunglig 30-raders forskningsmatris från projektets Google Drive: https://drive.google.com/file/d/1p7a52GmmjFnCKRfGwHRQrsO-ftSgB03A/view
- Tidigare snäv R1-genomgång: https://github.com/Odourman/the-skraun/blob/main/docs/R1_30_ATARI_TRICKS_RELEVANCE_AUDIT_2026-11-16.md
- Tidigare MAIN II visuell trickgranskning: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_II_RESEARCH_30_ATARI_TRICKS_SKRAUN_UPRIGHT_IDENTITY_OPTIONS_2026-11-16.md
- N3 worst scene S0-S9: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N3_WORST_SCENE_RESOURCE_OWNERSHIP_CONTRACT_2026-11-17.md
- N4 PF fargdeadline negativt source-only: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N4_PF_G1_SOURCE_TIMING_REPORT_2026-11-17.md
- N5 verklig R3 36-frame omrakning: https://github.com/Odourman/the-skraun/blob/main/docs/MAIN_III_N5_P1_SAME_Y_FEASIBILITY_AND_GAME_DECISION_2026-11-17.md
- Bindande design och U1-LEG1 korrigeringar: https://github.com/Odourman/the-skraun/blob/main/docs/DESIGN_DECISIONS_01-60_2026-11-16.md
- Ursprunglig historisk IEEE Spectrum-designstudie från mars 1983: https://www.atariage.com/2600/archives/design_case.html?SystemID=2600
- Om Video Chess och verklig kommenterad disassembly: https://nanochess.org/video_chess.html
- Atari Stella Programmer's Guide: https://www.atariage.com/2600/programming/2600_101/docs/stella.html
- Steven Hugg 2025 PF: https://8bitworkshop.com/docs/posts/2025/versatile-playfield-kernel.html
- Steven Hugg 2025 trestrom: https://8bitworkshop.com/docs/posts/2025/versatile-three-stream-kernel.html
- AtariAge historiskt verklig Superchip-vagn: https://static.atariage.com/2600/faq/index.html?SystemID=2600

## Viktig sjalvkorrigering

Tidigare bedömning gav #03 Venetian Blinds for låg prioritet för att pixelrader försvinner. Detta missade att just Video Chess anvande tekniken för att visa 8 objekt i samma bildruta (4 på jämna och 4 på udda rader), och att den anvandes på animationer i Stampede och Sky Jinks. Det ar fel att kräva att ett trick ensamt löser hela scenen; bedöm kombinationer och vad de kostar.

VIKTIG PRECISERING AV TIDIGARE HALO-ORB-IDE: PF halo och BL orb KAN ritas SAMTIDIGT pa SAMMA fysiska rasterrad utan Venetian Blinds om de far DELA COLUPF-färg och bådas former kan representeras. BL ar smal (1/2/4/8 color clocks). #03 behövs först om vi vill ha olika färger på olika rader eller dela upp GOLD HALO och annorlunda färgade PF-hinder. Venetian tillför inte ett femte färgregister, andra PF-bitar eller fler CPU-cykler.

Den viktigaste skillnaden från Video Chess ar att våra två riddare och grona bågskytt kan rora sig fritt i X/Y, inte stå i fasta schackkolumner. En 3-vags randning av R3:s 8 source-row fiendeillustrationer kan ge endast 2-3 unika source-rader per fiende; läsbar svärdsvarning blir då mycket osäker. Vår R3 visar 20Hz per same-Y fiende i exakt EN viss kernel, inte ett universellt tak på Atari 2600.

## Alla 30 trick, ny bedömning

Prioritet A = ska prövas i kombinerad source studie. B = stödfunktion eller reserv. C = begränsad nytta. D = inte nu. DONE = bevarat redan auktoriserat innehall.

| # | Teknik | Prioritet | Konkret nyttjande | Hårt villkor / risk |
|---:|---|---|---|---|
| 01 | Sprite multiplexing | **A** | P1 different Y; add adaptive same-Y row sharing | Does not alone allow 3 P1 actors on same line |
| 02 | Mid-scanline GRP rewriting | **A** | Blackjack-like different graphics among NUSIZ copies | Original copy spacing and GRP/COLUP1 deadlines still bind |
| 03 | Venetian Blinds | **A UPGRADE** | Alternate source rows for same-Y enemies OR PF halo/solid | No extra color plane; 3-way P1 can reduce an 8-row sprite to 2-3 unique rows |
| 04 | Sprite flickering | **B** | Rare fallback with attacking knight prioritized, not universal 20Hz | R3 4/12 frames per same-Y enemy too disruptive as default |
| 05 | Dynamic Playfield sprites | **A** | PF as active halo on some rows, obstacles on others | Same PF mask and COLUPF domain at same physical instant |
| 06 | Mid-frame sprite resizing | **C** | Existing U1-LEG1 scale presentation and conditional P1 | Must not redraw frozen sprite; x4/y3 L3 aspect caveat |
| 07 | Asymmetric Playfield | **A/B** | Distinct left and right PF masks | R3 six expensive PF writes per scanline |
| 08 | Two-line kernel | **A** | Split PF/GRP workload across rows and VDEL | Every physical-line beam deadline remains |
| 09 | VDEL delayed graphics | **A** | P0/P1 pixel prefetch and row sharing | Only latch timing, no new player generator |
| 10 | HMOVE fine positioning | **A** | P1 and BL reposition without accidental P0 displacement | R3 had real P0-shift glitch on midframe HMOVE |
| 11 | Late HMOVE | **D** | Special timing fallback | Potential ugly HMOVE bars and TIA model dependence |
| 12 | Raster color changes | **A UPGRADE** | Gold on halo rows, stone on other rows | PF/BL same COLUPF every physical instant |
| 13 | 48-pixel score kernel | **B** | Dedicated top HUD region | Not free in overlapping arena rows |
| 14 | Multiple display kernels | **A** | HUD / plain field / halo / crowded combat modes | Transitions and worst three same-Y remain |
| 15 | NUSIZ duplication | **A/B** | Combine copies and between-copy graphic rewrites | Horizontal copy spacing fixed, different actor X not automatic |
| 16 | REFP mirroring | **DONE** | Source exact visual facing of U1-LEG1 | Keep reversed source RIGHT/LEFT semantic mapping |
| 17 | Missile and Ball reuse | **A UPGRADE** | BL orb, M0/M1 possible arrow or contour | BL=PF color; M0=P0 color; M1=P1 color; narrow shapes |
| 18 | SCORE mode | **C** | Half-field color split for selected zones | Half colors derive from P0/P1; not free ring versus stone colors |
| 19 | Playfield priority | **B/C** | Actor visibility where halo/stone overlap | Only changes visual priority, not color or collision truth |
| 20 | Hardware collision latches | **B** | Optional collision hint | Cannot treat halo-PF bit as solid hitbox |
| 21 | RIOT timer scheduling | **A** | Prepare PF data, AI, collisions, audio outside kernel | Does not expand 76 CPU cycles per scanline |
| 22 | Stack and RAM reuse | **B** | Scoped scratch liveness, replace big R3 buffer | RIOT stack shares 128 bytes; no naive 112+28 merge |
| 23 | Undocumented opcodes | **D** | Only after measured and hardware-tested win | No new TIA timing windows or owners |
| 24 | Precomputed tables | **A UPGRADE** | Compile per-row register write plan and source masks | Critical worst-case event burst, RAM and ROM must fit |
| 25 | Stack-based TIA writes | **D** | Exceptional byte/cycle local trick | Stack/JSR hazards and no second PF plane |
| 26 | Timing-based horizontal scrolling | **D** | Not needed for eight fixed open arenas | Do not change game layout just to ease kernel |
| 27 | SCABS / special banking | **D** | Not a synonym for ordinary F8/F6 ROM banking | No new raster cycles, format compatibility unknown |
| 28 | Superchip cartridge RAM | **B UPGRADE** | 128 extra bytes on compatible original-console cart | Extra RAM does not add players, color owners or scanline cycles |
| 29 | DPC data chip | **C** | Historical data/audio acceleration alternative | Separate cart architecture, not extra independently colored PF pixel |
| 30 | DPC+/CDF/ARM | **C** | Data prep and game logic on special cartridge if chosen | User approval, RetroN77 compatibility and original-TIA limits remain |

## Nya kombinationer – verkliga kandidater, EJ genomforda resultat

### K1: Adaptiv PF-radrandning for HALO + STEN (+ BL-orb)

Trick #03 + #05 + #07 + #08 + #12 + #14 + #17 + #24. PF ritar halo guld på ena fysiska radsorten och solida hinder separat färg på den andra, i SAMMA 60Hz-bildruta. Bara konfliktrader behöver delas om kontur och sparade färgskift medger det. BL-orb kan utnyttja sin egen enable och horisontell position men ärver COLUPF på varje rad. På rader utan ring/hinder-konflikt kan en kategori få full vertikal upplösning. Fysik: stone blockerar kropp/pil/svärd, halo tränger igenom oberoende av synliga PF-ränder.

RISK/STOP: 50% vertikala samples kan göra ringens övre/nedre del trasig eller stenen oläslig. Två sorters rader kan inte samtidigt ge 3 olika färgägare för gold, stone och en orb med krav på en tredje färg. R3 sex PF-registeruppdateringar och exakta PF-cell-deadlines kvarstår. Ingen riktig DASM kernel har gjorts. GÖR FÖRST originalmask-sourcecompositing 13 X, särskilt X80/X84 maskrad98, båda 2-line faser, 16 HUD + S6 orb collisions, plus perphysical-line write tally.

### K2: Tre P1-fiender med villkorad Venetian och attackerande riddarprioritet

Trick #01 + #02 + #03 + #04 endast reserv + #09 + #14 + #15 + #24. Normal multiplexer på separat Y. På konfliktande Y dela fysisk radrandning efter identitet. Visa aktiv svärdsförvarning högre radandel och andra fiender med lägre men fortfarande deklarerad synlighet under ~24 varningsframes. Prova hårdvarukopior plus BETWEEN-COPY GRP rewrite när spacing/cykler tillåter; tvinga aldrig tre aktörer till fasta X som spelfusk.

RISK/STOP: Chess-metod garanterar inte tre FRIA X/Y som P1 kan ompositionera varje ny rad, och när aktörer står tätt är färg/bitmap/RESP-tid snäv. R3 8-byte originalfiendegrafik blir mycket gles under 1/3-radandel. Källtest S1 (32,101,147, Y78), S2 close/permutation, S3 P0 occlusion och synlig attackvarning. Mät 12/24 råa frames, inte en stillbild, och separera nödvändig TIA rewrite från visuell uppskattning.

### K3: BL som orb, M0/M1 som pil, PF för halo/sten

Trick #05 + #12 + #14 + #17 + #24. Detta kan frigöra P1 från att behöva rita orb och pil; P0 behålls helt låst av U1-LEG1. BL orb rör sig oberoende av PF position men delar PF-färg; M0 pil delar P0-grått, M1 pil delar fiendens färg. S6 ska testa faktisk samtidig färg, horisontell flyttning, enable-byte, objektens sträckning och spriteskadekollision. Inget hårdvaruobjekt uppstår gratis.

### K4: Sparse PF display list + exakt precompute + eventuell cartridge RAM

Trick #07 + #08 + #09 + #14 + #21 + #22 + #24 och #28 ENDAST om RAM kräver det. Förkompilera per-scene giltiga registerskrivningar, positioner och kontaktgränser utanför kernel. Beräkna BÄSTA FALL samt ABSOLUT VÄRSTA PF+P1+P0+BL/Mx-rad; inte genomsnitt. Hugg 2025 tre-stream har 3 register-events/line och 32B per display-list, så det är inte drop-in; vi måste pröva RAM-livstider i hela spelet. R3 buffer 89B, state 23B, COL1 28B får inte summeras som två befintliga lösningar. Superchip ger mer RAM på originalkonsol med kompatibelt cartridge, INTE mer TIA-bandbredd eller gratisfärg. Kolla RetroN77 separat.

### K5: Situationsstyrd lågdetaljgrafik utan ständigt helframeflimmer

Trick #03 + #04 + #08 + #12 + #14 + #19. Använd full sprite och hinderupplösning där resurser inte krockar, radrandning ENDAST vid krävande same-Y/halo-hinder-overlap. Ge farlig aktiv svärdsvarning prioritet, men ingen fiende får tas bort LOGISKT. Det vore en visuell kompromiss, inte en automatiskt godkänd spelregel. Jämför 60Hz video original-Stella och låt användaren utvärdera läsbarhet efter verkligt byggt mikroprov.

### K6: Normal F8/F6 bankning och cartridge RAM - saknad eller feltolkad punkt i originalkatalog

Ursprungliga #27 handlar om SCABS/special banking, inte normalt 8/16K-ROM. Konventionell F8/F6 är ett ytterligare viktigt tekniskt alternativ för 8 banor och maskdata; #28 Superchip för RAM är realistisk om vi behöver hålla buffert och AI samtidigt. Båda fungerar med kompatibelt cartridge på originalmaskinen. DPC/ARM #29/#30 kan öka beräknings- och lagringskapacitet i specialkassett, men ingen lösning garanterar separat PF-kulör i en pixel; besluta format först efter jämförbar data.

## Tre KILLER TESTS i denna ordning – endast source, inga nya ROMs

T1 HALO/STEN/BL-orb: source-exakt R3 X80/X84 row98 och X56/X104, både parity-val och adaptiv switch i mitten av scen. Jämför faktisk source pixelmask mot halvupplost tvåfärgsbild; beräkna register/COLUPF/PF cell deadlines i 76-cyklers fysiska raster. Negativ R3 hela-frame 30/30 får inte påstås fixad om renderresultatet egentligen är samma.

T2 P1 två riddare+grön archer: samma 3 separata X/Y inklusive R3 same-Y och S2/S3 nära X, 1/2 och 1/3 radrandning samt 24-frame sword attack priority. Lista faktiskt visningsbara bitrader och X/color/GRP/RESP writes; ingen helframe-slot-formel får beskrivas som faktisk visual sampling utan Stella.

T3 GEMENSAM ägar-/RAM-/CPU-kontroll: P0 L3 U1-LEG1, 3 P1-logikfiender, PF guld/sten, BL orb, missile pil, HUD, kollisioner/AI/timer och scanline beam deadlines på SAMMA scene. Kandidateffekt är NO-GO vid enda hård registerkrock eller överskriden deadline, och source-only PASS är aldrig production GO.

## Beslut

ALLA 30 har omgranskats som kombinationer. Högst omvärderade är #03 Venetian, #12 raster color, #17 Ball/missiles, #24 precompute och #28 extra cart RAM. Ingen ny hårdvaru-/källimplementation, ingen gameplayförändring, ingen N6 full-arkitektur-GO, ingen merge/Verification. R3 och N4 specifika negativa resultat kvarstår. Nästa lämpliga uppgift: T1+T2 source-only och gemensam T3; om T1/T2 kräver otillåten synlig försämring, eskalera till användaren i stället för att dölja.
