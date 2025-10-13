import pygame
from sys import exit
from pieces import Pieces

pygame.init()
screen = pygame.display.set_mode((416, 624))
pygame.display.set_caption('Double Jump')
clock = pygame.time.Clock()

# Background image
cyber_board = pygame.image.load('/Users/landonphipps/PycharmProjects/DoubleJump/sprites/Green_Cyber_checker_board.jpg')
cyber_board = pygame.transform.scale(cyber_board, (416, 624))

# Board layout constants
CELL_W, CELL_H = 38, 38
ORIGIN_X, ORIGIN_Y = 44, 134  # A8 at this top-left
COLUMNS = "ABCDEFGH"
ROWS = list(range(8, 0, -1))  # 8 down to 1 (A8 is top-left)

def create_board_squares():
    """
    Create a dict mapping 'A8'..'H1' -> (surface, rect),
    with A8 at (ORIGIN_X, ORIGIN_Y).
    """
    x_offset = 2
    y_offset = 5
    
    squares = {}
    for c_idx, file_ in enumerate(COLUMNS):         # 0..7
        x = (ORIGIN_X + c_idx * (CELL_W+x_offset))
        
        for r_idx, rank in enumerate(ROWS):      # 0..7 for 8..1
                

            y = ORIGIN_Y + r_idx * (CELL_H+y_offset)
            name = f"{file_}{rank}"

            # Alternate colors like a chessboard
            color = 'Grey'

            surf = pygame.Surface((CELL_W, CELL_H))
            surf.fill(color)
            rect = surf.get_rect(topleft=(x, y))

            squares[name] = (surf, rect)
    return squares


squares = create_board_squares()

#adds pieces constructor
pieces = Pieces(CELL_W, CELL_H)

# Example: how to access one square later:
# A8_surf, A8_rect = squares["A8"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
        else:
            mouse_click = False

    screen.blit(cyber_board, (0, 0))



    # Draw all 64 squares
    for name, (surf, rect) in squares.items():
        screen.blit(surf, rect)


    mouse_pos = pygame.mouse.get_pos()
    for name, (surf, rect) in squares.items():
        if rect.collidepoint(mouse_pos):
            if (mouse_click):
                print(f"Clicked: {name}")

    # Draw the pieces on the board
    pieces.draw_piece(screen, squares)



    

    pygame.display.update()
    clock.tick(60)

