import pygame
from a_star_solver import generate_extreme_maze, a_star_search, manhattan_distance

# --- PYGAME SETUP ---
pygame.init()

# --- CONFIGURATION FOR EXTREME HARD MAZE ---
GRID_ROWS = 50 
GRID_COLS = 50
WALL_DENSITY = 0.35 # Lower density ensures connectivity, but still challenging

CELL_SIZE = 15 # Size in pixels for each grid cell
WIDTH = GRID_COLS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Extreme A* Maze Solver Visualization")

# --- COLORS ---
BLACK = (10, 10, 10)    # Background/Grid color (Dark Gray/Black)
WALL_COLOR = (50, 50, 50) # NEW: A noticeable dark gray for walls
WHITE = (200, 200, 200) # Grid lines
GREEN = (0, 255, 0)     # Start node
RED = (255, 0, 0)       # Goal node
YELLOW = (255, 255, 0)  # Nodes in Open List
BLUE = (0, 0, 255)      # Nodes in Closed/Explored List
CYAN = (0, 255, 255)    # Final Path

# --- MAZE INITIALIZATION ---
START = (0, 0)
GOAL = (GRID_ROWS - 1, GRID_COLS - 1)
MAZE = generate_extreme_maze(GRID_ROWS, GRID_COLS, WALL_DENSITY)
# Ensure the Start/Goal are accessible right away
MAZE[START[0]][START[1]] = 0
MAZE[GOAL[0]][GOAL[1]] = 0

# --- A* INITIALIZATION ---
# Create the A* search generator
search_generator = a_star_search(MAZE, START, GOAL, heuristic_func=manhattan_distance)
# manhattan_distance is generally the right choice for non-diagonal movement.

# --- DRAWING FUNCTIONS ---

def draw_grid():
    """Draws the grid lines."""
    for i in range(GRID_ROWS):
        pygame.draw.line(SCREEN, WHITE, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for j in range(GRID_COLS):
        pygame.draw.line(SCREEN, WHITE, (j * CELL_SIZE, 0), (j * CELL_SIZE, HEIGHT))

def draw_cell(r, c, color):
    """Draws a single cell as a filled rectangle."""
    rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(SCREEN, color, rect)

def draw_maze_and_path(explored_nodes, open_set_nodes, path, current_node):
    """Draws the current state of the maze and search."""
    
    # 1. Clear screen and draw walls
    SCREEN.fill(BLACK)
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            # *** CRITICAL FIX HERE ***
            if MAZE[r][c] == 1:
                draw_cell(r, c, WALL_COLOR) # Draw walls using the new, visible color
            # If it's an open path (0), we don't draw anything here, 
            # letting the BLACK background show.

    # 2. Draw search state
    for node in explored_nodes:
        draw_cell(node[0], node[1], BLUE) # Explored nodes
    
    for node in open_set_nodes:
        draw_cell(node[0], node[1], YELLOW) # Nodes in the open list

    # 3. Draw final path if found
    if path:
        for node in path:
            draw_cell(node[0], node[1], CYAN) # Final shortest path

    # 4. Draw Start and Goal (always on top)
    draw_cell(START[0], START[1], GREEN)
    draw_cell(GOAL[0], GOAL[1], RED)

    # 5. Draw the grid lines last for definition
    draw_grid()

    pygame.display.flip()

# --- MAIN GAME LOOP ---
def main_loop():
    running = True
    path_found = False
    
    # Initial state variables
    explored_nodes = set()
    open_set_nodes = set()
    path = None
    current_node = START

    # Set frame rate for animation speed (e.g., 60 updates per second)
    clock = pygame.time.Clock() 
    
    # The A* search is driven by the game loop
    while running:
        # Event handling (to close the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Optional: Allow speeding up the search with a key press
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                 # Fast-forward/Skip animation (set path_found=True after generator is consumed)
                 pass

        # If the path hasn't been found, take the next step from the generator
        if not path_found:
            try:
                # Get the next state from the A* solver
                explored_nodes, open_set_nodes, path, current_node = next(search_generator)
                
                if path is not None:
                    path_found = True
                    print(f"\nPath Found! Length: {len(path) - 1} steps.")
                    
            except StopIteration:
                path_found = True # Path either found or confirmed unreachable
                print("\nSearch complete.")
                if path is None:
                    print("Goal is unreachable.")

        # Draw the current state of the visualization
        draw_maze_and_path(explored_nodes, open_set_nodes, path, current_node)
        
        # Control the animation speed (e.g., 60 frames per second)
        # Reduce this number (e.g., to 10) to make the animation slower
        clock.tick(60) 

    pygame.quit()

if __name__ == '__main__':
    main_loop()