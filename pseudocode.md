### depth limited minimax
def get_action(self, state):
    _, move = depth_limited_minimax(state, 0, 2)

def depth_limited_minimax(self, curr_state, curr_depth, player_id):
    if curr_state is terminal state:
        return score of curr state, None
    if curr_depth == depth_limit
        return score of curr state, None

    legal_moves = ...
//    legal_move_count = len(legal_moves)
    successors = next states of current state after taking actions in legal_moves
    
    if player_id == 1: // human player -> maximize
        scores = [depth_limited_minimax(sucessor, curr_depth++, 2)[0]]
        best_score = max(scores)
    else: // id = 2 -> ai player -> minimize
        scores = [depth_limited_minimax(sucessor, curr_depth, 1)[0]]
        best_score = min(scores)
    return best_score, best_move = move that leads to best score

### minimax after having game state
def minimax(state, maximizing)
    valid_moves = state.get_empty_squares()
    successors = get successor of valid move 

    if maximizing:
        scores = array of scores returned from minimax(successors, false)
        best_score = get max scores 
    else:
        scores = array of scores returned from minimax(successors, true)
        best_score = get max scores 

    return (score, the action that leads to optimal score)