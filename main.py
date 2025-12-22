import pygame
import sys
from weather_api import get_weather
from bunny import Bunny

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BLUE = (135, 206, 235)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
TEAL = (64, 224, 208)
DARK_TEAL = (0, 128, 128)
LIGHT_TEAL = (178, 255, 255)

# Fonts
font_large = pygame.font.Font(None, 48,)
font_medium = pygame.font.Font(None, 36,)
font_small = pygame.font.Font(None, 28,)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Weather Bunny")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Create bunny
bunny = Bunny(SCREEN_WIDTH // 2, 400)

# Input box variables
input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 100, 300, 40)
input_text = ""
input_active = False

# Button
button = pygame.Rect(SCREEN_WIDTH // 2 - 90, 160, 180, 40)

# Weather data
weather_data = None
show_weather = False
use_celsius = True
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def draw_rounded_rect(surface, rect, color, radius=10):
    """Draw a rectangle with rounded corners"""
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_input_screen():
    """Draw the location input screen"""
    # Title
    title_text = font_large.render("Weather Bunny", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
    screen.blit(title_text, title_rect)
    
    # Instruction
    instruction = font_small.render("Enter your location:", True, WHITE)
    instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, 75))
    screen.blit(instruction, instruction_rect)
    
    # Input box
    box_color = WHITE if input_active else GRAY
    draw_rounded_rect(screen, input_box, box_color, 10)
    
    # Input text
    if input_text:
       text_surface = font_medium.render(input_text, True, BLACK)
       clip_rect = pygame.Rect(input_box.x+10, input_box.y, input_box.width-20, input_box.height)
       screen.set_clip(clip_rect)
       text_rect = text_surface.get_rect(center=input_box.center)
       screen.blit(text_surface, text_rect)
       screen.set_clip(None)
    
    
    
    
    # Button
    mouse_pos = pygame.mouse.get_pos()
    button_color = DARK_TEAL if button.collidepoint(mouse_pos) else TEAL
    draw_rounded_rect(screen, button, button_color, 10)
    
    button_text = font_medium.render("Get Weather", True, WHITE)
    button_rect = button_text.get_rect(center=button.center)
    screen.blit(button_text, button_rect)

def draw_weather_screen():
    """Draw the weather display screen"""
    if not weather_data:
        error_text = font_medium.render("Could not fetch weather :(", True, WHITE)
        error_rect = error_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(error_text, error_rect)
        return
    
    # Location name
    location_name = weather_data.get('name', 'Unknown')
    location_text = font_large.render(location_name, True, WHITE)
    location_rect = location_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    screen.blit(location_text, location_rect)
    
    # Temperature (with conversion)
    temp_celsius = weather_data['main']['temp']

    if use_celsius:
        temp_display = f"{temp_celsius:.1f} °C"
    else:
        temp_fahrenheit = celsius_to_fahrenheit(temp_celsius)
        temp_display = f"{temp_fahrenheit:.1f} °F"

    temp_text = font_large.render(temp_display, True, WHITE)
    temp_rect = temp_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
    screen.blit(temp_text, temp_rect)

    # Temperature toggle button
    toggle_button = pygame.Rect(SCREEN_WIDTH//2+80, 95, 80, 35)
    mouse_pos = pygame.mouse.get_pos()
    toggle_color = DARK_TEAL if toggle_button.collidepoint(mouse_pos) else LIGHT_TEAL
    draw_rounded_rect(screen, toggle_button, toggle_color)

    #Button text

    toggle_text = "°F" if use_celsius else "°C"
    toggle_text_surface = font_small.render(toggle_text, True, BLACK)
    toggle_text_rect = toggle_text_surface.get_rect(center=toggle_button.center)
    screen.blit(toggle_text_surface, toggle_text_rect)


    # Weather condition
    condition = weather_data['weather'][0]['main']
    condition_text = font_medium.render(condition, True, WHITE)
    condition_rect = condition_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
    screen.blit(condition_text, condition_rect)
    
    # Description
    description = weather_data['weather'][0]['description'].title()
    desc_text = font_small.render(description, True, WHITE)
    desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, 195))
    screen.blit(desc_text, desc_rect)
    
    # Update bunny with weather
    bunny.update(condition.lower())
    bunny.draw(screen)
    
    # Back button
    back_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, 520, 150, 40)
    mouse_pos = pygame.mouse.get_pos()
    back_color = DARK_TEAL if back_button.collidepoint(mouse_pos) else TEAL
    draw_rounded_rect(screen, back_button, back_color, 10)
    
    back_text = font_small.render("New Search", True, WHITE)
    back_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_rect)
    
    return back_button, toggle_button

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if not show_weather:
            # Input screen events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if input box clicked
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                
                # Check if button clicked
                if button.collidepoint(event.pos) and input_text:
                    print(f"Fetching weather for: {input_text}")
                    weather_data = get_weather(input_text)
                    if weather_data:
                        show_weather = True
                    else:
                        print("Failed to get weather data")
            
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN and input_text:
                    # Enter key pressed
                    print(f"Fetching weather for: {input_text}")
                    weather_data = get_weather(input_text)
                    if weather_data:
                        show_weather = True
                    else:
                        print("Failed to get weather data")
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    # Add character to input
                    if len(input_text) < 25:
                        input_text += event.unicode
        else:
            # Weather screen events
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button = pygame.Rect(SCREEN_WIDTH//2-75,520,150,40)
                toggle_button = pygame.Rect(SCREEN_WIDTH//2+80,95,80,35)

                #Check back button
                if back_button.collidepoint(event.pos):
                    show_weather = False
                    input_text = ""
                
                #Check temperature toggle button
                if toggle_button.collidepoint(event.pos):
                    use_celsius = not use_celsius
                    print(f"Switched to {'Celsius' if use_celsius else 'Fahrenheit'}")

                
    
    # Fill screen with background color
    screen.fill(LIGHT_BLUE)
    
    # Draw appropriate screen
    if not show_weather:
        draw_input_screen()
    else:
        draw_weather_screen()
        mouse_pos = pygame.mouse.get_pos()
        bunny.check_hover(mouse_pos)
        bunny.animation_frame += 1
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate (60 FPS)
    clock.tick(60)

# Quit
pygame.quit()
sys.exit()