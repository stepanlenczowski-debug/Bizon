"""
Simple Chess Game in Pygame

Implements basic moves for all pieces including:
- Pawns, Rooks, Knights, Bishops, Queen and King
- Pawn promotion at the end of the board
- Castling (when conditions are met)

White pieces are uppercase, black pieces are lowercase.
"""

import pygame

pygame.init()
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8

WHITE, GREEN = (235, 235, 208), (119, 148, 85)

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

# Tracking piece movements for castling validation
white_king_moved = False
black_king_moved = False
white_rook_moved = {0: False, 7: False}  # a1 and h1
black_rook_moved = {0: False, 7: False}  # a8 and h8

win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 32, bold=True)


def get_valid_moves(r, c):
    """
    Returns a list of all valid moves for a piece at position (r, c).
    
    Args:
        r (int): Row on the chessboard (0-7)
        c (int): Column on the chessboard (0-7)
    
    Returns:
        list: List of tuples (r, c) representing valid moves
    """
    moves = []
    piece = board[r][c]

    if piece == "":
        return moves

    # ----------------
    # PAWN
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
    # ROOK
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
    # KNIGHT 🐎
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
    # BISHOP
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
    # QUEEN
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
    # KING
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
    Draws the chessboard with color highlighting for selected piece and available moves.
    
    Args:
        selected_sq (tuple): Tuple (r, c) of selected piece or None
        moves (list): List of tuples representing available moves
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
    Draws all pieces at correct positions with proper colors.
    Pieces are centered using rect.center.
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
    Marks a king as moved, preventing castling.
    
    Args:
        piece (str): Piece (K or k)
    """
    global white_king_moved, black_king_moved
    if piece == "K":
        white_king_moved = True
    elif piece == "k":
        black_king_moved = True


def mark_rook_moved(piece, c):
    """
    Marks a rook as moved, preventing castling.
    
    Args:
        piece (str): Piece (R or r)
        c (int): Column (0 for a-file, 7 for h-file)
    """
    global white_rook_moved, black_rook_moved
    if piece == "R" and c in [0, 7]:
        white_rook_moved[c] = True
    elif piece == "r" and c in [0, 7]:
        black_rook_moved[c] = True


def is_castling_possible(king_r, king_c, rook_c, is_white):
    """
    Checks if castling is possible.
    
    Args:
        king_r (int): King's row
        king_c (int): King's column (4)
        rook_c (int): Rook's column (0 or 7)
        is_white (bool): Whether it's white king
    
    Returns:
        bool: True if castling is possible
    """
    king_moved = white_king_moved if is_white else black_king_moved
    rook_moved = white_rook_moved if is_white else black_rook_moved
    
    if king_moved or rook_moved[rook_c]:
        return False
    
    # Check if there are pieces between king and rook
    start, end = min(king_c, rook_c), max(king_c, rook_c)
    for c in range(start + 1, end):
        if board[king_r][c] != "":
            return False
    
    return True


def perform_move(start_r, start_c, end_r, end_c, is_white):
    """
    Executes a move including special moves (pawn promotion, castling).
    
    Args:
        start_r (int): Starting row
        start_c (int): Starting column
        end_r (int): Ending row
        end_c (int): Ending column
        is_white (bool): Whether it's a white move
    
    Returns:
        bool: True if move was executed
    """
    piece = board[start_r][start_c]
    
    # Pawn promotion
    if piece.lower() == "p" and ((piece.isupper() and end_r == 0) or (piece.islower() and end_r == 7)):
        board[end_r][end_c] = "Q" if piece.isupper() else "q"
        board[start_r][start_c] = ""
    else:
        board[end_r][end_c] = piece
        board[start_r][start_c] = ""

        # Castling move: king moves two squares horizontally
        if piece.lower() == "k" and abs(end_c - start_c) == 2:
            if end_c == 6:
                rook_start_c, rook_end_c = 7, 5
            else:
                rook_start_c, rook_end_c = 0, 3
            rook_piece = board[end_r][rook_start_c]
            board[end_r][rook_end_c] = rook_piece
            board[end_r][rook_start_c] = ""
            mark_rook_moved(rook_piece, rook_start_c)

    # Track movements for castling
    mark_king_moved(piece)
    mark_rook_moved(piece, start_c)
    
    return True


def handle_click(mouse_pos, selected_sq, moves, turn):
    """
    Handles mouse click on the chessboard.
    
    Args:
        mouse_pos (tuple): Mouse position (x, y)
        selected_sq (tuple): Currently selected piece
        moves (list): Available moves for selected piece
        turn (str): Current turn ('white' or 'black')
    
    Returns:
        tuple: (new selected_sq, new moves, new turn)
    """
    c, r = mouse_pos[0] // SQ_SIZE, mouse_pos[1] // SQ_SIZE
    
    # Protect against clicking outside the board
    if not (0 <= r < 8 and 0 <= c < 8):
        return selected_sq, moves, turn
    
    if selected_sq:
        start_r, start_c = selected_sq
        piece = board[start_r][start_c]
        
        if (r, c) in moves:
            # Move is valid
            is_white = piece.isupper()
            perform_move(start_r, start_c, r, c, is_white)
            turn = "black" if turn == "white" else "white"
            selected_sq = None
            moves = []
        elif board[r][c] != "":
            # Select different piece
            is_white = board[r][c].isupper()
            if (is_white and turn == "white") or (not is_white and turn == "black"):
                selected_sq = (r, c)
                moves = get_valid_moves(r, c)
            else:
                selected_sq = None
                moves = []
        else:
            # Click on empty square
            selected_sq = None
            moves = []
    else:
        # Select piece
        if board[r][c] != "":
            is_white = board[r][c].isupper()
            if (is_white and turn == "white") or (not is_white and turn == "black"):
                selected_sq = (r, c)
                moves = get_valid_moves(r, c)
    
    return selected_sq, moves, turn


def main():
    """
    Main game loop. Processes events and draws the game.
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
