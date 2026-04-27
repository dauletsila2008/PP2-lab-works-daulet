import pygame
import random
import time

# Түстер палитрасы (егер color_palette файлы болмаса, осы жерде анықталған)
colorBLUE = (0, 0, 255)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorYELLOW = (255, 255, 0)
colorGRAY = (50, 50, 50)
colorWHITE = (255, 255, 255)

pygame.init()

# Экран параметрлері
WIDTH, HEIGHT = 600, 600
CELL = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Practice 11")

FPS = 5
clock = pygame.time.Clock()

score = 0
level = 1

def draw_grid():
    for i in range(0, WIDTH, CELL):
        pygame.draw.line(screen, colorGRAY, (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, colorGRAY, (0, i), (WIDTH, i))

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx, self.dy = 1, 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        for i, segment in enumerate(self.body):
            color = colorRED if i == 0 else colorYELLOW
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        head = self.body[0]
        return head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL

    def check_self_collision(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

class Food:
    def __init__(self):
        self.generate_random_pos([])
        
    def generate_random_pos(self, snake_body):
        # 1. Тамақтың салмағын кездейсоқ анықтау (1-ден 3-ке дейін)
        self.weight = random.randint(1, 3)
        # Тамақтың пайда болған уақытын сақтау
        self.spawn_time = pygame.time.get_ticks() 
        
        while True:
            self.pos = Point(random.randint(0, WIDTH // CELL - 1), random.randint(0, HEIGHT // CELL - 1))
            if all(segment.x != self.pos.x or segment.y != self.pos.y for segment in snake_body):
                break

    def draw(self):
        # Салмағына қарай түсін өзгерту (мысалы, ауыр тамақ қоюырақ)
        color = (0, 255 - (self.weight * 50), 0) if self.weight > 1 else colorGREEN
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def check_timer(self, snake_body):
        # 2. Тамақ 5 секундтан (5000 мс) кейін жоғалып, басқа жерде пайда болады
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > 5000:
            self.generate_random_pos(snake_body)

# Ойын нысандары
snake = Snake()
food = Food()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    screen.fill((0, 0, 50))
    draw_grid()
    
    snake.move()
    
    # Қабырғаға немесе өзіне соғылуды тексеру
    if snake.check_wall_collision() or snake.check_self_collision():
        running = False

    # Тамақтың уақытын тексеру
    food.check_timer(snake.body)

    # Тамақты жеуді тексеру
    head = snake.body[0]
    if head.x == food.pos.x and head.y == food.pos.y:
        score += food.weight
        # Салмағына қарай денесін ұзарту
        for _ in range(food.weight):
            snake.body.append(Point(head.x, head.y))
        
        # Деңгей жүйесі (әр 5 ұпай сайын жылдамдық артады)
        if score // 5 >= level:
            level += 1
            FPS += 1
            
        food.generate_random_pos(snake.body)

    snake.draw()
    food.draw()

    # Ақпаратты шығару
    font = pygame.font.SysFont("Verdana", 20)
    info = font.render(f"Score: {score}  Level: {level}  Weight: {food.weight}", True, colorWHITE)
    screen.blit(info, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()