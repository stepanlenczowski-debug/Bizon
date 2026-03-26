import random

# Vytvoření dvojic karet
# Každá karta má svůj symbol (A-D), každý symbol se opakuje 2x kvůli párům
karty = ["A", "A", "B", "B", "C", "C", "D", "D"]
random.shuffle(karty)

# Seznam odhalených karet - sleduje, které karty už byly spárovány
# False = karta zatím skryta, True = karta byla odhalena a seřadí správně
odhalene = [False] * len(karty)

# Počet tahů (hráč vybírá 2 karty najednou = 1 tah)
tahy = 0

# Hlavní herní smyčka - pokračuje dokud nejsou všechny karty odhalené
while not all(odhalene):
    print("\nPexeso:")
    
    # Výstup aktuálního stavu hry
    for i in range(len(karty)):
        if odhalene[i]:
            # Odhalená karta - zobrazí se symbol
            print(karty[i], end=" ")
        else:
            # Skrytá karta - zobrazí se index pro výběr
            print(f"[{i}]", end=" ")
    print()

    try:
        # Hráč vybírá pozici první karty
        a = int(input("Vyber první kartu: "))
        # Hráč vybírá pozici druhé karty
        b = int(input("Vyber druhou kartu: "))

        # Validace: kontrola že hráč nevolí stejnou kartu dvakrát
        if a == b:
            print("Musíš vybrat dvě různé karty.")
            continue

        # Validace: kontrola že pozice jsou v platném rozsahu
        if a < 0 or b < 0 or a >= len(karty) or b >= len(karty):
            print("Neplatná pozice.")
            continue

        # Validace: kontrola že vybrané karty nejsou už odhalené
        if odhalene[a] or odhalene[b]:
            print("Jedna z těch karet už je odhalená.")
            continue

        # Zobrazí co hráč odkryl
        print(f"Otočil jsi: {karty[a]} a {karty[b]}")
        tahy += 1

        # Kontrola: pokud se karty shodují, zůstanou odhalené
        if karty[a] == karty[b]:
            print("Shoda!")
            odhalene[a] = True
            odhalene[b] = True
        else:
            # Karty se neshodovaly - zůstávají skryté pro další tah
            print("Neshoda!")

    # Chyba: uživatel zadal text místo čísla
    except ValueError:
        print("Zadej čísla.")

# Konec hry - zobrazí počet tahů
print(f"\nVyhrál jsi za {tahy} tahů!")
