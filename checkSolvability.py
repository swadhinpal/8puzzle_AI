def is_solvable(state):
    inv = 0  # Count inversions
    flat_state = [tile for tile in state if tile != 0]  # Exclude blank tile
    for i in range(len(flat_state)):
        for j in range(i + 1, len(flat_state)):
            if flat_state[i] > flat_state[j]:
                inv += 1
    return inv % 2 == 0  # Even inversions mean solvable
