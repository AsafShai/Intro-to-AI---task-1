from typing import List, Set
from puzzleTypes import Node, PuzzleState, Path
from utils import manhattan, successors, reconstruct_path
import heapq

# Depth-First Search for the puzzle
def dfs(start: PuzzleState, n: int, goal: PuzzleState) -> Path:
    """Depth-First Search: explores as far as possible along each path."""
    stack = [Node(start)]
    seen: Set[PuzzleState] = set()
    while stack:
        node = stack.pop()
        if node.state == goal:
            return reconstruct_path(node)
        seen.add(node.state)
        for s, m in reversed(successors(node.state, n)):
            if s not in seen:
                stack.append(Node(s, node, m))
    return []

# Breadth-First Search for the puzzle
def bfs(start: PuzzleState, n: int, goal: PuzzleState) -> Path:
    """Breadth-First Search: explores all neighbors level by level."""
    from collections import deque
    q = deque([Node(start)])
    seen: Set[PuzzleState] = {start}
    while q:
        node = q.popleft()
        if node.state == goal:
            return reconstruct_path(node)
        for s, m in successors(node.state, n):
            if s not in seen:
                seen.add(s)
                q.append(Node(s, node, m))
    return []

# Iterative Deepening Depth-First Search for the puzzle.
def ids(start: PuzzleState, n: int, goal: PuzzleState) -> Path:
    """Iterative Deepening DFS: DFS with increasing depth limits."""
    def dls(node: Node, depth: int, limit: int, seen: Set[PuzzleState]) -> Path | None:
        if node.state == goal:
            return reconstruct_path(node)
        if depth == limit:
            return None
        seen.add(node.state)
        for s, m in successors(node.state, n):
            if s not in seen:
                sol = dls(Node(s, node, m), depth + 1, limit, seen)
                if sol:
                    return sol
        seen.remove(node.state)
        return None

    depth = 0
    while True:
        sol = dls(Node(start), 0, depth, set())
        if sol is not None:
            return sol
        depth += 1

# A* Search with Manhattan heuristic for the puzzle
def astar(start: PuzzleState, n: int, goal: PuzzleState) -> Path:
    """A* Search: uses a priority queue with g (cost so far) + h (Manhattan heuristic)."""
    open_list = []
    heapq.heappush(open_list, Node(start, g=0, h=manhattan(start, n)))
    best_g = {start: 0}
    closed: Set[PuzzleState] = set()
    while open_list:
        node = heapq.heappop(open_list)
        if node.state == goal:
            return reconstruct_path(node)
        closed.add(node.state)
        for s, m in successors(node.state, n):
            g2 = node.g + 1
            if s in closed and g2 >= best_g.get(s, float('inf')):
                continue
            if g2 < best_g.get(s, float('inf')):
                best_g[s] = g2
                heapq.heappush(open_list, Node(s, node, m, g2, manhattan(s, n)))
    return []

# Iterative Deepening A* Search for the puzzle
def idastar(start: PuzzleState, n: int, goal: PuzzleState) -> Path:
    """Iterative Deepening A*: like IDS but guided by f = g + h."""
    limit = manhattan(start, n)
    path = [Node(start)]

    def dfs_limit(g: int) -> int | str:
        node = path[-1]
        f = g + manhattan(node.state, n)
        if f > limit:
            return f
        if node.state == goal:
            return 'FOUND'
        min_next = float('inf')
        for s, m in successors(node.state, n):
            if any(n_.state == s for n_ in path):
                continue
            path.append(Node(s, node, m))
            t = dfs_limit(g + 1)
            if t == 'FOUND':
                return 'FOUND'
            min_next = min(min_next, t)
            path.pop()
        return min_next

    while True:
        t = dfs_limit(0)
        if t == 'FOUND':
            return reconstruct_path(path[-1])
        limit = t 