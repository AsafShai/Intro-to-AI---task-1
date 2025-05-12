from typing import Optional, Tuple, NewType, List, Literal

PuzzleState = NewType('PuzzleState', Tuple[int, ...])
Action = Literal['U', 'D', 'L', 'R']
Path = NewType('Path', List[Action])



class Node:
    """This class Represents a board, the parent and the action taken to reach it."""
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
        """
        Compare two nodes based on their f-values, return True if self is lower.
        """
        return self.f < other.f 