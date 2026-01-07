import pygame
from button import Button
from datetime import date

class Task:
    def __init__(self, position, size):
        self.full_size = size
        self.collapsed_size = (size[0], 160)  # smaller height when collapsed
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(topleft=position)
        self.font = pygame.font.SysFont(None, 24)

        # Task input state
        self.task_text = ""
        self.date_text = ""
        self.duration_text = ""
        self.active_task = False
        self.active_date = False
        self.active_duration = False
        self.availability = None

        # Panel state
        self.collapsed = False

        # UI Rects
        self.task_box = pygame.Rect(20, 20, size[0]-40, 40)
        self.date_box = pygame.Rect(20, 80, 200, 40)
        self.duration_box = pygame.Rect(240, 80, 100, 40)

        self.buttons = {
            "Morning": pygame.Rect(20, 140, 100, 40),
            "Afternoon": pygame.Rect(130, 140, 120, 40),
            "Evening": pygame.Rect(260, 140, 100, 40),
        }

        # Done button
        self.done_button = Button(
            x=size[0]-120, y=size[1]-60, width=100, height=40,
            text="Done", colour=(180,180,180), hover_colour=(0,255,0),
            action=self.toggle_collapse
        )

    def toggle_collapse(self):
        self.collapsed = not self.collapsed
        if self.collapsed:
            self.surface = pygame.Surface(self.collapsed_size)
            self.rect.height = self.collapsed_size[1]
            self.done_button.rect.topleft = (self.collapsed_size[0]-120, self.collapsed_size[1]-60)
        else:
            self.surface = pygame.Surface(self.full_size)
            self.rect.height = self.full_size[1]
            self.done_button.rect.topleft = (self.full_size[0]-120, self.full_size[1]-60)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            local_mouse = (event.pos[0]-self.rect.x, event.pos[1]-self.rect.y)
            self.done_button.handle_event_local(local_mouse, event.type)

        if self.collapsed:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse(event.pos)
        if event.type == pygame.KEYDOWN:
            self._handle_keys(event)

    def _handle_mouse(self, mouse_pos):
        local = (mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y)
        self.active_task = self.task_box.collidepoint(local)
        self.active_date = self.date_box.collidepoint(local)
        self.active_duration = self.duration_box.collidepoint(local)

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

        if self.active_duration:
            if event.key == pygame.K_BACKSPACE:
                self.duration_text = self.duration_text[:-1]
            elif event.unicode.isdigit():
                self.duration_text += event.unicode

    def draw(self, screen):
        self.surface.fill((30,30,30))
        if self.collapsed:
            self._draw_collapsed()
        else:
            self._draw_task_box()
            self._draw_date_box()
            self._draw_duration_box()
            self._draw_buttons()

        # Done button
        mouse_pos = pygame.mouse.get_pos()
        local_mouse = (mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y)
        self.done_button.update_hover(local_mouse)
        self.done_button.draw(self.surface)

        screen.blit(self.surface, self.rect)

    def _draw_task_box(self):
        color = (200,200,200) if self.active_task else (120,120,120)
        pygame.draw.rect(self.surface, color, self.task_box, 2)
        text = self.task_text or "Enter task..."
        txt_surf = self.font.render(text, True, (255,255,255))
        self.surface.blit(txt_surf, (self.task_box.x+5, self.task_box.y+10))

    def _draw_date_box(self):
        color = (200,200,200) if self.active_date else (120,120,120)
        pygame.draw.rect(self.surface, color, self.date_box, 2)
        text = self.date_text or "Due date YYYY-MM-DD"
        txt_surf = self.font.render(text, True, (255,255,255))
        self.surface.blit(txt_surf, (self.date_box.x+5, self.date_box.y+10))

    def _draw_duration_box(self):
        color = (200,200,200) if self.active_duration else (120,120,120)
        pygame.draw.rect(self.surface, color, self.duration_box, 2)
        text = self.duration_text or "Duration (times)"
        txt_surf = self.font.render(text, True, (255,255,255))
        self.surface.blit(txt_surf, (self.duration_box.x+5, self.duration_box.y+10))

    def _draw_buttons(self):
        for label, rect in self.buttons.items():
            selected = self.availability == label
            color = (0,180,0) if selected else (100,100,100)
            pygame.draw.rect(self.surface, color, rect)
            txt = self.font.render(label, True, (0,0,0))
            self.surface.blit(txt, txt.get_rect(center=rect.center))

    def _draw_collapsed(self):
        lines = [
            f"Task: {self.task_text or '[empty]'}",
            f"Due: {self.date_text or '[empty]'}",
            f"Duration: {self.duration_text or '[empty]'}",
            f"Availability: {self.availability or '[none]'}"
        ]
        y = 20
        for line in lines:
            txt_surf = self.font.render(line, True, (255,255,255))
            self.surface.blit(txt_surf, (20, y))
            y += 30

    # Save/load support
    def to_dict(self):
        return {
            "task_text": self.task_text,
            "date_text": self.date_text,
            "duration": self.duration_text,
            "availability": self.availability,
            "collapsed": self.collapsed
        }

    @classmethod
    def from_dict(cls, data, position):
        panel = cls(position, (500,220))
        panel.task_text = data.get("task_text","")
        panel.date_text = data.get("date_text","")
        panel.duration_text = data.get("duration","")
        panel.availability = data.get("availability", None)
        if data.get("collapsed", False):
            panel.toggle_collapse()
        return panel
    def convert_data(self):
        return{
            "name": self.task_text,
            "due": date.fromisoformat(self.date_text),
            "duration": int(self.duration_text) if self.duration_text else 0, # done to handle edge case
            "availability": [self.availability]
        }
