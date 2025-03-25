import pygame

from menu import Menu
from game_state import GameState
from src.trainer import Trainer

class App:
    def __init__(self):
        pygame.font.init()

        self.game_state = GameState.MENU
        self.menu = Menu()
        self.trainer = Trainer()

    def run(self):
        pygame.init()
        pygame.font.init()

        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()

        while True:
            self.poll_events()

            if self.game_state == GameState.MENU:
                self.menu.draw(screen)
                print("menu")
            elif self.game_state == GameState.PLAYING:
                print("playing")
            elif self.game_state == GameState.TRAINING:
                self.trainer.run_neat("src/config-neat.txt")
                print("training")

            pygame.display.flip()
            clock.tick(60)

    def poll_events(self):
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
