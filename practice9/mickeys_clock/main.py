import os
import sys
import pygame
from clock import MickeyClock

WIDTH, HEIGHT = 600, 650
FPS = 10


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32, bold=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    face_path = os.path.join(base_dir, "images", "clock_face.png")
    hand_path = os.path.join(base_dir, "images", "mickey_hand.png")

    face_surf = pygame.image.load(face_path).convert_alpha()
    face_surf = pygame.transform.smoothscale(face_surf, (500, 500))

    hand_surf = pygame.image.load(hand_path).convert_alpha()
    hand_surf = pygame.transform.smoothscale(hand_surf, (110, 220))

    mickey_clock = MickeyClock(
        face_image=face_surf,
        hand_image=hand_surf,
        center=(WIDTH // 2, HEIGHT // 2 + 20),
        pivot_ratio=(0.70, 0.86),
        hand_offset_angle=-35.0,  # подстройте под точное направление на 12 часов
        show_hours=True,        # поставьте False, если нужны только минуты и секунды
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 255))
        mickey_clock.draw(screen, font)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()