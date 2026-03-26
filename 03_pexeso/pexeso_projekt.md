# Pexeso Projekt

## 1. Název, Popis a Cíl Projektu

### Název
**Pexeso** - Klasická paměťová hra

### Popis
Projekt implementuje klasickou vzdělávací hru Pexeso pro příkazový řádek. Hra testuje paměť hráče a jeho schopnost zapamatovat si pozice karet.

### Cíl Projektu
Vytvořit jednoduchou, interaktivní hru Pexeso pro jednoho hráče, která běží v konzoli. Cílem je odkrýt všechny páry karet se stejnými symboly s co nejmenším počtem tahů. Hra slouží jako procvičení základních programovacích konceptů včetně seznamů, smyček, podmínek a validace vstupu.

**Pro koho:** Hobbistu či studentům, kteří si chtějí procvičit paměť a zároveň hrát jednoduchou hru v terminálu.

---

## 2. Funkcionalita

### Technické Prvky

- **Inicializace hry:** Vytvoření osmi karet se čtyřmi dvojicemi symbolů
- **Náhodné seřazení:** Zamíchání karet pomocí `random.shuffle()`
- **Vizualizace stavu:** Zobrazení skrytých a odhalených karet
- **Uživatelský vstup:** Hráč volí pozice karet pomocí indexů
- **Logika párů:** Kontrola, zda se dvě vybrané karty shodují
- **Sledování pokroku:** Počítání počtu tahů (každý tah = výběr 2 karet)
- **Ukončení hry:** Automatické skončení, když jsou všechny páry odkryty

### Herní Mechanika

1. Na začátku jsou všech 8 karet skryto
2. Hráč v každém tahu vybere dvě pozice karet (indexy 0-7)
3. Pokud se karty shodují → zůstanou odkryty
4. Pokud se karty neshodují → zůstanou skryty
5. Hra pokračuje dokud nejsou všechny párů odkryty
6. Na konci se zobrazí počet tahů

---

## 3. Technická Část

### Použité Knihovny
- **`random`** - Standardní knihovna Pythonu
  - Funkce `shuffle()` - náhodné zamíchání seznamu na místě

### Datové Struktury

- **`karty` (list)** - Seznam obsahující symboly karet
  - Typ prvků: `list[str]`
  - Délka: 8 prvků (4 páry)
  - Obsah: `["A", "A", "B", "B", "C", "C", "D", "D"]`

- **`odhalene` (list)** - Sleduje stav odkrytí každé karty
  - Typ prvků: `list[bool]`
  - Délka: 8 prvků (odpovídá počtu karet)
  - `True` = karta odkryta, `False` = karta skryta

- **`tahy` (int)** - Počítadlo tahů

### Algoritmy a Logika

#### Validace Uživatelského Vstupu
```
1. Kontrola: pozice <> pozice (nemohou být stejné)
2. Kontrola: index >= 0 a index < 8
3. Kontrola: karta není již odhalena
```

#### Logika Párů
```
IF karty[pozice1] == karty[pozice2]
   THEN odhalene[pozice1] = True, odhalene[pozice2] = True
   ELSE karty zůstanou skryty
```

#### Podmínka Výhry
```
WHILE NOT všechny prvky v odhalene jsou True
   pokračuj v hře
```

### Komplexnost
- Časová složitost inicializace: O(n) - shuffle
- Časová složitost jednoho tahu: O(1) - porovnání dvou prvků
- Prostorová složitost: O(n) - seznamy o délce 8

---

## 4. User Guide (Návod pro Uživatele)

### Spuštění Hry

```bash
python pexeso.py
```

### Jak Hrát

1. **Spusťte program** - Hra se automaticky spustí
2. **Podívejte se na karty** - Zobrazí se síť karet:
   - `[0] [1] [2] [3]` atd. = skryté karty
   - `A B C` atd. = odhalené karty
3. **Vyberte první kartu** - Zadejte index (0-7)
4. **Vyberte druhou kartu** - Zadejte index (0-7)
5. **Systém vám řekne** - Zda se karty shodují:
   - ✓ "Shoda!" = karty zůstanou viditelné
   - ✗ "Neshoda!" = karty se znovu skryjí
6. **Opakujte** dokud nejsou všechny páry odkryty

### Příklad Hry

```
Pexeso:
[0] [1] [2] [3] [4] [5] [6] [7]
Vyber první kartu: 0
Vyber druhou kartu: 2
Otočil jsi: A a C
Neshoda!

Pexeso:
[0] [1] C [3] [4] [5] [6] [7]
Vyber první kartu: 1
Vyber druhou kartu: 4
Otočil jsi: A a A
Shoda!

Pexeso:
A [1] C A [4] [5] [6] [7]
...
```

### Chyby a Jejich Řešení

| Chyba | Příčina | Řešení |\n|---|---|---|\n| "Musíš vybrat dvě různé karty." | Vybrali jste stejný index 2x | Vyberte dvě různé pozice |\n| "Neplatná pozice." | Index mimo rozsah 0-7 | Používejte pouze indexy 0-7 |\n| "Jedna z těch karet už je odhalená." | Vybrali jste již odhalenu kartu | Vyberte skryté karty |\n| "Zadej čísla." | Zadali jste text místo čísla | Zadejte číselný index (0-7) |\n\n### Tipy pro Hráče\n\n- **Zapamatujte si pozice** - Důležité je zapamatovat si, kde jaké karty jsou\n- **Buďte systematičtí** - Odhalujte karty postupně a logicky\n- **Praxe dělá mistra** - S více hrami se budete lépe pamatovat pozice\n- **Cíl:** Odkrýt všechny páry s co nejmenším počtem tahů\n\n---\n\n## 5. Poznámky k Vývoji\n\n### Aktuální Verze\n- Verze 1.0 - Základní hra s 8 kartami (4 páry)\n\n### Možné Rozšíření\n- Zvýšit počet karet (např. 16 = 8 párů)\n- Přidat různé motivy (zvířata, čísla, obrázky)\n- Implementovat více hráčů\n- Přidat difficulty levely\n- Ukládat high scores\n- Grafické rozhraní (pygame)\n"