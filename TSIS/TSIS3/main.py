import pygame
import sys
from persistence import load_settings, save_score, load_leaderboard, save_settings
from ui import main_menu, settings_screen, leaderboard_screen, game_over_screen, get_username
from racer import RacerGame
 
pygame.init()
 
W, H = 900, 650
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Racer — TSIS3")
clock = pygame.time.Clock()
 
 
def run_game(settings, username):
    game = RacerGame(W, H, settings, username)
 
    while True:
        dt = clock.tick(60)
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_player(-1)
                elif event.key == pygame.K_RIGHT:
                    game.move_player(1)
 
        if not game.game_over:
            game.update(dt)
            game.draw(screen)
            pygame.display.flip()
        else:
            save_score(username, game.score, game.distance, game.coins_count)
            result = game_over_screen(screen, clock, W, H, game.score, game.distance, game.coins_count)
            if result == "retry":
                game.reset()
            else:
                return
 
 
def main():
    settings = load_settings()
 
    while True:
        action = main_menu(screen, clock, W, H)
 
        if action == "Play":
            username = get_username(screen, clock, W, H)
            run_game(settings, username)
 
        elif action == "Leaderboard":
            board = load_leaderboard()
            leaderboard_screen(screen, clock, W, H, board)
 
        elif action == "Settings":
            settings_screen(screen, clock, W, H, settings)
            save_settings(settings)
 
        elif action == "Quit":
            pygame.quit()
            sys.exit()
 
 
if __name__ == "__main__":
    main()
 