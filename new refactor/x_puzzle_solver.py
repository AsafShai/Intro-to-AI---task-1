#---------------------------------------------------------
# Team Number 2

# Student Name 1: 
# Student ID 1: 

# Student Name 2: 
# Student ID 2: 

# Student Name 3: 
# Student ID 3: 

# Student Name 4: 
# Student ID 4:
 
# Student Name 5: 
# Student ID 5: 
#---------------------------------------------------------


import sys
import heapq

# This class holds a board and links to how we got here
class Node:
    def __init__(self, state, parent=None, action=None, g=0, h=0):
        self.state = state      # The tiles as a tuple
        self.parent = parent    # Where we came from
        self.action = action    # Move that got us here (U/D/L/R)
        self.g = g              # Number of moves so far
        self.h = h              # A guess of how many moves remain (using Manhattan)
        self.f = g + h          # Total estimate (for A*/IDA*)

    def __lt__(self, other):
        # pick the node with smaller f first
        return self.f < other.f

# Read input: what algorithm, board size, and starting borad
def parse_input(path='input.txt'):
    with open(path) as f:
        lines = f.read().splitlines()
    k = int(lines[0])                     # 1=IDDFS, 2=BFS, 3=A*, 4=IDA*, 5=DFS
    N = int(lines[1])                     # Board is N×N
    tiles = list(map(int, lines[2].split('-')))
    return k, N, tuple(tiles)

# Write moves into output.txt
def write_output(moves, path='output.txt'):
    with open(path, 'w') as f:
        f.write(''.join(moves))

# Heuristic: sum of Manhattan distances of each tile from its goal spot
def manhattan(state, N):
    total = 0
    for idx, val in enumerate(state):
        if val == 0:
            continue
        goal_r, goal_c = divmod(val - 1, N)
        r, c = divmod(idx, N)
        total += abs(r - goal_r) + abs(c - goal_c)
    return total

# Given a board, slide the blank in all possible directions
def successors(state, N):
    blank = state.index(0)
    r, c = divmod(blank, N)
    result = []
    for move, (dr, dc) in [('R', (0,1)), ('L', (0,-1)), ('D', (1,0)), ('U', (-1,0))]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < N and 0 <= nc < N:
            nxt = nr * N + nc
            new_state = list(state)
            new_state[blank], new_state[nxt] = new_state[nxt], new_state[blank]
            result.append((tuple(new_state), move))
    return result

# Follow the chain of parents back to the start, then flip the move list
def reconstruct_path(node):
    moves = []
    while node.parent:
        moves.append(node.action)
        node = node.parent
    return list(reversed(moves))

# dfs
def dfs(start, N, goal):
    stack = [Node(start)]
    seen = set()
    while stack:
        node = stack.pop()
        if node.state == goal:
            return reconstruct_path(node)
        seen.add(node.state)
        for s, m in reversed(successors(node.state, N)):
            if s not in seen:
                stack.append(Node(s, node, m))
    return []

# bfs
def bfs(start, N, goal):
    from collections import deque
    q = deque([Node(start)])
    seen = {start}
    while q:
        node = q.popleft()
        if node.state == goal:
            return reconstruct_path(node)
        for s, m in successors(node.state, N):
            if s not in seen:
                seen.add(s)
                q.append(Node(s, node, m))
    return []

# Iterative Deepening DFS
def iddfs(start, N, goal):
    def dls(node, depth, limit, seen):
        if node.state == goal:
            return reconstruct_path(node)
        if depth == limit:
            return None
        seen.add(node.state)
        for s, m in successors(node.state, N):
            if s not in seen:
                sol = dls(Node(s, node, m), depth+1, limit, seen)
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

# A* search with Manhattan heuristic
def astar(start, N, goal):
    open_list = []
    heapq.heappush(open_list, Node(start, g=0, h=manhattan(start, N)))
    best_g = {start: 0}
    closed = set()
    while open_list:
        node = heapq.heappop(open_list)
        if node.state == goal:
            return reconstruct_path(node)
        closed.add(node.state)
        for s, m in successors(node.state, N):
            g2 = node.g + 1
            if s in closed and g2 >= best_g.get(s, float('inf')):
                continue
            if g2 < best_g.get(s, float('inf')):
                best_g[s] = g2
                heapq.heappush(open_list, Node(s, node, m, g2, manhattan(s, N)))
    return []

# IDA*
def idastar(start, N, goal):
    limit = manhattan(start, N)
    path = [Node(start)]
    def dfs_limit(g):
        node = path[-1]
        f = g + manhattan(node.state, N)
        if f > limit:
            return f
        if node.state == goal:
            return 'FOUND'
        min_next = float('inf')
        for s, m in successors(node.state, N):
            if any(n.state == s for n in path):
                continue
            path.append(Node(s, node, m))
            t = dfs_limit(g+1)
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



# Check if this puzzle layout can ever be solved
def is_solvable(state, N):
    vals = [x for x in state if x]
    inv = sum(vals[i] > vals[j] for i in range(len(vals)) for j in range(i+1, len(vals))) #Count inversions
    
    #### Board width is odd 
    if N % 2 == 1: # if the witdh of the board is odd and the count of inversions is even then solvable
        return inv % 2 == 0
    
    
    #### Board width is even 
    # check row of blank 
    row = state.index(0) // N  
    from_bottom = N - row
    
    # the puzzle is solvable if the row index and number of inversions have different parity
    return (inv % 2) == ((from_bottom + 1) % 2)



# Script entry
if __name__ == '__main__':
    k, N, start = parse_input()
    goal = tuple(range(1, N*N)) + (0,)
    if not is_solvable(start, N):
        write_output([])
        print("This puzzle can't be solved.")
        sys.exit(0)

    choices = {1: iddfs, 2: bfs, 3: astar, 4: idastar, 5: dfs}
    solution = choices[k](start, N, goal)
    write_output(solution)
    #print('Solution moves:', ''.join(solution)) # For Debugging
