from modules.boards import Board

class App:
    """The class containing the functions for user interaction"""
    board = Board()

    def run(self):
        """Endlessly prompt the user to input commands"""
        while (True):
            response = input("Enter a command: ").lower()
            if response == "help":
                for attr_name in App.__dict__:
                    if attr_name == "run":
                        continue
                    attr = getattr(App, attr_name)
                    if callable(attr):
                        print("COMMAND: " + attr_name)
                        print(attr.__doc__)
                        print()
            elif response in App.__dict__ and callable(getattr(self, response)):
                getattr(self, response)()
                print()
            else:
                print("Command not recognised. Type help for a list of valid commands")
                print()

    def new_game(self):
        """Start a new game. This happens automatically when the program starts"""
        self.board = Board()

    def load_position(self):
        """Provide a FEN to load a game from that position"""
        fen = input("Enter FEN: ").lower()
        valid = self.board.load(fen)
        if not valid:
            print("Invalid FEN supplied")

    def make_move(self):
        """Make a move. Provide the move in uci format e.g. e2e4 d7d8q"""
        move = input("Enter move: ").lower()
        valid = self.board.make_move(move)
        if not valid:
            print("Invalid move supplied")

    def print_board(self):
        """Print a representation of the board. Dots are empty squares, capital letters are white pieces"""
        print("\n" + self.board.__str__())

    def print_fen(self):
        """Print the FEN for the current position in the game"""
        print("\n" + self.board.output_fen())

    def print_move_notation(self):
        """Print the algebraic notation for a move in uci format. This does not actually make the move"""
        move = input("Enter move: ").lower()
        print("\n" + self.board.move_notation(move))

    def print_game_state(self):
        """Prints whether the game is checkmate, stalemate, or else which colour is next to move"""
        if self.board.is_checkmate() and self.board.current_player == "black":
            state = "Checkmate - White Wins"
        elif self.board.is_checkmate() and self.board.current_player == "white":
            state = "Checkmate - Black Wins"
        elif self.board.is_stalemate():
            state = "Draw - Stalemate"
        else:
            state = self.board.current_player + " to move"
        print("\n" + state)