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
    def generate_valid_moves(self, board: BoardManager) -> list:
        """returns a list of all the valid moves the piece can make"""
        pass

    @property
    @abstractmethod
    def symbol(self) -> str:
        """Returns the symbol that represents the piece"""
        pass


class Pawn(Piece):
    """Class representing a pawn"""

    def __init__(self, color: Color) -> None:
        """Creates an instance of a Pawn of the given color
        """
        super().__init__(color)


