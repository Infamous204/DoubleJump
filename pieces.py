import pygame

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

    def try_move(self, src: str, dst: str):
        """
        Very basic legality:
          - src has a piece
          - dst is empty
          - move is 1 step diagonally forward (no jumps/kings yet)
            * red ('r') moves "up" the board: row + 1
            * green ('g') moves "down": row - 1
        """
        if src not in self.positions:
            return False
        if dst in self.positions:
            return False

        piece = self.positions[src]   # 'r' or 'g'
        src_c, src_r = self.algebra_to_rc(src)
        dst_c, dst_r = self.algebra_to_rc(dst)

        dc = dst_c - src_c
        dr = dst_r - src_r

        # forward direction by color
        forward = 1 if piece in ("r", "rk") else -1

        # Basic move
        if abs(dc) == 1 and (dr == forward or piece.endswith("k") and abs(dr) ==1):
            # legal simple move
            del self.positions[src]
            self.positions[dst] = piece
            self.can_king(dst, piece)
            return True

        # Jump and capture opponents piece
        if abs(dc) == 2 and (dr == 2 * forward or piece.endswith("k") and abs(dr) == 2):
            # Calculates the midpoints between a piece and the space it's jumping to
            middle_col = src_c + dc // 2
            middle_row = src_r + dr // 2
            middle_square = self.rc_to_algebra(middle_col, middle_row)

            if middle_square in self.positions:
                middle_piece = self.positions[middle_square]
                # Checks to make sure captured piece is opposite color
                if (piece[0] == "r" and middle_piece[0] == "g") or (piece[0] == "g" and middle_piece[0] == "r"):
                    del self.positions[middle_square]
                    del self.positions[src]
                    self.positions[dst] = piece
                    self.can_king(dst, piece)
                    return True

        return False

    # Promotes a piece to king if it reaches the other end of the board
    def can_king(self, square, piece):
        _, row = self.algebra_to_rc(square)
        if piece == "r" and row == 8:
            self.positions[square] = "rk"
        elif piece == "g" and row == 1:
            self.positions[square] = "gk"


