import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, TILE_SIZE, BOARD_ORIGIN_X, BOARD_ORIGIN_Y, BUTTON_COLOR, BOARD_WIDTH, BOARD_HEIGHT
from mechanics import update_game_state, move_left, move_right, rotate_shape, hard_drop, move_down
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def create_board():
    board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    return board

def draw_board(screen, board):
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            cell_value = board[y][x]
            cell_x = BOARD_ORIGIN_X + x * TILE_SIZE
            cell_y = BOARD_ORIGIN_Y + y * TILE_SIZE
            if cell_value == 0:
                pygame.draw.rect(screen, BUTTON_COLOR, (cell_x, cell_y, TILE_SIZE, TILE_SIZE), 1)
            else:
                pygame.draw.rect(screen, cell_value, (cell_x, cell_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, TILE_SIZE, TILE_SIZE), 1)

def draw_shape(screen, shape):
    shape_image = shape.image()
    for row_idx, row in enumerate(shape_image):
        for col_idx, cell in enumerate(row):
            if cell:
                cell_x = BOARD_ORIGIN_X + (shape.x + col_idx) * TILE_SIZE
                cell_y = BOARD_ORIGIN_Y + (shape.y + row_idx) * TILE_SIZE
                pygame.draw.rect(screen, shape.color, (cell_x, cell_y, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(screen, WHITE, (cell_x, cell_y, TILE_SIZE, TILE_SIZE), 1)

def main():
    pygame.display.set_caption("Tetris")
    board = create_board()
    current_shape = None
    next_shape = None
    score = 0
    level = 1
    game_over = False
    drop_counter = 0
    drop_interval = max(5, FPS // level)
    lock_timer_ms = 0
    did_soft_drop = False
    accumulated_time = 0

    while True:
        dt = clock.tick(FPS)  # delta time in milliseconds
        accumulated_time += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
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
                if not game_over and current_shape:
                    if event.key == pygame.K_LEFT:
                        move_left(current_shape, board)
                    elif event.key == pygame.K_RIGHT:
                        move_right(current_shape, board)
                    elif event.key == pygame.K_DOWN:
                        old_y = current_shape.y
                        move_down(current_shape, board)
                        if current_shape.y > old_y:
                            did_soft_drop = True
                    elif event.key == pygame.K_UP:
                        rotate_shape(current_shape, board)
                    elif event.key == pygame.K_SPACE:
                        hard_drop(current_shape, board)
                        current_shape, next_shape, board, score, level, game_over, lock_timer_ms = update_game_state(current_shape, next_shape, board, score, level, lock_timer_ms, accumulated_time, force_lock=True)
                        accumulated_time = 0
                        drop_interval = max(5, FPS // level)
        if not game_over:
            drop_counter += 1
            if drop_counter >= drop_interval or did_soft_drop:
                drop_counter = 0
                score += 1 if did_soft_drop else 0
                current_shape, next_shape, board, score, level, game_over, lock_timer_ms = update_game_state(
                    current_shape, next_shape, board, score, level, lock_timer_ms, accumulated_time, force_lock=False)
                accumulated_time = 0
                did_soft_drop = False
                drop_interval = max(5, FPS // level)

        screen.fill(BLACK)
        draw_board(screen, board)
        if current_shape:
            draw_shape(screen, current_shape)
        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Game Over! Final Score: {score}", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()
if __name__ == "__main__":
    main()