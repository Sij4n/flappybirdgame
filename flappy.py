import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 235)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 20
    
    def flap(self):
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(screen, BLACK, (int(self.x + 8), int(self.y - 5)), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, HEIGHT - 150 - PIPE_GAP)
        self.passed = False
    
    def update(self):
        self.x -= PIPE_SPEED
    
    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, 0, PIPE_WIDTH, self.height), 3)
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, 
                                        PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))
        pygame.draw.rect(screen, BLACK, (self.x, self.height + PIPE_GAP, 
                                        PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP), 3)
    
    def collides(self, bird):
        bird_rect = bird.get_rect()
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 
                                  PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)
    
    def off_screen(self):
        return self.x + PIPE_WIDTH < 0

def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

def game_loop():
    bird = Bird()
    pipes = [Pipe(WIDTH + 200)]
    score = 0
    game_over = False
    
    while True:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_over:
                        bird.flap()
                    else:
                        return  # Restart game
        
        if not game_over:
            # Update bird
            bird.update()
            
            # Check if bird hit ground or ceiling
            if bird.y + bird.radius > HEIGHT or bird.y - bird.radius < 0:
                game_over = True
            
            # Update pipes
            for pipe in pipes:
                pipe.update()
                
                # Check collision
                if pipe.collides(bird):
                    game_over = True
                
                # Increase score
                if not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1
            
            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if not pipe.off_screen()]
            
            # Add new pipes
            if len(pipes) == 0 or pipes[-1].x < WIDTH - 250:
                pipes.append(Pipe(WIDTH))
        
        # Draw everything
        screen.fill(BLUE)
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw()
        
        # Draw bird
        bird.draw()
        
        # Draw score
        draw_text(str(score), font, WHITE, WIDTH // 2, 50)
        
        # Draw game over
        if game_over:
            draw_text("GAME OVER", font, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Score: {score}", small_font, WHITE, WIDTH // 2, HEIGHT // 2)
            draw_text("Press SPACE to restart", small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        
        pygame.display.flip()

# Main game loop
while True:
    game_loop()