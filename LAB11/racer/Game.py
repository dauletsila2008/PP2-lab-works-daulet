import pygame, sys
from pygame.locals import *
import random, time

# Инициализация
pygame.init()

# FPS баптау
FPS = 60
FramePerSec = pygame.time.Clock()

# Түстер
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

# Негізгі айнымалылар
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0          # Жалпы жиналған ұпай (салмағына қарай)
COINS_COUNT = 0    # Жиналған тиындардың нақты саны (жылдамдық үшін)

# Қаріптер
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Фон және экран
background = pygame.image.load("AnimatedStreet.png")
DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Practice 11")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 1. Түрлі салмақтағы тиындарды генерациялау
        self.weight = random.choice([1, 5]) # 1 немесе 5 ұпай
        if self.weight == 5:
            # Алтын тиын сәл үлкенірек және сары түсті болады (немесе басқа сурет)
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 215, 0)) # Gold түсі
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((192, 192, 192)) # Silver түсі
            
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        self.rect.move_ip(0, 5) # Тиынның тұрақты жылдамдығы
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

    def reset(self):
        self.weight = random.choice([1, 5])
        if self.weight == 5:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 215, 0))
        else:
            self.image = pygame.Surface((20, 20))
            self.image.fill((192, 192, 192))
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

# Спрайттарды дайындау
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Ойын циклі
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0,0))
    
    # Статистиканы шығару
    scores_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    speed_text = font_small.render(f"Speed: {SPEED}", True, BLACK)
    DISPLAYSURF.blit(scores_text, (10, 10))
    DISPLAYSURF.blit(speed_text, (10, 30))

    # Спрайттарды жылжыту және суреттеу
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Ойыншы тиын жинағанда
    coin_hit = pygame.sprite.spritecollideany(P1, coins)
    if coin_hit:
        SCORE += coin_hit.weight # Салмағына қарай ұпай қосу
        COINS_COUNT += 1         # Тиын санын санау
        
        # 2. Әр 10 тиын сайын Enemy жылдамдығын арттыру
        if COINS_COUNT % 10 == 0:
            SPEED += 1
            
        coin_hit.reset() # Тиынды қайтадан жоғарыға жіберу

    # Ойыншы Enemy-мен соқтығысқанда
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)