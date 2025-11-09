import pygame
from button import Button

class Concede:
    def __init__(self, screen_width, screen_height, Font=None):
        if font is None:
            font = pygame.font.SysFont("Ariel",22)

        #Appearence
        btn_img = pygame.Surface((140, 40))
        btn_img.fill((240, 240, 240))

        #Button position (bottom left)
        self.button = Button(img=btn_img, x_pos=100, y_pos=screen_height - 50, text_input="Concede", font=font, text_color=(30, 30, 30), hover_color=(160, 0,0))

    def draw(self, screen, mouse_pos):
        self.button.update_hover(mouse_pos)
        self.button.draw(screen)

    def handle_event(self, event):
        """Returns True when button is clicked"""
        return self.button.handle_event(event)