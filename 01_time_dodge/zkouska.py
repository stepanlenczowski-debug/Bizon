"""Time Dodge - jednoduchá hra v Pygame."""

import pygame
import random
import sys

pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 900, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Time Dodge")

CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 24)

# Barvy
WHITE = (240, 240, 240)
RED = (255, 80, 80)
BLUE = (80, 150, 255)
BG = (20, 20, 30)

# Herní konstanty
MAX_TIME_ENERGY = 180
START_SPAWN_TIME = 400
MIN_SPAWN_TIME = 150
DIFFICULTY_STEP = 5000
BULLET_EVENT = pygame.USEREVENT + 1

# Globální proměnné
player = None
bullets = []
time_energy = 0
time_active = False
score = 0
spawn_time = 0
last_difficulty_tick = 0
start_time = 0
survival_time = 0


def reset_game():
    global player, bullets, time_energy, time_active
    global score, spawn_time, last_difficulty_tick, start_time

    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 30, 30)
    bullets = []
    time_energy = MAX_TIME_ENERGY
    time_active = False
    score = 0

    spawn_time = START_SPAWN_TIME
    last_difficulty_tick = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    pygame.time.set_timer(BULLET_EVENT, spawn_time)


def spawn_bullet():
    for _ in range(random.randint(1, 4)):
        side = random.choice(["top", "bottom", "left", "right"])
        speed = random.randint(3, 5 + score // 600)
        size = random.randint(8, 16)

        if side == "top":
            rect = pygame.Rect(random.randint(0, WIDTH), -size, size, size)
            vel = (0, speed)
        elif side == "bottom":
            rect = pygame.Rect(random.randint(0, WIDTH), HEIGHT + size, size, size)
            vel = (0, -speed)
        elif side == "left":
            rect = pygame.Rect(-size, random.randint(0, HEIGHT), size, size)
            vel = (speed, 0)
        else:
            rect = pygame.Rect(WIDTH + size, random.randint(0, HEIGHT), size, size)
            vel = (-speed, 0)

        bullets.append([rect, vel])


def game_over_screen():
    while True:
        WIN.fill(BG)

        minutes = survival_time // 60
        seconds = survival_time % 60

        texts = [
            (FONT.render("GAME OVER", True, RED), HEIGHT // 2 - 70),
            (FONT.render(f"Score: {score}", True, WHITE), HEIGHT // 2 - 30),
            (FONT.render(f"Time survived: {minutes:02}:{seconds:02}", True, WHITE), HEIGHT // 2 + 10),
            (FONT.render("SPACE = restart", True, WHITE), HEIGHT // 2 + 50),
            (FONT.render("ESC = quit", True, WHITE), HEIGHT // 2 + 80),
        ]

        for text, y in texts:
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        CLOCK.tick(60)


def main():
    global time_energy, time_active, score
    global spawn_time, last_difficulty_tick, start_time, survival_time

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

        # Pohyb hráče
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.x += 5
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.y -= 5
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.y += 5

        player.clamp_ip(WIN.get_rect())

        # Time stop
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and time_energy > 0:
            time_active = True
            time_energy -= 1
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

        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        minutes = elapsed // 60
        seconds = elapsed % 60
        WIN.blit(FONT.render(f"Time: {minutes:02}:{seconds:02}", True, WHITE), (20, 75))

        if not time_active:
            score += 1

        pygame.display.update()

    survival_time = (pygame.time.get_ticks() - start_time) // 1000
    game_over_screen()


if __name__ == "__main__":
    while True:
        main()