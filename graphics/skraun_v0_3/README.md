# THE SKRAUN – GRAPHICS v0.3, sista avgränsade förfiningen

**Datum:** 2026-11-16. **Status:** PIXELGRAFIK / STATISKA MOCKUPS, INTE Stella, INTE MAIN-godkänd färdig grafik. Ingen ROM-implementation, R4, B3c, merge, gameplayändring eller oberoende VERIFICATION.

## Källor och ordning

- Bindande: MAIN:s [v0.3 arbetsorder](https://github.com/Odourman/the-skraun/blob/main/handoff/MAIN_TO_GRAPHICS_V0_3_OVERHEAD_READABILITY_FINAL_DESIGN_GATE_2026-11-16.md), beslut 01–60 och visuell riktning i `main`.
- Originalteckning: privat Google Drive. Originalfotot ingår **inte** i paketet och har **inte** publicerats på GitHub.
- Bas: autentiskt v0.2 ZIP och source JSON; nya bitmappar är fristående grafikförslag. Samtliga pixelbilder genererade deterministiskt från maskdata i detta paket.

## Filer att börja med

- `01_SKRAUN_TRE_KANDIDATER_PIXELBOARD.png`: tidigare C-overhead samt nya Q1 och Q2, båda A/B och liten rasterstorlek.
- `02_SKRAUN_SILHUETT_SVARTVITT.png`: enfärgade silhuetter och anatomiska rader.
- `03_SKRAUN_TRE_LEVELS_OCH_SPEGLING.png`: P0 nivå 1–3, två poser, båda spegelvändningar, TV-proportioner 4:3.
- `04_SKRAUN_GANGDIFFERENS.png`: ändrade pixlar för armar och bakben.
- `05_FIENDER_VAPEN_TOPDOWN.png`, `06_FIENDER_KONTRAST_ATTACK_AB.png`: svärd och båge, naturlig storlek och förvarning.
- `08_VARLDAR_GRASKALA_8PF.png` och `08_VARLDAR_FARG_8PF.png`: två speglade layouter vardera för skog, berg, dröm och natt.
- `09_HALO_V03_RUND_VS_V01_V02.png`, `10_HALO_V03_CENTRERAD_OCH_4_KANTER.png`: den ENDA nya runda halofamiljen, jämförelse och klippning.
- `12_8x14_TANKEEXPERIMENT_INTE_ROM.png`: förslag som **inte** ingår i den auktoriserade 8×12-formatgrunden.
- `15_ANIMATION_*.gif` och `16_ANIMATION_*.gif`: fyras tvåbilds-animationer i grafisk förhandsvisning.
- `SKRAUN_V03.json`, `ENEMIES_V03.json`, `WORLDS_V03.json`, `HALO_V03.json`: exakta källa-till-bild-masker och metadata.
- `.inc`: assemblerkompatibla bitmaptabeller, **bara grafikdata**, både TOP och BOTTOM med exakt horisontell spegling.
- `verify_graphics_v03.py`: oberoende körbar källdatakontroll, INTE Stella-test.
- `MAIN_DECISION_V03.md`: separat slutlig estetisk rekommendation och återstående blockerare.

## Data- och hårdvarugränser

Alla Skraun- och fiendekandidater är 8×12, logiskt top-first. R3-VFIX:s 177-indexerade, omvända raster-tabell kan **inte** ersättas med 12 `dc.b`-rader direkt. Spelaren kan gå i 8 riktningar, men vi ritar ENDAST horisontella spegelpar och två A/B-poser. Godkända storlekar och attackradier påverkas inte av konstskisser.

PF-maskerna är 40 x 24 celler, 4 color clocks per cell, 8 scanlines per band, reflekterade runt skärmens mitt. **Alla fyra världarna är bara hypotetiska PF-grafiklayouter.** Samma PF-cell kan inte utan annan renderingsmetod ha både självständigt guldfärgad halo och separat färgat hinder. Ingen P1-schemaläggning, P0/P1 samtidighet, extra ram-minne eller rastertiming har bevisats av färgbilderna.

R3-fiender med samma Y syntes 20Hz vardera, de två PF-faserna halo/hinder 30Hz, och värsta rasterlinjerna hade cirka 2–4 beräknade cykler kvar. Dessa tekniska problem är inte lösta.

### HALO-korrektion

För det av MAIN angivna 4:3-approximationen med 160 cc och 192 scanlines antas 1 cc ge 1,6 synliga scanline-enheter i bredd. `1.6 * cc_width / scanline_height` ≈ 1 för rund halo. Maskerna har 40/56/72 cc bredd och 64/80/112 scanlines höjd på nivå 1/2/3, alltså formfaktorer 1,000/1,120/1,029. Tolerans ±15% i denna modell uppfylld för alla tre. **Inga av dessa mått etablerar gameplay attack-räckvidd.** Den ursprungliga statiska nivå3-masken 88×176 scanlines var orimligt hög och R3:s 48×72 var ett separat tekniskt test, inte samma artmask.

### Grafisk slutsats

Q1 erbjuder en tydligare fyra-tassars kropp än v0.2 men **fortfarande inte otvetydigt topdown vid nivå 1**. Q2 är mer avlång men håller inte heller någon estetiskt säker fyrbent topdown-identitet. 8×12-gränsen är därmed **estetiskt EJ GODKÄND av GRAPHICS**. Endast MAIN får besluta om en ny dimension eller kompromiss; 8×14-experimentet tillför +2/+4/+6 scanlines på nivå 1/2/3 och skulle kräva ny RAM-/cykel- och ROM-bedömning. Inte garanterat heller där.

Detta uppdrag är nu avslutat vid v0.3-grinden. Inga fler iterationer föreslås inom befintligt scope.
