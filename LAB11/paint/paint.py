import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    clock = pygame.time.Clock()
    
    radius = 5
    mode = 'blue'
    points = []
    strokes = [] 
    figures = []
    figures_perm = []
    drawing = True
    drawing_mode = 1 # 1: brush, 2: rect, 3: circle, 4: square, 5: right_tri, 6: eq_tri, 7: rhombus
    fig_start = 0

    # Мәзір мәтіні
    text_info = [
        "L - Line, Z - Rect, X - Circle",
        "S - Square, T - Right Triangle",
        "E - Equilateral Tri, R - Rhombus",
        "C - Eraser, A - Clear All"
    ]

    r_btn = pygame.Rect(30, 150, 30, 30)
    g_btn = pygame.Rect(30, 200, 30, 30)
    b_btn = pygame.Rect(30, 250, 30, 30)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: drawing = not drawing
                elif event.key == pygame.K_c: mode = 'erase'
                elif event.key == pygame.K_l: drawing_mode = 1
                elif event.key == pygame.K_z: drawing_mode = 2
                elif event.key == pygame.K_x: drawing_mode = 3
                # Practice 11: Жаңа режимдер
                elif event.key == pygame.K_s: drawing_mode = 4 # Square
                elif event.key == pygame.K_t: drawing_mode = 5 # Right triangle
                elif event.key == pygame.K_e: drawing_mode = 6 # Eq triangle
                elif event.key == pygame.K_r: drawing_mode = 7 # Rhombus
                elif event.key == pygame.K_a:
                    strokes, figures_perm = [], []

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if drawing_mode != 1:
                        fig_start = mouse_pos
                    points = [] 
                
                # Түс таңдау
                if r_btn.collidepoint(mouse_pos): mode = 'red'
                elif g_btn.collidepoint(mouse_pos): mode = 'green'
                elif b_btn.collidepoint(mouse_pos): mode = 'blue'

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if drawing_mode == 1 and points:
                        strokes.append((points.copy(), mode, radius))
                    elif drawing_mode > 1 and figures:
                        figures_perm.append((figures[0], mode, radius, drawing_mode))
                        figures = []

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    if drawing_mode == 1:
                        points.append(event.pos)
                    else:
                        figures = [(fig_start, mouse_pos)]
                
        screen.fill((0, 0, 0))

        # Ескі сызықтарды салу
        for pts, col_mode, rad in strokes:
            for i in range(len(pts) - 1):
                drawLineBetween(screen, pts[i], pts[i+1], rad, col_mode)
        
        # Сақталған фигураларды салу
        for coords, col_mode, rad, d_mode in figures_perm:
            st, et = coords
            drawfig(screen, st, et, rad, col_mode, d_mode)

        # Қазіргі салынып жатқан фигура
        if drawing:
            if drawing_mode == 1:
                for i in range(len(points) - 1):
                    drawLineBetween(screen, points[i], points[i+1], radius, mode)
            elif figures:
                s, e = figures[0]
                drawfig(screen, s, e, radius, mode, drawing_mode)
            
        # Интерфейс
        font = pygame.font.SysFont("Arial", 18)
        for i, txt in enumerate(text_info):
            screen.blit(font.render(txt, True, (255, 255, 255)), (10, 10 + i*20))

        pygame.draw.rect(screen, (255, 0, 0), r_btn)
        pygame.draw.rect(screen, (0, 255, 0), g_btn)
        pygame.draw.rect(screen, (0, 0, 255), b_btn)
        
        pygame.display.flip()
        clock.tick(60)

def drawfig(screen, start, end, width, color_mode, draw_mode):
    x1, y1 = start
    x2, y2 = end
    color = (255, 255, 255)
    if color_mode == 'red': color = (255, 0, 0)
    elif color_mode == 'green': color = (0, 255, 0)
    elif color_mode == 'blue': color = (0, 0, 255)
    elif color_mode == 'erase': color = (0, 0, 0)

    dx, dy = x2 - x1, y2 - y1

    if draw_mode == 2: # Rectangle
        pygame.draw.rect(screen, color, (min(x1, x2), min(y1, y2), abs(dx), abs(dy)), width)
    elif draw_mode == 3: # Circle
        r = int((dx**2 + dy**2)**0.5 // 2)
        pygame.draw.circle(screen, color, ((x1+x2)//2, (y1+y2)//2), r, width)
    elif draw_mode == 4: # Square (Practice 11)
        side = max(abs(dx), abs(dy))
        pygame.draw.rect(screen, color, (x1, y1, side, side), width)
    elif draw_mode == 5: # Right Triangle (Practice 11)
        pygame.draw.polygon(screen, color, [(x1, y1), (x1, y2), (x2, y2)], width)
    elif draw_mode == 6: # Equilateral Triangle (Practice 11)
        height = int(abs(dx) * (3**0.5) / 2)
        pygame.draw.polygon(screen, color, [(x1, y2), (x2, y2), ((x1+x2)//2, y2 - height)], width)
    elif draw_mode == 7: # Rhombus (Practice 11)
        pygame.draw.polygon(screen, color, [((x1+x2)//2, y1), (x2, (y1+y2)//2), ((x1+x2)//2, y2), (x1, (y1+y2)//2)], width)

def drawLineBetween(screen, start, end, width, color_mode):
    color = (255, 255, 255)
    if color_mode == 'red': color = (255, 0, 0)
    elif color_mode == 'green': color = (0, 255, 0)
    elif color_mode == 'blue': color = (0, 0, 255)
    elif color_mode == 'erase': color = (0, 0, 0)
    pygame.draw.line(screen, color, start, end, width)

main()