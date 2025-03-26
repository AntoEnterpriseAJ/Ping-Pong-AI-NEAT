---

# PingPong AI NEAT

This repository implements a ping-pong game with an **AI agent that learns to play using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm**. Built with Python, Pygame, and NEAT-Python, the project provides both a training mode—where the AI evolves through gameplay—and a play mode, where you can play with the trained AI.

## Features

- **NEAT-based AI Training:** Evolve and train an AI agent to control the paddle by rewarding successful paddle-ball interactions.
- **Interactive Gameplay:** Enjoy a visually engaging ping-pong game with both AI and manual control options.
- **Modular Design:** Organized into separate modules for game logic, AI training, and user interface.

## Requirements

- Python 3.7+
- [Pygame](https://www.pygame.org/news)
- [NEAT-Python](https://neat-python.readthedocs.io/en/latest/)
- [NumPy](https://numpy.org/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AntoEnterpriseAJ/Ping-Pong-AI-NEAT
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Application Modes

- **Menu:** Upon launch, the application displays a menu with two options:
  - **Play:** Runs the game using a pre-trained AI. If a best genome is saved (see below), it will be loaded and used to control the AI paddle.
  - **Train:** Initiates the training mode where NEAT evolves the AI. The training process runs for a set number of generations, saving the best genome to `src/trainer/best_genome.pkl`.

- **Manual Play:** In the playing mode, you can control the left paddle using the keyboard:
  - Press `W` to move the paddle **up**.
  - Press `S` to move the paddle **down**.

- **Exiting:** Press `ESC` at any time to exit the game.

### Training the AI

To train the AI:

1. Select the **Train** option from the menu.
2. The NEAT algorithm will start evolving a population of genomes.
3. The training stops when the fitness criterion specified in `src/trainer/config-neat.txt` is met or when we reach the set number of generations
4. Once complete, the best genome is saved at `src/trainer/best_genome.pkl`.

### Playing with the Trained AI

1. Ensure you have a saved best genome (`best_genome.pkl`).
2. Select the **Play** option from the menu.
3. The game loads the trained genome and the AI paddle is controlled by the neural network built from it.

## Configuration

- **NEAT Configuration:** Modify the settings in `src/trainer/config-neat.txt` to adjust parameters for the NEAT algorithm.
- **Game Configuration:** Adjust game parameters like screen size, paddle speed, and ball speed in `src/game/config.py`.

## Credits

- Developed using [Pygame](https://www.pygame.org) and [NEAT-Python](https://neat-python.readthedocs.io).
- Inspired by classic ping-pong games and AI evolution experiments.

## License

[MIT License](LICENSE)

---
