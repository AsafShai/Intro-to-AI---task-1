from typing import List, Tuple
from puzzleTypes import Action, Node, PuzzleState, Path



def parse_input(path: str = 'input.txt') -> tuple[int, int, PuzzleState]:
    """Parse the input file and return algorithm choice, board size, and initial state."""
    with open(path) as f:
        lines = f.read().splitlines()
    k = int(lines[0])
    n = int(lines[1])
    tiles = list(map(int, lines[2].split('-')))
    return k, n, tuple(tiles)


def write_output(moves: List[str], path: str = 'output.txt') -> None:
    """Write the solution moves to output file."""
    with open(path, 'w') as f:
        f.write(''.join(moves))


def manhattan(state: PuzzleState, n: int) -> int:
    """Heuristic function: sum of Manhattan distances of each tile from its goal spot"""
    total = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        goal_r, goal_c = divmod(val - 1, n)
        r, c = divmod(idx, n)
        total += abs(r - goal_r) + abs(c - goal_c)
    return total


def successors(state: PuzzleState, n: int) -> List[Tuple[PuzzleState, Action]]:
    """
    Given a board, slide the blank in all possible directions based on tile moves (U, D, L, R preference).
    Returns a list of successor states and the action taken to get to them.
    """
    successors_list: List[Tuple[PuzzleState, Action]] = []
    blank_idx: int = state.index(0)
    blank_row, blank_col = divmod(blank_idx, n)

    preferred_tile_actions_and_moves: List[Tuple[Action, Tuple[int, int]]] = [
        ('U',(1, 0)),
        ('D',(-1, 0)),
        ('L',(0, 1)),
        ('R',(0, -1))
    ]

    for tile_action, (d_row, d_col) in preferred_tile_actions_and_moves:
        new_blank_row, new_blank_col = blank_row + d_row, blank_col + d_col
        if 0 <= new_blank_row < n and 0 <= new_blank_col < n:
            tile_to_move_idx = new_blank_row * n + new_blank_col
            new_state_list = list(state) 
            new_state_list[blank_idx], new_state_list[tile_to_move_idx] = \
                new_state_list[tile_to_move_idx], new_state_list[blank_idx]
            successors_list.append((tuple(new_state_list), tile_action))
    return successors_list



def reconstruct_path(node: Node) -> Path:
    """
    Reconstruct the path of moves from the initial state to the current node using chain of parents, 
    then reverse the moves list.
    """
    moves = []
    while node.parent:
        moves.append(node.action)
        node = node.parent
    return Path(list(reversed(moves)))


def is_solvable(state: PuzzleState, n: int) -> bool:
    """Check if this puzzle layout can ever be solved."""
    vals = [x for x in state if x]
    inv = sum(vals[i] > vals[j] for i in range(len(vals)) for j in range(i + 1, len(vals))) #Count inversions
    if n % 2 == 1:
        return inv % 2 == 0
    row = state.index(0) // n
    from_bottom = n - row
    return (inv % 2) == ((from_bottom + 1) % 2) 