import pygame
from sys import exit
from game_board import Game_board  # From your original attachments

class GameInitializer:
    def __init__(self):
        # Init Pygame
        pygame.init()

        # Set caption
        pygame.display.set_caption('Double Jump Checkers')

        # Create and run the game board
        self.game = Game_board()

    def run(self):
        try:
            result = self.game.board_loop()
            return result
        except Exception as e:
            print(f"Game error: {e}")  # Debug
            return "quit"
        finally:
            # Clean shutdown
            pygame.quit()

if __name__ == "__main__":
    game_init = GameInitializer()
    result = game_init.run()
    print(f"Game ended with: {result}")