# Initialize Pygame
import pygame
from settings import TEXT_COLOR, UI_BG_COLOR, UI_FONT_PATH, UI_FONT_SIZE

pygame.init()

# Initialize font with a size of 22
font = pygame.font.Font(UI_FONT_PATH, UI_FONT_SIZE)

def debug(info, y = 10, x = 10):
    """
    Display debugging information on the Pygame screen.

    Parameters:
    - info: The information to be displayed.
    - y (optional): The y-coordinate of the text position.
    - x (optional): The x-coordinate of the text position.
    """

    display_surface = pygame.display.get_surface()
    
    if display_surface is None:
        
        # Error handling if the display surface is not initialized
        print("Error: Display surface not initialized.")
        
        return

    debug_surface = font.render(str(info), True, TEXT_COLOR)
    debug_rectangle = debug_surface.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surface, UI_BG_COLOR, debug_rectangle)
    display_surface.blit(debug_surface, debug_rectangle)
