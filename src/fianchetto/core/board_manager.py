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
        mate (int | None): set to 1 if white won, -1 if black won, 0 if a stale mate, and None if there are still moves
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
        self.mate = None

    def move(self, move: str) -> None:
        """Makes a chess move on the board. If the move is not valid it will throw an error

        Args:
            start (tuple[int, int]): The coordinates of the square that the piece to be moved is on
            end (tuple[int, int]): The coordinates of the square that the piece will end up on
        """
        letters_to_num = {"a" : 0,
                        "b" : 1,
                        "c" : 2,
                        "d" : 3,
                        "e" : 4,
                        "f" : 5,
                        "g" : 6,
                        "h" : 7,
                        }
        
        # Check if its a pawn move (not a take)
        if len(move) == 2:
            try:
                x = letters_to_num[move[0]]
                y = int(move[1])

            except:
                raise ValueError("Please enter a vaild mpve")
            
            self._check_pawn_move(x, y)

        
        if len(move) == 3:
            # If its a take, its a pawn take
            if 'x' in move:
                try:
                    x = letters_to_num[move[0]]
                    y = int(move[1])

                except:
                    raise ValueError("Please enter a vaild mpve")
                
                

    def _check_pawn_move(self, x, y):
        if self.to_move == Color.WHITE:
            direction = 1
        else:
            direction = - 1
        if self.board[x][y - direction] is not None and self.board[x][y - direction].color == self.to_move:
            self.board[x][y - direction].generate_valid_moves()

        elif self.board[x][y - direction * 2] is not None and self.board[x][y - direction * 2].color == self.to_move:
            self.board[x][y - direction * 2].generate_valid_moves()


        


    def _check_for_mates(self) -> None:
        """Checks to see if there is either checkmate or stalemate on the board and sets the mate attribute accordingly"""
        for i in range(8):
            for j in range(8):
                square = self.board[i][j]
                if square is not None and len(square.generate_valid_moves((i, j), self)) != 0:
                    if square.color != self.to_move:
                        return
                
        if self.check is None:
            self.mate = 0
        
        elif self.check == Color.WHITE:
            self.mate = -1

        elif self.check == Color.BLACK:
            self.mate = 1

        else:
            raise Exception("Something went wrong")
            
        
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
        