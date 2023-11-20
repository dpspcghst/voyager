import sys
import pygame
from level import Level
from settings import WIDTH, HEIGHT, FPS

class Game():

    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Voyager (v2023.11.20.0.11.0)")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

            self.screen.fill("black")
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
