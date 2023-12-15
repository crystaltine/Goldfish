from game import C4Board

class C4Engine:
    """
    Moves are integers from lowest column (0) to highest column (num_cols - 1), default (6).
    
    Evaluation:
    + 0 for unsure
    + 1 for draw
    + 2 for player 1 win
    + 3 for player 2 win
    """
    # int to evaluation integer
    
    def __init__(self):
        """
        This engine is instance-based so that it can use a transposition table.
        """
        self.ttable = {}
        self._lookups = 0
        
        self.PLY_LIMIT = 10
    
    def bestmoves(self, board: C4Board) -> list:
        """
        Returns a list of integers representing the columns where the player should move
        """
        
        currfen = board.get_fen()
        evals = {}
        
        self.lookups = 0
        
        # Search down each of the columns
        for col in board.all_available_moves():
            board.make_move_at_column(col)
            
            eval = -self.negamax(board, -100, 100, 0)
            
            board.set_position(currfen)
            
            print(f"Move @ \x1b[32mColumn {col}\x1b[0m: \x1b[33m{eval}\x1b[0m")
            
            evals[col] = eval
            
        # Loop through and find moves that resulted in the best evaluation (here, they are the highest scoring moves)
        max_eval = max(evals.values())
        
        # Find the indices of the max_eval
        indicies = [i for i in evals.keys() if evals.get(i) is not None and evals.get(i) == max_eval]
        
        print(f"Lookups this search: \x1b[33m{self._lookups}\x1b[0m")
        self._lookups = 0
        
        return indicies
    
    def negamax(self, board: C4Board, alpha: int, beta: int, ply: int) -> int:
        # print(f"[Negamax] Searching at depth \x1b[34m{ply}\x1b[0m ply...")
        """
        Returns the evaluation for the player whose turn it is to move.
        Uses an evaluation-based scheme: 100 for positive result (win on this side), -100 for negative result (loss on this side), 0 for draw.
        """
        
        if ply >= self.PLY_LIMIT:
            return self.evaluate_position(board)
        
        if board.get_result() >= 2: # meaning there is a winner
            return -100
        
        if board.get_result() == 1:            
            # Add the board to the transposition table
            return 0 # draw
        
        # return ttable evaluation if it exists
        ttable_eval = self.ttable.get(board.get_fen())
        if ttable_eval is not None:
            self._lookups += 1
            return ttable_eval
        
        best_value = -100
        
        for move in board.all_available_moves():
            # Move here is a zero-indexed column number
            
            currfen = board.get_fen()
            board.make_move_at_column(move)
            value = -self.negamax(board, -beta, -alpha, ply + 1)    
            board.set_position(currfen)
            
            best_value = max(best_value, value)
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break
            
        # Store the result in the transposition table
        self.ttable[board.get_fen()] = best_value

        return best_value           
        

    def evaluate_position(self, board: C4Board) -> int:
        """
        Returns static evaluation (if any) of the board.
        
        Currently just returns based on board result
        """
        
        match board.get_result():
            case 0:
                return 0
            case 1:
                return 0
            case 2:
                return 100
            case 3:
                return -100
            case _:
                return 0