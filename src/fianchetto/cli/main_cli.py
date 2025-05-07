from fianchetto.core.board_manager import BoardManager
from fianchetto.core.pieces import Color



def main():
    game = BoardManager()
    if main_menu(game):
        keep_going = True

        while keep_going:
            print_board(game)
            alg_move = input("Please enter a move by entering the starting and ending coordinates seprataed by commas (Ex: g1, f3): ")

            if alg_move.lower() == "reset":
                keep_going = False
                continue

            try:
                move = alg_to_coord(alg_move)

            except ValueError as e:
                print()
                print()
                print(e)
                continue

            try:
                game.move(move[0], move[1])

            except ValueError as e:
                print()
                print()
                print(e)
                continue


    main()


def main_menu(game: BoardManager):
    keep_going = True
    while keep_going:
        keep_going = False
        print()
        print("________________________")
        print("Welcome to FianchettoPy!")
        ans = input("Would you like to play a local game? Y/N (type Q to quit): ")
        if ans.lower() == "y":
            return start_game(game)
        
        elif ans.lower() == "n":
            print("")
            return quit()
        
        else:
            keep_going = True
            print("Please enter either Y or N")
            print()
    
def start_game(game: BoardManager):
    game.generate_starting_position()
    game.to_move = Color.WHITE
    return True

def alg_to_coord(alg_move: str) -> list[tuple[int, int]]:
    """Converts string coordinates into index coordinates"""
    raw_moves = alg_move.split(",")
    moves = []
    letters_to_num = {"a" : 0,
                      "b" : 1,
                      "c" : 2,
                      "d" : 3,
                      "e" : 4,
                      "f" : 5,
                      "g" : 6,
                      "h" : 7,
                      }
    
    for move in raw_moves:
        move = move.strip()

        if len(move) != 2:
            raise ValueError("Please use the correct format for the square. (See example)")
        
        else:
            if move[0] in letters_to_num:
                x = letters_to_num[move[0]]
                y = int(move[1]) - 1
                moves.append((x, y))
                             
    return moves

def print_board(game: BoardManager):
    print()
    print("type RESET as your move at any time to head back to the main menu")
    if game.to_move == Color.WHITE:
        print_white_side(game)

    else:
        print_black_side(game)

def print_white_side(game: BoardManager):
    print()
    print("      White to move     ")
    print("________________________")
    print("  a  b  c  d  e  f  g  h")
    print("  |  |  |  |  |  |  |  | ")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[j][7 - i] is None:
                line += "-- "
            else:
                line += f"{game.board[j][7 - i]} "

        print(f"{line}] - {8 - i}")

    print("________________________")

def print_black_side(game):
    print()
    print("      Black to move     ")
    print("________________________")
    print("  h  g  f  e  d  c  b  a")
    print("  |  |  |  |  |  |  |  | ")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[7 - j][i] is None:
                line += "-- "
            else:
                line += f"{game.board[7 - j][i]} "

        print(f"{line}] - {i + 1}")

    print("________________________")


if __name__ == "__main__":
    main()