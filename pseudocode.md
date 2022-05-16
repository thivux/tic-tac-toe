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