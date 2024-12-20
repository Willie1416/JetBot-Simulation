import pygame
import sys

import Main  # The main that has all the functions with A* and heuristics
import Heatmap  # Heatmap that collects data and makes a heatmmap
import DataCollecter  # Collects the result from the tests

# Data File for this model
DATA_FILE = 'maze_data_passive.csv'

# Name for the test files in the heatmap
TEST_NUMBER = 1 # TODO please change based on your test number
MODEL = "Passive" # TODO change based on your model

# Set weights for the specific A* search
DANGER_COST = 60  # high penalty for being near thieves
SAFE_DISTANCE = 8  # avoid thiefs that are within 8 steps

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Thief color
YELLOW = (255, 215, 0)  # Coin color
BLUE = (0, 0, 255)  # Goal color

CELL_SIZE = 20  
screen_width = 800
screen_height = 560

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

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Game")
font = pygame.font.SysFont("New Roman Times", 24) # font
screen_font = pygame.font.SysFont("New Roman Times", 17) # Font
line_spacing = 80


# positions for AI, and goal
ai_start = (1, 1)
goal_position = (26, 28) 


def main():
    
    collected_indices = [] # Keep track of coins for display on the screen purpose

    maze_data_df = DataCollecter.load_or_initialize_data(DATA_FILE)
    current_position = ai_start
    coin_collected = set()
    coin_positions = [(9,16), (18, 8), (25,22), (5, 26), (7, 8), (16, 18), (22, 20), (5, 1), (18, 1), (26, 1)]  # 10 coin positions
    thief_positions = [(9, 15), (18, 6), (25, 20), (5, 25), (22, 14)]  # thief starting positions
    last_moves = thief_positions[:]  # Initialize last_moves to be the starting positions of the thieves
    step_counter = 0  # Initialize the step counter
    completed_maze = False
    coins_collected = 0 # Keep track of coins collected


    clock = pygame.time.Clock()
    table = Heatmap.read_table(MODEL, TEST_NUMBER, maze)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move thieves
        thief_positions, last_moves = Main.move_thieves(thief_positions, maze, last_moves)

        # Draw the maze, coins, and thieves
        screen.fill(WHITE)
        Main.draw_maze(thief_positions, coin_positions)
        Main.display_text()


        # Remaining coins in the maze
        remaining_coins = [coin for coin in coin_positions if coin not in coin_collected]

        if remaining_coins:
            # Find nearest coin from current position
            closest_coin = min(remaining_coins, key=lambda coin: Main.heuristic(current_position, coin))
            # Find the path to that coin using A*
            path_to_coin = Main.a_star_search(current_position, closest_coin, thief_positions, DANGER_COST, SAFE_DISTANCE)

            if path_to_coin:
                # Get the next step
                next_step = path_to_coin[1]
                current_position = next_step
                table = Heatmap.add_to_table(table, current_position) # adding to np array for record

                # If AI collides with thief decrement coin counter if AI has coins
                if current_position in thief_positions:
                    print(f"Collision with a thief at {current_position}! You lost a coin.")
                    if coins_collected > 0 and len(remaining_coins) < 10:
                        coins_collected -= 1
                step_counter += 1

                # If AI picks up a coin add it to coins collected and increment coin counter
                if current_position == closest_coin:
                    coin_collected.add(closest_coin)
                    print(f"Collected coin at {closest_coin}")
                    coins_collected +=1
                    collected_indices.append(closest_coin)


                    # Replace coin with a path 0 in the maze for display purpose
                    maze[closest_coin[0]][closest_coin[1]] = 0
                    # Update the coin_positions to path when the coin is collected
                    coin_positions.remove(closest_coin)
        else:
            # Find the path to the finish goal with A*
            path_to_goal = Main.a_star_search(current_position, goal_position, thief_positions, DANGER_COST, SAFE_DISTANCE)

            if path_to_goal:
                # Get the next step
                next_step = path_to_goal[1]
                current_position = next_step
                table = Heatmap.add_to_table(table, current_position) # adding to np array for record

                # If AI collides with thief decrement coin counter
                if current_position in thief_positions:
                    print(f"Collision with a thief at {current_position}! You lost a coin.")
                    if coins_collected > 0:
                        coins_collected -= 1
                step_counter += 1

                # If AI reaches the goal it completes the game and prints out how many steps
                if current_position == goal_position:
                    print(f"AI reached the finish in {step_counter} steps!")
                    text = screen_font.render('You collected all the coin', True, BLACK)
                    screen.blit(text, (650, 450))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    completed_maze = True
                    break
            else:
                print("No reachable path to goal!")
                break

        # Draw the AI at its current position
        ai_x = current_position[1] * CELL_SIZE
        ai_y = current_position[0] * CELL_SIZE
        pygame.draw.rect(screen, GREEN, (ai_x, ai_y, CELL_SIZE, CELL_SIZE))

        Main.draw_coin_count(coins_collected)
        Main.display_coinindex(collected_indices)
        
        # Update the screen
        pygame.display.flip()
        

        # Cap the frame rate
        clock.tick(5)

    # Store all the data collected for testing
    maze_data_df = DataCollecter.log_maze_data(step_counter, completed_maze, coins_collected, maze_data_df)
    DataCollecter.save_data(maze_data_df, DATA_FILE)
    print(maze_data_df)
    Heatmap.create_heatmap(table, TEST_NUMBER, MODEL)
    Heatmap.save_table(table, MODEL, TEST_NUMBER)

if __name__ == "__main__":
    for _ in range(10):
        main()
