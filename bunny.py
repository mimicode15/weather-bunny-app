import pygame
import math

class Bunny:
    """Animated bunny that changes based on weather"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.weather_type = "clear"
        self.animation_frame = 0
        self.is_hovered = False
        self.bobble_offset = 0
        
        # Colors
        self.white = (255, 255, 255)
        self.pink = (255, 182, 193)
        self.black = (0, 0, 0)
        self.yellow = (255, 255, 0)
        self.blue = (100, 149, 237)
        self.gray = (169, 169, 169)
        
        # Load sprite images
        print(" Loading sprites...")
        
        try:
            self.bunny_sunny = pygame.image.load('assets/bunny_sunny.png')
            self.bunny_sunny = pygame.transform.scale(self.bunny_sunny, (350, 350))
            print(" Sunny bunny loaded!")
        except Exception as e:
            print(f" Error loading sunny bunny: {e}")
            self.bunny_sunny = None
        
        try:
            self.bunny_rainy = pygame.image.load('assets/bunny_rainy.png')
            self.bunny_rainy = pygame.transform.scale(self.bunny_rainy, (350, 350))
            print(" Rainy bunny loaded!")
        except Exception as e:
            print(f" Error loading rainy bunny: {e}")
            self.bunny_rainy = None
        
        try:
            self.bunny_cloudy = pygame.image.load('assets/bunny_cloudy.png')
            self.bunny_cloudy = pygame.transform.scale(self.bunny_cloudy, (350, 350))
            print(" Cloudy bunny loaded!")
        except Exception as e:
            print(f" Error loading cloudy bunny: {e}")
            self.bunny_cloudy = None
        
        try:
            self.bunny_snowy = pygame.image.load('assets/bunny_snowy.png')
            self.bunny_snowy = pygame.transform.scale(self.bunny_snowy, (350, 3050))
            print(" Snowy bunny loaded!")
        except Exception as e:
            print(f" Error loading snowy bunny: {e}")
            self.bunny_snowy = None
            
        
        
    def update(self, weather_type):
        """Update bunny animation based on weather"""
        self.weather_type = weather_type
    
    def check_hover(self, mouse_pos):
        # Create a rectangle around the bunny for collision detection
        bunny_rect = pygame.Rect(self.x - 125, self.y - 125, 250, 250)
        self.is_hovered = bunny_rect.collidepoint(mouse_pos)
        
        # Debug message
        if self.is_hovered:
            print("Mouse is hovering!")


    def draw_speech_bubble(self, screen, text):
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, self.black)
        text_rect = text_surface.get_rect()

        bubble_x = self.x + 80
        bubble_y = self.y - 150
        padding = 15
        bubble_width = text_rect.width + padding * 2
        bubble_height = text_rect.height + padding * 2
        bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
        pygame.draw.ellipse(screen, self.white, bubble_rect)
        pygame.draw.ellipse(screen, self.black, bubble_rect, 2)

        triangle_points = [
            (bubble_x + 20, bubble_y + bubble_height),
            (bubble_x, bubble_y + bubble_height + 15),
            (bubble_x + 30, bubble_y + bubble_height)
        ]

        text_rect.center = (bubble_x + bubble_width // 2, bubble_y + bubble_height // 2)
        screen.blit(text_surface, text_rect)





        

    def draw(self, screen):
        """Draw the bunny on the screen"""
        self.animation_frame += 1
        print(f"Current weather: {self.weather_type}")
        
        # If sprite didn't load, draw a simple placeholder
        if self.bunny_sunny is None:
            pygame.draw.circle(screen, self.white, (self.x, self.y), 50)
            pygame.draw.circle(screen, self.pink, (self.x, self.y - 10), 5)
            return
        
        # Choose which sprite to show based on weather
        if self.weather_type in ["clear", "sunny", "sun"]:
            current_sprite = self.bunny_sunny
        elif self.weather_type in ["rain", "rainy", "drizzle"]:
            current_sprite = self.bunny_rainy
        elif self.weather_type in ["snow", "snowy", "slush","sleet", "hail"]:
            current_sprite = self.bunny_snowy
        elif self.weather_type in ["cloudy", "overcast", "clouds"]:
            current_sprite = self.bunny_cloudy
        else:
            current_sprite = self.bunny_sunny
        
        # Safety check
        if current_sprite is None:
            pygame.draw.circle(screen, self.white, (self.x, self.y), 50)
            pygame.draw.circle(screen, self.pink, (self.x, self.y - 10), 5)
            return
        
        # Calculate bobble effect when hovered
        if self.is_hovered:
            # Create a bouncing effect using sine wave
            self.bobble_offset = math.sin(self.animation_frame * 0.1) * 10
        else:
            self.bobble_offset = 0
        
        # Get the rectangle for positioning
        bunny_rect = current_sprite.get_rect()
        # Center it at our x, y position (with bobble offset!)
        bunny_rect.center = (self.x, self.y + self.bobble_offset)
        # Draw the sprite!
        screen.blit(current_sprite, bunny_rect)
        
        # Draw text if hovered
        if self.is_hovered:
            # Create font for the text
            font = pygame.font.SysFont('comicsans', 24)
            
            # Choose message based on weather
            if self.weather_type in ["clear", "sunny"]:
                message = "Enjoying the sunshine!"
            elif self.weather_type in ["rain", "rainy", "drizzle", "thunderstorm"]:
                message = "Don't forget your umbrella!"
            elif self.weather_type in ["snow", "snowy"]:
                message = "Brrr! Put on a coat!"
            elif self.weather_type in ["cloudy", "overcast", "clouds"]:
                message = "A bit gloomy today"
            else:
                message = "Enjoy your day!"
            
            # Render the text
            text_surface = font.render(message, True, self.white)
            text_rect = text_surface.get_rect()
            
            # Position above the bunny
            text_rect.center = (self.x, self.y - 150)
            #Position
            text_rect.midleft = (self.x+120, self.y - 80)
            
            # Draw the text
            screen.blit(text_surface, text_rect)
       