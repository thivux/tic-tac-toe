## Introduction
Classic tic-tac-toe with different modes:
- play against another person 
- play against random AI
- play against minimax AI
- play against alpha-beta pruning AI

You win when you can place a full row, column or diagonal with you mark.

By default, the board is of size 3x3, you can change it if you want.
## How to play
1. Install required libraries
    ```
    pip install < requirements.txt
    ```
2. Run the game
    ```
    python tic-tac-toe.py
    ```
3. Hotkeys
    - press `1` to play with another person
    - press `2` to play with random ai
    - press `3` to play with depth-limited minimax ai
    - press `r` to start a new game
4. Other configurations
    - change the size of the board: by changing value of `NUM_ROWS = NUM_COLS` in line 8 of constants.py
    - change the depth of alpha-beta pruning algorithm: by changing the value of the `depth` argument in line 198 of tic-tac-toe.py