from time import time

class Node:
    def __init__(self, state, parent, action, depth, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

    def path_from_start(self):
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

def create_node(state, parent, action, depth, cost):
    return Node(state, parent, action, depth, cost)

def move_blank(state, dx, dy):
    new_state = state[:]
    index = new_state.index(0)
    x, y = divmod(index, 3)
    nx, ny = x + dx, y + dy
    if 0 <= nx < 3 and 0 <= ny < 3:
        swap_idx = nx * 3 + ny
        new_state[index], new_state[swap_idx] = new_state[swap_idx], new_state[index]
        return new_state
    return None

def expand(node):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    children = [
        create_node(move_blank(node.state, dx, dy), node, (dx, dy), node.depth + 1, 0)
        for dx, dy in moves
    ]
    return [child for child in children if child.state]

def dls(start, goal, limit):
    stack = [create_node(start, None, None, 0, 0)]
    while stack:
        node = stack.pop()
        if node.state == goal:
            return node.path_from_start()
        if node.depth < limit:
            stack.extend(expand(node))
    return None

def ids(start, goal, max_depth=50):
    for depth in range(max_depth):
        result = dls(start, goal, depth)
        if result:
            return result
    return None
