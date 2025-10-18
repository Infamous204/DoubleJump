from game_board import Game_board
import pygame


def board_screen():
    game = Game_board()
    game_on = True

    game.board_loop()

game_on = False

while True:

    if(not(game_on)):
       pygame.init()
    
    board_screen()

