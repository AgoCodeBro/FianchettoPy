from .pieces import (Color,   
                    Piece, 
                    Pawn, 
                    Bishop, 
                    Rook,
                    King,
                    Knight,
                    Queen)

class BoardManager():
    """Represents the board and controls the legal moves

    Attributes:
        board (list[list[None|pieces]]): and 8 X 8 2d list that represents the chess board (0,0) is a1 and (7,7)
            is h8. The first number is the file and the second the rank
        to_move (bool): Flag designating whos turn it is
        en_passant (bool): Flag that says if enpassant is playable this turn
        en_passant_pos (tuple[int, int] | None): Holds postion of pawn capturable with en passant or None if there 
            is no such pawn
        debug (bool): Flag to enter debug mode. Will allow play out of turn while enforcing other rules
    """
    def __init__(self, debug: bool=False):
        """Creates and instance of the board managers"""
        self.board = [[None] * 8 for _ in range(8)]
        self.to_move = Color.WHITE
        self.en_passant = False
        self.en_passant_pos = None
        self.debug = debug

    def move(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        # Check that starting square is on the board
        if start[0] < 0 or start[0] > 7 or start[1] < 0 or start[1] > 7:
            raise ValueError("This piece is off the board")
        
        piece = self.board[start[0]][start[1]]


        # Check if a piece was selected
        if piece is not None:
            legal_moves = piece.generate_valid_moves(start, self)

            # Check if piece is the correct color
            if piece.color != self.to_move and not self.debug:
                raise ValueError("The piece is the wrong color")

            # Check if the attempted move is allowed
            if end in legal_moves:
                self._free_move(start, end)
                piece.has_moved = True

                if self.en_passant:
                    # Check if En Passant was just played, if it was, remove the pawn
                    if type(piece).__name__ == "Pawn":
                        if end == (self.en_passant_pos[0], self.en_passant_pos[1] + 1) or end == (self.en_passant_pos[0], self.en_passant_pos[1] - 1):
                            self.board[self.en_passant_pos[0]][self.en_passant_pos[1]] = None

                self.check_en_passant(piece, start, end)

                self.check_promotion(piece, end)

                self._change_turn()
                           
            else:
                raise ValueError("Not a legal move")
            
        else: 
            raise ValueError("No piece selected")
        
    def _change_turn(self):
        if self.to_move == Color.WHITE:
            self.to_move = Color.BLACK

        else:
            self.to_move = Color.WHITE
        
    def _free_move(self, start, end):
        """Moves what ever piece is selected to what ever location is given as long as its on the board
        
        Useful for editing positions later on. moving and empty square onto a piece is used
        to remove a piece off the board
        
        Args:
            start (tuple[int, int]): square the piece is starting at
            end (tuple[int, int]): square the piece is headed to
        """
        # Check that starting square is on the board
        if start[0] < 0 or start[0] > 7 or start[1] < 0 or start[1] > 7:
            raise ValueError("This piece is off the board")
        
        # Check that end square is on the board
        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7:
            raise ValueError("This square is off the board")
        
        self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
        self.board[start[0]][start[1]] = None
        
    def check_en_passant(self, piece: Piece, start: tuple[int, int], end: tuple[int, int]) -> None:
        """Checks if en passant is playable on the board next move and sets self.en_passant, and self.en_passant_pos to the correct values

        Args:
            piece (Piece): piece that was just moved
            start (tuple[int, int]): Square the piece started on
            end (tuple[int, int]): Square the piece ended on
        """
        if type(piece).__name__ == "Pawn":
            if start[1] - end[1] == 2 or start[1] - end[1] == -2:
                if end[0] + 1 <= 7:
                    square_to_the_right = self.board[end[0] + 1][end[1]]

                    if type(square_to_the_right).__name__ == "Pawn" and square_to_the_right.color != piece.color:
                        self.en_passant = True
                        self.en_passant_pos = end
                        return

                if end[0] - 1 >= 0:
                    square_to_the_left = self.board[end[0] - 1][end[1]]

                    if type(square_to_the_left).__name__ == "Pawn" and square_to_the_left.color != piece.color:
                        self.en_passant = True
                        self.en_passant_pos = end
                        return
                    
        self.en_passant = False
        self.en_passant_pos = None

    def check_promotion(self, piece: Piece, end: tuple[int, int]) -> None:
        if type(piece).__name__ == "Pawn" and (end[1] == 0 or end[1] == 1):
            print("this pawn should promote")

    def generate_starting_position(self):
        # Add Pawns
        for i in range(8):
            self.board[i][1] = Pawn(Color.WHITE)
            self.board[i][6] = Pawn(Color.BLACK)

        # Add Rooks
        self.board[0][0] = Rook(Color.WHITE)
        self.board[7][0] = Rook(Color.WHITE)
        self.board[0][7] = Rook(Color.BLACK)
        self.board[7][7] = Rook(Color.BLACK)

        # Add Knights
        self.board[1][0] = Knight(Color.WHITE)
        self.board[6][0] = Knight(Color.WHITE)
        self.board[1][7] = Knight(Color.BLACK)
        self.board[6][7] = Knight(Color.BLACK)

        # Add Bishops 
        self.board[2][0] = Bishop(Color.WHITE)
        self.board[5][0] = Bishop(Color.WHITE)
        self.board[2][7] = Bishop(Color.BLACK)
        self.board[5][7] = Bishop(Color.BLACK) 

        # Add Queens
        self.board[3][0] = Queen(Color.WHITE)
        self.board[3][7] = Queen(Color.BLACK)

        # Add Kings
        self.board[4][0] = King(Color.WHITE)
        self.board[4][7] = King(Color.BLACK)
        