import math
import pygame
from copy import deepcopy

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 24)

screen = pygame.display.set_mode((500, 600))
screen.fill("black")
pygame.display.set_caption("TTT")
clock = pygame.time.Clock()
running = True
start = False


line = 400/3
white = (255, 255, 255)


clicked = False
grid = []
for _ in range(3):
    row = [0] * 3
    grid.append(row)
player_turn = True
x_turn = True

wins = 0
losses = 0
ties = 0

def newTable():
    screen.fill("black")
    pygame.draw.line(screen, white, (50, 100 + 1 * line), (450, 100 + 1 * line) , 5)
    pygame.draw.line(screen, white, (450, 100 + 2 * line), (50, 100 + 2 * line) , 5)
    pygame.draw.line(screen, white, (50 + 1 * line, 100), (50 + 1 * line, 500) , 5)
    pygame.draw.line(screen, white, (50 + 2 * line, 500), (50 + 2 * line, 100) , 5)

def reset():
    global grid
    grid = []
    for _ in range(3):
        row = [0] * 3
        grid.append(row)
    newTable()

def draw_x(x, y):
    pygame.draw.line(screen, white, (50 + y * line, 100 + x * line), (50 + 1 * line + y * line, 100 + 1 * line + x * line), 5)
    pygame.draw.line(screen, white, (50 + y * line, 100 + 1 * line + x * line), (50 + 1 * line + y * line, 100 + x * line), 5)

def draw_o(x, y):
    pygame.draw.circle(screen, white, (50 + line/2 + y * line, 100 + line/2 + x * line), line/2, 5)

def init():
    if not start:
        img = font.render("Press any key to start", True, white)
        screen.blit(img, (120, 500))
    rect = pygame.Rect(0, 0, 500, 100)
    pygame.draw.rect(screen, (0, 0, 0), rect)
    img_w = font.render("Wins: " + str(wins), True, white)
    screen.blit(img_w, (50, 50))
    img_l = font.render("Losses: " + str(losses), True, white)
    screen.blit(img_l, (50 + 1 * line, 50))
    img_t = font.render("Ties: " + str(ties), True, white)
    screen.blit(img_t, (50 + 2 * line, 50))

def check_winner(g):
    sum_x = 0
    sum_y = 0
    sum_d1 = 0
    sum_d2 = 0
    sum_d1 = g[0][0] + g[1][1] + g[2][2]
    sum_d2 = g[0][2] + g[1][1] + g[2][0]
    has_zero = False
    for i in range(3):
        sum_x = 0
        sum_y = 0
        if 0 in g[i]:
            has_zero = True
        for j in range(3):
            sum_x += g[i][j]
            sum_y += g[j][i]
            if sum_x == 3 or sum_y == 3 or sum_d1 == 3 or sum_d2 == 3:
                return 1 # x won
            elif sum_x == -3 or sum_y == -3 or sum_d1 == -3 or sum_d2 == -3:
                return -1 # o won



    if not has_zero:
        return 0 # draw
    else:
        return None # not draw

def minimax(grid_clone, depth, x_turn, alpha, beta):
    # base case
    if depth == 0 or check_winner(grid_clone) != None:
        if check_winner(grid_clone) == None:
            return 0
        else:
            return check_winner(grid_clone)

    if x_turn:
        res = -math.inf
        for i in range(3):
            for j in range(3):
                if grid_clone[i][j] == 0:
                    grid_clone[i][j] = 1
                    score = minimax(grid_clone, depth - 1, not x_turn, alpha, beta)
                    grid_clone[i][j] = 0
                    res = max(score, res)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return res
    else:
        res = math.inf
        for i in range(3):
            for j in range(3):
                if grid_clone[i][j] == 0:
                    grid_clone[i][j] = -1
                    score = minimax(grid_clone, depth - 1, not x_turn, alpha, beta)
                    grid_clone[i][j] = 0
                    res = min(score, res)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return res

def computers_turn():
    global x_turn, grid, player_turn
    next_move = best_move(x_turn, deepcopy(grid))
    if next_move is not None:
        x = next_move[0]
        y = next_move[1]
        if x_turn:
            draw_x(x, y)
            grid[x][y] = 1
        else:
            draw_o(x, y)
            grid[x][y] = -1
        x_turn = not x_turn
        player_turn = True

def best_move(x_turn, grid_clone):
    if x_turn:
        score = -math.inf
    else:
        score = math.inf
    move = None

    for i in range(3):
        for j in range(3):
            if grid_clone[i][j] == 0:
                if x_turn:
                    grid_clone[i][j] = 1
                else:
                    grid_clone[i][j] = -1
                res = minimax(grid_clone, 9, not x_turn, -math.inf, math.inf)
                grid_clone[i][j] = 0

                if x_turn:
                    if res > score:
                        score = res
                        move = (i ,j)
                else:
                    if res < score:
                        score = res
                        move = (i, j)

    return move

while running:
    init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not start:
                start = True
                reset()
                if not player_turn:
                    computers_turn()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start:
                clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked:
            clicked = False
            pos = pygame.mouse.get_pos()
            x = -1
            y = -1
            if pos[0] > 50 and pos[0] < 50 + 1 * line:
                y = 0
            elif pos[0] < 450 and pos[0] > 50 + 2 * line:
                y = 2
            elif pos[0] > 50 and pos[0] < 450:
                y = 1
            if pos[1] > 100 and pos[1] < 100 + 1 * line:
                x = 0
            elif pos[1] < 500 and pos[1] > 100 + 2 * line:
                x = 2
            elif pos[1] > 100 and pos[1] < 500:
                x = 1

            if x != -1 and y != -1:
                if grid[x][y] == 0:
                    if x_turn:
                        draw_x(x, y)
                        grid[x][y] = 1
                    else:
                        draw_o(x, y)
                        grid[x][y] = -1
                    x_turn = not x_turn
                    player_turn = False
                    computers_turn()
                res = check_winner(grid)
                if res != None:
                    img = None
                    if res == 1:
                        if not player_turn:
                            wins += 1
                        else:
                            losses += 1
                        x_turn = not x_turn
                        img = font.render("X wins!", True, white)
                    elif res == -1:
                        if not player_turn:
                            wins += 1
                        else:
                            losses += 1
                        img = font.render("O wins!", True, white)
                    else:
                        ties += 1
                        x_turn = not x_turn
                        img = font.render("Draw!", True, white)
                    screen.blit(img, (220, 550))
                    start = False



    pygame.display.update()
    clock.tick(60)



pygame.quit()



