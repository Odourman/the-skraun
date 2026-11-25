# THE SKRAUN — GRAPHICS II → MAIN V | FINAL WORLD GRAPHICS REVISION 2

**2026-11-25 — SOURCE_ONLY; estetiskt ej slutgodkänd.** Exakt användarreferens (oförändrad) samt samtliga 8 banor, 16 egna grundmotiv och färdig PlayPF1-table enligt befintlig Atari-2600-kernel. Ingen ROM, DASM/Stella-nykörning, ingen main-merge.

## Teknisk diagnos och förbättring

- Ursprungliga Revision 1 repeterade 6 motivrader × 8 fysiska scanlines för 14 motiv (spiraler 12 × 4). Därför blev formerna visuellt långsmala och klippte på överkanten.
- Originalbank3 PR60 visar: 186 synliga rasterrader i `Visible` / `VisibleArrow`, `WorldPFIndex[X] = floor(X/2)`, `LDA (WorldPFPtr),Y; STA PF1`. **En tabellpost visas i två rasterrader**, inte åtta. Det finns **96 bytes per arena**.
- Revision 2 ger oberoende PF1-byte per **2 scanlines**: kompaktare proportioner, 15–25 rasterrader övre marginal, minst 13 rasterrader nedre marginal. Övergången i mitten är tom och väl tilltagen; inga extra TIA-skrivningar/RAM/mapper.
- TIA bit7→bit0 vänster-till-höger i PF1 x16..47; varje bit är **4 färgklockor** bred. Spelplanen är 160 färgklockor och 186 scanlines i den aktuella synliga loopen. Därför levereras både exakt 160×186 native och TV-proportionerad presentation med **2 horisontella bildpunkter per färgklocka**. Exakt analog CRT-kalibrering ingår inte.
- **Viktig risktolkning:** De två oanvända toppindex 94/95 ändras inte; y=0–15 lämnas tomt. Indextabell, bankpekare, spegling/upprepning, färg och source ownership är oförändrade.

## Åtta banor

| Bana | Värld | Övre motiv | Nedre motiv | PF-sätt |
|---|---|---|---|---|
| 1 | Skog | Barrträd A (42 rader) | Rundkronat lövträd A (44 rader) | mirror |
| 2 | Skog | Barrträd B (42 rader) | Rundkronat lövträd B (44 rader) | repeat |
| 3 | Berg | Spetsigt berg A (34 rader) | Rundat berg A (32 rader) | mirror |
| 4 | Berg | Spetsigt berg B (34 rader) | Rundat berg B (32 rader) | repeat |
| 5 | Dröm | Spiral A (42 rader) | Portal A (40 rader) | mirror |
| 6 | Dröm | Spiral B (42 rader) | Portal B (40 rader) | repeat |
| 7 | Natt | Mur A (40 rader) | Ruin A (38 rader) | mirror |
| 8 | Natt | Mur B (40 rader) | Ruin B (38 rader) | repeat |

## Byteproveniens

- PR60 fryst baseline commit: `2af9855fbe8d3edbe6d01609d3e539547b744aef`; ROM SHA256 `3977c1e04e2cb5a43944e32477b8fa6f443bff270e3af8db4ae3d25e497b9647` **(den gamla ROM:en, inte en ny körning)**.
- Revision 1 grafikcommit `bd18c41fc24e56759d13a182dceea6e4932eb16b`, oförändrad; ursprunglig R1 PF1 data SHA256 `deba82b22fae37567f885a90e4ea4a862e893d3be1f91653c21c8ef53d3c824e`.
- Revision 2 PlayPF1 **768 bytes** SHA256 `253bd7180259cf699a4315379b900ca47801ae6259f0955a002bc601f5ef98f8`; 451 ändrade byte mot R1 och 458 mot PR60 original PF1.
- Alla bitmasker och samtliga PNG-renderingar kommer från EXAKT samma 768 byte som `_PLAYFIELD_DATA.asm`. Kontrollera med `09_GENERATOR/rebuild.py` efter behov; assertions av längd, parser och navigationsmodell.

## Visuell självgranskning (16 motiv)

1. Skog: barrträd A/B bredare och nivåsluttande triangulära kronor, ordentligt smala stammar; lövträd A/B rundare större kronor och kortare stammar.
2. Berg: spetsar A/B har två tydliga stegsluttningar, rundare berg har kompakt slätare topp och låg bred kropp.
3. Dröm: spiraler A/B statiska och avsiktligt tvåradigt upprepade för att se kvadratiska ut; portaler A/B har bred båge med negativ öppning i mitten. PF-bitbredden begränsar fortfarande inre slingdetaljer.
4. Natt: breda murkrön med skilda tinnar; ruiner varierar höjd på varje sidopelare och faller mot en låg, bred grund.
5. Placering: överst och nederst tydliga kantmarginaler. Öppen centrumyta; inget motiv inverterat. Åtta grupper använder olika bitmasker även inom samma värld.

## Kollisionsanalys och kvarstående osäkerhet

- Alla 8 banor har **fyra separata konservativa AABB-förslag**, baserade på synlig faktiska masker och nuvarande mirror/repeat. Befintliga bank0 `WorldRects` matchar inte exakt och har INTE modifierats.
- Source-only BFS på spelarcentrum med L3 half-width=16 och half-height=18 anger sammanhängande rörelseområde från (80,88) i samtliga 8 arenor, under denna enkla axeljusterade rektangelmodell. Det är **inte** ett bevis på fysisk 8-vägs rörelse, diagonalglid, orb-säkerhet, fiendeplacering eller verkliga Stella-kollisioner.
- Portaler och spiraler innehåller synliga hål som omsluts av konservativa solida rektanglar. Detta är en estetik/soliditet-kompromiss att MAIN måste välja vid separat ROM-integration; spelmotorn är oförändrad.
- Halo-testmodell B: all PF blir guldfärgad när halo aktiv; GPU/ROM begränsar synlig full 360° ring. SOURCE_ONLY guldbilder är en PF-färgmodell, inte ett bevis på rörlig ring.

## Nästa steg (endast rekommendation)

MAIN V godkänner eventuellt konst. Därefter separat ROM DEVELOPMENT-uppdrag för att byta de 768 databyten i bank3 och eventuellt de 128 WorldRects-byten i bank0. Kör verklig DASM/Stella NTSC, äkta ban- och kollisionsspeltest L3, 262 scanlines, beamdeadlines, och mot aktuell gameplay-Halo. Ingen fryst sprite eller canon ändras av denna grafikleverans.

**STOP: GRAPHICS II, SOURCE_ONLY_REVISION2, ingen implementationsorder.**
