# SÖKLOGG, 2026-11-17 (ingen bakgrundsbevakning)

## Verktyg och metod
- Ansluten Google Drive-sökning efter "The Skraun", "SKRAUN RESEARCH", mappar och projektstatus, samt direkt läsning av Google-dokumentet "Aktuell projektstatus", "beslut 01–60" och "MAIN researchaudit". Drive-resultaten kunde läsas. Sökning gav ingen separat RESEARCH-startprompt.
- Ansluten GitHub: direkt hämtning av 9 definierade Skraun-filer, issues #1/#15/#17/#19/#21/#22/#23/#24, öppna PR-sökresultat; äkta källkod i flera externa repositorier. Notera skillnad i historiskt dokument vs nuläge.
- Public web: flera sökomgångar, först brett om multiplexer/HMOVE/PF/kernels; sedan internationella sökningar, spelkodsarkiv, cartridge/kompatibilitet, historisk Venetian. Webbsökträffar användes till att öppna angivna källor där tillgängligt.
- För GitHub-kod genomlästes texten programmässigt och relevanta rader/källkommentarer analyserades. Ingen DASM/Stella-emulering utfördes i denna RESEARCH-leverans.

## Sökfrågor / språk (representativa ordagranna)

ENG: Atari 2600 same scanline different sprites 2 players reuse mid scanline GRP1 NUSIZ trick programming source
ENG: Atari 2600 multi sprite game source code Pac Man 4k Ms Pac Man flicker reduction kernel
ENG: Atari 2600 variable width sprites display list kernel TIA Supercharger DPC+ CDFJ Champ Games
ENG: Atari 2600 cycle exact TIA scanline 76 cycles 128 bytes RAM Stella programmers guide
ENG: Atari 2600 playfield ball missile sprite overlay independent color same scanline examples
ENG: github Atari 2600 homebrew 6502 assembly source cyloid code missile enemies
ENG: github Atari 2600 Adventure / Pitfall / River Raid / Berzerk / Combat disassembly source
ENG: Atari 2600 source code Space Invaders NUSIZ, developers and GitHub
ENG: Atari 2600 8bitworkshop multisprites chapter 28 source 6502
ENG: site:atariage.com "Venetian Blinds" Atari 2600 programming
ENG: Atari 2600 DPC+ CDFJ ARM RetroN 77 compatibility
DEU: Atari 2600 Programmieren mehrere Sprites gleiche Scanline ohne Flackern TIA NUSIZ
DEU: Atari 2600 rasterzeile sprite multiplexing Assembler deutsch forum
FRA: Atari 2600 programmation plusieurs sprites même ligne balayage scintillement noyau
FRA: Atari 2600 ligne scanline sprites programmation français forum
ESP: Atari 2600 programación varios sprites misma línea kernel sin parpadeo
ESP: Atari 2600 kernel asimétrico sprites múltiples espanhol
POR: Atari 2600 programação sprites mesma linha de varredura técnica multiplexação
POR: Atari 2600 truques sprites multiplexação varredura português
ITA: Atari 2600 programmazione sprite multipli stessa linea scansione kernel TIA
ITA: Atari 2600 programmazione kernel gioco assembler italiana scanline
JPN: Atari 2600 同じ走査線 複数 スプライト プログラミング
JPN: Atari 2600 ベネチアンブラインド スプライト 6502 走査線
SWE: Atari 2600 flera sprites samma skanningsrad programmering

## Lässtatus
- Webb öppnade: Stella Programmer's Guide; 8bitworkshop versatile PF + three-stream; AtariAge 2023 flimmertråd; Bumbershoot 2024; Kovi Kovi AtariAge-forum; Stella emulator docs; 8bitworkshop VCS dokumentation. Den historiska AtariAge design-case visades i sökindex men själva öppningsförsöket gav cache miss. Batari multisprite hittades i sökindex men direkt läsning misslyckades. Detta har tydligt markerats.
- Källkod läst direkt via GitHub: Combat 1988 rader, River Raid 3646, Pitfall 3351, Adventure 2797, Raiders 7276, Cyloid 2314, Pacman4K 4868. Specifika etiketter och källhuvuden kontrollerade.
- Kodindex/repo upptäckt men ej djupläst: Space Invaders modern klon, Berzerk disassembly-samling, fler historiska spel, E7-Kovi Kovi-kärnan.

## Falska lösningar och kvarvarande luckor
- Venetian är historiskt real; full fri X/Y plus 3 fiender fortfarande ej visat. Intra-frame raddelning ger kraftig bitmap-degradering.
- En PF-mask kan inte självständigt ge guldhallo och blå hinder i samma pixel/rasteradress bara för att ROM har större tabell.
- Tre-stream minst 64B två dlist om de används enligt Huggs exemplar, krockar med R3 112B; kräver arkitekturell ersättning.
- Inte uppmätt: exakt retrofysisk TIA cykelbudget för varje ny modell, RCA/CRT/LCD-kvalitet, RetroN77 för avancerade mappers, PAL implementation, src-code för Kovi Kovi.
- Ytterligare internationell primary source är en forskningslucka; icke-engelska resultat var oftast sekundära eller otillgängliga. Någon 100%-sökning av samtliga internetarkiv påstås inte ha gjorts.