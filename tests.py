import unittest

from modules.boards import Board
from modules.pieces import Pawn, Queen

class ChessTests(unittest.TestCase):
    def _test_moves_of_square(self, fen, answer, square):
        board = Board(fen)
        piece = board.squares.get(square)
        moves = piece.get_moves(square, board)
        test_values = []
        for move in moves:
            test_values.append(move[2:4])
        self.assertEqual(test_values.sort(), answer.sort())

    def test_instantiate_blank(self):
        fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        board = Board()
        self.assertEqual(fen, board.output_fen())

    def test_instantiate_fen(self):
        fen = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1'
        board = Board(fen)
        self.assertEqual(fen, board.output_fen())

    def test_load_fen(self):
        fen = 'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1'
        board = Board(fen)
        self.assertEqual(fen, board.output_fen())

    def test_king_location_1(self):
        board = Board()
        self.assertEqual('e1', board.king_location)

    def test_king_location_2(self):
        board = Board('rn5r/pppk1pbp/5np1/3Pp3/8/2P5/PP1P1PPP/RNB1K1NR b KQ - 0 9')
        self.assertEqual('d7', board.king_location)

    def test_bishop_moves(self):
        self._test_moves_of_square(
            'r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1', 
              ['a6', 'a4', 'c6', 'c4'], 'b5')

    def test_queen_moves(self):
        self._test_moves_of_square(
            'rn1qkb1r/pppbpppp/5n2/3p4/Q1PP4/8/PP2PPPP/RNB1KBNR w KQkq - 0 1',
              ['a3', 'a5', 'a6', 'b3', 'b4', 'b5', 'c6', 'c2', 'd1', 'd7'], 'a4')

    def test_rook_moves(self):
        self._test_moves_of_square(
            '2kr1bnr/ppp1pppp/2n5/q6b/3P4/2N2N1P/PPP1BPP1/R1BQK2R b KQkq - 0 1',
              ['d7', 'd6', 'd5', 'd4', 'e8'], 'd8')
      
    def test_knight_moves(self):
        self._test_moves_of_square(
            'rnb1kbnr/pppp1ppp/8/4p3/4P2q/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3', 
              ['g1', 'h4', 'g5', 'e5', 'd4'], 'f3')
    
    def test_king_moves_1(self):
        self._test_moves_of_square(
            '6k1/p4ppp/8/8/2P5/6P1/P1P1n3/3K4 w - - 0 29', 
              ['c1', 'd2', 'e2', 'e1'], 'd1')

    def test_king_moves_2(self):
        self._test_moves_of_square(
            'r3k2r/ppp2ppp/5n2/6N1/1bn3b1/2N1P3/PP1B1PPP/R3K2R b KQkq - 7 11', 
              ['e7', 'd7', 'f8', 'g8', 'd8', 'c8'], 'e8')

    def test_king_moves_3(self):
        self._test_moves_of_square(
            'r3k2r/ppp2pp1/5n1p/6N1/1bn3b1/2N1P3/PP1B1PPP/R3K2R w KQkq - 0 12', 
              ['f1', 'g1'], 'e1')

    def test_king_moves_4(self):
        self._test_moves_of_square(
            '2kr3r/ppp2pp1/5n1p/7b/1b6/2N1B3/PP3PPP/R3K1NR w KQ - 3 15', 
              ['f1'], 'e1')

    def test_king_moves_5(self):
        self._test_moves_of_square(
            '2k4r/ppp2pp1/5n1p/8/1b4b1/2N1B3/PP3PPP/3RK1NR b K - 0 15', 
              ['b8'], 'c8')
        
    def test_pawn_moves_1(self):
        self._test_moves_of_square(
            'rnbqkb1r/pppp1ppp/4p2B/4P3/3P1n2/8/PPP2PPP/RN1QKBNR w KQkq - 3 5', 
              ['c3'], 'f2')
        
    def test_pawn_moves_2(self):
        self._test_moves_of_square(
            'rnbqkb1r/pppp2pp/4p2B/4Pp2/3P1n2/5P2/PPP3PP/RN1QKBNR w KQkq f6 0 6', 
              ['f6'], 'e5')

    def test_pawn_moves_3(self):
        self._test_moves_of_square(
            'rnbqkb1r/pppp2pp/4p2B/4Pp2/3P4/5P1n/PPP1Q1PP/RN2KBNR w KQkq - 2 7', 
              ['g3', 'g4', 'h4'], 'g2')

    def test_promotion_1(self):
        board = Board('8/2KP4/5n2/8/8/8/5kp1/8 w - - 0 1')
        board.make_move('d7d8q')
        piece = board.squares['d8']
        self.assertTrue(isinstance(piece, Queen))
        self.assertTrue(piece.color == 'white')

    def test_illegal_uci_1(self):
        board = Board('8/2KP4/5n2/8/8/8/5kp1/8 w - - 0 1')
        self.assertFalse(board.is_move_legal('d7d8'))

    def test_illegal_uci_2(self):
        board = Board('8/2K5/3P4/8/8/1n6/5kp1/8 w - - 0 1')
        self.assertFalse(board.is_move_legal('d6d7q'))
        
    def test_notation_1(self):
        board = Board('r1bqkb1r/pp2pppp/2p5/3Pn1B1/QnB1P3/2N5/PP2NPPP/R4RK1 b Qkq - 0 1')
        notation = board.move_notation('e5d3')
        self.assertEqual(notation, 'Ned3')

    def test_notation_2(self):
        board = Board('8/8/5k2/4n3/3P4/8/2K5/8 w - - 0 1')
        notation = board.move_notation('d4e5')
        self.assertEqual(notation, 'dxe5+')

    def test_notation_3(self):
        board = Board('8/3k4/8/r5r1/8/8/2PPP3/3K4 b - - 0 1')
        notation = board.move_notation('a5a1')
        self.assertEqual(notation, 'Ra1#')

    def test_notation_4(self):
        board = Board('8/1k6/7r/8/3PPP2/3RK2N/q7/7r b - - 0 1')
        notation = board.move_notation('h1h3')
        self.assertEqual(notation, 'Rhxh3#')

    def test_notation_5(self):
        board = Board('5k2/1KP2n2/8/8/8/8/8/8 w - - 0 1')
        notation = board.move_notation('c7c8q')
        self.assertEqual(notation, 'c8=Q+')

    def test_notation_6(self):
        board = Board('rnbqkb1r/pp1p1ppp/5n2/2pPp3/4P3/8/PPP2PPP/RNBQKBNR w KQkq c6 0 1')
        notation = board.move_notation('d5c6')
        self.assertEqual(notation, 'dxc6')

    def test_notation_7(self):
        board = Board('8/4B1pp/8/3Q4/P4kn1/2N5/6P1/4K2R w KQ - 1 30')
        notation = board.move_notation('e1g1')
        self.assertEqual(notation, 'O-O+')

    def test_notation_8(self):
        board = Board('r3k1nr/ppp2ppp/1bn5/3qN3/3P4/2P5/PP2QPPP/R1B3KR b kq - 0 13')
        notation = board.move_notation('e8c8')
        self.assertEqual(notation, 'O-O-O')

    def test_check_1(self):
        board = Board('r2qk2r/ppp1bppp/2npbn2/4p3/4PP2/1P3N2/PBPP2PP/RN1QKB1R b KQkq - 2 7')
        self.assertFalse(board.is_check())

    def test_check_2(self):
        board = Board('r1bqkb1r/pppp1Bpp/2n5/4p1N1/4n3/8/PPPP1PPP/RNBQK2R b KQkq - 0 5')
        self.assertTrue(board.is_check())

    def test_checkmate_1(self):
        board = Board('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
        self.assertTrue(board.is_checkmate())

    def test_checkmate_2(self):
        board = Board('r4b1r/ppp3kp/4QBp1/8/8/8/PPP2PPP/RN2K2R b KQ - 2 16')
        self.assertFalse(board.is_checkmate())

    def test_stalemate_1(self):
        board = Board('8/8/8/8/8/n1p5/P2k4/K7 w - - 0 1')
        self.assertTrue(board.is_stalemate())

    def test_stalemate_2(self):
        board = Board('8/8/8/8/7p/2n5/2k1p2P/K7 w - - 0 1')
        self.assertFalse(board.is_stalemate())

    def test_insufficient_material_1(self):
        board = Board('8/8/8/3kn3/8/8/3K4/8 w - - 0 1')
        self.assertTrue(board.insufficient_material())

    def test_insufficient_material_2(self):
        board = Board('8/8/8/3kn3/8/8/3K4/2R5 w - - 0 1')
        self.assertFalse(board.insufficient_material())
        
    def test_illegal_move_1(self):
        board = Board('r1bqkbnr/ppp1pppp/2n5/1B1P4/8/8/PPPP1PPP/RNBQK1NR b KQkq - 0 3')
        self.assertFalse(board.is_move_legal('c6d4'))
        
    def test_illegal_move_2(self):
        board = Board('r1b1kbnr/ppp1pppp/2n5/1B2q3/8/2N5/PPPP1PPP/R1BQK1NR w KQkq - 2 5')
        self.assertFalse(board.is_move_legal('e1e2'))

    def test_illegal_move_3(self):
        board = Board()
        self.assertFalse(board.make_move('a1a3'))

    def test_illegal_move_4(self):
        board = Board()
        self.assertFalse(board.is_move_legal('d7d5'))

    def test_legal_move_1(self):
        board = Board('r1b1kbnr/ppp1pppp/2n5/1B2q3/8/2N5/PPPP1PPP/R1BQK1NR w KQkq - 2 5')
        self.assertTrue(board.is_move_legal('g1e2'))

    def test_legal_move_2(self):
        board = Board('r1b1kbnr/ppp1pppp/2n5/1B2q3/8/2N5/PPPP1PPP/R1BQK1NR w KQkq - 2 5')
        self.assertTrue(board.is_move_legal('e1f1'))

    def test_castling_1(self):
        board = Board('8/4B1pp/8/3Q4/P4kn1/2N5/6P1/4K2R w KQ - 1 30')
        board.make_move('e1g1')
        self.assertEqual(board.fen, '8/4B1pp/8/3Q4/P4kn1/2N5/6P1/5RK1 b - - 2 30')

    def test_castling_2(self):
        board = Board('r3k1nr/ppp2ppp/1bn5/3qN3/3P4/2P5/PP2QPPP/R1B3KR b kq - 0 13')
        board.make_move('e8c8')
        self.assertEqual(board.fen, '2kr2nr/ppp2ppp/1bn5/3qN3/3P4/2P5/PP2QPPP/R1B3KR w - - 1 14')
        
if __name__ == '__main__':
    unittest.main(verbosity=2)