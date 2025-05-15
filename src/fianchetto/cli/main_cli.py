from fianchetto.core.board_manager import BoardManager
from fianchetto.core.pieces import (Color,
                                    Pawn,
                                    Rook,
                                    Knight,
                                    Bishop,
                                    Queen,
                                    King)



def main(mode):
    print_board_modes = {0 : print_board_dark,
                         1 : print_board_light,
                         2 : print_board_text,
                         }
    
    print_board = print_board_modes[mode]
    
    game = BoardManager()
    if main_menu(game):
        keep_going = True

        while keep_going:
            if game.mate is not None:
                if game.mate == 1:
                    print()
                    print()
                    print("White Wins!")

                elif game.mate == 0:
                    print()
                    print()
                    print("Black Wins!")

                elif game.mate == 0:
                    print()
                    print()
                    print("It's a Draw!")

                else:
                    raise Exception()
                
                quit()


            print_board(game)
            alg_move = input("Please enter a move in standard algebreic notation (i.e, e4 or Nbxc6): ")

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


    main(mode)


def main_menu(game: BoardManager):
    keep_going = True
    while keep_going:
        keep_going = False
        print()
        print("________________________")
        print("Welcome to FianchettoPy!")
        ans = input("Would you like to play a local game? Y/N: ")
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

def print_board_text(game: BoardManager):
    print()
    print("type RESET as your move at any time to head back to the main menu")
    if game.to_move == Color.WHITE:
        print_white_side_text(game)

    else:
        print_black_side_text(game)

def print_white_side_text(game: BoardManager):
    print()
    print("      White to move     ")
    if game.check is not None:
        print("         Check!         ")
    print("________________________")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[j][7 - i] is None:
                line += "-- "
            else:
                line += f"{game.board[j][7 - i]} "

        print(f"{line}] - {8 - i}")
    
    print("  |  |  |  |  |  |  |  | ")
    print("  a  b  c  d  e  f  g  h")

    print("________________________")

def print_black_side_text(game):
    print()
    print("      Black to move     ")
    if game.check is not None:
        print("         Check!         ")
    print("________________________")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[7 - j][i] is None:
                line += "-- "
            else:
                line += f"{game.board[7 - j][i]} "

        print(f"{line}] - {i + 1}")

    print("  |  |  |  |  |  |  |  | ")
    print("  h  g  f  e  d  c  b  a")

    print("________________________")

def print_board_dark(game):
    print()
    print("type RESET as your move at any time to head back to the main menu")
    if game.to_move == Color.WHITE:
        print_white_side_dark(game)

    else:
        print_black_side_dark(game)

def print_white_side_dark(game: BoardManager):
    pieces = {"Pawn" : ["♟ ", "♙ "],
              "Rook" : ["♜ ", "♖ "],
              "Knight" :["♞ ", "♘ "],
              "Bishop" : ["♝ ", "♗ "],
              "Queen" : ["♛ ", "♕ "],
              "King" : ["♚ ", "♔ "],
              }

    print()
    print("      White to move     ")
    if game.check is not None:
        print("         Check!         ")
    print(" _________________________")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[j][7 - i] is None:
                line += "-- "

            else:
                piece = game.board[j][7 - i]
                if piece.color == Color.WHITE:
                    print_color = 0

                else:
                    print_color = 1
                piece_name = type(piece).__name__
                line += f"{pieces[piece_name][print_color]} "

        print(f"{line}] - {8 - i}")
    
    print("  |  |  |  |  |  |  |  |")
    print("  a  b  c  d  e  f  g  h")

    print(" _________________________")

def print_black_side_dark(game):
    pieces = {"Pawn" : ["♟ ", "♙ "],
              "Rook" : ["♜ ", "♖ "],
              "Knight" :["♞ ", "♘ "],
              "Bishop" : ["♝ ", "♗ "],
              "Queen" : ["♛ ", "♕ "],
              "King" : ["♚ ", "♔ "],
              }

    print()
    print("      Black to move     ")
    if game.check is not None:
        print("         Check!         ")
    print("________________________")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[7 - j][i] is None:
                line += "-- "
            else:
                piece = game.board[7 - j][i]
                if piece.color == Color.WHITE:
                    print_color = 0

                else:
                    print_color = 1

                piece_name = type(piece).__name__
                line += f"{pieces[piece_name][print_color]} "

        print(f"{line}] - {i + 1}")

    print("  |  |  |  |  |  |  |  | ")
    print("  h  g  f  e  d  c  b  a")

    print("________________________")


def print_board_light(game):
    print()
    print("type RESET as your move at any time to head back to the main menu")
    if game.to_move == Color.WHITE:
        print_white_side_light(game)

    else:
        print_black_side_light(game)

def print_white_side_light(game: BoardManager):
    pieces = {"Pawn" : ["♟ ", "♙ "],
              "Rook" : ["♜ ", "♖ "],
              "Knight" :["♞ ", "♘ "],
              "Bishop" : ["♝ ", "♗ "],
              "Queen" : ["♛ ", "♕ "],
              "King" : ["♚ ", "♔ "],
              }

    print()
    print("      White to move     ")
    if game.check is not None:
        print("         Check!         ")
    print("________________________")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[j][7 - i] is None:
                line += "-- "

            else:
                piece = game.board[j][7 - i]
                if piece.color == Color.WHITE:
                    print_color = 1

                else:
                    print_color = 0
                piece_name = type(piece).__name__
                line += f"{pieces[piece_name][print_color]} "

        print(f"{line}] - {8 - i}")

    print("  |  |  |  |  |  |  |  |")
    print("  a  b  c  d  e  f  g  h")
    print("________________________")

def print_black_side_light(game):
    pieces = {"Pawn" : ["♟ ", "♙ "],
              "Rook" : ["♜ ", "♖ "],
              "Knight" :["♞ ", "♘ "],
              "Bishop" : ["♝ ", "♗ "],
              "Queen" : ["♛ ", "♕ "],
              "King" : ["♚ ", "♔ "],
              }

    print()
    print("      Black to move     ")
    if game.check is not None:
        print("         Check!         ")
    print("________________________")
    for i in range(8):
        line = "[ "
        for j in range(8):
            if game.board[7 - j][i] is None:
                line += "-- "
            else:
                piece = game.board[7 - j][i]
                if piece.color == Color.WHITE:
                    print_color = 1

                else:
                    print_color = 0

                piece_name = type(piece).__name__
                line += f"{pieces[piece_name][print_color]} "

        print(f"{line}] - {i + 1}")

    print("  |  |  |  |  |  |  |  | ")
    print("  h  g  f  e  d  c  b  a")

    print("________________________")



if __name__ == "__main__":
    main()