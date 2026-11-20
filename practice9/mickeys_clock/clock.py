import datetime
import pygame


class MickeyClock:
    def __init__(
        self,
        face_image: pygame.Surface,
        hand_image: pygame.Surface,
        center: tuple[int, int],
        pivot_ratio: tuple[float, float] = (0.72, 0.92),
        hand_offset_angle: float = 0.0,
        show_hours: bool = True,
    ):
        self.face_image = face_image
        self.hand_image = hand_image
        self.center = center
        # Координаты точки крепления (начало руки) в долях ширины и высоты картинки
        self.pivot_ratio = pivot_ratio
        self.hand_offset_angle = hand_offset_angle
        self.show_hours = show_hours

    def get_time_angles(self) -> tuple[float, float, int, int, int]:
        now = datetime.datetime.now()
        seconds = min(now.second, 59)
        minutes = now.minute
        hours = now.hour

        minute_angle = -(minutes / 60.0) * 360.0 + self.hand_offset_angle
        second_angle = -(seconds / 60.0) * 360.0 + self.hand_offset_angle
        return minute_angle, second_angle, hours, minutes, seconds

    def _rotate_around_pivot(
        self, image: pygame.Surface, angle: float, center: tuple[int, int], pivot_ratio: tuple[float, float]
    ) -> tuple[pygame.Surface, pygame.Rect]:
        w, h = image.get_size()
        pivot = pygame.math.Vector2(w * pivot_ratio[0], h * pivot_ratio[1])
        img_center = pygame.math.Vector2(w / 2.0, h / 2.0)

        # Вектор от центра картинки до точки крепления (начало руки)
        offset_from_center = pivot - img_center
        # В Pygame rotate() поворачивает на +angle против часовой стрелки,
        # в Vector2.rotate() положительный угол — по часовой, поэтому берем -angle
        rotated_offset = offset_from_center.rotate(-angle)

        rotated_image = pygame.transform.rotate(image, angle)
        # Позиция центра повернутого спрайта так, чтобы pivot попал ровно в center циферблата
        new_center = pygame.math.Vector2(center) - rotated_offset
        rect = rotated_image.get_rect(center=(round(new_center.x), round(new_center.y)))
        return rotated_image, rect

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        face_rect = self.face_image.get_rect(center=self.center)
        screen.blit(self.face_image, face_rect)

        minute_angle, second_angle, hours, minutes, seconds = self.get_time_angles()

        # Правая рука — минуты, левая (отзеркаленная по X) — секунды
        min_img, min_rect = self._rotate_around_pivot(
            self.hand_image, minute_angle, self.center, self.pivot_ratio
        )
        left_hand = pygame.transform.flip(self.hand_image, True, False)
        left_pivot = (1.0 - self.pivot_ratio[0], self.pivot_ratio[1])
        sec_img, sec_rect = self._rotate_around_pivot(
            left_hand, second_angle, self.center, left_pivot
        )

        screen.blit(min_img, min_rect)
        screen.blit(sec_img, sec_rect)

        # Маленькая точка в центре для аккуратного крепления рук
        pygame.draw.circle(screen, (30, 30, 30), self.center, 5)

        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}" if self.show_hours else f"{minutes:02d}:{seconds:02d}"
        time_text = font.render(time_str, True, (20, 20, 20))
        screen.blit(time_text, time_text.get_rect(center=(self.center[0], 35)))