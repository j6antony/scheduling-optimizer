import pygame

class Task:
    def __init__(self, position, size):
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(topleft=position)

        self.font = pygame.font.SysFont(None, 24)

        # ------------------
        # Input state
        # ------------------
        self.task_text = ""
        self.date_text = ""
        self.active_task = False
        self.active_date = False
        self.availability = None

        # ------------------
        # UI Rects (panel-space)
        # ------------------
        self.task_box = pygame.Rect(20, 20, size[0] - 40, 40)
        self.date_box = pygame.Rect(20, 80, 200, 40)

        self.buttons = {
            "Morning": pygame.Rect(240, 80, 100, 40),
            "Afternoon": pygame.Rect(350, 80, 120, 40),
            "Evening": pygame.Rect(20, 140, 100, 40),
        }

    # ------------------
    # Event handling
    # ------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse(event.pos)

        if event.type == pygame.KEYDOWN:
            self._handle_keys(event)

    def _handle_mouse(self, mouse_pos):
        local = (mouse_pos[0] - self.rect.x,
                 mouse_pos[1] - self.rect.y)

        self.active_task = self.task_box.collidepoint(local)
        self.active_date = self.date_box.collidepoint(local)

        for label, rect in self.buttons.items():
            if rect.collidepoint(local):
                self.availability = label

    def _handle_keys(self, event):
        if self.active_task:
            if event.key == pygame.K_BACKSPACE:
                self.task_text = self.task_text[:-1]
            else:
                self.task_text += event.unicode

        if self.active_date:
            if event.key == pygame.K_BACKSPACE:
                self.date_text = self.date_text[:-1]
            else:
                self.date_text += event.unicode

    # ------------------
    # Drawing
    # ------------------
    def draw(self, screen):
        self.surface.fill((30, 30, 30))
        self._draw_task_box()
        self._draw_date_box()
        self._draw_buttons()
        screen.blit(self.surface, self.rect)

    def _draw_task_box(self):
        color = (200, 200, 200) if self.active_task else (120, 120, 120)
        pygame.draw.rect(self.surface, color, self.task_box, 2)

        text = self.task_text or "Enter task..."
        txt_surf = self.font.render(text, True, (255, 255, 255))
        self.surface.blit(txt_surf, (self.task_box.x + 5, self.task_box.y + 10))

    def _draw_date_box(self):
        color = (200, 200, 200) if self.active_date else (120, 120, 120)
        pygame.draw.rect(self.surface, color, self.date_box, 2)

        text = self.date_text or "Due date (YYYY-MM-DD)"
        txt_surf = self.font.render(text, True, (255, 255, 255))
        self.surface.blit(txt_surf, (self.date_box.x + 5, self.date_box.y + 10))

    def _draw_buttons(self):
        for label, rect in self.buttons.items():
            selected = self.availability == label
            color = (0, 180, 0) if selected else (100, 100, 100)

            pygame.draw.rect(self.surface, color, rect)
            txt = self.font.render(label, True, (0, 0, 0))
            self.surface.blit(txt, txt.get_rect(center=rect.center))

    # ------------------
    # Data access
    # ------------------
    def get_task_data(self):
        return {
            "task": self.task_text,
            "due_date": self.date_text,
            "availability": self.availability
        }

    def clear(self):
        self.task_text = ""
        self.date_text = ""
        self.availability = None
