from main_menu import Menu
import pygame

def run_menu_get_choice():
    app = Menu()
    app.mainloop() # closes when user chooses something or closes the window
    return getattr(app, "choice", None)  # return "local" or None

def run_local_game():
    import game_board
    Game_board = game_board.Game_board
 
    pygame.init()
    game = Game_board()
    result = game.board_loop() # return "menu" or "quit"

    # Fully tear down Pygame window before returning
    pygame.event.clear()
    pygame.display.quit()
    pygame.quit() 
    return result

if __name__ == "__main__":
    while True:
        choice = run_menu_get_choice()
        if choice == "local":
            out = run_local_game()
            if out == "quit": # if out == "menu": loop back to Tk menu automatically
                break
            
        else:
            break
