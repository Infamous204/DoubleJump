import pygame
from sys import exit
from pieces import Pieces
from win import Win
import main_menu
from pause import Pause
from concede import Concede

class Game_board:
    """These are commented out beacuse I THINK we don't need them anymore but I'm not 100% sure."""
    #screen = pygame.display.set_mode((416, 624))
    #pygame.display.set_caption('Double Jump')
    #clock = pygame.time.Clock()

    #cyber_board = pygame.image.load(r'sprites/Green_Cyber_checker_board.jpg')
    #cyber_board = pygame.transform.scale(cyber_board, (416, 624))

    # Board layout constants
    #CELL_W, CELL_H = 39, 39
    #ORIGIN_X, ORIGIN_Y = 44, 134  # A8 at this top-left
    #COLUMNS = "ABCDEFGH"
    #ROWS = list(range(8, 0, -1))  # 8 down to 1 (A8 is top-left)

    #pieces = Pieces(CELL_W, CELL_H)

    def __init__(self):

        self.screen = pygame.display.set_mode((416, 624))
        pygame.display.set_caption('Double Jump')
        self.clock = pygame.time.Clock()

        self.cyber_board = pygame.image.load(r'sprites/Green_Cyber_checker_board.jpg')
        self.cyber_board = pygame.transform.scale(self.cyber_board, (416, 624))

        CELL_W, CELL_H = 39, 39

        self.pieces = Pieces(CELL_W, CELL_H)

        self.selected_square = None
        self.highlight_color = (255, 215, 0)  # gold outline for selection
        self.highlight_thickness = 3
        self.current_turn = "r"

        #Turn timer
        self.turn_time = 60 # 1 minute timer for each turn
        self.turn_start = pygame.time.get_ticks()
        self.time_remaining = self.turn_time
        self.paused_time = 0
        self.pause_start = None

        self.win = Win(self.pieces)

        # game-over UI state
        self.game_over = False
        self.winner = None  # "Red" or "Green"
        self.menu_button_rect = None  # clickable button area

        #Concede button
        self.concede_button = Concede(self.screen.get_width(), self.screen.get_height())

        # Paused vars
        self.pause = Pause()
        self.paused = False
        self.paused_button_rect = None
        return

    #Missing (self)? Not sure if that was intentional so leaving as-is for now.
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
            mouse_position = pygame.mouse.get_pos()
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Pause button click?
                    if self.paused_button_rect and self.paused_button_rect.collidepoint(event.pos):
                        self.pause_start = pygame.time.get_ticks()
                        choice = self.pause.show_menu(self.screen)
                        paused_length = (pygame.time.get_ticks() - self.pause_start)
                        self.turn_start += paused_length
                        if choice == "menu":
                            return "menu"  # returns to checkers_game.py
                    # Concede button click
                    if self.concede_button.handle_event(event) and not self.game_over:
                        self.handle_concede()



                

                if self.game_over:
                    # Only listen for clicks on the button when game is over
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.menu_button_rect and self.menu_button_rect.collidepoint(event.pos):
                            return "menu"
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
                            #Updates turn timer for new turn
                            self.turn_start = pygame.time.get_ticks()
                            self.time_remaining = self.turn_time

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

            # Draw pause button, hides on game over
            if not self.game_over:
                self.paused_button_rect = self.pause.draw_pause_button(self.screen)

            #Draw the concede button and hides on game over
            if not self.game_over:
                self.concede_button.draw(self.screen, mouse_position)

            # Update turn timer
            elapsed_time = (pygame.time.get_ticks() - self.turn_start) / 1000
            self.time_remaining = max(0, self.turn_time - elapsed_time)

            # End turn if the timer runs out
            if self.time_remaining <= 0:
                self.current_turn = "g" if self.current_turn == "r" else "r"
                self.turn_start = pygame.time.get_ticks()
                self.time_remaining = self.turn_time

            # Add timer on game board, hides on game over
            font = pygame.font.SysFont('Arial', 28)
            timer_text = f"Timer: {int(self.time_remaining)}s"
            timer_surf = font.render(timer_text, True, (255, 255, 255))
            if not self.game_over:
                self.screen.blit(timer_surf, (225, 10))


            pygame.display.update()
            self.clock.tick(60)

    #Sets so the current player conceding makes the other player win.
    def handle_concede(self):
        """Current player concedes; opponent wins."""
        if self.game_over:
            return
        opponent = "g" if self.current_turn == "r" else "r"
        self.game_over = True
        self.winner = "Red" if opponent == "r" else "Green"
        self.selected_square = None

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



    def test(self):
        print("testing!!!")