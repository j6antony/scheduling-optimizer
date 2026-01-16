import calendar
import json
from datetime import date
from pathlib import Path

import pygame

W, H = 900, 780

BG = (245, 245, 245)
GRID = (60, 60, 60)
TEXT = (20, 20, 20)
HEADER_BG = (220, 220, 220)
TODAY_BG = (255, 240, 180)
SEL_BG = (200, 230, 255)

BTN_BG = (200, 200, 200)
BTN_HOVER = (180, 180, 180)

PAD = 24
HEADER_H = 75
DOW_H = 32

calendar.setfirstweekday(calendar.MONDAY)
dow_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# ---- READ-ONLY EVENTS (fill these in however you want) ----
# Key: (year, month, day)
# Value: {"morning": "...", "afternoon": "...", "evening": "..."}
def load_events_from_json(filename="events.json"):
    try:
        path = Path(__file__).resolve().parent / filename
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    events = {}
    for key, slots in data.items():
        try:
            y, m, d = map(int, key.split("-"))
        except ValueError:
            continue
        events[(y, m, d)] = slots
    return events

# -----------------------------------------------------------

def run():
    pygame.init()

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Read-only Calendar (M/A/E)")

    font_big = pygame.font.SysFont(None, 44)
    font = pygame.font.SysFont(None, 24)
    font_small = pygame.font.SysFont(None, 16)

    today = date.today()
    year, month = today.year, today.month

    prev_btn = pygame.Rect(W - PAD - 210, PAD + 18, 90, 36)
    next_btn = pygame.Rect(W - PAD - 105, PAD + 18, 90, 36)
    events = load_events_from_json()

    def month_weeks(y, m):
        weeks = calendar.monthcalendar(y, m)
        weeks = [w for w in weeks if any(d != 0 for d in w)]
        return weeks

    def inc_month(y, m):
        m += 1
        if m == 13:
            m = 1
            y += 1
        return y, m

    def dec_month(y, m):
        m -= 1
        if m == 0:
            m = 12
            y -= 1
        return y, m

    def draw_button(rect, label):
        mx, my = pygame.mouse.get_pos()
        hover = rect.collidepoint(mx, my)
        pygame.draw.rect(screen, BTN_HOVER if hover else BTN_BG, rect, border_radius=8)
        pygame.draw.rect(screen, GRID, rect, 2, border_radius=8)
        surf = font.render(label, True, TEXT)
        screen.blit(surf, (rect.centerx - surf.get_width() / 2,
                           rect.centery - surf.get_height() / 2))

    def clip_text(s, max_chars):
        s = (s or "").strip()
        if len(s) > max_chars:
            return s[:max_chars - 1] + "…"
        return s

    def grid_layout(rows):
        grid_x = PAD
        grid_y = PAD + HEADER_H + DOW_H
        grid_w = W - 2 * PAD
        grid_h = H - grid_y - PAD - 30  # small footer margin
        cell_w = grid_w / 7
        cell_h = grid_h / rows
        return grid_x, grid_y, cell_w, cell_h

    def day_at_pos(y, m, pos):
        weeks = month_weeks(y, m)
        rows = len(weeks)
        grid_x, grid_y, cell_w, cell_h = grid_layout(rows)
        for r in range(rows):
            for c in range(7):
                rect = pygame.Rect(grid_x + c * cell_w, grid_y + r * cell_h,
                                   cell_w, cell_h)
                if rect.collidepoint(pos):
                    d = weeks[r][c]
                    if d != 0:
                        return d
        return None

    def draw(y, m, selected_day):
        screen.fill(BG)

        pygame.draw.rect(screen, HEADER_BG, (PAD, PAD, W - 2*PAD, HEADER_H),
                         border_radius=10)
        month_name = date(y, m, 1).strftime("%B %Y")
        title_surf = font_big.render(month_name, True, TEXT)
        screen.blit(title_surf, (PAD + 16, PAD + 18))

        draw_button(prev_btn, "Prev")
        draw_button(next_btn, "Next")

        weeks = month_weeks(y, m)
        rows = len(weeks)
        grid_x, grid_y, cell_w, cell_h = grid_layout(rows)

        # DOW labels
        for i, lab in enumerate(dow_labels):
            surf = font.render(lab, True, TEXT)
            screen.blit(surf, (grid_x + i * cell_w + 8, PAD + HEADER_H + 6))

        line_spacing = 16

        # Cells
        for r in range(rows):
            for c in range(7):
                rect = pygame.Rect(grid_x + c * cell_w, grid_y + r * cell_h,
                                   cell_w, cell_h)
                day_num = weeks[r][c]

                if day_num != 0 and today.year == y and today.month == m and today.day == day_num:
                    pygame.draw.rect(screen, TODAY_BG, rect)

                if day_num != 0 and selected_day == day_num:
                    pygame.draw.rect(screen, SEL_BG, rect)

                pygame.draw.rect(screen, GRID, rect, 2)

                if day_num != 0:
                    day_surf = font.render(str(day_num), True, TEXT)
                    screen.blit(day_surf, (rect.x + 6, rect.y + 4))

                    slots = events.get((y, m, day_num))
                    if slots:
                        lines = [
                            "M: " + clip_text(slots.get("morning", ""), 20),
                            "A: " + clip_text(slots.get("afternoon", ""), 20),
                            "E: " + clip_text(slots.get("evening", ""), 20),
                        ]
                        base_y = rect.y + 28
                        for i, line in enumerate(lines):
                            surf = font_small.render(line, True, TEXT)
                            screen.blit(surf, (rect.x + 6, base_y + i * line_spacing))

        pygame.display.flip()

    running = True
    clock = pygame.time.Clock()
    selected_day = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if next_btn.collidepoint(event.pos):
                    year, month = inc_month(year, month)
                    selected_day = None
                elif prev_btn.collidepoint(event.pos):
                    year, month = dec_month(year, month)
                    selected_day = None
                else:
                    d = day_at_pos(year, month, event.pos)
                    selected_day = d  # either a day number or None

        draw(year, month, selected_day)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    run()
