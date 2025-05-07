import unittest
from fianchetto import BoardManager
from fianchetto.core.pieces import Piece, Bishop, Color

class TestBishop(unittest.TestCase):
    def test_bishop_move(self):
        game = BoardManager(True)
        self._generate_bishops(game)
        game.move((2,0), (4,2))
        game.move((2,7), (7,2))

        self.assertEqual(game.board[2][0], None)
        self.assertEqual(game.board[2][7], None)

        self.assertEqual(game.board[4][2].color, Color.WHITE)
        self.assertEqual(game.board[7][2].color, Color.BLACK)

    def test_bishop_take(self):
        game = BoardManager(True)
        self._generate_bishops(game)
        game.move((2,0), (4,2))
        game.move((5,7), (2,4))
        game.move((4,2), (2,4))

        self.assertEqual(game.board[4][2], None)
        self.assertEqual(game.board[2][4].color, Color.WHITE)

    def test_bishop_jump(self):
        game = BoardManager(True)
        self._generate_bishops(game)
        game.move((2,0), (4,2))
        game.move((5,7), (2,4))

        with self.assertRaises(ValueError):
            game.move((4,2), (1,5))



    #helper function
    def _generate_bishops(self, game: BoardManager):
        game.board[2][0] = Bishop(Color.WHITE)
        game.board[5][0] = Bishop(Color.WHITE)
        game.board[2][7] = Bishop(Color.BLACK)
        game.board[5][7] = Bishop(Color.BLACK)



if __name__ == '__main__':
    unittest.main()