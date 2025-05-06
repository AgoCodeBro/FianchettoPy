from board_manager import BoardManager
from pieces import Color



def main():
    game = BoardManager()
    if main_menu(game):
        keep_going = True

        while keep_going:
            game.printBoard()
            alg_move = input("Please enter a move by entering the starting and ending coordinates seprataed by commas (Ex: g1, f3): ")

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




    else:
        return


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
            return False
        
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



if __name__ == "__main__":
    main()