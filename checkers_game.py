from main_menu import Menu
import pygame

def run_menu_get_choice():
    app = Menu()
    app.mainloop()
    return getattr(app, "choice", None)

def run_local_game():
    from game_board import Game_board
    pygame.init()
    game = Game_board()
    game.board_loop()

if __name__ == "__main__":
    choice = run_menu_get_choice()
    if choice == "local":
        run_local_game()


