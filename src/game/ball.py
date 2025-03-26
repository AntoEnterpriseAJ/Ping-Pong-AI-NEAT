import pygame
import src.game.config as config
import numpy as np
from src.game.circle import Circle

class Ball:
    def __init__(self, center, radius, color = pygame.color.Color("red")):
        self.circle = Circle(center, radius, color)

        target_point = pygame.Vector2(0, np.random.random() * config.SCREEN_HEIGHT)
        self.velocity = (target_point - self.circle.center).normalize() * config.BALL_SPEED

    def reset(self):
        self.circle.center = pygame.Vector2(config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0)

        target_point = pygame.Vector2(0, np.random.random() * config.SCREEN_HEIGHT)
        self.velocity = (target_point - self.circle.center).normalize() * config.BALL_SPEED

    def update(self, training = True):
        ball_center = self.circle.center
        ball_radius = self.circle.radius

        self.circle.center += self.velocity

        if training:
            if ball_center.x + ball_radius >= config.SCREEN_WIDTH:
                self.velocity.x = -self.velocity.x

        if ball_center.y - ball_radius <= 0:
            self.velocity.y = -self.velocity.y
            self.circle.center[1] = config.BALL_RADIUS

        if ball_center.y + ball_radius >= config.SCREEN_HEIGHT:
            self.velocity.y = -self.velocity.y
            self.circle.center[1] = config.SCREEN_HEIGHT - config.BALL_RADIUS

        min_x_velocity = 0.5
        if abs(self.velocity.x) < min_x_velocity:
            self.velocity.x = min_x_velocity if self.velocity.x > 0 else -min_x_velocity

        self.velocity = self.velocity.normalize() * config.BALL_SPEED

    def draw(self, screen):
        self.circle.draw(screen)
