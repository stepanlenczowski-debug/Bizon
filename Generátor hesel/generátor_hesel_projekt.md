# Generátor hesel

## Název projektu
Generátor hesel

## Popis a cíl projektu
Cílem je vytvořit jednoduchý konzolový nástroj pro generování bezpečných hesel. Projekt slouží jako cvičení základů Pythonu (funkce, validace, uživatelské rozhraní) a učí bezpečné zacházení s náhodností (modul `secrets`).

## Pro koho je
Pro uživatele, kteří potřebují rychle vygenerovat silné a variabilní heslo pro účty nebo testování.

## Funkcionalita
- Zadání délky hesla (4-128 znaků).
- Volba, zda používat čísla.
- Volba, zda používat symboly.
- Výstup náhodného hesla podle zvolených parametrů.

## Technická část
- Knihovny: `secrets`, `string`.
- Algoritmus: náhodný výběr znaků pomocí `secrets.choice` z definované sady znaků.
- Datové struktury: řetězce.
- No input/output soubory; vše probíhá v konzoli.

## User guide
1. Spusť skript `python generátor_hesel.py`.
2. Zadej požadovanou délku hesla (minimálně 4, max 128).
3. Rozhodni se pro použití čísel (y/n).
4. Rozhodni se pro použití symbolů (y/n).
5. Uvidíš výsledné heslo, které můžeš zkopírovat.

## Bezpečnostní poznámky
- Používá se modul `secrets`, nikoli `random`, pro kryptograficky bezpečné náhodné volby.
- Udržuj donesná hesla v bezpečí a nepoužívej je pro dlouhodobé účty bez další správy hesel.
