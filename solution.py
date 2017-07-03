rows = 'ABCDEFGHI'
cols = '123456789'

assignments = []

def assign_value(values, box, value):
    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(a, b):
    # Cross product of elements in A and elements in B.
    return [s + t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
forward_diagonal_unit = [a + b for a,b in list(zip(rows, cols))]
backward_diagonal_unit = [a + b for a,b in list(zip(rows[::-1], cols))]
unitlist = row_units + column_units + square_units + [forward_diagonal_unit] + [backward_diagonal_unit]
# Define all the units for a box
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Define all the peers for a box
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    for unit in unitlist:
        # For each unit, find all the boxes with two possible values
        doubles = [box for box in unit if len(values[box]) == 2]
        for double in doubles:
            for peer in peers[double]:
                # For each box with two possible values find if it has a peer with
                # the same two possible values
                if values[peer] == values[double]:
                    for other_peer in set.intersection(peers[double], peers[peer]):
                        # For every other peer, eliminate those two values
                        for i in values[double]:
                            values = assign_value(values, other_peer, values[other_peer].replace(i, ''))
    return values

def grid_values(grid):
    # Convert a string representation of a grid into a dictionary
    # Substitute all empty boxes ('.') with all possible values for that box ('123456789')
    grid = list(grid)
    for i, n in enumerate(grid):
        if n == '.':
            grid[i] = '123456789'
    assert len(grid) == 81
    return dict(zip(boxes, grid))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    pass

def eliminate(values):
    for key, value in values.items():
        if len(value) == 1:
            for peer in peers[key]:
                values = assign_value(values, peer, values[peer].replace(value, ''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            # Generate a list of all boxes in that unit that allow for the
            # number to be stored. If only on box allows for that number then
            # assign it the number
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        if solved_values_before == 81:
            break
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = (solved_values_before == solved_values_after)
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
