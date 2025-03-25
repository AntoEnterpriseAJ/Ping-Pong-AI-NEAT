import pygame

class Circle:
    def __init__(self, center, radius, color = pygame.color.Color("red")):
        self.center, self.radius = center, radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
