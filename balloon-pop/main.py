"""Main game loop for Balloon Pop."""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Balloon Pop")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)

    engine = GameEngine()
    running = True
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and engine.game_over:
                    engine.start_new_round()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if engine.game_over:
                    engine.start_new_round()
                else:
                    engine.handle_click(event.pos)

        engine.update(dt)
        engine.draw(screen, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
