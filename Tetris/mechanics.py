# Tetris mechanics module
from constants import BOARD_WIDTH, BOARD_HEIGHT, SCORE_SINGLE_LINE, SCORE_DOUBLE_LINE, SCORE_TRIPLE_LINE, SCORE_TETRIS, LOCK_DELAY_MS
import shapes

# Drop a piece onto the board
def drop(shape):
    shape.y += 1

# Check if a piece collides with the bottom of the board or another piece
def check_collision(board, shape):
    matrix = shape.image()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                continue
            board_y = shape.y + i
            board_x = shape.x + j
            if board_y < 0:
                continue
            if board_x < 0 or board_x >= BOARD_WIDTH:
                return True
            if board_y >= BOARD_HEIGHT:
                return True
            if board_y >= 0 and board[board_y][board_x] != 0:
                return True
    return False

# Keep pieces in place
def lock_shape(board, shape):
    matrix = shape.image()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                continue
            board_y = shape.y + i
            board_x = shape.x + j
            if 0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH:
                board[board_y][board_x] = shape.color

# clear the lines of the board when a piece fills all spaces in a row
def clear_lines(board):
    new_board = []
    lines_cleared = 0
    for row in board:
        if all(cell != 0 for cell in row):
            lines_cleared += 1
        else:
            new_board.append(row)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
    return new_board, lines_cleared

# scoring helper
def score_for_lines(lines_cleared):
    if lines_cleared == 1:
        return SCORE_SINGLE_LINE
    elif lines_cleared == 2:
        return SCORE_DOUBLE_LINE
    elif lines_cleared == 3:
        return SCORE_TRIPLE_LINE
    elif lines_cleared == 4:
        return SCORE_TETRIS
    return 0

# level helper
def update_level(score):
    level = score // 1000 + 1
    return level

# Check to see if a shape can be placed
def can_place_shape(board, shape):
    return not check_collision(board, shape)

# update the game state
def update_game_state(current_shape, next_shape, board, score, level, lock_timer_ms, dt, force_lock=False):
    game_over = False
    if current_shape is None:
        if next_shape is None:
            current_shape = shapes.get_random_shape()
            next_shape = shapes.get_random_shape()
        else:
            current_shape = next_shape
            next_shape = shapes.get_random_shape()
        if check_collision(board, current_shape):
            game_over = True
            return current_shape, next_shape, board, score, level, game_over, lock_timer_ms
        return current_shape, next_shape, board, score, level, game_over, lock_timer_ms
    
    current_shape.y += 1
    grounded =  check_collision(board, current_shape)
    current_shape.y -= 1
    if grounded:
        lock_timer_ms += dt
    else:
        lock_timer_ms = 0

    if not grounded:
        current_shape.y += 1

    should_lock = force_lock or (lock_timer_ms >= LOCK_DELAY_MS)

    if should_lock:
        lock_shape(board, current_shape)
        board, lines_cleared = clear_lines(board)
        score += score_for_lines(lines_cleared)
        level = update_level(score)
        current_shape = next_shape
        next_shape = shapes.get_random_shape()
        lock_timer_ms = 0
        if check_collision(board, current_shape):
            game_over = True
    return current_shape, next_shape, board, score, level, game_over, lock_timer_ms

# movement helpers
def move_left(shape, board):
    shape.x -= 1
    if check_collision(board, shape):
        shape.x += 1

def move_right(shape, board):
    shape.x += 1
    if check_collision(board, shape):
        shape.x -= 1

def move_down(shape, board):
    shape.y += 1
    if check_collision(board, shape):
        shape.y -= 1

def rotate_shape(shape, board):
    shape.rotate()
    if check_collision(board, shape):
        shape.rotate_back()

def hard_drop(shape, board):
    moved = False
    while not check_collision(board, shape):
        shape.y += 1
        moved = True
    if moved == True:
        shape.y -= 1
    return moved

# allow piece holding and swapping
def hold_shape(current_shape, held_shape, board):
    game_over = False
    can_hold = None
    if held_shape is None:
        held_shape = current_shape
        current_shape = shapes.get_random_shape()
        can_hold = False
    else:
        temp = held_shape
        held_shape = current_shape
        current_shape = temp
        can_hold = True
    if not can_place_shape(board, current_shape):
        game_over = True
    return current_shape, held_shape, can_hold, game_over