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

    # Draw the menu screen and wait for the player to click the start button
    high_score = 0
    start_button, quit_button = mechanics.draw_menu(screen, high_score)
    pygame.display.flip()
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting_for_start = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.is_clicked(mouse_pos):
                    waiting_for_start = False
                elif quit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    return
    
    # check if the player has a saved high score and load it
    try:
        with open('high_score.bin', 'r') as f:
            high_score = int(f.read())
    except FileNotFoundError:
        high_score = 0