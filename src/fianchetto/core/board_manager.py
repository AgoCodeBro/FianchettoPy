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
        white_king (tuple[int, int]): Location of white's king
        black_king (tuple[int, int]): Location of black's king
        check (Color | None): Set to the color of the side in check or to None other wise
    """
    def __init__(self, debug: bool=False):
        """Creates and instance of the board managers

        Args:
            debug (bool): Flag that allows the board to not enforce certain move rules for debugging
        """
        self.board = [[None] * 8 for _ in range(8)]
        self.to_move = Color.WHITE
        self.en_passant = False
        self.en_passant_pos = None
        self.debug = debug
        self.white_king_pos = (4,0)
        self.black_king_pos = (4,7)
        self.check = None

    def move(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """Makes a ches move on the board. If the move is not valid it will throw an error

        Args:
            start (tuple[int, int]): The coordinates of the square that the piece to be moved is on
            end (tuple[int, int]): The coordinates of the square that the piece will end up on
        """
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

                # If the king moved update its position
                if type(piece).__name__ == "King":
                    if piece.color == Color.WHITE:
                        self.white_king_pos = end

                    else:
                        self.black_king_pos = end

                # See if the player put their opponent in check.
                if piece.color == Color.WHITE:
                    opp_king = self.board[self.black_king_pos[0]][self.black_king_pos[1]]

                else:
                    opp_king = self.board[self.white_king_pos[0]][self.white_king_pos[1]]

                if opp_king is not None and opp_king.in_check(self):
                    # King might be none durring debuging
                    self.check = opp_king.color

                else:
                    self.check  = None


                self._check_en_passant(piece, start, end)

                self._check_promotion(piece, end)

                self._change_turn()
                           
            else:
                raise ValueError("Not a legal move")
            
        else: 
            raise ValueError("No piece selected")
        
    def _change_turn(self):
        """Flips whos turn it is"""
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
        
    def _check_en_passant(self, piece: Piece, start: tuple[int, int], end: tuple[int, int]) -> None:
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

    def _check_promotion(self, piece: Piece, end: tuple[int, int]) -> None:
        """Checks if a pawn has reached the end of the board"""
        if type(piece).__name__ == "Pawn" and (end[1] == 0 or end[1] == 7):
            self._promote(end)

    def _promote(self, square: tuple[int, int]) -> None:
        """Promotes a pawn to a piece of the users choice
        
        Args:
            square (tuple[int, int]): The coordinates of the square where the pawn promoted
        """
        keep_going = True
        x = square[0]
        y = square[1]
        color = self.board[x][y].color
        choice_to_piece = {1 : Queen,
                           2 : Rook,
                           3 : Bishop,
                           4 : Knight}

        while keep_going:
            print("Please select what piece to turn the pawn into by typing the corrosponding number")
            ans_str = input("1) Queen\n2) Rook\n3) Bishop\n4) Knight\n")

            try:
                ans = int(ans_str)
                if ans > 4 or ans < 1:
                    raise ValueError("Number out of range of options")

            except:
                print("Please select a valid option")
                continue

            try:
                self.board[x][y] = choice_to_piece[ans](color)

            except Exception as e:
                # All data should have been validated by this point
                raise e
            
            else:
                keep_going = False
                
    def generate_starting_position(self):
        """Adds all the pieces in their starting positions"""
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
        