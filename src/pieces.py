from enum import Enum
from abc import ABC, abstractmethod

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

    def generate_valid_moves(self,position: tuple[int, int], game: 'BoardManager') -> list[tuple[int, int]]:
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

        # Validate positon is on the board
        for i in position:
            if i > 7 or i < 0:
                raise ValueError("Piece's position is off of the board")
        
        if position[1] == 7 or position[1] == 0:
            raise ValueError("Pawns cant be at the end of the board. Promotion did not occur")
            
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

  
