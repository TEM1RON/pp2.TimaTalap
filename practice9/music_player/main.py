import os
import sys
import pygame
from player import MusicPlayer

WIDTH, HEIGHT = 640, 360
FPS = 30


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("Arial", 28, bold=True)
    font_info = pygame.font.SysFont("Arial", 22)
    font_help = pygame.font.SysFont("Arial", 18)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    music_dir = os.path.join(base_dir, "music")
    player = MusicPlayer(music_dir)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                player.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    player.stop()
                    pygame.quit()
                    sys.exit()

        screen.fill((245, 247, 250))

        status = "Playing" if player.is_playing else ("Stopped" if player.is_stopped else "Paused")
        pos = int(player.position_seconds)
        pos_str = f"{pos // 60:02d}:{pos % 60:02d}"
        index_str = f"{player.current_index + 1}/{len(player.tracks)}" if player.tracks else "0/0"

        lines = [
            (font_title, f"Track [{index_str}]: {player.current_track_name}", (20, 20, 20), 50),
            (font_info, f"Status: {status}   |   Position: {pos_str}", (50, 80, 140), 115),
            (font_help, "[P] Play   [S] Stop   [N] Next   [B] Back   [Q] Quit", (80, 80, 80), 210),
        ]

        for fnt, text, color, y in lines:
            surf = fnt.render(text, True, color)
            screen.blit(surf, surf.get_rect(center=(WIDTH // 2, y)))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()