import pygame
from sys import exit
from pieces import Pieces
from win import Win
import main_menu

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
        self.current_turn = "r"
        self.win = Win(self.pieces)

        # game-over UI state
        self.game_over = False
        self.winner = None  # "Red" or "Green"
        self.menu_button_rect = None  # clickable button area
        return

    def create_board_squares():
        squares = {}
        CELL_W, CELL_H = 39, 39
        ORIGIN_X, ORIGIN_Y = 44, 134  # A8 at this top-left
        COLUMNS = "ABCDEFGH"
        ROWS = list(range(8, 0, -1))  # 8 down to 1 (A8 is top-left)

        x_offset = 1.5
        y_offset = 3.5

        for c_idx, file_ in enumerate(COLUMNS):  # 0..7
            x = (ORIGIN_X + c_idx * (CELL_W + x_offset))
            for r_idx, rank in enumerate(ROWS):  # 0..7 for 8..1
                y = ORIGIN_Y + r_idx * (CELL_H + y_offset)
                name = f"{file_}{rank}"
                color = 'Grey'

                surf = pygame.Surface((CELL_W, CELL_H))
                surf.fill(color)
                rect = surf.get_rect(topleft=(x, y))

                squares[name] = (surf, rect)
        return squares

    squares = create_board_squares()

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

                if self.game_over:
                    # Only listen for clicks on the button when game is over
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.menu_button_rect and self.menu_button_rect.collidepoint(event.pos):
                            self.return_to_menu()
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_clicked_square = self.square_at_pixel(event.pos)

            # draw background
            self.screen.blit(self.cyber_board, (0, 0))

            # draw board squares
            for name, (surf, rect) in self.squares.items():
                self.screen.blit(surf, rect)

            # handle selection/move if a click happened (only if not game over)
            if not self.game_over and mouse_clicked_square:
                if self.selected_square is None:
                    # Pick a piece (only if it's the players turn)
                    if self.pieces.has_piece(mouse_clicked_square):
                        piece = self.pieces.get_piece(mouse_clicked_square)
                        if piece[0] == self.current_turn:
                            self.selected_square = mouse_clicked_square
                else:
                    # We have a selected piece; attempt to move
                    if mouse_clicked_square == self.selected_square:
                        # Clicking it again cancels selection
                        self.selected_square = None
                    else:
                        moved = self.pieces.try_move(self.selected_square, mouse_clicked_square)
                        if moved:
                            self.current_turn = "g" if self.current_turn == "r" else "r"

                            # WIN
                            just_moved = "g" if self.current_turn == "r" else "r"
                            winner = self.win.check_winner(just_moved)
                            if winner:
                                self.game_over = True
                                self.winner = "Red" if winner == "r" else "Green"

                                # reset any selection so highlight disappears
                                self.selected_square = None

                        self.selected_square = None

            # draw selection highlight (after squares but before pieces)
            if not self.game_over and self.selected_square is not None:
                _surf, rect = self.squares[self.selected_square]
                pygame.draw.rect(self.screen, self.highlight_color, rect, self.highlight_thickness)

            # draw pieces and show turns on screen
            self.pieces.draw_piece(self.screen, self.squares)

            if not self.game_over:
                font = pygame.font.SysFont('Arial', 28)
                turn = f"Turn: {'Red' if self.current_turn == 'r' else 'Green'}"
                text = font.render(turn, True, (255, 255, 255))
                self.screen.blit(text, (10, 10))
            else:
                self.show_winner_screen()  # draws overlay + button

            pygame.display.update()
            self.clock.tick(60)

    def show_winner_screen(self):
        """Draw the overlay, winner text, and a button to return to the menu."""
        # dark translucent overlay
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # big centered Wins!"
        big_font = pygame.font.SysFont('Arial', 64)
        msg = f"{self.winner} Wins!"
        msg_surf = big_font.render(msg, True, (255, 255, 255))
        msg_rect = msg_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        self.screen.blit(msg_surf, msg_rect)

        # draw the button
        btn_w, btn_h = 260, 56
        btn_x = (self.screen.get_width() - btn_w) // 2
        btn_y = msg_rect.bottom + 20
        self.menu_button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

        # button background
        pygame.draw.rect(self.screen, (240, 240, 240), self.menu_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_button_rect, width=2, border_radius=8)

        # button label
        btn_font = pygame.font.SysFont('Arial', 28)
        btn_text = btn_font.render("Back to Main Menu", True, (20, 20, 20))
        btn_text_rect = btn_text.get_rect(center=self.menu_button_rect.center)
        self.screen.blit(btn_text, btn_text_rect)

    def return_to_menu(self):
        """Close pygame and go back to the main menu."""
        pygame.quit()
        main_menu.Menu().mainloop()
        exit()

    def test(self):
        print("testing!!!")

