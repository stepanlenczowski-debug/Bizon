# 01 Time Dodge - Projekt

## Název
Time Dodge

## Cíl projektu
Hra, kde hráč ovládá čtverec a vyhýbá se objek­tům. Cílem je přežít co nejdéle a získat co nejvyšší skóre.

## Popis funkcionality
- Pohyb hráče ve čtyřech směrech.
- Vznikající nepřátelské objekty (střely) ze stran obrazovky.
- Schopnost „zastavení času“ (omezený ukazatel energie).
- Postupné zvyšování obtížnosti.

## Technická část
- Jazyk: Python 3
- Knihovny: `pygame`
- Hlavní soubory: `projekt.py`
- Hlavní algoritmy: náhodné spawnování střel, kolize obdélníků, časovače pro zvyšování obtížnosti.

## User Guide
1. Nainstalujte závislosti:
```
pip install -r requirements.txt
```
2. Spuštění hry:
```
python projekt.py
```
3. Ovládání:
- `A`/`LEFT`: pohyb vlevo
- `D`/`RIGHT`: pohyb vpravo
- `W`/`UP`: pohyb nahoru
- `S`/`DOWN`: pohyb dolů
- `SHIFT` (držený): zastavení času (spotřebovává energii)

## Poznámky pro vývoj
- Přidejte docstringy a komentáře k funkcím.
- Doplňte testy a případně skóre ukládejte do souboru pro přehledy.
