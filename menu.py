import pygame
from button import Button
#------------------------------
# window setup
#------------------------------
pygame.init()
window = pygame.display.set_mode([800, 600])
pygame.display.set_caption('Schedule Optimizer')

#------------------------------
# colours
#------------------------------
GREY = (64, 60, 60)
DARKGREY = (38, 36, 36)

#------------------------------
# Functions
#------------------------------
def new_task ():
    pass


#------------------------------
# buttons
#------------------------------
# new task
add_task = Button(10, 10, 100, 50, "new task", GREY, DARKGREY, new_task)


#window loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
