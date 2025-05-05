import unittest
import sys
import os
# This line makes Python find src/ directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from board_manager import BoardManager
from pieces import Piece, Rook, Color

class TestPawn(unittest.TestCase):
    
    def test_rook_move(self):
        game = BoardManager()
        self._generate_rooks(game)

        game.move((0, 0), (0, 4))
        self.assertEqual(game.board[0][0], None)
        self.assertEqual(game.board[0][4].color, Color.WHITE)

        game.move((0,7), (4,7))
        self.assertEqual(game.board[0][7], None)
        self.assertEqual(game.board[4][7].color, Color.BLACK)

        with self.assertRaises(ValueError):
            game.move((0, 4), (5,6))

    def test_rook_take(self):
        game = BoardManager()
        self._generate_rooks(game)

        game.move((0, 0), (0, 7))
        self.assertEqual(game.board[0][0], None)
        self.assertEqual(game.board[0][7].color, Color.WHITE)
        self.assertEqual(game.board[7][7].color, Color.BLACK)
        game.move((0, 7), (7, 7))
        self.assertEqual(game.board[7][7].color, Color.WHITE)

    def test_rook_take_self(self):
        game = BoardManager()
        self._generate_rooks(game)

        with self.assertRaises(ValueError):
            game.move((0,0), (7,0))

    def test_rook_cant_jump_self(self):
        game = BoardManager()
        self._generate_rooks(game)

        game.move((7,0), (5,0))

        with self.assertRaises(ValueError):
            game.move((0,0), (7,0))

    def test_rook_cant_jump_opp(self):
        game = BoardManager()
        self._generate_rooks(game)

        game.move((7,7), (5,7))
        game.move((5, 7), (5,0))

        with self.assertRaises(ValueError):
            game.move((0,0), (6,0))

    #helper method
    def _generate_rooks(self, game: BoardManager) -> None:
        game.board[0][0] = Rook(Color.WHITE)
        game.board[7][0] = Rook(Color.WHITE)
        game.board[0][7] = Rook(Color.BLACK)
        game.board[7][7] = Rook(Color.BLACK)


if __name__ == '__main__':
    unittest.main()
