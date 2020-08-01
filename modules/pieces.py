class _Piece:
    """The base class for all pieces"""

    def __init__(self, color):
        """
        Initializes the class.

        Parameters:
            color(str): Either "black" or "white"
        """
        self.color = color

    def __repr__(self):
        """Returns the color and type of the piece."""
        return('<' + self.color + ' ' + type(self).__name__ + '>')

    def get_moves(self, location, board, captures_only=False):
        """
        Get the possible moves for this piece. Does not consider whether the move is legal

        Parameters:
            location(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves
                (useful for considering whether a pawn is giving check)

        Returns:
            (list): A list of moves in uci format.
        """
        return self._moves(location, board, captures_only)

    @staticmethod
    def _next_sq_in_direction(square, direction):
        """
        Finds the name of the next square in a given compass direction.

        Parameters:
            square(str): The name of the starting square e.g. e2

            direction(str): The compass direction to move in, abbreviated to 1 or 2 letters
                e.g. n, ne, sw, etc.

        Returns:
            (str): The name of the next square in the given direction
                e.g. ne from d2 is e3
                Can return non-real squares e.g. i9
        """
        if 'n' in direction: 
            vertical = 1
        elif 's' in direction: 
            vertical = -1
        else: 
            vertical = 0

        if 'e' in direction: 
            horizontal = 1
        elif 'w' in direction: 
            horizontal = -1
        else: 
            horizontal = 0

        x = ord(square[0]) + horizontal - 96
        y = int(square[1]) + vertical
        return x, y

    @classmethod
    def _bqr_moves(cls, current_square, squares, color, directions):
        """
        Finds all the possible moves, including illegal moves, in a given set of directions

        Parameters:
            current_square(str): The starting square

            squares(dict): A dictionary of squares containing pieces.
                Keys should be named after squares e.g. e4
                The dict should only contain squares that contain a piece

            color(str): The color to use when calculating the moves ("black" or "white")

            directions(list): A list of compass directions, abbreviated to 1 or 2 letters
                e.g. [ne, se, nw, sw] for a bishop

        Returns:
            (str): The name of the next square in the given direction
                e.g. ne from d2 is e3
                Can return non-real squares e.g. i9
        """
        moves_list = []
        for dir in directions:
            previous = current_square

            for i in range(10):
                x, y = cls._next_sq_in_direction(previous, dir)
                if x < 1 or y < 1 or x > 8 or y > 8: 
                    break
                destination = chr(x + 96) + str(y)
                if (squares.get(destination) is not None and
                   squares.get(destination).color == color): 
                    break
                move = current_square + destination
                moves_list.append(move)
                if (squares.get(destination) is not None):
                    break
                previous = destination
        return moves_list


class Pawn(_Piece):
    """A pawn"""
    symbol = 'p'

    def _moves(self, square, board, captures_only):
        """
        Gets a list of the possible moves for this piece.
        This function is used by the parent class (_Piece) to return moves.

        Parameters:
            square(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves

        Returns:
            (list): A list of moves in uci format.
        """
        move_list = []

        if self.color == 'black':
            y = -1
            starting_rank = 7
        else:
            y = 1
            starting_rank = 2
    
        potential_moves = []
        single = square[0] + str(int(square[1]) + y)
        double = square[0] + str(int(square[1]) + (2 * y))

        captures = [
            chr(ord(square[0]) + 1) + str(int(square[1]) + y),
            chr(ord(square[0]) - 1) + str(int(square[1]) + y)]

        if (board.squares.get(single) is None and
            not captures_only):
            move = square + single
            move_list.append(move)

        if (board.squares.get(single) is None and
            board.squares.get(double) is None and
            square[1] == str(starting_rank) and
            not captures_only):
            move = square + double
            move_list.append(move)

        for destination in captures:
            if board.ghost_pawn == destination:
                move = square + destination
                move_list.append(move)

            piece = board.squares.get(destination)
            if piece is not None and piece.color != board.current_player:
                move = square + destination
                move_list.append(move)

        return move_list


class Knight(_Piece):
    """A Knight"""
    symbol = 'n'

    def _moves(self, current_square, board, captures_only):
        """
        Gets a list of the possible moves for this piece.
        This function is used by the parent class (_Piece) to return moves.

        Parameters:
            square(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves

        Returns:
            (list): A list of moves in uci format.
        """
        x = ord(current_square[0])
        y = int(current_square[1])
        moves_list = []
        potential_moves = [
            (x + 1, y + 2), (x + 1, y - 2),
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 1, y + 2), (x - 1, y - 2),
            (x - 2, y + 1), (x - 2, y - 1)]

        for potential in potential_moves:
            destination = chr(potential[0]) + str(potential[1])
            piece = board.squares.get(destination)
            if (potential[0] < 97 or 
                potential[0] > 104 or 
                potential[1] < 1 or 
                potential[1] > 8):
                continue
            if not piece is None and piece.color == self.color:
                continue
            move = current_square + destination
            moves_list.append(move)

        return moves_list


class Bishop(_Piece):
    """A Bishop"""
    symbol = 'b'

    def _moves(self, square, board, captures_only):
        """
        Gets a list of the possible moves for this piece.
        This function is used by the parent class (_Piece) to return moves.

        Parameters:
            square(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves

        Returns:
            (list): A list of moves in uci format.
        """
        move_dir = ['ne', 'nw', 'se', 'sw']
        moves = self._bqr_moves(square, board.squares, self.color, move_dir)
        return moves


class Rook(_Piece):
    """A Rook"""
    symbol = 'r'

    def _moves(self, square, board, captures_only):
        """
        Gets a list of the possible moves for this piece.
        This function is used by the parent class (_Piece) to return moves.

        Parameters:
            square(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves

        Returns:
            (list): A list of moves in uci format.
        """
        move_dir = ['n', 'e', 's', 'w']
        moves = self._bqr_moves(square, board.squares, self.color, move_dir)
        return moves


class Queen(_Piece):
    """A Queen"""
    symbol = 'q'

    def _moves(self, square, board, captures_only):
        """
        Gets a list of the possible moves for this piece.
        This function is used by the parent class (_Piece) to return moves.

        Parameters:
            square(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves

        Returns:
            (list): A list of moves in uci format.
        """
        move_dir = ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw']
        moves = self._bqr_moves(square, board.squares, self.color, move_dir)
        return moves


class King(_Piece):
    """A King"""
    symbol = 'k'

    def _moves(self, square, board, captures_only):
        """
        Gets a list of the possible moves for this piece.
        This function is used by the parent class (_Piece) to return moves.

        Parameters:
            square(str): The location of this piece e.g. e4

            board(Board): The board object upon which this piece exists

            captures_only(bool): Whether the returned value should only include capturing moves

        Returns:
            (list): A list of moves in uci format.
        """
        x = ord(square[0])
        y = int(square[1])
        moves_list = []
        potential_moves = [
            (x + 1, y), (x - 1, y), 
            (x, y + 1), (x, y - 1),
            (x + 1, y + 1), (x + 1, y - 1), 
            (x - 1, y + 1), (x - 1, y - 1)]

        for potential in potential_moves:
            destination = chr(potential[0]) + str(potential[1])
            piece = board.squares.get(destination)
            if (potential[0] < 97 or 
                potential[0] > 104 or 
                potential[1] < 1 or 
                potential[1] > 8):
                continue
            if not piece is None and piece.color == self.color:
                continue
            move = square + destination
            moves_list.append(move)

        if (self.color == 'black' and
                not captures_only and
                board.castling_bk and
                not board.is_check() and 
                board.squares.get('f8') is None and
                board.squares.get('g8') is None and 
                not board._move_puts_self_in_check('e8f8') and
                not board._move_puts_self_in_check('e8g8')):
            moves_list.append('e8g8')

        if (self.color == 'black' and
                not captures_only and
                board.castling_bq and
                not board.is_check() and 
                board.squares.get('d8') is None and
                board.squares.get('b8') is None and 
                not board._move_puts_self_in_check('e8d8') and
                not board._move_puts_self_in_check('e8c8')):
            moves_list.append('e8c8')

        if (self.color == 'white' and
                not captures_only and
                board.castling_wk and
                not board.is_check() and 
                board.squares.get('f1') is None and
                board.squares.get('g1') is None and 
                not board._move_puts_self_in_check('e1f1') and
                not board._move_puts_self_in_check('e1g1')):
            moves_list.append('e1g1')

        if (self.color == 'white' and
                not captures_only and
                board.castling_wq and
                not board.is_check() and 
                board.squares.get('d1') is None and
                board.squares.get('b1') is None and 
                not board._move_puts_self_in_check('e1d1') and
                not board._move_puts_self_in_check('e1c1')):
            moves_list.append('e1c1')

        return moves_list