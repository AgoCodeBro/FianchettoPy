import unittest
from fianchetto import BoardManager
from fianchetto.core.pieces import King, Color

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
        game = BoardManager(True)
        game.board[4][0] = King(Color.WHITE)
        game.board[4][7] = King(Color.BLACK)
        return game


if __name__ == '__main__':
    unittest.main()