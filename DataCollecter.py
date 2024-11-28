import os
import pandas as pd


def load_or_initialize_data(data_file):
    """
    Loads the maze data from a CSV file or initializes a new DataFrame if the file doesn't exist.
    """
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    else:
        # Initialize a new DataFrame if the file doesn't exist
        return pd.DataFrame(columns=["Steps", "Completed_Maze", "Number of coins"])

def save_data(dataframe, data_file):
    """
    Saves the DataFrame to a CSV file.
    """
    dataframe.to_csv(data_file, index=False)


def log_maze_data(steps, completed, coins, df):
    """
    Logs data about the maze into the DataFrame.
    """
    # Convert the completed boolean to a string
    completed_str = "Yes" if completed else "No"
    # Create a new row of data
    new_row = {
        "Steps": steps,
        "Completed_Maze": completed_str,
        "Number of coins": coins
    }
    # Append the new row to the DataFrame
    return pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

