import os
import pickle
import sys

import neat
import pygame

import src.game.config as game_config
from src.app.menu import Menu
from src.app.game_state import GameState
from src.game.game import Game
from src.trainer.trainer import Trainer

class App:
    def __init__(self):
        pygame.font.init()
        self.game_state = GameState.MENU

        self.menu = Menu()
        self.trainer = Trainer()

        self.game = Game()

    def run(self):
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()

        while True:
            self._poll_events()

            if self.game_state == GameState.MENU:
                self.menu.draw(screen)
            elif self.game_state == GameState.PLAYING:
                genome_path = game_config.BASE_PATH / "src/trainer/best_genome.pkl"
                config_path = game_config.BASE_PATH / "src/trainer/config-neat.txt"

                genome, config = App._load_genome(
                    genome_path, config_path
                )
                self.game.update_network(genome, config)
                self.game.run()
            elif self.game_state == GameState.TRAINING:
                self.trainer.run_neat(game_config.BASE_PATH / "src/trainer/config-neat.txt")
                self.game_state = GameState.MENU

            pygame.display.flip()
            clock.tick(60)

    def _poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.game_state = GameState.MENU
            elif self.game_state == GameState.MENU and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.menu.play_button.rect.collidepoint(mouse_pos):
                    self.game_state = GameState.PLAYING
                elif self.menu.train_button.rect.collidepoint(mouse_pos):
                    self.game_state = GameState.TRAINING

    @staticmethod
    def _load_genome(path: str, config_path: str):
        if not os.path.exists(path):
            print(f"Genome file not found: {path}")
            sys.exit(1)

        try:
            with open(path, "rb") as f:
                genome = pickle.load(f)
        except Exception as e:
            print(f"Failed to load genome: {e}")
            sys.exit(1)

        try:
            config = neat.Config(
                neat.DefaultGenome,
                neat.DefaultReproduction,
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation,
                config_path
            )
        except Exception as e:
            print(f"Failed to load NEAT config: {e}")
            sys.exit(1)

        return genome, config
