import unittest
import sys
import os
# This line makes Python find src/ directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from board_manager import BoardManager
from pieces import King, Color

class TestKing(unittest.TestCase):
    def test_king_move(self):
        game = self._generate_kings()
        game.move((4,0), (4,1))
        game.move((4,7), (3,7))

        self.assertEqual(game.board[4][0], None)
        self.assertEqual(game.board[4][7], None)
        self.assertEqual(game.board[4][1].color, Color.WHITE)
        self.assertEqual(game.board[3][7].color, Color.BLACK)


    # Helper method for tests
    def _generate_kings(self) -> BoardManager:
        game = BoardManager()
        game.board[4][0] = King(Color.WHITE)
        game.board[4][7] = King(Color.BLACK)
        return game


if __name__ == '__main__':
    unittest.main()