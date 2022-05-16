from copy import deepcopy
import random as rand
import sys
import pygame
import numpy as np
from constants import *


# pygame setup
pygame.init
screen = pygame.display.set_mode(size=(WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')


'''
controls the board 
attributes: board, x2, x1, o2, o1, score, empty_squares
'''
class GameState: 
    def __init__(self, prev_state=None, new_move=None):
        if prev_state is None:          # first time initialize a game state
            self.board = np.zeros(shape=(NUM_ROWS, NUM_COLS))
            self.empty_squares = []
            for i in range(NUM_ROWS):
                for j in range(NUM_COLS):
                    self.empty_squares.append((i, j))
            self.x2 = 0     # number of lines with 2 x's and 1 blank
            self.x1 = 0     # number of lines with 1 x's and 2 blanks
            self.o2 = 0     # number of lines with 2 o's and 1 blank
            self.o1 = 0     # number of lines with 1 o's and 2 blanks
            self.score = 0
        else:
            self.new_move_row, self.new_move_col, player_id = new_move
            self.board = deepcopy(prev_state.board)
            self.empty_squares = deepcopy(prev_state.get_empty_squares())
            self.mark_square(self.new_move_row, self.new_move_col, player_id)
            self.x2 = prev_state.x2
            self.x1 = prev_state.x1
            self.o2 = prev_state.o2
            self.o1 = prev_state.o1

    def get_successor(self, row, col, player_id):
        return GameState(self, (row, col, player_id))

    '''
    modify x1, x2, o1, o2 after an action is taken
    '''
    def modify_score_components(self, direction):
        new_move_value = self.board[self.new_move_row][self.new_move_col]
        # check row 
        if direction=='row':
            in_a_row = 0
            opponent_count = 0  
            for col in range(NUM_COLS):
                if self.board[self.new_move_row][col] == new_move_value:
                    in_a_row += 1
                if self.board[self.new_move_row][col] == (new_move_value % 2 + 1):
                    opponent_count += 1

        # check col
        if direction=='col':
            in_a_row = 0
            opponent_count = 0
            for row in range(NUM_ROWS):
                if self.board[row][self.new_move_col] == new_move_value:
                    in_a_row += 1
                if self.board[row][self.new_move_col] == (new_move_value % 2 + 1):
                    opponent_count += 1
        
        # check diagonally desc
        if direction=='dia_desc':
            in_a_row = 0
            opponent_count = 0
            for i in range(NUM_COLS):
                if self.board[i][i] == new_move_value:
                    in_a_row += 1
                if self.board[i][i] == (new_move_value % 2 + 1):
                    opponent_count += 1

        # check diagonally ascen
        if direction=='dia_ascen':
            in_a_row = 0
            opponent_count = 0
            for i in range(NUM_COLS):
                if self.board[i][NUM_COLS - i - 1] == new_move_value:
                    in_a_row += 1
                if self.board[i][NUM_COLS - i - 1] == (new_move_value % 2 + 1):
                    opponent_count += 1

        # increase current player's score
        if in_a_row == 2 and opponent_count == 0:
            if new_move_value == 1:
                self.x2 += 1
                self.x1 -= 1
            else:
                self.o2 += 1
                self.o1 -= 1
        if in_a_row == 1 and opponent_count == 0:
            if new_move_value == 1:
                self.x1 += 1
            else:
                self.o1 += 1

        # decrease opponent's score
        if opponent_count == 2:
            if new_move_value == 1:
                self.o2 -= 1
            else:
                self.x2 -= 1
        if opponent_count == 1:
            if new_move_value == 1:
                self.o1 -= 1
            else:
                self.x1 -= 1

    # evaluation function
    def get_score(self):
        self.modify_score_components(direction='col')        
        self.modify_score_components(direction='row')        
        if self.new_move_col == self.new_move_row:
            self.modify_score_components(direction='dia_desc')        
        if self.new_move_col + self.new_move_row + 1 == NUM_COLS:
            self.modify_score_components(direction='dia_ascen')        
        # print(f'{self.x2}, {self.x1}, {self.o2}, {self.o1}')

        return 3 * self.x2 + self.x1 - (3 * self.o2 + self.o1)
        
    def check_result(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''
        # check virtically
        if (self.board[0][self.new_move_col] == self.board[1][self.new_move_col] == self.board[2][self.new_move_col] != 0):
            if show:
                top = (self.new_move_col * SQUARE_SIZE + SQUARE_SIZE / 2, OFFSET)
                bottom = (self.new_move_col * SQUARE_SIZE + SQUARE_SIZE / 2, SQUARE_SIZE * NUM_ROWS - OFFSET)
                self.show_final_line(self.board[0][self.new_move_col], start_pos=top, end_pos=bottom)
            return self.board[0][self.new_move_col]

        # check horizontally
        if (self.board[self.new_move_row][0] == self.board[self.new_move_row][1] == self.board[self.new_move_row][2] != 0):
            if show:
                left = (OFFSET, SQUARE_SIZE * self.new_move_row + SQUARE_SIZE / 2)
                right = (SQUARE_SIZE * NUM_COLS - OFFSET, SQUARE_SIZE * self.new_move_row + SQUARE_SIZE / 2)
                self.show_final_line(self.board[self.new_move_row][0], start_pos=left, end_pos=right)
            return self.board[self.new_move_row][0]
        
        if self.new_move_row == self.new_move_col or self.new_move_col + self.new_move_row + 1 == NUM_COLS:
            # check diagonally desc 
            if (self.board[0][0] == self.board[1][1] == self.board[2][2] != 0):
                if show:
                    top_left = (OFFSET, OFFSET)
                    bot_right = (SQUARE_SIZE * NUM_ROWS - OFFSET, SQUARE_SIZE * NUM_COLS - OFFSET)
                    self.show_final_line(self.board[0][0], top_left, bot_right)
                return self.board[0][0]

            # check diagonally asc
            win_diagonally_asc = True
            for i in range(NUM_COLS - 1):
                if (self.board[i][NUM_COLS - 1 - i] != self.board[i + 1][NUM_COLS - 2 - i]):
                    win_diagonally_asc = False
                    break
            if win_diagonally_asc and self.board[0][2] != 0:
                if show:
                    top_right = (SQUARE_SIZE * NUM_COLS - OFFSET, OFFSET)
                    bot_left = (OFFSET, SQUARE_SIZE * NUM_COLS - OFFSET)
                    self.show_final_line(self.board[0][2], top_right, bot_left)
                return self.board[0][2]
        
        return 0

    def show_final_line(self, who_win, start_pos, end_pos):
        color = CROSS_COLOR if who_win == 1 else CIRCLE_COLOR
        pygame.draw.line(screen, color, start_pos, end_pos, CIRCLE_WIDTH)

    def mark_square(self, row, col, player_id):
        if self.is_empty_square(row, col):
            self.board[row][col] = player_id
            self.empty_squares.remove((row, col))
            # print('marking: ', (row, col))
            # print('empty squares: ', self.empty_squares, end='\n')
        else:
            print('square already marked')

    def is_empty_square(self, row, col):
        return self.board[row][col] == 0

    def get_empty_squares(self):
        return self.empty_squares

    def is_full(self):
        return len(self.empty_squares) == 0


class AI:
    def __init__(self, type=MINIMAX_AI, id=2):
        self.type = type        # type 0: random ai, type 1: minimax ai 
        self.id = id

    def random_ai(self, board):
        empty_squares = board.get_empty_squares()
        idx = rand.randrange(0, len(empty_squares))
        return empty_squares[idx]
    
    '''
        return score, move
        by default, this function tries to 
        minizing the game result, because it is ai's turn.
    '''
    def minimax(self, board, maximizing=False): 
        # check if the board is in final state
        res = board.check_result()
        # print(res)
        if res == 1:    # player 1 aka human wins
            return 1, None
        elif board.is_full():  # draw
            return 0, None
        elif res == 2:           # player 2 aka ai wins
            return -1, None
        
        # evaluate the next action
        if maximizing:
            max_eval = -100
            best_move = None
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares: 
                temp_board = deepcopy(board)
                temp_board.mark_square(row, col, player=1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        else:
            min_eval = 100
            best_move = None
            empty_squares = board.get_empty_squares()
            for (row, col) in empty_squares: 
                temp_board = deepcopy(board)
                temp_board.mark_square(row, col, player=self.id)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    def get_action(self, board):
        if self.type == 0:  # random AI
            move = self.random_ai(board)
        else:
            eval, move = self.minimax(board, False)
            print(f'ai has chosen move at pos {move} with an evaluation of {eval}')
        return move

    

# control game UI
class Game:
    def __init__(self):
        screen.fill(BACKGROUND_COLOR)
        self.show_lines()
        self.game_state = GameState()
        self.ai = AI()
        self.opponent = 3
        print('playing with minimax ai')
        self.player_id = 1         # 1-cross, 2-circle
        self.is_running = True

    def show_lines(self):
        # vertical lines 
        for i in range(NUM_ROWS - 1):
            pygame.draw.line(screen, color=LINE_COLOR, start_pos=((i + 1) * SQUARE_SIZE, 0), end_pos=((i + 1) * SQUARE_SIZE, HEIGHT), width=LINE_WIDTH)
        
        # horizontal lines 
        for i in range(NUM_ROWS - 1):
            pygame.draw.line(screen, color=LINE_COLOR, start_pos=(0, (i + 1) * SQUARE_SIZE), end_pos=(HEIGHT, (i + 1) * SQUARE_SIZE), width=LINE_WIDTH)
    
    def take_turn(self, row, col):
        # self.game_state.mark_square(row, col, self.player)
        self.game_state = self.game_state.get_successor(row, col, self.player_id)
        self.draw_fig(row, col)
        self.next_turn()

    def draw_fig(self, row, col):
        if self.player_id == 1:
            # draw cross
            top_left = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            top_right = ((col + 1) * SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET)
            bottom_left = (col * SQUARE_SIZE + OFFSET, (row + 1) * SQUARE_SIZE - OFFSET)
            bottom_right = ((col + 1) * SQUARE_SIZE - OFFSET, (row + 1) * SQUARE_SIZE - OFFSET)
            pygame.draw.line(screen, color=CROSS_COLOR, start_pos=top_left, end_pos=bottom_right, width=CROSS_WIDTH)
            pygame.draw.line(screen, color=CROSS_COLOR, start_pos=top_right, end_pos=bottom_left, width=CROSS_WIDTH)

        if self.player_id == 2:
            # draw circle
            coordinate_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
            coordinate_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.circle(screen, color=CIRCLE_COLOR, center=(coordinate_x, coordinate_y), radius=RADIUS, width=CIRCLE_WIDTH)

    def coordinates_to_board(self, pos):
        return pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

    def next_turn(self):
        self.player_id = self.player_id % 2 + 1

    def change_opponent(self, opponent_id):
        self.opponent = opponent_id
        if self.opponent == OTHER_PERSON:
            print('playing with another person...')
        if self.opponent == RANDOM_AI:
            self.ai.type = RANDOM_AI
            print('playing with random ai...')
        if self.opponent == MINIMAX_AI:
            self.ai.type = MINIMAX_AI
            print('playing with minimax ai...')

    def reset(self):
        self.__init__()

    def check_is_over(self):
        if self.game_state.is_full() or self.game_state.check_result(show=True) != 0:
            self.is_running = False
    

def main():

    # tutorial
    print('press 1 to play with another person')
    print('press 2 to play with random ai')
    print('press 3 to play with minimax ai')
    print('press r to start a new game', end='\n\n')

    game = Game()

    # main loop 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game.is_running:
                row, col = game.coordinates_to_board(event.pos)
                game.take_turn(row, col)
                game.check_is_over()
            # change game config
            if event.type == pygame.KEYDOWN:
                # change opponent
                if event.key == pygame.K_1:
                    game.change_opponent(1)
                if event.key == pygame.K_2:
                    game.change_opponent(2)
                if event.key == pygame.K_3:
                    game.change_opponent(3)
                # r-restart game
                if event.key == pygame.K_r:
                    game.reset()


        if (game.opponent == RANDOM_AI or game.opponent == MINIMAX_AI) and game.player_id == game.ai.id and game.is_running:
            pygame.display.update()
            row, col = game.ai.get_action(game.game_state)
            game.take_turn(row, col)
            game.check_is_over()

        pygame.display.update()

main()
