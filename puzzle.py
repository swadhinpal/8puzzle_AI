from copy import deepcopy

# Goal state for the 8-puzzle
GOAL_STATE = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 0]]  # 0 represents the empty space

# Helper to find the position of the empty tile (0)
def find_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Check if the current state is the goal state
def is_goal_state(state):
    return state == GOAL_STATE

# Generate the next possible states by moving the empty tile
def generate_next_states(state):
    next_states = []
    x, y = find_empty_tile(state)
    
    # Define possible moves (up, down, left, right)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            # Swap empty tile with the neighboring tile
            new_state = deepcopy(state)
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            next_states.append(new_state)
    
    return next_states

# Perform DFS up to the given depth limit
def dfs(state, depth, limit, path):
    print(f"Exploring state at depth {depth}: {state}")  # Debugging line
    if depth > limit:
        return None  # Exceeded depth limit
    
    if is_goal_state(state):
        return path  # Return the path if goal is reached
    
    for next_state in generate_next_states(state):
        result = dfs(next_state, depth + 1, limit, path + [next_state])
        if result:
            return result  # Solution found
    
    return None  # No solution within the current depth limit

# Iterative Deepening Search (IDS)
def iterative_deepening_search(initial_state):
    limit = 0  # Start with depth limit 0
    while True:
        print(f"Trying depth limit: {limit}")  # Debugging line
        result = dfs(initial_state, 0, limit, [initial_state])
        if result:
            return result  # Return the solution path
        limit += 1  # Increase depth limit

# Check if the puzzle is solvable by counting inversions
def is_solvable(state):
    flat_state = [tile for row in state for tile in row if tile != 0]
    inversions = sum(1 for i in range(len(flat_state)) 
                       for j in range(i + 1, len(flat_state)) 
                       if flat_state[i] > flat_state[j])
    return inversions % 2 == 0  # Solvable if inversions are even

# Input the initial state from the user
def input_initial_state():
    print("Enter the initial state row by row (use 0 for the empty space):")
    state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        state.append(row)
    return state

# Print the solution path step by step
def print_solution(path):
    print("Solution found in", len(path) - 1, "steps:")
    for step in path:
        for row in step:
            print(row)
        print()  # Print a blank line between steps

# Main function
def main():
    initial_state = input_initial_state()
    
    # Check if the initial state is solvable
    if not is_solvable(initial_state):
        print("This puzzle configuration is unsolvable.")
        return

    print("Solving the puzzle...")
    solution = iterative_deepening_search(initial_state)

    if solution:
        print_solution(solution)
    else:
        print("No solution found.")

# Run the main function
if __name__ == "__main__":
    main()
