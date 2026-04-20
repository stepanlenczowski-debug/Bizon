# Šachy

## Popis projektu
Cílem projektu je vytvořit jednoduchou vizuální šachovou hru v Pythonu pomocí knihovny `pygame`. Program umožňuje zobrazit šachovnici, vybrat figurku a provést tah mezi políčky. Projekt je určen pro začínající hráče nebo studenty, kteří se učí programování her a práci s událostmi myši.

## Funkcionalita
- Zobrazení šachovnice 8x8 s klasickými barvami políček.
- Kreslení šachových figurek jako textových symbolů (`K`, `Q`, `R`, `B`, `N`, `P` pro bílého a malé písmena pro černého hráče).
- Výběr figurky kliknutím levým tlačítkem myši.
- Provádění tahu změnou pozice figurky v herní matici.
- Střídání tahu mezi bílými a černými figurkami.

## Technická část
- Jazyk: Python
- Knihovna: `pygame`
- Algoritmy:
  - jednoduché zpracování kliknutí myší pro výběr a přesun figurky
  - přepnutí tahu po dokončení přesunu
- Datová struktura:
  - `board` jako seznam seznamů (`list[list[str]]`) reprezentuje aktuální rozmístění figurek na šachovnici
  - každá buňka obsahuje znak figurky nebo prázdný řetězec
- Hlavní funkce:
  - `draw_board(selected_sq)` – vykreslí šachovnici a zvýrazní vybrané políčko
  - `draw_pieces()` – vykreslí figurky podle `board`
  - `main()` – hlavní smyčka hry, zpracování událostí a tahů

## Uživatelský návod
1. Otevři terminál ve složce `Šachy`.
2. Spusť program příkazem:
   ```bash
   python sachy.py
   ```
3. Hra se zobrazí v novém okně.
4. Kliknutím na políčko s figurkou vybereš figurku.
5. Dalším kliknutím na cílové políčko figurku přesuneš.
6. Program střídá tah mezi bílými a černými figurkami automaticky.
7. Okno zavři kliknutím na křížek nebo stisknutím klávesy pro ukončení.

## Omezení a další vylepšení
- Program aktuálně neřeší pravidla šachu, jako jsou:
  - pravidla pohybu jednotlivých figur
  - šach a mat
  - braní figurky a proměna pěšce
- Další možná vylepšení:
  - přidat validaci tahů pro jednotlivé figurky
  - zobrazit skóre nebo stav hry
  - přidat zvukové efekty a animace
