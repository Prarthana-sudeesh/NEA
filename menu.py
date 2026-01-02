import pygame
import sys

pygame.init()
# Goals: I will make a class so i can link the menu to the main game this would allow me to make a home page
# Goals: I also intend to add a link back to menu so they can go back to the menu
class Menu:
    def __init__(self, width=800, height=600):
        # Set the dimensions of the window
        self.WIDTH, self.HEIGHT = width, height
       
        # Initialize Pygame
        pygame.init()
       
        # Create the display surface
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
       
        # Set the title of the window
        pygame.display.set_caption("Menu")
       
        # Create a clock object to manage the frame rate
        self.clock = pygame.time.Clock()
       
        # Load the default font
        self.font = pygame.font.Font(None, 50)
     
        # Load the menu image
        self.menu_image = pygame.image.load("images/menu.jpeg")
       
        # Scale the menu image to fit the window dimensions 
        self.menu_image = pygame.transform.scale(self.menu_image, (self.WIDTH, self.HEIGHT))
       
        # Load the play button image and scale it
        self.play_button = pygame.image.load("images/Play.png")
        self.play_button = pygame.transform.scale(self.play_button, (150, 100))
        self.play_button_rect = self.play_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
       
        # Load and scale the title image
        self.title = pygame.image.load("images/title.png")
        self.title = pygame.transform.scale(self.title, (500, 100))
        self.title_rect = self.title.get_rect(center=(self.WIDTH // 2, 50))
        self.distance = 0  # Initialize distance variable


        # Pressed buttons
        self.play_clicked = False
        self.endless_button_pressed=False
        # Image change
        self.play_pressed = pygame.image.load("images/Play_button.png")
        self.play_pressed = pygame.transform.scale(self.play_pressed, (150, 100))
        #Main game loop
        self.running = True
          # Flag to indicate play button click
        self.info_button = pygame.image.load("images/info2.png")
        self.info_button = pygame.transform.scale(self.info_button, (140, 100))
        self.info_button_rect = self.info_button.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 170))
        self.info_button_pressed = False
        

    #Drawing all the buttons
    def menu_draw(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with a white color
        self.screen.blit(self.menu_image, (0, 0))  # Draw the background image
        self.screen.blit(self.title, self.title_rect)  # Draw the title
        self.screen.blit(self.play_button, self.play_button_rect)  # Draw the play button
        self.screen.blit(self.info_button, self.info_button_rect)#Draw the info button



        pygame.display.flip()  # Update the display
    #Check if info button is clicked
    def info_click(self, x, y):
           if self.info_button_rect.collidepoint(x, y):
               print("Info button clicked")
               self.info_button_pressed = True
               return True
           return False

         
    #function for play click
    def play_click(self, x, y):
        if self.play_button_rect.collidepoint(x, y):
            self.play_button_pressed = True
            self.play_clicked = True  # Set the flag when play button is clicked
            return True
        return False
    
    #Info button functions to open that file when clicked
    def start_info(self):
        try:
            from info import run_info
            run_info() 
        except ImportError:
            print("Error")
 
    # Function and validation so the map runs and used for debugging in case it doesnt.
    def start_main_game(self):
        try:
            from endless import run_map3
            run_map3()
        except ImportError:
            print("Error")
        


    #Main function to check if buttons are clicked and update boolean variables accordingly
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if the mouse is clicked 
                    x, y = event.pos
                    #Mouse collision with buttons checked
                    self.play_click(x, y)
                    self.info_click(x, y)
                    #Boolean variables updated
                    if self.info_button_pressed:
                       self.info_button_pressed = False
                       self.start_info()
                    if self.play_clicked:
                       self.play_clicked = False # Reset the button state
                       self.running = False
                       self.start_main_game() #transition to the main game
            pygame.mouse.set_visible(True)
            #draws the menu
            self.menu_draw()
            # Limit the frame rate to 60 FPS
            self.clock.tick(60)
            pygame.display.flip()  # Update the display
        pygame.quit()
        sys.exit()


#Function that calls all the other functions in order to run them.      
def run_menu():
    menu = Menu()
    menu.run()

#Makes sure there are no issues
if __name__ == "__main__":
    run_menu()
    # Run the menu


