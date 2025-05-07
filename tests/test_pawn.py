import unittest
from fianchetto import BoardManager
from fianchetto.core.pieces import Piece, Pawn, Color

class TestPawn(unittest.TestCase):
    def test_value(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        self.assertEqual(game.board[0][1].value, 1)

    def test_symbol(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        self.assertEqual(game.board[0][1].symbol, 'p')

    def test_move_pawn_one_square(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,2))
        game.move((6,6), (6,5))
        
        start_square = game.board[0][1]
        end_square = game.board[0][2]

        self.assertEqual(start_square, None)
        self.assertEqual(type(end_square).__name__, "Pawn")

        start_square = game.board[6][6]
        end_square = game.board[6][5]

        self.assertEqual(start_square, None)
        self.assertEqual(type(end_square).__name__, "Pawn")

    def test_move_two_squares(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,3))
        game.move((6,6), (6,4))

        start_square = game.board[0][1]
        end_square = game.board[0][3]

        self.assertEqual(start_square, None)
        self.assertEqual(type(end_square).__name__, "Pawn")

        start_square = game.board[6][6]
        end_square = game.board[6][4]

        self.assertEqual(start_square, None)
        self.assertEqual(type(end_square).__name__, "Pawn")

    def test_cant_move_two_after_first_move(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,2))
        game.move((6,6), (6,5))

        with self.assertRaises(ValueError):
            game.move((0,2), (0,4))

        with self.assertRaises(ValueError):
            game.move((6,5), (6,3))

    def test_no_jumping(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,3))
        game.move((0, 3), (0, 4))
        game.move((0, 4), (0, 5))

        game.move((6,6), (6,4))
        game.move((6,4), (6,3))
        game.move((6,3), (6,2))

        with self.assertRaises(ValueError):
            game.move((6,1), (6,3))

        with self.assertRaises(ValueError):
            game.move((0,6), (0,4))

    def test_no_fowrard_take(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((4,1), (4,3))
        game.move((4,6), (4,4))
        
        with self.assertRaises(ValueError):
            game.move((4,3), (4,4))

        with self.assertRaises(ValueError):
            game.move((4,4), (4,3))

    def test_no_forwad_2_square_take(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((4,1), (4,3))
        game.move((4,3), (4,4))
        game.move((3,6), (3,4))
        game.move((3,4), (3,3))

        with self.assertRaises(ValueError):
            game.move((4,6), (4,4))

        with self.assertRaises(ValueError):
            game.move((3,1), (3,3))

    def test_take(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((4,1), (4,3))
        game.move((3,6), (3,4))

        game.move((4,3), (3,4))

        self.assertEqual(game.board[3][4].color, Color.WHITE)
        self.assertEqual(game.board[4][3], None)

    def test_no_take_air(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,2))
        game.move((6,6), (6,5))

        with self.assertRaises(ValueError):
            game.move((0,2), (1,3))

        with self.assertRaises(ValueError):
            game.move((6,5), (7,4))

    def test_no_backwards_move(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,3))
        game.move((6,6), (6,4))

        with self.assertRaises(ValueError):
            game.move((0,3), (0,1))

        with self.assertRaises(ValueError):
            game.move((6,4), (6,6))

    def test_en_passant_white(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,1), (0,3))
        game.move((0,3), (0,4))

        game.move((1,6), (1,4))
        self.assertEqual(game.en_passant, True)
        self.assertEqual(game.en_passant_pos, (1,4))
        game.move((0,4), (1,5))

        self.assertEqual(game.board[1][5].color, Color.WHITE)
        self.assertEqual(game.board[1][4], None)
        self.assertEqual(game.en_passant, False)
        self.assertEqual(game.en_passant_pos, None)


        game.move((4,1), (4,3))
        game.move((4,3), (4,4))

        game.move((3,6), (3,4))
        self.assertEqual(game.en_passant, True)
        self.assertEqual(game.en_passant_pos, (3,4))
        game.move((4,4), (3,5))

        self.assertEqual(game.board[3][5].color, Color.WHITE)
        self.assertEqual(game.board[4][4], None)
        self.assertEqual(game.en_passant, False)
        self.assertEqual(game.en_passant_pos, None)

    def en_passant_black(self):
        game = BoardManager(True)
        self._genereate_pawns(game.board)
        game.move((0,6), (0,4))
        game.move((0,4), (0,3))

        game.move((1,1), (1,3))
        self.assertEqual(game.en_passant, True)
        self.assertEqual(game.en_passant_pos, (1,3))
        game.move((0,3), (1,2))

        self.assertEqual(game.board[1][2].color, Color.BLACK)
        self.assertEqual(game.board[1][3], None)
        self.assertEqual(game.en_passant, False)
        self.assertEqual(game.en_passant_pos, None)


        game.move((4,6), (4,4))
        game.move((4,4), (4,3))

        game.move((3,1), (3,3))
        self.assertEqual(game.en_passant, True)
        self.assertEqual(game.en_passant_pos, (3,3))
        game.move((4,3), (3,2))

        self.assertEqual(game.board[3][2].color, Color.BLACK)
        self.assertEqual(game.board[4][3], None)
        self.assertEqual(game.en_passant, False)
        self.assertEqual(game.en_passant_pos, None)

    # Helper method for testing
    def _genereate_pawns(self, board: list[list[Piece | None]]) -> None:
        for i in range(8):
            board[i][1] = Pawn(Color.WHITE)
            board[i][6] = Pawn(Color.BLACK)

if __name__ == '__main__':
    unittest.main()
