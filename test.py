import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Load image and audio
image_path = "ChatGPT Image 14. maj 2025, 19.30.49.png"
audio_path = "The Swingin' Swine (Remastered).mp3"
image = pygame.image.load(image_path)
pygame.mixer.music.load(audio_path)

# Additional assets
house_image = pygame.image.load("house.png")
house_image = pygame.transform.scale(house_image, (50, 50))

# Load road images
road_image = pygame.image.load("ChatGPT Image 14. maj 2025, 19.54.45(1).png")
road_image = pygame.transform.scale(road_image, (50, 50))

road_image_turn_right = pygame.image.load("ChatGPT Image 15. maj 2025, 07.29.29(1).png")
road_image_turn_right = pygame.transform.scale(road_image_turn_right, (50, 50))

# Load horizontal road image
road_image_horizontal = pygame.image.load("ChatGPT Image 15. maj 2025, 07.29.29(2).png")
road_image_horizontal = pygame.transform.scale(road_image_horizontal, (50, 50))

# Add new building type: Jazz Arena
jazz_arena_image = pygame.image.load("jazz_arena.png")
jazz_arena_image = pygame.transform.scale(jazz_arena_image, (50, 50))

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Farm Builder Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Building types
BUILDINGS = {
    "house": house_image,
    "farm": GREEN,
    "road": road_image,
    "road_turn_right": road_image_turn_right,
    "road_horizontal": road_image_horizontal,
    "jazz_arena": jazz_arena_image
}

selected_building = "house"

# Load Jazz Pig image (optional for future use)
jazz_pig_chance = 0.1  # 10% chance for Jazz Pig to appear

# Game variables
farm_tiles = []
particles = []

# Add particle effects for Jazz Pig
def create_particles(position):
    for _ in range(10):
        particles.append({
            "pos": list(position),
            "vel": [random.uniform(-2, 2), random.uniform(-2, 2)],
            "timer": random.randint(20, 50)
        })

def update_particles():
    for particle in particles[:]:
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]
        particle["timer"] -= 1
        if particle["timer"] <= 0:
            particles.remove(particle)
        else:
            pygame.draw.circle(screen, (255, 255, 0), (int(particle["pos"][0]), int(particle["pos"][1])), 3)

# Draw farm tiles with building types
def draw_farm():
    for tile, building in farm_tiles:
        if building == "house" or building == "road" or building == "road_turn_right" or building == "road_horizontal" or building == "jazz_arena":
            screen.blit(BUILDINGS[building], tile.topleft)
        else:
            pygame.draw.rect(screen, BUILDINGS[building], tile)

# Display UI for building selection
def draw_ui():
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"Selected: {selected_building.capitalize()} (Press H for House, F for Farm, R for Road, T for Turn Right, L for Horizontal Road, J for Jazz Arena)", True, BLACK)
    screen.blit(text, (10, 10))

# Main game loop
def main_loop():
    global farm_tiles, selected_building
    running = True
    jazz_pig_active = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:
                    selected_building = "house"
                elif event.key == pygame.K_f:
                    selected_building = "farm"
                elif event.key == pygame.K_r:
                    selected_building = "road"
                elif event.key == pygame.K_t:
                    selected_building = "road_turn_right"
                elif event.key == pygame.K_l:
                    selected_building = "road_horizontal"
                elif event.key == pygame.K_j:
                    selected_building = "jazz_arena"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    x, y = event.pos
                    tile = pygame.Rect(x - (x % 50), y - (y % 50), 50, 50)
                    farm_tiles.append((tile, selected_building))

                    # Check for Jazz Pig appearance only for farms and Jazz Arena
                    if selected_building == "farm" and random.random() < jazz_pig_chance:
                        jazz_pig_active = True
                        pygame.mixer.music.play(-1)
                    elif selected_building == "jazz_arena" and random.random() < jazz_pig_chance:
                        jazz_pig_active = True
                        pygame.mixer.music.play(-1)
                        create_particles((x, y))

        screen.fill(WHITE)
        draw_farm()
        draw_ui()
        update_particles()

        if jazz_pig_active:
            # Display a message instead of the image
            font = pygame.font.SysFont(None, 55)
            text = font.render("Jazz Pig is playing!", True, BLACK)
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

        pygame.display.flip()

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

main_loop()