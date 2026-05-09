import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8

WHITE = (235, 235, 208)
GREEN = (119, 148, 85)

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

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

font = pygame.font.SysFont("Arial", 32, bold=True)
clock = pygame.time.Clock()

# ROŠÁDA STAV
white_king_moved = False
black_king_moved = False

white_rook_left_moved = False
white_rook_right_moved = False

black_rook_left_moved = False
black_rook_right_moved = False


def get_valid_moves(r, c):
    moves = []
    piece = board[r][c]

    # PĚŠEC
    if piece.lower() == "p":
        direction = -1 if piece.isupper() else 1

        if 0 <= r + direction < 8 and board[r + direction][c] == "":
            moves.append((r + direction, c))

        if (r == 6 and piece.isupper()) or (r == 1 and piece.islower()):
            if board[r + direction][c] == "" and board[r + 2 * direction][c] == "":
                moves.append((r + 2 * direction, c))

        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc

            if 0 <= nr < 8 and 0 <= nc < 8:
                target = board[nr][nc]

                if target != "" and target.isupper() != piece.isupper():
                    moves.append((nr, nc))

    # VĚŽ
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

    # JEZDEC
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

    # BISKUP
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

    # DÁMA
    elif piece.lower() == "q":
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

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

    # KRÁL + ROŠÁDA
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

        # ROŠÁDA
        if piece == "K" and not white_king_moved:

            if not white_rook_right_moved and board[7][5] == "" and board[7][6] == "" and board[7][7] == "R":
                moves.append((7, 6))

            if not white_rook_left_moved and board[7][1] == "" and board[7][2] == "" and board[7][3] == "" and board[7][0] == "R":
                moves.append((7, 2))

        if piece == "k" and not black_king_moved:

            if not black_rook_right_moved and board[0][5] == "" and board[0][6] == "" and board[0][7] == "r":
                moves.append((0, 6))

            if not black_rook_left_moved and board[0][1] == "" and board[0][2] == "" and board[0][3] == "" and board[0][0] == "r":
                moves.append((0, 2))

    return moves


def draw_board(selected_sq, moves):
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
    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            if piece:
                color = (255, 255, 255) if piece.isupper() else (0, 0, 0)

                txt = font.render(piece, True, color)

                win.blit(
                    txt,
                    (c * SQ_SIZE + SQ_SIZE // 3, r * SQ_SIZE + SQ_SIZE // 4)
                )


def main():
    global white_king_moved, black_king_moved
    global white_rook_left_moved, white_rook_right_moved
    global black_rook_left_moved, black_rook_right_moved

    run = True
    selected_sq = None
    moves = []
    turn = "white"

    while run:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                c = event.pos[0] // SQ_SIZE
                r = event.pos[1] // SQ_SIZE

                if selected_sq:
                    start_r, start_c = selected_sq
                    piece = board[start_r][start_c]

                    if (r, c) in moves:
                        board[r][c] = piece
                        board[start_r][start_c] = ""

                        # ROŠÁDA AKCE
                        if piece == "K":
                            white_king_moved = True

                            if (r, c) == (7, 6):
                                board[7][5] = "R"
                                board[7][7] = ""

                            elif (r, c) == (7, 2):
                                board[7][3] = "R"
                                board[7][0] = ""

                        elif piece == "k":
                            black_king_moved = True

                            if (r, c) == (0, 6):
                                board[0][5] = "r"
                                board[0][7] = ""

                            elif (r, c) == (0, 2):
                                board[0][3] = "r"
                                board[0][0] = ""

                        elif piece == "R":
                            if start_r == 7 and start_c == 0:
                                white_rook_left_moved = True
                            elif start_r == 7 and start_c == 7:
                                white_rook_right_moved = True

                        elif piece == "r":
                            if start_r == 0 and start_c == 0:
                                black_rook_left_moved = True
                            elif start_r == 0 and start_c == 7:
                                black_rook_right_moved = True

                        turn = "black" if turn == "white" else "white"

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

        draw_board(selected_sq, moves)
        draw_pieces()

        pygame.display.flip()

    pygame.quit()


main()