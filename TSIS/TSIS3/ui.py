import pygame
 
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (180, 180, 180)
DGRAY  = (80,  80,  80)
GREEN  = (50,  200, 80)
RED    = (220, 60,  60)
BLUE   = (60,  120, 220)
YELLOW = (240, 200, 0)
DARK   = (20,  20,  30)
 
 
def draw_button(screen, text, rect, font, active=False):
    color = BLUE if active else DGRAY
    pygame.draw.rect(screen, color, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    label = font.render(text, True, WHITE)
    screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
 
 
def get_username(screen, clock, W, H):
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font_med = pygame.font.SysFont("Arial", 24)
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 16 and event.unicode.isprintable():
                    name += event.unicode
 
        screen.fill(DARK)
        title = font_big.render("Enter your name", True, YELLOW)
        screen.blit(title, (W // 2 - title.get_width() // 2, H // 2 - 80))
        box = pygame.Rect(W // 2 - 150, H // 2 - 20, 300, 48)
        pygame.draw.rect(screen, DGRAY, box, border_radius=6)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=6)
        inp = font_med.render(name + "|", True, WHITE)
        screen.blit(inp, (box.x + 10, box.y + 10))
        hint = font_med.render("Press Enter to start", True, GRAY)
        screen.blit(hint, (W // 2 - hint.get_width() // 2, H // 2 + 50))
        pygame.display.flip()
        clock.tick(60)
 
 
def main_menu(screen, clock, W, H):
    font_big = pygame.font.SysFont("Arial", 52, bold=True)
    font_med = pygame.font.SysFont("Arial", 26)
    buttons = {
        "Play":        pygame.Rect(W // 2 - 120, 220, 240, 52),
        "Leaderboard": pygame.Rect(W // 2 - 120, 290, 240, 52),
        "Settings":    pygame.Rect(W // 2 - 120, 360, 240, 52),
        "Quit":        pygame.Rect(W // 2 - 120, 430, 240, 52),
    }
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        return name
 
        screen.fill(DARK)
        title = font_big.render("RACER", True, YELLOW)
        screen.blit(title, (W // 2 - title.get_width() // 2, 130))
        for name, rect in buttons.items():
            draw_button(screen, name, rect, font_med, rect.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def settings_screen(screen, clock, W, H, settings):
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font_med = pygame.font.SysFont("Arial", 22)
 
    car_colors = ["red", "blue", "green", "yellow", "white"]
    difficulties = ["easy", "normal", "hard"]
 
    back_btn = pygame.Rect(W // 2 - 100, H - 80, 200, 44)
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(mx, my):
                    return
 
                sound_btn = pygame.Rect(W // 2 + 20, 160, 120, 36)
                if sound_btn.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
 
                for i, c in enumerate(car_colors):
                    btn = pygame.Rect(W // 2 - 200 + i * 80, 240, 70, 36)
                    if btn.collidepoint(mx, my):
                        settings["car_color"] = c
 
                for i, d in enumerate(difficulties):
                    btn = pygame.Rect(W // 2 - 160 + i * 110, 320, 100, 36)
                    if btn.collidepoint(mx, my):
                        settings["difficulty"] = d
 
        screen.fill(DARK)
        title = font_big.render("Settings", True, YELLOW)
        screen.blit(title, (W // 2 - title.get_width() // 2, 80))
 
        screen.blit(font_med.render("Sound:", True, WHITE), (W // 2 - 200, 168))
        sound_btn = pygame.Rect(W // 2 + 20, 160, 120, 36)
        draw_button(screen, "ON" if settings["sound"] else "OFF", sound_btn, font_med, settings["sound"])
 
        screen.blit(font_med.render("Car color:", True, WHITE), (W // 2 - 200, 248))
        COLOR_MAP = {"red":(220,50,50),"blue":(50,100,220),"green":(50,180,50),"yellow":(220,200,0),"white":(240,240,240)}
        for i, c in enumerate(car_colors):
            btn = pygame.Rect(W // 2 - 200 + i * 80, 240, 70, 36)
            active = settings["car_color"] == c
            pygame.draw.rect(screen, COLOR_MAP[c], btn, border_radius=6)
            pygame.draw.rect(screen, WHITE if active else GRAY, btn, 2 if not active else 3, border_radius=6)
 
        screen.blit(font_med.render("Difficulty:", True, WHITE), (W // 2 - 200, 328))
        for i, d in enumerate(difficulties):
            btn = pygame.Rect(W // 2 - 160 + i * 110, 320, 100, 36)
            draw_button(screen, d.capitalize(), btn, font_med, settings["difficulty"] == d)
 
        draw_button(screen, "Back", back_btn, font_med, back_btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def leaderboard_screen(screen, clock, W, H, board):
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font_med = pygame.font.SysFont("Arial", 20)
    font_sm  = pygame.font.SysFont("Arial", 18)
    back_btn = pygame.Rect(W // 2 - 100, H - 70, 200, 44)
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(mx, my):
                    return
 
        screen.fill(DARK)
        title = font_big.render("Top 10 Leaderboard", True, YELLOW)
        screen.blit(title, (W // 2 - title.get_width() // 2, 40))
 
        headers = ["#", "Name", "Score", "Distance", "Coins"]
        xs = [40, 90, 280, 390, 500]
        for i, h in enumerate(headers):
            screen.blit(font_med.render(h, True, GRAY), (xs[i], 100))
        pygame.draw.line(screen, GRAY, (30, 125), (W - 30, 125), 1)
 
        for rank, entry in enumerate(board):
            y = 135 + rank * 36
            color = YELLOW if rank == 0 else (GRAY if rank == 1 else WHITE)
            vals = [str(rank+1), entry["name"], str(entry["score"]),
                    f"{entry['distance']}m", str(entry["coins"])]
            for i, v in enumerate(vals):
                screen.blit(font_sm.render(v, True, color), (xs[i], y))
 
        draw_button(screen, "Back", back_btn, font_med, back_btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def game_over_screen(screen, clock, W, H, score, distance, coins):
    font_big = pygame.font.SysFont("Arial", 42, bold=True)
    font_med = pygame.font.SysFont("Arial", 24)
    retry_btn = pygame.Rect(W // 2 - 130, 380, 120, 48)
    menu_btn  = pygame.Rect(W // 2 + 10,  380, 120, 48)
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(mx, my):
                    return "retry"
                if menu_btn.collidepoint(mx, my):
                    return "menu"
 
        screen.fill(DARK)
        title = font_big.render("GAME OVER", True, RED)
        screen.blit(title, (W // 2 - title.get_width() // 2, 160))
 
        for i, line in enumerate([f"Score:    {score}", f"Distance: {int(distance)} m", f"Coins:    {coins}"]):
            t = font_med.render(line, True, WHITE)
            screen.blit(t, (W // 2 - t.get_width() // 2, 240 + i * 38))
 
        draw_button(screen, "Retry",     retry_btn, font_med, retry_btn.collidepoint(mx, my))
        draw_button(screen, "Main Menu", menu_btn,  font_med, menu_btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)