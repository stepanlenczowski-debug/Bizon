import random
import time

# vytvoření karet (každý symbol je 2x)
karty = ["A", "A", "B", "B", "C", "C", "D", "D"]
random.shuffle(karty)

# seznam, který si pamatuje odhalené karty
odhalene = [False] * len(karty)

# počítání tahů
tahy = 0

# začátek měření času
start = time.time()

# hra běží dokud nejsou všechny karty odhalené
while not all(odhalene):
    print("\nPexeso:")

    # vykreslení aktuálního stavu
    for i in range(len(karty)):
        if odhalene[i]:
            print(karty[i], end=" ")
        else:
            print(f"[{i}]", end=" ")
    print()

    try:
        # výběr karet
        a = int(input("Vyber první kartu: "))
        b = int(input("Vyber druhou kartu: "))

        # kontrola stejné karty
        if a == b:
            print("Musíš vybrat dvě různé karty.")
            continue

        # kontrola rozsahu
        if a < 0 or b < 0 or a >= len(karty) or b >= len(karty):
            print("Neplatná pozice.")
            continue

        # kontrola jestli už není odhalená
        if odhalene[a] or odhalene[b]:
            print("Jedna z těch karet už je odhalená.")
            continue

        # otočení karet
        print(f"Otočil jsi: {karty[a]} a {karty[b]}")
        tahy += 1

        # kontrola shody
        if karty[a] == karty[b]:
            print("Shoda!")
            odhalene[a] = True
            odhalene[b] = True
        else:
            print("Neshoda!")

    except ValueError:
        print("Zadej čísla.")

# konec měření času
end = time.time()
cas = end - start

# výpis výsledku
print(f"\nVyhrál jsi za {tahy} tahů!")

# převod času na minuty a sekundy (vypadá líp)
minuty = int(cas // 60)
sekundy = int(cas % 60)
print(f"Čas: {minuty} min {sekundy} s")
