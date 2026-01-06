import pygame
from button import Button
from task import Task
import json

# ------------------------------
# Window setup
# ------------------------------
pygame.init()
pygame.font.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Schedule Optimizer')
clock = pygame.time.Clock()

# ------------------------------
# Colors
# ------------------------------
GREY = (64, 60, 60)
DARKGREY = (38, 36, 36)

# ------------------------------
# State
# ------------------------------
task_panels = []  # store all TaskPanels
scroll_offset = 0
SCROLL_SPEED = 20  # pixels per scroll

# ------------------------------
# Functions
# ------------------------------
def new_task():
    global task_panels
    y_position = 80 + len(task_panels) * 150  # panel spacing
    panel = Task(position=(150, y_position), size=(500, 220))
    task_panels.append(panel)
def finished():
    global running
    # convert the data to rigth format
    print("saving tasks:", len(task_panels), task_panels)
    panels = []
    for panel in task_panels:
        panels.append(panel.convert_data())
    #write the data to a json file
    with open("tasks.json", "w") as file:
        json.dump(panels, file, indent=4)
    #close the current window
    running = False

# ------------------------------
# Buttons
# ------------------------------
add_task = Button(10, 10, 100, 50, "New Task", GREY, (120, 120, 120), new_task)
complete = Button(650, 10, 100, 50, "finished", GREY, (120, 120, 120), finished)
# ------------------------------
# Main loop
# ------------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Scroll wheel
        if event.type == pygame.MOUSEWHEEL:
            scroll_offset -= event.y * SCROLL_SPEED
            max_scroll = max(0, len(task_panels) * 150 - WINDOW_HEIGHT + 100)
            scroll_offset = max(0, min(scroll_offset, max_scroll))

        # Buttons and panels
        add_task.handle_event(event)
        complete.handle_event(event)
        for panel in task_panels:
            panel.handle_event(event)
        
    # --------------------------
    # Updates
    # --------------------------
    mouse_pos = pygame.mouse.get_pos()
    add_task.update_hover(mouse_pos)
    complete.update_hover(mouse_pos)
    # --------------------------
    # Drawing
    # --------------------------
    window.fill(DARKGREY)
    add_task.draw(window)
    complete.draw(window)

    for i, panel in enumerate(task_panels):
        # Adjust y position for scrolling
        base_y = 80 + i * 150
        panel.rect.y = base_y - scroll_offset
        # Only draw panels that are visible
        if -panel.rect.height < panel.rect.y < WINDOW_HEIGHT:
            panel.draw(window)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
