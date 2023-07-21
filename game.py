import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Monster Shooter")
background_image = pygame.transform.scale(pygame.image.load("img.png"), (1200, 800))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255,125,0)


# Button class
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GREEN
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 40)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()


# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets, up_key, down_key, left_key, right_key, shoot_key):
        super().__init__()
        #self.image = pygame.Surface((60, 60))
        self.image = pygame.transform.scale(pygame.image.load("tank.png"), (100, 100))
        #self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(x, y))
        self.bullets = bullets
        self.speed = 5
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key
        self.shoot_key = shoot_key
        self.shoot_delay = 300  # Delay between shots (in milliseconds)
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_power = 1

    def update(self):
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[self.up_key]:
            self.rect.y -= self.speed
        if keys[self.down_key]:
            self.rect.y += self.speed
        if keys[self.left_key]:
            self.rect.x -= self.speed
        if keys[self.right_key]:
            self.rect.x += self.speed

        # Limit player movement within the screen boundaries
        self.rect.clamp_ip(screen.get_rect())

        # Shoot bullets
        if keys[self.shoot_key]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shoot_delay:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        for i in range(self.shoot_power):
            bullet = Bullet(
                self.rect.centerx + i * 10, self.rect.top, ORANGE, self.shoot_power
            )
            self.bullets.add(bullet)


# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, power):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 10
        self.power = power

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# Monster class
class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.image = pygame.Surface((40, 40))
        self.image = pygame.transform.scale(pygame.image.load("alien.png"), (60, 60))
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect(
            center=(random.randint(40, screen_width - 40), 0)
        )
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = 0
            self.rect.centerx = random.randint(40, screen_width - 40)


# Bonus class
class Bonus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.circle_radius = 10
        self.image = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (self.circle_radius, self.circle_radius), self.circle_radius)
        self.rect = self.image.get_rect(
            center=(random.randint(40, screen_width - 40), 0)
        )
        self.speed = 3

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.rect.y = 0
            self.rect.centerx = random.randint(40, screen_width - 40)


# Function to create players based on the selected number of players
def create_players(num_players):
    players = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()

    if num_players >= 1:
        player1 = Player(
            screen_width // 4,
            screen_height - 50,
            player_bullets,
            pygame.K_w,
            pygame.K_s,
            pygame.K_a,
            pygame.K_d,
            pygame.K_SPACE,
        )
        players.add(player1)
    if num_players >= 2:
        player2 = Player(
            screen_width // 4 * 3,
            screen_height - 50,
            player_bullets,
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_KP_0,
        )
        players.add(player2)

    return players, player_bullets


# Function to start the game with the selected number of players
def start_game(num_players):
    players, player_bullets = create_players(num_players)
    monsters = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    level = 1
    score = 0

    for _ in range(level * 10):
        monster = Monster()
        monsters.add(monster)

    clock = pygame.time.Clock()
    game_over = False
    next_level = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        players.update()
        player_bullets.update()
        monsters.update()
        bonuses.update()

        # Check collision between bullets and monsters
        for bullet in player_bullets:
            if pygame.sprite.spritecollide(bullet, monsters, True):
                bullet.kill()
                score += 1

        # Check collision between players and monsters
        for player in players:
            if pygame.sprite.spritecollide(player, monsters, False):
                game_over = True

        # Check collision between players and bonuses
        for player in players:
            if pygame.sprite.spritecollide(player, bonuses, True):
                player.shoot_power += 1

        # Level up if all monsters are defeated
        if not monsters:
            next_level = True

        # Spawn bonuses randomly
        if random.randint(0, 1000) < 3:
            bonus = Bonus()
            bonuses.add(bonus)

        #screen.fill(background_image)
        screen.blit(background_image, (0, 0))
        players.draw(screen)
        player_bullets.draw(screen)
        monsters.draw(screen)
        bonuses.draw(screen)

        # Display score
        score_font = pygame.font.Font(None, 36)
        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Display level
        level_font = pygame.font.Font(None, 36)
        level_text = level_font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

        # Show game summary before moving to the next level
        if next_level:
            game_over = show_summary(score, level)
            level += 1
            next_level = False
            score = 0
            players, player_bullets = create_players(num_players)
            monsters.empty()

            for _ in range(level * 10):
                monster = Monster()
                monsters.add(monster)

    # Game over screen
    game_over_font = pygame.font.Font(None, 80)
    game_over_text = game_over_font.render("Game Over", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))

    restart_button = Button(
        screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, "Restart", lambda: start_menu()
    )
    buttons = [restart_button]

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        screen.fill(BLACK)
        screen.blit(game_over_text, game_over_rect)
        for button in buttons:
            button.draw()

        pygame.display.flip()
        clock.tick(60)


# Function to show game summary before moving to the next level
def show_summary(score, level):
    screen.fill(BLACK)

    summary_font = pygame.font.Font(None, 60)
    summary_text = summary_font.render("Level Complete!", True, WHITE)
    summary_rect = summary_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    score_font = pygame.font.Font(None, 40)
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

    next_button = Button(
        screen_width // 2 - 100, screen_height // 2 + 100, 200, 50, "Next Level", lambda: None
    )
    buttons = [next_button]

    while True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in buttons:
                button.handle_event(event)

        screen.blit(summary_text, summary_rect)
        screen.blit(score_text, score_rect)
        for button in buttons:
            button.draw()

        pygame.display.flip()
        clock.tick(60)

        if next_button.action:
            return False


# Function to start the menu screen
def start_menu():
    screen.fill(BLACK)

    start_buttons = [
        Button(100, 200, 200, 100, "1 Player", lambda: start_game(1)),
        Button(500, 200, 200, 100, "2 Players", lambda: start_game(2)),
    ]

    for button in start_buttons:
        button.draw()

    pygame.display.flip()

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for button in start_buttons:
                button.handle_event(event)
        clock.tick(60)


# Start the menu screen
start_menu()
