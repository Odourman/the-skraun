# Föreslagen nästa arbetsorder

Verifiera åtkomst till GitHub, Actions, Drive och DASM/Stella. Läs PR62 och hämta exakt PR61 7c189cf03a9f0c836599d81a203e33a3a10ea8cd med SHA-256 6db40c950a35cc3ac40c8774664da87b8cf3404d0644936efdc88dfc1189010f.

1. Bryt ut miljöfärg, motivflytt och svart förlustvy separat. Kör generatorn med PR61:s fyra bankfiler och en variantrot, sedan dess build.py. F6, 16 384 byte och hash per variant. Återställ en felande delpatch till PR61.
2. Gör lokalt COLUPF-fönster runt orbens tomma band. Mät skrivcykel/beam för COLUPF, PF1 och ENABL, både normal- och pilkernel. Kontrollera åtta banor, tre nivåer, orb kvar/tagen, halo av/på och same-Y med P0/P1/M1 vid kantläge. Ta råmask och STL-pixlar. Ett enda feldaterat guldbyte till miljö är FAIL.
3. Använd verklig rutt till förlust med positiv score, svart bild med en läsbar score på ordinarie vänsterplats, FIRE väntar, RESET startar om. Kör 120 uppmätta frame-endpoints och exakta vägen där PR61-föregångaren hade 263 med Stage 1/Level 2 och kvarhängande pil vid vågslut.
4. Prova faktisk joystick och kollision på alla jämna banor, därefter alla 24 kombinationer. Kontrollera motivens orientering, vertikalt byte och tillväxt vid säker orbposition. Jämför minst en full naturlig pendel mot PR61.
5. Kör Ranger neutral/drag/släpp, pil läsbar och svärdshugg efter läsbar pose. 24 konsekutiva bilder för samma-Y och vertikalt åtskilda Y. Bevara tre logiska aktörer. Testa riktad CPU/stacktrace med båda attacker, halo, HUD, ljud och bankreturer.
6. Begär beslut innan permanent stilla halo, världsfärgad halo-orb, ändring av kamouflage eller färre aktiva fiender. Behåll rörelse och guldhalo som grund. Återanvänd ej globalt PF-guld, ±96-layout eller HEALTH-2:s /30-positionerare.

Leverera reproducerbar källpatch, bankhashar, skillnader mellan naturliga och injicerade lägen, råa Stella-fångster och högsta uppmätta SP-djup. Återställning per delpatch.
