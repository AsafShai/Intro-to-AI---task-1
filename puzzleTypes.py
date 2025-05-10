from typing import Optional, Tuple, NewType, List, Literal
from enum import Enum

PuzzleState = NewType('PuzzleState', Tuple[int, ...])
# Action = NewType('Action', str)  # Represents a tile move: U, D, L, R
Action = Literal['U', 'D', 'L', 'R']
Path = NewType('Path', List[Action])



class Node:
    """Represents a state in the puzzle search."""
    def __init__(
        self,
        state: PuzzleState,
        parent: Optional['Node'] = None,
        action: Optional[Action] = None,
        g: int = 0,
        h: int = 0
    ) -> None:
        self.state: PuzzleState = state
        self.parent: Optional['Node'] = parent
        self.action: Optional[Action] = action
        self.g: int = g
        self.h: int = h
        self.f: int = g + h

    def __lt__(self, other: 'Node') -> bool:
        return self.f < other.f 