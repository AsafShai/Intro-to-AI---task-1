import sys
from utils import parse_input, write_output, is_solvable
from constants import choices
from puzzleTypes import Path

if __name__ == '__main__':
    algorithm_choice, board_size, start_state = parse_input()
    goal_state = tuple(range(1, board_size * board_size)) + (0,)
    if not is_solvable(start_state, board_size):
        write_output([])
        print("This puzzle can't be solved.")
        sys.exit(0)

    
    solution: Path = choices[algorithm_choice](start_state, board_size, goal_state)
    write_output(solution) 