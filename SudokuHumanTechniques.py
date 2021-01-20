import numpy as np


# Imports 1000 Sudoku puzzles and solutions from a csv

sudoku_1000 = '1000Sudokus - Sheet1.csv'
puzzles_test = np.zeros((1000, 81), np.int32)
solutions_test = np.zeros((1000, 81), np.int32)
for i, line in enumerate(open(sudoku_1000, 'r').read().splitlines()):
    puzzle, solution = line.split(",")
    for j, q_s in enumerate(zip(puzzle, solution)):
        q, s = q_s
        puzzles_test[i, j] = q
        solutions_test[i, j] = s
puzzles_test = puzzles_test.reshape((-1, 9, 9))
solutions_test = solutions_test.reshape((-1, 9, 9))
X_test = puzzles_test
Y_test = solutions_test


# Initializes Sudoku grids

sudoku = np.empty([9, 9], dtype=object)
sudoku_input = np.empty([9, 9], dtype=int)


# Defines the unit class

class Unit:
    def __init__(self, r, c):
        self.row = r
        self.column = c
        self.name = f"{r}{c}"
        self.value = sudoku_input[r, c]
        sudoku[r, c] = self
        self.probability_dict = {1: True,
                                 2: True,
                                 3: True,
                                 4: True,
                                 5: True,
                                 6: True,
                                 7: True,
                                 8: True,
                                 9: True}

    def __repr__(self):
        return f"{self.value}"

    def set_value(self, n):
        self.value = n

    def true_count(self):
        return (list(self.probability_dict.values())).count(True)


# Function that defines regions

def regions(a_sudoku):
    regions_2d = [a_sudoku[:3, 0:3], a_sudoku[:3, 3:6], a_sudoku[:3, 6:9],
                  a_sudoku[3:6, 0:3], a_sudoku[3:6, 3:6], a_sudoku[3:6, 6:9],
                  a_sudoku[6:9, 0:3], a_sudoku[6:9, 3:6], a_sudoku[6:9, 6:9]]
    return [region.flatten() for region in regions_2d]


# Function that checks if the sudoku is solved

def finished(a_sudoku):
    if 0 in [unit.value for row in a_sudoku for unit in row]:
        return False
    else:
        return True


# Function that applies each technique once

def solve_one_step(a_sudoku):

    # Sets values for: at least one of each number has to be in each row

    merged_dict = {n: [] for n in range(1, 10)}
    for row in a_sudoku:
        for unit in row:
            for key, value in unit.probability_dict.items():
                merged_dict[key].append(value)
        for key, value in merged_dict.items():
            if value.count(True) == 1:
                row[value.index(True)].set_value(key)
        merged_dict = {n: [] for n in range(1, 10)}

    # Sets values for: at least one of each number has to be in each column

    for column in a_sudoku:
        for unit in column:
            for key, value in unit.probability_dict.items():
                merged_dict[key].append(value)
        for key, value in merged_dict.items():
            if value.count(True) == 1:
                column[value.index(True)].set_value(key)
        merged_dict = {n: [] for n in range(1, 10)}

    # Sets values for: at least one of each number has to be in each region

    for region in regions(a_sudoku):
        for unit in region:
            for key, value in unit.probability_dict.items():
                merged_dict[key].append(value)
        for key, value in merged_dict.items():
            if value.count(True) == 1:
                region[value.index(True)].set_value(key)
        merged_dict = {n: [] for n in range(1, 10)}

    # Updates values according to new unit probabilities

    for row in a_sudoku:
        for unit in row:
            if unit.true_count() == 1:
                unit.set_value(list(unit.probability_dict.values()).index(True) + 1)

    # Scans rows for values and re-adjust probabilities

    for row in a_sudoku:
        for unit in row:
            for n in range(1, 10):
                if unit.value == n:
                    for m in range(1, 10):
                        unit.probability_dict[m] = False
                    unit.probability_dict[n] = True
                    for i in range(9):
                        row[i].probability_dict[n] = False
                        unit.probability_dict[n] = True

    # Scans columns for values and re-adjusts probabilities

    for column in a_sudoku.T:
        for unit in column:
            for n in range(1, 10):
                if unit.value == n:
                    for m in range(1, 10):
                        unit.probability_dict[m] = False
                    unit.probability_dict[n] = True
                    for i in range(9):
                        column[i].probability_dict[n] = False
                        unit.probability_dict[n] = True

    # Scans regions for values and re-adjusts probabilities

    for region in regions(a_sudoku):
        for unit in region:
            for n in range(1, 10):
                if unit.value == n:
                    for m in range(1, 10):
                        unit.probability_dict[m] = False
                    unit.probability_dict[n] = True
                    for i in range(9):
                        region[i].probability_dict[n] = False
                        unit.probability_dict[n] = True

    # Omission 1:

    for region in regions(a_sudoku):
        for unit in region:
            if unit.value == 0:
                for key, value in unit.probability_dict.items():
                    merged_dict[key].append(value)
        for key2, value2 in merged_dict.items():
            # For doubles
            if value2.count(True) == 2:
                for unit1 in region:
                    for unit2 in region:
                        if unit1.value == 0 and unit2.value == 0:

                            # For rows
                            if (unit1 != unit2 and unit1.row == unit2.row and unit1.probability_dict[key2] == True
                                    and unit2.probability_dict[key2] == True):
                                for unit3 in a_sudoku[unit1.row]:
                                    if unit3 not in region:
                                        unit3.probability_dict[key2] = False

                            # For columns
                            if (unit1 != unit2 and unit1.column == unit2.column and unit1.probability_dict[key2] == True
                                    and unit2.probability_dict[key2] == True):
                                for unit3 in a_sudoku.T[unit1.column]:
                                    if unit3 not in region:
                                        unit3.probability_dict[key2] = False
            # For triples
            if value2.count(True) == 3:
                for unit1 in region:
                    for unit2 in region:
                        for unit3 in region:
                            if unit1.value == 0 and unit2.value == 0 and unit3.value == 0:

                                # For rows
                                if (unit1 != unit2 and unit1.row == unit2.row and unit1.probability_dict[key2]
                                        and unit2.probability_dict[key2] and unit2 != unit3 and
                                        unit3.probability_dict[key2] and unit2.row == unit3.row and unit1 != unit3):
                                    for unit4 in a_sudoku[unit1.row]:
                                        if unit4 not in region:
                                            unit4.probability_dict[key2] = False

                                # For columns
                                if (unit1 != unit2 and unit1.column == unit2.column and unit1.probability_dict[key2]
                                        and unit2.probability_dict[key2] and unit2 != unit3 and
                                        unit3.probability_dict[key2] and unit2.column == unit3.column and unit1 != unit3):
                                    for unit4 in a_sudoku.T[unit1.column]:
                                        if unit4 not in region:
                                            unit4.probability_dict[key2] = False
        merged_dict = {n: [] for n in range(1, 10)}

    # Omission 2:

    # For rows
    for row in a_sudoku:
        for unit in row:
            if unit.value == 0:
                for key, value in unit.probability_dict.items():
                    merged_dict[key].append(value)
        for key2, value2 in merged_dict.items():

            # For doubles
            if value2.count(True) == 2:
                for unit1 in row:
                    for unit2 in row:
                        if unit1.value == 0 and unit2.value == 0:
                            for region in regions(a_sudoku):
                                if (unit1 != unit2 and unit1 in region and unit2 in region
                                        and unit1.probability_dict[key2] == True
                                        and unit2.probability_dict[key2] == True):
                                    for unit3 in region:
                                        if unit3 not in row:
                                            unit3.probability_dict[key2] = False

            # For triples
            if value2.count(True) == 3:
                for unit1 in row:
                    for unit2 in row:
                        for unit3 in row:
                            if unit1.value == 0 and unit2.value == 0 and unit3.value == 0:
                                for region in regions(a_sudoku):
                                    if (unit1 != unit2 and unit1 in region and unit2 in region
                                            and unit1.probability_dict[key2]
                                            and unit2.probability_dict[key2] and unit2 != unit3 and
                                            unit3.probability_dict[key2] and unit3 in region
                                            and unit1 != unit3):
                                        for unit4 in region:
                                            if unit4 not in row:
                                                unit4.probability_dict[key2] = False
        merged_dict = {n: [] for n in range(1, 10)}

    # For column
    for column in a_sudoku.T:
        for unit in column:
            if unit.value == 0:
                for key, value in unit.probability_dict.items():
                    merged_dict[key].append(value)
        for key2, value2 in merged_dict.items():

            # For doubles
            if value2.count(True) == 2:
                for unit1 in column:
                    for unit2 in column:
                        if unit1.value == 0 and unit2.value == 0:
                            for region in regions(a_sudoku):
                                if (unit1 != unit2 and unit1 in region and unit2 in region
                                        and unit1.probability_dict[key2] == True
                                        and unit2.probability_dict[key2] == True):
                                    for unit3 in region:
                                        if unit3 not in column:
                                            unit3.probability_dict[key2] = False

            # For triples
            if value2.count(True) == 3:
                for unit1 in column:
                    for unit2 in column:
                        for unit3 in column:
                            if unit1.value == 0 and unit2.value == 0 and unit3.value == 0:
                                for region in regions(a_sudoku):
                                    if (unit1 != unit2 and unit1 in region and unit2 in region
                                            and unit1.probability_dict[key2]
                                            and unit2.probability_dict[key2] and unit2 != unit3 and
                                            unit3.probability_dict[key2] and unit3 in region
                                            and unit1 != unit3):
                                        for unit4 in region:
                                            if unit4 not in column:
                                                unit4.probability_dict[key2] = False
        merged_dict = {n: [] for n in range(1, 10)}

    # Naked duos:

    # For rows
    for row in a_sudoku:
        for unit1 in row:
            for unit2 in row:
                if unit1.value == 0 and unit2.value == 0:
                    if (unit1 != unit2 and unit1.probability_dict == unit2.probability_dict
                            and list(unit1.probability_dict.values()).count(True) == 2):
                        for unit3 in row:
                            if unit3 != unit1 and unit3 != unit2:
                                for key, value in unit1.probability_dict.items():
                                    if value == True:
                                        unit3.probability_dict[key] = False

    # For columns
    for column in a_sudoku.T:
        for unit1 in column:
            for unit2 in column:
                if unit1.value == 0 and unit2.value == 0:
                    if (unit1 != unit2 and unit1.probability_dict == unit2.probability_dict
                            and list(unit1.probability_dict.values()).count(True) == 2):
                        for unit3 in column:
                            if unit3 != unit1 and unit3 != unit2:
                                for key, value in unit1.probability_dict.items():
                                    if value == True:
                                        unit3.probability_dict[key] = False

    # For regions
    for region in regions(a_sudoku):
        for unit1 in region:
            for unit2 in region:
                if unit1.value == 0 and unit2.value == 0:
                    if (unit1 != unit2 and unit1.probability_dict == unit2.probability_dict
                            and list(unit1.probability_dict.values()).count(True) == 2):
                        for unit3 in region:
                            if unit3 != unit1 and unit3 != unit2:
                                for key, value in unit1.probability_dict.items():
                                    if value == True:
                                        unit3.probability_dict[key] = False

    # Hidden doubles:

    # For rows
    for row in a_sudoku:
        for unit1 in row:
            for unit2 in row:
                if unit1 != unit2 and unit1.value == 0 and unit2.value == 0:
                    for n in range(1, 10):
                        merged_dict[n].append(unit1.probability_dict[n])
                        merged_dict[n].append(unit2.probability_dict[n])
                    if list(merged_dict.values()).count([True, True]) >= 2:
                        shared = []
                        for m in range(1, 10):
                            only = True
                            if merged_dict[m] == [True, True]:
                                for unit3 in row:
                                    if unit3 != unit1 and unit3 != unit2 and unit3.value == 0 and \
                                            unit3.probability_dict[m] != False:
                                        only = False
                            if only == True:
                                shared.append(m)
                        if len(shared) == 2:
                            for i in range(1, 10):
                                if i not in shared:
                                    unit1.probability_dict[i] = False
                                    unit2.probability_dict[i] = False
                merged_dict = {n: [] for n in range(1, 10)}

    # For columns
    for column in a_sudoku.T:
        for unit1 in column:
            for unit2 in column:
                if unit1 != unit2 and unit1.value == 0 and unit2.value == 0:
                    for n in range(1, 10):
                        merged_dict[n].append(unit1.probability_dict[n])
                        merged_dict[n].append(unit2.probability_dict[n])
                    if list(merged_dict.values()).count([True, True]) >= 2:
                        shared = []
                        for m in range(1, 10):
                            only = True
                            if merged_dict[m] == [True, True]:
                                for unit3 in column:
                                    if unit3 != unit1 and unit3 != unit2 and unit3.value == 0 and \
                                            unit3.probability_dict[m] != False:
                                        only = False
                            if only == True:
                                shared.append(m)
                        if len(shared) == 2:
                            for i in range(1, 10):
                                if i not in shared:
                                    unit1.probability_dict[i] = False
                                    unit2.probability_dict[i] = False
                        merged_dict = {n: [] for n in range(1, 10)}

    # For regions
    for region in regions(a_sudoku):
        for unit1 in region:
            for unit2 in region:
                if unit1 != unit2 and unit1.value == 0 and unit2.value == 0:
                    for n in range(1, 10):
                        merged_dict[n].append(unit1.probability_dict[n])
                        merged_dict[n].append(unit2.probability_dict[n])
                    if list(merged_dict.values()).count([True, True]) >= 2:
                        shared = []
                        for m in range(1, 10):
                            only = True
                            if merged_dict[m] == [True, True]:
                                for unit3 in region:
                                    if unit3 != unit1 and unit3 != unit2 and unit3.value == 0 and \
                                            unit3.probability_dict[m] != False:
                                        only = False
                            if only == True:
                                shared.append(m)
                        if len(shared) == 2:
                            for i in range(1, 10):
                                if i not in shared:
                                    unit1.probability_dict[i] = False
                                    unit2.probability_dict[i] = False
                        merged_dict = {n: [] for n in range(1, 10)}

    # X Wing

    # For rows:
    merged_dict_2 = {n: [] for n in range(1, 10)}
    indices = {n: [] for n in range(1, 10)}
    indices_2 = {n: [] for n in range(1, 10)}
    doubles_in_row = []
    for row in a_sudoku:
        for unit in row:
            for key, value in unit.probability_dict.items():
                merged_dict[key].append(value)
        for key, value in merged_dict.items():
            if value.count(True) == 2:
                doubles_in_row.append(key)
                for i in range(9):
                    if value[i] == True:
                        indices[key].append(i)
        for row2 in a_sudoku:
            if not np.array_equal(row, row2):
                for unit2 in row2:
                    for key2, value2 in unit2.probability_dict.items():
                        merged_dict_2[key2].append(value2)
                for key, value in merged_dict_2.items():
                    if value.count(True) == 2 and key in doubles_in_row:
                        for i in range(9):
                            if value[i] == True:
                                indices_2[key].append(i)
                for i in range(1, 10):
                    if indices[i] != [] and indices[i] == indices_2[i]:
                        for row3 in a_sudoku:
                            if not np.array_equal(row, row3) and not np.array_equal(row2, row3):
                                row3[indices[i][0]].probability_dict[i] = False
                                row3[indices[i][1]].probability_dict[i] = False
                indices_2 = {n: [] for n in range(1, 10)}
                merged_dict_2 = {n: [] for n in range(1, 10)}
        indices = {n: [] for n in range(1, 10)}
        merged_dict = {n: [] for n in range(1, 10)}
        doubles_in_row = []

    # For column:
    merged_dict_2 = {n: [] for n in range(1, 10)}
    indices = {n: [] for n in range(1, 10)}
    indices_2 = {n: [] for n in range(1, 10)}
    doubles_in_column = []
    for column in a_sudoku.T:
        for unit in column:
            for key, value in unit.probability_dict.items():
                merged_dict[key].append(value)
        for key, value in merged_dict.items():
            if value.count(True) == 2:
                doubles_in_column.append(key)
                for i in range(9):
                    if value[i] == True:
                        indices[key].append(i)
        for column2 in a_sudoku.T:
            if not np.array_equal(column, column2):
                for unit2 in column2:
                    for key2, value2 in unit2.probability_dict.items():
                        merged_dict_2[key2].append(value2)
                for key, value in merged_dict_2.items():
                    if value.count(True) == 2 and key in doubles_in_column:
                        for i in range(9):
                            if value[i] == True:
                                indices_2[key].append(i)
                for i in range(1, 10):
                    if indices[i] != [] and indices[i] == indices_2[i]:
                        for column3 in a_sudoku.T:
                            if not np.array_equal(column, column3) and not np.array_equal(column2, column3):
                                column3[indices[i][0]].probability_dict[i] = False
                                column3[indices[i][1]].probability_dict[i] = False
                indices_2 = {n: [] for n in range(1, 10)}
                merged_dict_2 = {n: [] for n in range(1, 10)}
        indices = {n: [] for n in range(1, 10)}
        merged_dict = {n: [] for n in range(1, 10)}
        doubles_in_column = []


# Solves the given sudoku puzzle

def solve(a_sudoku):

    global sudoku_input
    global sudoku
    global units

    sudoku_input = a_sudoku

    # Initializes a Sudoku grid
    sudoku = np.empty([9, 9], dtype=object)

    # Ins unit objects
    units = [Unit(r, c) for r in range(9) for c in range(9)]

    count = 0

    while not finished(sudoku):

        solve_one_step(sudoku)

        count += 1

        if count == 15:
            break

    return sudoku


# Solves 1000 Sudoku puzzles and counts the correctly solved ones (594/1000)

correct_count = 0
for i in range(1000):
    comparison = solve(X_test[i]).astype(str) == Y_test[i].astype(str)
    if comparison.all():
        correct_count += 1

print(correct_count)
