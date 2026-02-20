import pygame
from constants import *
import shapes
import button
import random
import pickle

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

# draw the menu screen with the title, start button, high score display, and quit button
def draw_menu(screen, high_score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    title_surface = font.render('Tetris', True, WHITE)
    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_surface, title_rect)

    start_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, 'Start')
    quit_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 50, 'Quit')
    start_button.draw(screen)
    quit_button.draw(screen)

    high_score_surface = font.render(f'High Score: {high_score}', True, WHITE)
    high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
    screen.blit(high_score_surface, high_score_rect)

    return start_button, quit_button

# draw the game over screen with the final score and a restart button
def draw_game_over(screen, score):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    game_over_surface = font.render('Game Over', True, WHITE)
    game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(game_over_surface, game_over_rect)

    score_surface = font.render(f'Final Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
    screen.blit(score_surface, score_rect)

    restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, 'Restart')
    restart_button.draw(screen)

    return restart_button

# draw the pause screen with a resume button
def draw_pause(screen):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    pause_surface = font.render('Paused', True, WHITE)
    pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(pause_surface, pause_rect)

    resume_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, 'Resume')
    resume_button.draw(screen)

    return resume_button

# draw the settings screen with options to adjust the game speed and controls
def draw_settings(screen, game_speed, controls):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    settings_surface = font.render('Settings', True, WHITE)
    settings_rect = settings_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(settings_surface, settings_rect)

    # draw game speed options
    speed_surface = font.render(f'Game Speed: {game_speed}', True, WHITE)
    speed_rect = speed_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
    screen.blit(speed_surface, speed_rect)

    # draw controls options
    controls_surface = font.render(f'Controls: {controls}', True, WHITE)
    controls_rect = controls_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 200))
    screen.blit(controls_surface, controls_rect)

    return speed_rect, controls_rect

# save the high score to a binary file
def save_high_score(high_score):
    with open('high_score.bin', 'wb') as f:
        pickle.dump(high_score, f)

# load the high score from a binary file
def load_high_score():
    try:
        with open('high_score.bin', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return 0
    
# reset the game state for a new game
def reset_game():
    global board, current_shape, next_shape, score, level
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    current_shape = None
    next_shape = None
    score = 0
    level = 1

# generate a random tetromino shape
def generate_random_shape():
    shape_type = random.choice(list(TETROMINO_SHAPES.keys()))
    color = COLORS[shape_type]
    return shapes.Shape(BOARD_WIDTH // 2 - 1, 0, color)

# generate the next shape and set it as the current shape
def generate_next_shape():
    global current_shape, next_shape
    if next_shape is None:
        next_shape = generate_random_shape()
    current_shape = next_shape
    next_shape = generate_random_shape()

# check if the current shape can be placed on the board
def can_place_shape(board, shape):
    for i in range(len(shape.image())):
        for j in range(len(shape.image()[i])):
            if shape.image()[i][j] == 1:
                if shape.y + i >= BOARD_HEIGHT or shape.x + j < 0 or shape.x + j >= BOARD_WIDTH or board[shape.y + i][shape.x + j] != 0:
                    return False
    return True

# check if the current shape can be moved in the specified direction
def can_move_shape(board, shape, direction):
    if direction == 'left':
        shape.x -= 1
        if not can_place_shape(board, shape):
            shape.x += 1
            return False
    elif direction == 'right':
        shape.x += 1
        if not can_place_shape(board, shape):
            shape.x -= 1
            return False
    elif direction == 'down':
        shape.y += 1
        if not can_place_shape(board, shape):
            shape.y -= 1
            return False
    return True

# check if the current shape can be rotated
def can_rotate_shape(board, shape):
    shape.rotate()
    if not can_place_shape(board, shape):
        shape.rotate()  # rotate back if it cannot be placed
        return False
    return True

# check if the current shape can be hard dropped
def can_hard_drop_shape(board, shape):
    while not check_collision(board, shape):
        shape.y += 1
    shape.y -= 1  # move back up one row to the last valid position
    return can_place_shape(board, shape)

# check if the player has achieved a new high score and update it if necessary
def check_and_update_high_score(score):
    high_score = load_high_score()
    if score > high_score:
        save_high_score(score)
        return score
    return high_score

# check if the player has reached a new level and update the game speed accordingly
def check_and_update_level(score, level):
    new_level = score // 1000 + 1
    if new_level > level:
        return new_level
    return level
