import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen):
        # draw the button rectangle
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        # draw the button text
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.width) and (self.y <= mouse_pos[1] <= self.y + self.height)