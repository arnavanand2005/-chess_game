import chess
import random
import math


class ChessAI:
    def __init__(self, depth=3):
        self.depth = depth
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

    def evaluate_board(self, board):
        """
        Evaluate the current board state from the perspective of the current player.
        Positive score favors the current player, negative favors the opponent.
        """
        if board.is_checkmate():
            if board.turn:  # Black just played and checkmated white
                return -math.inf
            else:
                return math.inf
        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
            return 0

        score = 0

        # Material score
        for piece_type in self.piece_values:
            score += len(board.pieces(piece_type, chess.WHITE)) * self.piece_values[piece_type]
            score -= len(board.pieces(piece_type, chess.BLACK)) * self.piece_values[piece_type]

        # Multiply by -1 if black's turn to always evaluate from current player's perspective
        if board.turn == chess.BLACK:
            score = -score

        # Add some positional evaluation (simple version)
        score += self.evaluate_pawn_structure(board)
        score += self.evaluate_mobility(board)

        return score

    def evaluate_pawn_structure(self, board):
        """Evaluate pawn structure (very simplified)"""
        score = 0
        # Doubled pawn penalty
        for file in range(8):
            white_pawns_on_file = len(board.pieces(chess.PAWN, chess.WHITE) & chess.BB_FILES[file])
            black_pawns_on_file = len(board.pieces(chess.PAWN, chess.BLACK) & chess.BB_FILES[file])

            if white_pawns_on_file > 1:
                score -= 10 * (white_pawns_on_file - 1)
            if black_pawns_on_file > 1:
                score += 10 * (black_pawns_on_file - 1)

        return score if board.turn == chess.WHITE else -score

    def evaluate_mobility(self, board):
        """Evaluate mobility (number of legal moves)"""
        mobility = board.legal_moves.count()
        return mobility if board.turn == chess.WHITE else -mobility

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        if maximizing_player:
            max_eval = -math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.alpha_beta_search(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:
            min_eval = math.inf
            for move in board.legal_moves:
                board.push(move)
                eval = self.alpha_beta_search(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def find_best_move(self, board):
        """Find the best move using alpha-beta pruning with iterative deepening"""
        best_move = None
        best_value = -math.inf if board.turn == chess.WHITE else math.inf

        # Iterative deepening (optional but helps with time management)
        for current_depth in range(1, self.depth + 1):
            for move in board.legal_moves:
                board.push(move)
                if board.turn == chess.WHITE:  # We just made a move, so it's opponent's turn
                    move_value = self.alpha_beta_search(board, current_depth - 1, -math.inf, math.inf, False)
                else:
                    move_value = self.alpha_beta_search(board, current_depth - 1, -math.inf, math.inf, True)
                board.pop()

                if board.turn == chess.WHITE and move_value > best_value:
                    best_value = move_value
                    best_move = move
                elif board.turn == chess.BLACK and move_value < best_value:
                    best_value = move_value
                    best_move = move

        # If no move found (shouldn't happen), pick random legal move
        if best_move is None:
            best_move = random.choice(list(board.legal_moves))

        return best_move