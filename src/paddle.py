import random
import neat
import numpy as np
import pygame
import config

class Paddle:
    def __init__(self, genome, neat_config):
        self.active = True
        self.color = pygame.Color(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

        self.genome = genome
        self.network = neat.nn.FeedForwardNetwork.create(genome, neat_config)
        self.rectangle = pygame.Rect(30, (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) / 2,
                                     config.PADDLE_WIDTH, config.PADDLE_HEIGHT)

        # bias, rectangle_center_y, ball_center_y, ball_vel_y, ball_vel_x
        self.vision = np.array([1.0, 0.5, 0.5, 1.0, 0.5])

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rectangle)

    def update(self, ball):
        if self.active:
            self.think()

            self.vision[1] = self.rectangle.center[1]
            self.vision[2] = ball.circle.center[1]
            self.vision[3] = ball.velocity.y
            self.vision[4] = ball.velocity.x

            self.handle_collisions(ball)

    def think(self):
        actions = {
            0: "up",
            1: "none",
            2: "down"
        }

        prediction = self.network.activate(self.vision)
        best_prediction = prediction.index(max(prediction))

        if actions[best_prediction] == "up":
            self.rectangle.y = max(self.rectangle.y - config.PADDLE_SPEED, 0)
        elif actions[best_prediction] == "down":
            self.rectangle.y = min(self.rectangle.y + config.PADDLE_SPEED,
                                   config.SCREEN_HEIGHT - config.PADDLE_HEIGHT)

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

        if ball_center.x - ball_radius <= 0:
            self.active = False

        if ball_center.x + ball_radius >= config.SCREEN_WIDTH:
            ball.velocity.x = -ball.velocity.x

        if ball_center.y - ball_radius <= 0 or \
                ball_center.y + ball_radius >= config.SCREEN_HEIGHT:
            ball.velocity.y = -ball.velocity.y

            min_x_velocity = 0.5
            if abs(ball.velocity.x) < min_x_velocity:
                ball.velocity.x = min_x_velocity if ball.velocity.x > 0 else -min_x_velocity

            ball.velocity = ball.velocity.normalize() * config.BALL_SPEED
