import os
import sys
import random
import pygame
from db import get_or_create_user, save_score

pygame.init()
CELL_SIZE      = 20
GRID_WIDTH     = 30
GRID_HEIGHT    = 20
WIDTH          = GRID_WIDTH  * CELL_SIZE
HEIGHT         = GRID_HEIGHT * CELL_SIZE
screen         = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock          = pygame.time.Clock()

WHITE          = (255, 255, 255)
BLACK          = (0,   0,   0)
GREEN_HEAD     = (0, 255,   0)
GREEN_BODY     = (0, 200,   0)
RED            = (255, 0,   0)

BASE_SPEED     = 5
FOODS_PER_LEVEL= 3
FOOD_LIFETIME  = 5000  # мс

font = pygame.font.SysFont(None, 36)

def random_food_position(snake_positions):
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake_positions:
            return (x, y)

def draw_snake(surface, snake_positions):
    for i, (x, y) in enumerate(snake_positions):
        rect  = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        color = GREEN_HEAD if i == 0 else GREEN_BODY
        pygame.draw.rect(surface, color, rect)

def draw_food(surface, food_position):
    x, y = food_position
    rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, RED, rect)

def draw_game_info(surface, score, level, speed):
    info_text = font.render(f"Score: {score}  Level: {level}  Speed: {speed}", True, WHITE)
    surface.blit(info_text, (10, 10))

def move_snake(snake_positions, direction):
    head_x, head_y = snake_positions[0]
    return [(head_x + direction[0], head_y + direction[1])] + snake_positions[:-1]

def check_collisions(snake_positions):
    head = snake_positions[0]
    if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):
        return True
    if head in snake_positions[1:]:
        return True
    return False

def game_over_screen(score, level, user_id):
    save_score(user_id, score, level)

    screen.fill(BLACK)
    over_text  = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)

    over_rect  = over_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))

    screen.blit(over_text, over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    username = input("Enter username: ").strip()
    user_id  = get_or_create_user(username)

    snake_positions = [(5, 5), (4, 5), (3, 5)]
    direction       = (1, 0)
    input_queue     = []

    food_position   = random_food_position(snake_positions)
    food_weight     = random.choice([1,2,3])
    food_spawn_time = pygame.time.get_ticks()

    score           = 0
    level           = 1
    foods_eaten     = 0
    running         = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                new_dir = None
                if event.key == pygame.K_UP:    new_dir = (0, -1)
                if event.key == pygame.K_DOWN:  new_dir = (0,  1)
                if event.key == pygame.K_LEFT:  new_dir = (-1, 0)
                if event.key == pygame.K_RIGHT: new_dir = (1,  0)
                if new_dir:
                    last = input_queue[-1] if input_queue else direction
                    if new_dir != (-last[0], -last[1]):
                        input_queue.append(new_dir)

        if input_queue:
            direction = input_queue.pop(0)

        if pygame.time.get_ticks() - food_spawn_time >= FOOD_LIFETIME:
            food_position   = random_food_position(snake_positions)
            food_weight     = random.choice([1,2,3])
            food_spawn_time = pygame.time.get_ticks()

        snake_positions = move_snake(snake_positions, direction)

        if check_collisions(snake_positions):
            running = False
            continue

        if snake_positions[0] == food_position:
            score      += food_weight
            foods_eaten+= 1
            snake_positions.append(snake_positions[-1])
            food_position   = random_food_position(snake_positions)
            food_weight     = random.choice([1,2,3])
            food_spawn_time = pygame.time.get_ticks()
            if foods_eaten >= FOODS_PER_LEVEL:
                level      += 1
                foods_eaten = 0

        screen.fill(BLACK)
        draw_snake(screen, snake_positions)
        draw_food(screen, food_position)
        current_speed = BASE_SPEED + (level - 1)*2
        draw_game_info(screen, score, level, current_speed)
        pygame.display.flip()
        clock.tick(current_speed)

    game_over_screen(score, level, user_id)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
