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


def region(r, c, sudoku):
    rr = (r // 3) * 3
    rc = (c // 3) * 3
    return sudoku[rr:(rr + 3), rc:(rc + 3)]


def finished(sudoku):
    for row in sudoku:
        if 0 in row:
            return False
    return True


def is_possible(r, c, n, sudoku):
    if n in sudoku[r]:
        return False
    if n in sudoku[:, c]:
        return False
    if n in region(r, c, sudoku):
        return False
    return True


def solve(sudoku):
    for r in range(9):
        for c in range(9):
            if sudoku[r, c] == 0:
                for n in range(1, 10):
                    if is_possible(r, c, n, sudoku):
                        sudoku[r, c] = n
                        solve(sudoku)
                        if not finished(sudoku):
                            sudoku[r, c] = 0
                return sudoku


# Solves 1000 Sudoku puzzles and counts the correctly solved ones (1000/1000)

correct_count = 0
for i in range(1000):
    comparison = solve(X_test[i]) == Y_test[i]
    if comparison.all():
        correct_count += 1

print(correct_count)



