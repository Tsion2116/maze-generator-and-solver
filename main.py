import pygame

#initalize pygame
pygame.init()

#game window dimensions and colors
WIDTH = 800
HEIGHT = 600

WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")

#Grid dimensions
R=10
C=10
CELL_SIZE = 50

#wall arrays
north_wall = [[1] * C for i in range(R+1)]
east_wall = [[1] * (C+1) for i in range(R)]

#center the the grid starting 
START_X = (WIDTH - (C * CELL_SIZE)) // 2
START_Y = (HEIGHT - (R * CELL_SIZE)) //2

def draw_maze():
  for row in range(R):
    for col in range(C):

      x = START_X + col * CELL_SIZE
      y = START_Y + row * CELL_SIZE

      # Draw top wall
      if north_wall[row][col] == 1:
        pygame.draw.line(
          screen,
          BLACK,
          (x, y),
          (x + CELL_SIZE, y),
          2
        )

      # Draw right wall
      if east_wall[row][col] == 1:
        pygame.draw.line(
          screen,
          BLACK,
          (x + CELL_SIZE, y),
          (x + CELL_SIZE, y + CELL_SIZE),
          2
          )
    # Draw the bottom row edge
    for col in range(C):
      x = START_X + col * CELL_SIZE
      y = START_Y + R * CELL_SIZE
      
      if north_wall[R][col] == 1:
        pygame.draw.line(
          screen,
          BLACK,
          (x,y),
          (x + CELL_SIZE, y),
          2
        )
      
    #Draw the left column edge
    for row in range(R):
      x = START_X + 0
      y = START_Y + row * CELL_SIZE
      
      if east_wall[row][0] == 1:
        pygame.draw.line(
          screen,
          BLACK,
          (x,y),
          (x, y + CELL_SIZE),
          2
        ) 
    


#Main loop
running = True

while running:
  screen.fill(WHITE)
  draw_maze()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running=False
      
  pygame.display.update()
  
pygame.quit()
