import unittest
from unittest.mock import patch
from fianchetto import BoardManager
from fianchetto.core.pieces import (Pawn,
                                    Rook,
                                    Knight,
                                    Bishop,
                                    Queen,
                                    Color)

class TestPromotion(unittest.TestCase):

    @patch('builtins.input', side_effect=["7", "Test", "-2", "1"])
    def test_promotion_to_queen(self, mock_input):
        game = BoardManager(True)
        game.board[2][6] = Pawn(Color.WHITE, True)
        game.move((2,6) , (2, 7))
        piece = game.board[2][7]
        self.assertEqual(piece.color, Color.WHITE)
        self.assertEqual(type(piece).__name__, "Queen")

    @patch('builtins.input', side_effect=["7", "Test", "-2", "2"])
    def test_promotion_to_rook(self, mock_input):
        game = BoardManager(True)
        game.board[2][1] = Pawn(Color.BLACK, True)
        game.move((2,1) , (2, 0))
        piece = game.board[2][0]
        self.assertEqual(piece.color, Color.BLACK)
        self.assertEqual(type(piece).__name__, "Rook")

    @patch('builtins.input', side_effect=["7", "Test", "-2", "3"])
    def test_promotion_to_bishop(self, mock_input):
        game = BoardManager(True)
        game.board[3][6] = Pawn(Color.WHITE, True)
        game.move((3,6) , (3, 7))
        piece = game.board[3][7]
        self.assertEqual(piece.color, Color.WHITE)
        self.assertEqual(type(piece).__name__, "Bishop")

    @patch('builtins.input', side_effect=["7", "Test", "-2", "4"])
    def test_promotion_to_knight(self, mock_input):
        game = BoardManager(True)
        game.board[3][1] = Pawn(Color.BLACK, True)
        game.move((3,1) , (3, 0))
        piece = game.board[3][0]
        self.assertEqual(piece.color, Color.BLACK)
        self.assertEqual(type(piece).__name__, "Knight")
    
if __name__ == '__main__':
    unittest.main()
