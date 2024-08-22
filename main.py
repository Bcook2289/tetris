# Example file showing a circle moving on screen
import pygame
from random import choice, randrange
from copy import deepcopy

# set width and height
W, H = 10, 20
# set tile height
TILE = 45
# set game resolution
GAME_RES = W * TILE, H * TILE
RES = 1050, 940
PIECE_RES = 180, 180
SCORE_RES = 300, 100

# set FPS
FPS = 60

# initialize pygame
pygame.init()
# set main screen
sc = pygame.display.set_mode(RES)
# set game screen to be resolution
game_sc = pygame.Surface(GAME_RES, pygame.SRCALPHA, 32)
piece_sc = pygame.Surface(PIECE_RES, pygame.SRCALPHA, 32)
score_sc = pygame.Surface(SCORE_RES, pygame.SRCALPHA, 32)
# create an object to help track time
clock = pygame.time.Clock()

# create a 2 dimensional array where each item is an instance of the pygame.Rect class
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# create tile pieces
figure_pos = [
    [(-1, 0),(-2, 0),(0, 0),(1, 0)],    # Line piece
    [(0, -1),(-1, -1),(-1, 0),(0, 0)],  # Square piece
    [(-1, 0),(-1, 1),(0, 0),(0, -1)],   # Backwards Z piece
    [(0, 0),(-1, 0),(0, 1),(-1, -1)],   # Z piece
    [(0, 0),(0, -1),(0, 1),(-1, -1)],   # L piece
    [(0, 0),(0, -1),(0, 1),(-1, 1)],    # Backwards L piece
    [(0, 0),(0, -1),(0, 1),(-1, 0)]     # T piece
    ]
    
colors = {
    "red":(255, 0, 0), 
    "yellow": (255, 255, 0), 
    "orange": (255, 150, 0), 
    "blue":(0, 0, 255), 
    "green": (0, 255, 0), 
    "light blue":(0, 255, 255), 
    "purple":(125, 0, 255)
    }

figures = [[pygame.Rect(x + W // 2, y + 1, 1,1) for x, y in fig_pos] for fig_pos in figure_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)

# create the game grid
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load('./imgs/tetris-background.jpg').convert()

font = pygame.font.Font('./font/Silkscreen-Regular.ttf', 45)

title_score = font.render('score:', True, pygame.Color('green'))

get_color_random = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
def get_color(fig): 
    if figures.index(fig) == 0:         # if straight piece
        return colors["light blue"] 
    elif figures.index(fig) == 1:       # if square piece
        return colors["yellow"] 
    elif figures.index(fig) == 2:       # if S piece
        return colors["green"] 
    elif figures.index(fig) == 3:       # if Z piece
        return colors["red"]
    elif figures.index(fig) == 4:       # if L piece
        return colors["orange"] 
    elif figures.index(fig) == 5:       # if J piece
        return colors["blue"] 
    elif figures.index(fig) == 6:       # if T piece
        return colors["purple"] 

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(figure), get_color(next_figure)

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True

while True:
    dx, rotate = 0, False
    
    # create new screens
    sc.blit(bg, (310, 0))
    sc.blit(game_sc, (20, 20))
    sc.blit(piece_sc, (674, 460))
    sc.blit(score_sc, (540, 797))

    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)

    # fill game screen with black screens
    game_sc.fill(pygame.Color('black'))
    piece_sc.fill(pygame.Color('black'))
    score_sc.fill(pygame.Color('black'))

    # control 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                rotate = True

    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    
    # constrain right and left border
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure = deepcopy(choice(figures))
                next_color = get_color(next_figure)
                anim_limit = 2000
                break

    # rotate the piece
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    # check lines
    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # compute score
    score += scores[lines]

    # draw the grid
    [pygame.draw.rect(game_sc, (50, 50, 50), i_rect, 1) for i_rect in grid]

    # draw the figures
    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)

    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 540
        figure_rect.y = next_figure[i].y * TILE + 485
        pygame.draw.rect(sc, next_color, figure_rect)

    sc.blit(title_score, (535, 780))
    sc.blit(font.render(str(score), True, pygame.Color('green')), (550,840))

    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color_random(), i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)