import neat
import numpy as np
import pygame

from src.game import config
from src.game.paddle import Paddle
from src.game.ball import Ball
from src.game.position import Position
from src.trainer.action import Action

class Game:
    def __init__(self):
        self.ball = Ball(
            pygame.Vector2(config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0),
            config.BALL_RADIUS,
            (255, 255, 255)
        )
        self.player = Paddle(
            30,
            (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) / 2
        )

        self.ai_vision = np.array([1.0, 0.5, 0.5, 1.0, 0.5])
        self.ai_player = Paddle(
            config.SCREEN_WIDTH - 30,
            (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) / 2,
            position=Position.RIGHT
        )

        self.network = None

    def update_network(self, genome, neat_config):
        self.network = neat.nn.FeedForwardNetwork.create(genome, neat_config)

    def run(self, screen):
        pygame.init()
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        while True:
            self._poll_events()
            screen.fill((0, 0, 0))

            self.draw(screen)
            self.update(screen)

            pygame.display.flip()
            clock.tick(60)

    def draw(self, screen):
        self.player.draw(screen)
        self.ai_player.draw(screen)
        self.ball.draw(screen)

    def update(self, screen):
        if not self.player.active or not self.ai_player.active:
            self._reset()

        self.ball.update(training=False)
        self.player.update(self.ball)

        self.ai_player.update(self.ball)
        self.ai_vision[1] = self.ai_player.rectangle.center[1]
        self.ai_vision[2] = self.ball.circle.center[1]
        self.ai_vision[3] = self.ball.velocity.y
        self.ai_vision[4] = self.ball.velocity.x

        prediction = self.network.activate(self.ai_vision)
        best_prediction = Action(prediction.index(max(prediction)))

        if best_prediction == Action.UP:
            self.ai_player.rectangle.y = max(self.ai_player.rectangle.y - config.PADDLE_SPEED, 0)
        elif best_prediction == Action.DOWN:
            self.ai_player.rectangle.y = min(self.ai_player.rectangle.y + config.PADDLE_SPEED,
                                          config.SCREEN_HEIGHT - config.PADDLE_HEIGHT)

    def _reset(self):
        target_point = pygame.Vector2(
            np.random.choice([0, config.SCREEN_WIDTH]),
            np.random.random() * config.SCREEN_HEIGHT
        )

        self.ball.circle.center = pygame.Vector2(config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0)
        self.ball.velocity = (target_point - self.ball.circle.center).normalize() * config.BALL_SPEED

        self.player.rectangle.x = 30
        self.player.rectangle.y = (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) / 2

        self.ai_player.rectangle.x = config.SCREEN_WIDTH - 30
        self.ai_player.rectangle.y = (config.SCREEN_HEIGHT - config.PADDLE_HEIGHT) / 2

        self.ai_player.active = True
        self.player.active = True


    def _poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.rectangle.y = max(self.player.rectangle.y - config.PADDLE_SPEED, 0)
        if keys[pygame.K_s]:
            self.player.rectangle.y = min(self.player.rectangle.y + config.PADDLE_SPEED,
                                          config.SCREEN_HEIGHT - config.PADDLE_HEIGHT)
