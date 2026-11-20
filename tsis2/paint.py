import datetime
import os
import sys
import pygame
from tools import BRUSH_SIZES, draw_shape, flood_fill

WIDTH, HEIGHT = 1100, 750
TOOLBAR_H = 90
FPS = 60

TOOLS = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("fill", "Fill"),
    ("text", "Text"),
    ("eraser", "Eraser"),
    ("rect", "Rect"),
    ("circle", "Circle"),
    ("square", "Square"),
    ("right_tri", "R-Tri"),
    ("eq_tri", "Eq-Tri"),
    ("rhombus", "Rhombus"),
]

COLORS = [
    (0, 0, 0),
    (220, 30, 30),
    (30, 150, 50),
    (30, 90, 220),
    (240, 190, 20),
    (160, 50, 200),
    (240, 120, 20),
    (255, 255, 255),
]


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 - Extended Paint")
    clock = pygame.time.Clock()

    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
    canvas.fill((255, 255, 255))

    font_ui = pygame.font.SysFont("Arial", 14, bold=True)
    font_text = pygame.font.SysFont("Arial", 24)

    active_tool = "pencil"
    active_color = (0, 0, 0)
    brush_size = BRUSH_SIZES["small"]

    drawing = False
    start_pos: tuple[int, int] | None = None
    last_pos: tuple[int, int] | None = None

    text_pos: tuple[int, int] | None = None
    text_buffer = ""

    tool_buttons = [
        (pygame.Rect(10 + i * 74, 10, 68, 32), tid, label)
        for i, (tid, label) in enumerate(TOOLS)
    ]
    size_buttons = [
        (pygame.Rect(840 + i * 52, 10, 46, 32), name, px)
        for i, (name, px) in enumerate(BRUSH_SIZES.items())
    ]
    color_buttons = [
        (pygame.Rect(10 + i * 34, 50, 28, 28), col)
        for i, col in enumerate(COLORS)
    ]

    def to_canvas(pos: tuple[int, int]) -> tuple[int, int] | None:
        x, y = pos
        if y >= TOOLBAR_H:
            return x, y - TOOLBAR_H
        return None

    def commit_text() -> None:
        nonlocal text_pos, text_buffer
        if text_pos is not None and text_buffer:
            surf = font_text.render(text_buffer, True, active_color)
            canvas.blit(surf, text_pos)
        text_pos = None
        text_buffer = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                mods = pygame.key.get_mods()
                if (mods & pygame.KMOD_CTRL) and event.key == pygame.K_s:
                    commit_text()
                    base_dir = os.path.dirname(os.path.abspath(__file__))
                    save_dir = os.path.join(base_dir, "saves")
                    os.makedirs(save_dir, exist_ok=True)
                    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    fname = os.path.join(save_dir, f"canvas_{stamp}.png")
                    pygame.image.save(canvas, fname)
                    continue

                if text_pos is not None:
                    if event.key == pygame.K_RETURN:
                        commit_text()
                    elif event.key == pygame.K_ESCAPE:
                        text_pos = None
                        text_buffer = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]
                    elif event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode
                    continue

                if event.key == pygame.K_1:
                    brush_size = BRUSH_SIZES["small"]
                elif event.key == pygame.K_2:
                    brush_size = BRUSH_SIZES["medium"]
                elif event.key == pygame.K_3:
                    brush_size = BRUSH_SIZES["large"]

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if my < TOOLBAR_H:
                    commit_text()
                    for rect, tid, _ in tool_buttons:
                        if rect.collidepoint(event.pos):
                            active_tool = tid
                    for rect, _, px in size_buttons:
                        if rect.collidepoint(event.pos):
                            brush_size = px
                    for rect, col in color_buttons:
                        if rect.collidepoint(event.pos):
                            active_color = col
                else:
                    cpos = to_canvas(event.pos)
                    if cpos is None:
                        continue
                    if active_tool == "text":
                        commit_text()
                        text_pos = cpos
                        text_buffer = ""
                    elif active_tool == "fill":
                        commit_text()
                        flood_fill(canvas, cpos, active_color)
                    else:
                        commit_text()
                        drawing = True
                        start_pos = cpos
                        last_pos = cpos
                        if active_tool in ("pencil", "eraser"):
                            col = (255, 255, 255) if active_tool == "eraser" else active_color
                            pygame.draw.circle(canvas, col, cpos, brush_size // 2)

            elif event.type == pygame.MOUSEMOTION and drawing:
                cpos = to_canvas(event.pos)
                if cpos and last_pos and active_tool in ("pencil", "eraser"):
                    col = (255, 255, 255) if active_tool == "eraser" else active_color
                    pygame.draw.line(canvas, col, last_pos, cpos, brush_size)
                    last_pos = cpos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                cpos = to_canvas(event.pos)
                if start_pos and active_tool not in ("pencil", "eraser", "fill", "text"):
                    end_pt = cpos if cpos else start_pos
                    draw_shape(canvas, active_tool, start_pos, end_pt, active_color, brush_size)
                drawing = False
                start_pos = None
                last_pos = None

        # Рендер холста и предпросмотра
        screen.fill((225, 228, 232))
        screen.blit(canvas, (0, TOOLBAR_H))

        if drawing and start_pos and active_tool not in ("pencil", "eraser", "fill", "text"):
            cur = to_canvas(pygame.mouse.get_pos()) or start_pos
            preview = canvas.copy()
            draw_shape(preview, active_tool, start_pos, cur, active_color, brush_size)
            screen.blit(preview, (0, TOOLBAR_H))

        if text_pos is not None:
            live = font_text.render(text_buffer + "|", True, active_color)
            screen.blit(live, (text_pos[0], text_pos[1] + TOOLBAR_H))

        # Панель инструментов
        pygame.draw.rect(screen, (235, 238, 242), (0, 0, WIDTH, TOOLBAR_H))
        pygame.draw.line(screen, (170, 175, 180), (0, TOOLBAR_H), (WIDTH, TOOLBAR_H), 2)

        for rect, tid, label in tool_buttons:
            selected = active_tool == tid
            pygame.draw.rect(screen, (190, 215, 250) if selected else (255, 255, 255), rect, border_radius=4)
            pygame.draw.rect(screen, (80, 90, 105), rect, 1, border_radius=4)
            txt = font_ui.render(label, True, (20, 20, 20))
            screen.blit(txt, txt.get_rect(center=rect.center))

        for rect, name, px in size_buttons:
            selected = brush_size == px
            pygame.draw.rect(screen, (190, 215, 250) if selected else (255, 255, 255), rect, border_radius=4)
            pygame.draw.rect(screen, (80, 90, 105), rect, 1, border_radius=4)
            txt = font_ui.render(f"{px}px", True, (20, 20, 20))
            screen.blit(txt, txt.get_rect(center=rect.center))

        for rect, col in color_buttons:
            pygame.draw.rect(screen, col, rect, border_radius=4)
            border_w = 3 if col == active_color else 1
            pygame.draw.rect(screen, (30, 30, 30), rect, border_w, border_radius=4)

        hint = font_ui.render("Keys: 1/2/3 = Size | Ctrl+S = Save PNG | Text: Enter/Esc", True, (60, 65, 75))
        screen.blit(hint, (310, 56))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()