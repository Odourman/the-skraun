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
