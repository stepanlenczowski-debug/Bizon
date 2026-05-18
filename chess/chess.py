"""
Jednoduchá šachová hra v Pygame.

Podporuje základní tahy pro všechny figury včetně:
- pěšců, věží, jezdců, střelců, dámy a krále
- proměny pěšce na konci desky
- rošády (pokud jsou splněny podmínky)

Bílé figurky jsou velká písmena, černé malé.
"""

import pygame

pygame.init()
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8

WHITE, GREEN = (235, 235, 208), (119, 148, 85)

# Počáteční nastavení šachovnice
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

# Sledování, zda král nebo věž již provedly tah (potřebné pro rošádu)
white_king_moved = False
black_king_moved = False
white_rook_moved = {0: False, 7: False}  # a1 a h1
black_rook_moved = {0: False, 7: False}  # a8 a h8

win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 32, bold=True)


def is_square_attacked(r, c, attacker_is_white):
    """
    Zjistí, zda pole (r, c) je napadeno protivníkovou figurou.
    """
    enemy_pawn = "P" if attacker_is_white else "p"
    enemy_knight = "N" if attacker_is_white else "n"
    enemy_bishop = "B" if attacker_is_white else "b"
    enemy_rook = "R" if attacker_is_white else "r"
    enemy_queen = "Q" if attacker_is_white else "q"
    enemy_king = "K" if attacker_is_white else "k"

    # Kontrola útoku pěšcem
    pawn_row = r + 1 if attacker_is_white else r - 1
    for dc in (-1, 1):
        pc = c + dc
        if 0 <= pawn_row < 8 and 0 <= pc < 8:
            if board[pawn_row][pc] == enemy_pawn:
                return True

    # Kontrola útoku jezdcem
    knight_moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]
    for dr, dc in knight_moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == enemy_knight:
            return True

    # Kontrola rovných linií pro věž a dámu
    straight_dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in straight_dirs:
        nr, nc = r, c
        while True:
            nr += dr
            nc += dc
            if not (0 <= nr < 8 and 0 <= nc < 8):
                break
            target = board[nr][nc]
            if target == "":
                continue
            if target == enemy_rook or target == enemy_queen:
                return True
            break

    # Kontrola diagonál pro střelce a dámu
    diagonal_dirs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in diagonal_dirs:
        nr, nc = r, c
        while True:
            nr += dr
            nc += dc
            if not (0 <= nr < 8 and 0 <= nc < 8):
                break
            target = board[nr][nc]
            if target == "":
                continue
            if target == enemy_bishop or target == enemy_queen:
                return True
            break

    # Kontrola okolních polí pro útok králem
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] == enemy_king:
                return True

    return False


def get_valid_moves(r, c):
    """
    Vrací seznam všech validních tahů figurky na pozici (r, c).
    """
    moves = []
    piece = board[r][c]

    if piece == "":
        return moves

    # ----------------
    # PĚŠEC
    # ----------------
    if piece.lower() == "p":
        direction = -1 if piece.isupper() else 1

        if 0 <= r + direction < 8 and board[r + direction][c] == "":
            moves.append((r + direction, c))

        if (r == 6 and piece.isupper()) or (r == 1 and piece.islower()):
            if board[r + direction][c] == "" and board[r + 2 * direction][c] == "":
                moves.append((r + 2 * direction, c))

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
    elif piece.lower() == "r":
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            nr, nc = r, c
            while True:
                nr += dr
                nc += dc
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break
                target = board[nr][nc]
                if target == "":
                    moves.append((nr, nc))
                else:
                    if target.isupper() != piece.isupper():
                        moves.append((nr, nc))
                    break

    # ----------------
    # JEDINEC
    # ----------------
    elif piece.lower() == "n":
        knight_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target == "" or target.isupper() != piece.isupper():
                    moves.append((nr, nc))

    # ----------------
    # STŘELEC
    # ----------------
    elif piece.lower() == "b":
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            nr, nc = r, c
            while True:
                nr += dr
                nc += dc
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break
                target = board[nr][nc]
                if target == "":
                    moves.append((nr, nc))
                else:
                    if target.isupper() != piece.isupper():
                        moves.append((nr, nc))
                    break

    # ----------------
    # DÁMA
    # ----------------
    elif piece.lower() == "q":
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            nr, nc = r, c
            while True:
                nr += dr
                nc += dc
                if not (0 <= nr < 8 and 0 <= nc < 8):
                    break
                target = board[nr][nc]
                if target == "":
                    moves.append((nr, nc))
                else:
                    if target.isupper() != piece.isupper():
                        moves.append((nr, nc))
                    break

    # ----------------
    # KRÁL
    # ----------------
    elif piece.lower() == "k":
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dr, dc in king_moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]
                if target == "" or target.isupper() != piece.isupper():
                    moves.append((nr, nc))

        if c == 4 and r in [0, 7]:
            rook_row = r
            for rook_c in [0, 7]:
                rook_piece = "R" if piece.isupper() else "r"
                if board[rook_row][rook_c] == rook_piece and is_castling_possible(rook_row, c, rook_c, piece.isupper()):
                    if rook_c == 0:
                        moves.append((rook_row, c - 2))
                    else:
                        moves.append((rook_row, c + 2))

    return moves


def draw_board(selected_sq, moves):
    """
    Vykreslí šachovnici a zvýrazní vybranou figurku a dostupné tahy.
    """
    for r in range(8):
        for c in range(8):
            color = WHITE if (r + c) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            if selected_sq == (r, c):
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(150)
                s.fill((255, 255, 0))
                win.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

            if (r, c) in moves:
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(100)
                s.fill((0, 0, 255))
                win.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


def draw_pieces():
    """
    Vykreslí figurky na šachovnici.
    """
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece:
                color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                txt = font.render(piece, True, color)
                rect = txt.get_rect(center=(c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2))
                win.blit(txt, rect)


def mark_king_moved(piece):
    """
    Označí krále jako pohybovaného, aby nebyla povolena rošáda.
    """
    global white_king_moved, black_king_moved
    if piece == "K":
        white_king_moved = True
    elif piece == "k":
        black_king_moved = True


def mark_rook_moved(piece, c):
    """
    Označí věž jako pohybovanou, aby nebyla povolena rošáda z její strany.
    """
    global white_rook_moved, black_rook_moved
    if piece == "R" and c in [0, 7]:
        white_rook_moved[c] = True
    elif piece == "r" and c in [0, 7]:
        black_rook_moved[c] = True


def is_castling_possible(king_r, king_c, rook_c, is_white):
    """
    Zjistí, zda je rošáda možná pro daného krále a věž.
    """
    king_moved = white_king_moved if is_white else black_king_moved
    rook_moved = white_rook_moved if is_white else black_rook_moved
    king_piece = "K" if is_white else "k"
    rook_piece = "R" if is_white else "r"

    if king_c != 4 or king_moved or rook_moved[rook_c]:
        return False

    if board[king_r][king_c] != king_piece or board[king_r][rook_c] != rook_piece:
        return False

    start, end = min(king_c, rook_c), max(king_c, rook_c)
    for c in range(start + 1, end):
        if board[king_r][c] != "":
            return False

    if is_square_attacked(king_r, king_c, not is_white):
        return False

    step = 1 if rook_c == 7 else -1
    for i in range(1, 3):
        check_c = king_c + step * i
        if is_square_attacked(king_r, check_c, not is_white):
            return False

    return True


def perform_move(start_r, start_c, end_r, end_c, is_white):
    """
    Provádí tah včetně speciálních tahů jako proměna pěšce a rošáda.
    """
    piece = board[start_r][start_c]

    if piece.lower() == "p" and ((piece.isupper() and end_r == 0) or (piece.islower() and end_r == 7)):
        board[end_r][end_c] = "Q" if piece.isupper() else "q"
        board[start_r][start_c] = ""
    else:
        board[end_r][end_c] = piece
        board[start_r][start_c] = ""

        if piece.lower() == "k" and abs(end_c - start_c) == 2:
            if end_c == 6:
                rook_start_c, rook_end_c = 7, 5
            else:
                rook_start_c, rook_end_c = 0, 3
            rook_piece = board[end_r][rook_start_c]
            board[end_r][rook_end_c] = rook_piece
            board[end_r][rook_start_c] = ""
            mark_rook_moved(rook_piece, rook_start_c)

    mark_king_moved(piece)
    mark_rook_moved(piece, start_c)

    return True


def handle_click(mouse_pos, selected_sq, moves, turn):
    """
    Zpracuje kliknutí myší a provede výběr nebo tah.
    """
    c, r = mouse_pos[0] // SQ_SIZE, mouse_pos[1] // SQ_SIZE

    if not (0 <= r < 8 and 0 <= c < 8):
        return selected_sq, moves, turn

    if selected_sq:
        start_r, start_c = selected_sq
        piece = board[start_r][start_c]

        if (r, c) in moves:
            is_white = piece.isupper()
            perform_move(start_r, start_c, r, c, is_white)
            turn = "black" if turn == "white" else "white"
            selected_sq = None
            moves = []
        elif board[r][c] != "":
            is_white = board[r][c].isupper()
            if (is_white and turn == "white") or (not is_white and turn == "black"):
                selected_sq = (r, c)
                moves = get_valid_moves(r, c)
            else:
                selected_sq = None
                moves = []
        else:
            selected_sq = None
            moves = []
    else:
        if board[r][c] != "":
            is_white = board[r][c].isupper()
            if (is_white and turn == "white") or (not is_white and turn == "black"):
                selected_sq = (r, c)
                moves = get_valid_moves(r, c)

    return selected_sq, moves, turn


def main():
    """
    Hlavní herní smyčka: zpracování událostí a vykreslování.
    """
    run = True
    selected_sq = None
    moves = []
    turn = "white"

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_sq, moves, turn = handle_click(event.pos, selected_sq, moves, turn)

        draw_board(selected_sq, moves)
        draw_pieces()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
