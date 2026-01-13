# ----------------- imports
import pygame
import datetime
import calendar
# ----------------- basic info
current_date = datetime.datetime.now()
YEAR = current_date.year
MONTH = current_date.month

# ----------------- calender display stuff

width, height = 900, 650
window = pygame.display.set_mode((width, height))
pygame.display.set_catpion()

