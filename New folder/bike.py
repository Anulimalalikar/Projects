import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bike Riding Game")

# Load images
bike_img = pygame.image.load('bike.png')  # Replace 'bike.png' with your bike image file

# Get image dimensions
bike_width = bike_img.get_width()
bike_height = bike_img.get_height()

# Initial position of the bike
bike_x = SCREEN_WIDTH // 2 - bike_width // 2
bike_y = SCREEN_HEIGHT - bike_height - 20

# Variables for obstacles
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 5
obstacles = []
obstacle_gap = 200
next_obstacle = 0

# Game loop
running = True
clock = pygame.time.Clock()
score = 0

def draw_bike(x, y):
    screen.blit(bike_img, (x, y))

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        pygame.draw.rect(screen, RED, obstacle)

def detect_collision(bike_x, bike_y, obstacles):
    bike_rect = pygame.Rect(bike_x, bike_y, bike_width, bike_height)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], obstacle_width, obstacle_height)
        if bike_rect.colliderect(obstacle_rect):
            return True
    return False

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the bike
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bike_x > 0:
        bike_x -= 5
    if keys[pygame.K_RIGHT] and bike_x < SCREEN_WIDTH - bike_width:
        bike_x += 5

    # Generate obstacles
    if next_obstacle <= 0:
        obstacle_x = random.randrange(0, SCREEN_WIDTH - obstacle_width)
        obstacle_y = -obstacle_height
        obstacles.append([obstacle_x, obstacle_y])
        next_obstacle = obstacle_gap + random.randrange(-30, 30)
    else:
        next_obstacle -= 1

    # Move obstacles
    for obstacle in obstacles:
        obstacle[1] += obstacle_speed

    # Remove obstacles that have passed the screen
    obstacles = [obstacle for obstacle in obstacles if obstacle[1] < SCREEN_HEIGHT]

    # Detect collisions
    if detect_collision(bike_x, bike_y, obstacles):
        running = False

    # Draw everything
    screen.fill(WHITE)
    draw_bike(bike_x, bike_y)
    draw_obstacles(obstacles)

    # Update score
    score += 1
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, RED)
    screen.blit(text, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over screen
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Game Over", True, RED)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
pygame.display.flip()

# Wait for a moment before closing the game
pygame.time.wait(2000)

# Quit Pygame
pygame.quit()