### minimax after having game state
valid_moves = state.get_empty_squares()
successors = get successor of valid move 
scores = successors.get_scores()

if maximizing:
    best_score = get max scores 
else:
    best_score = get max scores 

return (action, the action that leads to optimal score)