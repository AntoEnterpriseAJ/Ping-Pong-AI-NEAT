import pygame

class Button:
    def __init__(self, top_left, width_height, color, text, font, centered_text = True):
        self.rect = pygame.Rect(top_left, width_height)
        self.font = font
        self.color = color

        self.centered_text = centered_text
        self.text_surface = self._create_text_surface(text)
        self.text_position = self._calc_text_pos()

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_position)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def _calc_text_pos(self):
        if self.centered_text:
            return (self.rect.center[0] - self.text_surface.get_width() / 2
                   , self.rect.center[1] - self.text_surface.get_height() / 2)
        else:
            return self.rect

    def _create_text_surface(self, text):
        font = pygame.font.SysFont("Arial", self.font)
        font.bold = True
        return font.render(text, True, (255, 255, 255))
