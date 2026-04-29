import pygame
import random
import time
 
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
GRAY   = (160, 160, 160)
DGRAY  = (60,  60,  60)
GREEN  = (50,  200, 80)
RED    = (220, 60,  60)
YELLOW = (240, 200, 0)
ORANGE = (240, 140, 0)
BLUE   = (60,  120, 220)
DARK   = (20,  20,  30)
ROAD   = (50,  50,  60)
LANE_LINE = (200, 200, 0)
NITRO_C  = (0,   220, 255)
SHIELD_C = (100, 100, 255)
REPAIR_C = (50,  220, 100)
 
COLOR_MAP = {
    "red":    (220, 50,  50),
    "blue":   (50,  100, 220),
    "green":  (50,  180, 50),
    "yellow": (220, 200, 0),
    "white":  (240, 240, 240),
}
 
LANES = 5
ROAD_LEFT  = 100
ROAD_RIGHT = 700
LANE_W = (ROAD_RIGHT - ROAD_LEFT) // LANES
 
DIFFICULTY_CONFIG = {
    "easy":   {"traffic_rate": 0.008, "obstacle_rate": 0.005, "base_speed": 4},
    "normal": {"traffic_rate": 0.015, "obstacle_rate": 0.010, "base_speed": 6},
    "hard":   {"traffic_rate": 0.025, "obstacle_rate": 0.018, "base_speed": 9},
}
 
 
def lane_x(lane):
    return ROAD_LEFT + lane * LANE_W + LANE_W // 2
 
 
class Player:
    W, H = 40, 70
 
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.shield = False
        self.nitro   = False
        self.nitro_end = 0
        self.shield_active = False
 
    def draw(self, screen):
        c = self.color
        pygame.draw.rect(screen, c, (self.x - self.W//2, self.y - self.H//2, self.W, self.H), border_radius=6)
        pygame.draw.rect(screen, WHITE, (self.x - 14, self.y - 28, 28, 18), border_radius=3)
        pygame.draw.rect(screen, DGRAY, (self.x - 18, self.y + 22, 14, 10), border_radius=3)
        pygame.draw.rect(screen, DGRAY, (self.x + 4,  self.y + 22, 14, 10), border_radius=3)
        if self.shield_active:
            pygame.draw.circle(screen, SHIELD_C, (self.x, self.y), 44, 3)
 
    def rect(self):
        return pygame.Rect(self.x - self.W//2, self.y - self.H//2, self.W, self.H)
 
 
class TrafficCar:
    W, H = 40, 65
    COLORS = [(180,40,40),(40,80,180),(40,160,40),(180,120,0),(120,0,160)]
 
    def __init__(self, lane, speed, H_screen):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = -self.H
        self.speed = speed
        self.color = random.choice(self.COLORS)
        self.H_screen = H_screen
 
    def update(self):
        self.y += self.speed
 
    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x - self.W//2, self.y - self.H//2, self.W, self.H), border_radius=5)
        pygame.draw.rect(screen, (180,220,255),
                         (self.x - 13, self.y - 24, 26, 16), border_radius=3)
        pygame.draw.rect(screen, DGRAY,
                         (self.x - 17, self.y + 20, 13, 10), border_radius=3)
        pygame.draw.rect(screen, DGRAY,
                         (self.x + 4,  self.y + 20, 13, 10), border_radius=3)
 
    def rect(self):
        return pygame.Rect(self.x - self.W//2, self.y - self.H//2, self.W, self.H)
 
    def off_screen(self):
        return self.y > self.H_screen + self.H
 
 
class Obstacle:
    TYPES = ["oil", "pothole", "barrier", "nitro_strip"]
 
    def __init__(self, lane, speed, H_screen):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = -30
        self.speed = speed
        self.type = random.choice(self.TYPES)
        self.H_screen = H_screen
        self.w = LANE_W - 10
        self.h = 22
 
    def update(self):
        self.y += self.speed
 
    def draw(self, screen):
        if self.type == "oil":
            pygame.draw.ellipse(screen, (20, 20, 80),
                                (self.x - self.w//2, self.y - 12, self.w, 24))
            t = pygame.font.SysFont("Arial", 11).render("OIL", True, WHITE)
            screen.blit(t, (self.x - t.get_width()//2, self.y - 8))
        elif self.type == "pothole":
            pygame.draw.ellipse(screen, (30, 25, 20),
                                (self.x - self.w//2, self.y - 10, self.w, 20))
            t = pygame.font.SysFont("Arial", 11).render("HOLE", True, GRAY)
            screen.blit(t, (self.x - t.get_width()//2, self.y - 7))
        elif self.type == "barrier":
            pygame.draw.rect(screen, ORANGE,
                             (self.x - self.w//2, self.y - 12, self.w, 24), border_radius=4)
            t = pygame.font.SysFont("Arial", 11).render("STOP", True, BLACK)
            screen.blit(t, (self.x - t.get_width()//2, self.y - 7))
        elif self.type == "nitro_strip":
            pygame.draw.rect(screen, NITRO_C,
                             (self.x - self.w//2, self.y - 10, self.w, 20), border_radius=4)
            t = pygame.font.SysFont("Arial", 11).render("NITRO", True, BLACK)
            screen.blit(t, (self.x - t.get_width()//2, self.y - 7))
 
    def rect(self):
        return pygame.Rect(self.x - self.w//2, self.y - 12, self.w, 24)
 
    def off_screen(self):
        return self.y > self.H_screen + 40
 
 
class Coin:
    def __init__(self, lane, speed, H_screen, value=1):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = -20
        self.speed = speed
        self.value = value
        self.H_screen = H_screen
        self.r = 14
 
    def update(self):
        self.y += self.speed
 
    def draw(self, screen):
        color = YELLOW if self.value == 1 else (200, 200, 200) if self.value == 2 else (200, 160, 50)
        pygame.draw.circle(screen, color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)
        t = pygame.font.SysFont("Arial", 11, bold=True).render(str(self.value), True, BLACK)
        screen.blit(t, (self.x - t.get_width()//2, self.y - t.get_height()//2))
 
    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r*2, self.r*2)
 
    def off_screen(self):
        return self.y > self.H_screen + 30
 
 
class PowerUp:
    TYPES = ["nitro", "shield", "repair"]
 
    def __init__(self, lane, speed, H_screen):
        self.lane = lane
        self.x = lane_x(lane)
        self.y = -30
        self.speed = speed
        self.type = random.choice(self.TYPES)
        self.H_screen = H_screen
        self.r = 18
        self.spawn_time = time.time()
        self.lifetime = 8
 
    def update(self):
        self.y += self.speed
 
    def expired(self):
        return time.time() - self.spawn_time > self.lifetime
 
    def draw(self, screen):
        color = NITRO_C if self.type == "nitro" else SHIELD_C if self.type == "shield" else REPAIR_C
        pygame.draw.circle(screen, color, (self.x, self.y), self.r)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), self.r, 2)
        label = {"nitro": "N", "shield": "S", "repair": "R"}[self.type]
        t = pygame.font.SysFont("Arial", 14, bold=True).render(label, True, BLACK)
        screen.blit(t, (self.x - t.get_width()//2, self.y - t.get_height()//2))
 
    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r*2, self.r*2)
 
    def off_screen(self):
        return self.y > self.H_screen + 40
 
 
class RacerGame:
    def __init__(self, W, H, settings, username):
        self.W = W
        self.H = H
        self.settings = settings
        self.username = username
        self.cfg = DIFFICULTY_CONFIG[settings["difficulty"]]
        self.reset()
 
    def reset(self):
        cfg = self.cfg
        self.player = Player(
            lane_x(LANES // 2), self.H - 120,
            COLOR_MAP[self.settings["car_color"]]
        )
        self.base_speed   = cfg["base_speed"]
        self.road_speed   = self.base_speed
        self.score        = 0
        self.coins_count  = 0
        self.distance     = 0
        self.road_offset  = 0
        self.traffic      = []
        self.obstacles    = []
        self.coins        = []
        self.powerups     = []
        self.active_powerup     = None
        self.active_powerup_end = 0
        self.nitro_speed_bonus  = 0
        self.game_over    = False
        self.current_lane = LANES // 2
 
    def _cur_speed(self):
        return self.road_speed + self.nitro_speed_bonus
 
    def update(self, dt):
        if self.game_over:
            return
 
        self.distance += self._cur_speed() * 0.05
        self.score = int(self.distance * 0.5 + self.coins_count * 10)
 
        level = int(self.distance / 300)
        self.road_speed = self.base_speed + level * 0.5
 
        if self.active_powerup == "nitro" and time.time() > self.active_powerup_end:
            self.active_powerup = None
            self.nitro_speed_bonus = 0
 
        self.road_offset = (self.road_offset + self._cur_speed()) % 60
 
        if random.random() < self.cfg["traffic_rate"] + level * 0.001:
            lane = random.randint(0, LANES - 1)
            if lane != self.current_lane:
                self.traffic.append(TrafficCar(lane, self._cur_speed() * 0.6, self.H))
 
        if random.random() < self.cfg["obstacle_rate"] + level * 0.001:
            lane = random.randint(0, LANES - 1)
            self.obstacles.append(Obstacle(lane, self._cur_speed(), self.H))
 
        if random.random() < 0.012:
            lane = random.randint(0, LANES - 1)
            value = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
            self.coins.append(Coin(lane, self._cur_speed(), self.H, value))
 
        if random.random() < 0.005 and not self.powerups:
            lane = random.randint(0, LANES - 1)
            self.powerups.append(PowerUp(lane, self._cur_speed(), self.H))
 
        for obj in self.traffic + self.obstacles + self.coins + self.powerups:
            obj.update()
 
        pr = self.player.rect()
 
        for t in self.traffic[:]:
            if t.rect().colliderect(pr):
                if self.active_powerup == "shield":
                    self.active_powerup = None
                    self.traffic.remove(t)
                else:
                    self.game_over = True
                    return
            elif t.off_screen():
                self.traffic.remove(t)
 
        for ob in self.obstacles[:]:
            if ob.rect().colliderect(pr):
                if ob.type == "nitro_strip":
                    self._activate_powerup("nitro")
                    self.obstacles.remove(ob)
                elif self.active_powerup == "repair":
                    self.active_powerup = None
                    self.obstacles.remove(ob)
                elif self.active_powerup == "shield":
                    self.active_powerup = None
                    self.obstacles.remove(ob)
                else:
                    self.game_over = True
                    return
            elif ob.off_screen():
                self.obstacles.remove(ob)
 
        for c in self.coins[:]:
            if c.rect().colliderect(pr):
                self.coins_count += c.value
                self.score += c.value * 10
                self.coins.remove(c)
            elif c.off_screen():
                self.coins.remove(c)
 
        for p in self.powerups[:]:
            if p.rect().colliderect(pr):
                self._activate_powerup(p.type)
                self.powerups.remove(p)
            elif p.off_screen() or p.expired():
                self.powerups.remove(p)
 
    def _activate_powerup(self, ptype):
        self.active_powerup = ptype
        if ptype == "nitro":
            self.nitro_speed_bonus = 4
            self.active_powerup_end = time.time() + 4
        elif ptype == "shield":
            self.active_powerup_end = time.time() + 9999
        elif ptype == "repair":
            self.active_powerup_end = time.time() + 9999
 
    def move_player(self, direction):
        new_lane = self.current_lane + direction
        if 0 <= new_lane < LANES:
            self.current_lane = new_lane
            self.player.x = lane_x(new_lane)
 
    def draw(self, screen):
        screen.fill(DARK)
 
        pygame.draw.rect(screen, ROAD, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, self.H))
 
        for lane in range(1, LANES):
            x = ROAD_LEFT + lane * LANE_W
            for y in range(-60 + int(self.road_offset), self.H + 60, 60):
                pygame.draw.line(screen, LANE_LINE, (x, y), (x, y + 30), 2)
 
        pygame.draw.rect(screen, GRAY, (0, 0, ROAD_LEFT, self.H))
        pygame.draw.rect(screen, GRAY, (ROAD_RIGHT, 0, self.W - ROAD_RIGHT, self.H))
 
        for obj in self.coins + self.obstacles + self.traffic + self.powerups:
            obj.draw(screen)
 
        self.player.shield_active = (self.active_powerup == "shield")
        self.player.draw(screen)
 
        self._draw_hud(screen)
 
    def _draw_hud(self, screen):
        font = pygame.font.SysFont("Arial", 20, bold=True)
        font_sm = pygame.font.SysFont("Arial", 16)
 
        lines = [
            f"Score:    {self.score}",
            f"Distance: {int(self.distance)} m",
            f"Coins:    {self.coins_count}",
            f"Speed:    {int(self._cur_speed())}",
        ]
        for i, line in enumerate(lines):
            t = font.render(line, True, WHITE)
            screen.blit(t, (self.W - 220, 15 + i * 28))
 
        if self.active_powerup:
            remaining = max(0, int(self.active_powerup_end - time.time()))
            color = NITRO_C if self.active_powerup == "nitro" else SHIELD_C if self.active_powerup == "shield" else REPAIR_C
            label = f"[{self.active_powerup.upper()}]" + (f" {remaining}s" if self.active_powerup == "nitro" else " ACTIVE")
            t = font.render(label, True, color)
            screen.blit(t, (self.W // 2 - t.get_width() // 2, 12))
 
        hint = font_sm.render("← → to steer", True, GRAY)
        screen.blit(hint, (10, self.H - 28))
 