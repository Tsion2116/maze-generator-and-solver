import pygame

#initalize pygame
pygame.init()

#game window dimensions and colors
WIDTH = 800
HEIGHT = 600

WHITE = (255,255,255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")

#Main loop
running = True

while running:
  screen.fill(WHITE)
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running=False
      
  pygame.display.update()
  
pygame.quit()
