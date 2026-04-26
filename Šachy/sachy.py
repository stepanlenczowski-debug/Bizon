# Jednoduchá šachová hra v Pygame
# Implementuje základní pohyby pěšců a věží

import pygame

# Inicializace Pygame a nastavení velikosti okna
pygame.init()
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8

# Barvy pro šachovnici
WHITE, GREEN = (235, 235, 208), (119, 148, 85)

# Startovní rozestavení figurek na šachovnici
# Velká písmena = bílé, malá = černé
# r = rook (věž), n = knight (jezdec), b = bishop (střelec), q = queen (dáma), k = king (král), p = pawn (pěšec)
board = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

# Vytvoření okna a fontu pro text
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 32, bold=True)


def get_valid_moves(r, c):
    """
    Vrátí seznam platných tahů pro figuru na pozici (r, c).
    Implementuje pohyby pro pěšce a věž.
    """
    moves = []
    piece = board[r][c]

    # ----------------
    # PĚŠEC
    # ----------------
    if piece.lower() == "p":
        # Určení směru pohybu: bílí pěšci nahoru (-1), černí dolů (+1)
        direction = -1 if piece.isupper() else 1

        # Normální pohyb o jedno pole dopředu
        if 0 <= r + direction < 8 and board[r + direction][c] == "":
            moves.append((r + direction, c))

        # Dvojitý pohyb ze startovní pozice
        if (r == 6 and piece.isupper()) or (r == 1 and piece.islower()):
            if board[r + direction][c] == "" and board[r + 2 * direction][c] == "":
                moves.append((r + 2 * direction, c))

        # Útoky diagonálně
        for dc in [-1, 1]:
            nc = c + dc
            nr = r + direction
            if 0 <= nc < 8 and 0 <= nr < 8:
                target = board[nr][nc]
                if target != "" and target.isupper() != piece.isupper():
                    moves.append((nr, nc))

    # ----------------
    # VĚŽ
    # ----------------
    if piece.lower() == "r":
        # Směry pohybu: nahoru, dolů, vlevo, vpravo
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r, c

            while True:
                nr += dr
                nc += dc

                # Kontrola hranic šachovnice
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break

                target = board[nr][nc]

                if target == "":
                    moves.append((nr, nc))
                else:
                    # Pokud je cíl soupeřova figura, můžeme ji vzít
                    if target.isupper() != piece.isupper():
                        moves.append((nr, nc))
                    break

    return moves


def draw_board(selected_sq, moves):
    """
    Vykreslí šachovnici s zvýrazněním vybraného pole a možných tahů.
    """
    for r in range(8):
        for c in range(8):
            # Střídavé barvy polí
            color = WHITE if (r + c) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            # Zvýraznění vybraného pole žlutou barvou
            if selected_sq == (r, c):
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(150)
                s.fill((255, 255, 0))
                win.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            # Zvýraznění možných tahů modrou barvou
            if (r, c) in moves:
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)
                s.fill((0, 0, 255))
                win.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def draw_pieces():
    """
    Vykreslí všechny figury na šachovnici.
    Bílé figury jsou bílé, černé černé.
    """
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece:
                # Barva textu: bílá pro bílé figury, černá pro černé
                color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                txt = font.render(piece, True, color)
                # Umístění textu do středu pole
                rect = txt.get_rect(center=(c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2))
                win.blit(txt, rect)


def main():
    """
    Hlavní herní smyčka.
    Zpracovává události, vykresluje hru a střídá tahy.
    """
    run = True
    selected_sq = None  # Vybrané pole (řádek, sloupec)
    moves = []  # Seznam možných tahů
    turn = "white"  # Čí je tah

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Převedení pozice myši na souřadnice šachovnice
                c, r = event.pos[0] // SQ_SIZE, event.pos[1] // SQ_SIZE

                if selected_sq:
                    # Pokud je vybráno pole, zkusíme provést tah
                    start_r, start_c = selected_sq
                    piece = board[start_r][start_c]

                    if (r, c) in moves:
                        # Provedení tahu
                        board[r][c] = piece
                        board[start_r][start_c] = ""
                        # Změna tahu
                        turn = "black" if turn == "white" else "white"

                    # Zrušení výběru
                    selected_sq = None
                    moves = []

                else:
                    # Výběr nového pole
                    if board[r][c] != "":
                        is_white = board[r][c].isupper()
                        # Kontrola, zda je tah na hráči
                        if (is_white and turn == "white") or (not is_white and turn == "black"):
                            selected_sq = (r, c)
                            moves = get_valid_moves(r, c)

        # Vykreslení hry
        draw_board(selected_sq, moves)
        draw_pieces()
        pygame.display.flip()

    pygame.quit()


# Spuštění hry
main()