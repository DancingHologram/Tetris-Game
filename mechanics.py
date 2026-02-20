import pygame
from constants import *
import shapes
import button

# drop tetronimos by one row
def drop(shape):
    shape.y += 1

# check for collision with the bottom of the board or other pieces
def check_collision(board, shape):
    for i in range(len(shape.image())):
        for j in range(len(shape.image()[i])):
            if shape.image()[i][j] == 1:
                if shape.y + i >= BOARD_HEIGHT or board[shape.y + i][shape.x + j] != 0:
                    return True
    return False

# lock the shape in place on the board
def lock_shape(board, shape):
    for i in range(len(shape.image())):
        for j in range(len(shape.image()[i])):
            if shape.image()[i][j] == 1:
                board[shape.y + i][shape.x + j] = shape.color

# clear completed lines and return the number of lines cleared
def clear_lines(board):
    lines_cleared = 0
    for i in range(len(board)):
        if all(x != 0 for x in board[i]):
            del board[i]
            board.insert(0, [0] * BOARD_WIDTH)
            lines_cleared += 1
    return lines_cleared

# check for game over condition
def check_game_over(board):
    for j in range(BOARD_WIDTH):
        if board[0][j] != 0:
            return True
    return False

# move the shape left or right
def move(shape, direction, board):
    if direction == 'left':
        shape.x -= 1
        if check_collision(board, shape):
            shape.x += 1
    elif direction == 'right':
        shape.x += 1
        if check_collision(board, shape):
            shape.x -= 1

# rotate the shape
def rotate(shape, board):
    shape.rotate()
    if check_collision(board, shape):
        shape.rotate()  # rotate back if there is a collision

# hard drop the shape
def hard_drop(shape, board):
    while not check_collision(board, shape):
        shape.y += 1
    shape.y -= 1  # move back up one row to the last valid position

# calculate the score based on the number of lines cleared
def calculate_score(lines_cleared):
    if lines_cleared == 1:
        return 100
    elif lines_cleared == 2:
        return 300
    elif lines_cleared == 3:
        return 500
    elif lines_cleared == 4:
        return 800
    else:
        return 0
    
# update the score and level based on the number of lines cleared
def update_score_and_level(score, level, lines_cleared):
    score += calculate_score(lines_cleared)
    if score >= level * 1000:
        level += 1
    return score, level

# draw the current score and level on the screen
def draw_score_and_level(screen, score, level):
    font = pygame.font.SysFont(None, 36)
    score_surface = font.render(f'Score: {score}', True, WHITE)
    level_surface = font.render(f'Level: {level}', True, WHITE)
    screen.blit(score_surface, (MARGIN, MARGIN))
    screen.blit(level_surface, (MARGIN, MARGIN + 40))

# draw the next shape preview on the screen
def draw_next_shape(screen, next_shape):
    font = pygame.font.SysFont(None, 36)
    next_surface = font.render('Next:', True, WHITE)
    screen.blit(next_surface, (RIGHT_BOUNDARY - 100, MARGIN))
    for i in range(len(next_shape.image())):
        for j in range(len(next_shape.image()[i])):
            if next_shape.image()[i][j] == 1:
                pygame.draw.rect(screen, next_shape.color, (RIGHT_BOUNDARY - 100 + j * TILE_SIZE, MARGIN + 40 + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# draw the game board and the current shape on the screen
def draw_board(screen, board, shape):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                pygame.draw.rect(screen, board[i][j], (BOARD_ORIGIN_X + j * TILE_SIZE, BOARD_ORIGIN_Y + i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for i in range(len(shape.image())):
        for j in range(len(shape.image()[i])):
            if shape.image()[i][j] == 1:
                pygame.draw.rect(screen, shape.color, (BOARD_ORIGIN_X + (shape.x + j) * TILE_SIZE, BOARD_ORIGIN_Y + (shape.y + i) * TILE_SIZE, TILE_SIZE, TILE_SIZE))