import pygame


class Ball:
    def __init__(
        self,
        x: int,
        y: int,
        radius: int = 25,
        step: int = 20,
        color: tuple[int, int, int] = (220, 30, 30),
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.step = step
        self.color = color

    def move(self, dx: int, dy: int, screen_width: int, screen_height: int) -> None:
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step

        # Игнорируем ввод, если шар выйдет за границы экрана
        if new_x - self.radius < 0 or new_x + self.radius > screen_width:
            return
        if new_y - self.radius < 0 or new_y + self.radius > screen_height:
            return

        self.x = new_x
        self.y = new_y

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)