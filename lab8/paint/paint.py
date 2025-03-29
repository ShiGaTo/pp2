import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))


brush_icon = pygame.image.load("brush.png").convert_alpha()
rectangle_icon = pygame.image.load("rectangle.png").convert_alpha()
circle_icon = pygame.image.load("circle.png").convert_alpha()
eraser_icon = pygame.image.load("eraser.png").convert_alpha()

icon_size = (40, 40)
brush_icon = pygame.transform.scale(brush_icon, icon_size)
rectangle_icon = pygame.transform.scale(rectangle_icon, icon_size)
circle_icon = pygame.transform.scale(circle_icon, icon_size)
eraser_icon = pygame.transform.scale(eraser_icon, icon_size)

icon_positions = {
    "brush": pygame.Rect(10, 10, icon_size[0], icon_size[1]),
    "rectangle": pygame.Rect(60, 10, icon_size[0], icon_size[1]),
    "circle": pygame.Rect(110, 10, icon_size[0], icon_size[1]),
    "eraser": pygame.Rect(160, 10, icon_size[0], icon_size[1])
}

RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

current_color = BLACK
current_tool = "brush"

drawing = False
start_pos = (0, 0)
last_pos = None

BRUSH_SIZE = 5
ERASER_SIZE = 20

color_positions = {
    "red": pygame.Rect(10, 60, 30, 30),
    "green": pygame.Rect(50, 60, 30, 30),
    "blue": pygame.Rect(90, 60, 30, 30),
    "black": pygame.Rect(130, 60, 30, 30)
}

def draw_ui():
    screen.blit(brush_icon, icon_positions["brush"].topleft)
    screen.blit(rectangle_icon, icon_positions["rectangle"].topleft)
    screen.blit(circle_icon, icon_positions["circle"].topleft)
    screen.blit(eraser_icon, icon_positions["eraser"].topleft)

def draw_color_ui():
    pygame.draw.rect(screen, RED, color_positions["red"])
    pygame.draw.rect(screen, GREEN, color_positions["green"])
    pygame.draw.rect(screen, BLUE, color_positions["blue"])
    pygame.draw.rect(screen, BLACK, color_positions["black"])

def handle_tool_selection(pos):
    for tool, rect in icon_positions.items():
        if rect.collidepoint(pos):
            return tool
    return None

def handle_color_selection(pos):
    for color_name, rect in color_positions.items():
        if rect.collidepoint(pos):

            if color_name == "red":
                return RED
            elif color_name == "green":
                return GREEN
            elif color_name == "blue":
                return BLUE
            elif color_name == "black":
                return BLACK
    return None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                chosen_color = handle_color_selection(event.pos)
                if chosen_color is not None:
                    current_color = chosen_color
                else:
                    chosen_tool = handle_tool_selection(event.pos)
                    if chosen_tool is not None:
                        current_tool = chosen_tool
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if current_tool == "rectangle":
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(canvas, current_color, rect, width=2)
                elif current_tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, width=2)
                drawing = False

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if current_tool == "brush":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, BRUSH_SIZE)
                    last_pos = event.pos
                elif current_tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, ERASER_SIZE)
                    last_pos = event.pos

    screen.blit(canvas, (0, 0))
    draw_ui()
    draw_color_ui()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
