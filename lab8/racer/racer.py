import pygame
import sys
import random

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

ROAD_LEFT = 60
ROAD_RIGHT = 340

BASE_SPEED = 20
COINS_PER_LEVEL = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 36)

bg_img = pygame.image.load("background-1_0.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
player_car_img = pygame.image.load("player_car.png").convert_alpha()
coin_img = pygame.image.load("coin.png").convert_alpha()

player_car_img = pygame.transform.scale(player_car_img, (70, 100))
coin_img = pygame.transform.scale(coin_img, (30, 30))

class PlayerCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_car_img
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        self.speed_x = 0

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left < ROAD_LEFT:
            self.rect.left = ROAD_LEFT
        if self.rect.right > ROAD_RIGHT:
            self.rect.right = ROAD_RIGHT

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.x = random.randint(ROAD_LEFT, ROAD_RIGHT - self.rect.width)
        self.rect.y = -random.randint(50, 300)
        self.speed_y = random.randint(3, 5)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.reset_position()

def draw_game_info(surface, score, level, speed):
    info = font.render(f"Score: {score}  Level: {level}  Speed: {speed}", True, WHITE)
    surface.blit(info, (10, 10))

def game_over_screen(score, level):
    screen.fill(BLACK)
    over_text = font.render("Game over", True, WHITE)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    over_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
    screen.blit(over_text, over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    player = PlayerCar()
    coins = pygame.sprite.Group()
    for _ in range(5):
        coins.add(Coin())
    all_sprites = pygame.sprite.Group(player, coins)

    score = 0
    level = 1
    coins_collected = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Continuous movement using key.get_pressed()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            player.speed_x = 5
        else:
            player.speed_x = 0

        all_sprites.update()

        # Check for coin collisions
        hits = pygame.sprite.spritecollide(player, coins, False)
        for coin in hits:
            score += 1
            coins_collected += 1
            coin.reset_position()
            if coins_collected >= COINS_PER_LEVEL:
                level += 1
                coins_collected = 0

        current_speed = BASE_SPEED + (level - 1) * 2

        screen.blit(bg_img, (0, 0))
        all_sprites.draw(screen)
        draw_game_info(screen, score, level, current_speed)
        pygame.display.flip()
        clock.tick(current_speed)

    game_over_screen(score, level)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
