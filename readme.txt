
Summary
--------

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


Instructions to run
---------------------

To run the sudoku solver on the puzzles directory

    python3 sudoku.py

To train the threshold on the data directory

    python3 sudoku_train.py
