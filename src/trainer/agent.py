import pygame
import numpy as np
import neat

from src.game import config
from src.game.ball import Ball
from src.game.paddle import Paddle
from src.trainer.action import Action

class Agent:
    def __init__(self, genome, neat_config):
        self.genome = genome
        self.network = neat.nn.FeedForwardNetwork.create(genome, neat_config)

        self.paddle = Paddle(
            30,
            (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) / 2
        )

        self.ball = Ball(
            pygame.Vector2(config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0),
            config.BALL_RADIUS,
            self.paddle.color
        )

        self.vision = np.array([1.0, 0.5, 0.5, 1.0, 0.5])

    def update(self):
        self.vision[1] = self.paddle.rectangle.center[1]
        self.vision[2] = self.ball.circle.center[1]
        self.vision[3] = self.ball.velocity.y
        self.vision[4] = self.ball.velocity.x

        prediction = self.network.activate(self.vision)
        best_prediction = Action(prediction.index(max(prediction)))

        if best_prediction == Action.UP:
            self.paddle.rectangle.y = max(self.paddle.rectangle.y - config.PADDLE_SPEED, 0)
        elif best_prediction == Action.DOWN:
            self.paddle.rectangle.y = min(self.paddle.rectangle.y + config.PADDLE_SPEED,
                                          config.SCREEN_HEIGHT - config.PADDLE_HEIGHT)

        self.paddle.update(self.ball)
        self.ball.update()

        vertical_distance = abs(self.paddle.rectangle.center[1] - self.ball.circle.center[1])
        if vertical_distance < self.paddle.rectangle.height / 2:
            self.genome.fitness += 0.5

    def draw(self, screen):
        self.paddle.draw(screen)
        self.ball.draw(screen)
