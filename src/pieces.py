from enum import Enum
from board_manager import BoardManager
from abc import ABC, abstractmethod

class Color(Enum):
    """An enum to for each type of piece"""
    WHITE = 'W'
    BLACK = 'B'



class Piece(ABC):
    """Abstract class to for each of the piece type to inherit from

    Attributes:
        color (Color): Tracks what color a piece is
        symbol (str): Symbol that represents the piece type
    """

    def __init__(self, color: Color) -> None:
        """Initializes piece with the given color

        Args:
            color (Color): The color of the piece
        """
        self.color = color

    @abstractmethod
    def generate_valid_moves(self, position: tuple[int,int], board: list[list['Piece' | None]], en_passant: bool = False) -> list[tuple[int, int]]:
        """returns a list of all the valid moves the piece can make
        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            board (list[list['Piece' | None]]): A representation of the board itself.
            en_passant (bool): Flag that says if there is en_passant possible on this move
        """
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Returns the symbol that represents the piece"""
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        """Returns the value of the piece"""
        pass

    def __repr__(self):
        return f"{self.color.value}{self.symbol}"


class Pawn(Piece):
    """Class representing a pawn"""

    def __init__(self, color: Color) -> None:
        """Creates an instance of a Pawn of the given color

        Args:
            color (Color):
        """
        super().__init__(color)
        self.has_moved = False
        self._symbol = 'p'
        self._value = 1

    def generate_valid_moves(self,
                             position: tuple[int, int],
                             board: list[list['Piece' | None]],
                             en_passant: bool = False,
                             en_passant_pos: tuple[int,int] | None = None
                             ) -> list:
        """Generates a list of all the valid moves this piece can make
        Args:
            position (tuple[int, int]): A tuple contating 2 ints that give where on the board this piece is.
            board (list[list['Piece' | None]]): A representation of the board itself.
            en_passant (bool): Flag that says if there is en_passant possible on this move
            en_passant_pos (tuple[int,int] | None): Holds the square of the pawn available for enpassant and None if there is no enpassant
        """
        if self.color == Color.WHITE:
            move_direction = 1

        else:
            move_direction = -1

        # Validate positon is on the board
        for i in position:
            if i > 7 or i < 0:
                raise ValueError("Piece's position is off of the board")
            
            elif i == 7 or i == 0:
                raise ValueError("Pawns cant be at the end of the board. Promotion did not occur")
            
        # Check forward movement
        moves = []
        next_square = board[position[0]][position[1] + move_direction]

        if next_square is None:
            moves.append((position[0], position[1] + move_direction))

            next_square = board[position[0]][position[1] + (move_direction * 2)]

            if next_square is None and not self.has_moved:
                moves.append((position[0], position[1] + (move_direction * 2)))

        # Check takes
        if position[0] + 1  <= 7:
            next_square = board[position[0] + 1][position[1] + move_direction]

            if next_square is not None and next_square.color != self.color:
                moves.append((position[0] + 1, position[1] + move_direction))

        if position[0] - 1  <= 7:
            next_square = board[position[0] - 1][position[1] + move_direction]

            if next_square is not None and next_square.color != self.color:
                moves.append((position[0] - 1, position[1] + move_direction))

        # Check en_passant
        if en_passant:
            if en_passant_pos[0] + 1 == position[0] or en_passant_pos[0] - 1 == position[0]:
                if en_passant_pos[1] == position[1]:
                    moves.append((en_passant_pos[0], en_passant_pos[1] + move_direction))


        return moves



