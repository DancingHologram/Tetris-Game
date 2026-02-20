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
high_score = 0

# initialize pygame and create the game window
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# display the main menu with start, settings, scores, and quit buttons
# use mechanics to handle button clicks and navigate to the appropriate menu or start the game loop
def main_menu():
    start_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Start Game")
    settings_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Settings")
    scores_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "High Scores")
    quit_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200, 200, 50, "Quit")

    while True:
        screen.fill(BLACK)
        start_button.draw(screen)
        settings_button.draw(screen)
        scores_button.draw(screen)
        quit_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    game_loop()
                elif settings_button.is_clicked(mouse_pos):
                    settings_menu()
                elif scores_button.is_clicked(mouse_pos):
                    high_scores_menu()
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    return
        
        pygame.display.flip()
        clock.tick(FPS)


# display the settings menu with options to adjust game speed and controls
def settings_menu():
    speed_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Adjust Speed")
    controls_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Change Controls")
    back_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Back")

    while True:
        screen.fill(BLACK)
        speed_button.draw(screen)
        controls_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if speed_button.is_clicked(mouse_pos):
                    adjust_speed_menu()
                elif controls_button.is_clicked(mouse_pos):
                    change_controls_menu()
                elif back_button.is_clicked(mouse_pos):
                    return
        
        pygame.display.flip()
        clock.tick(FPS)

# display adjust speed menu with options to increase or decrease the game speed
def adjust_speed_menu():
    increase_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Increase Speed")
    decrease_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Decrease Speed")
    back_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Back")

    while True:
        screen.fill(BLACK)
        increase_button.draw(screen)
        decrease_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if increase_button.is_clicked(mouse_pos):
                    mechanics.increase_speed()
                elif decrease_button.is_clicked(mouse_pos):
                    mechanics.decrease_speed()
                elif back_button.is_clicked(mouse_pos):
                    return
        
        pygame.display.flip()
        clock.tick(FPS)

# display change controls menu with options to customize the game controls
def change_controls_menu():
    controls_surface = pygame.font.SysFont(None, 36).render("Control customization coming soon!", True, WHITE)
    controls_rect = controls_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    back_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Back")

    while True:
        screen.fill(BLACK)
        screen.blit(controls_surface, controls_rect)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button.is_clicked(mouse_pos):
                    return
                # add functionality to customize controls here
        
        pygame.display.flip()
        clock.tick(FPS)

# display the high scores menu from a binary file and allow the player to reset the high score
def high_scores_menu():
    global high_score
    reset_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Reset High Score")
    back_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Back")

    while True:
        screen.fill(BLACK)
        high_score_surface = pygame.font.SysFont(None, 36).render(f"High Score: {high_score}", True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(high_score_surface, high_score_rect)
        reset_button.draw(screen)
        back_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if reset_button.is_clicked(mouse_pos):
                    high_score = 0
                    mechanics.save_high_score(high_score)
                elif back_button.is_clicked(mouse_pos):
                    return
        
        pygame.display.flip()
        clock.tick(FPS)

# main game loop where the player controls the falling tetronimos and tries to clear lines to earn points
def game_loop():
    global current_shape, next_shape, score, level, high_score

    current_shape = shapes.get_random_shape()
    next_shape = shapes.get_random_shape()

    while True:
        screen.fill(BLACK)
        # draw the game board and current shape here

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                # add functionality to move and rotate the current shape here
                if event.key == pygame.K_LEFT:
                    mechanics.move_left(current_shape, board)
                elif event.key == pygame.K_RIGHT:
                    mechanics.move_right(current_shape, board)
                elif event.key == pygame.K_DOWN:
                    mechanics.move_down(current_shape, board)
                elif event.key == pygame.K_UP:
                    mechanics.rotate(current_shape, board)

        # add functionality to drop the current shape and check for line clears here
        mechanics.drop(current_shape)
        if mechanics.check_line_clears():
            score += 100
            if score > high_score:
                high_score = score
                mechanics.save_high_score(high_score)
            level = score // 1000 + 1

        # update the display and control the game speed
        mechanics.update_display(screen, board, current_shape, next_shape, score, level)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main_menu()