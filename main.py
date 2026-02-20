from constants import *
import random
import pygame
import button
import shapes
import mechanics

# global variables for the game state
board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
current_shape = None
next_shape = None
score = 0
level = 1

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # create buttons
    start_button = button.Button(50, 50, 100, 50, "Start")
    quit_button = button.Button(50, 120, 100, 50, "Quit")
    speed_button = button.Button(50, 190, 100, 50, "Speed")
    controls_button = button.Button(50, 260, 100, 50, "Controls")
    buttons = [start_button, quit_button, speed_button, controls_button]

    # create the menu loop
    menu_running = True
    while menu_running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    menu_running = False  # exit the menu loop to start the game
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    return
                elif speed_button.is_clicked(mouse_pos):
                    mechanics.show_speed_menu(screen)
                elif controls_button.is_clicked(mouse_pos):
                    mechanics.show_controls_menu(screen)

        for btn in buttons:
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    # start the game loop
    game_running = True
    while game_running:
        # draw the game state
        screen.fill(BLACK)
        mechanics.draw_board(screen, board)
        mechanics.draw_current_shape(screen, current_shape)
        mechanics.draw_next_shape(screen, next_shape)
        mechanics.draw_score(screen, score)
        pygame.display.flip()

        # handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mechanics.move_left(current_shape, board)
                elif event.key == pygame.K_RIGHT:
                    mechanics.move_right(current_shape, board)
                elif event.key == pygame.K_DOWN:
                    mechanics.drop(current_shape, board)
                elif event.key == pygame.K_UP:
                    mechanics.rotate(current_shape, board)

        # update the game state
        mechanics.update_game_state(current_shape, next_shape, board, score, level)
        clock.tick(FPS)

        # check for game over
        if mechanics.check_game_over(board):
            game_running = False

        # save the high score if necessary
        if score > mechanics.load_high_score():
            mechanics.save_high_score(score)
    pygame.quit()

if __name__ == "__main__":
    main()