import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR1 = (252, 186, 3)
BUTTON_COLOR2 = (252, 20, 3)
BUTTON_COLOR3 = (245, 66, 209)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_FONT_SIZE = 24
BACKGROUND_IMAGE_PATH = "bg.jpeg"  # Replace with your image path

# Title
TITLE_FONT_PATH = "Gula FREE.otf"  # Replace with the path to your font file

# Load the stylish font
TITLE_FONT_SIZE = 110
TITLE_TEXT_COLOR = (0, 0, 66)
title_font = pygame.font.Font(TITLE_FONT_PATH, TITLE_FONT_SIZE)
title_text = title_font.render("SnakePy", True, TITLE_TEXT_COLOR)
title_text_rect = title_text.get_rect()
title_text_rect.centerx = WINDOW_WIDTH // 2
title_text_rect.y = 50  # Adjust the vertical position of the title

# Create the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SankePy")

# Load the background image
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

game_script_path1 = "test.py"
game_script_path2 = "test2.py"

# Create fonts and buttons
font = pygame.font.Font(None, BUTTON_FONT_SIZE)
normal_button = pygame.Rect(
    (WINDOW_WIDTH - BUTTON_WIDTH) // 2,
    WINDOW_HEIGHT // 2 - BUTTON_HEIGHT,  # Adjusted vertical position
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
hard_button = pygame.Rect(
    (WINDOW_WIDTH - BUTTON_WIDTH) // 2,
    WINDOW_HEIGHT // 2 + BUTTON_HEIGHT,  # Adjusted vertical position
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# Define the quit button
quit_button = pygame.Rect(
    (WINDOW_WIDTH - BUTTON_WIDTH) // 2,
    WINDOW_HEIGHT // 2 + 2 * BUTTON_HEIGHT + 40,  # Adjusted vertical position
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

# Button animation variables
normal_button_clicked = False
hard_button_clicked = False

# Game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if normal_button.collidepoint(event.pos):
                normal_button_clicked = True
                subprocess.Popen(["python", game_script_path1])
            elif hard_button.collidepoint(event.pos):
                hard_button_clicked = True
                subprocess.Popen(["python", game_script_path2])
            elif quit_button.collidepoint(event.pos):
                running = False  # Close the window and exit the game loop

    # Draw the background image
    window.blit(background_image, (0, 0))

    # Draw the title
    window.blit(title_text, title_text_rect)

    # Draw buttons with animation
    normal_color = BUTTON_COLOR1 if not normal_button_clicked else (200, 200, 200)
    hard_color = BUTTON_COLOR2 if not hard_button_clicked else (200, 200, 200)

    pygame.draw.rect(window, normal_color, normal_button)
    pygame.draw.rect(window, hard_color, hard_button)
    pygame.draw.rect(window, BUTTON_COLOR3, quit_button)  # Quit button color

    # Add text to buttons
    normal_text = font.render("Normal Level", True, BUTTON_TEXT_COLOR)
    hard_text = font.render("Hard Level", True, BUTTON_TEXT_COLOR)
    quit_text = font.render("Quit", True, BUTTON_TEXT_COLOR)  # Quit button text

    window.blit(normal_text, (normal_button.centerx - normal_text.get_width() // 2, normal_button.centery - normal_text.get_height() // 2))
    window.blit(hard_text, (hard_button.centerx - hard_text.get_width() // 2, hard_button.centery - hard_text.get_height() // 2))
    window.blit(quit_text, (quit_button.centerx - quit_text.get_width() // 2, quit_button.centery - quit_text.get_height() // 2))  # Quit button text

    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
