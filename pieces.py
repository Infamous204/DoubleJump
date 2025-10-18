import pygame

class Pieces:
    def __init__(self, cell_w, cell_h):
        # Create and scale red and green pieces
        self.red = pygame.image.load('sprites/Red_puck.png').convert_alpha()
        self.green = pygame.image.load('sprites/green_puck.png').convert_alpha()

        scale = 1
        size = (int(cell_w * scale), int(cell_h * scale))
        self.red = pygame.transform.smoothscale(self.red, size)
        self.green = pygame.transform.smoothscale(self.green, size)

        # Set the starting positions
        self.positions = {
            "B8": "g", "D8": "g", "F8": "g", "H8": "g",
            "A7": "g", "C7": "g", "E7": "g", "G7": "g",
            "B6": "g", "D6": "g", "F6": "g", "H6": "g",
            "A3": "r", "C3": "r", "E3": "r", "G3": "r",
            "B2": "r", "D2": "r", "F2": "r", "H2": "r",
            "A1": "r", "C1": "r", "E1": "r", "G1": "r",
        }

    
    # Draws pieces
    def draw_piece(self, screen, squares):
        for name, piece in self.positions.items():
            surf, rect = squares[name]
            img = self.red if piece == "r" else self.green
            piece_rect = img.get_rect(center=rect.center)
            screen.blit(img, piece_rect)

    
    def has_piece(self, square_name: str) -> bool:
        return square_name in self.positions

    def get_piece(self, square_name: str):
        return self.positions.get(square_name)  # "r" or "g" or None

    def algebra_to_rc(self, name: str):
        """
        Convert like 'B6' -> (col_index 1..8, row_number 6)
        Columns: A..H => 1..8
        Rows: numeric already
        """
        col = "ABCDEFGH".index(name[0]) + 1
        row = int(name[1])
        return col, row

    def try_move(self, src: str, dst: str) -> bool:
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

        dc = abs(dst_c - src_c)
        dr = dst_r - src_r

        # forward direction by color
        forward = 1 if piece == "r" else -1

        if dc == 1 and dr == forward:
            # legal simple move
            del self.positions[src]
            self.positions[dst] = piece
            return True

        return False
        
