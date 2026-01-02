import pygame
import sys
from menu import Menu  

def run_info():
    pygame.init()

    # Set the dimensions of the window
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Game over Level 2")
    # Set a background color (dark maroon red)
    background_color = (128, 0, 32)

    # Load and scale the back button image
    back_button = pygame.image.load("images/back.png")
    back_button = pygame.transform.scale(back_button, (100, 50))

    # Back button position
    back_x = 10
    back_y = 10
    text_font = pygame.font.Font(None, 36)

    #Function to draw the text for instructions
    def draw_text(text,font,text_color,x,y):
       img=font.render(text,True,text_color)
       screen.blit(img,(x,y))
    #Class Button  for back button
    class Button:
        def __init__(self, image, x, y):
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
        #Blit the button on a screen
        def draw(self, surface):
            surface.blit(self.image, self.rect.topleft)
        #check if the button has been clicked 
        def is_clicked(self, event):
            return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    # functions for starting the menu using a modular approach 
    def start_menu():
        pygame.quit()
        menu = Menu()
        menu.run()
    #create back button object
    back_button_obj = Button(back_button, back_x, back_y)

    #Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # usage of the function to check if the button is pressed
            if back_button_obj.is_clicked(event):
                print("Back button clicked!")
                running = False
                start_menu()

        # Draw everything
        screen.fill(background_color)
        #draw button
        back_button_obj.draw(screen)


        # Draw text for instructions
        draw_text("Use the arrow keys to choose your path:", text_font, (255, 255, 255), 170, 160)
        draw_text("- Right key: right position", text_font, (255, 255, 255), 220, 195)
        draw_text("- Up key or Down key: middle position", text_font, (255, 255, 255), 220, 230)
        draw_text("- Left key: left position", text_font, (255, 255, 255), 220, 260)
        draw_text("Your goal: collect enough coins to pay for your journey!", text_font, (255, 255, 255), 110, 300)

        #update game window 
        pygame.display.flip()
# Call the function to run the game over screen
run_info()
pygame.quit()
sys.exit()