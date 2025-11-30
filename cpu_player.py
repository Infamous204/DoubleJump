# Defines the CPU opponent and minimax algorithm for decision making
class CPUPlayer:
    def __init__(self, depth=3):
        self.depth = depth

    def get_all_moves(self, pieces, player, squares):
        pcopy = pieces.copy_positions_only()  # now returns SimplePieces
        moves = []
        for pos in pcopy.get_all_player_positions(player):
            # add your legal moves logic
            for dst in pieces.get_legal_moves_for_piece(pos):
                moves.append((pos, dst))
        return moves

    def evaluate_board(self, pieces):
        """Simple evaluation: normal piece = 1, king = 2"""
        score = 0
        for p in pieces.positions.values():
            if p == "g":
                score += 1
            elif p == "gk":
                score += 2
            elif p == "r":
                score -= 1
            elif p == "rk":
                score -= 2
        return score

    # Defines our algorithm for CPU decision making
    def minimax(self, pieces, depth, alpha, beta, maximizing_player, squares):
        if depth == 0:
            return self.evaluate_board(pieces)

        player = "g" if maximizing_player else "r"
        moves = self.get_all_moves(pieces, player, squares)

        if not moves:
            return float('-inf') if maximizing_player else float('inf')

        if maximizing_player:
            max_eval = float('-inf')
            for src, dst in moves:
                pcopy = pieces.copy_positions_only()
                pcopy.try_move(src, dst)
                val = self.minimax(pcopy, depth-1, alpha, beta, False, squares)
                max_eval = max(max_eval, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for src, dst in moves:
                pcopy = pieces.copy_positions_only()
                pcopy.try_move(src, dst)
                val = self.minimax(pcopy, depth-1, alpha, beta, True, squares)
                min_eval = min(min_eval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, pieces, squares):
        """
        Returns the best move for CPU ('g') using minimax.
        If no evaluated best move exists, force a legal move.
        """
        all_moves = []

        # Gather all legal moves for green
        for pos in pieces.get_all_player_positions("g"):
            legal_dests = pieces.get_legal_moves_for_piece(pos)
            for dst in legal_dests:
                all_moves.append((pos, dst))

        if not all_moves:
            return None, None  # no moves possible, game over

        # Evaluate moves using minimax
        best_val = float('-inf')
        best_move = None

        for src, dst in all_moves:
            pcopy = pieces.copy_positions_only()
            pcopy.try_move(src, dst)
            val = self.minimax(pcopy, self.depth - 1, float('-inf'), float('inf'), False, squares)
            if val > best_val:
                best_val = val
                best_move = (src, dst)

        # Force a move even if minimax fails
        return best_move if best_move else all_moves[0]

