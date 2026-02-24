import pygame
import sys
import button
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, TILE_SIZE, BOARD_ORIGIN_X, BOARD_ORIGIN_Y, BUTTON_COLOR, BOARD_WIDTH, BOARD_HEIGHT
from mechanics import update_game_state, move_left, move_right, rotate_shape, hard_drop, move_down
pygame.init()

# set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# set up clock
clock = pygame.time.Clock()

# board creation and drawing
def create_board():
    # create empty board
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    return board

# draw the game board
def draw_board(screen, board):
    # draw each cell
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            # draw each cell based on its value
            cell_value = board[y][x]
            # calculate cell position
            # uses origin offsets and tile size
            cell_x = BOARD_ORIGIN_X + x * TILE_SIZE
            cell_y = BOARD_ORIGIN_Y + y * TILE_SIZE
            # draw cell
            # empty cell
            if cell_value == 0:
                # draw empty cell border
                pygame.draw.rect(screen, BUTTON_COLOR, (cell_x, cell_y, TILE_SIZE, TILE_SIZE), 1)
            # filled cell
            else:
                # draw filled cell
                pygame.draw.rect(screen, cell_value, (cell_x, cell_y, TILE_SIZE, TILE_SIZE))
                # draw cell border
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, TILE_SIZE, TILE_SIZE), 1)

# draw the current shape on the board
def draw_shape(screen, shape):
    # draw each cell of the shape
    shape_image = shape.image()
    # iterate over shape image
    for row_idx, row in enumerate(shape_image):
        for col_idx, cell in enumerate(row):
            # draw only filled cells
            if cell:
                # calculate cell position on board
                cell_x = BOARD_ORIGIN_X + (shape.x + col_idx) * TILE_SIZE
                cell_y = BOARD_ORIGIN_Y + (shape.y + row_idx) * TILE_SIZE
                # draw the cell
                pygame.draw.rect(screen, shape.color, (cell_x, cell_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, TILE_SIZE, TILE_SIZE), 1)

# draw title text at center top
def draw_title(text, y):
    # draw title text at center top
    font = pygame.font.Font(None, 74)
    # render the text
    text_surface = font.render(text, True, WHITE)
    # center the text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    # blit to screen
    screen.blit(text_surface, text_rect)

# draw centered text
def draw_center_text(text, y, size=36):
    # draw centered text at given y position
    font = pygame.font.Font(None, size)
    # render the text
    text_surface = font.render(text, True, WHITE)
    # center the text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    # blit to screen
    screen.blit(text_surface, text_rect)

# main game loop
def main():
    # set window title
    pygame.display.set_caption("Tetris")
    # game state
    state = "menu"
    # create buttons
    # position buttons in center of screen
    start_button = button.Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 80, 240, 50, "Start")
    scores_button = button.Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20, 240, 50, "Scores")
    options_button = button.Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40, 240, 50, "Options")
    quit_button = button.Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 100, 240, 50, "Quit")
    # back button for options and scores
    back_button = button.Button(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT - 100, 240, 50, "Back")
    # initialize game variables
    board = create_board()
    # current and next shapes
    current_shape = None
    next_shape = None
    # game variables
    score = 0
    level = 1
    game_over = False
    # timers
    drop_counter = 0
    drop_interval = max(5, FPS // level)
    lock_timer_ms = 0
    did_soft_drop = False
    accumulated_time = 0
    # main loop
    while True:
        # handle events and update game state
        dt = clock.tick(FPS)  # delta time in milliseconds
        accumulated_time += dt
        # get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # update button hover states
        for btn in (start_button, scores_button, options_button, quit_button, back_button):
            btn.update_hover(mouse_pos)
        
        # event handling
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # handle button clicks based on state
            if state == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
                # check which button was clicked
                if start_button.is_clicked(mouse_pos):
                    # reset game state
                    board = create_board()
                    current_shape = None
                    next_shape = None
                    score = 0
                    level = 1
                    game_over = False
                    lock_timer_ms = 0
                    drop_counter = 0
                    drop_interval = max(5, FPS // level)
                    did_soft_drop = False
                    accumulated_time = 0
                    # change state to playing
                    state = "playing"
                # other buttons
                elif scores_button.is_clicked(mouse_pos):
                    state = "scores"
                elif options_button.is_clicked(mouse_pos):
                    state = "options"
                # quit button
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()

            # back button in options or scores
            elif state in ("options", "scores") and event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.is_clicked(mouse_pos):
                    state = "menu"

            # game over restart or menu
            elif state == "game_over" and event.type == pygame.KEYDOWN:
                # restart game
                if event.key == pygame.K_r:
                    board = create_board()
                    current_shape = None
                    next_shape = None
                    score = 0
                    level = 1
                    game_over = False
                    lock_timer_ms = 0
                    drop_counter = 0
                    drop_interval = max(5, FPS // level)
                    did_soft_drop = False
                    accumulated_time = 0
                    state = "playing"
                # return to menu
                elif event.key == pygame.K_m:
                    state = "menu"

            # in-game controls
            elif state == "playing" and event.type == pygame.KEYDOWN:
                # handle key presses
                if event.key == pygame.K_ESCAPE:
                    state = "menu"
                # restart game
                elif event.key == pygame.K_r:
                    board = create_board()
                    current_shape = None
                    next_shape = None
                    score = 0
                    level = 1
                    game_over = False
                    lock_timer_ms = 0
                    drop_counter = 0
                    drop_interval = max(5, FPS // level)
                    did_soft_drop = False
                    accumulated_time = 0
                    state = "playing"
                # movement keys
                elif current_shape:
                    if event.key == pygame.K_LEFT:
                        move_left(current_shape, board)
                    elif event.key == pygame.K_RIGHT:
                        move_right(current_shape, board)
                    elif event.key == pygame.K_DOWN:
                        old_y = current_shape.y
                        # soft drop
                        move_down(current_shape, board)
                        if current_shape.y > old_y:
                            did_soft_drop = True
                        if game_over:
                            state = "game_over"
                    # rotation
                    elif event.key == pygame.K_UP:
                        rotate_shape(current_shape, board)
                    # hard drop
                    elif event.key == pygame.K_SPACE:
                        hard_drop(current_shape, board)
                        current_shape, next_shape, board, score, level, game_over, lock_timer_ms = update_game_state(current_shape, next_shape, board, score, level, lock_timer_ms, accumulated_time, force_lock=True)
                        accumulated_time = 0
                        drop_interval = max(5, FPS // level)
                        if state == "playing" and game_over:
                            state = "game_over"

        # game logic updates
        if state == "playing" and not game_over:
            drop_counter += 1
            # update game state based on drop interval
            if drop_counter >= drop_interval or did_soft_drop:
                drop_counter = 0 
                score += 1 if did_soft_drop else 0  # soft drop score
                current_shape, next_shape, board, score, level, game_over, lock_timer_ms = update_game_state(
                    current_shape, next_shape, board, score, level, lock_timer_ms, accumulated_time, force_lock=False)
                if state == "playing" and game_over:
                    state = "game_over"
                accumulated_time = 0
                did_soft_drop = False  # reset soft drop flag
                drop_interval = max(5, FPS // level)
                if game_over:
                    state = "game_over"
        # drawing
        screen.fill(BLACK)
        # draw based on state
        if state == "menu":
            draw_title("TETRIS", SCREEN_HEIGHT // 4)
            start_button.draw(screen)
            scores_button.draw(screen)
            options_button.draw(screen)
            quit_button.draw(screen)
        # game playing state
        elif state == "playing":
            draw_board(screen, board)
            if current_shape:
                draw_shape(screen, current_shape)
            draw_center_text(f"Score: {score}   Level: {level}", 30, size=32)
        # scores and options screens
        elif state == "scores":
            draw_title("SCORES", SCREEN_HEIGHT // 4)
            draw_center_text("High scores screen coming next step", SCREEN_HEIGHT // 2)
            back_button.draw(screen)
        # options screen
        elif state == "options":
            draw_title("OPTIONS", SCREEN_HEIGHT // 4)
            draw_center_text("Controls remap screen coming next step", SCREEN_HEIGHT // 2)
            back_button.draw(screen)
        # game over screen
        elif state == "game_over":
            draw_board(screen, board)
            if current_shape:
                draw_shape(screen, current_shape)
            # display game over text
            draw_center_text(f"Game Over! Final Score: {score}", SCREEN_HEIGHT // 2 - 20)
            draw_center_text("Press R to Restart or M for Menu", SCREEN_HEIGHT // 2 + 20, size=30)
        # update the display
        pygame.display.flip()

# run the game
if __name__ == "__main__":
    main()