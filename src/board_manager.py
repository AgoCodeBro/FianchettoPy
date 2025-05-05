from pieces import Color, Piece
class BoardManager():
    """Represents the board and controls the legal moves

    Attributes:
        board (list[list[None|pieces]]): and 8 X 8 2d list that represents the chess board (0,0) is a1 and (7,7)
            is h8. The first number is the file and the second the rank
        to_move (bool): Flag designating whos turn it is
        en_passant (bool): Flag that says if enpassant is playable this turn
        en_passant_pos (tuple[int, int] | None): Holds postion of pawn capturable with en passant or None if there 
            is no such pawn
    """

    def __init__(self):
        """Creates and instance of the board managers"""
        self.board = [[None] * 8 for _ in range(8)]
        self.to_move = Color.WHITE
        self.en_passant = False
        self.en_passant_pos = None

    def move(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        piece = self.board[start[0]][start[1]]

        if piece is not None:
            legal_moves = piece.generate_valid_moves(start, self.board, self.en_passant, self.en_passant_pos)

            if end in legal_moves:
                self.board[end[0]][end[1]] = piece
                self.board[start[0]][start[1]] = None

                self.check_en_passant(piece, start, end)

                self.check_promotion(piece, end)
                          
            
            else:
                raise ValueError("Not a legal move")
            
        else: 
            raise ValueError("No piece selected")
        
    def check_en_passant(self, piece: Piece, start: tuple[int, int], end: tuple[int, int]) -> None:
        """Checks if en passant is playable on the board next move and sets self.en_passant, and self.en_passant_pos to the correct values

        Args:
            piece (Piece): piece that was just moved
            start (tuple[int, int]): Square the piece started on
            end (tuple[int, int]): Square the piece ended on
        """
        if type(piece).__Name__ == "Pawn":
            if start[1] - end[1] == 2 or start[1] - end[1] == -2:
                if end[0] + 1 <= 7:
                    square_to_the_right = self.board[end[0] + 1][end[1]]

                    if type(square_to_the_right).__Name__ == "Pawn" and square_to_the_right.color != piece.color:
                        en_passant = True
                        en_passant_pos = end
                        return

                if end[0] - 1 >= 0:
                    square_to_the_left = self.board[end[0] - 1][end[1]]

                    if type(square_to_the_left).__Name__ == "Pawn" and square_to_the_left.color != piece.color:
                        en_passant = True
                        en_passant_pos = end
                        return
                    
        en_passant = False
        en_passant_pos = None

    def check_promotion(self, piece: Piece, end: tuple[int, int]) -> None:
        if type(piece).__Name__ == "Pawn" and (end[1] == 0 or end[1] == 1):
            print("this pawn should promote")
        