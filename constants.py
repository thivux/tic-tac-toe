
# screen
WIDTH = 600
HEIGHT = 600
BACKGROUND_COLOR = (28, 170, 156)

# division of board
NUM_ROWS = 5
NUM_COLS = 5
SQUARE_SIZE = WIDTH // NUM_ROWS

# line
LINE_COLOR = (23, 145, 135)
LINE_WIDTH = 5

# circle
RADIUS = SQUARE_SIZE // 4
CIRCLE_WIDTH = LINE_WIDTH * 2
CIRCLE_COLOR = (239, 231, 200)

# cross
OFFSET = SQUARE_SIZE // 5
CROSS_WIDTH = CIRCLE_WIDTH
CROSS_COLOR = (66, 66, 66)

# opponents
OTHER_PERSON = 1
RANDOM_AI = 2
MINIMAX_AI = 3
