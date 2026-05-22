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

#starting position of the generator in the maze
current_row = random.randint(0, R - 1)
current_col = random.randint(0, C - 1)

maze_complete = False

entrance_created = False

# solver variables
solver_row = 0
solver_col = 0

solver_stack = []

solver_visited = set()

dead_ends = []

solver_started = False
solver_finished = False


#visited set to keep track of which cells have been visited during maze generation
visited = set()
stack = []
stack.append((current_row, current_col))
visited.add((current_row, current_col))

#center the the grid starting 
START_X = (WIDTH - (C * CELL_SIZE)) // 2
START_Y = (HEIGHT - (R * CELL_SIZE)) //2

# check if a cell is within the grid bounds
def in_bounds(row, col):
    return 0 <= row < R and 0 <= col < C

def remove_wall(current_row, current_col, next_row, next_col):

    # move UP
    if next_row == current_row - 1:
        north_wall[current_row][current_col] = 0

    # move DOWN
    elif next_row == current_row + 1:
        north_wall[current_row + 1][current_col] = 0

    # move LEFT
    elif next_col == current_col - 1:
        east_wall[current_row][current_col] = 0

    # move RIGHT
    elif next_col == current_col + 1:
        east_wall[current_row][current_col + 1] = 0

#for the solver wall check functions
def can_move_up(row, col):
    return north_wall[row][col] == 0

def can_move_down(row, col):
    return north_wall[row + 1][col] == 0

def can_move_left(row, col):
    return east_wall[row][col] == 0

def can_move_right(row, col):
    return east_wall[row][col + 1] == 0

# visualize the visited cells during maze generation        
def draw_visited():

    for row in range(R):
        for col in range(C):

            if (row, col) in visited:

                x = START_X + col * CELL_SIZE
                y = START_Y + row * CELL_SIZE

                pygame.draw.rect(
                    screen,
                    (200, 200, 255),
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

# visualize the current cell being processed during maze generation
def draw_current_cell():

    if not stack:
        return

    row, col = stack[-1]

    x = START_X + col * CELL_SIZE
    y = START_Y + row * CELL_SIZE

    pygame.draw.rect(
        screen,
        (255, 100, 100),
        (x, y, CELL_SIZE, CELL_SIZE)
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
        if (row - 1, col) not in visited:
            neighbors.append((row - 1, col))

    # DOWN
    if in_bounds(row + 1, col):
        if (row + 1, col) not in visited:
            neighbors.append((row + 1, col))

    # LEFT
    if in_bounds(row, col - 1):
        if (row, col - 1) not in visited:
            neighbors.append((row, col - 1))

    # RIGHT
    if in_bounds(row, col + 1):
        if (row, col + 1) not in visited:
            neighbors.append((row, col + 1))

    return neighbors

def get_solver_neighbors(row, col):

    neighbors = []

    # UP
    if in_bounds(row - 1, col):
        if can_move_up(row, col) and (row - 1, col) not in solver_visited:
            neighbors.append((row - 1, col))

    # DOWN
    if in_bounds(row + 1, col):
        if can_move_down(row, col) and (row + 1, col) not in solver_visited:
            neighbors.append((row + 1, col))

    # LEFT
    if in_bounds(row, col - 1):
        if can_move_left(row, col) and (row, col - 1) not in solver_visited:
            neighbors.append((row, col - 1))

    # RIGHT
    if in_bounds(row, col + 1):
        if can_move_right(row, col) and (row, col + 1) not in solver_visited:
            neighbors.append((row, col + 1))

    return neighbors

# move to the next cell in the depth-first search algorithm, removing the wall between the current cell and the next cell. 
def generate_maze_step():
    global current_row
    global current_col
    global maze_complete

    if stack:
        current_row, current_col = stack[-1]

        neighbors = get_unvisited_neighbors(current_row, current_col)

        if neighbors:
            next_row, next_col = random.choice(neighbors)
            remove_wall(current_row, current_col, next_row, next_col)

            visited.add((next_row,next_col))
            stack.append((next_row, next_col))

        else:
            stack.pop()
    
    if not stack:
        maze_complete = True
        
# def move_solver():

#     global solver_row, solver_col, solver_finished

#     if solver_finished:
#         return

#     neighbors = get_solver_neighbors(solver_row, solver_col)

#     # MOVE FORWARD
#     if neighbors:

#         next_row, next_col = neighbors[0]

#         solver_stack.append((next_row, next_col))

#         solver_row = next_row
#         solver_col = next_col

#         solver_visited.add((solver_row, solver_col))

#     # DEAD END → BACKTRACK
#     else:

#         dead_ends.append((solver_row, solver_col))

#         solver_stack.pop()

#         if solver_stack:
#             solver_row, solver_col = solver_stack[-1]

#     # CHECK EXIT
#     if solver_col == C - 1 and east_wall[solver_row][C] == 0:
#         solver_finished = True
        


def draw_maze():
    # draw internal walls
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

# def draw_entrance():
#     text = font.render("START", True, (0, 150, 0))

#     x = START_X + 5
#     y = START_Y + entrance_row * CELL_SIZE + CELL_SIZE // 2 - 10

#     screen.blit(text, (x, y))


# def draw_exit():
#     text = font.render("END", True, (200, 0, 0))

#     x = START_X + (C - 1) * CELL_SIZE + 5
#     y = START_Y + exit_row * CELL_SIZE + CELL_SIZE // 2 - 10

#     screen.blit(text, (x, y))

# def draw_solver():

#     x = START_X + solver_col * CELL_SIZE
#     y = START_Y + solver_row * CELL_SIZE

#     pygame.draw.rect(
#         screen,
#         (0, 255, 0),
#         (x, y, CELL_SIZE, CELL_SIZE)
#     )
    
# def draw_dead_ends():

#     for row, col in dead_ends:

#         x = START_X + col * CELL_SIZE
#         y = START_Y + row * CELL_SIZE

#         pygame.draw.rect(
#             screen,
#             (100, 100, 255),
#             (x, y, CELL_SIZE, CELL_SIZE)
#         )
        
# def draw_solution_path():

#     for row, col in solver_stack:

#         x = START_X + col * CELL_SIZE
#         y = START_Y + row * CELL_SIZE

#         pygame.draw.rect(
#             screen,
#             (255, 255, 0),  # yellow
#             (x, y, CELL_SIZE, CELL_SIZE)
#         )

# set the frames per second for the game loop 
FPS = 2

#Main loop
running = True

while running:
    screen.fill(WHITE)

    generate_maze_step()

    if maze_complete and not entrance_created:

        entrance_row = random.randint(0, R - 1)
        exit_row = random.randint(0, R - 1)

        east_wall[entrance_row][0] = 0
        east_wall[exit_row][C] = 0

        entrance_created = True
    
    # if maze_complete and entrance_created and not solver_started:

    #     solver_row = entrance_row
    #     solver_col = 0

    #     solver_stack.append((solver_row, solver_col))
    #     solver_visited.add((solver_row, solver_col))

    #     solver_started = True
    
    # if maze_complete and solver_started:
    #     move_solver()


    draw_visited()
    
    # draw_dead_ends()
    
    # if solver_finished:
    #     draw_solution_path()
    
    draw_current_cell()
    
    # if solver_started:
    #     draw_solver()
    
    # draw_coordinates()
    
    # if entrance_created:
    #     draw_entrance()
    #     draw_exit()
    
    # draw_maze()

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
