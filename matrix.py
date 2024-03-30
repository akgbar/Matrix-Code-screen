# Matrix Rain Effect with Varying Font Sizes and Dimming Effect
# Created by Baris Akgoz for educational purposes
# Feel free to use and modify this code

import pygame  # Import the pygame library for creating the game
import random  # Import the random library for generating random values
import string  # Import the string library for working with strings
import os      # Import the os library for file and directory operations

# Initialize Pygame
pygame.init()

# Get display info for all available screens
screens = [pygame.display.Info() for i in range(pygame.display.get_num_displays())]

# Choose the second screen if available, otherwise use the primary screen
screen_index = 1 if len(screens) > 1 else 0
screen_info = screens[screen_index]

# Set screen dimensions
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h

# Define colors (green text on a black background)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Define character set for the matrix effect (Japanese and Latin letters)
# Adjust this based on your font and system settings
CHARACTER_SET = ''.join(chr(i) for i in range(0x3041, 0x3097)) + string.ascii_letters

# Define text properties
FONT_SIZE_RANGE = (10, 24)  # Range for random font sizes
FONT_PATH = "matrixcode_nfi.ttf"  # Assuming the font file is in the same folder as the script
FONT_CACHE = {}  # Cache for font sizes

# Define the probability of a character changing during each update
CHARACTER_CHANGE_PROBABILITY = 0.01  # Adjust as needed

# Define the maximum number of lines
MAX_LINES = 50  # Adjust as needed

# Define alpha ranges based on font size
ALPHA_RANGE = {
    10: (50, 200),   # Font size 10: alpha range (min, max)
    12: (70, 220),   # Font size 12: alpha range (min, max)
    14: (90, 240),   # Font size 14: alpha range (min, max)
    16: (110, 255),  # Font size 16: alpha range (min, max)
    18: (130, 255),  # Font size 18: alpha range (min, max)
    20: (150, 255),  # Font size 20: alpha range (min, max)
    22: (170, 255),  # Font size 22: alpha range (min, max)
    24: (190, 255),  # Font size 24: alpha range (min, max)
}

# Define class for Matrix characters
class MatrixColumn:
    def __init__(self, x):
        # Initialize a Matrix column with position x
        self.x = x

        # Random initial speed
        self.speed = random.randint(5, 30)

        # Random initial length
        self.length = random.randint(5, 80)

        # Initialize at the top of the screen
        self.y = random.randint(-self.length, 0) * max(FONT_SIZE_RANGE)

        # Generate characters for the column
        self.characters = self._generate_characters()

    def _generate_characters(self):
        # Generate random characters for the column
        font_size = random.randint(*FONT_SIZE_RANGE)
        scaled_font = pygame.font.Font(FONT_PATH, font_size)
        FONT_CACHE[font_size] = scaled_font
        return [(random.choice(CHARACTER_SET), font_size) for _ in range(self.length)]

    def draw(self, surface):
        # Draw the Matrix column on the surface
        for i, (char, font_size) in enumerate(self.characters):
            text_surface = FONT_CACHE[font_size].render(char, True, GREEN)
            text_surface.set_alpha(self._calculate_alpha(font_size))
            surface.blit(text_surface, (self.x, self.y + i * font_size))

    def _calculate_alpha(self, font_size):
        # Calculate alpha value based on font size
        min_alpha, max_alpha = ALPHA_RANGE.get(font_size, (0, 255))
        return random.randint(min_alpha, max_alpha)

    def update(self):
        # Update the position of the Matrix column
        self.y += self.speed

        # If the column reaches the bottom, reset its position and properties
        if self.y > HEIGHT:
            self.y = -self.length * max(FONT_SIZE_RANGE)
            self.speed = random.randint(5, 30)
            self.length = random.randint(5, 80)
            self.characters = self._generate_characters()
        else:
            # Update characters within the column
            self._update_characters()

    def _update_characters(self):
        # Update characters in the column
        for i in range(len(self.characters)):
            if random.random() < CHARACTER_CHANGE_PROBABILITY:
                # Randomly change characters in the column
                self.characters[i] = (random.choice(CHARACTER_SET), self.characters[i][1])

def add_column(columns):
    # Add a new Matrix column to the list of columns
    x = random.randint(0, WIDTH - max(FONT_SIZE_RANGE))
    columns.append(MatrixColumn(x))

def remove_column(columns):
    # Remove the oldest Matrix column if the maximum number of lines is exceeded
    if len(columns) > MAX_LINES:
        del columns[0]

def main():
    # Initialize the Pygame screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Matrix Rain")
    clock = pygame.time.Clock()

    # Initialize a list to hold Matrix columns
    columns = []

    # Initialize counters for adding and removing columns
    add_column_counter = 0
    remove_column_counter = 0

    running = True
    while running:
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen with a black background
        screen.fill(BLACK)

        # Draw and update each Matrix column
        for col in columns:
            col.draw(screen)
            col.update()

        # Increment counters for adding and removing columns
        add_column_counter += 1
        remove_column_counter += 1

        # Add a new column if the add_column_counter exceeds a threshold
        if add_column_counter >= 5:
            add_column(columns)
            add_column_counter = 0

        # Remove the oldest column if the remove_column_counter exceeds a threshold
        if remove_column_counter >= 200:
            remove_column(columns)
            remove_column_counter = 0

        # Update the display and limit the frame rate
        pygame.display.flip()
        clock.tick(120)

    # Quit Pygame when the main loop exits
    pygame.quit()

# Run the main function if this script is executed
if __name__ == "__main__":
    main()
