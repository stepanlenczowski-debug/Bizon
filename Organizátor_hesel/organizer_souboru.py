import os
import shutil

# cesta ke složce, kterou chceš uklidit
slozka = input("Zadej cestu ke složce: ")

# kategorie a přípony
kategorie = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "docs": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx"],
    "videos": [".mp4", ".mov", ".avi", ".mkv"],
    "music": [".mp3", ".wav", ".flac"],
    "archives": [".zip", ".rar", ".7z"],
    "code": [".py", ".html", ".css", ".js", ".java", ".cpp"]
}

# kontrola, jestli složka existuje
if not os.path.exists(slozka):
    print("Tahle složka neexistuje.")
    exit()

# projde všechny položky ve složce
for soubor in os.listdir(slozka):
    puvodni_cesta = os.path.join(slozka, soubor)

    # přeskočí složky, bere jen soubory
    if os.path.isfile(puvodni_cesta):
        nazev, pripona = os.path.splitext(soubor)
        pripona = pripona.lower()

        presunuto = False

        # hledání správné kategorie
        for cilova_slozka, pripony in kategorie.items():
            if pripona in pripony:
                nova_slozka = os.path.join(slozka, cilova_slozka)

                # vytvoří složku, pokud neexistuje
                if not os.path.exists(nova_slozka):
                    os.mkdir(nova_slozka)

                