from constants import *
import pygame

# button class
class Button:
    def __init__(self, x, y, width, height, text, color=None, text_color=None, hover_color=None, font_size=36, enabled=True):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color if color else (100,100,100) # gray default if none specified
        self.text_color = text_color if text_color else (255,255,255) # white default
        self.hover_color = hover_color if hover_color else (150,150,150) # light gray default
        self.font_size = font_size
        self.is_hovered = False
        self.enabled = enabled

        # disabled button appearance
        self.disabled_color = (70,70,70)
        self.disabled_text_color = (150,150,150)
        self.disabled_alpha = 128
        
    def draw(self, screen):
        # Choose the text color based on hover state and if button enabled
        # Defalut to color if not hovered
        if not self.enabled:
            current_color = self.disabled_color
            current_text_color = self.disabled_text_color
        else:
            current_color = self.hover_color if self.is_hovered else self.color
            current_text_color = self.text_color
        # Draw the button background
        pygame.draw.rect(screen, current_color, (self.x, self.y, self.width, self.height))
        # Draw the button border
        border_color = (100,100,100) if not self.enabled else WHITE
        pygame.draw.rect(screen, border_color, (self.x, self.y, self.width, self.height), 2)
        # Create the button font and render the text
        font = pygame.font.SysFont(None, self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        # position the text at the center of the button
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2)
        # Put the button on the screen
        screen.blit(text_surface, text_rect)
        # disabled button state
        if not self.enabled:
            # draw a semi transparent overlay
            overlay = pygame.surface((self.width, self.height))
            overlay.set_alpha(self.disabled_alpha)
            overlay.fill(BLACK)
            screen.blit(overlay, (self.x, self.y))

    def is_clicked(self, mouse_pos):
        # return true only if button enabled and clicked
        if not self.enabled:
            return False
        # check cursor collision
        x_in_range = self.x <= mouse_pos[0] <= self.x + self.width
        y_in_range = self.y <= mouse_pos[1] <= self.y + self.height
        return x_in_range and y_in_range

    def update_hover(self, mouse_pos):
        if not self.enabled:
            self.is_hovered = False
            return
        x_in_range = self.x <= mouse_pos[0] <= self.x + self.width
        y_in_range = self.y <= mouse_pos[1] <= self.y + self.height
        self.is_hovered = x_in_range and y_in_range
