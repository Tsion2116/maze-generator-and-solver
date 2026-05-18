import pygame
import random

#initalize pygame
pygame.init()

#game window dimensions and colors
WIDTH = 800
HEIGHT = 600

WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 20)

#Grid dimensions
R=10
C=10
CELL_SIZE = 50

#wall arrays
north_wall = [[1] * C for i in range(R+1)]
east_wall = [[1] * (C+1) for i in range(R)]

#visited array to keep track of which cells have been visited during maze generation
visited = [[False] * C for _ in range(R)]

path = []

#starting position of the mouse in the maze
current_row = 0
current_col = 0

#mark the starting cell as visited
visited[current_row][current_col] = True

path.append((current_row, current_col))

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

# visualize the path taken during maze generation
def draw_path():

    if len(path) < 2:
        return

    for i in range(len(path) - 1):

        row1, col1 = path[i]
        row2, col2 = path[i + 1]

        x1 = START_X + col1 * CELL_SIZE + CELL_SIZE // 2
        y1 = START_Y + row1 * CELL_SIZE + CELL_SIZE // 2

        x2 = START_X + col2 * CELL_SIZE + CELL_SIZE // 2
        y2 = START_Y + row2 * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.line(
            screen,
            (0, 150, 0),
            (x1, y1),
            (x2, y2),
            4
        )
# the current dfs mouse cell will be drawn in red, and the visited cells will be drawn in light blue. The walls will be drawn in black. The maze will be generated using a depth-first search algorithm, and the walls will be removed as the algorithm progresses.

# the draw_coordinates function will display the row and column indices of each cell in the maze, which can be helpful for debugging and understanding the maze structure. The coordinates will be displayed in the top-left corner of each cell, and they will be updated as the maze is generated.
def draw_coordinates():

    for row in range(R):
        for col in range(C):

            text = font.render(
                f"{row},{col}",
                True,
                (0, 0, 0)
            )

            x = START_X + col * CELL_SIZE + 5
            y = START_Y + row * CELL_SIZE + 5

            screen.blit(text, (x, y))

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

# move to the next cell in the depth-first search algorithm, removing the wall between the current cell and the next cell. The function first gets a list of unvisited neighbors for the current cell, and if there are any, it randomly selects one of them as the next cell. It then removes the wall between the current cell and the next cell using the remove_wall function, updates the current row and column to the next cell's position, and marks the next cell as visited.
def move_to_next_cell():

    global current_row
    global current_col

    neighbors = get_unvisited_neighbors(current_row, current_col)

    if neighbors:

        next_row, next_col = random.choice(neighbors)

        remove_wall(current_row, current_col, next_row, next_col)

        current_row = next_row
        current_col = next_col

        visited[current_row][current_col] = True
        path.append((current_row, current_col))

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

# set the frames per second for the game loop, which controls how fast the maze is generated and displayed on the screen. A lower FPS will make the maze generation slower and more visually appealing, while a higher FPS will make it faster but less visually distinct. In this case, an FPS of 5 is chosen to allow for a clear visualization of the maze generation process.
FPS = 2

#Main loop
running = True

while running:
  screen.fill(WHITE)

  move_to_next_cell()

  draw_visited()
  draw_path()
  draw_current_cell()
  draw_coordinates()
  draw_maze()

  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running=False
    
    if event.type == pygame.KEYDOWN:

      if event.key == pygame.K_UP:
          FPS += 2

      elif event.key == pygame.K_DOWN:
          FPS = max(1, FPS - 2)
      
    
  pygame.display.update()
  clock.tick(FPS)
  
pygame.quit()
