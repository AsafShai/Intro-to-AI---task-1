from algorithms import iddfs, bfs, astar, idastar, dfs
from typing import Dict, Callable
from puzzleTypes import PuzzleState, Path

# Match user input to the correct search algorithm function
choices: Dict[int, Callable[[PuzzleState, int, PuzzleState], Path]] = {
        1: iddfs,
        2: bfs,
        3: astar,
        4: idastar,
        5: dfs,
}