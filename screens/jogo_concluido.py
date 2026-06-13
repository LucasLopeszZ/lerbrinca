import pygame
# ... Import custom classes for Sprites/Particles

# --- Initialization & Constants ---
pygame.init()
SCREEN_W, SCREEN_H = 800, 450
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Você Ganhou!")

# COLORS (matching the image)
LEGO_YELLOW = (254, 212, 1)
BLUE = (0, 85, 166)
RED = (214, 0, 0)
WHITE = (255, 255, 255)

# FONTS
font_large = pygame.font.Font("LEGO_Blocky.ttf", 64)
font_med = pygame.font.Font("LEGO_Edu.ttf", 36)

# --- Classes for Animation ---
class Firework(pygame.sprite.Sprite):
    """ Animated explosion behind the certificate """
    # This class should iterate through a sequence of transparent PNGs
    # or handle the pixel manipulation for particle bursts.
    pass

class SpinningStar(pygame.sprite.Sprite):
    """ Rotating lego-block stars for celebration """
    # Uses pygame.transform.rotate to spin the sprite.
    pass

# --- Loading Assets (matching image_0.png) ---
cert_bg = pygame.image.load("lego_certificate_background.png").convert_alpha()
# cert_bg = pygame.transform.scale(cert_bg, (600, 350)) # Center the main panel

# --- Game State ---
# Groups for automatic management (drawing and updating)
all_sprites = pygame.sprite.Group()
fireworks_group = pygame.sprite.Group()
# Note: Particles/Stars usually go in a separate group above or below text

# --- Initial Setup ---
# Add foreground stars
for i in range(5):
    star = SpinningStar(x=100 + (i*150), y=70) # Positions matching top of image
    all_sprites.add(star)

# Setup a clock for timing
clock = pygame.time.Clock()
firework_timer = pygame.USEREVENT + 1
pygame.time.set_timer(firework_timer, 1200) # Add a new firework every 1.2 seconds

# --- MAIN LOOP ---
running = True
while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Action triggered by keypress or completion
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Add logic to restart the game or exit to menu
                print("Returning to menu...")
                running = False
                
        # Trigger dynamic fireworks behind the certificate
        if event.type == firework_timer:
            new_fw = Firework() # Instantiate new firework object
            fireworks_group.add(new_fw)

    # 2. Update States
    all_sprites.update()    # Update stars/particles
    fireworks_group.update() # Update the explosions/bursts

    # 3. Drawing Phase
    
    # Layer 0: Deep Background (Solid Color)
    screen.fill((50, 150, 220)) # Match the blue tone
    
    # Layer 1: Background Fireworks (Dynamic)
    # Drawing fireworks before the certificate ensures they appear 'behind' it.
    fireworks_group.draw(screen)

    # Layer 2: Main Certificate Panel (Static)
    # (Center the 600x350 panel on the 800x450 screen)
    cert_rect = cert_bg.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
    screen.blit(cert_bg, cert_rect)
    
    # Layer 3: Foreground Animated Sprites (Static Stars)
    # Draw these last so they are visible on top of everything.
    all_sprites.draw(screen)

    # Layer 4: Text Rendering (Dynamic but stable on panel)
    # The image text is rendered directly onto the certificate coordinates.
    title_text = font_large.render("PARABÉNS!", True, BLUE)
    cert_title_rect = title_text.get_rect(center=(SCREEN_W//2, 180))
    screen.blit(title_text, cert_title_rect)
    
    msg_text = font_med.render("VOCÊ COMPLETOU O DESAFIO", True, RED)
    screen.blit(msg_text, (220, 240)) # Positioning matching the middle text

    sub_text = font_med.render("DO PEQUENO CONSTRUTOR!", True, BLUE)
    screen.blit(sub_text, (200, 280)) # Positioning matching the bottom text

    # Final Flip
    pygame.display.flip()
    clock.tick(60) # Maintain 60 FPS for smooth animation

pygame.quit()