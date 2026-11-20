import sys
import pygame
from ball import Ball

WIDTH, HEIGHT = 600, 600
FPS = 60


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()

    # Диаметр 50x50 -> радиус 25
    ball = Ball(x=WIDTH // 2, y=HEIGHT // 2, radius=25, step=20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -1, WIDTH, HEIGHT)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 1, WIDTH, HEIGHT)
                elif event.key == pygame.K_LEFT:
                    ball.move(-1, 0, WIDTH, HEIGHT)
                elif event.key == pygame.K_RIGHT:
                    ball.move(1, 0, WIDTH, HEIGHT)

        screen.fill((255, 255, 255))
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()