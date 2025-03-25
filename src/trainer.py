import neat
import pygame
from src import config
from src.ball import Ball
from src.paddle import Paddle

class Trainer:
    def run_neat(self, config_file):
        neat_config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                         config_file)
        population = neat.Population(neat_config)

        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(neat.Checkpointer(5))

        best_genome = population.run(self._eval_genomes, 100)

        print(f"Best genome:\n{best_genome}")

    def _eval_genomes(self, genomes, neat_config):
        pygame.init()
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        agents = []
        for genome_id, genome in genomes:
            genome.fitness = 0.0

            paddle = Paddle(genome, neat_config)
            ball = Ball(pygame.Vector2(config.SCREEN_WIDTH / 2.0, config.SCREEN_HEIGHT / 2.0),
                        config.BALL_RADIUS, paddle.color)

            agents.append((paddle, ball))

        while not Trainer._is_extinct(agents):
            self._poll_events()
            screen.fill("purple")

            for paddle, ball in agents:
                paddle.update(ball)
                ball.update()
                paddle.draw(screen)
                ball.draw(screen)

                vertical_distance = abs(paddle.rectangle.center[1] - ball.circle.center[1])
                if vertical_distance < paddle.rectangle.height / 2:
                    paddle.genome.fitness += 0.5

            pygame.display.flip()
            clock.tick(60)

    @staticmethod
    def _is_extinct(agents):
        is_extinct = True
        for (paddle, ball) in agents:
            if paddle.active:
                is_extinct = False

        return is_extinct

    def _poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
