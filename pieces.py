import pygame

class Pieces:

  def __init__(self, cell_w, cell_h):
    # loads pngs and scales them
    self.red = pygame.image.load("sprites/Red_puck.png").convert_alpha()
    self.green = pygame.image.load("sprites/green_puck.png").convert_alpha()
    scale = 0.9
    size = (int(cell_w * scale), int(cell_h * scale))
    self.red = pygame.transform.smoothscale(self.red, size)
    self.green = pygame.transform.smoothscale(self.green, size)

    self.positions = {  "B8": "g", "D8": "g", "F8": "g", "H8": "g",
            "A7": "g", "C7": "g", "E7": "g", "G7": "g",
            "B6": "g", "D6": "g", "F6": "g", "H6": "g",
            "A3": "r", "C3": "r", "E3": "r", "G3": "r",
            "B2": "r", "D2": "r", "F2": "r", "H2": "r",
            "A1": "r", "C1": "r", "E1": "r", "G1": "r",
                     }

def draw_piece(self, screen, squares):
  for name, piece in self.positions.items():
    rect = squares[name]
    img = self.red if piece == "r" else self.green
    piece_rect = img.get_rect(center=rect.center)
    screen.blit(img, piece_rect)

def move_piece(self, from_sqr, to_sqr):
  if from_sqr in self.positions:
    self.positions[to_sqr] = self.positions.pop(from_sqr)
