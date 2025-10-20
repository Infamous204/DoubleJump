import pygame
from sys import exit
from pieces import Pieces

class Game_board:

    screen = pygame.display.set_mode((416, 624))
    pygame.display.set_caption('Double Jump')
    clock = pygame.time.Clock()

    cyber_board = pygame.image.load(r'sprites/Green_Cyber_checker_board.jpg')
    cyber_board = pygame.transform.scale(cyber_board, (416, 624))

    # Board layout constants
    CELL_W, CELL_H = 39, 39
    ORIGIN_X, ORIGIN_Y = 44, 134  # A8 at this top-left
    COLUMNS = "ABCDEFGH"
    ROWS = list(range(8, 0, -1))  # 8 down to 1 (A8 is top-left)

    pieces = Pieces(CELL_W, CELL_H)

    def __init__(self):
        
        self.selected_square = None
        self.highlight_color = (255, 215, 0)  # gold outline for selection
        self.highlight_thickness = 3
        return

        
    def create_board_squares():
        squares = {}
        CELL_W, CELL_H = 39, 39
        ORIGIN_X, ORIGIN_Y = 44, 134  # A8 at this top-left
        COLUMNS = "ABCDEFGH"
        ROWS = list(range(8, 0, -1))  # 8 down to 1 (A8 is top-left)

        """
        Create a dict mapping 'A8'..'H1' -> (surface, rect),
        with A8 at (ORIGIN_X, ORIGIN_Y).
        """
        x_offset = 1.5
        y_offset = 3.5
        
        for c_idx, file_ in enumerate(COLUMNS):         # 0..7
            x = (ORIGIN_X + c_idx * (CELL_W+x_offset))
            
            for r_idx, rank in enumerate(ROWS):      # 0..7 for 8..1
                    

                y = ORIGIN_Y + r_idx * (CELL_H+y_offset)
                name = f"{file_}{rank}"

                # Alternate colors like a chessboard
                color = 'Grey'

                surf = pygame.Surface((CELL_W, CELL_H))
                surf.fill(color)
                rect = surf.get_rect(topleft=(x, y))

                squares[name] = (surf, rect)
        return squares


    squares = create_board_squares()

    # Example: how to access one square later:
    # A8_surf, A8_rect = squares["A8"]


    def square_at_pixel(self, pos):
        """Return the algebraic name (e.g., 'B6') of the square under pixel pos, or None."""
        for name, (_surf, rect) in self.squares.items():
            if rect.collidepoint(pos):
                return name
        return None

    def board_loop(self):
        while True:
        
            mouse_clicked_square = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_clicked_square = self.square_at_pixel(event.pos)

            # draw background
            self.screen.blit(self.cyber_board, (0, 0))

            # draw board squares
            for name, (surf, rect) in self.squares.items():
                self.screen.blit(surf, rect)

            # handle selection/move if a click happened
            if mouse_clicked_square:
                if self.selected_square is None:
                    # Pick a piece (only if one exists here)
                    if self.pieces.has_piece(mouse_clicked_square):
                        self.selected_square = mouse_clicked_square
                else:
                    # We have a selected piece; attempt to move
                    if mouse_clicked_square == self.selected_square:
                        # Clicking it again cancels selection
                        self.selected_square = None
                    else:
                        moved = self.pieces.try_move(self.selected_square, mouse_clicked_square)
                        # Either way, clear selection after attempting
                        self.selected_square = None

            # draw selection highlight (after squares but before pieces)
            if self.selected_square is not None:
                _surf, rect = self.squares[self.selected_square]
                pygame.draw.rect(self.screen, self.highlight_color, rect, self.highlight_thickness)

            # draw pieces
            self.pieces.draw_piece(self.screen, self.squares)

            pygame.display.update()
            self.clock.tick(60)

    
    def test(self):
        print("testing!!!")
