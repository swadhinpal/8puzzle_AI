import tkinter as tk
from tkinter import messagebox
from time import sleep
from copy import deepcopy
from collections import deque

# Images for the puzzle tiles (Ensure these files are in the same directory)
IMAGES = {
    1: "1dog.png", 2: "2dog.png", 3: "3dog.png",
    4: "4dog.png", 5: "5dog.png", 6: "6dog.png",
    7: "7dog.png", 8: "8dog.png", 0: "blank.png"  # 0 is the blank tile
}

# Goal state for the 8-puzzle
GOAL_STATE = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

class PuzzleGUI:
    def __init__(self, root, initial_state):
        self.root = root
        self.state = initial_state
        self.tiles = [[None] * 3 for _ in range(3)]  # Grid to store image labels

        self.create_grid()  # Initialize the grid with the current state

        # Add a Start button to begin solving the puzzle
        self.start_button = tk.Button(self.root, text="Start", command=self.start_solution)
        self.start_button.grid(row=3, column=0, columnspan=3)

    # Display the images corresponding to the current state
    def create_grid(self):
        for i in range(3):
            for j in range(3):
                tile_value = self.state[i][j]
                image = tk.PhotoImage(file=IMAGES[tile_value])
                self.tiles[i][j] = tk.Label(self.root, image=image, borderwidth=2, relief="solid")
                self.tiles[i][j].image = image  # Keep a reference to prevent garbage collection
                self.tiles[i][j].grid(row=i, column=j)

    # Update the GUI with a new state
    def update_grid(self, new_state):
        self.state = new_state
        self.create_grid()  # Refresh the grid with the new state
        self.root.update()

    # Display the solution step-by-step with a delay
    def show_solution(self, solution):
        for state in solution:
            self.update_grid(state)
            sleep(0.5)  # 0.5-second delay between each step

    # Triggered when the Start button is clicked
    def start_solution(self):
        solution = bfs(self.state)
        if solution:
            self.show_solution(solution)
        else:
            messagebox.showinfo("No Solution", "No solution found for the given puzzle.")

# Find the position of the blank tile (0)
def find_empty_tile(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

# Generate all possible next states by moving the blank tile
def generate_next_states(state):
    next_states = []
    x, y = find_empty_tile(state)

    # Possible moves: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            next_states.append(new_state)

    return next_states

# Breadth-First Search (BFS) to solve the puzzle
def bfs(initial_state):
    queue = deque([(initial_state, [])])  # Store (state, path to reach it)
    visited = set()

    while queue:
        current_state, path = queue.popleft()
        visited.add(tuple(map(tuple, current_state)))  # Mark state as visited

        if current_state == GOAL_STATE:
            return path + [current_state]  # Return the solution path

        for next_state in generate_next_states(current_state):
            if tuple(map(tuple, next_state)) not in visited:
                queue.append((next_state, path + [current_state]))

    return None  # No solution found

# Check if the puzzle is solvable by counting inversions
def is_solvable(state):
    flat_state = [tile for row in state for tile in row if tile != 0]
    inversions = sum(1 for i in range(len(flat_state))
                     for j in range(i + 1, len(flat_state))
                     if flat_state[i] > flat_state[j])
    return inversions % 2 == 0  # Solvable if inversions are even

# Input the initial state from the user via console
def input_initial_state():
    print("Enter the initial state row by row (use 0 for the blank space):")
    state = []
    for _ in range(3):
        row = list(map(int, input().split()))
        state.append(row)
    return state

# Main function to run the puzzle game
def main():
    initial_state = input_initial_state()

    # Check if the initial state is solvable
    if not is_solvable(initial_state):
        messagebox.showinfo("Unsolvable", "This puzzle configuration is unsolvable.")
        return

    # Create the GUI with the initial state
    root = tk.Tk()
    root.title("8-Puzzle Game")
    puzzle_gui = PuzzleGUI(root, initial_state)
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
