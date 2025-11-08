import pygame

class Button:
    def __init__(self, image, x_pos, y_pos, text_input, font=None, text_color="white", hover_color="#dddddd"):
        self.image = image  # pre-sized Surface OR None (we’ll autosize off text)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = font or pygame.font.SysFont("Arial", 32)
        self.text_input = text_input
        self.text_color = text_color
        self.hover_color = hover_color

        self.text_surface = self.font.render(self.text_input, True, self.text_color)

        if self.image is None:
            pad_x, pad_y = 20, 12
            self.image = pygame.Surface((self.text_surface.get_width() + pad_x*2, self.text_surface.get_height() + pad_y*2))
            self.image.fill((40, 40, 40))

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    # Draw button
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    # When mouse hovering over button, change the colors a bit 
    def update_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.text_surface = self.font.render(self.text_input, True, self.hover_color)
        else:
            self.text_surface = self.font.render(self.text_input, True, self.text_color)

    # Return True on a left-click inside button
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False
