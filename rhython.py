import pygame
import sys

# Initialize Pygame
pygame.init()

# Setup the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pygame Tutorial")

# Initialize font and sound
font = pygame.font.Font(pygame.font.get_default_font(), 100)

from pygame import mixer
mixer.init()

clock = pygame.time.Clock()

# Define key class
class Key():
    def __init__(self, x, y, color1, color2, key):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2
        self.key = key
        self.rect = pygame.Rect(self.x, self.y, 100, 40)
        self.handled = False

# Define keys
keys = [
    Key(100, 500, (255, 0, 0), (220, 0, 0), pygame.K_a),
    Key(200, 500, (0, 255, 0), (0, 220, 0), pygame.K_s),
    Key(300, 500, (0, 0, 255), (0, 0, 220), pygame.K_l),
    Key(400, 500, (255, 255, 0), (220, 220, 0), pygame.K_SEMICOLON),
]

# Load map
def load(map_name):
    rects = []
    mixer.music.load(map_name + ".mp3")
    mixer.music.play()
    
    try:
        with open(map_name + ".txt", 'r') as f:
            data = f.readlines()
    except FileNotFoundError:
        print(f"File {map_name}.txt not found.")
        return rects
    
    for y in range(len(data)):
        for x in range(len(data[y])):
            if x < len(keys):  # Ensure x is within bounds of keys
                if data[y][x] == '0':
                    rects.append(pygame.Rect(keys[x].rect.centerx - 25, y * -65, 50, 25))
            else:
                print(f"Warning: Index {x} exceeds number of keys {len(keys)}")
    
    return rects


# Display menu
def show_menu():
    menu_font = pygame.font.Font(pygame.font.get_default_font(), 50)
    menu_text = menu_font.render("Press ENTER to Start", True, (255, 255, 255))
    menu_rect = menu_text.get_rect(center=(400, 300))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(menu_text, menu_rect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Exit the menu loop

# Game loop
def game_loop():
    combo = 0
    map_rect = load("Axion")

    while True:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Handle key inputs
        k = pygame.key.get_pressed()
        for key in keys:
            if k[key.key]:
                pygame.draw.rect(screen, key.color1, key.rect)
                key.handled = False
            if not k[key.key]:
                pygame.draw.rect(screen, key.color2, key.rect)
                key.handled = True

        for rect in map_rect:
            pygame.draw.rect(screen, (200, 0, 0), rect)
            rect.y += 9

            for key in keys:
                if key.rect.colliderect(rect) and not key.handled:
                    map_rect.remove(rect)
                    combo += 1
                    key.handled = True
                    break
            if keys[0].rect.bottom < rect.y:
                map_rect.remove(rect)
                combo = 0
        
        # Display combo text
        text = font.render(str(combo), True, "white")
        screen.blit(text, (0, 0))

        pygame.display.update()
        clock.tick(60)

# Main execution
if __name__ == "__main__":
    show_menu()  # Show menu before starting the game
    game_loop()  # Start the game loop
