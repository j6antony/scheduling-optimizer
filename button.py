import pygame
class Button:
    def __init__(self, x, y, width, height, text, colour, hover, action):
        self.color = colour
        self.hover = hover
        self.current_colour = colour
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
    def draw (self, screen):
        pygame.draw.rect(screen, self.current_colour, self.rect, 3)
        text_surface = pygame.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    def clicked (self, event):
        if event == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint:
                self.action
            return True
        return False
    def hover (self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_colour = self.hover
        else:
            self.current_colour = self.color





