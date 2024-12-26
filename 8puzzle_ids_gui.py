import tkinter as tk
from PIL import Image, ImageTk
import time
from checkSolvability import is_solvable  # Import your solvability checker

class Node:
    """Structure of a puzzle node."""
    def __init__(self, state, parent, action, depth, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.cost = cost

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getMoves(self):
        return self.action

    def pathFromStart(self):
        """Retrieve the path from the initial state to the goal."""
        stateList, movesList = [], []
        currNode = self
        while currNode.getMoves() is not None:
            stateList.append(currNode.getState())
            movesList.append(currNode.getMoves())
            currNode = currNode.getParent()
        stateList.reverse()
        movesList.reverse()
        return stateList

def createNode(state, parent, action, depth, cost):
    return Node(state, parent, action, depth, cost)

def moveUp(state):
    newState = state[:]
    index = newState.index(0)
    if index not in [0, 1, 2]:
        newState[index], newState[index - 3] = newState[index - 3], newState[index]
        return newState
    return None

def moveDown(state):
    newState = state[:]
    index = newState.index(0)
    if index not in [6, 7, 8]:
        newState[index], newState[index + 3] = newState[index + 3], newState[index]
        return newState
    return None

def moveLeft(state):
    newState = state[:]
    index = newState.index(0)
    if index not in [0, 3, 6]:
        newState[index], newState[index - 1] = newState[index - 1], newState[index]
        return newState
    return None

def moveRight(state):
    newState = state[:]
    index = newState.index(0)
    if index not in [2, 5, 8]:
        newState[index], newState[index + 1] = newState[index + 1], newState[index]
        return newState
    return None

def expandedNodes(node):
    nodes = [
        createNode(moveUp(node.state), node, "up", node.depth + 1, 0),
        createNode(moveDown(node.state), node, "down", node.depth + 1, 0),
        createNode(moveLeft(node.state), node, "left", node.depth + 1, 0),
        createNode(moveRight(node.state), node, "right", node.depth + 1, 0)
    ]
    return [n for n in nodes if n.state is not None]

def dls(startState, goalState, depth=20):
    stack = [createNode(startState, None, None, 0, 0)]
    explored = set()

    while stack:
        node = stack.pop()
        explored.add(tuple(node.getState()))

        if node.getState() == goalState:
            return node.pathFromStart()

        if node.depth < depth:
            for neighbor in expandedNodes(node):
                if tuple(neighbor.getState()) not in explored:
                    stack.append(neighbor)
    return None

def ids(startState, goalState, max_depth=50):
    for depth in range(max_depth):
        result = dls(startState, goalState, depth)
        if result is not None:
            return result
    return None

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Game")

        self.puzzle_state = [None] * 9  # Initial empty state
        self.next_tile_index = 0  # Tracks the next tile to place
        self.goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]  # Goal state

        self.load_images()
        self.create_gui()

    def load_images(self):
        """Load images for the tiles."""
        self.images = [ImageTk.PhotoImage(Image.open(f"girl/{i}girl.png").resize((100, 100))) 
                      for i in range(1, 9)]  # Load images for tiles 1 to 8
        self.images.insert(0, ImageTk.PhotoImage(Image.open("girl/blank.png").resize((100, 100))))  # Load blank.png for the empty tile

    def create_gui(self):
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10)

        full_image = Image.open("girl/girl.png").resize((300, 300))
        self.full_image = ImageTk.PhotoImage(full_image)

        self.left_image_label = tk.Label(self.left_frame, image=self.full_image)
        self.left_image_label.pack()

        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                button = tk.Button(self.right_frame, command=lambda i=i, j=j: self.set_tile(i, j))
                button.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        for i in range(3):
            self.right_frame.grid_rowconfigure(i, weight=1)
            self.right_frame.grid_columnconfigure(i, weight=1)

        self.start_button = tk.Button(self.root, text="Start", command=self.solve_puzzle)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Label to show the step number
        self.step_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.step_label.grid(row=2, column=0, columnspan=2)

        # Label to show the total time
        self.time_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.time_label.grid(row=3, column=0, columnspan=2)

    def set_tile(self, i, j):
        index = i * 3 + j
        if self.puzzle_state[index] is None and self.next_tile_index < 9:
            self.puzzle_state[index] = self.next_tile_index
            self.buttons[i][j].config(image=self.images[self.next_tile_index])
            self.next_tile_index += 1

    def solve_puzzle(self):
        if None in self.puzzle_state:
            print("Please complete the puzzle first.")
            return

        if is_solvable(self.puzzle_state):
            start_time = time.time()  # Start the timer
            solution = ids(self.puzzle_state, self.goal_state)
            self.animate_solution(solution, start_time)  # Pass the start_time to animate_solution
        else:
            print("No solution exists for this state.")

    def animate_solution(self, solution, start_time):
        total_steps = len(solution)
        for step_number, state in enumerate(solution, start=1):
            self.update_grid(state)
            self.step_label.config(text=f"Step: {step_number}/{total_steps}")  # Update step label
            self.root.update()
            time.sleep(1)

        elapsed_time = time.time() - start_time  # Calculate elapsed time
        self.time_label.config(text=f"Total Time: {elapsed_time:.2f} seconds")  # Update time label
        self.step_label.config(text="Solved!")  # Indicate completion

    def update_grid(self, state):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                tile = state[index]
                self.buttons[i][j].config(image=self.images[tile])

if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()
