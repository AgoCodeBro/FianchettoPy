from enum import Enum
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fianchetto import BoardManager

class Color(Enum):
    """An enum to for each type of piece"""
    WHITE = 'W'
    BLACK = 'B'



class Piece(ABC):
    """Abstract class to for each of the piece type to inherit from

    Attributes:
        color (Color): Tracks what color a piece is
        _symbol (str): Symbol that represents the piece type
        _value (int): Integer representing point value of the piece
        has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool) -> None:
        """Initializes piece with the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        self.color = color
        self.has_moved = has_moved

    @abstractmethod
    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager', checks: bool = False) -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.
            checks (bool): Is true if it is being used to look for checks and not make a move

        Return:
            list of coordinates where the piece can end up
        """
        pass

    def _remove_checks(self, position: tuple[int, int], moves: list[tuple[int, int]], game: 'BoardManager') -> list[tuple[int, int]]:
        """Helper function to generate valid moves that removes all moves that put yourself in check

        Args:
            position (tuple[int, int]): Current position of piece being moved
            moves (list[tuple[int, int]]): List of posible moves the piece can make
            game (BoardManager): Representation of the board itself
        """
        pos_x = position[0]
        pos_y = position[1]
        piece = game.board[pos_x][pos_y]
        result = []

        # Select the correct king
        if piece.color == Color.WHITE:
            king_pos = game.white_king_pos
    
        else:
            king_pos = game.black_king_pos

        king = game.board[king_pos[0]][king_pos[1]]

        for move in moves:
            #If its a king move, update the kings position
            if type(piece).__name__ == "King":
                if piece.color == Color.WHITE:
                    game.white_king_pos = move
            
                else:
                    game.black_king_pos = move

            # Create a temp to hold what was on the destination square
            temp = game.board[move[0]][move[1]]
            game._free_move(position, move)

            if king is None or not king.in_check(game):
                # King might be none durring debuging
                result.append(move)

            # Reset king position
            if type(piece).__name__ == "King":
                if piece.color == Color.WHITE:
                    game.white_king_pos = (pos_x, pos_y)
            
                else:
                    game.black_king_pos = (pos_x, pos_y)
            
            game._free_move(move, position)
            game.board[move[0]][move[1]] = temp
            
        
        return result

    @property
    def symbol(self) -> str:
        """Returns the symbol that represents the piece"""
        return self._symbol

    @property
    def value(self) -> int:
        """Returns the value of the piece"""
        return self._value

    def __repr__(self):
        return f"{self.color.value}{self.symbol}"



class Pawn(Piece):
    """Class representing a pawn

    Attributes:
        color (Color): Tracks what color a piece is
        _symbol (str): Symbol that represents the piece type
        _value (int): Integer representing point value of the piece
        has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool = False) -> None:
        """Creates an instance of a Pawn of the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        super().__init__(color, has_moved)
        self._symbol = 'p'
        self._value = 1

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager', checks: bool = False) -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.
            checks (bool): Is true if it is being used to look for checks and not make a move

        Return:
            list of coordinates where the piece can end up
        """
        if self.color == Color.WHITE:
            move_direction = 1

        else:
            move_direction = -1
            
        # Check forward movement
        moves = []
        next_square = game.board[position[0]][position[1] + move_direction]

        if next_square is None:
            moves.append((position[0], position[1] + move_direction))

            if not self.has_moved:

                next_square = game.board[position[0]][position[1] + (move_direction * 2)]

                if next_square is None:
                    moves.append((position[0], position[1] + (move_direction * 2)))

        # Check takes
        if position[0] + 1  <= 7:
            next_square = game.board[position[0] + 1][position[1] + move_direction]

            if next_square is not None and next_square.color != self.color:
                moves.append((position[0] + 1, position[1] + move_direction))

        if position[0] - 1  <= 7:
            next_square = game.board[position[0] - 1][position[1] + move_direction]

            if next_square is not None and next_square.color != self.color:
                moves.append((position[0] - 1, position[1] + move_direction))

        # Check en_passant
        if game.en_passant:
            if game.en_passant_pos[0] + 1 == position[0] or game.en_passant_pos[0] - 1 == position[0]:
                if game.en_passant_pos[1] == position[1]:
                    moves.append((game.en_passant_pos[0], game.en_passant_pos[1] + move_direction))

                # If we are looking for checks, dont try to look for checks again
        if checks:
            return moves

        return self._remove_checks(position, moves, game)

  
class Rook(Piece):
    """Class representing a rook

        Attributes:
            color (Color): Tracks what color a piece is
            _symbol (str): Symbol that represents the piece type
            _value (int): Integer representing point value of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool = False) -> None:
        """Creates an instance of a bishop of the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        super().__init__(color, has_moved)
        self._symbol = 'R'
        self._value = 5

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager', checks: bool = False) -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.
            checks (bool): Is true if it is being used to look for checks and not make a move

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        x = position[0]
        y = position[1]

        check_up = True
        check_down = True
        check_left = True
        check_right = True
        dist = 1

        while check_up or check_down or check_left or check_right:
            if check_up:
                if (y + dist) <= 7 and game.board[x][y + dist] is not None:
                    check_up = False
                    if game.board[x][y + dist].color != self.color:
                        moves.append((x, y + dist))
                
                elif (y + dist) <= 7 and game.board[x][y + dist] is None:
                    moves.append((x, y + dist))

                else:
                    check_up = False

            if check_down:
                if (y - dist) >= 0 and game.board[x][y - dist] is not None:
                    check_down = False
                    if game.board[x][y - dist].color != self.color:
                        moves.append((x, y - dist))
                
                elif (y - dist) >= 0 and game.board[x][y - dist] is None:
                    moves.append((x, y - dist))

                else:
                    check_down = False

            if check_right:
                if (x + dist) <= 7 and game.board[x + dist][y] is not None:
                    check_right = False
                    if game.board[x + dist][y].color != self.color:
                        moves.append((x + dist, y))
                
                elif (x + dist) <= 7 and game.board[x + dist][y] is None:
                    moves.append((x + dist, y))

                else:
                    check_right = False

            if check_left:
                if (x - dist) >= 0 and game.board[x - dist][y] is not None:
                    check_left = False
                    if game.board[x - dist][y].color != self.color:
                        moves.append((x + dist, y))
                
                elif (x - dist) >= 0 and game.board[x - dist][y] is None:
                    moves.append((x - dist, y))

                else:
                    check_left = False

            dist += 1

        # If we are looking for checks, dont try to look for checks again
        if checks:
            return moves
        
        return self._remove_checks(position, moves, game)

class Bishop(Piece):
    """Class representing a bishop

    Attributes:
        color (Color): Tracks what color a piece is
        _symbol (str): Symbol that represents the piece type
        _value (int): Integer representing point value of the piece
        has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool = False) -> None:
        """Creates an instance of a bishiop of the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        super().__init__(color, has_moved)
        self._symbol = 'B'
        self._value = 3

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager', checks: bool = False) -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.
            checks (bool): Is true if it is being used to look for checks and not make a move

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        x = position[0]
        y = position[1]

        check_up_right = True
        check_down_right = True
        check_up_left = True
        check_down_left = True
        dist = 1

        while check_up_right or check_down_right or check_up_left or check_down_left:
            if check_up_right:
                if (y + dist) > 7:
                    check_up_right = False
                    check_up_left = False

                elif (x + dist) > 7:
                    check_up_right = False
                    check_down_right = False
                
                else:
                    if game.board[x + dist][y + dist] is None:
                        moves.append((x + dist, y + dist))

                    else:
                        if game.board[x + dist][y + dist].color != self.color:
                            moves.append((x + dist, y + dist))

                        check_up_right = False

            if check_up_left:
                if (y + dist) > 7:
                    check_up_right = False
                    check_up_left = False

                elif (x - dist) < 0:
                    check_up_left = False
                    check_down_left = False
                
                else:
                    if game.board[x - dist][y + dist] is None:
                        moves.append((x - dist, y + dist))

                    else:
                        if game.board[x - dist][y + dist].color != self.color:
                            moves.append((x - dist, y + dist))
                            
                        check_up_left = False

            if check_down_left:
                if (y - dist) < 0:
                    check_down_right = False
                    check_down_left = False

                elif (x - dist) < 0:
                    check_up_left = False
                    check_down_left = False
                
                else:
                    if game.board[x - dist][y - dist] is None:
                        moves.append((x - dist, y - dist))

                    else:
                        if game.board[x - dist][y - dist].color != self.color:
                            moves.append((x - dist, y - dist))
                            
                        check_down_left = False

            if check_down_right:
                if (y - dist) < 0:
                    check_down_right = False
                    check_down_left = False

                elif (x + dist) > 7:
                    check_up_right = False
                    check_down_right = False
                
                else:
                    if game.board[x + dist][y - dist] is None:
                        moves.append((x + dist, y - dist))

                    else:
                        if game.board[x + dist][y - dist].color != self.color:
                            moves.append((x + dist, y - dist))
                            
                        check_down_right = False

            dist += 1

        # If we are looking for checks, dont try to look for checks again
        if checks:
            return moves
        
        return self._remove_checks(position, moves, game)
    
class Queen(Rook, Bishop):
    """Class representing a queen

    Attributes:
        color (Color): Tracks what color a piece is
        _symbol (str): Symbol that represents the piece type
        _value (int): Integer representing point value of the piece
        has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool = False) -> None:
        """Creates an instance of a queen of the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        super().__init__(color, has_moved)
        self._symbol = 'Q'
        self._value = 9

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager', checks: bool = False) -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.
            checks (bool): Is true if it is being used to look for checks and not make a move

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        moves.extend(Rook.generate_valid_moves(self, position, game, checks))
        moves.extend(Bishop.generate_valid_moves(self, position, game, checks))

        # If we are looking for checks, dont try to look for checks again
        if checks:
            return moves
        
        return self._remove_checks(position, moves, game)
    

class Knight(Piece):
    """Class representing a knight

    Attributes:
        color (Color): Tracks what color a piece is
        _symbol (str): Symbol that represents the piece type
        _value (int): Integer representing point value of the piece
        has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool = False) -> None:
        """Creates an instance of a knight of the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        super().__init__(color, has_moved)
        self._symbol = 'N'
        self._value = 3

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager', checks:bool = False) -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.
            checks (bool): Is true if it is being used to look for checks and not make a move

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        choices = [(1, 2), (1 ,-2), (2, 1), (2, -1), (-1, 2), (-1 ,-2), (-2, 1), (-2, -1)]

        for choice in choices:
            if self._is_on_board(position, choice):
                if game.board[position[0] + choice[0]][position[1] + choice[1]] == None:
                    moves.append((position[0] + choice[0], position[1] + choice[1]))

                elif game.board[position[0] + choice[0]][position[1] + choice[1]].color != self.color:
                    moves.append((position[0] + choice[0], position[1] + choice[1]))

        # If we are looking for checks, dont try to look for checks again
        if checks:
            return moves
        
        return self._remove_checks(position, moves, game)


    def _is_on_board(self, position: tuple[int, int], choice: tuple[int, int]) -> bool:
        """Checks if moving from the current position to the choice ends up on the board

        Args:
            position (tuple[int, int]): Holds the current position of the knight
            choice (tuple[int, int]): Holds the direction we are trying to move

        Returns: flag indicating if knight would end up on the board or not
        """
        if (position[0] + choice[0]) > 7 or (position[0] + choice[0]) < 0:
            return False
        
        elif (position[1] + choice[1]) > 7 or (position[1] + choice[1]) < 0:
            return False
        
        else:
            return True
        

class King(Piece):
    """Class representing a king

    Attributes:
        color (Color): Tracks what color a piece is
        _symbol (str): Symbol that represents the piece type
        _value (int): Integer representing point value of the piece
        has_moved (bool): Flag that says if this piece has moved from its starting square
    """

    def __init__(self, color: Color, has_moved: bool = False) -> None:
        """Creates an instance of a king of the given color

        Args:
            color (Color): The color of the piece
            has_moved (bool): Flag that says if this piece has moved from its starting square, Defaults to false
        """
        super().__init__(color, has_moved)
        self._symbol = 'K'
        self._value = None

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        choices = [0, 1, -1]
        x = position[0]
        y = position[1]

        for i in choices:
            for j in choices:
                if x + i >= 0 and y + j >= 0 and x + i <= 7 and y + j <= 7:
                    if game.board[x + i][y + j] is None or game.board[x + i][y + j].color != self.color:
                        moves.append((x + i, y + j))

        moves.extend(self.castling(game))

        return self._remove_checks(position, moves, game)
    
    def castling(self, game: 'BoardManager') -> list[tuple[int, int]]:
        moves = []
        # Ensure king is not in check and hasnt moved
        if self.has_moved or self.in_check(game):
            return moves

        # Select correct side of the board
        if self.color == Color.WHITE:
            pos = game.white_king_pos
            y = 0

        else:
            pos = game.black_king_pos
            y = 7

        # Check kingside rook
        if game.board[7][y] is not None and not game.board[7][y].has_moved:
            # Check path is clear
            is_clear = True
            for i in range(5,7):
                if game.board[i][y] is not None:
                    is_clear = False
                    break
            
            if is_clear:
                # Check if crossing check
                path = self._remove_checks(pos,[(5, y)], game)

                if len(path) == 1:
                    moves.append((6, y))

        # Check queenside rook
        if game.board[0][y] is not None and not game.board[0][y].has_moved:
            # Check path is clear
            is_clear = True
            for i in range(1,4):
                if game.board[i][y] is not None:
                    is_clear = False
                    break
            
            if is_clear:
                # Check if crossing check
                path = self._remove_checks(pos,[(3, y)], game)

                if len(path) == 1:
                    moves.append((2, y))

        return moves

    
    def in_check(self, game: 'BoardManager') -> bool:
        """Returns if true if in check and false otherwise"""    
        if self.color == Color.WHITE:
            x = game.white_king_pos[0]
            y = game.white_king_pos[1]
        
        
        else:
            x = game.black_king_pos[0]
            y = game.black_king_pos[1]

        # Pawn checks
        pawn = Pawn(self.color)
        vision = pawn.generate_valid_moves((x, y), game, True)
        if self._check_vision(vision, game, [type(pawn)]):
            return True
                
        # Knight checks
        knight = Knight(self.color)
        vision = knight.generate_valid_moves((x, y), game, True)
        if self._check_vision(vision, game, [type(knight)]):
            return True
        
        # Queen and Rook checks
        rook = Rook(self.color)
        queen = Queen(self.color)
        vision = rook.generate_valid_moves((x, y), game, True)
        if self._check_vision(vision, game, [type(queen), type(rook)]):
            return True
        
        # Queen and Bishiop checks
        bishop = Bishop(self.color)
        queen = Queen(self.color)
        vision = bishop.generate_valid_moves((x, y), game, True)
        if self._check_vision(vision, game, [type(queen), type(bishop)]):
            return True
        
        return False

    def _check_vision(self, vision: list[tuple[int, int]], game: 'BoardManager', piece_names: list[str]) -> bool:
        """Checks squares in vision to see if an opposing piece is checking the king

        Args:
            vision (list[tuple[int, int]]): A list of coordinates containing square that have line of sight on the king
            game (BoardManager): Representation of the board
            piece_names (list[str]): A list of the names of the pieces that could check the king from these squares

        Return:
            Returns true if any of the squares in vision contains an enemy piece whos name is in piece_names and false otherwise
        """
        for square in vision:
            potential_threat = game.board[square[0]][square[1]]
            if potential_threat is not None and potential_threat.color != self.color:
                if type(potential_threat) in piece_names:
                    return True
                
        return False