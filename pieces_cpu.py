import copy

# This class allows the CPU to simulate moves without actually changing the game pieces

class PiecesCPU:
    def __init__(self, positions=None):
        """
        positions: dict {square_name: "r", "g", "rk", "gk"}
        """
        if positions is None:
            # Default starting positions
            positions = {
                "B8": "g", "D8": "g", "F8": "g", "H8": "g",
                "A7": "g", "C7": "g", "E7": "g", "G7": "g",
                "B6": "g", "D6": "g", "F6": "g", "H6": "g",
                "A3": "r", "C3": "r", "E3": "r", "G3": "r",
                "B2": "r", "D2": "r", "F2": "r", "H2": "r",
                "A1": "r", "C1": "r", "E1": "r", "G1": "r",
            }
        self.positions = positions.copy()


    # Copy & basic helpers
    def copy_positions_only(self):
        return PiecesCPU(self.positions)

    def get_all_player_positions(self, player):
        return [pos for pos, color in self.positions.items() if color[0] == player]

    def has_piece(self, square_name):
        return square_name in self.positions

    def get_piece(self, square_name):
        return self.positions.get(square_name)

    # Coordinate conversion (from pieces.py)
    def algebra_to_rc(self, name):
        col = "ABCDEFGH".index(name[0].upper()) + 1
        row = int(name[1])
        return col, row

    def rc_to_algebra(self, col, row):
        if 1 <= col <= 8 and 1 <= row <= 8:
            return f"{'ABCDEFGH'[col - 1]}{row}"
        return None


    # Move & king logic
    def try_move(self, src: str, dst: str):
        if src not in self.positions or dst in self.positions:
            return False

        piece = self.positions[src]
        src_c, src_r = self.algebra_to_rc(src)
        dst_c, dst_r = self.algebra_to_rc(dst)

        dc = dst_c - src_c
        dr = dst_r - src_r
        forward = 1 if piece in ("r", "rk") else -1

        # Simple move
        if abs(dc) == 1 and (dr == forward or piece.endswith("k") and abs(dr) == 1):
            self.positions[dst] = self.positions.pop(src)
            self.can_king(dst, piece)
            return True

        # Jump / capture
        if abs(dc) == 2 and (dr == 2 * forward or piece.endswith("k") and abs(dr) == 2):
            middle_col = src_c + dc // 2
            middle_row = src_r + dr // 2
            middle_square = self.rc_to_algebra(middle_col, middle_row)

            if middle_square in self.positions:
                middle_piece = self.positions[middle_square]
                if piece[0] != middle_piece[0]:
                    # Execute capture
                    del self.positions[middle_square]
                    self.positions[dst] = self.positions.pop(src)
                    self.can_king(dst, piece)

                    # Check for additional jumps from new position
                    additional_jumps = self.get_legal_jumps_for_piece(dst)
                    if additional_jumps:
                        # Must continue jumping if double jump is available
                        return "jump_available"
                    return True

        return False

    def can_king(self, square, piece):
        _, row = self.algebra_to_rc(square)
        if piece == "r" and row == 8:
            self.positions[square] = "rk"
        elif piece == "g" and row == 1:
            self.positions[square] = "gk"


    # Legal moves for CPU
    def get_legal_moves_for_piece(self, src):
        """Return all legal destination squares for a given piece."""
        if src not in self.positions:
            return []

        piece = self.positions[src]
        src_c, src_r = self.algebra_to_rc(src)
        moves = []

        forward = 1 if piece[0] == "r" else -1
        directions = [(1, forward), (-1, forward)]

        if piece.endswith("k"):
            directions += [(1, -forward), (-1, -forward)]

        # Simple moves
        for dc, dr in directions:
            dst_c, dst_r = src_c + dc, src_r + dr
            dst = self.rc_to_algebra(dst_c, dst_r)
            if dst and dst not in self.positions:
                moves.append(dst)

        # Jumps/ captures
        for dc, dr in directions:
            mid_c, mid_r = src_c + dc, src_r + dr
            dst_c, dst_r = src_c + 2*dc, src_r + 2*dr
            mid = self.rc_to_algebra(mid_c, mid_r)
            dst = self.rc_to_algebra(dst_c, dst_r)
            if dst and mid in self.positions:
                mid_piece = self.positions[mid]
                if mid_piece[0] != piece[0] and dst not in self.positions:
                    moves.append(dst)

        return moves

    # Checks possible legal moves
    def get_legal_jumps_for_piece(self, src):
        piece = self.positions.get(src)
        if not piece:
            return []

        src_c, src_r = self.algebra_to_rc(src)
        jumps = []

        forward = 1 if piece[0] == "r" else -1
        directions = [(1, forward), (-1, forward)]
        if piece.endswith("k"):
            directions += [(1, -forward), (-1, -forward)]

        for dc, dr in directions:
            mid_c, mid_r = src_c + dc, src_r + dr
            dst_c, dst_r = src_c + 2 * dc, src_r + 2 * dr
            mid = self.rc_to_algebra(mid_c, mid_r)
            dst = self.rc_to_algebra(dst_c, dst_r)

            if dst and mid in self.positions:
                mid_piece = self.positions[mid]
                if piece[0] != mid_piece[0] and dst not in self.positions:
                    jumps.append(dst)

        return jumps

    # Simulated move (for minimax)
    def try_move_simulated(self, src, dst):
        temp = copy.deepcopy(self)
        temp.try_move(src, dst)
        return temp
