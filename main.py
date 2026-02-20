from constants import *
import pygame
import button
import shapes
import mechanics

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
                
    # Start the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game logic and drawing code goes here

        pygame.display.flip()
        clock.tick(FPS)