import pygame

class Button:
    def __init__(self, x, y, width, height, text, colour, hover_colour, action):
        self.color = colour
        self.hover_colour = hover_colour
        self.current_colour = colour

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

        self.font = pygame.font.SysFont(None, 24)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_colour, self.rect, 3)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_colour = self.hover_colour
        else:
            self.current_colour = self.color
