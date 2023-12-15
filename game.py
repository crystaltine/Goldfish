class C4Board:
    """
    Represents a 7-column, 6-row, gravity-affected, 2-player Connect Four board.
    """
    
    def __init__(self, cols: int = 7, rows: int = 6, connect_num: int = 4):
        """
        Initializes a new C4Board object with an empty board and no winner.
        """
        
        # Board squares are None, False for Player 1, True for Player 2.
        # We actually represent columns as lists. When len(col) == 6, the column is full.
        # Index 0 of each of these columns is the bottom of the column.
        self._board = [[] for i in range(cols)]
        self.size = (cols, rows)
        self.connect_num = connect_num
        self._result = 0 # 0 for none yet, 1 for draw, 2 for player 1 win, 3 for player 2 win
        self._win_reason = 0 # 0 for none yet, 1 for horizontal, 2 for vertical, 3 for diagonal
        self._turn = False # Start with Player 1's turn
        
        self.win_locs = [] # List of (x, y) tuples of the winning locations
        
    def __str__(self) -> str:
        return self.to_string()

    def __hash__(self) -> int:
        """
        Returns a hash of the board.
        """
        boardstate = [tuple(col) for col in self._board]
        boardstate.append(self._turn)
        
        return hash(tuple(boardstate))

    def make_move_at_column(self, col: int) -> bool:
        """
        Places a piece at the specified column. Zero-indexed (0 for leftmost col, 6 for rightmost col).
        Returns True if the move is able to be played (column is not full), False otherwise.
        
        If the game is won, raises a ValueError.
        """
        
        if (col < 0 or col >= self.size[0]):
            return False
        
        # Check if column is full
        if len(self._board[col]) == self.size[1]:
            return False
        
        # Otherwise, "drop" a piece into the column (append to the list)
        self._board[col].append(self._turn)
        
        # Change turns
        self._turn = not self._turn
        
        # Check for winner
        self.check_result()
        
        return True
    
    def delete_move_at_column(self, col: int) -> bool:
        """
        Removes the topmost piece from the specified column. Zero-indexed (0 for leftmost col, 6 for rightmost col).
        Returns True if the move is able to be undone (column is not empty), False otherwise.
        
        This function is provided assuming that it will be only be called with the correct column number.
        """
        
        if len(self._board[col]) == 0:
            return False
        
        self._board[col].pop()
        
        # Change turns back
        self._turn = not self._turn
        
        # Remove result
        self._result = 0
        
        # Remove loggings
        self._win_reason = 0
        self.win_locs = []
        
        return True
    
    def p1_won(self) -> bool:
        """
        Returns True if Player 1 has won, False otherwise.
        """
        
        return self._result == 2

    def p2_won(self) -> bool:
        """
        Returns True if Player 2 has won, False otherwise.
        """
        
        return self._result == 3

    def is_draw(self) -> bool:
        """
        Returns True if the game is a draw, False otherwise.
        """
        
        return self._result == 1
    
    def set_position(self, fen: str) -> None:
        """
        Sets the boardstate to the board specified by the FEN string.
        FEN string formatting:
        
        A string of characters, where each character is one of the following:
        + 1 for player 1's piece
        + 2 for player 2's piece
        + Whitespaces are placed between columns
        
        Start at the bottom right of the board, then move up. At the top of the column, move left to the next column.
        Then at the end of the string, a space and then 1 for Player 1's turn, 2 for Player 2's turn.
        
        ### Example FEN:
        Board:
        ```
        Player 2's Turn
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | |1| | | | |
        | | |1|1| |2| |
        |2|2|2|1|2|1|1|
        =0=1=2=3=4=5=6=
        ```
        
        FEN:
        `1 12 2 11 211 2 2 2`
        """
        
        self._board = []
        self._turn = int(fen[-1]) == 2
        
        fen = fen[:-2]
         
        # Parse into chunks
        chunks = fen.split(" ")
        
        for chunk in chunks:
            if chunk == '':
                self._board.append([])
                continue
            
            self._board.append([])
            
            for char in chunk:
                if char == '1':
                    self._board[-1].append(False)
                elif char == '2':
                    self._board[-1].append(True)
                    
        # Reverse the board
        self._board.reverse()                        
    
    def get_fen(self) -> str:
        """
        Gets the boardstate to the board as a FEN string.
        FEN string formatting:
        
        A string of characters, where each character is one of the following:
        + 1 for player 1's piece
        + 2 for player 2's piece
        + Whitespaces are placed between columns
        
        Start at the bottom right of the board, then move up. At the top of the column, move left to the next column.
        Then at the end of the string, a space and then 1 for Player 1's turn, 2 for Player 2's turn.
        
        ### Example FEN:
        Board:
        ```
        Player 2's Turn
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | |1| | | | |
        | | |1|1| |2| |
        |2|2|2|1|2|1|1|
        =0=1=2=3=4=5=6=
        ```
        
        FEN:
        `1 12 2 11 211 2 2 2`
        """
        
        chunks = []
        
        for _list in self._board:
            chunk = []
            for item in _list:
                chunk.append("2" if item else "1")
            chunks.append("".join(chunk))
            
        # Reverse chunks due to how board is stored
        chunks.reverse()
        
        # add the turn        
        return " ".join(chunks) + " " + ("2" if self._turn else "1")
    
    def set_turn(self, player_num: int) -> None:
        """
        Sets the turn to the specified player number (1 or 2).
        1 is by default the first player.
        """
        
        self._turn = player_num == 2
        
    def get_turn(self) -> int:
        """
        Returns the number of the player whose turn it is (1 or 2).
        """
        
        return 2 if self._turn else 1
    
    def check_result(self):
        """
        Internal function that scans the board to check for a winner (4 in a row diagonally, vertically, or horizontally).
        
        This sets `self._result` as follows:
        0 for no result yet
        1 for draw
        2 for player 1 win
        3 for player 2 win        
        """
        
        # If board is full, it's a draw
        if all(len(col) == self.size[1] for col in self._board):
            self._result = 1
            return
        
        # Check for win along a diagonal (probably the most common)
        # This should similar to checking along a row, but we need to check both directions of diagonal
        # And we also can cut some of the board off since we can't have a diagonal win in the first (connect_num - 1) rows
        # or the last (connect_num - 1) rows
        
        # top left to bottom right diagonals
        for i in range(self.size[0] - self.connect_num + 1):
            # For each element in those lists, check connect_num spaces below it
            for j in range(len(self._board[i]) - self.connect_num + 1):
                # Check if all of those elements are the same
                if (
                len(self._board[i]) > j and
                len(self._board[i + 1]) > j + 1 and
                len(self._board[i + 2]) > j + 2 and
                len(self._board[i + 3]) > j + 3 and
                self._board[i][j] == self._board[i + 1][j + 1] == self._board[i + 2][j + 2] == self._board[i + 3][j + 3]):
                    self._result = 3 if self._board[i][j] else 2 if self._board[i][j] == False else 0
                    #self._win_reason = 3
                    #self.win_locs = f"BOARD:\n{self._board}\n>> Winning indxs: {[(i, j), (i + 1, j + 1), (i + 2, j + 2), (i + 3, j + 3)]}"
                    return
                    
        # top right to bottom left diagonals
        for i in range(self.size[0] - self.connect_num + 1):
            # For each element in those lists, check connect_num spaces below it
            for j in range(self.connect_num - 1, len(self._board[i])):
                # Check if all of those elements are the same
                if (
                len(self._board[i]) > j and
                len(self._board[i + 1]) > j-1 and
                len(self._board[i + 2]) > j-2 and
                len(self._board[i + 3]) > j-3 and    
                self._board[i][j] == self._board[i + 1][j - 1] == self._board[i + 2][j - 2] == self._board[i + 3][j - 3]):
                    self._result = 3 if self._board[i][j] else 2 if self._board[i][j] == False else 0
                    #self._win_reason = 3
                    #self.win_locs = f"BOARD:\n{self._board}\n>> Winning indxs: {[(i, j), (i + 1, j - 1), (i + 2, j - 2), (i + 3, j - 3)]}"
                    return
        
        # Check for win along a row (second most common)
        # We need to check the beginnings of chains in the top (col - connect_num + 1) lists
        for i in range(self.size[0] - self.connect_num + 1):
            # For each element in those lists, check connect_num spaces below it
            for j in range(len(self._board[i])):
                # Check if all of those elements are the same
                if (
                len(self._board[i]) > j and
                len(self._board[i + 1]) > j and
                len(self._board[i + 2]) > j and
                len(self._board[i + 3]) > j and
                self._board[i][j] == self._board[i + 1][j] == self._board[i + 2][j] == self._board[i + 3][j]):
                    
                    self._result = 3 if self._board[i][j] else 2 if self._board[i][j] == False else 0
                    #self._win_reason = 1
                    #self.win_locs = [(i, j), (i + 1, j), (i + 2, j), (i + 3, j)]
                    return
        
        # Check for win along a column (least common since people just drop pieces)
        # Loop through each column
        for col in range(len(self._board)):
            if (len(self._board[col]) < self.connect_num):
                continue
            
            for piece in range(len(self._board[col]) - self.connect_num + 1):
                if (self._board[col][piece] == self._board[col][piece + 1] == self._board[col][piece + 2] == self._board[col][piece + 3]):
                    self._result = 3 if self._board[col][piece] else 2 if self._board[col][piece] == False else 0
                    #self._win_reason = 2
                    #self.win_locs = f"BOARD: \n{self._board}\n Column idx {col}, col={self._board[col]}, @position {piece}"
                    return
                
        self._result = 0
        #self._win_reason = 0
        #self.win_locs = []

    def get_result(self) -> int:
        """
        Returns:
        + 0 for no result yet
        + 1 for draw
        + 2 for player 1 win
        + 3 for player 2 win
        """
        
        return self._result
    
    def all_available_moves(self) -> list:
        """
        Returns a list of all available moves (columns that are not full).
        
        Example return: `[0, 1, 2, 3, 4, 6]` when columns 5 is full.
        """
        
        return [i for i in range(self.size[0]) if len(self._board[i]) < self.size[1]]
    
    def to_string(self) -> str:
        
        """
        Returns a string representation of the board in the a readable format:
        Example:
        ```
        Player 2's Turn
        | | | | | | | |
        | | | | | | | |
        | | | | | | | |
        | | |1| | | | |
        | | |1|1| |2| |
        |2|2|2|1|2|1|1|
        =0=1=2=3=4=5=6=
        ```        
        """
        
        string = ""
        # Remember that colums are stored as lists, so we need to print the board in an inverted way
        
        if self._turn == False: # Player 1's turn
            string += "\x1b[33mPlayer 1's\x1b[0m Turn\n"
        else: # Player 2's turn
            string += "\x1b[31mPlayer 2's\x1b[0m Turn\n"
            
        for row in range(self.size[1] - 1, -1, -1):
            for col in range(self.size[0]):
                if len(self._board[col]) <= row:
                    string += "| "
                elif self._board[col][row] == False:
                    string += "|\x1b[33m1\x1b[0m"
                else:
                    string += "|\x1b[31m2\x1b[0m"
            string += "|\n"
        
        # Add the bottom column numbers
        string += "".join([f"={i}" for i in range(self.size[0])]) + "="
        
        return string