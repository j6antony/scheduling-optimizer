import pygame
from button import Button
from datetime import date

class Task:
    def __init__(self, position, size):
        self.full_size = size
        self.collapsed_size = (size[0], 190)
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.surface.get_rect(topleft=position)
        self.title_font = pygame.font.SysFont("georgia", 26, bold=True)
        self.label_font = pygame.font.SysFont("georgia", 18, bold=True)
        self.font = pygame.font.SysFont("georgia", 22)
        self.meta_font = pygame.font.SysFont("georgia", 18)

        self.palette = {
            "card": (241, 232, 216),
            "card_dark": (224, 209, 184),
            "shadow": (22, 24, 30),
            "ink": (36, 34, 32),
            "muted": (101, 95, 87),
            "field": (255, 249, 240),
            "field_border": (199, 171, 122),
            "active": (199, 103, 56),
            "accent": (150, 59, 43),
            "accent_soft": (210, 150, 96),
            "chip": (219, 202, 176),
            "chip_selected": (211, 121, 72),
            "chip_text": (47, 35, 25),
        }

        # Task input state
        self.task_text = ""
        self.date_text = ""
        self.duration_text = ""
        self.active_task = False
        self.active_date = False
        self.active_duration = False
        self.availability = []

        # Panel state
        self.collapsed = False

        # UI Rects
        self.task_box = pygame.Rect(20, 92, size[0] - 60, 48)
        self.date_box = pygame.Rect(20, 166, 240, 48)
        self.duration_box = pygame.Rect(278, 166, 140, 48)

        self.buttons = {
            "Morning": pygame.Rect(20, 238, 120, 44),
            "Afternoon": pygame.Rect(154, 238, 140, 44),
            "Evening": pygame.Rect(308, 238, 120, 44),
        }

        # Done button
        self.done_button = Button(
            x=size[0]-130, y=size[1]-64, width=110, height=44,
            text="Done",
            colour=(232, 176, 118),
            hover_colour=(243, 195, 145),
            action=self.toggle_collapse,
            text_colour=(55, 37, 24),
            border_colour=(255, 238, 214),
        )

    def toggle_collapse(self):
        self.collapsed = not self.collapsed
        if self.collapsed:
            self.surface = pygame.Surface(self.collapsed_size, pygame.SRCALPHA)
            self.rect.height = self.collapsed_size[1]
            self.done_button.rect.topleft = (self.collapsed_size[0]-130, self.collapsed_size[1]-64)
        else:
            self.surface = pygame.Surface(self.full_size, pygame.SRCALPHA)
            self.rect.height = self.full_size[1]
            self.done_button.rect.topleft = (self.full_size[0]-130, self.full_size[1]-64)

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
                if label in self.availability:
                    self.availability.remove(label)
                else:
                    self.availability.append(label)

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
        self.surface.fill((0, 0, 0, 0))
        self._draw_card()
        if self.collapsed:
            self._draw_collapsed()
        else:
            self._draw_task_box()
            self._draw_date_box()
            self._draw_duration_box()
            self._draw_buttons()

        mouse_pos = pygame.mouse.get_pos()
        local_mouse = (mouse_pos[0]-self.rect.x, mouse_pos[1]-self.rect.y)
        self.done_button.update_hover(local_mouse)
        self.done_button.draw(self.surface)

        screen.blit(self.surface, self.rect)

    def _draw_card(self):
        shadow_rect = pygame.Rect(10, 12, self.rect.width - 20, self.rect.height - 12)
        pygame.draw.rect(self.surface, self.palette["shadow"], shadow_rect, border_radius=28)

        card_rect = pygame.Rect(0, 0, self.rect.width - 20, self.rect.height - 14)
        pygame.draw.rect(self.surface, self.palette["card"], card_rect, border_radius=28)
        pygame.draw.rect(self.surface, self.palette["card_dark"], card_rect, width=2, border_radius=28)

        accent_rect = pygame.Rect(0, 0, card_rect.width, 56)
        pygame.draw.rect(self.surface, self.palette["accent"], accent_rect, border_radius=28)
        accent_fill = pygame.Rect(0, 28, card_rect.width, 30)
        pygame.draw.rect(self.surface, self.palette["accent"], accent_fill)

        title = self.title_font.render(self.task_text or "Untitled Focus Block", True, (250, 243, 232))
        subtitle = self.meta_font.render("Plan the work before the deadline.", True, (244, 214, 188))
        self.surface.blit(title, (24, 16))
        self.surface.blit(subtitle, (24, 48))

    def _draw_input_field(self, rect, label, text, placeholder, active):
        label_surface = self.label_font.render(label, True, self.palette["muted"])
        self.surface.blit(label_surface, (rect.x, rect.y - 24))

        fill_colour = self.palette["field"] if not active else (255, 246, 235)
        border_colour = self.palette["active"] if active else self.palette["field_border"]
        pygame.draw.rect(self.surface, fill_colour, rect, border_radius=18)
        pygame.draw.rect(self.surface, border_colour, rect, width=2, border_radius=18)

        display_text = text or placeholder
        text_colour = self.palette["ink"] if text else self.palette["muted"]
        text_surface = self.font.render(display_text, True, text_colour)
        self.surface.blit(text_surface, (rect.x + 14, rect.y + 11))

    def _draw_task_box(self):
        self._draw_input_field(
            self.task_box,
            "Task Name",
            self.task_text,
            "Enter a task you need to finish",
            self.active_task,
        )

    def _draw_date_box(self):
        self._draw_input_field(
            self.date_box,
            "Due Date",
            self.date_text,
            "YYYY-MM-DD",
            self.active_date,
        )

    def _draw_duration_box(self):
        self._draw_input_field(
            self.duration_box,
            "Sessions",
            self.duration_text,
            "0",
            self.active_duration,
        )

    def _draw_buttons(self):
        label_surface = self.label_font.render("Available Time Blocks", True, self.palette["muted"])
        self.surface.blit(label_surface, (20, 214))

        for label, rect in self.buttons.items():
            selected = label in self.availability
            color = self.palette["chip_selected"] if selected else self.palette["chip"]
            border = self.palette["accent"] if selected else self.palette["field_border"]
            pygame.draw.rect(self.surface, color, rect, border_radius=18)
            pygame.draw.rect(self.surface, border, rect, width=2, border_radius=18)
            txt = self.meta_font.render(label, True, self.palette["chip_text"])
            self.surface.blit(txt, txt.get_rect(center=rect.center))

    def _draw_collapsed(self):
        summary_title = self.label_font.render("Task Summary", True, self.palette["muted"])
        self.surface.blit(summary_title, (20, 76))
        lines = [
            f"Task: {self.task_text or '[empty]'}",
            f"Due: {self.date_text or '[empty]'}",
            f"Sessions: {self.duration_text or '[empty]'}",
            f"Availability: {', '.join(self.availability) or '[none]'}",
        ]
        y = 102
        for line in lines:
            txt_surf = self.meta_font.render(line, True, self.palette["ink"])
            self.surface.blit(txt_surf, (20, y))
            y += 24

    # Save/load support
    def to_dict(self):
        due = None
        if self.date_text:
            if isinstance(self.date_text, date):
                due = self.date_text
            else:
                try:
                    due = date.fromisoformat(self.date_text)
                except ValueError:
                    due = None

        duration = self.duration_text
        if isinstance(duration, str):
            duration = int(duration) if duration.isdigit() else 0
        else:
            duration = int(duration) if duration is not None else 0

        return {
            "name": self.task_text,
            "due": due,
            "duration": duration,
            "availability": self.availability or []
        }

    @classmethod
    def from_dict(cls, data, position):
        panel = cls(position, (840, 330))
        panel.task_text = data.get("task_text") or data.get("name", "")
        due = data.get("date_text") or data.get("due", "")
        if isinstance(due, date):
            panel.date_text = due.isoformat()
        elif due is None:
            panel.date_text = ""
        else:
            panel.date_text = str(due)

        duration = data.get("duration", "")
        panel.duration_text = str(duration) if duration is not None else ""
        availability = data.get("availability", [])
        panel.availability = availability if isinstance(availability, list) else [availability]
        if data.get("collapsed", False):
            panel.toggle_collapse()
        return panel
