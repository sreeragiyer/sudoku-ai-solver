
# Summary

This is a sudoku solver that uses AC-3 and XYWing inferences. It also gives an estimate of the difficulty of a puzzle as per Will Shortz’ levels.

There are 2 files containing the souce code for the solver- sudoku.py and XYWing.py. 
Backtracking, MRV and AC-3 are implemented in sudoku.py while XYWing.py contains the implementation of the XY-Wing inference.
The ./puzzles directory contains 16 puzzles given for the assignment.
The code outputs the solved sudoku board and the number of guesses required for:
    - Plain Backtracking
    - Backtracking with MRV (no inferences)
    - Backtracking with MRV using only AC-3 inference
    - Backtracking with MRV using AC-3 and XY-Wing inferences
It also outputs the difficulty level of the problem.
sudoku_train.py contains the code to train the theshold.


# How to run


To run the sudoku solver on the puzzles directory (to test the solver, you can add your own puzzles here)

    python3 sudoku.py

To train the threshold on the data directory

    python3 sudoku_train.py

# Computing the difficulty level of a Sudoku puzzle

- A more difficult Sudoku will be one that takes a human more time to solve. Determining difficulty of Sudoku puzzles can be done by counting the number of times different inference tech-
niques have been used. Simpler problems will require lesser number of techniques to be used, and
can be solved by a human by smart guesswork. More difficult problems will involve using tech-
niques like XY-Chains, AIC, etc. (Reference for various techniques that can be used in Sudoku:
http://hodoku.sourceforge.net/en/techniques.php)
- Each technique can have a cost associated with it. Simpler techniques (ones that a human would
be able to see easily) like single values, remote pairs can have a lower cost associated as compared
to more complicated techniques like XYZ-chains and Nice Loops. The total cost will be sum of the
number of times a technique is used multiplied by its cost. The higher this total cost, the more
difficult the problem. So, if there are more complicated techniques implemented in the waterfall,
we will be able to get a more accurate estimation.
We can also add the total number of guesses to the previous total cost since the more difficult
problems will have larger number of guesses.
- Given a training set (we know the difficulty of the problems in this set), we run the solver and get
the cost for each of the problems. For a given level of difficulty, the minimum cost (from all the
problems in that difficulty level) associated with that level will be the threshold for a problem to
qualify for that difficulty level. After computing the 3 thresholds (since Will Shortz’ problems are
grouped into 4 difficulty levels), we can run the solver on a test problem to get the cost, compare
with the threshold and classify its difficulty.
