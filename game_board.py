import pygame
from sys import exit
from pieces import Pieces
from win import Win
import main_menu
import threading
from pause import Pause
from concede import Concede
from button import Button
from datetime import datetime
from cpu_player import CPUPlayer
import os
import time

class Game_board:
    def __init__(self, game_mode="PVP"):
        pygame.init()
        self.screen = pygame.display.set_mode((416, 624))
        pygame.display.set_caption('Double Jump')
        self.clock = pygame.time.Clock()

        # Board background
        self.cyber_board = pygame.image.load(r'sprites/Green_Cyber_checker_board.jpg')
        self.cyber_board = pygame.transform.scale(self.cyber_board, (416, 624))

        # Pieces
        CELL_W, CELL_H = 39, 39
        self.pieces = Pieces(CELL_W, CELL_H)

        self.selected_square = None
        self.highlight_color = (255, 215, 0)
        self.highlight_thickness = 3
        self.current_turn = "r"

        # Game mode (PVP or PVC)
        self.game_mode = game_mode
        self.cpu = CPUPlayer(depth=3) if self.game_mode == "PVC" else None
        self.cpu_move_src = None
        self.cpu_move_dst = None

        # CPU threading flags
        self.cpu_thread = None
        self.cpu_done = False
        self.cpu_thinking_delay = 500
        # Timer
        self.turn_time = 60
        self.turn_start = pygame.time.get_ticks()
        self.time_remaining = self.turn_time

        self.win = Win(self.pieces)
        self.game_over = False
        self.winner = None
        self.menu_button_rect = None

        # Concede and undo buttons
        self.concede_button = Concede(self.screen.get_width(), self.screen.get_height())

        btn_img = pygame.Surface((140, 40))
        btn_img.fill((240, 240, 240))
        self.undo_button = Button(
            btn_img,
            x_pos=self.screen.get_width() - 100,
            y_pos=self.screen.get_height() - 50,
            text_input="Undo",
            font=pygame.font.SysFont("Arial", 22),
            text_color=(30, 30, 30),
            hover_color=(0, 0, 160),
        )

        # Logging
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_filename = f"move_log_{timestamp}.txt"
        os.makedirs("logs", exist_ok=True)
        self.log_filepath = os.path.join("logs", self.log_filename)
        with open(self.log_filepath, "w") as f:
            f.write(f"Move Log — Game Started {timestamp}\n")
            f.write("---------------------------------------\n")
        self.move_history = []

        # Pause
        self.pause = Pause()
        self.paused = False
        self.paused_button_rect = None

        # Board squares
        self.squares = self.create_board_squares()

    # CPU logic and movement
    def cpu_move(self):
        """Starts CPU move in a thread."""
        self.cpu_done = False
        self.cpu_thread = threading.Thread(target=self.move_logic)
        self.cpu_thread.start()

    # Gets the best move from minimax
    def move_logic(self):
        """CPU makes a move (called in a thread)."""
        time.sleep(1)
        src, dst = self.cpu.get_best_move(self.pieces, self.squares)
        print("CPU selected move:", src, dst)  # Debug

        # If CPU has a valid move, it will execute it
        if src is not None and dst is not None:
            prev_positions = self.pieces.positions.copy()
            moved = self.pieces.try_move(src, dst)

            while moved == "jump_available":
                # CPU must continue jumping
                next_jumps = self.pieces.get_legal_jumps_for_piece(dst)
                if not next_jumps:
                    break
                # Pick the first available jump
                next_dst = next_jumps[0]
                prev_positions = self.pieces.positions.copy()
                moved = self.pieces.try_move(dst, next_dst)
                dst = next_dst

            if moved:
                # Log move
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.move_history.append({
                    "positions": prev_positions,
                    "turn": "g",
                    "from": src,
                    "to": dst,
                    "saved_at": timestamp,
                })
                with open(self.log_filepath, "a") as f:
                    f.write(f"{timestamp}  G: {src} -> {dst}\n")

                # Check win
                winner = self.win.check_winner("g")
                if winner:
                    self.game_over = True
                    self.winner = "Red" if winner == "r" else "Green"
            else:
                print("CPU move failed legality check:", src, dst)
        else:
            print("CPU has no moves")

        self.cpu_done = True

    # Board Squares
    def create_board_squares(self):
        squares = {}
        CELL_W, CELL_H = 39, 39
        ORIGIN_X, ORIGIN_Y = 44, 134
        COLUMNS = "ABCDEFGH"
        ROWS = list(range(8, 0, -1))
        x_offset, y_offset = 1.5, 3.5

        for c_idx, file_ in enumerate(COLUMNS):
            x = ORIGIN_X + c_idx * (CELL_W + x_offset)
            for r_idx, rank in enumerate(ROWS):
                y = ORIGIN_Y + r_idx * (CELL_H + y_offset)
                surf = pygame.Surface((CELL_W, CELL_H), pygame.SRCALPHA)
                rect = surf.get_rect(topleft=(x, y))
                squares[f"{file_}{rank}"] = (surf, rect)
        return squares

    def square_at_pixel(self, pos):
        for name, (_surf, rect) in self.squares.items():
            if rect.collidepoint(pos):
                return name
        return None

    # Main game loop
    def board_loop(self):

        while True:
            mouse_clicked_square = None
            mouse_position = pygame.mouse.get_pos()

            elapsed_time = (pygame.time.get_ticks() - self.turn_start) / 1000
            self.time_remaining = max(0, self.turn_time - elapsed_time)
            if self.time_remaining <= 0:
                # switch turns
                self.current_turn = "g" if self.current_turn == "r" else "r"
                self.turn_start = pygame.time.get_ticks()
                self.time_remaining = self.turn_time

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                # Pause button
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.paused_button_rect and self.paused_button_rect.collidepoint(event.pos):
                        self.pause_start = pygame.time.get_ticks()
                        choice = self.pause.show_menu(self.screen)
                        paused_length = (pygame.time.get_ticks() - self.pause_start)
                        self.turn_start += paused_length
                        if choice == "menu":
                            return "menu"

                    # Concede button
                    if self.concede_button.handle_event(event) and not self.game_over:
                        self.handle_concede()

                    # Undo button
                    if not self.game_over and self.undo_button.handle_event(event):
                        self.undo_last_move()

                    # Human click on board
                    if not self.game_over:
                        mouse_clicked_square = self.square_at_pixel(event.pos)

                    # Menu button (after game over)
                    if self.game_over and self.menu_button_rect and self.menu_button_rect.collidepoint(event.pos):
                        return "menu"



            # CPU turn (PVC mode)
            if self.game_mode == "PVC" and self.current_turn == "g" and not self.game_over:
                if self.cpu_thread is None:
                    # Start CPU move thread
                    self.cpu_move()
                elif self.cpu_done:
                    # CPU has finished move, switch to Red's turn
                    self.current_turn = "r"
                    self.turn_start = pygame.time.get_ticks()
                    self.time_remaining = self.turn_time
                    self.cpu_thread = None  # reset for next CPU move

            # Player movement
            if mouse_clicked_square and not self.game_over and (
                    self.game_mode == "PVP" or
                    (self.game_mode == "PVC" and self.current_turn == "r")
            ):
                self.handle_player_click(mouse_clicked_square)

            # Draw the board
            self.draw_board(mouse_position)

            pygame.display.update()
            self.clock.tick(60)

    def handle_player_click(self, square):
        """Handle selecting and moving a player's piece."""
        if self.selected_square is None:
            # Pick a piece
            if self.pieces.has_piece(square):
                piece = self.pieces.get_piece(square)
                if piece[0] == self.current_turn:
                    self.selected_square = square
        else:
            # Attempt a move
            if square == self.selected_square:
                self.selected_square = None  # deselect
            else:
                prev_positions = self.pieces.positions.copy()
                prev_turn = self.current_turn

                moved = self.pieces.try_move(self.selected_square, square)

                # Checks for double jump
                if moved == "jump_available":
                    self.selected_square = square
                    return

                if moved:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.move_history.append({
                        "positions": prev_positions,
                        "turn": prev_turn,
                        "from": self.selected_square,
                        "to": square,
                        "saved_at": timestamp,
                    })
                    with open(self.log_filepath, "a") as f:
                        f.write(f"{timestamp}  {prev_turn.upper()}: {self.selected_square} -> {square}\n")

                    # Switch turn
                    self.current_turn = "g" if self.current_turn == "r" else "r"
                    self.turn_start = pygame.time.get_ticks()
                    self.time_remaining = self.turn_time

                    # Check winner
                    winner = self.win.check_winner(prev_turn)
                    if winner:
                        self.game_over = True
                        self.winner = "Red" if winner == "r" else "Green"

                self.selected_square = None

    # -- Handle concede --
    def handle_concede(self):
        if self.game_over:
            return
        opponent = "g" if self.current_turn == "r" else "r"
        self.game_over = True
        self.winner = "Red" if opponent == "r" else "Green"
        self.selected_square = None

    # -- Undo last move ---
    def undo_last_move(self):
        if not self.move_history:
            return
        last = self.move_history.pop()
        self.pieces.positions = last["positions"]
        self.current_turn = last["turn"]
        self.game_over = False
        self.winner = None
        self.selected_square = None
        self.turn_start = pygame.time.get_ticks()
        self.time_remaining = self.turn_time
        print(f"Undoing move {last['from']} -> {last['to']} from {last['saved_at']}")

    # --- Draw winner overlay ---
    def show_winner_screen(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        font = pygame.font.SysFont('Arial', 64)
        msg = font.render(f"{self.winner} Wins!", True, (255, 255, 255))
        rect = msg.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 40))
        self.screen.blit(msg, rect)

        # Menu button
        btn_w, btn_h = 260, 56
        btn_x = (self.screen.get_width() - btn_w) // 2
        btn_y = rect.bottom + 20
        self.menu_button_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        pygame.draw.rect(self.screen, (240, 240, 240), self.menu_button_rect, border_radius=8)
        pygame.draw.rect(self.screen, (50, 50, 50), self.menu_button_rect, width=2, border_radius=8)
        btn_text = pygame.font.SysFont('Arial', 28).render("Back to Main Menu", True, (20, 20, 20))
        self.screen.blit(btn_text, btn_text.get_rect(center=self.menu_button_rect.center))

    # --- Draw everything ---
    def draw_board(self, mouse_pos):
        self.screen.blit(self.cyber_board, (0, 0))
        for surf, rect in self.squares.values():
            self.screen.blit(surf, rect)

        # Highlight selection
        if self.selected_square and not self.game_over:
            pygame.draw.rect(self.screen, self.highlight_color, self.squares[self.selected_square][1], self.highlight_thickness)

        # Draw pieces
        self.pieces.draw_piece(self.screen, self.squares)

        # Draw UI
        if not self.game_over:
            # Turn
            font = pygame.font.SysFont('Arial', 28)
            turn_text = f"Turn: {'Red' if self.current_turn == 'r' else 'Green'}"
            self.screen.blit(font.render(turn_text, True, (255, 255, 255)), (10, 10))
            # Timer
            timer_text = f"Timer: {int(self.time_remaining)}s"
            self.screen.blit(font.render(timer_text, True, (255, 255, 255)), (225, 10))
            # Buttons
            self.paused_button_rect = self.pause.draw_pause_button(self.screen)
            self.concede_button.draw(self.screen, mouse_pos)
            self.undo_button.update_hover(mouse_pos)
            self.undo_button.draw(self.screen)
        else:
            self.show_winner_screen()

    def return_to_menu(self):
        return "menu"

    def test(self):
        print("testing!!!")
