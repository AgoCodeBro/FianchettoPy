import unittest
import sys
import os
# This line makes Python find src/ directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from board_manager import BoardManager
from pieces import Knight, Color

class TestKnight(unittest.TestCase):
    def test_kinight_move(self):
        game = self._generate_knights()
        game.move((6,0), (5,2))
        game.move((6,7), (5,5))
        
        self.assertEqual(game.board[6][0], None)
        self.assertEqual(game.board[6][7], None)
        self.assertEqual(game.board[5][2].color, Color.WHITE)
        self.assertEqual(game.board[5][5].color, Color.BLACK)

    def test_knight_take(self):
        game = self._generate_knights()
        game.move((6,0), (5,2))
        game.move((6,7), (5,5))
        game.move((1, 0), (2,2))
        game.move((1,7), (2,5))
        game.move((5,2), (3,3))
        game.move((5,5), (4,3))
        game.move((2,2), (4,3))
        game.move((2,5), (3,3))
        
        self.assertEqual(game.board[2][2], None)
        self.assertEqual(game.board[2][5], None)
        self.assertEqual(game.board[4][3].color, Color.WHITE)
        self.assertEqual(game.board[3][3].color, Color.BLACK)

    def test_knight_off_board(self):
        game = self._generate_knights()

        with self.assertRaises(ValueError):
            game.move((1,0), (-1,1))

    # Helper method for tests
    def _generate_knights(self) -> BoardManager:
        game = BoardManager()
        game.board[1][0] = Knight(Color.WHITE)
        game.board[1][7] = Knight(Color.BLACK)
        game.board[6][0] = Knight(Color.WHITE)
        game.board[6][7] = Knight(Color.BLACK)
        return game


if __name__ == '__main__':
    unittest.main()