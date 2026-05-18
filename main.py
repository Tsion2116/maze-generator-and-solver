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

#visited array to keep track of which cells have been visited during maze generation
visited = [[False] * C for _ in range(R)]

#starting position of the mouse in the maze
current_row = 0
current_col = 0

#mark the starting cell as visited
visited[current_row][current_col] = True

#center the the grid starting 
START_X = (WIDTH - (C * CELL_SIZE)) // 2
START_Y = (HEIGHT - (R * CELL_SIZE)) //2

# check if a cell is within the grid bounds
def in_bounds(row, col):
    return 0 <= row < R and 0 <= col < C

def remove_wall(current_row, current_col, next_row, next_col):

    # moving UP
    if next_row == current_row - 1:
        north_wall[current_row][current_col] = 0

    # moving DOWN
    elif next_row == current_row + 1:
        north_wall[current_row + 1][current_col] = 0

    # moving RIGHT
    elif next_col == current_col + 1:
        east_wall[current_row][current_col + 1] = 0

    # moving LEFT
    elif next_col == current_col - 1:
        east_wall[current_row][current_col] = 0

# visualize the visited cells during maze generation        
def draw_visited():

    for row in range(R):
        for col in range(C):

            if visited[row][col]:

                x = START_X + col * CELL_SIZE
                y = START_Y + row * CELL_SIZE

                pygame.draw.rect(
                    screen,
                    (200, 200, 255),
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

# visualize the current cell being processed during maze generation
def draw_current_cell():

    x = START_X + current_col * CELL_SIZE
    y = START_Y + current_row * CELL_SIZE

    pygame.draw.rect(
        screen,
        (255, 100, 100),
        (x, y, CELL_SIZE, CELL_SIZE)
    )

# the current dfs mouse cell will be drawn in red, and the visited cells will be drawn in light blue. The walls will be drawn in black. The maze will be generated using a depth-first search algorithm, and the walls will be removed as the algorithm progresses.

# get a list of unvisited neighbors for a given cell
def get_unvisited_neighbors(row, col):

    neighbors = [] # list to store unvisited neighbors

    # UP
    if in_bounds(row - 1, col):
        if not visited[row - 1][col]:
            neighbors.append((row - 1, col))

    # DOWN
    if in_bounds(row + 1, col):
        if not visited[row + 1][col]:
            neighbors.append((row + 1, col))

    # LEFT
    if in_bounds(row, col - 1):
        if not visited[row][col - 1]:
            neighbors.append((row, col - 1))

    # RIGHT
    if in_bounds(row, col + 1):
        if not visited[row][col + 1]:
            neighbors.append((row, col + 1))

    return neighbors
# this will return a list of unvisited neighbors for the current cell, which will be used in the depth-first search algorithm to generate the maze. The function checks each of the four possible directions (up, down, left, right) and adds any unvisited neighbors to the list.

def draw_maze():
  # draw internal walls
  for row in range(R):
    for col in range(C):

      x = START_X + col * CELL_SIZE
      y = START_Y + row * CELL_SIZE

      # Draw top wall
      if north_wall[row + 1][col] == 1:
        pygame.draw.line(
          screen,
          BLACK,
          (x, y),
          (x + CELL_SIZE, y),
          2
        )

      # Draw right wall
      if east_wall[row][col + 1] == 1:
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

  draw_visited()
  draw_current_cell()
  draw_maze()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running=False
      
  pygame.display.update()
  
pygame.quit()
