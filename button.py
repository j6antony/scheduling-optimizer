import pygame

class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        colour,
        hover_colour,
        action,
        text_colour=(22, 28, 36),
        border_colour=(255, 255, 255),
    ):
        self.color = colour
        self.hover_colour = hover_colour
        self.current_colour = colour
        self.text_colour = text_colour
        self.border_colour = border_colour

        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

        self.font = pygame.font.SysFont("georgia", 24, bold=True)

    def draw(self, screen):
        shadow_rect = self.rect.move(0, 6)
        pygame.draw.rect(screen, (13, 18, 25), shadow_rect, border_radius=18)
        pygame.draw.rect(screen, self.current_colour, self.rect, border_radius=18)
        pygame.draw.rect(screen, self.border_colour, self.rect, width=2, border_radius=18)

        highlight_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 5, self.rect.width - 12, max(8, self.rect.height // 3))
        pygame.draw.rect(screen, (255, 236, 214), highlight_rect, border_radius=14)

        text_surface = self.font.render(self.text, True, self.text_colour)
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

    # -----------------------------
    # NEW METHOD
    # -----------------------------
    def handle_event_local(self, local_pos, event_type=pygame.MOUSEBUTTONDOWN):
        if event_type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(local_pos):
                self.action()
