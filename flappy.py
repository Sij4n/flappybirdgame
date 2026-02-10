"""
Flappy Bird Game
A simple implementation of the popular Flappy Bird game using Pygame.
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# ==================== GAME CONSTANTS ====================
# Screen dimensions
WIDTH, HEIGHT = 400, 600

# Physics
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Pipe settings
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_SPAWN_DISTANCE = 250

# Bird settings
BIRD_RADIUS = 20
BIRD_START_X = 80

# ==================== COLORS ====================
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

# High score tracking
HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    """Load high score from file."""
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    """Save high score to file."""
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

class Bird:
    """Represents the player bird in the game."""
    
    def __init__(self):
        self.x = BIRD_START_X
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = BIRD_RADIUS
    
    def flap(self):
        """Make the bird flap (jump)."""
        self.velocity = FLAP_STRENGTH
    
    def update(self):
        """Update bird position and velocity."""
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self, surface):
        """Draw the bird with eyes."""
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(surface, BLACK, (int(self.x + 8), int(self.y - 5)), 3)
    
    def get_rect(self):
        """Return the bird's collision rectangle."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    """Represents a pipe obstacle in the game."""
    
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, HEIGHT - 150 - PIPE_GAP)
        self.passed = False
    
    def update(self):
        """Update pipe position."""
        self.x -= PIPE_SPEED
    
    def draw(self, surface):
        """Draw the pipe with borders."""
        # Top pipe
        pygame.draw.rect(surface, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(surface, BLACK, (self.x, 0, PIPE_WIDTH, self.height), 3)
        # Bottom pipe
        pygame.draw.rect(surface, GREEN, (self.x, self.height + PIPE_GAP, 
                                        PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))
        pygame.draw.rect(surface, BLACK, (self.x, self.height + PIPE_GAP, 
                                        PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP), 3)
    
    def collides(self, bird):
        """Check if pipe collides with bird."""
        bird_rect = bird.get_rect()
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 
                                  PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
        return bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe)
    
    def off_screen(self):
        """Check if pipe has moved off the left side of the screen."""
        return self.x + PIPE_WIDTH < 0

def draw_text(surface, text, font, color, x, y, center=True):
    """Render and display text on the screen."""
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(text_surface, rect)

def game_loop(screen, high_score):
    """Main game loop."""
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
                        return max(score, high_score)  # Return updated high score
        
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
            if len(pipes) == 0 or pipes[-1].x < WIDTH - PIPE_SPAWN_DISTANCE:
                pipes.append(Pipe(WIDTH))
        
        # Draw everything
        screen.fill(BLUE)
        
        # Draw pipes
        for pipe in pipes:
            pipe.draw(screen)
        
        # Draw bird
        bird.draw(screen)
        
        # Draw score
        draw_text(screen, str(score), font, WHITE, WIDTH // 2, 50)
        
        # Draw high score
        draw_text(screen, f"Best: {high_score}", small_font, WHITE, WIDTH // 2, 100)
        
        # Draw game over
        if game_over:
            draw_text(screen, "GAME OVER", font, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(screen, f"Score: {score}", small_font, WHITE, WIDTH // 2, HEIGHT // 2)
            draw_text(screen, "Press SPACE to restart", small_font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        
        pygame.display.flip()

# Main game loop
if __name__ == "__main__":
    high_score = load_high_score()
    while True:
        high_score = game_loop(screen, high_score)
        save_high_score(high_score)