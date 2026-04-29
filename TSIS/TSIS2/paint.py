import pygame
import sys
import datetime
from tools import (
    draw_pencil, draw_line, draw_rectangle, draw_circle,
    draw_square, draw_right_triangle, draw_equilateral_triangle,
    draw_rhombus, flood_fill
)
 
pygame.init()
 
WIDTH, HEIGHT = 1100, 700
TOOLBAR_W = 180
CANVAS_W = WIDTH - TOOLBAR_W
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint — TSIS2")
 
canvas = pygame.Surface((CANVAS_W, HEIGHT))
canvas.fill((255, 255, 255))
 
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GRAY    = (200, 200, 200)
DGRAY   = (150, 150, 150)
BLUE    = (70,  130, 180)
 
COLORS = [
    (0,0,0),(255,255,255),(255,0,0),(0,200,0),
    (0,0,255),(255,255,0),(255,165,0),(128,0,128),
    (0,255,255),(255,192,203),(139,69,19),(128,128,128),
]
 
TOOLS = ["Pencil","Line","Rect","Circle","Square","R.Tri","E.Tri","Rhombus","Fill","Eraser","Text"]
SIZES = [2, 5, 10]
SIZE_LABELS = ["S", "M", "L"]
 
font_ui   = pygame.font.SysFont("Arial", 14)
font_tool = pygame.font.SysFont("Arial", 13)
font_text = pygame.font.SysFont("Arial", 20)
 
current_tool  = "Pencil"
current_color = BLACK
brush_size    = SIZES[0]
 
drawing    = False
start_pos  = None
prev_pos   = None
preview    = None
 
text_mode   = False
text_pos    = None
text_input  = ""
 
clock = pygame.time.Clock()
 
 
def toolbar_rect():
    return pygame.Rect(CANVAS_W, 0, TOOLBAR_W, HEIGHT)
 
 
def draw_toolbar():
    pygame.draw.rect(screen, GRAY, toolbar_rect())
    pygame.draw.line(screen, DGRAY, (CANVAS_W, 0), (CANVAS_W, HEIGHT), 2)
 
    y = 10
    label = font_ui.render("Tools", True, BLACK)
    screen.blit(label, (CANVAS_W + 10, y))
    y += 20
 
    for tool in TOOLS:
        active = (tool == current_tool)
        color = BLUE if active else WHITE
        rect = pygame.Rect(CANVAS_W + 8, y, TOOLBAR_W - 16, 24)
        pygame.draw.rect(screen, color, rect, border_radius=4)
        pygame.draw.rect(screen, DGRAY, rect, 1, border_radius=4)
        txt = font_tool.render(tool, True, WHITE if active else BLACK)
        screen.blit(txt, (rect.x + 6, rect.y + 5))
        y += 28
 
    y += 6
    label = font_ui.render("Size (1/2/3)", True, BLACK)
    screen.blit(label, (CANVAS_W + 10, y))
    y += 18
 
    for i, (s, lbl) in enumerate(zip(SIZES, SIZE_LABELS)):
        active = (s == brush_size)
        rect = pygame.Rect(CANVAS_W + 8 + i * 54, y, 48, 26)
        pygame.draw.rect(screen, BLUE if active else WHITE, rect, border_radius=4)
        pygame.draw.rect(screen, DGRAY, rect, 1, border_radius=4)
        txt = font_ui.render(lbl, True, WHITE if active else BLACK)
        screen.blit(txt, (rect.x + 17, rect.y + 5))
    y += 34
 
    label = font_ui.render("Colors", True, BLACK)
    screen.blit(label, (CANVAS_W + 10, y))
    y += 18
 
    for i, c in enumerate(COLORS):
        col = i % 3
        row = i // 3
        rect = pygame.Rect(CANVAS_W + 8 + col * 54, y + row * 36, 46, 28)
        pygame.draw.rect(screen, c, rect)
        pygame.draw.rect(screen, BLACK if c == current_color else DGRAY, rect, 2)
 
    y += (len(COLORS) // 3) * 36 + 10
 
    label = font_ui.render("Ctrl+S = Save", True, DGRAY)
    screen.blit(label, (CANVAS_W + 8, HEIGHT - 22))
 
 
def handle_toolbar_click(mx, my):
    global current_tool, brush_size, current_color
 
    y = 30
    for tool in TOOLS:
        rect = pygame.Rect(CANVAS_W + 8, y, TOOLBAR_W - 16, 24)
        if rect.collidepoint(mx, my):
            current_tool = tool
            return
        y += 28
 
    y += 6 + 18
    for i, s in enumerate(SIZES):
        rect = pygame.Rect(CANVAS_W + 8 + i * 54, y, 48, 26)
        if rect.collidepoint(mx, my):
            brush_size = s
            return
    y += 34 + 18
 
    for i, c in enumerate(COLORS):
        col = i % 3
        row = i // 3
        rect = pygame.Rect(CANVAS_W + 8 + col * 54, y + row * 36, 46, 28)
        if rect.collidepoint(mx, my):
            current_color = c
            return
 
 
def canvas_pos(mx, my):
    return (mx, my)
 
 
def apply_tool(surface, start, end, color, size, tool):
    if tool == "Pencil":
        draw_pencil(surface, start, end, color, size)
    elif tool == "Line":
        draw_line(surface, start, end, color, size)
    elif tool == "Rect":
        draw_rectangle(surface, start, end, color, size)
    elif tool == "Circle":
        draw_circle(surface, start, end, color, size)
    elif tool == "Square":
        draw_square(surface, start, end, color, size)
    elif tool == "R.Tri":
        draw_right_triangle(surface, start, end, color, size)
    elif tool == "E.Tri":
        draw_equilateral_triangle(surface, start, end, color, size)
    elif tool == "Rhombus":
        draw_rhombus(surface, start, end, color, size)
    elif tool == "Eraser":
        draw_pencil(surface, start, end, WHITE, size * 4)
 
 
def save_canvas():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{ts}.png"
    pygame.image.save(canvas, filename)
    print(f"Сохранено: {filename}")
 
 
running = True
while running:
    clock.tick(60)
    mx, my = pygame.mouse.get_pos()
    on_canvas = mx < CANVAS_W
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = SIZES[0]
            elif event.key == pygame.K_2:
                brush_size = SIZES[1]
            elif event.key == pygame.K_3:
                brush_size = SIZES[2]
 
            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas()
 
            elif text_mode:
                if event.key == pygame.K_RETURN:
                    surf = font_text.render(text_input, True, current_color)
                    canvas.blit(surf, text_pos)
                    text_mode = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                    text_pos = None
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                else:
                    if event.unicode:
                        text_input += event.unicode
 
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not on_canvas:
                handle_toolbar_click(mx, my)
            else:
                if current_tool == "Fill":
                    flood_fill(canvas, (mx, my), current_color)
                elif current_tool == "Text":
                    text_mode = True
                    text_pos = (mx, my)
                    text_input = ""
                else:
                    drawing = True
                    start_pos = (mx, my)
                    prev_pos = (mx, my)
                    if current_tool not in ("Line","Rect","Circle","Square","R.Tri","E.Tri","Rhombus"):
                        preview = None
                    else:
                        preview = canvas.copy()
 
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing and on_canvas:
                if current_tool in ("Line","Rect","Circle","Square","R.Tri","E.Tri","Rhombus"):
                    if preview:
                        canvas.blit(preview, (0, 0))
                    apply_tool(canvas, start_pos, (mx, my), current_color, brush_size, current_tool)
                drawing = False
                start_pos = None
                prev_pos = None
                preview = None
 
        elif event.type == pygame.MOUSEMOTION:
            if drawing and on_canvas:
                if current_tool in ("Pencil", "Eraser"):
                    apply_tool(canvas, prev_pos, (mx, my), current_color, brush_size, current_tool)
                    prev_pos = (mx, my)
 
    screen.fill(GRAY)
    screen.blit(canvas, (0, 0))
 
    if drawing and current_tool in ("Line","Rect","Circle","Square","R.Tri","E.Tri","Rhombus") and preview:
        tmp = preview.copy()
        apply_tool(tmp, start_pos, (mx, my), current_color, brush_size, current_tool)
        screen.blit(tmp, (0, 0))
 
    if text_mode and text_pos:
        preview_surf = font_text.render(text_input + "|", True, current_color)
        screen.blit(preview_surf, text_pos)
 
    draw_toolbar()
    pygame.display.flip()
 
pygame.quit()
sys.exit()
 