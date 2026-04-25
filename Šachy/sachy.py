import pygame

# Inicializace
pygame.init()
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8

# Barvy
WHITE, GREEN = (235, 235, 208), (119, 148, 85)

# Startovní rozestavení
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
font = pygame.font.SysFont("Arial", 32, bold=True)


def get_valid_moves(r, c):
    moves = []
    piece = board[r][c]

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
    if piece.lower() == "r":
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
                rect = txt.get_rect(center=(c * SQ_SIZE + SQ_SIZE // 2, r * SQ_SIZE + SQ_SIZE // 2))
                win.blit(txt, rect)


def main():
    run = True
    selected_sq = None
    moves = []
    turn = "white"

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                c, r = event.pos[0] // SQ_SIZE, event.pos[1] // SQ_SIZE

                if selected_sq:
                    start_r, start_c = selected_sq
                    piece = board[start_r][start_c]

                    if (r, c) in moves:
                        board[r][c] = piece
                        board[start_r][start_c] = ""
                        turn = "black" if turn == "white" else "white"

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