import pygame
import sys
from menu import Menu  

def run_gameover():
    pygame.init()

    # Set the dimensions of the window
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game over")
    # Set a background color (dark maroon red)
    background_color = (139,0,0)

    # Load and scale the back button image
    back_button = pygame.image.load("images/Replay.png")
    back_button = pygame.transform.scale(back_button, (120, 50))

    #image
    game_over_image=pygame.image.load("images/game_over.webp")
    game_over_image=pygame.transform.scale(game_over_image,(500,300))

    # Back button position
    back_x = 10
    back_y = 10
    #Game over text position
    game_over_image_x=170
    game_over_image_y=150
     
    #Class intialised
    class Button:
        def __init__(self, image, x, y):
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
        # Draw the image on a surface
        def draw(self, surface):
            surface.blit(self.image, self.rect.topleft)
        #Check if the button has been clicked
        def is_clicked(self, event):
            return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    # functions for starting the menu using a modular approach 
    def start_menu():
        pygame.quit()
        menu = Menu()
        menu.run()
    #create the object
    back_button_obj = Button(back_button, back_x, back_y)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button_obj.is_clicked(event):
                print("Back button clicked!")
                running = False
                start_menu()

        # Draw the background and the back button and the game_over text
        screen.fill(background_color)
        back_button_obj.draw(screen)
        screen.blit(game_over_image,(game_over_image_x,game_over_image_y))
        #update the screen
        pygame.display.flip()

# Call the function to run the game over screen
run_gameover()
pygame.quit()
sys.exit()