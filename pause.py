import pygame
from button import Button

class Pause:
    def __init__(self):
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.big_font = pygame.font.SysFont("Arial", 56)

        # Small pause button (top-right)
        self.pause_btn_w, self.pause_btn_h = 40, 32
        self.pause_btn_surf = pygame.Surface((self.pause_btn_w, self.pause_btn_h), pygame.SRCALPHA)
        self.draw_pause_icon(self.pause_btn_surf)
        self.pause_btn_rect = self.pause_btn_surf.get_rect()

        # Large menu buttons (built on-demand so they center correctly)
        self.resume_button = None
        self.menu_button = None

    def draw_pause_icon(self, surf):
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, (240, 240, 240), surf.get_rect(), border_radius=6)
        # pause bars
        w = surf.get_width(); h = surf.get_height()
        bar_w = 6; gap = 8
        x1 = w//2 - gap//2 - bar_w; x2 = w//2 + gap//2
        pygame.draw.rect(surf, (40, 40, 40), pygame.Rect(x1, 6, bar_w, h-12), border_radius=2)
        pygame.draw.rect(surf, (40, 40, 40), pygame.Rect(x2, 6, bar_w, h-12), border_radius=2)

    # Draws the small pause button at the top-right and returns its rect.
    def draw_pause_button(self, screen):
        margin = 10
        self.pause_btn_rect.topright = (screen.get_width() - margin, margin)
        screen.blit(self.pause_btn_surf, self.pause_btn_rect)
        return self.pause_btn_rect

    # Modal pause menu loop. Returns 'resume' or 'menu'
    def show_menu(self, screen):
        # Build overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))

        # Title
        title_surf = self.big_font.render("Paused", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 120))

        # Buttons
        btn_img = pygame.Surface((260, 56))
        btn_img.fill((240, 240, 240))
        cx = screen.get_width()//2

        self.resume_button = Button(btn_img, cx, title_rect.bottom + 60, "Resume", font=pygame.font.SysFont("Arial", 28), text_color=(20,20,20), hover_color='red')
        self.menu_button   = Button(btn_img, cx, title_rect.bottom + 130, "Main Menu", font=pygame.font.SysFont("Arial", 28), text_color=(20,20,20), hover_color='red')

        clock = pygame.time.Clock()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"    # or "quit" if you want window X to quit the whole app
                if self.resume_button.handle_event(event):
                    return "resume"
                if self.menu_button.handle_event(event):
                    return "menu"


            # hover updates
            self.resume_button.update_hover(mouse_pos)
            self.menu_button.update_hover(mouse_pos)

            # draw the modal frame
            screen.blit(overlay, (0, 0))
            screen.blit(title_surf, title_rect)
            self.resume_button.draw(screen)
            self.menu_button.draw(screen)

            pygame.display.update()
            clock.tick(60)
