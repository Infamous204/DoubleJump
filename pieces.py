import pygame

class Pieces:
    def __init__(self, cell_w, cell_h):
        # Create and scale red and green pieces
        self.red = pygame.image.load('sprites/Red_puck.png').convert_alpha()
        self.green = pygame.image.load('sprites/green_puck.png').convert_alpha()

        scale = 1
        size = (int(cell_w * scale), int(cell_h * scale))
        self.red = pygame.transform.smoothscale(self.red, size)
        self.green = pygame.transform.smoothscale(self.green, size)

        # Set the starting positions
        self.positions = {
            "B8": "g", "D8": "g", "F8": "g", "H8": "g",
            "A7": "g", "C7": "g", "E7": "g", "G7": "g",
            "B6": "g", "D6": "g", "F6": "g", "H6": "g",
            "A3": "r", "C3": "r", "E3": "r", "G3": "r",
            "B2": "r", "D2": "r", "F2": "r", "H2": "r",
            "A1": "r", "C1": "r", "E1": "r", "G1": "r",
        }

    
    # Draws pieces
    def draw_piece(self, screen, squares):
        for name, piece in self.positions.items():
            surf, rect = squares[name]
            img = self.red if piece == "r" else self.green
            piece_rect = img.get_rect(center=rect.center)
            screen.blit(img, piece_rect)
