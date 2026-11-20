from collections import deque
import math
import pygame

BRUSH_SIZES = {"small": 2, "medium": 5, "large": 10}


def flood_fill(surface: pygame.Surface, start_pos: tuple[int, int], fill_color: tuple[int, int, int]) -> None:
    w, h = surface.get_size()
    sx, sy = start_pos
    if not (0 <= sx < w and 0 <= sy < h):
        return

    target_color = surface.get_at((sx, sy))[:3]
    fill_rgb = fill_color[:3]
    if target_color == fill_rgb:
        return

    queue = deque([(sx, sy)])
    visited = {(sx, sy)}

    while queue:
        x, y = queue.popleft()
        if surface.get_at((x, y))[:3] != target_color:
            continue
        surface.set_at((x, y), fill_rgb)

        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))


def equilateral_triangle_points(p1: tuple[int, int], p2: tuple[int, int]) -> list[tuple[int, int]]:
    x1, y1 = p1
    x2, y2 = p2
    base_len = math.hypot(x2 - x1, y2 - y1)
    if base_len == 0:
        return [p1, p2, p1]
    height = (math.sqrt(3) / 2.0) * base_len
    mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
    dx, dy = (x2 - x1) / base_len, (y2 - y1) / base_len
    # Перпендикуляр вверх/вбок
    vx, vy = dy, -dx
    apex = (round(mx + vx * height), round(my + vy * height))
    return [(x1, y1), (x2, y2), apex]


def rhombus_points(p1: tuple[int, int], p2: tuple[int, int]) -> list[tuple[int, int]]:
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    rx, ry = abs(x2 - x1) // 2, abs(y2 - y1) // 2
    return [(cx, cy - ry), (x2, cy), (cx, cy + ry), (x1, cy)]


def draw_shape(
    surface: pygame.Surface,
    tool: str,
    start: tuple[int, int],
    end: tuple[int, int],
    color: tuple[int, int, int],
    width: int,
) -> None:
    x1, y1 = start
    x2, y2 = end

    if tool == "line":
        pygame.draw.line(surface, color, start, end, width)
    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, color, rect, width)
    elif tool == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        sx = x1 + (side if x2 >= x1 else -side)
        sy = y1 + (side if y2 >= y1 else -side)
        rect = pygame.Rect(min(x1, sx), min(y1, sy), side, side)
        pygame.draw.rect(surface, color, rect, width)
    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        if radius > 0:
            pygame.draw.circle(surface, color, start, radius, width)
    elif tool == "right_tri":
        pts = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, pts, width)
    elif tool == "eq_tri":
        pts = equilateral_triangle_points(start, end)
        pygame.draw.polygon(surface, color, pts, width)
    elif tool == "rhombus":
        pts = rhombus_points(start, end)
        pygame.draw.polygon(surface, color, pts, width)