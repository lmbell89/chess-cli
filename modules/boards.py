import re

from modules.pieces import Pawn, Knight, Bishop, Rook, Queen, King

class Board:
    current_player = 'white'
    ghost_pawn = None
    half_moves = 0
    turn = 0
    castling_bk = False
    castling_bq = False
    castling_wk = False
    castling_wq = False
    king_location = None

    types = {
        Pawn: 'p', 
        Knight: 'n',
        Bishop: 'b', 
        Rook: 'r', 
        Queen: 'q', 
        King: 'k',
        'p': Pawn, 
        'n': Knight, 
        'b': Bishop, 
        'r': Rook, 
        'q': Queen, 
        'k': King
        }

    square_list = [
        'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8',
        'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
        'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
        'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
        'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
        'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
        'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
        'a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1'
        ]

    def __init__(self, fen=None):
        """
        Initializes a Board object. 
        If a FEN string is not provided, the starting position is used.

        Parameters:
            fen (str): A FEN string representing a chess position (optional)
        """
        self.squares = {}
        if fen is None:
            self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        else:
            self.fen = fen
        self.load(self.fen)

    def __str__(self):
        """
        Returns an ASCII representation of the board. 
        Empty squares are dots, white pieces are capital letters.
        """
        ascii_board = ""
        for square_name in self.square_list:
            if not self.squares.get(square_name):
                ascii_board  += ". "
            else:
                symbol = self.squares[square_name].symbol
                if self.squares[square_name].color == 'white': 
                    symbol = symbol.upper()
                ascii_board += symbol + " "
            if 'h' in square_name and not '1' in square_name:
                ascii_board += "\n"
        return ascii_board


    def load(self, fen):
        """Load a chess position from a FEN string. 
        You can also do this by passing the fen as an argument
        when instantiating the Board.

        Parameters:
            fen(str): The FEN string used to determine the position

        Returns:
            (bool): Indicating whether or not the FEN was valid
        """
        if not self.is_fen_parseable(fen):
            return False

        self.squares = {}
        color = self.fen.split(' ')[1]
        if color == 'w': 
            self.current_player = 'white'
        else: self.current_player = 'black'

        col = 97 # start at chr(col) = 'a'
        row = 8
        pieces_string = self.fen.split(' ')[0]
        for c in pieces_string:
            if c.isnumeric():
                col += int(c)
            elif c == '/':
                row -= 1
                col = 97
            else:
                if c.isupper(): color = 'white'
                else: color = 'black'
                piece = self.types[c.lower()](color)
                self.squares[chr(col) + str(row)] = piece                
                if self.current_player == 'black' and c == 'k':
                    self.king_location = chr(col) + str(row)
                if self.current_player == 'white' and c == 'K':
                    self.king_location = chr(col) + str(row)
                col += 1

        castling_string = self.fen.split(' ')[2]
        self.castling_bk = 'k' in castling_string
        self.castling_bq = 'q' in castling_string
        self.castling_wk = 'K' in castling_string
        self.castling_wq = 'Q' in castling_string

        if not self.fen.split(' ')[2] == '-': 
            self.ghost_pawn = self.fen.split(' ')[3]
        self.half_moves = int(self.fen.split(' ')[4])
        self.turn = int(self.fen.split(' ')[5])

        return True


    def output_fen(self):
        """Returns the FEN string for the current position"""
        fen = []
        empty_squares = 0
        for s in self.square_list:
            if self.squares.get(s):
                if empty_squares > 0:
                    fen.append(str(empty_squares))
                    empty_squares = 0
                symbol = self.squares[s].symbol
                if self.squares[s].color == 'white': 
                    symbol = symbol.upper()
                fen.append(symbol)
            else:
                empty_squares += 1
            if 'h' in s:
                if empty_squares > 0:
                    fen.append(str(empty_squares))
                empty_squares = 0
            if 'h' in s and not '1' in s:
                fen.append('/')

        fen.append(' ' + self.current_player[0] + ' ')

        castling_rights = ''
        if self.castling_wk == True: 
            castling_rights += 'K'
        if self.castling_wq == True: 
            castling_rights += 'Q'
        if self.castling_bk == True: 
            castling_rights += 'k'
        if self.castling_bq == True: 
            castling_rights += 'q'
        if castling_rights == '': 
            castling_rights = '-'
        fen.append(castling_rights + ' ')

        if self.ghost_pawn is None:
            fen.append('-')
        else:
            fen.append(self.ghost_pawn)

        fen.append(' ' + str(self.half_moves) + ' ' + str(self.turn))
        output = ''.join(fen)
        return output


    def is_check(self):
        """Returns a bool indicating whether the current player is in check"""
        check = False
        # From the king's location, consider every legal move
        # as if the king were each other type of piece.
        # If you encounter that type of piece, it could capture the king.
        knight_moves = (
            Knight(self.current_player)
            .get_moves(self.king_location, self, True)
            )
        bishop_moves = (
            Bishop(self.current_player)
            .get_moves(self.king_location, self, True)
            )
        rook_moves = (
            Rook(self.current_player)
            .get_moves(self.king_location, self, True)
            )
        pawn_moves = (
            Pawn(self.current_player)
            .get_moves(self.king_location, self, True)
            )
        king_moves = (
            King(self.current_player)
            .get_moves(self.king_location, self, True)
            )
        for move in knight_moves:
            piece = self.squares.get(move[2:4])
            if isinstance(piece, Knight):
                check = True
        for move in bishop_moves:
            if check:
                break
            piece = self.squares.get(move[2:4])
            if isinstance(piece, (Bishop, Queen)):
                check = True
        for move in rook_moves:
            if check:
                break
            piece = self.squares.get(move[2:4])
            if isinstance(piece, (Rook, Queen)):
                check = True
        for move in pawn_moves:
            if check:
                break
            piece = self.squares.get(move[2:4])
            if isinstance(piece, Pawn):
                check = True
        for move in king_moves:
            if check:
                break
            piece = self.squares.get(move[2:4])
            if isinstance(piece, King):
                check = True
        return check

    def is_checkmate(self):
        """Returns a bool indicating whether the current player is in checkmate."""
        checkmate = self.is_check() and not self.can_move()
        return checkmate

    def is_stalemate(self):
        """Returns a bool indicating whether the game is drawn due to stalemate."""
        stalemate = not self.is_check() and not self.can_move()
        return stalemate

    def insufficient_material(self):
        """
        Returns a bool indicating whether the game is drawn due to insufficient material.
        Situations where checkmate is possible but highly unlikely,
        such as Kknn (king vs king and two knights), will return false.
        """
        symbols = []
        insufficient = False
        light_bishop = False
        dark_bishop = False

        for square, piece in self.squares.items():
            symbol = piece.symbol
            x = ord(square[0])
            y = int(square[1])
            dark_square = x-y % 2 == 0
            if piece.color == 'white':
                symbol = symbol.upper()
            symbols.append(symbol)
            if isinstance(piece, Bishop) and dark_square:
                dark_bishop = True
            elif isinstance(piece, Bishop) and not dark_square:
                light_bishop = True

        symbols.sort()        
        if symbols == ['K', 'k']:
            insufficient = True
        elif symbols == ['B', 'K', 'k']:
            insufficient = True
        elif symbols == ['K', 'b', 'k']:
            insufficient = True
        elif symbols == ['K', 'N', 'k']:
            insufficient = True
        elif symbols == ['K', 'k', 'n']:
            insufficient = True
        elif symbols == ['B', 'K', 'b', 'k'] and not light_bishop:
            insufficient = True
        elif symbols == ['B', 'K', 'b', 'k'] and not dark_bishop:
            insufficient = True
        return insufficient

    def make_move(self, uci_move):
        """
        Commit a move to the board. This does nothing if move is not legal.

        Parameters:
            uci_move(str): The move in uci format 
                e.g. e2e4 not e4, b2c3 not Nxc3, d7d8q not d8=Q

        Returns:
        (bool): Indicating whether or not the move was valid
        """
        if not self.is_move_legal(uci_move):
            return False

        origin = uci_move[0:2]
        destination = uci_move[2:4]
        king_move = self.king_location == origin
        rook_move = isinstance(self.squares[origin], Rook)
        castle_long = king_move and ord(destination[0]) - ord(origin[0]) == -2
        castle_short = king_move and ord(destination[0]) - ord(origin[0]) == 2
        pawn_move = isinstance(self.squares[origin], Pawn)
        final_rank = destination[1] == '1' or destination[1] == '8'
        double_move = abs(int(origin[1]) - int(destination[1])) == 2
        promotion = pawn_move and final_rank        
        capture = self.squares.get(destination) is not None        

        if promotion:
            new_piece = self.types[uci_move[4]]
            self.squares[origin] = new_piece(self.current_player)

        self.ghost_pawn = None
        if pawn_move and double_move:
            row_behind_pawn = int((int(destination[1]) + int(origin[1])) / 2)
            self.ghost_pawn = origin[0] + str(row_behind_pawn)

        if king_move and self.current_player == 'white':
            self.castling_wk = False
            self.castling_wq = False
        if king_move and self.current_player == 'black':
            self.castling_bk = False
            self.castling_bq = False

        if rook_move and origin == 'a1':
            self.castling_wq = False
        if rook_move and origin == 'h1':
            self.castling_wk = False
        if rook_move and origin == 'a8':
            self.castling_bq = False
        if rook_move and origin == 'h8':
            self.castling_bk = False

        if self.current_player == 'white':
            self.current_player = 'black'
        elif  self.current_player == 'black':
            self.current_player = 'white'
            self.turn += 1

        for square, sq_piece in self.squares.items():
            if (isinstance(sq_piece, King) and 
                sq_piece.color == self.current_player):
                self.king_location = square
                break

        if pawn_move or capture:
            self.half_moves = 0
        else:
            self.half_moves += 1

        if castle_long:
            rook_dest = chr(ord(destination[0]) + 1) + destination[1]
            rook_origin = 'a' + destination[1]
        if castle_short:
            rook_dest = chr(ord(destination[0]) - 1) + destination[1]
            rook_origin = 'h' + destination[1]
        if castle_long or castle_short:
            self.squares[rook_dest] = self.squares[rook_origin]
            del self.squares[rook_origin]

        self.squares[destination] = self.squares[origin]
        del self.squares[origin]
        self.fen = self.output_fen()

        return True


    def is_move_legal(self, uci_move):
        """
        Returns a bool indicating whether a given move is valid and legal.

        Parameters:
            uci_move(str): The move in uci format 
                e.g. e2e4 not e4, b2c3 not Nxc3, d7d8q not d8=Q
        """
        piece = self.squares.get(uci_move[0:2])
        if piece is None:
            return False

        legal = True
        origin = uci_move[0:2]
        destination = uci_move[2:4]        
        pawn_move = isinstance(piece, Pawn)
        final_rank = destination[1] == '1' or destination[1] == '8'
        promotion = final_rank and pawn_move
        plausible_moves = piece.get_moves(origin, self)

        # check validity of string
        if re.fullmatch("[a-h]{1}[1-8]{1}[a-h]{1}[1-8]{1}[bnrq]?", uci_move) is None:
            legal = False
        if self.squares.get(origin) is None:
            legal = False
        if promotion and len(uci_move) != 5:
            legal = False
        if not promotion and len(uci_move) != 4:
            legal = False

        if self.squares[origin].color != self.current_player:
            legal = False
        if not uci_move[0:4] in plausible_moves:
            legal = False

        ## try making the move and see if you are left in check
        #board_clone = Board(self.fen)
        #board_clone.squares[destination] = board_clone.squares[origin]
        #del board_clone.squares[origin]
        #if origin == board_clone.king_location:
        #    board_clone.king_location = destination
        #if board_clone.is_check():
        #    legal = False
        if self._move_puts_self_in_check(uci_move):
            legal = False

        return legal


    def move_notation(self, uci_move):
        """
        Get the algebraic notation for a move provided in uci format.
        This does not commit the move to the board.

        Parameters:
            uci_move(str): The move in uci format 
                e.g. e2e4 not e4, b2c3 not Nxc3, d7d8q not d8=Q

        Returns:
            (str) The algebraic notation for the given move, 
            or None if the given move is not legal.
        """
        if not self.is_move_legal(uci_move):
            return None

        notation = ''
        row = uci_move[0:1]
        col = uci_move[1:2]
        origin = uci_move[0:2]
        destination = uci_move[2:4]
        castle_short = False
        castle_long = False
        capture = False
        piece = self.squares.get(origin)
        specify_row = False
        specify_col = False
        pawn_move = isinstance(piece, Pawn)
        promote_to = None
        final_rank = destination[1] == '1' or destination[1] == '8'

        if pawn_move and final_rank:
            if len(uci_move) != 5:
                raise ValueError
            promote_to = uci_move[4].upper()

        # check if other pieces of same type and color can reach destination square
        next_player = 'white'
        if self.current_player == 'white':
            next_player = 'black'
        piece.color = next_player
        moves = piece.get_moves(destination, self)
        for move in moves:
            move_origin = move[0:2]
            move_destination = move[2:4]
            if move_destination == origin:
                continue
            destination_piece = self.squares.get(move_destination)
            same_type = isinstance(piece, type(destination_piece))
            same_col = move_destination[1] == origin[1]
            if same_type and not same_col:
                specify_row = True
            if same_type and same_col:
                specify_col = True
        piece.color = self.current_player

        if origin == self.king_location and ord(destination[0]) - ord(row) == 2:
            castle_short = True
        if origin == self.king_location and ord(destination[0]) - ord(row) == -2:
            castle_long = True

        if self.squares.get(destination) is not None:
            capture = True
        if self.ghost_pawn == destination and isinstance(piece, Pawn):
            capture = True

        if castle_short:
            notation = 'O-O'
        elif castle_long:
            notation = 'O-O-O'
        elif not isinstance(piece, Pawn):
            notation = piece.symbol.upper()
            if specify_row:
                notation += row
            if specify_col:
                notation += col

        if capture and isinstance(piece, Pawn):
            notation += row + 'x'
        elif capture:
            notation += 'x'

        if not castle_long and not castle_short:
            notation += destination

        if not promote_to is None:
            notation += '=' + promote_to

        board_clone = Board(self.fen)
        board_clone.make_move(uci_move)

        if board_clone.is_checkmate():
            notation += '#'
        elif board_clone.is_check():
            notation += '+'

        return notation

    def is_fen_parseable(self, fen):
        """
        Returns a bool indicating whether the fen can safely be parsed.
        Does not check whether the position is actually legal.

        Parameters:
            fen(str): The FEN to be tested
        """
        parseable = True
        if fen is None or  len(fen.split(" ")) != 6:
            return False

        fen_parts = fen.split(" ")
        if re.fullmatch("(?i)[\/pbnrkq1-8]{17,71}", fen_parts[0]) is None:
            parseable = False
        if re.fullmatch("[wb]{1}", fen_parts[1]) is None:
            parseable = False
        if re.fullmatch("-{1}|K?Q?k?q?", fen_parts[2]) is None:
            parseable = False
        if re.fullmatch("-{1}|[a-h]{1}[1-8]{1}", fen_parts[3]) is None:
            parseable = False
        if not fen_parts[4].isnumeric():
            parseable = False
        if not fen_parts[5].isnumeric():
            parseable = False

        rows = fen_parts[0].split("/")
        if len(rows) != 8:
            parseable = False
        for row in rows:
            squares_in_row = 0
            for char in row:
                if char.isnumeric():
                    squares_in_row += int(char)
                else:
                    squares_in_row += 1
            if squares_in_row != 8:
                parseable = False

        return parseable

    def can_move(self):
        """Returns a bool indicating whether the current player has any legal moves"""
        can_move = False
        for square, piece in self.squares.items():
            if piece.color != self.current_player:
                continue
            for move in piece.get_moves(square, self):
                if self.is_move_legal(move):
                    can_move = True
                    break
        return can_move

    def _move_puts_self_in_check(self, move):
        """Returns a bool indicating whether a move would put the current_player into check"""
        origin = move[0:2]
        destination = move[2:4]
        board_clone = Board(self.fen)
        board_clone.squares[destination] = board_clone.squares[origin]
        del board_clone.squares[origin]
        if origin == board_clone.king_location:
            board_clone.king_location = destination
        return board_clone.is_check()