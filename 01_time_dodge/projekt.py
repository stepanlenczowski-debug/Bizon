"""Time Dodge - jednoduchá hra v Pygame.

Tento modul obsahuje hlavní smyčku a pomocné funkce pro hru,
včetně spawnování střel, logiky "time stop" a zvyšování obtížnosti.
"""

import pygame
import random
import sys

# Inicializace pygame
pygame.init()

# Nastavení obrazovky a času
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 24)

# Barvy
WHITE, RED, BLUE, BG = (240, 240, 240), (255, 80, 80), (80, 150, 255), (20, 20, 30)

# Herní konstanty
MAX_TIME_ENERGY, START_SPAWN_TIME, MIN_SPAWN_TIME, DIFFICULTY_STEP = 180, 400, 150, 5000
BULLET_EVENT = pygame.USEREVENT + 1

# Globální proměnné (budou inicializovány v reset_game)
player = bullets = time_energy = time_active = score = spawn_time = last_difficulty_tick = None


def reset_game():
    """Nastaví počáteční hodnoty pro novou hru.

    Inicializuje pozici hráče, seznam projektilů, energii pro time-stop,
    skóre a časovač pro spawnování.
    """
    global player, bullets, time_energy, time_active, score, spawn_time, last_difficulty_tick
    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 30, 30)
    bullets, time_energy, time_active, score = [], MAX_TIME_ENERGY, False, 0
    spawn_time, last_difficulty_tick = START_SPAWN_TIME, pygame.time.get_ticks()
    pygame.time.set_timer(BULLET_EVENT, spawn_time)


def spawn_bullet():
    """Vygeneruje 1-4 nepřátelské střely náhodně po stranách obrazovky.

    Každá střela má náhodnou rychlost a velikost. Střely jsou reprezentovány
    jako `[rect, (vel_x, vel_y)]` a ukládány do globálního `bullets`.
    """
    for _ in range(random.randint(1, 4)):
        side = random.choice(["top", "bottom", "left", "right"])
        speed, size = random.randint(3, 5 + score // 600), random.randint(8, 16)

        if side == "top":
            rect, vel = pygame.Rect(random.randint(0, WIDTH), -size, size, size), (0, speed)
        elif side == "bottom":
            rect, vel = pygame.Rect(random.randint(0, WIDTH), HEIGHT + size, size, size), (0, -speed)
        elif side == "left":
            rect, vel = pygame.Rect(-size, random.randint(0, HEIGHT), size, size), (speed, 0)
        else:
            rect, vel = pygame.Rect(WIDTH + size, random.randint(0, HEIGHT), size, size), (-speed, 0)

        bullets.append([rect, vel])


def game_over_screen():
    """Zobrazení obrazovky po konci hry a čekání na restart nebo ukončení."""
    while True:
        WIN.fill(BG)
        for text, y in [
            (FONT.render("GAME OVER", True, RED), HEIGHT // 2 - 50),
            (FONT.render(f"Score: {score}", True, WHITE), HEIGHT // 2 - 10),
            (FONT.render("SPACE = restart | ESC = konec", True, WHITE), HEIGHT // 2 + 30),
        ]:
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        CLOCK.tick(60)


def main():
    """Hlavní herní smyčka.

    Zpracovává události, pohyb hráče, update projektilů, kolize a vykreslování.
    """
    global time_energy, time_active, score, spawn_time, last_difficulty_tick
    reset_game()
    running = True

    while running:
        CLOCK.tick(60)
        WIN.fill(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == BULLET_EVENT and not time_active:
                spawn_bullet()

        keys = pygame.key.get_pressed()

        # Pohyb hráče (4 směry)
        for key, dx, dy in [
            (pygame.K_a, -5, 0),
            (pygame.K_LEFT, -5, 0),
            (pygame.K_d, 5, 0),
            (pygame.K_RIGHT, 5, 0),
            (pygame.K_w, 0, -5),
            (pygame.K_UP, 0, -5),
            (pygame.K_s, 0, 5),
            (pygame.K_DOWN, 0, 5),
        ]:
            if keys[key]:
                player.x += dx
                player.y += dy
                break
        player.clamp_ip(WIN.get_rect())

        # Time stop
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and time_energy > 0:
            time_active, time_energy = True, time_energy - 1
        else:
            time_active = False
            if time_energy < MAX_TIME_ENERGY:
                time_energy += 1

        # Zvyšování obtížnosti
        now = pygame.time.get_ticks()
        if now - last_difficulty_tick > DIFFICULTY_STEP:
            spawn_time = max(MIN_SPAWN_TIME, spawn_time - 70)
            pygame.time.set_timer(BULLET_EVENT, spawn_time)
            last_difficulty_tick = now

        # Pohyb a kontrola střel
        for bullet in bullets[:]:
            rect, vel = bullet
            if not time_active:
                rect.x += vel[0]
                rect.y += vel[1]

            if rect.colliderect(player):
                running = False

            if rect.x < -30 or rect.x > WIDTH + 30 or rect.y < -30 or rect.y > HEIGHT + 30:
                bullets.remove(bullet)

            pygame.draw.rect(WIN, RED, rect)

        pygame.draw.rect(WIN, WHITE, player)
        pygame.draw.rect(WIN, BLUE, (20, 20, time_energy, 15))
        WIN.blit(FONT.render(f"Score: {score}", True, WHITE), (20, 45))

        if not time_active:
            score += 1

        pygame.display.update()

    game_over_screen()


if __name__ == "__main__":
    # Nekonečná smyčka - hrají se jednotlivé hry za sebou
    while True:
        main()
