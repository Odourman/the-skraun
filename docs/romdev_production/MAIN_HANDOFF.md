# The Skraun – slutproduktion till MAIN V

**Spelbar ROM.** `THE_SKRAUN_FINAL_PLAYABLE_CHECKPOINT_NTSC_F6.bin`, standard F6 NTSC, 16 384 byte. SHA-256 `3f5595bfb6b53568882bc08420ea0527e6c9099cf04ae007cca6a9deda67ecd9`. Utkast-PR [#66](https://github.com/Odourman/the-skraun/pull/66).

**Vad som blev färdigt.** Kompakt Skraun på nivå 2 och 3, fyra fasade halomarkörer, rättvis rotation vid lika fiendehot och två av tre faser åt en ensam prioriterad fiende. Bågskytten kontrollerar skottbanan och låser en lutning vid släpp. Pilar kan träffa även ovanför den gamla övre gränsen. Vid livsförlust återplaceras överlevande fiender medan döda förblir döda. Numerisk HUD i ljus färg och ett poängfält, max nio liv och synlig poäng mättad vid 9 999. Nya TIA-effektlängder, svep och en kort avslutningsmelodi för banan.

**Releasegrindar.** Leveransen är `PLAYABLE_CHECKPOINT / DEVELOPER_OBSERVED`. Full pixel- och deadlinekvalificering för alla samtidiga TIA-objekt och alla världar är öppen. I maskjämförelsen återstår fyra L3-bilder åt vänster med oisolerad kropp, samma antal som PR65. Mätta fiendeluckor är avgränsade till testade scener. Den konservativa siktrutan kan avstå från en fri diagonal när rutans hörn träffar ett hinder. Allvärldstest av pilens löpande synlighet, alla osårbarhetsövergångar och full AI-rättvisa före varje träff är öppna. Mänsklig speltest och ljudbedömning samt fysisk Atari/RetroN 77 är ej utförda.

## Resultat och spårbarhet

| Prov | Resultat |
| --- | --- |
| Historisk 264/310-raderssekvens | 634 synkade Stella-bildrutor på 262 lokalt |
| Arkiverad pendelsekvens | 4 401 synkade Stella-bildrutor på 262, med 8 400 poäng, sju liv och L3 vid sista startbesöket |
| Ny kontinuerlig joystickkörning | 16 000 steg över flera pendlar. 15 999 synkade bildrutor på 262, slut på L3 med nio liv och 9 999 på displayen |
| 17 äldre prov | Alla slutpunkter på 262. Förväntade speltillstånd skiljer sig i vissa stridsscener efter ändrad styrning av pil, schema och återplacering |
| Orber och rörelse | 32 upptagningar över båda X per bana, 16 L3-fall där orb ligger kvar, samt 24 riktade ban-/nivåprov med joystick i ROM |
| Halo och projektil | 48 in-/utanförprov för åtta riktningar och tre nivåer. Riktade prov på projektilvektor, övre träffområde, hinder och halointerception |
| Styrd poäng och skada | Fyra prov på 2 000-passering och poängtak, nivåfall och livsförlust i tre prov |
| Förlust och återstart | Naturlig förlust med 900 poäng. Eld höll förlustläget. RESET återställde bana 1, L1, tre liv och noll poäng |
| Inspelning | 126,67 sekunder video, 7 599 aktiva bildrutor i åtta banor, PCM från samma körning. Separat kort utsnitt av förlust/RESET |

Startintervallet i råloggarna föregår första hela VSYNC-perioden och är märkt separat. Avvikelser efter synk framgår i `MEASUREMENTS.json`. Stackprovet loggar SP efter skrivning, med lägsta observerade värde `$F5` i regressionssekvensen. Det är ett provbundet värde. RAM-ägarskap och kvarvarande beamfrågor finns i `TECHNICAL_CHOICES.md`. Godkänd PF1 har SHA-256 `4c52651d7eca55e8e5c5158d33c90bec6bbd4f85e1732e65cf94321cd2b5334d`.

Spela med joystick och FIRE. Se `PLAYER_GUIDE.md` för uppgraderingar, liv och RESET. Byte-identisk DASM-reproduktion beskrivs i `PLAYTEST.md`.
