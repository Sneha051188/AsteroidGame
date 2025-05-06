import pygame
import random
import os

# Setup
pygame.init()
WIDTH, HEIGHT = 600, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Asteroid Game")

# Load Assets
spaceship_img = pygame.image.load("images/spaceship.png")
asteroid_img = pygame.image.load("images/asteroid.png")
bg_music = "sounds/background.wav"
crash_sound = pygame.mixer.Sound("sounds/crash.wav")

pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)

# Constants
WHITE = (255, 255, 255)
FPS = 60
SPACESHIP_WIDTH = 60
SPACESHIP_HEIGHT = 60
ASTEROID_SIZE = 50
FONT = pygame.font.SysFont("comicsans", 36)

# Game Elements
player = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - 80, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
player_speed = 7

asteroids = []
asteroid_speed = 5
score = 0

# High Score
def load_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                return int(f.read())  # Try to read and convert to an integer
            except ValueError:  # If conversion fails, return 0
                return 0
    return 0

def save_highscore(new_score):
    with open("highscore.txt", "w") as f:
        f.write(str(new_score))

high_score = load_highscore()

# Draw Elements
def draw_window():
    win.fill((0, 0, 0))
    win.blit(spaceship_img, (player.x, player.y))
    
    for asteroid in asteroids:
        win.blit(asteroid_img, (asteroid.x, asteroid.y))
    
    score_text = FONT.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (10, 10))

    high_text = FONT.render(f"High Score: {high_score}", True, WHITE)
    win.blit(high_text, (10, 50))

    pygame.display.update()

# Start Screen
def start_screen():
    win.fill((0, 0, 0))
    title = FONT.render("🚀 Asteroid Game", True, WHITE)
    msg = FONT.render("Press any key to start", True, WHITE)
    win.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
    win.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
    pygame.display.update()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                wait = False

# Game Over Screen
def game_over_screen(final_score):
    win.fill((0, 0, 0))
    over = FONT.render("💥 Game Over!", True, WHITE)
    scr = FONT.render(f"Score: {final_score}", True, WHITE)
    msg = FONT.render("Press R to Retry or Q to Quit", True, WHITE)
    win.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2 - 60))
    win.blit(scr, (WIDTH//2 - scr.get_width()//2, HEIGHT//2))
    win.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 60))
    pygame.display.update()
    wait = True
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Main Loop
def main():
    global score, asteroids, player, high_score
    clock = pygame.time.Clock()
    run = True
    score = 0
    asteroids = []
    player = pygame.Rect(WIDTH//2 - SPACESHIP_WIDTH//2, HEIGHT - 80, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    while run:
        clock.tick(FPS)
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_highscore(high_score)
                run = False

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + SPACESHIP_WIDTH < WIDTH:
            player.x += player_speed

        # Asteroids
        if random.randint(1, 20) == 1:
            asteroid = pygame.Rect(random.randint(0, WIDTH - ASTEROID_SIZE), 0, ASTEROID_SIZE, ASTEROID_SIZE)
            asteroids.append(asteroid)

        for asteroid in asteroids[:]:
            asteroid.y += asteroid_speed
            if asteroid.colliderect(player):
                pygame.mixer.Sound.play(crash_sound)
                if score > high_score:
                    high_score = score
                    save_highscore(high_score)
                game_over_screen(score)
            if asteroid.y > HEIGHT:
                asteroids.remove(asteroid)
                score += 1

# Launch Game
start_screen()
main()
