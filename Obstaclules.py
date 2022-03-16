# Import the pygame module
import pygame

# Import random for random numbers
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("image/sprite.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("image/Dark VFX 2 (48x64)6.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)
        
    # move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#Define the background object by extewnding pygame.sprite.Sprite
# Use an image for a better-looking sprite
class Stars(pygame.sprite.Sprite):
    def __init__(self):
        super(Stars, self).__init__()
        self.surf = pygame.image.load("image/stars.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    
    # Move the stars based on a constant speed
    # Remove the stars when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Initialize pygame
pygame.init()

# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Display name
icon = pygame.image.load("image/icon.png")
pygame.display.set_icon(icon)

# Set caption
pygame.display.set_caption("Into the Void")

# Set a background image
#bg = pygame.image.load("image/background.png")
#bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDSTARS = pygame.USEREVENT + 2
pygame.time.set_timer(ADDSTARS, 1000)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# -enemies is used for collision detection and position updates
# all_sprites is used for rendering
enemies = pygame.sprite.Group()
stars = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# declare i for looping
i = 0

# Variable to keep the main loop running
running = True

# Main loop
while running:
    
    # Running background image
    screen.fill((0, 0, 0))
    
    #screen.blit(bg, (i, 0))
    #screen.blit(bg, (SCREEN_WIDTH + i, 0))
    
    # For loading further background image
    #if (i == -SCREEN_WIDTH):
        #screen.blit(bg, (SCREEN_WIDTH + i, 0))
        #i = 0
    #i -= 1
    
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
                
        # Did the user click the window close button? If so, stop the program
        elif event.type == QUIT:
            running = False
            
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create a new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        # Add a new star
        elif event.type == ADDSTARS:
            # Create the new star and add it to sprite groups
            new_stars = Stars()
            stars.add(new_stars)
            all_sprites.add(new_stars)
            
        # Update display
        #pygame.display.update()

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    
    # Update enemy position
    enemies.update()
    stars.update()
        
    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check if any enemues have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If som then remove the player and stop the loop
        player.kill()
        running = False
    
    # Flip everything to the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)