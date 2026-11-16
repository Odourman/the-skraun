# THE SKRAUN — Visuell riktning för spelarkaraktären (16 november 2026)

**Status:** Användarbekräftad riktning för motiv, kamera, kulör och animation. De exakta TIA-pixelmaskerna är fortfarande tekniska prototyper, inte slutgodkänd karaktärsgrafik.

## Referens och källordning

1. Användarens egen handritade Skraun (16 november 2026) visar kroppens kännetecken: huvud med två öron/horn, två ögon, mun, utsträckta främre armar/framben och två längre bakben med stora fötter. Pilarna i teckningen anger vilka lemmar som ska röra sig.
2. Användaren förtydligade uttryckligen att **spelet visas rakt uppifrån**. Teckningen är anatomisk/designmässig referens, **inte ett godkännande av framifrån-kameravinkeln** i tidigare AI-konceptgrafik.
3. Användaren gillade ljusgrått. **Ljusgrå Skraun** ersätter grön testkulör. Den gröna bågskytten förblir grön; halon planeras guldfärgad. Färgens NTSC-värde behöver bekräftas i Stella och mot alla fyra världars bakgrunder.
4. Användaren bad om **mycket kort, tvåstegs gånganimation**: främre armarna/frambenen **viftar fram och tillbaka** medan bakbenen rör sig. Två poser (A och B), inte en lång animation.
5. **Endast två horisontella vändningar:** högerpose och dess spegelvända vänsterpose. Ingen separat sprite ritad för att vara vänd uppåt eller nedåt. Joystick kan fortfarande gå i åtta riktningar. Att behålla senast vald horisontell orientering under uppåt-/nedåtrörelse är ett tekniskt förslag, inte ett nytt spelregelbeslut.

## Avstämning mot de 60 spelbesluten

Det tidigare beslutet om en symmetrisk, fyrbent trollfigur sedd uppifrån kvarstår som grunddesign. Armarna i skissen tolkas i den spelbara overhead-silhuetten som främre lemmar, och benen som bakre lemmar. På denna extremt lilla spelarsprite kan varje anatomisk detalj inte ritas bokstavligt utan att silhuetten förlorar läsbarhet.

Beslut 46 (åtta rörelseriktningar), 47 (tre nivåstorlekar), och 49 (intryckt eldknapp kan upprepa attack) ändras **inte**. Bara den visuella orienteringen är tvådelad.

## Tekniska avvägningar

- P01:s första gröna 8×12-bitmap är en **tillfällig testfigur**, inte godkänd slutdesign. Det krävs inte en designändring av halon för att testa grå sprite.
- Experimentet `experiments/p01_skraun_gray_topdown.asm` i grenen `experiment/gray-topdown-skraun` använder en 8×12-bitmap med två gångposer A/B, vardera i vänster-/högervänd variant. Två riktningar skapas genom **exakt bitvis horisontell spegling**, ingen ny upp-/nedritning.
- Stora nivåer testas först med TIA `NUSIZ0` (1×/2×/4× bredd) och ROM-radrepetition (12/24/36 scanlines). På nivå 3 blir formen grovkornig; det är en verifieringsfråga, inte slutligt godkänd grafik.
- Föreslagen NTSC-färg `COLUP0=$0C` (ljus neutralgrå) behöver testas för kontrast i skog, berg, dröm och natt.
- Endast P0 används till den här grafikprototypen. P02-B2:s playfield-ring är ännu ett **separat** experiment; ingen sammanslagen rörlig halo har verifierats.
- Originalfoto lagras i projektets Google Drive-mapp, **inte i det publika GitHub-repot**, eftersom det är användarens originalteckning.

## Verifieringspunkter före att sprite ersätter P01

1. Kontrollera de fyra bitmaptabellerna (A/B höger/vänster) och exakt spegelvändning.
2. Bygg 4 KiB NTSC-ROM reproducerbart med DASM, notera SHA-256.
3. Få riktiga Stella-bilder av alla tre storlekar i ljusgrått.
4. Verifiera att joystick ger rörelse även upp/ner, men bara vänster-/högerorientering, att armar och ben byter pose, och att figuren inte klipps vid skärmkanterna.
5. Mät NTSC-scanlines och 6502-cykler, helst i riktig Stella Debugger.
6. Kontrollera användarens estetiska acceptans för en tydlig overhead-silhuett innan grafikändringen slås ihop med huvudgrenen.

**Ingen av dessa egenkontroller är oberoende verifiering. P01-grinden är fortfarande öppen och P02-B3 är planerad, inte implementerad.**

## Projektlänkar

- GitHub: https://github.com/Odourman/the-skraun
- Visuell referens: https://drive.google.com/file/d/1c5denehs2Cd3TT64enzj5Uq32zCTNPh-/view
- Projektets tecknings-/spritesamling: https://drive.google.com/drive/folders/1udBPud9jpVzvMevcgKL8duib94GyV_yJ
- P01 oberoende verifiering: https://github.com/Odourman/the-skraun/issues/1

## MAIN II — SENARE ANVÄNDARKORRIGERING: SPELPLAN UPPIFRÅN, TROLL UPPRÄTT (2026-11-16)

**Högre prioritet än tidigare P1/P2-anatomitolkning:** Användaren har explicit korrigerat att **spelbilden är uppifrån men Skraun ska alltid stå UPPRÄTT, aldrig ligga ner med horisontell kropp**. Det råder ingen automatisk skillnad i joystickrörelser: bara två visuella facing-varianter (höger och dess exakta vänsterspegel); upp/ned-förflyttning behåller en av dessa och roterar aldrig figuren. Trollets huvud/horn, ögon/mun längst upp; armar från överkroppen åt sidorna och ben/fötter nedåt i spritebilden. Ett **stiliskt läsbart framåtriktat ansikte är förenligt med overhead-spelplanen**, och behöver inte avvisas med krav på fotorealistiskt uppifrånperspektiv på trollets ansiktsplan. Detta är ingen ändring till sidokamera eller liggande sprite.

Tidigare formuleringen "fyrfotat"/fyrbent kan inte längre användas för att kräva fyra tassar kring en horisontell rygg. Användarens nya klargörande gäller **figurens visuella anatomi**, utan att ändra ursprungligt beslut 01:s haloattack eller övriga beslut 01–60. De gamla dokumenten/experimenten förblir historiskt intakta; ändringar av själva spelregler kräver separat beslut. Originalteckningen är fortfarande privat i Google Drive.

**GRAPHICS P3:** Två nya upprätta 8×12-kandidater U1/U2 är granskade som reproducerbara **designförhandsvisningar**, ej Stella. **U1 är preliminär visuellt föredragen referens** eftersom den bevarar horn/ögon/mun bättre; dess spegelvändningar har dokumenterade bitmässiga skillnader men uppfattningsbar höger/vänster-vändning i faktisk spelstorlek är ännu inte godkänd. U2 har mer detaljerade armar/ben men svagare ansikte. Varken U1, U2 eller äldre Q1 är slutgodkänd. P1-A/P2:s liggande/horisontella kropp får bara användas som **negativ kontroll** för anatomisk feltolkning. Inga nya sprites, ROM, spritedimensioner eller verifieringssteg auktoriseras genom denna statusändring.

[MAIN II:s fullständiga P3-beslut](MAIN_II_GRAPHICS_P3_UPRIGHT_USER_CLARIFICATION_REVIEW_AND_DECISION_2026-11-16.md). [P3-designkälla](https://github.com/Odourman/the-skraun/tree/graphics/p3-upright-overhead-character-proof-20261116/graphics/skraun_p3_upright_overhead). Visuell grind [#15](https://github.com/Odourman/the-skraun/issues/15) kvarstår OPEN.


## SENARE ANVÄNDARBESLUT — UPPRÄTT U1-FIX1 ÖVERDEL RÄTT, GETLIKNANDE BEN ÖNSKAS (2026-11-16)

Efter att ha sett U1-FIX1 med rättad huvudpixel och två befintliga GIF-poser sade användaren uttryckligen: **"Övre delen är perfekt nu. Men det hade varit bra om benen rörde sig lika bra, som att den går med getben. Ben som en get har."** Alltså **bevara nuvarande U1-FIX1 övre del**; det är ett användarpositivt delbesked, **inte** acceptans av hela spelarspriten eller löst uppfattad gångriktning. Det konkreta nya formmålet gäller **två upprätta getlika bakben med vinklad has och hovform**, som alternerar i A/B-steget under den redan gillade överdelen. Figuren skall inte göras horisontell/fyrbent, och endast horizontal L/R spegelvändning gäller fortfarande.

[MAIN II separata källgrafikuppdrag U1-LEG1](../handoff/MAIN_II_TO_GRAPHICS_U1_LEG1_CAPRINE_GAIT_SOURCE_ONLY_AUTHORIZED_2026-11-16.md) är snävt avgränsat till **lägsta tre pixelraderna y9–11 i 8×12 U1-FIX1**, med y0–8 frysta för båda poser. Om gethas/hov inte kan synas med tre rader skall uppdraget avslutas med NEGATIVT designresultat, inte mer zoom, större sprite, extra bildrutor eller ROM-kod. [Issue #22](https://github.com/Odourman/the-skraun/issues/22) OPEN, [visuell gate #15](https://github.com/Odourman/the-skraun/issues/15) OPEN. Inga produktionsformat eller hardware gates ändrade.


## SENASTE ANVÄNDAR-GODKÄNNANDE: U1-LEG1 NIVÅ 1 OCH OMVÄND GÅNG-RIKTNINGSETIKETT (2026-11-16)

Användaren har sett de faktiska U1-LEG1 två-rutors getbens-GIF:arna först med tidigare riktningsetiketter (användaren uppfattade "Höger" som vänster och "Vänster" som höger), därefter **exakt samma pixelanimationer med etiketter bytta**. Användaren bekräftade uttryckligen: **"Ja, nu är det perfekt. Exakt så här bör den se ut. Fast vilken nivå är den på? 1,2 eller3?"** Detta är därmed ett **POSITIVT ANVÄNDAR-GODKÄNNANDE av nivå-1-figurens UTSEENDE och benanimation i den ommärkta riktningskopplingen**, inte godkännande av andra storlekar, färg/miljö i autentisk Stella eller spelmekanisk implementation.

**Frys för framtida grafisk referens:** U1-LEG1 [exakt 8×12 A/B source](https://github.com/Odourman/the-skraun/blob/graphics/u1-leg1-caprine-gait-20261116/graphics/u1_leg1/SOURCE_U1_LEG1.json), två A/B poser, uppåtriktat hornhuvud, godkänd överdel och skiftande getlika ben, ljusgrå, SPEGLAD L/R. Högervänd VID VISNING och i framtida mappning = **U1-LEG1:s tidigare LEFT-data**; vänstervänd = **tidigare RIGHT-data**, båda med ursprungliga A/B-pixlar. **INGEN bitmapcell byts** och arkivversionerna lämnas orörda. Det är en riktningstolkning/nomenklatur, inte en redan genomförd ROM-ändring. Gångens faktiska förflyttning i 8-riktnings-joystick, Stella eller runtime inte här bevisad.

**Gällande storleksplan:** Level 1 = **8×12 (nu användar-godkänd som design)**; Level 2 = konceptuell **16×24**; Level 3 = konceptuell **32×36** (horisontellt P0 x1/x2/x4, vertikalt radrepetition x1/x2/x3). Varken L2 eller L3 har godkänts med den nya U1-LEG1-animationen och ingen ROM körts; nivå 3 har dessutom oavklarad ART1 #19 första rasterrad. Visuell global grind [#15](https://github.com/Odourman/the-skraun/issues/15) FORTFARANDE ÖPPEN för fiender, världar, två högre nivåer och riktig hardware-/spelrendering. Ingen merge, ROM/Stella, ytterligare grafikversion eller VERIFICATION implicit auktoriserad.

## NYTT UTTRYCKLIGT ANVÄNDARBESLUT – SAMMA U1-LEG1 PÅ NIVÅ 1, 2 OCH 3, ENDAST STORLEKEN ÄNDRAS (2026-11-16)

Användaren bekräftade efter godkännandet av U1-LEG1 nivå 1: **"Ok, ja nivå 2 och tre ska se likadan ut men de ska vara större."**

**Bindande grafisk regel:** ALLA TRE nivåer ska utgå från **exakt samma slutligt användargillade U1-LEG1 8×12 källpixelmasker** och de två ursprungliga A/B-gångposerna. Inga nya detaljer, ny pixelteckning, nytt ansikte, nya getben, nya gångposer, andra proportioner avsiktligt eller alternativa sprites per nivå. Bevara ljusgrå färg och samma spegelvända riktningar, med den av användaren GODKÄNDA omvända kopplingen: framtida VISUELL HÖGER = LEG1-källans tidigare LEFT-data, framtida VISUELL VÄNSTER = tidigare RIGHT-data. Det är en grafik-/presentationsregel, inte bevis på implementerad joystick- eller runtime-koppling.

Den redan dokumenterade **preliminära** storleksmappningen för ROM-prototyper får vara utgångspunkt (nivå 1: **8×12**, nivå 2: **16×24** genom 2× horisontellt och 2× rasterradrepetition; nivå 3: **32×36** genom 4× horisontellt och 3× rasterradrepetition). Dessa dimensioner är **tekniska koncept/ej godkänt maskinrenderat resultat**. Särskilt nivå 3 har **x4 men y3**, vilket kan ge andra uppfattade proportioner än en verkligt likformig skalning. Om det syns ska MAIN tydligt redovisa problemet och få ett särskilt beslut om metod/kompromiss; förvräng inte källfiguren eller lägg till detaljer på eget initiativ. #19 nivå-3-förstaradsfel är fortfarande ÖPPET.

**Användarbeslutets räckvidd:** identisk DESIGN för alla levels, **inte** ett separat visuellt PASS av L2/L3 i autentisk Stella, inte en ROM-implementationsorder, ingen merge och ingen full [visuell kvalitetsgrind #15](https://github.com/Odourman/the-skraun/issues/15) PASS. R3 fullscen NO-GO, [#19](https://github.com/Odourman/the-skraun/issues/19) och P01 oberoende [#1](https://github.com/Odourman/the-skraun/issues/1) förblir öppna. Ingen ny grafikversion, storleksmodifiering, ROM/STELLA, ART1-reparation eller Verification auktoriseras av enbart detta visuella beslut.
