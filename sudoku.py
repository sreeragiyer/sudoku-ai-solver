import math
from os import listdir
from os.path import isfile, join
import re
from copy import deepcopy
from XYWing import xyWing


# Each variable is represented as board[i][j]
def getNextEmpty(board):
    rtot = len(board) 
    # return next blank cell
    for r in range(rtot):
        for c in range(rtot): 
            if board[r][c] == '-':
                return r, c
    return None, None  


def getNextMRV(board, domains):
    rtot = len(board)
    nextr=None
    nextc=None
    minsum = 10
    # return most constrained variable (cell)
    for r in range(rtot):
        for c in range(rtot): 
            if board[r][c] == '-':
                s = sum(domains[r][c])
                if s < minsum:
                    minsum = s
                    nextr = r
                    nextc = c
    return nextr, nextc  


def validateAndUpdateDomain(guess, row, col, d, additionalInferences, inferenceCtr):
    if d[row][col][guess-1]:
        domains = deepcopy(d)   # copying so that state is not mutated during AC3
        inferenceCtr = updateDomainWithAC3(guess, row, col, domains, additionalInferences, inferenceCtr)
        return [True, domains, inferenceCtr]
    return [False, d, inferenceCtr]


# inference by AC3. can also use XY-Wing in addition
def updateDomainWithAC3(guess, row, col, domains, additionalInferences, inferenceCtr):
    rows = len(domains) # length of complete row of the board
    rn = int(math.sqrt(rows))   # length of square
    # arc consistency by setting 'guess' for all cells in same column, row and square equal to false 
    # (so guess is removed from the domains of those variables)
    for c in range(rows):   # remove from cells in same column
        if domains[row][c][guess-1] and sum(domains[row][c]) == 2: # inference eliminated all possible other candidates
            inferenceCtr+=1
        domains[row][c][guess-1] = False
    for r in range(rows):   # remove from cells in same row
        if domains[row][c][guess-1] and sum(domains[row][c]) == 2: 
            inferenceCtr+=1
        domains[r][col][guess-1] = False
    row_start = (row // rn) * rn
    col_start = (col // rn) * rn
    for r in range(row_start, row_start + rn):  # remove from cells in same square
        for c in range(col_start, col_start + rn):
            if domains[row][c][guess-1] and sum(domains[row][c]) == 2: 
                inferenceCtr+=1
            domains[r][c][guess-1] = False
    domains[row][col][guess-1] = True   
    if additionalInferences:
        inferenceCtr = xyWing(domains, row, col, inferenceCtr)
    return inferenceCtr


# initialize domains of each variable based on the initial assignment of the board
# domain is represented as a n X n X 9 array
def initDomains(board):
    rows = len(board)
    domains = [[[True for k in range(9)] for j in range(rows)] for i in range(rows)]
    for i in range(rows):
        for j in range(rows):
            if board[i][j] != '-':
                # reduce domain based on constraints
                [_, domains, _] = validateAndUpdateDomain(board[i][j], i, j, domains, False, 0)
                for k in range(9):
                    if k+1 != board[i][j]:
                        domains[i][j][k] = False
    return domains


# only checks for the constraints with no inference
def validateNaively(board, guess, row, col):
    rows = len(board)
    rn = int(math.sqrt(rows))
    # check that guess is not present in row
    row_vals = board[row]
    if guess in row_vals:
        return False 
    # check that guess is not present in column
    col_vals = [board[i][col] for i in range(rows)]
    if guess in col_vals:
        return False
    row_start = (row // rn) * rn
    col_start = (col // rn) * rn
    # check if guess is not present in sqaure
    for r in range(row_start, row_start + rn):
        for c in range(col_start, col_start + rn):
            if board[r][c] == guess:
                return False
    return True



def sudokuByPlainBacktracking(board, guess_ctr):
    # select-unassigned-variable step
    row, col = getNextEmpty(board)
    # exit if no more variables to assign
    if row is None:  
        return [True, guess_ctr]
    # guess numbers in ascending order from 1 to 9
    for guess in range(1, 10): 
        # no inference in this case, only validation
        if validateNaively(board, guess, row, col):
            board[row][col] = guess
            [flag, guess_ctr] = sudokuByPlainBacktracking(board, guess_ctr)
            if flag:
                return [True, guess_ctr]
            guess_ctr+=1 # count number of guesses
        # restore to blank in case of incorrect guess
        board[row][col] = '-'
    return [False, guess_ctr] # board cannot be solved with current assignments


def sudokuByBacktrackingWithMRV(board, guess_ctr, domains):
    # select-unassigned-variable step
    row, col = getNextMRV(board, domains)
    # exit if no more variables to assign
    if row is None:  
        return [True, guess_ctr]
    # guess numbers in ascending order from 1 to 9
    for guess in range(1, 10): 
        # validation step
        if validateNaively(board, guess, row, col):
            board[row][col] = guess
            [flag, guess_ctr] = sudokuByBacktrackingWithMRV(board, guess_ctr, domains)
            if flag:
                return [True, guess_ctr]
            guess_ctr+=1 # count number of guesses
        # restore to blank in case of incorrect guess
        board[row][col] = '-'
    return [False, guess_ctr] # board cannot be solved with current assignments


def sudokuByBacktrackingWithMRVAndInference(board, guess_ctr, domains, additionalInferences, inferenceCtr):
    # select-unassigned-variable step
    row, col = getNextMRV(board, domains)
    # exit if no more variables to assign
    if row is None:  
        return [True, guess_ctr, inferenceCtr]
    # take the next guess as the next value between 1 to 9 that is available
    for guess in range(1, 10): 
        # validation and inference step
        [isValid, newDomains, inferenceCtr] = validateAndUpdateDomain(guess, row, col, domains, additionalInferences, inferenceCtr)
        if isValid:
            board[row][col] = guess
            [flag, guess_ctr, inferenceCtr] = sudokuByBacktrackingWithMRVAndInference(board, guess_ctr, newDomains, additionalInferences, inferenceCtr)
            if flag:
                return [True, guess_ctr, inferenceCtr]
            guess_ctr+=1 # count number of guesses
        # restore to blank in case of incorrect guess
        board[row][col] = '-'
    return [False, guess_ctr, inferenceCtr] # board cannot be solved with current assignments


#print nXn matrix
def printSudoku(board, guesses, fileName):
    print("\n--------------------------"+fileName+"--------------------------")
    rows = len(board)
    for i in range(rows):
        for j in range(rows):
            print(board[i][j], end="\t")
        print()
    print()


# get nXn array from string
def getboard(txt):
    rows = re.split('\n+', txt)
    board = []
    for r in rows:
        chars = re.split('\s+', r)
        prow = []
        for c in chars:
            if c == '-':
                prow.append('-')
            elif len(c) > 0:
                prow.append(int(c))
        if len(prow) > 0:
            board.append(prow)
    return board


def getTotalCost(guesses, inferenceCtr):
    return guesses + 20*inferenceCtr

def getDifficulty(guesses, inferenceCtr):
    thresh = []
    with open('thresholds.txt', 'r') as f:
        txt = f.read()
        txt = txt.split("\n")
        for s in txt:
            thresh.append(int(s))
    thresh.sort()
    c = getTotalCost(guesses, inferenceCtr)
    lvl = 4
    for i in range(len(thresh)):
        if c<thresh[i]:
            lvl = i+1
            break
    return lvl


if __name__ == "__main__":
    relDir = "./puzzles"
    allFiles = [f for f in listdir(relDir) if isfile(join(relDir, f))]
    # call the solver on each file
    for fileName in allFiles:
        f = open(join(relDir, fileName), "r")
        txt = f.read()
        board = getboard(txt)
        [isSolvable, g] = sudokuByPlainBacktracking(board, 0) 
        if isSolvable:
            printSudoku(board, g, fileName)
            print("Number of guesses by plain backtracking: ", g)
        else:
            print(fileName+" has no solution!")
        board = getboard(txt)
        domains = initDomains(board)
        [isSolvable, g] = sudokuByBacktrackingWithMRV(board, 0, domains)
        if isSolvable:
            print("Number of guesses by backtracking with MRV: ", g)
        else:
            print(fileName+" has no solution!")
        board = getboard(txt)
        domains = initDomains(board)
        [isSolvable, g, inferenceCtr] = sudokuByBacktrackingWithMRVAndInference(board, 0, domains, False, 0)
        if isSolvable:
            print("Number of guesses by backtracking with MRV and AC3: ", g)
        else:
            print(fileName+" has no solution!")
        board = getboard(txt)
        domains = initDomains(board)
        [isSolvable, g, inferenceCtr] = sudokuByBacktrackingWithMRVAndInference(board, 0, domains, True, 0)
        if isSolvable:
            print("Number of guesses by backtracking with MRV and AC3 + XY-Wing: ", g)
            print("Difficulty level: ", getDifficulty(g, inferenceCtr))
        else:
            print(fileName+" has no solution!")
        
