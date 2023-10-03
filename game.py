import pygame
import random
import json
import os

pygame.init()

script_dir = os.path.dirname(__file__)

pygame.mixer.music.load(os.path.join(script_dir, 'assets', 'sounds', 'music.mp3'))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

loss_music = pygame.mixer.Sound(os.path.join(script_dir, 'assets', 'sounds', 'loss_sound.mp3'))
explosion_sound = pygame.mixer.Sound(os.path.join(script_dir, 'assets', 'sounds', 'explosion_sound.wav'))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

window_dimensions = (640, 480)
window = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption("Fast'n Rocks")

player_width = 50
player_height = 70
player_x = window_dimensions[0] // 2 - player_width // 2
player_y = window_dimensions[1] - player_height - 10

# Diretório do script

# Carregue os arquivos de imagem usando caminhos relativos
road_image = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'background.png')), window_dimensions)
score_image = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'score-image.png')), (150, 150))

obstacle_width = 50
obstacle_height = 50
obstacle_speed = 3
obstacles = []

font = pygame.font.Font(None, 30)

lives = 3
max_lives = 3

def draw_hearts(surface, x, y, lives, max_lives):
    heart_icon = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'heart.png')), (30, 30))
    heart_width, heart_height = heart_icon.get_size()
    for i in range(max_lives):
        if i < lives:
            surface.blit(heart_icon, (x + i * (heart_width + 5), y))

player_image = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'car.png')), (player_width, player_height))

car_obstacle_images = [
    pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'car-truck1.png')), (40, 70)),
    pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'car-truck2.png')), (40, 70)),
    pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'car-truck3.png')), (40, 80)),
    pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'car-truck4.png')), (40, 100)),
]

score = 0
clock = pygame.time.Clock()
in_game = True
game_over = False

best_score = 0
try:
    with open(os.path.join(script_dir, 'best_score.json'), 'r') as file:
        best_score = json.load(file)
except FileNotFoundError:
    pass

game_over_image = pygame.transform.scale(pygame.image.load(os.path.join(script_dir, 'assets', 'images', 'gameOver.png')), (400, 400))

new_best_score = False

while in_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_game = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.mixer.music.pause()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            pygame.mixer.music.unpause()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 100:
        player_x -= 5
    elif keys[pygame.K_RIGHT] and player_x < 545 - player_width:
        player_x += 5

    for obstacle in obstacles:
        obstacle[1] += obstacle_speed
    if len(obstacles) == 0 or obstacles[-1][1] > 250:
        x = random.randint(135, 520 - obstacle_width)
        car_image = random.choice(car_obstacle_images)
        obstacles.append([x, -obstacle_height, car_image])
    if obstacles[0][1] > window_dimensions[1]:
        obstacles.pop(0)

    for obstacle in obstacles:
        if player_x < obstacle[0] + obstacle_width and \
                player_x + player_width > obstacle[0] and \
                player_y < obstacle[1] + obstacle_height and \
                player_y + player_height > obstacle[1]:
            obstacles.remove(obstacle)
            lives -= 1
            explosion_sound.play()
            explosion_sound.set_volume(0.1)
            if lives <= 0:
                loss_music.play()
                loss_music.set_volume(0.1)
                pygame.mixer.music.stop()

                if score > best_score:
                    best_score = score
                    new_best_score = True 

    score += 1

    if score % 250 == 0:
        obstacle_speed += 1

    window.blit(road_image, (0, 0))

    for obstacle in obstacles:
        window.blit(obstacle[2], (obstacle[0], obstacle[1]))

    window.blit(player_image, (player_x, player_y))

    window.blit(score_image, (-8, -45))

    score_text = font.render(str(score), True, BLACK)
    window.blit(score_text, (33, 20))

    draw_hearts(window, window_dimensions[0] - 50 - (max_lives * 25), 10, lives, max_lives)

    best_score_text = font.render("Best Score: " + str(best_score), True, WHITE)
    best_score_rect = best_score_text.get_rect(center=(window_dimensions[0] // 2, 20))
    window.blit(best_score_text, best_score_rect)

    pygame.display.update()

    clock.tick(60)

    if lives <= 0:
        game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_game = False
                game_over = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                lives = max_lives
                score = 0
                obstacles.clear()
                obstacle_speed = 3
                game_over = False
                pygame.mixer.music.load(os.path.join(script_dir, 'assets', 'sounds', 'music.mp3'))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.1)

        image_rect = game_over_image.get_rect(center=(window_dimensions[0] // 2, window_dimensions[1] // 2 - 50))
        window.blit(game_over_image, image_rect)

        game_over_text = font.render("Press 'R' to Restart.", True, WHITE)
        text_rect = game_over_text.get_rect(center=(window_dimensions[0] // 2, window_dimensions[1] // 2 + 50))
        window.blit(game_over_text, text_rect)

        if new_best_score:
            best_score_text = font.render("New Best Score: " + str(best_score), True, GREEN)
            best_score_rect = best_score_text.get_rect(center=(window_dimensions[0] // 2, window_dimensions[1] // 2 + 100))
            window.blit(best_score_text, best_score_rect)

        pygame.display.update()

with open(os.path.join(script_dir, 'best_score.json'), 'w') as file:
    json.dump(best_score, file)

pygame.quit()
