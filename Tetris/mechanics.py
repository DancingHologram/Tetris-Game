# Tetris mechanics module
from constants import BOARD_WIDTH, BOARD_HEIGHT, SCORE_SINGLE_LINE, SCORE_DOUBLE_LINE, SCORE_TRIPLE_LINE, SCORE_TETRIS, LOCK_DELAY_MS
import shapes

# Drop a piece onto the board
def drop(shape):
    # move shape down by one
    shape.y += 1

# Check if a piece collides with the bottom of the board or another piece
def check_collision(board, shape):
    # get shape matrix
    matrix = shape.image()
    # check each cell in the shape matrix
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # skip empty cells
            if matrix[i][j] == 0:
                continue
            # calculate board position
            board_y = shape.y + i
            board_x = shape.x + j
            # check boundaries
            # if the shape is above the board, ignore
            if board_y < 0:
                continue
            # check left, right, bottom boundaries
            # if the shape is out of horizontal bounds or below the board, collision occurs
            if board_x < 0 or board_x >= BOARD_WIDTH:
                return True
            # check bottom boundary and existing blocks
            # if the shape is below the board or overlaps with existing blocks, collision occurs
            if board_y >= BOARD_HEIGHT:
                return True
            # check existing blocks
            # if the shape overlaps with existing blocks on the board, collision occurs
            if board_y >= 0 and board[board_y][board_x] != 0:
                return True
    return False

# Keep pieces in place
def lock_shape(board, shape):
    # get shape matrix
    matrix = shape.image()
    # place each cell in the shape matrix onto the board
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # skip empty cells
            if matrix[i][j] == 0:
                continue
            # calculate board position
            board_y = shape.y + i
            board_x = shape.x + j
            # place the block on the board if within bounds
            if 0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH:
                # set the board cell to the shape's color
                board[board_y][board_x] = shape.color

# clear the lines of the board when a piece fills all spaces in a row
def clear_lines(board):
    # create new board without full lines
    new_board = []
    # count how many lines are cleared
    lines_cleared = 0
    # check each row
    for row in board:
        # if the row is full, increment cleared lines
        if all(cell != 0 for cell in row):
            lines_cleared += 1
        # else, keep the row
        else:
            new_board.append(row)
    # add empty rows at the top for each cleared line
    for _ in range(lines_cleared):
        # insert an empty row at the top
        new_board.insert(0, [0 for _ in range(BOARD_WIDTH)])
    return new_board, lines_cleared

# scoring helper
def score_for_lines(lines_cleared):
    # return score based on number of lines cleared
    # uses constants from constants.py
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
    # simple level calculation based on score
    level = score // 1000 + 1
    return level

# Check to see if a shape can be placed
def can_place_shape(board, shape):
    # check if placing the shape causes a collision
    return not check_collision(board, shape)

# update the game state
def update_game_state(current_shape, next_shape, board, score, level, lock_timer_ms, dt, force_lock=False):
    # update the game state based on current shape, next shape, board, score, level, and timers
    game_over = False
    # spawn new shape if needed
    if current_shape is None:
        # spawn the first shape or move next shape to current
        if next_shape is None:
            # spawn the first shape
            current_shape = shapes.get_random_shape()
            # spawn the next shape
            next_shape = shapes.get_random_shape()
        # move next shape to current
        else:
            # move next shape to current shape
            current_shape = next_shape
            # spawn a new next shape
            next_shape = shapes.get_random_shape()
        # check for game over
        if check_collision(board, current_shape):
            # set game over flag
            game_over = True
            # return early
            return current_shape, next_shape, board, score, level, game_over, lock_timer_ms
        # return early after spawning shape
        return current_shape, next_shape, board, score, level, game_over, lock_timer_ms
    
    # move shape down by one
    current_shape.y += 1
    # check for collision
    grounded =  check_collision(board, current_shape)
    # move shape back up
    current_shape.y -= 1
    # update lock timer
    if grounded:
        # increment lock timer
        lock_timer_ms += dt
    # reset lock timer if not grounded
    else:
        lock_timer_ms = 0

    # if not grounded, move shape down
    if not grounded:
        current_shape.y += 1
    # check if we should lock the shape
    should_lock = force_lock or (lock_timer_ms >= LOCK_DELAY_MS)
    # lock the shape if needed
    if should_lock:
        # place shape on board
        lock_shape(board, current_shape)
        # clear lines and update score
        board, lines_cleared = clear_lines(board)
        # update score and level
        score += score_for_lines(lines_cleared)
        # update level based on new score
        level = update_level(score)
        # spawn new shape
        current_shape = next_shape
        # spawn a new next shape
        next_shape = shapes.get_random_shape()
        # reset
        lock_timer_ms = 0
        # check for game over
        if check_collision(board, current_shape):
            # set game over flag
            game_over = True
    # return updated game state
    return current_shape, next_shape, board, score, level, game_over, lock_timer_ms

# movement helpers
def move_left(shape, board):
    # move shape left
    shape.x -= 1
    # check for collision
    if check_collision(board, shape):
        shape.x += 1

def move_right(shape, board):
    # move shape right
    shape.x += 1
    # check for collision
    if check_collision(board, shape):
        shape.x -= 1

def move_down(shape, board):
    # move shape down
    shape.y += 1
    # check for collision
    if check_collision(board, shape):
        shape.y -= 1

def rotate_shape(shape, board):
    # rotate shape clockwise
    shape.rotate()
    # check for collision
    if check_collision(board, shape):
        shape.rotate_back()

# hard drop implementation
def hard_drop(shape, board):
    # drop shape until it collides
    moved = False
    # keep moving down until collision
    while not check_collision(board, shape):
        # move down
        shape.y += 1
        # check for collision
        moved = True
    # move back up one step
    if moved == True:
        # adjust position back up
        shape.y -= 1
    return moved

# allow piece holding and swapping
def hold_shape(current_shape, held_shape, board):
    # hold or swap the current shape with the held shape
    game_over = False
    # determine if holding is allowed
    can_hold = None
    # perform hold or swap
    if held_shape is None:
        # hold the current shape and spawn a new one
        held_shape = current_shape
        # spawn a new current shape
        current_shape = shapes.get_random_shape()
        # reset hold ability
        can_hold = False
    # swap current and held shapes
    else:
        # swap the shapes
        temp = held_shape
        held_shape = current_shape
        current_shape = temp
        # reset hold ability
        can_hold = True
    # check for game over
    if not can_place_shape(board, current_shape):
        game_over = True
    # return updated shapes and game over status
    return current_shape, held_shape, can_hold, game_over