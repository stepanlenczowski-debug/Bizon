import pygame

# Inicializace
pygame.init()
WIDTH, HEIGHT = 600, 600
SQ_SIZE = WIDTH // 8

# Barvy
WHITE, GREEN = (235, 235, 208), (119, 148, 85)
HIGHLIGHT = (186, 202, 68, 100) # Poloprůhledná žlutá

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

def draw_board(selected_sq):
    for r in range(8):
        for c in range(8):
            color = WHITE if (r + c) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            
            # Zvýraznění vybraného pole
            if selected_sq == (r, c):
                s = pygame.Surface((SQ_SIZE, SQ_SIZE))
                s.set_alpha(150) # Průhlednost
                s.fill((255, 255, 0))
                win.blit(s, (c * SQ_SIZE, r * SQ_SIZE))

def draw_pieces():
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece:
                # Bílé jsou velká písmena, černé malá
                color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                txt = font.render(piece, True, color)
                rect = txt.get_rect(center=(c * SQ_SIZE + SQ_SIZE//2, r * SQ_SIZE + SQ_SIZE//2))
                win.blit(txt, rect)

def main():
    run = True
    selected_sq = None # První klik (r, c)
    turn = "white"    # Začíná bílá (velká písmena)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                c, r = event.pos[0] // SQ_SIZE, event.pos[1] // SQ_SIZE
                
                if selected_sq:
                    # --- LOGIKA PŘESUNU ---
                    start_r, start_c = selected_sq
                    piece = board[start_r][start_c]
                    
                    # Kontrola, zda hráč netlačí na stejné políčko
                    if (start_r, start_c) != (r, c):
                        # Provedeme tah v matici
                        board[r][c] = piece
                        board[start_r][start_c] = ""
                        # Přepneme tah (velmi zjednodušeně)
                        turn = "black" if turn == "white" else "white"
                    
                    selected_sq = None # Resetujeme výběr
                else:
                    # --- LOGIKA VÝBĚRU ---
                    if board[r][c] != "":
                        # Kontrola, zda klikáme na svoji figurku
                        is_white = board[r][c].isupper()
                        if (is_white and turn == "white") or (not is_white and turn == "black"):
                            selected_sq = (r, c)

        draw_board(selected_sq)
        draw_pieces()
        pygame.display.flip()

    pygame.quit()

main()