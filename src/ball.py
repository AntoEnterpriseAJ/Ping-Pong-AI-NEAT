import pygame
import config
import numpy as np
from circle import Circle

class Ball:
    def __init__(self, center, radius, color = pygame.color.Color("red")):
        self.circle = Circle(center, radius, color)

        target_point = pygame.Vector2(0, np.random.random() * config.SCREEN_HEIGHT)
        self.velocity = (target_point - self.circle.center).normalize() * config.BALL_SPEED

    def reset(self):
        self.circle.center = pygame.Vector2(config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0)

        target_point = pygame.Vector2(0, np.random.random() * config.SCREEN_HEIGHT)
        self.velocity = (target_point - self.circle.center).normalize() * config.BALL_SPEED

    def update(self):
        self.circle.center += self.velocity

    def draw(self, screen):
        self.circle.draw(screen)
