import pygame
import heapq
import random


# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Thief color
YELLOW = (255, 215, 0)  # Coin color
BLUE = (0, 0, 255)  # Goal color

CELL_SIZE = 20  
WIDTH, HEIGHT = 30 * CELL_SIZE, 30 * CELL_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Coin Collector")
font = pygame.font.SysFont("New Roman Times", 24) 


maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1], 
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# positions for AI, thieves, coins, and goal
ai_start = (1, 1)
goal_position = (26, 28)  


# Function to draw the maze
def draw_maze(thief_positions, coin_positions):
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            color = BLACK if maze[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw coins
    for coin in coin_positions:
        coin_x = coin[1] * CELL_SIZE
        coin_y = coin[0] * CELL_SIZE
        pygame.draw.circle(screen, YELLOW, (coin_x + CELL_SIZE // 2, coin_y + CELL_SIZE // 2), CELL_SIZE // 4)

    # Draw thieves
    for thief in thief_positions:
        thief_x = thief[1] * CELL_SIZE
        thief_y = thief[0] * CELL_SIZE
        pygame.draw.rect(screen, RED, (thief_x, thief_y, CELL_SIZE, CELL_SIZE))

    # Draw goal
    goal_x = goal_position[1] * CELL_SIZE
    goal_y = goal_position[0] * CELL_SIZE
    pygame.draw.rect(screen, BLUE, (goal_x, goal_y, CELL_SIZE, CELL_SIZE))

# Heuristic for A* search, Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* search algorithm with dynamic thief avoidance
def a_star_search(start, goal, thief_positions, danger_cost, safe_distance):
    frontier = []     # Min-Heap that stores the shortest next step to take
    heapq.heappush(frontier, (0, start)) # Initialize min heap with start
    came_from = {start: None} # Map to keep track of where it has gone so far
    cost_so_far = {start: 0} # Map to keep track of the cost to get to that specific position
    


    while frontier:
        current = heapq.heappop(frontier)[1] # Get the next move

        if current == goal:
            break


        # Explore neighbors up, down, left, right
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + direction[0], current[1] + direction[1])

            # Check if the neighbor is walkable
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[0]][neighbor[1]] == 0:
                new_cost = cost_so_far[current] + 1  # Base cost to move to neighbor
                
                # Adjust cost based on proximity to thieves
                for thief in thief_positions:
                    distance_to_thief = heuristic(neighbor, thief) # Calculate the distance to each thief
                    
                    if distance_to_thief <= 2:
                        new_cost += danger_cost*100
                    elif distance_to_thief <= safe_distance:  # Near, but not immediate danger
                        new_cost += danger_cost * (safe_distance - distance_to_thief + 1)**2
                
                # If the neighbor have not been visited or the new cost is lower than previous cost at that position
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    # Update the cost to go to that position
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(goal, neighbor) # Calculate new priortity
                    heapq.heappush(frontier, (priority, neighbor)) # Push it to the min heap
                    came_from[neighbor] = current # Update where it came from to get there


    # If goal is not in came_from, no valid path was found
    if goal not in came_from:
        return []

    # Reconstruct path
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

def move_thieves(thief_positions, maze, last_moves):
    #Move each thief to a new position, avoiding backtracking unless at a dead end.
    new_thief_positions = []
    updated_last_moves = []

    # Goes over each thief last move
    for i, thief in enumerate(thief_positions):
        last_move = last_moves[i]  # Get the last move of the current thief

        # Generate possible moves up, down, left, right
        possible_moves = [
            (thief[0] - 1, thief[1]),  # Up
            (thief[0] + 1, thief[1]),  # Down
            (thief[0], thief[1] - 1),  # Left
            (thief[0], thief[1] + 1)   # Right
        ]

        # Filter valid moves
        valid_moves = [
            move for move in possible_moves
            if 0 <= move[0] < len(maze) and 0 <= move[1] < len(maze[0])  # Within bounds
            and maze[move[0]][move[1]] != 1  # Not a wall
            and move not in thief_positions  # Avoid overlapping with other thieves
        ]

        # Exclude the last move from valid options if there are other valid moves
        if last_move in valid_moves and len(valid_moves) > 1:
            valid_moves.remove(last_move)

        # Pick a random move out of available moves
        if valid_moves:
            # Random movement
            new_position = random.choice(valid_moves)
            new_thief_positions.append(new_position)
            updated_last_moves.append(thief)  # Update the last move to the current position
        else:
            # No valid moves, stay in place
            new_thief_positions.append(thief)
            updated_last_moves.append(last_move)  # Keep the last move as is

    return new_thief_positions, updated_last_moves

def draw_coin_count(count):
    coin_font = pygame.font.SysFont("New Roman Times", 20)
    text = coin_font.render(f"Coins Collected: {count} ", True, BLACK)
    screen.blit(text, (650, 45))  # Draw the text in the top-left corner

def display_text():
    text = font.render('Maze Game', True, BLACK)
    # Set position to top-left with a small padding
    x = 650  # 10 pixels from the left edge
    y = 10  # 10 pixels from the top edge

    screen.blit(text, (x, y))

# Shows the coin index  
def display_coinindex(collected_indices):
    line_spacing = 20  # Vertical spacing between lines
    index_font = pygame.font.SysFont("New Roman Times", 20)  # Font for text
    for i, coin in enumerate(collected_indices):
        text = index_font.render(f"Coin Index: {coin}", True, BLACK)
        screen.blit(text, (650, 65 + i * line_spacing))  # Display each index in a new line

