import neat
import pygame
import pickle

from src.game import config
from src.trainer.agent import Agent

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

        with open("src/trainer/best_genome.pkl", "wb") as f:
            pickle.dump(best_genome, f)
            print("saved best genome")

    def _eval_genomes(self, genomes, neat_config):
        pygame.init()
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        agents = []
        for genome_id, genome in genomes:
            genome.fitness = 0.0

            agents.append(Agent(genome, neat_config))

        while not Trainer._is_extinct(agents):
            self._poll_events()
            screen.fill("purple")

            for agent in agents:
                agent.update()
                agent.draw(screen)

            pygame.display.flip()
            clock.tick(60)

    @staticmethod
    def _is_extinct(agents):
        is_extinct = True
        for agent in agents:
            if agent.paddle.active:
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
