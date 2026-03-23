import pygame
from button import Button
from task import Task
import json

pygame.init()
pygame.font.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 820
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Schedule Optimizer')
clock = pygame.time.Clock()

BACKGROUND_TOP = (24, 33, 52)
BACKGROUND_BOTTOM = (243, 230, 212)
SIDEBAR = (33, 45, 69)
SIDEBAR_EDGE = (67, 86, 118)
SIDEBAR_TEXT = (245, 238, 226)
SIDEBAR_MUTED = (203, 196, 184)
CONTENT_HINT = (102, 93, 81)
CONTENT_TITLE = (49, 43, 35)
GLOW_ONE = (185, 111, 74)
GLOW_TWO = (122, 156, 185)

HEADER_FONT = pygame.font.SysFont("georgia", 54, bold=True)
SUBTITLE_FONT = pygame.font.SysFont("georgia", 24)
SECTION_FONT = pygame.font.SysFont("georgia", 26, bold=True)
BODY_FONT = pygame.font.SysFont("georgia", 20)
META_FONT = pygame.font.SysFont("georgia", 18)

SIDEBAR_RECT = pygame.Rect(32, 28, 320, WINDOW_HEIGHT - 56)
CONTENT_X = 392
CONTENT_TOP = 180
PANEL_GAP = 28
PANEL_SIZE = (840, 330)

task_panels = []
scroll_offset = 0
SCROLL_SPEED = 48

def new_task():
    y_position = CONTENT_TOP + len(task_panels) * (PANEL_SIZE[1] + PANEL_GAP)
    panel = Task(position=(CONTENT_X, y_position), size=PANEL_SIZE)
    task_panels.append(panel)


def total_content_height():
    if not task_panels:
        return 0
    panel_height = sum(panel.rect.height for panel in task_panels)
    return panel_height + PANEL_GAP * (len(task_panels) - 1)


def clamp_scroll():
    global scroll_offset
    visible_height = WINDOW_HEIGHT - CONTENT_TOP - 40
    max_scroll = max(0, total_content_height() - visible_height)
    scroll_offset = max(0, min(scroll_offset, max_scroll))


def finished():
    global running
    panels = []
    for panel in task_panels:
        panels.append(panel.to_dict())
    with open("tasks.json", "w") as file:
        json.dump(panels, file, indent=4, default=str)
    running = False


def draw_vertical_gradient(surface, top_colour, bottom_colour):
    height = surface.get_height()
    width = surface.get_width()
    for y in range(height):
        blend = y / max(1, height - 1)
        colour = (
            int(top_colour[0] + (bottom_colour[0] - top_colour[0]) * blend),
            int(top_colour[1] + (bottom_colour[1] - top_colour[1]) * blend),
            int(top_colour[2] + (bottom_colour[2] - top_colour[2]) * blend),
        )
        pygame.draw.line(surface, colour, (0, y), (width, y))


def draw_background(surface):
    draw_vertical_gradient(surface, BACKGROUND_TOP, BACKGROUND_BOTTOM)
    pygame.draw.circle(surface, GLOW_ONE, (1060, 100), 180)
    pygame.draw.circle(surface, GLOW_TWO, (1010, 680), 220)
    pygame.draw.circle(surface, (241, 200, 155), (540, 760), 140)


def draw_sidebar(surface):
    shadow_rect = SIDEBAR_RECT.move(0, 10)
    pygame.draw.rect(surface, (16, 24, 39), shadow_rect, border_radius=34)
    pygame.draw.rect(surface, SIDEBAR, SIDEBAR_RECT, border_radius=34)
    pygame.draw.rect(surface, SIDEBAR_EDGE, SIDEBAR_RECT, width=2, border_radius=34)

    badge_rect = pygame.Rect(SIDEBAR_RECT.x + 24, SIDEBAR_RECT.y + 26, 118, 34)
    pygame.draw.rect(surface, (219, 141, 87), badge_rect, border_radius=17)
    badge_text = META_FONT.render("Daily Planner", True, (42, 31, 23))
    surface.blit(badge_text, badge_text.get_rect(center=badge_rect.center))

    title = HEADER_FONT.render("Calendar", True, SIDEBAR_TEXT)
    subtitle = SUBTITLE_FONT.render("Shape your week into deliberate work blocks.", True, SIDEBAR_MUTED)
    surface.blit(title, (SIDEBAR_RECT.x + 24, SIDEBAR_RECT.y + 78))
    surface.blit(subtitle, (SIDEBAR_RECT.x + 24, SIDEBAR_RECT.y + 144))

    section_title = SECTION_FONT.render("Overview", True, SIDEBAR_TEXT)
    surface.blit(section_title, (SIDEBAR_RECT.x + 24, SIDEBAR_RECT.y + 220))

    stats = [
        ("Tasks", str(len(task_panels))),
        ("Scroll", f"{scroll_offset}px"),
        ("Mode", "Planning"),
    ]

    stat_y = SIDEBAR_RECT.y + 266
    for label, value in stats:
        card_rect = pygame.Rect(SIDEBAR_RECT.x + 24, stat_y, SIDEBAR_RECT.width - 48, 74)
        pygame.draw.rect(surface, (47, 62, 90), card_rect, border_radius=22)
        pygame.draw.rect(surface, (92, 116, 153), card_rect, width=1, border_radius=22)
        label_surface = META_FONT.render(label, True, SIDEBAR_MUTED)
        value_surface = SECTION_FONT.render(value, True, SIDEBAR_TEXT)
        surface.blit(label_surface, (card_rect.x + 18, card_rect.y + 14))
        surface.blit(value_surface, (card_rect.x + 18, card_rect.y + 34))
        stat_y += 88

    notes_title = SECTION_FONT.render("How It Works", True, SIDEBAR_TEXT)
    notes_body = [
        "Add each task as a card.",
        "Select every time block the task can use.",
        "Collapse cards when the details are set.",
    ]
    surface.blit(notes_title, (SIDEBAR_RECT.x + 24, SIDEBAR_RECT.y + 560))
    text_y = SIDEBAR_RECT.y + 606
    for line in notes_body:
        body_surface = BODY_FONT.render(line, True, SIDEBAR_MUTED)
        surface.blit(body_surface, (SIDEBAR_RECT.x + 24, text_y))
        text_y += 34


def draw_content_header(surface):
    title = HEADER_FONT.render("Build Your Schedule", True, CONTENT_TITLE)
    subtitle = SUBTITLE_FONT.render(
        "Create rich task cards and define when each one can be completed.",
        True,
        CONTENT_HINT,
    )
    surface.blit(title, (CONTENT_X, 42))
    surface.blit(subtitle, (CONTENT_X, 108))

    hint = BODY_FONT.render("Tip: choose multiple availability windows for more flexible scheduling.", True, CONTENT_HINT)
    surface.blit(hint, (CONTENT_X, 142))


def draw_empty_state(surface):
    card_rect = pygame.Rect(CONTENT_X, CONTENT_TOP + 24, PANEL_SIZE[0], 240)
    shadow_rect = card_rect.move(0, 10)
    pygame.draw.rect(surface, (55, 45, 39), shadow_rect, border_radius=30)
    pygame.draw.rect(surface, (245, 236, 221), card_rect, border_radius=30)
    pygame.draw.rect(surface, (202, 177, 138), card_rect, width=2, border_radius=30)

    title = SECTION_FONT.render("No tasks yet", True, CONTENT_TITLE)
    body = BODY_FONT.render("Use New Task to create your first planning card.", True, CONTENT_HINT)
    surface.blit(title, (card_rect.x + 28, card_rect.y + 78))
    surface.blit(body, (card_rect.x + 28, card_rect.y + 118))


add_task = Button(
    930,
    46,
    150,
    54,
    "New Task",
    (232, 170, 103),
    (244, 191, 129),
    new_task,
    text_colour=(50, 34, 23),
    border_colour=(255, 231, 204),
)
complete = Button(
    1092,
    46,
    150,
    54,
    "Save",
    (139, 89, 70),
    (165, 109, 88),
    finished,
    text_colour=(249, 241, 232),
    border_colour=(223, 190, 170),
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            scroll_offset -= event.y * SCROLL_SPEED
            clamp_scroll()

        add_task.handle_event(event)
        complete.handle_event(event)
        for panel in task_panels:
            panel.handle_event(event)

    mouse_pos = pygame.mouse.get_pos()
    add_task.update_hover(mouse_pos)
    complete.update_hover(mouse_pos)
    clamp_scroll()

    draw_background(window)
    draw_sidebar(window)
    draw_content_header(window)
    add_task.draw(window)
    complete.draw(window)

    if not task_panels:
        draw_empty_state(window)

    y_cursor = CONTENT_TOP - scroll_offset
    for panel in task_panels:
        panel.rect.x = CONTENT_X
        panel.rect.y = y_cursor
        if -panel.rect.height < panel.rect.y < WINDOW_HEIGHT:
            panel.draw(window)
        y_cursor += panel.rect.height + PANEL_GAP

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
