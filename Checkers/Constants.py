import pygame

NUM = int(input("What are your dimensions:"))

rowscols = int(input("How many rows and columns:"))

WIDTH, HEIGHT = NUM, NUM
ROWS, COLS = rowscols, rowscols
SQUARE_SIZE = WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
