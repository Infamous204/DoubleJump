import copy
import pygame
from pieces_cpu import PiecesCPU

class Pieces:
    def __init__(self, cell_w, cell_h):
        # Create and scale red and green pieces
        self.red = pygame.image.load('sprites/Red_puck.png').convert_alpha()
        self.green = pygame.image.load('sprites/green_puck.png').convert_alpha()
        self.red_king = pygame.image.load('sprites/Red_King.png').convert_alpha()
        self.green_king = pygame.image.load('sprites/Green_King.png').convert_alpha()

        scale = 1
        size = (int(cell_w * scale), int(cell_h * scale))
        self.red = pygame.transform.smoothscale(self.red, size)
        self.green = pygame.transform.smoothscale(self.green, size)
        self.red_king = pygame.transform.smoothscale(self.red_king, size)
        self.green_king = pygame.transform.smoothscale(self.green_king, size)

        # Set the starting positions
        self.positions = {
            "B8": "g", "D8": "g", "F8": "g", "H8": "g",
            "A7": "g", "C7": "g", "E7": "g", "G7": "g",
            "B6": "g", "D6": "g", "F6": "g", "H6": "g",
            "A3": "r", "C3": "r", "E3": "r", "G3": "r",
            "B2": "r", "D2": "r", "F2": "r", "H2": "r",
            "A1": "r", "C1": "r", "E1": "r", "G1": "r",
        }

    
    # Draws pieces and checks if piece is red, green, red king, or green king
    def draw_piece(self, screen, squares):
        for name, piece in self.positions.items():
            surf, rect = squares[name]
            if piece == "r":
                img = self.red
            elif piece == "g":
                img = self.green
            elif piece == "rk":
                img = self.red_king
            elif piece == "gk":
                img = self.green_king
            else:
                continue
            piece_rect = img.get_rect(center=rect.center)
            screen.blit(img, piece_rect)

    def get_all_player_positions(self, player):
        """Return a list of positions for all pieces belonging to a player ('r' or 'g')."""
        positions = []
        for pos, piece in self.positions.items():  # assuming self.positions[pos] = (color, piece_type)
            if piece[0] == player:
                positions.append(pos)
        return positions

    def has_piece(self, square_name: str):
        return square_name in self.positions

    def get_piece(self, square_name: str):
        return self.positions.get(square_name)  # "r", "g", "rk", or "gk"

    def algebra_to_rc(self, name: str):
        """
        Convert like 'B6' -> (col_index 1..8, row_number 6)
        Columns: A..H => 1..8
        Rows: numeric already
        """
        col = "ABCDEFGH".index(name[0].upper()) + 1
        row = int(name[1])
        return col, row

    def rc_to_algebra(self, col, row):
        if 1 <= col <= 8 and 1 <= row <= 8:
            return f"{'ABCDEFGH'[col - 1]}{row}"
        return None

    def copy_positions_only(self):
        new_pieces = PiecesCPU()
        new_pieces.positions = self.positions.copy()
        return new_pieces

    def get_legal_moves_for_piece(self, src):
        """Return a list of all legal squares for the piece at src."""
        if src not in self.positions:
            return []

        piece = self.positions[src]
        src_c, src_r = self.algebra_to_rc(src)
        moves = []

        # Forward direction for normal pieces
        forward = 1 if piece[0] == "r" else -1
        directions = [(1, forward), (-1, forward)]

        # Kings can move backward too
        if piece.endswith("k"):
            directions += [(1, -forward), (-1, -forward)]

        # Simple moves
        for dc, dr in directions:
            dst_c, dst_r = src_c + dc, src_r + dr
            dst = self.rc_to_algebra(dst_c, dst_r)
            if dst and dst not in self.positions:
                moves.append(dst)

        # Jumps/captures
        for dc, dr in directions:
            mid_c, mid_r = src_c + dc, src_r + dr
            dst_c, dst_r = src_c + 2 * dc, src_r + 2 * dr
            mid = self.rc_to_algebra(mid_c, mid_r)
            dst = self.rc_to_algebra(dst_c, dst_r)
            if dst and mid in self.positions:
                mid_piece = self.positions[mid]
                if piece[0] != mid_piece[0] and dst not in self.positions:
                    moves.append(dst)

        return moves

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
                        # Must continue jumping; player or CPU will handle this next
                        return "jump_available"
                    return True

        return False

    # Promotes a piece to king if it reaches the other end of the board
    def can_king(self, square, piece):
        _, row = self.algebra_to_rc(square)
        if piece == "r" and row == 8:
            self.positions[square] = "rk"
        elif piece == "g" and row == 1:
            self.positions[square] = "gk"

    def try_move_simulated(self, src, dst):
        temp = copy.deepcopy(self)
        return temp.try_move(src, dst)
