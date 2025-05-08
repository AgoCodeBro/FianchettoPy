from enum import Enum
from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board_manager import BoardManager

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
    def generate_valid_moves(self, position: tuple[int,int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

        Return:
            list of coordinates where the piece can end up
        """
        pass

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

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

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

            next_square = game.board[position[0]][position[1] + (move_direction * 2)]

            if next_square is None and not self.has_moved:
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

        return moves

  
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

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

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

        return moves

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

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

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

        return moves
    
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

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        moves.extend(Rook.generate_valid_moves(self, position, game))
        moves.extend(Bishop.generate_valid_moves(self, position, game))

        return moves
    

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

    def generate_valid_moves(self, position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
        """Returns a list of all the valid moves the piece can make

        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            game (BoardManager): A representation of the board itself.

        Return:
            list of coordinates where the piece can end up
        """
        moves = []
        choices = [(1, 2), (1 ,-2), (2, 1), (2, -1), (-1, 2), (-1 ,-2), (-2, 1), (-2, -1)]

        for choice in choices:
            if self.is_on_board(position, choice):
                if game.board[position[0] + choice[0]][position[1] + choice[1]] == None:
                    moves.append((position[0] + choice[0], position[1] + choice[1]))

                elif game.board[position[0] + choice[0]][position[1] + choice[1]].color != self.color:
                    moves.append((position[0] + choice[0], position[1] + choice[1]))

        return moves


    def is_on_board(self, position: tuple[int, int], choice: tuple[int, int]) -> bool:
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

        return moves