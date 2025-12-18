import heapq
import math
import random

def manhattan_distance(p1, p2):
    """Calculates the Manhattan distance."""
    r1, c1 = p1
    r2, c2 = p2
    return abs(r1 - r2) + abs(c1 - c2)

def generate_extreme_maze(rows, cols, wall_density=0.4):
    """Generates a large, randomized maze."""
    maze = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if random.random() < wall_density:
                maze[r][c] = 1
    
    # Ensure start and goal are always open
    maze[0][0] = 0
    maze[rows - 1][cols - 1] = 0
    return maze

def a_star_search(maze, start, goal, heuristic_func=manhattan_distance):
    """
    Finds the shortest path using A* and yields updates for visualization.
    This function acts as a generator to allow step-by-step animation.
    """
    ROWS = len(maze)
    COLS = len(maze[0])
    
    open_list = [(0, 0, start)]  # (f_score, g_score, node)
    g_scores = {start: 0}
    parents = {start: None}
    
    # Track nodes for visualization categories
    explored_nodes = set()
    open_set_nodes = {start}
    
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

    while open_list:
        # Get the node with the lowest f_score
        current_f, current_g, current_node = heapq.heappop(open_list)
        
        # Update visualization sets
        open_set_nodes.remove(current_node)
        explored_nodes.add(current_node)
        
        # YIELD 1: Send the current state for drawing
        yield (explored_nodes, open_set_nodes, None, current_node)
        
        # Goal check
        if current_node == goal:
            path = reconstruct_path(parents, goal)
            # YIELD 2: Send the final path and stop
            yield (explored_nodes, open_set_nodes, path, current_node) 
            return # Exit the search
        
        current_r, current_c = current_node
        
        # Explore neighbors
        for dr, dc in neighbors:
            neighbor_r, neighbor_c = current_r + dr, current_c + dc
            neighbor_node = (neighbor_r, neighbor_c)
            
            # Check bounds and walls
            if not (0 <= neighbor_r < ROWS and 0 <= neighbor_c < COLS) or \
               maze[neighbor_r][neighbor_c] == 1:
                continue

            tentative_g_score = current_g + 1
            
            # If better path found
            if neighbor_node not in g_scores or tentative_g_score < g_scores[neighbor_node]:
                
                g_scores[neighbor_node] = tentative_g_score
                parents[neighbor_node] = current_node
                
                h_score = heuristic_func(neighbor_node, goal)
                f_score = tentative_g_score + h_score
                
                if neighbor_node not in open_set_nodes:
                    heapq.heappush(open_list, (f_score, tentative_g_score, neighbor_node))
                    open_set_nodes.add(neighbor_node)

    # Path not found
    yield (explored_nodes, open_set_nodes, None, None)

def reconstruct_path(parents, current_node):
    """Traces back the parents dictionary to build the path."""
    path = []
    while current_node is not None:
        path.append(current_node)
        current_node = parents.get(current_node)
    return path[::-1]