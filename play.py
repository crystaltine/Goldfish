from game import C4Board
from engine import C4Engine

def collect_game_settings() -> tuple:
    num_rows = None
    num_cols = None
    connect_num = None
    
    while connect_num is None:
        try:
            connect_num = input("Enter number of connected pieces to win (Press \x1b[35menter\x1b[0m for default = 4): ")
            
            if connect_num == '':
                connect_num = 4
            else:
                connect_num = int(connect_num)
                
        except ValueError:
            print("\x1b[31mInvalid number of connected pieces! Integer from 1 to 20 required! Press \x1b[35menter\x1b[0m for default = 4:\x1b[0m ")
            connect_num = None
    
    while num_cols is None:
        try:
            num_cols = input("Enter number of columns (Press \x1b[35menter\x1b[0m for default = 7): ")
            
            if num_cols == '':
                num_cols = 7
            else:
                num_cols = int(num_cols)
                
        except ValueError:
            print("\x1b[31mInvalid number of columns! Integer from 1 to 20 required! Press \x1b[35menter\x1b[0m for default = 7:\x1b[0m ")
            num_cols = None
            
    while num_rows is None:
        try:
            num_rows = input("Enter number of rows (Press \x1b[35menter\x1b[0m for default = 6): ")
            
            if num_rows == '':
                num_rows = 6
            else:
                num_rows = int(num_rows)
                
        except ValueError:
            print("\x1b[31mInvalid number of rows! Integer from 1 to 20 required! Press \x1b[35menter\x1b[0m for default = 6:\x1b[0m ")
            num_rows = None
    
    return num_cols, num_rows, connect_num

def run_game():
    
    goldfish = C4Engine()
    
    num_cols, num_rows, connect_num = collect_game_settings()
    print(f"Game parameter types: {type(num_cols)}, {type(num_rows)}, {type(connect_num)}")
    
    print(f"\x1b[34mWelcome to Connect 4! You are playing with a\x1b[0m {num_cols}x{num_rows}\x1b[34m board, with \x1b[0m{connect_num}\x1b[34m connected pieces required to win.\x1b[0m")
    
    board = C4Board(num_cols, num_rows, connect_num)
    print()
    print(board)
    
    while not board.get_result():
        
        move = None
        while move is None:
            move = input("Enter a command or a column number: ")
            if move == 'quit' or move == 'exit':
                return
            
            if move.startswith('eval'):
                print(f"Best moves in this position: {goldfish.bestmoves(board)}")
                move = None
                continue
            
            if move.startswith('setpos '):
                # parse fenstr from input
                fenstr = move[7:]
                board.set_position(fenstr)
                move = None
                print("\x1b[32mPosition set!\x1b[0m")
                print(board)
                continue
            
            if move.startswith('getfen'):
                print(f"\x1b[32mBoard FEN string: \x1b[0m{board.get_fen()}")
                move = None
                continue
            
            if move.startswith('checkresult'):
                board.check_result()
                print(f"\x1b[32mwinner code: {board._result}, reason={board._win_reason}, locs={board.win_locs}\x1b[0m")
                move = None
                continue

            try:
                move = int(move)

                res = board.make_move_at_column(move)
                if not res:
                    print(f"\x1b[31mInvalid move or command! Enter a non-full column between 0 and {num_cols - 1}!\x1b[0m")
                    move = None
                    
            except ValueError:
                print(f"\x1b[31mInvalid move or command! Enter a non-full column between 0 and {num_cols - 1}!\x1b[0m")
                move = None
        print()
        print(board)
    
    print("\n\x1b[1mGame Over! Result:", "Draw" if board.get_result() == 1 else "Player 1 Wins" if board.get_result() == 2 else "Player 2 Wins\x1b[0m")
    print(f"^ Game FEN: \x1b[32m{board.get_fen()}\x1b[0m")
    
if __name__ == '__main__':
    run_game()