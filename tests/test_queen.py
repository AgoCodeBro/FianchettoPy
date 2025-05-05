import unittest
import sys
import os
# This line makes Python find src/ directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from board_manager import BoardManager
from pieces import Queen, Color

class TestQueen(unittest.TestCase):
    def test_queen_move(self):
        game = self._generate_queens()
        game.move((3,0), (3,3))
        game.move((3,7), (3,4))
        game.move((3,3), (5,5))
        game.move((3,4), (1,6))

        self.assertEqual(game.board[3][4], None)
        self.assertEqual(game.board[3][3], None)

        self.assertEqual(game.board[5][5].color, Color.WHITE)
        self.assertEqual(game.board[1][6].color, Color.BLACK)

    def test_queen_take(self):
        game = self._generate_queens()
        game.move((3,0), (3,7))

        self.assertEqual(game.board[3][2], None)
        self.assertEqual(game.board[3][7].color, Color.WHITE)

    def test_queen_jump(self):
        game = self._generate_queens()
        game.move((3,7), (3,5))

        with self.assertRaises(ValueError):
            game.move((3,0), (3,7))
        
    def test_quee_take_self(self):
        game = self._generate_queens()
        game.board[3][5] = Queen(Color.WHITE)


        with self.assertRaises(ValueError):
            game.move((3,0), (3,5))

    # Helper method for tests
    def _generate_queens(self) -> BoardManager:
        game = BoardManager()
        game.board[3][0] = Queen(Color.WHITE)
        game.board[3][7] = Queen(Color.BLACK)
        return game


if __name__ == '__main__':
    unittest.main()