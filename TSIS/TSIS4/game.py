import pygame
import random
from config import *
 
 
def rand_cell(exclude=None):
    if exclude is None:
        exclude = set()
    while True:
        c = (random.randint(1, COLS - 2), random.randint(1, ROWS - 2))
        if c not in exclude:
            return c
 
 
class Food:
    def __init__(self, exclude, obstacles):
        blocked = set(exclude) | set(obstacles)
        self.pos = rand_cell(blocked)
        r = random.random()
        if r < 0.6:
            self.kind = "normal"; self.value = 1; self.color = GREEN
        elif r < 0.85:
            self.kind = "bonus";  self.value = 3; self.color = YELLOW
        else:
            self.kind = "super";  self.value = 5; self.color = ORANGE
        self.spawn = pygame.time.get_ticks()
        self.lifetime = 8000
 
    def expired(self):
        return pygame.time.get_ticks() - self.spawn > self.lifetime
 
 
class PoisonFood:
    def __init__(self, exclude, obstacles):
        blocked = set(exclude) | set(obstacles)
        self.pos = rand_cell(blocked)
        self.color = DRED
        self.spawn = pygame.time.get_ticks()
        self.lifetime = 6000
 
    def expired(self):
        return pygame.time.get_ticks() - self.spawn > self.lifetime
 
 
class PowerUp:
    TYPES = [
        ("speed",  CYAN,   "SPEED",  5000),
        ("slow",   PURPLE, "SLOW",   5000),
        ("shield", PINK,   "SHIELD", 0),
    ]
 
    def __init__(self, exclude, obstacles):
        blocked = set(exclude) | set(obstacles)
        self.pos = rand_cell(blocked)
        t = random.choice(self.TYPES)
        self.kind, self.color, self.label, self.duration = t
        self.spawn = pygame.time.get_ticks()
        self.field_lifetime = 8000
 
    def field_expired(self):
        return pygame.time.get_ticks() - self.spawn > self.field_lifetime
 
 
class SnakeGame:
    def __init__(self, settings, username, personal_best):
        self.settings = settings
        self.username = username
        self.personal_best = personal_best
        self.reset()
 
    def reset(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.next_dir = (1, 0)
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.obstacles = []
        self.food = None
        self.poison = None
        self.powerup = None
        self.active_effect = None
        self.effect_end = 0
        self.shield = False
        self.speed = FPS_BASE
        self.dead = False
        self._spawn_food()
        self._maybe_spawn_poison()
 
    def _blocked(self):
        return set(self.snake) | set(self.obstacles)
 
    def _spawn_food(self):
        self.food = Food(self._blocked(), self.obstacles)
 
    def _maybe_spawn_poison(self):
        if random.random() < 0.4:
            self.poison = PoisonFood(self._blocked() | ({self.food.pos} if self.food else set()), self.obstacles)
 
    def _spawn_powerup(self):
        if self.powerup is None and random.random() < 0.3:
            excl = self._blocked() | ({self.food.pos} if self.food else set())
            self.powerup = PowerUp(excl, self.obstacles)
 
    def _place_obstacles(self):
        count = 3 + self.level * 2
        head = self.snake[0]
        safe = {(head[0] + dx, head[1] + dy) for dx in range(-3, 4) for dy in range(-3, 4)}
        blocked = set(self.snake) | safe
        obs = []
        attempts = 0
        while len(obs) < count and attempts < 500:
            c = rand_cell(blocked | set(obs))
            obs.append(c)
            attempts += 1
        self.obstacles = obs
 
    def set_direction(self, d):
        if (d[0] + self.direction[0], d[1] + self.direction[1]) != (0, 0):
            self.next_dir = d
 
    def _apply_powerup(self, kind):
        self.active_effect = kind
        now = pygame.time.get_ticks()
        if kind == "speed":
            self.speed = FPS_BASE + 6
            self.effect_end = now + 5000
        elif kind == "slow":
            self.speed = max(2, FPS_BASE - 4)
            self.effect_end = now + 5000
        elif kind == "shield":
            self.shield = True
            self.effect_end = 0
 
    def _clear_effect(self):
        self.active_effect = None
        self.shield = False
        self.speed = FPS_BASE + (self.level - 1) * 1
 
    def step(self):
        if self.dead:
            return
 
        now = pygame.time.get_ticks()
 
        if self.active_effect in ("speed", "slow") and now > self.effect_end:
            self._clear_effect()
            self.speed = FPS_BASE + (self.level - 1)
 
        self.direction = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]
        new_head = (nx, ny)
 
        wall_hit = nx < 0 or ny < 0 or nx >= COLS or ny >= ROWS
        body_hit = new_head in self.snake[1:]
        obs_hit  = new_head in self.obstacles
 
        if wall_hit or body_hit or obs_hit:
            if self.shield:
                self.shield = False
                self.active_effect = None
                nx = max(1, min(COLS - 2, nx))
                ny = max(1, min(ROWS - 2, ny))
                new_head = (nx, ny)
                if new_head in self.snake[1:] or new_head in self.obstacles:
                    self.dead = True
                    return
            else:
                self.dead = True
                return
 
        self.snake.insert(0, new_head)
 
        ate = False
        if self.food and new_head == self.food.pos:
            self.score += self.food.value
            self.food_eaten += 1
            ate = True
            self._spawn_food()
            self._maybe_spawn_poison()
            self._spawn_powerup()
            if self.food_eaten % 5 == 0:
                self.level += 1
                self.speed = FPS_BASE + (self.level - 1)
                if self.level >= 3:
                    self._place_obstacles()
        elif self.poison and new_head == self.poison.pos:
            self.snake = self.snake[:-3] if len(self.snake) > 3 else self.snake[:1]
            self.poison = None
            if len(self.snake) <= 1:
                self.dead = True
                return
            ate = True
        elif self.powerup and new_head == self.powerup.pos:
            self._apply_powerup(self.powerup.kind)
            self.powerup = None
            ate = True
 
        if not ate:
            self.snake.pop()
 
        if self.food and self.food.expired():
            self._spawn_food()
        if self.poison and self.poison.expired():
            self.poison = None
        if self.powerup and self.powerup.field_expired():
            self.powerup = None
 
    def draw(self, screen):
        screen.fill(DARK)
 
        if self.settings.get("grid"):
            for x in range(0, W, CELL):
                pygame.draw.line(screen, (30, 30, 40), (x, 0), (x, ROWS * CELL))
            for y in range(0, ROWS * CELL, CELL):
                pygame.draw.line(screen, (30, 30, 40), (0, y), (W, y))
 
        pygame.draw.rect(screen, DGRAY, (0, 0, W, ROWS * CELL), 3)
 
        for obs in self.obstacles:
            r = pygame.Rect(obs[0]*CELL, obs[1]*CELL, CELL, CELL)
            pygame.draw.rect(screen, GRAY, r)
            pygame.draw.rect(screen, WHITE, r, 1)
 
        if self.food:
            r = pygame.Rect(self.food.pos[0]*CELL+2, self.food.pos[1]*CELL+2, CELL-4, CELL-4)
            pygame.draw.ellipse(screen, self.food.color, r)
 
        if self.poison:
            r = pygame.Rect(self.poison.pos[0]*CELL+2, self.poison.pos[1]*CELL+2, CELL-4, CELL-4)
            pygame.draw.ellipse(screen, DRED, r)
            pygame.draw.ellipse(screen, RED, r, 2)
 
        if self.powerup:
            r = pygame.Rect(self.powerup.pos[0]*CELL+1, self.powerup.pos[1]*CELL+1, CELL-2, CELL-2)
            pygame.draw.rect(screen, self.powerup.color, r, border_radius=4)
            f = pygame.font.SysFont("Arial", 9, bold=True)
            t = f.render(self.powerup.label[0], True, BLACK)
            screen.blit(t, (self.powerup.pos[0]*CELL + 5, self.powerup.pos[1]*CELL + 5))
 
        snake_color = tuple(self.settings.get("snake_color", [50, 200, 80]))
        for i, seg in enumerate(self.snake):
            r = pygame.Rect(seg[0]*CELL+1, seg[1]*CELL+1, CELL-2, CELL-2)
            c = snake_color if i > 0 else WHITE
            pygame.draw.rect(screen, c, r, border_radius=4)
            if self.shield and i == 0:
                pygame.draw.rect(screen, PINK, r, 2, border_radius=4)
 
        hud_y = ROWS * CELL + 8
        font = pygame.font.SysFont("Arial", 18, bold=True)
        font_sm = pygame.font.SysFont("Arial", 14)
 
        screen.blit(font.render(f"Score: {self.score}", True, WHITE), (10, hud_y))
        screen.blit(font.render(f"Level: {self.level}", True, YELLOW), (160, hud_y))
        screen.blit(font_sm.render(f"Best: {self.personal_best}", True, GRAY), (280, hud_y + 2))
        screen.blit(font_sm.render(f"{self.username}", True, CYAN), (400, hud_y + 2))
 
        if self.active_effect:
            now = pygame.time.get_ticks()
            if self.active_effect == "shield":
                label = "SHIELD"
            else:
                rem = max(0, (self.effect_end - now) // 1000)
                label = f"{self.active_effect.upper()} {rem}s"
            color = CYAN if self.active_effect == "speed" else PURPLE if self.active_effect == "slow" else PINK
            screen.blit(font.render(label, True, color), (520, hud_y))
 