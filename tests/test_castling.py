import unittest
from fianchetto import BoardManager
from fianchetto.core.pieces import King, Rook, Color, Pawn

class TestCastling(unittest.TestCase):

    def test_castle_short(self):
        game = BoardManager()
        game.board[5][1] = Pawn(Color.WHITE)
        game.board[4][0] = King(Color.WHITE)
        game.board[7][0] = Rook(Color.WHITE)
        game.board[4][7] = King(Color.BLACK)
        game.board[7][7] = Rook(Color.BLACK)

        game.move((4, 0), (6, 0))
        game.move((4, 7), (6, 7))

        white_king = game.board[6][0]
        white_rook = game.board[5][0]
        black_king = game.board[6][7]
        black_rook = game.board[5][7]

        self.assertEqual(type(white_king).__name__, "King")
        self.assertEqual(type(white_rook).__name__, "Rook")
        self.assertEqual(type(black_king).__name__, "King")
        self.assertEqual(type(black_rook).__name__, "Rook")

    def test_castle_long(self):
        game = BoardManager()
        game.board[3][1] = Pawn(Color.WHITE)
        game.board[4][0] = King(Color.WHITE)
        game.board[0][0] = Rook(Color.WHITE)
        game.board[4][7] = King(Color.BLACK)
        game.board[0][7] = Rook(Color.BLACK)

        game.move((4, 0), (2, 0))
        game.move((4, 7), (2, 7))

        white_king = game.board[2][0]
        white_rook = game.board[3][0]
        black_king = game.board[2][7]
        black_rook = game.board[3][7]

        self.assertEqual(type(white_king).__name__, "King")
        self.assertEqual(type(white_rook).__name__, "Rook")
        self.assertEqual(type(black_king).__name__, "King")
        self.assertEqual(type(black_rook).__name__, "Rook")

    def test_blocked_path(self):
        game = BoardManager()
        game.generate_starting_position()

        with self.assertRaises(ValueError):
            game.move((4, 0), (6, 0))
        
    def test_cross_check(self):
        game = BoardManager()
        game.board[4][0] = King(Color.WHITE)
        game.board[7][0] = Rook(Color.WHITE)
        game.board[5][3] = Rook(Color.BLACK)

        with self.assertRaises(ValueError):
            game.move((4, 0), (6, 0))

    def test_in_check(self):
        game = BoardManager()
        game.board[4][0] = King(Color.WHITE)
        game.board[7][0] = Rook(Color.WHITE)
        game.board[4][3] = Rook(Color.BLACK)

        with self.assertRaises(ValueError):
            game.move((4, 0), (6, 0))

if __name__ == '__main__':
    unittest.main()