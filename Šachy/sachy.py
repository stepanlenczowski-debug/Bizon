import pygame

# Inicializace Pygame
pygame.init()

# Konstanty
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQ_SIZE = WIDTH // COLS

# Barvy
WHITE = (235, 235, 208)
GREEN = (119, 148, 85)
HIGHLIGHT = (186, 202, 68)
BLACK_TEXT = (0, 0, 0)

# Reprezentace figurek (pro ukázku jen pár kusů)
# V reálné hře byste zde měli celou matici 8x8
board_layout = [
    ["r", "n", "b", "q", "k", "b", "n", "r"],
    ["p", "p", "p", "p", "p", "p", "p", "p"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["P", "P", "P", "P", "P", "P", "P", "P"],
    ["R", "N", "B", "Q", "K", "B", "N", "R"]
]

screen = pygame.display.set_caption("Jednoduché Šachy")
win = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("Arial", 32, bold=True)

def draw_board():
    """Vykreslí čtverce šachovnice."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else GREEN
            pygame.draw.rect(win, color, (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def draw_pieces():
    """Vykreslí textové symboly figurek na desku."""
    for row in range(ROWS):
        for col in range(COLS):
            piece = board_layout[row][col]
            if piece != "":
                text_surface = font.render(piece, True, BLACK_TEXT)
                # Vycentrování textu v políčku
                text_rect = text_surface.get_rect(center=(col * SQ_SIZE + SQ_SIZE//2, row * SQ_SIZE + SQ_SIZE//2))
                win.blit(text_surface, text_rect)

def main():
    run = True
    selected_sq = None # Uloží pozici (row, col) po kliknutí

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Získání souřadnic kliknutí
                x, y = pygame.mouse.get_pos()
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                selected_sq = (row, col)
                print(f"Kliknuto na políčko: {row}, {col}")

        # Vykreslování
        draw_board()
        
        # Zvýraznění vybraného políčka
        if selected_sq:
            r, c = selected_sq
            pygame.draw.rect(win, HIGHLIGHT, (c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)
            
        draw_pieces()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()