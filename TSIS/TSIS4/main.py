import pygame
import sys
import json
import os
from config import *
from game import SnakeGame
from db import init_db, get_or_create_player, save_session, get_personal_best, get_leaderboard
 
SETTINGS_FILE = "settings.json"
 
DEFAULT_SETTINGS = {
    "snake_color": [50, 200, 80],
    "grid": True,
    "sound": False
}
 
pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Snake — TSIS4")
clock = pygame.time.Clock()
 
 
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            data = json.load(f)
        for k, v in DEFAULT_SETTINGS.items():
            if k not in data:
                data[k] = v
        return data
    return DEFAULT_SETTINGS.copy()
 
 
def save_settings(s):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)
 
 
def draw_button(text, rect, font, hover=False):
    pygame.draw.rect(screen, BLUE if hover else DGRAY, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    t = font.render(text, True, WHITE)
    screen.blit(t, (rect.centerx - t.get_width()//2, rect.centery - t.get_height()//2))
 
 
def get_username_screen():
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font_med = pygame.font.SysFont("Arial", 22)
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 16 and event.unicode.isprintable():
                    name += event.unicode
        screen.fill(DARK)
        t = font_big.render("Enter username", True, YELLOW)
        screen.blit(t, (W//2 - t.get_width()//2, H//2 - 80))
        box = pygame.Rect(W//2 - 150, H//2 - 24, 300, 48)
        pygame.draw.rect(screen, DGRAY, box, border_radius=6)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=6)
        inp = font_med.render(name + "|", True, WHITE)
        screen.blit(inp, (box.x + 10, box.y + 12))
        hint = font_med.render("Press Enter to continue", True, GRAY)
        screen.blit(hint, (W//2 - hint.get_width()//2, H//2 + 40))
        pygame.display.flip()
        clock.tick(60)
 
 
def main_menu():
    font_big = pygame.font.SysFont("Arial", 52, bold=True)
    font_med = pygame.font.SysFont("Arial", 26)
    btns = {
        "Play":        pygame.Rect(W//2 - 120, 200, 240, 50),
        "Leaderboard": pygame.Rect(W//2 - 120, 268, 240, 50),
        "Settings":    pygame.Rect(W//2 - 120, 336, 240, 50),
        "Quit":        pygame.Rect(W//2 - 120, 404, 240, 50),
    }
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for name, r in btns.items():
                    if r.collidepoint(mx, my):
                        return name
        screen.fill(DARK)
        t = font_big.render("SNAKE", True, GREEN)
        screen.blit(t, (W//2 - t.get_width()//2, 110))
        for name, r in btns.items():
            draw_button(name, r, font_med, r.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def leaderboard_screen():
    font_big = pygame.font.SysFont("Arial", 32, bold=True)
    font_med = pygame.font.SysFont("Arial", 19)
    font_sm  = pygame.font.SysFont("Arial", 17)
    back_btn = pygame.Rect(W//2 - 100, H - 60, 200, 44)
    board = get_leaderboard()
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(mx, my):
                    return
        screen.fill(DARK)
        t = font_big.render("Top 10 Leaderboard", True, YELLOW)
        screen.blit(t, (W//2 - t.get_width()//2, 30))
 
        xs = [20, 80, 260, 360, 460]
        for i, h in enumerate(["#", "Name", "Score", "Level", "Date"]):
            screen.blit(font_med.render(h, True, GRAY), (xs[i], 80))
        pygame.draw.line(screen, GRAY, (10, 104), (W - 10, 104), 1)
 
        for rank, row in enumerate(board):
            y = 112 + rank * 32
            color = YELLOW if rank == 0 else GRAY if rank == 1 else WHITE
            vals = [str(rank+1), row[0], str(row[1]), str(row[2]), row[3]]
            for i, v in enumerate(vals):
                screen.blit(font_sm.render(v, True, color), (xs[i], y))
 
        draw_button("Back", back_btn, font_med, back_btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def settings_screen(settings):
    font_big = pygame.font.SysFont("Arial", 32, bold=True)
    font_med = pygame.font.SysFont("Arial", 22)
    back_btn = pygame.Rect(W//2 - 110, H - 70, 220, 46)
 
    COLORS = [
        ([50, 200, 80],  "Green"),
        ([60, 120, 220], "Blue"),
        ([220, 50, 50],  "Red"),
        ([240, 200, 0],  "Yellow"),
        ([200, 100, 220],"Purple"),
    ]
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(mx, my):
                    save_settings(settings)
                    return
 
                grid_btn = pygame.Rect(W//2 + 20, 160, 120, 36)
                if grid_btn.collidepoint(mx, my):
                    settings["grid"] = not settings["grid"]
 
                sound_btn = pygame.Rect(W//2 + 20, 216, 120, 36)
                if sound_btn.collidepoint(mx, my):
                    settings["sound"] = not settings["sound"]
 
                for i, (col, _) in enumerate(COLORS):
                    btn = pygame.Rect(W//2 - 220 + i * 90, 300, 80, 36)
                    if btn.collidepoint(mx, my):
                        settings["snake_color"] = col
 
        screen.fill(DARK)
        t = font_big.render("Settings", True, YELLOW)
        screen.blit(t, (W//2 - t.get_width()//2, 80))
 
        screen.blit(font_med.render("Grid:", True, WHITE), (W//2 - 180, 168))
        grid_btn = pygame.Rect(W//2 + 20, 160, 120, 36)
        pygame.draw.rect(screen, BLUE if settings["grid"] else DGRAY, grid_btn, border_radius=6)
        pygame.draw.rect(screen, WHITE, grid_btn, 2, border_radius=6)
        gl = font_med.render("ON" if settings["grid"] else "OFF", True, WHITE)
        screen.blit(gl, (grid_btn.centerx - gl.get_width()//2, grid_btn.centery - gl.get_height()//2))
 
        screen.blit(font_med.render("Sound:", True, WHITE), (W//2 - 180, 224))
        sound_btn = pygame.Rect(W//2 + 20, 216, 120, 36)
        pygame.draw.rect(screen, BLUE if settings["sound"] else DGRAY, sound_btn, border_radius=6)
        pygame.draw.rect(screen, WHITE, sound_btn, 2, border_radius=6)
        sl = font_med.render("ON" if settings["sound"] else "OFF", True, WHITE)
        screen.blit(sl, (sound_btn.centerx - sl.get_width()//2, sound_btn.centery - sl.get_height()//2))
 
        screen.blit(font_med.render("Snake color:", True, WHITE), (W//2 - 220, 268))
        for i, (col, lbl) in enumerate(COLORS):
            btn = pygame.Rect(W//2 - 220 + i * 90, 300, 80, 36)
            pygame.draw.rect(screen, tuple(col), btn, border_radius=6)
            active = settings["snake_color"] == col
            pygame.draw.rect(screen, WHITE if active else DGRAY, btn, 3 if active else 1, border_radius=6)
 
        draw_button("Save & Back", back_btn, font_med, back_btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def game_over_screen(score, level, personal_best):
    font_big = pygame.font.SysFont("Arial", 42, bold=True)
    font_med = pygame.font.SysFont("Arial", 24)
    retry_btn = pygame.Rect(W//2 - 140, 380, 130, 50)
    menu_btn  = pygame.Rect(W//2 + 10,  380, 130, 50)
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.collidepoint(mx, my):
                    return "retry"
                if menu_btn.collidepoint(mx, my):
                    return "menu"
 
        screen.fill(DARK)
        t = font_big.render("GAME OVER", True, RED)
        screen.blit(t, (W//2 - t.get_width()//2, 180))
 
        for i, line in enumerate([
            f"Score:        {score}",
            f"Level:        {level}",
            f"Personal best: {personal_best}",
        ]):
            s = font_med.render(line, True, WHITE)
            screen.blit(s, (W//2 - s.get_width()//2, 260 + i * 36))
 
        draw_button("Retry",     retry_btn, font_med, retry_btn.collidepoint(mx, my))
        draw_button("Main Menu", menu_btn,  font_med, menu_btn.collidepoint(mx, my))
        pygame.display.flip()
        clock.tick(60)
 
 
def run_game(settings, player_id, username, personal_best):
    game = SnakeGame(settings, username, personal_best)
    tick_acc = 0
 
    while True:
        dt = clock.tick(60)
        tick_acc += dt
 
        step_ms = 1000 // game.speed
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP,    pygame.K_w): game.set_direction((0, -1))
                if event.key in (pygame.K_DOWN,  pygame.K_s): game.set_direction((0,  1))
                if event.key in (pygame.K_LEFT,  pygame.K_a): game.set_direction((-1, 0))
                if event.key in (pygame.K_RIGHT, pygame.K_d): game.set_direction((1,  0))
 
        if tick_acc >= step_ms:
            tick_acc = 0
            game.step()
 
        game.draw(screen)
        pygame.display.flip()
 
        if game.dead:
            save_session(player_id, game.score, game.level)
            new_best = max(personal_best, game.score)
            result = game_over_screen(game.score, game.level, new_best)
            if result == "retry":
                game.reset()
                tick_acc = 0
                personal_best = new_best
                game.personal_best = personal_best
            else:
                return
 
 
def main():
    try:
        init_db()
    except Exception as e:
        print(f"DB connection failed: {e}\nRunning without DB.")
 
    settings = load_settings()
 
    while True:
        action = main_menu()
 
        if action == "Play":
            username = get_username_screen()
            try:
                player_id = get_or_create_player(username)
                personal_best = get_personal_best(player_id)
            except Exception:
                player_id = None
                personal_best = 0
            run_game(settings, player_id, username, personal_best)
 
        elif action == "Leaderboard":
            leaderboard_screen()
 
        elif action == "Settings":
            settings_screen(settings)
 
        elif action == "Quit":
            pygame.quit()
            sys.exit()
 
 
if __name__ == "__main__":
    main()
    