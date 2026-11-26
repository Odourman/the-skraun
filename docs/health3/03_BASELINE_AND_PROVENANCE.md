# Mätbilaga och ROM-register

| Variant | F6 NTSC SHA-256 | Resultat |
|---|---|---|
| baseline | 6db40c950a35cc3ac40c8774664da87b8cf3404d0644936efdc88dfc1189010f | Native DASM återbyggd med exakt PR61-hash |
| color | da7e614721c98e839d2d4886a7ceb4e500259c3f3e41a9881f2986280caa3008 | Färgprov, 9/9 riktade endpoints 262, rörelse bibehållen |
| combined | 63590e8bfe71c447d99b3d923ed2f0db597d4e49438afc7786804ae6bd259dea | Färg och layout, dubbel score i svart förlustvy, 8/8 fångade endpoints 262 |
| locked | 2cba4366b9de5dfc684b57eae6135635e7dbc2d85b1d29790e4ef52f93e9e17c | Referens för rörelselås, X81 i samma FIRE + höger-prov, 8/8 fångade endpoints 262 |
| single | 51975b84655ce8c05939190fa629580522116981c6e41ef0981eebee8215936b | Bästa rörliga experiment-ROM. Svart förlustvy, 296 på vänstra scoreplatsen, 0 pixlar till höger och i arenan. FIRE behåller score $1357, fysisk emulator-F2/RESET gav ny omgång. |

Alla varianter 16 384 byte. Bankarnas egna hashvärden ligger i BANK_USAGE.json i respektive Actions ZIP. Den inkluderade single-ROM:en är exakt den som byggdes i Actions och analyserades i Stella 6.7.1. Förlust/banval är injicerade fixtures och input för FIRE/RESET är emulerad fysisk kontroll. De rörliga FIRE-proven har enbart joystick. ROM-byggare: native DASM på Ubuntu Actions. Scrolla kompileringsloggen i respektive artefakt för exakta sökvägar och DASM-kommandon.

Första Actions [45796680190](https://github.com/Odourman/the-skraun/actions/runs/45796680190) byggde den preliminära ±96-combined, ROM ac90cd6cfda15474df0507e80a31962c65f58b141505b19b17e2e52876f4e8b1. PyAutoGUI kunde inte hitta Xauthority och tog inga giltiga riktade mätningar där. Filen behålls via Actions-artefakten som negativ kontroll av harness och layout.

Korrigerad layout och Xauthority [45797393262](https://github.com/Odourman/the-skraun/actions/runs/45797393262) byggde de fyra första raderna i tabellen. Baseline/combined/locked saknade sparad första idle-session. 8/8 fångade scenendpoints per variant var 262. Color hade 9/9 fångade. Single med separat förlustpoäng [45797813671](https://github.com/Odourman/the-skraun/actions/runs/45797813671) hade 8/8 fångade scenendpoints och en idle med svart X-fångst men utan debuggerlogg. Röd CI i dessa jobbrader är inte ett gameplay-PASS. Råfilerna visar exakt testutfall.

Den separata döds-HUD-rutinen ligger vid FED5. Källräkning från HUD-radens start efter WSYNC placerar första PF1-skrivning vid cykel 7 och första PF2-skrivning vid 19/21. Andra PF1 vid 45/47 och andra PF2 vid 52/54. Vänster PF1 slutar omkring cykel 39, vänster PF2 omkring 49. Höger PF1 börjar omkring 55 och höger PF2 omkring 65. Mätfönstret bekräftas via Stella-bildens ensamma score, och skrivtiderna är en källberäkning. Påverkan på split-kernel och TV-fas ligger inom detta testfönster.

Slutomkörning [45799148213](https://github.com/Odourman/the-skraun/actions/runs/45799148213), kod 20cf1e943c1f4246345441720f3d183389b9e9ad, väntade på en synlig Stella-process innan första kommandot. Samma single-ROM SHA. Samtliga 11 scener fångades med 262-raders slutvärde. 120 individuella frame-steg i naturlig joystick/FIRE-rutt gav 120×262. Start Stage 1/L1, 3 liv, slut Stage 1/L1, 2 liv. Den äldre problemrutten (naturlig scen) fångades vid Stage 1/L2, StageKills=KillsNeed=3, StagePause=17 och ArrowDX=ArrowDY=0 med 262 rader. Det är ett reproducerat kontrollställe efter PR61:s vågslutsrensning. En full per-line trace, fler samtidiga scenarier och lång soak har annan täckning.
