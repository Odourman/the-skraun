# THE SKRAUN – GRAPHICS v0.3: MAIN:s estetiska beslutsunderlag

**SLUTLIG KONCENTRERAD GRAFIKFÖRFINING.** Ej MAIN-godkänd slutgrafik, ej Stella. Inga programmerings- eller implementationssteg auktoriserade.

## 1. Huvudpersonen – beslutströskeln

| Version | Målsättning | Bedömning |
| --- | --- | --- |
| v0.2 C-overhead | Färre ansiktsdrag, utsträckta lemmar | Fortsatt frontfigur. Referens, inte godkänd. |
| v0.3 Q1 – utspridda tassar | Fyra sidobaserade tassar/ben, något större kroppen, två synliga steg | Bäst av v0.3-försöken i fyrbent läsbarhet, men ser fortfarande ut som humanoid/ansiktsfigur vid nivå 1. Inte godkänd. |
| v0.3 Q2 – lång rygg | Mer framträdande avlång torso, separat fram- och bakbensregion | Svagare liten skala; kan uppfattas som ett lodrätt spöke. Inte godkänd. |
| v0.3 separat 8×14 | Två extra logiska höjdrader med tydligare avstånd mellan fram- och bakben | **Ej produktionsförslag**. Kräver separat MAIN-beslut och kernelbudgetprövning. Inte heller säkert att detta räcker. |

**Rekommendation:** Ingen 8×12-spelarbitmap ska slutgodkännas ännu. Om MAIN ändå måste utse en visuell testbas, använd **Q1**; behåll C-overhead och Q2 som jämförelsematerial. Fortsätt inte med små pixeljusteringar i v0.4 utan separat beslut om dimensionsram eller förenklad anatomi.

Q1 ändrar 10 A/B-pixlar (6 i främre lemmarnas rader, 4 i bakben). Q2 ändrar 12 (4 främre och 8 bakre). Alla har logisk huvudrad överst och fötter nederst och är exakt vänster/höger spegelvända. Detta är källfilskontroller, inte faktisk Stella-orientering.

## 2. Fiender

Knight idle/raised sword skiljer på **12 bitar**, jämfört med v0.2:s 4. Archer idle/draw skiljer på **11 bitar**, jämfört med tidigare 2. De nya formerna separerar vapenrörelsen mer och grönt mot skog är prövat visuellt i statiskt montage. Även dessa kan fortfarande vara svåra att läsa i äkta spelrörelse. De är inga bevis för acceptabelt P1-flimmer.

## 3. Åtta miljöer

Två PF-layouter per värld, med granskningsbilder i både monokromt och färg. Skog: kronformer/stubbar. Berg: stegade stenåsar. Dröm: öppna brutna spiralruiner (utan att likna haloringens hela krets). Natt: murar och tinnar. Allt speglat kring mittlinjen som 40 PF-celler × 24 × 8-scanline-band. Färgerna är koncept, INTE fastslagna TIA-register.

## 4. Halo

**Endast en ny v0.3-familj** efter 4:3-korrigering. L1 40cc×64 linjer (ratio 1,000); L2 56cc×80 (1,120); L3 72cc×112 (1,029). Maskernas projicerade cirkelform ligger inom MAIN:s ±15%-tolerans; särskilt nivå 3. Fortfarande statisk konturteckning, inte rörlig attack, färglager eller kollisionsradie.

Nivå 3: centrerad 0% av ringmaskens ifyllda clock×scanlinepixlar klipps. Vid centrum x=8 respektive x=152 klipps omkring 40,32%; vid centrum y=12 respektive y=180 omkring 41,94%. Resultaten är exakta på diskret statisk mask i denna modell. Hinder/halo samma PF-cell är **OLÖST**, och kan inte grafiskt trollas bort.

## 5. Tekniska öppna risker och beslut som MAIN måste äga

1. Anatomisk slutacceptans vid 8×12 **ej uppnådd**; 8×14 kostar nya P0-rader: +2 scanlines nivå1, +4 nivå2 och +6 nivå3, fler artbyte och potentiellt ny 6502-kostnad; inget nytt format är auktoriserat.
2. R3 samma-Y fiendeschemaläggning: ungefär 20Hz per fiende. Nytt vapen löser inte det.
3. Halo och hinder konkurrerar om PF-pixelns färg. V0.3-kretsar upphäver inte kollision/overlap.
4. Värsta R3-rasterbudget omkring 2–4 beräknade CPU-cykler; mer detalj kan inte antas gratis.
5. Äkta Stella-, CRT-, PAL- och hardware-prover kräver separat ROM DEVELOPMENT-uppdrag.

**GRAPHICS stannar vid v0.3 enligt MAIN:s order. Issue #15 lämnas öppet, ingen merge, ingen Verification.**
