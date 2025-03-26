import random

import pygame
from src.game import config
from src.game.position import Position

class Paddle:
    def __init__(self, x, y, position = Position.LEFT):
        self.active = True
        self.position = position

        self.color = pygame.Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )
        self.rectangle = pygame.Rect(x, y, config.PADDLE_WIDTH, config.PADDLE_HEIGHT)

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rectangle)

    def update(self, ball):
        if self.active:
            self.handle_collisions(ball)

    def handle_collisions(self, ball):
        ball_center = ball.circle.center
        ball_radius = ball.circle.radius
        paddle_center = self.rectangle.center

        paddle_half_height = self.rectangle.height / 2.0
        paddle_half_width = self.rectangle.width / 2.0

        paddle_to_ball_vec = ball_center - paddle_center
        closest_point = pygame.Vector2(
            pygame.math.clamp(paddle_to_ball_vec.x, -paddle_half_width, paddle_half_width),
            pygame.math.clamp(paddle_to_ball_vec.y, -paddle_half_height, paddle_half_height)
        ) + paddle_center

        paddle_ball_distance = closest_point.distance_to(ball_center)

        if paddle_ball_distance <= ball_radius:
            collision_offset = abs(ball_radius - ball_center.distance_to(closest_point))
            ball.circle.center += paddle_to_ball_vec.normalize() * collision_offset

            bounce_vec = (ball_center - paddle_center).normalize()

            angle_perturbation = random.uniform(-0.2, 0.2)
            perturbation_vec = pygame.Vector2(random.uniform(-1, 1),
                                              random.uniform(-1, 1)).normalize() * angle_perturbation

            new_velocity = (bounce_vec + perturbation_vec).normalize() * config.BALL_SPEED

            min_x_velocity = 5.0
            if abs(new_velocity.x) < min_x_velocity:
                new_velocity.x = min_x_velocity if new_velocity.x > 0 else -min_x_velocity

            ball.velocity = new_velocity.normalize() * config.BALL_SPEED

        if self.position == Position.LEFT:
            if ball_center.x - ball_radius <= 0:
                self.active = False
        else:
            if ball_center.x + ball_radius >= config.SCREEN_WIDTH:
                self.active = False
