import sys
from utils import parse_input, write_output, is_solvable
from constants import choices
from puzzleTypes import Path

if __name__ == '__main__':
    # Parse user input
    algorithm_choice, board_size, start_state = parse_input()
    
    # Define the goal state based on board size
    goal_state = tuple(range(1, board_size * board_size)) + (0,)
    
    # Solvability Check
    if not is_solvable(start_state, board_size):
        write_output([]) # If not solvable, write an empty solution
        print("This puzzle can't be solved.")
        sys.exit(0)

    # Solve the puzzle using the selected algorithm and write the solution path
    solution: Path = choices[algorithm_choice](start_state, board_size, goal_state)
    write_output(solution) 