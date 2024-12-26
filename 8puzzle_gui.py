import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from checkSolvability import is_solvable

class PuzzleGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("8 Puzzle Game")

        # Left frame for the main image
        self.left_frame = tk.Frame(master)
        self.left_frame.grid(row=0, column=0)

        # Right frame for the puzzle grid
        self.right_frame = tk.Frame(master)
        self.right_frame.grid(row=0, column=1)

        self.load_images()  # Load tile images

        self.buttons = []  # Store button widgets in a 3x3 grid
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.right_frame, command=lambda i=i, j=j: self.set_initial_tile(i, j),
                                   width=10, height=3)
                button.grid(row=i, column=j, sticky='nsew')
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        # Set equal weights for buttons
        for i in range(3):
            self.right_frame.grid_rowconfigure(i, weight=1)
            self.right_frame.grid_columnconfigure(i, weight=1)

        self.left_image_label = tk.Label(self.left_frame)
        self.left_image_label.pack()
        self.update_left_image("girl/girl.png")  # Adjust to your path

        # Initialize puzzle state and tile placement tracking
        self.puzzle_state = [None] * 9  # Empty state initially
        self.next_tile_index = 0  # Track which tile (0-8) to place next

        # Button to start solving the puzzle
        self.solve_button = tk.Button(master, text="Start", command=self.solve_puzzle)
        self.solve_button.grid(row=1, column=0, columnspan=2)

    def load_images(self):
        """Load images for the tiles."""
        self.images = []
        self.images.append(ImageTk.PhotoImage(Image.open("girl/blank.png").resize((100, 100))))  # 0: blank
        for i in range(1, 9):
            img = Image.open(f"girl/{i}girl.png").resize((100, 100))
            self.images.append(ImageTk.PhotoImage(img))

    def update_left_image(self, img_path):
        """Update the image displayed on the left."""
        img = Image.open(img_path).resize((100, 100))
        self.left_image = ImageTk.PhotoImage(img)
        self.left_image_label.config(image=self.left_image)
        self.left_image_label.image = self.left_image

    def set_initial_tile(self, i, j):
        """Set the initial tiles one-by-one on clicks."""
        index = i * 3 + j  # Calculate the 1D index from (i, j)

        if self.puzzle_state[index] is None and self.next_tile_index < 9:
            # Place the next tile (0 for blank, 1-8 for images)
            self.puzzle_state[index] = self.next_tile_index
            self.buttons[i][j].config(image=self.images[self.next_tile_index])
            self.next_tile_index += 1  # Increment for the next tile

    def solve_puzzle(self):
        """Solve the puzzle and animate the solution."""
        if None in self.puzzle_state:
            messagebox.showinfo("Info", "Please fill all tiles before starting.")
            return

        goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Goal state
        if not is_solvable(self.puzzle_state):
            messagebox.showinfo("Info", "No solution exists for this initial state.")
            return

        result = ids(self.puzzle_state, goal_state)
        if result:
            self.animate_solution(result)
        else:
            messagebox.showinfo("Info", "No solution found.")

    def animate_solution(self, solution):
        """Animate the solution with a delay between steps."""
        def step_animation(step=0):
            if step < len(solution):
                self.update_puzzle(solution[step])
                self.master.after(500, step_animation, step + 1)  # Delay of 500ms

        step_animation()

    def update_puzzle(self, state):
        """Update the puzzle buttons based on a given state."""
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                img_index = state[index]
                self.buttons[i][j].config(image=self.images[img_index])

# Depth-Limited Search and IDS Functions
def dls(startState, goalState, depth=20):
    """Depth-Limited Search."""
    nodes = [Node(startState, None, None, 0, 0)]  # Initialize with the root node
    explored = set()
    while nodes:
        node = nodes.pop(0)
        if node.state == goalState:
            return node.pathFromStart()
        if node.depth < depth:
            expanded = expandedNodes(node)
            for child in expanded:
                if tuple(child.state) not in explored:
                    explored.add(tuple(child.state))
                    nodes.insert(0, child)

def ids(startState, goalState, max_depth=50):
    """Iterative Deepening Search."""
    for depth in range(max_depth):
        result = dls(startState, goalState, depth)
        if result is not None:
            return result
    return None

class Node:
    """Structure for nodes in the search tree."""
    def __init__(self, state, parent, action, depth, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

    def pathFromStart(self):
        """Get the path from the initial state to the current state."""
        path = []
        node = self
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

def expandedNodes(node):
    """Generate all valid moves from the current node."""
    moves = [moveUp, moveDown, moveLeft, moveRight]
    children = []
    for move in moves:
        new_state = move(node.state)
        if new_state:
            children.append(Node(new_state, node, move.__name__, node.depth + 1, 0))
    return children

def moveUp(state):
    index = state.index(0)
    if index > 2:
        state[index], state[index - 3] = state[index - 3], state[index]
        return state[:]
    return None

def moveDown(state):
    index = state.index(0)
    if index < 6:
        state[index], state[index + 3] = state[index + 3], state[index]
        return state[:]
    return None

def moveLeft(state):
    index = state.index(0)
    if index % 3 != 0:
        state[index], state[index - 1] = state[index - 1], state[index]
        return state[:]
    return None

def moveRight(state):
    index = state.index(0)
    if index % 3 != 2:
        state[index], state[index + 1] = state[index + 1], state[index]
        return state[:]
    return None

if __name__ == "__main__":
    root = tk.Tk()
    PuzzleGUI(root)
    root.mainloop()
