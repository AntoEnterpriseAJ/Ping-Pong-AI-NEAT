from src.game import config
from src.app.button import Button

class Menu:
    def __init__(self):
        play_button_size = (100, 60)
        play_button_pos = ((config.SCREEN_WIDTH - play_button_size[0]) / 2
                           , (config.SCREEN_HEIGHT - play_button_size[1]) / 2)

        train_button_size = (100, 60)
        train_button_pos = ((config.SCREEN_WIDTH - train_button_size[0]) / 2
                            , (config.SCREEN_HEIGHT - train_button_size[1]) / 2 + play_button_size[1] * 3 / 2)

        self.play_button = Button(play_button_pos, play_button_size, (80, 80, 80), "Play", 30)
        self.train_button = Button(train_button_pos, train_button_size, (80, 80, 80), "Train", 30)

    def draw(self, screen):
        self.play_button.draw(screen)
        self.train_button.draw(screen)
