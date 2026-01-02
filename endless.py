
import pygame
import sys
import random


pygame.init()
pygame.font.init()
def run_map3():
    # Constants
    WIDTH, HEIGHT = 800, 600#This is the width and height of the screen
    scroll_speed = 8 # This determines the speed of the background and also determines how fast the player views the movement of the card.
    coin_speed = 3 #This is the coin speed that  stays constant.
    rock_speed = 4 #This is the speed of the obstacle that changes as levels increase.
    speed = 3  #This is the speed of the cart
    money = 0 #This is the amount of money that increments as the player collects the coin.
    lives=3#Intial live count that decrements
    last_collision_time=0#updated variable when a collision is detection and is required to implement a collision cooldown.
    collision_cooldown=1000# This is time that controls how quickly the green bar decreases
    coin_rect = pygame.Rect(0, 0, 100, 100) #Position of coin as a rectangle to make it easier for collision detection
   
    # Set up the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blazeway Game")


    
    # cart set positions
    a = 180
    b = 320
    c = 485
    #The point at which the background scrolls back to the beginning 
    scroll_threshold = 100

    current_time=pygame.time.get_ticks()# time required for collision cooldown
    # Load and scale background images
    background2 = pygame.image.load("images/Paris.png")
    background2 = pygame.transform.scale(background2, (WIDTH, HEIGHT))
    background = pygame.image.load("images/track.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    background1=pygame.image.load("images/jungle.jpeg")
    background1=pygame.transform.scale(background1,(WIDTH,HEIGHT))
    background4=pygame.image.load("images/london_map.png")
    background4=pygame.transform.scale(background4,(WIDTH,HEIGHT))
    background5=pygame.image.load("images/chinese_map.png")
    background5=pygame.transform.scale(background5,(WIDTH,HEIGHT))
    background6=pygame.image.load("images/russia.png")
    background6=pygame.transform.scale(background6,(WIDTH,HEIGHT))
    background7=pygame.image.load("images/dubai.png")
    background7=pygame.transform.scale(background7,(WIDTH,HEIGHT))
    cart_width, cart_height = 300,120
    backgrounds=[]
    backgrounds.append(background2)
    backgrounds.append(background4)
    backgrounds.append(background1)
    backgrounds.append(background5)
    backgrounds.append(background6)
    backgrounds.append(background7)
    if not backgrounds:
        print("No background loaded")
        backgrounds=[pygame.Surface(WIDTH,HEIGHT)]


    # Background positions
    #Uses two sets of background images to cover the screen and blits the first image and then the second after the first to make scroll
    bg_height = background.get_height()
    bg_y1 = 0
    bg_y2 = -bg_height #used for background scrolling 


    # Load and scale cart image
    cart_image = pygame.image.load("images/cart.png")
    cart_image = pygame.transform.scale(cart_image, (150, 140))
    cart_x, cart_y = 320, 450
    cart_rect = cart_image.get_rect()
    cart_animated=pygame.image.load("images/cart_animation.png") #The image used for animation of movement
    cart_animated = pygame.transform.scale(cart_animated, (150, 140))

    # Load and scale coin image
    coin = pygame.image.load("images/coin.png")
    coin = pygame.transform.scale(coin, (80, 80))

    # Load and scale rock (obstacle) image
    #An array is created which is iterated through according to the background to allow for theme and creativity.
    obstacle1 = pygame.image.load("images/obstacle.png")
    obstacle2 =pygame.image.load("images/london_obstacle.png")
    obstacle3=pygame.image.load("images/panda.png")
    obstacle4=pygame.image.load("images/russia_obstacle.png")
    obstacle5=pygame.image.load("images/white_box.png")
    obstacle6=pygame.image.load("images/dolphin.png")
    obstacle1 = pygame.transform.scale(obstacle1, (100, 100))#
    obstacle2 = pygame.transform.scale(obstacle2, (100,200))
    obstacle3 = pygame.transform.scale(obstacle3, (200,200))
    obstacle4 = pygame.transform.scale(obstacle4, (100,400))
    obstacle5=pygame.transform.scale(obstacle5,(100,300))
    obstacle6=pygame.transform.scale(obstacle6,(200,200))
    obstacle_rect = pygame.Rect(
        random.randint(190, 320),  # Middle X range
        random.randint(300,600),  # Y range in top half
        100, 70  # Width and height of the obstacle
        )
    obstacles=[] #array used
    obstacles.append(obstacle1)
    obstacles.append(obstacle2)
    obstacles.append(obstacle5)
    obstacles.append(obstacle3)
    obstacles.append(obstacle4)
    obstacles.append(obstacle6)

    #Animated coin
    animated_coin = pygame.image.load("images/coin_animated.png")
    animated_coin = pygame.transform.scale(animated_coin, (80, 80))
    #The health bar that is posed as fuel tank which decreases due to collision
    # Uses two rectangles and blits them on top of each other and decreases one sequentially to make it seem as if they lost a life.
    #Scaling and loading of Health bar
    Red=pygame.image.load("images/red_radar.png") 
    Red=pygame.transform.scale(Red, (40, 300))
    Green=pygame.image.load("images/green_radar.webp")
    Green_width, Green_height = 40, 300
    Green=pygame.transform.scale(Green, (50, 300))
    Radar_x = 695
    Radar_y = 200
    target_height=300

    #Scaling and Loading of a fuel tank that adds theme to the idea of the cart being a vehicle as well as acts as a health bar icon.
    fuel_image= pygame.image.load("images/Fuel.png")
    fuel_image= pygame.transform.scale(fuel_image, (80, 80))


    #back button
    back_x=10 #Intial x value of back button 
    back_y=10 # intial y value of back button
    back_button=pygame.image.load("images/back.png")
    back_button=pygame.transform.scale(back_button, (100, 50))

    # The track positions on the game
    #In order to tackle one my errors used an array in order to reperesnt different positions in the game
    track_positions=[] 
    track_positions.append(a+20)
    track_positions.append(b+40)
    track_positions.append(c+40)

    #Text font 
    text_font = pygame.font.Font(None, 36)
    
    #Position of the mouse
    pos=pygame.mouse.get_pos()

    #Standalone functions for drawing text
    def draw_text(text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))
    #Drawing the background  and iterating through the backgrounds array that adds to the theme according to the money allows for levels
    def update_background_index(money,backgrounds):
        index = (money // 10) % len(backgrounds)
        return index
    #Iterating through the obstacles array to align with the background and add to the theme according to the money allows for levels.
    def update_obstacle(money,obstacles):
        if money<0:
            money=0
        if len(obstacles)==0:
            return None
        index = (money // 10) % len(obstacles)
        return index
    


    # Cart class
    class Cart(pygame.sprite.Sprite):
        def __init__(self,x,y,speed):
            super().__init__()
            self.x = x
            self.y = y
            self.speed = speed
            self.a = a
            self.b = b
            self.c = c
            self.animated_cart=cart_animated
            self.scroll_threshold = scroll_threshold
            self.current_position = 1
            self.sprites = []
            self.animated = False
            self.sprites.append(pygame.image.load("images/cart.png"))
            self.current_sprite_index = 0
            self.image = self.sprites[self.current_sprite_index]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
            self.scroll = 0
        #This is the function for the movement of the cart that uses an array , using left, right key and up or down key.
        #Using an array made it a lot more simpler and avoided complication , it also made it easier to find errors and debug such as the position of the obstacles and so on. 
        def move_cart(self):
                self.scroll = 0
                keys = pygame.key.get_pressed()
                positions = [self.a, self.b, self.c]
                moved = False
                if keys[pygame.K_LEFT]:
                    self.current_position = 0
                    moved = True
                elif keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                    self.current_position = 1
                    moved = True
                elif keys[pygame.K_RIGHT]:
                    self.current_position = 2
                    moved = True
                self.x = positions[self.current_position] #This controls the position of the cart whether it be middle , left or right.
                if moved:
                    self.animate()
        #usage of a boolean variable in order to check the animation of the cart
        def animate(self):
                self.animated = True
        # A minimal function in order to check the position of the cart.
        def get_position(self):
            return self.x, self.y
        #Checks the collision of the cart and the obstacle
        def collision_detection(self, cart_rect, obstacle_rect):
            return cart_rect.colliderect(obstacle_rect)

    # Coin class
    class Coin:
        #Intialise all variables
        def __init__(self, x, y, coin_image):
            self.coin_image = coin_image
            self.x = x
            self.y = y
            self.animated_coin = animated_coin
            self.track_positions=track_positions
            self.obstacle_rect=obstacle_rect
            self.rect = self.coin_image.get_rect()   
            
        #Updates the coin position as it blinks or changes position
        def update_rect(self):
            self.rect.x = self.x
            self.rect.y = self.y
        #Blits the coins animation once every second and then nothing the next second.
        def blink(self, frame):
            if frame % 60 < 30:# Blink every half second
                screen.blit(self.animated_coin, (self.x, self.y))       
        #the position of the coin must be randomised to ensure difficulty therefore allowing for this function
        def randomize_position(self):
            self.x = random.choice(self.track_positions)
            self.y = random.randint(0, 100)
            self.update_rect()
        #Moves the coin down the screen in set positions so that the player can move the cart to gain more coins.
        def movedown(self):
           self.y+=coin_speed
           self.update_rect()
           if self.y > HEIGHT-10:# to protect the coin from going off screen
               self.randomize_position()  # Reset the coin position to a random location at the top of the screen
        #This makes sure the obstacle and coin do not spawn in the same place so the player is able to collect the coin without losing a life.
        def safe_randomize_coin(self,obstacle):
           max = 10
           for i in range(max):
              self.randomize_position()
              if not self.rect.colliderect(obstacle.rect):
                return 
           self.x = 100
           self.y = 100
           self.update_rect() #Update position
    #Button class
    class Button:
        def __init__(self, image, x, y):
            self.image = image
            self.x = x
            self.y = y
            self.pos=pos
        #The collision between the image and position is checked with this function
        def collidepoint(self, pos):
            rect = self.image.get_rect(topleft=(self.x, self.y))
            return rect.collidepoint(pos)

    
    # Obstacle class
    class Obstacle:
        def __init__(self, x, y, image):
            self.image = image
            self.x = x
            self.y = y
            self.rect = image.get_rect(topleft=(x, y))
            self.cart_rect = cart_image.get_rect(topleft=(cart_x, cart_y))
            self.coin_rect=coin_rect
            self.track_positions=track_positions

        #Update the position
        def update_rect(self):
            self.rect.topleft = (self.x, self.y)
        #move the obstacle down with a given speed and use validation in order to prevent the obstacle from going off page
        def movedown(self):
            self.y += rock_speed
            self.update_rect()
            if self.y > HEIGHT - 10:  # to protect the coin from going off screen
                # Reset the coin position to a random location at the top of the screen
                self.y = random.randint(0, 100)
                self.x = random.choice(self.track_positions)
        #Randomise the position of the obstacle to increase difficulty and make it spawn higher up so it gives the player more time to react
        def randomize_position(self):   
            self.x = random.choice(self.track_positions)
            self.y = random.randint(0, 50)
            self.update_rect() 
    #Fuel class
    class Fuel:
        def __init__(self, x, y):
            self.fuel_image = fuel_image
            self.x = x
            self.y = y
            self.frame = 0
        #Make the fuel tank blink as a way of showing the tank is leaking due to a collision and to make the player aware of the health bar.
        def blink(self, frame):
            if frame % 60 < 30:  # Blink every half second
                screen.blit(self.fuel_image, (self.x, self.y))
    # Create objects
    #Back button
    Back_button = Button(back_button, back_x, back_y)
    #Coins
    passenger_cart = Cart(cart_x, cart_y, speed)
    coin1 = Coin(350, 300, coin)
    coin1.update_rect()

    # Obstacles
    obstacle1 = Obstacle(180, 100, obstacle1)
    # Fuel Gauge
    Gauge = Fuel(670, 500)
    # Main game loop
    running = True #Boolean used to run game window
    frame = 0
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type==pygame.MOUSEBUTTONDOWN: #Check if the button has been pressed
                if Back_button.collidepoint(event.pos):
                    #Import the menu function to run menu using a modular approach 
                    from menu import run_menu
                    run_menu()
        if lives <0 and lives>3:
            lives =3
        #Used a new function isinstance to check if money or lives is an integer as way of validation
        if not isinstance(money,int):
            money=int(money)
        if not isinstance(lives,int):
            lives=3

        # Update cart position
        passenger_cart.move_cart()
        cart_x, cart_y = passenger_cart.get_position()
        cart_rect.topleft = (cart_x, cart_y) #The position of the cart

        #The function is used to set an index to blit the background according to money and set levels
        #This part of the code is key in making it seem like the player is travelling through the world
        current_bg_index=update_background_index(money,backgrounds)
        current_obstacle_index = update_obstacle(money, obstacles)
        current_obstacle_img = obstacles[current_obstacle_index]
        if current_obstacle_index not in range(len(obstacles)):
            current_obstacle_index=0
        #This is the scaling of the image 
        obstacle1.image = pygame.transform.scale(current_obstacle_img, (100, 100))
        # Vertical scrolling
        #This is uses two images blitted one after the other to allow for vertical scorlling
        bg_y1 += scroll_speed
        bg_y2 += scroll_speed
        if bg_y1 >= HEIGHT:
            bg_y1 = bg_y2 - bg_height
        if bg_y2 >= HEIGHT:
            bg_y2 = bg_y1 - bg_height
        #Use of the index determined the money value which can them blitted on the screen
        bg=backgrounds[current_bg_index]
        # Draw backgrounds
        screen.blit(bg, (0, bg_y1))
        screen.blit(bg, (0, bg_y2))
        screen.blit(background, (0, 0)) #This is the additional image of the rails which stay constant throughout the game.
        # Draw cart with integrated blink logic
        #This allows for animation that lasts for barely a second as the cart  moves or animates
        if frame % 180 < 180 and passenger_cart.animated:
            screen.blit(passenger_cart.animated_cart, (cart_x, cart_y))
            passenger_cart.animated = False  # Reset animation flag after updating
        else:
            screen.blit(cart_image, (cart_x, cart_y))

        # Draw and update obstacle
        screen.blit(obstacle1.image, (obstacle1.x, obstacle1.y))
        #Represents the name of the map that the player is in
        country_names = ["France", "London","Africa", "China", "Russia", "Dubai"]
        #The country descriptions act as a for the player to learn more about each country
        country_descriptions=[
            "France: Famous for Eiffel Tower and delicious croissants",
            "London:Big Ben, red buses and royalty",
            "Africa: A continent with deserts, jungles and amazing animals.",
            "China:The Great Wall and Pandas live here like Kung Fu Panda",
            "Russia: Known for cold winters and colorful architecture",
            "Dubai: Famous for tall skyscrapers, the Burj Khalifa and desert adventures"
        ]

        #use of array in order to blit the text
        # uses MOD in  order to blit text according to the background so it is accurate
        index_description=(current_bg_index)%len(backgrounds)
        description=country_descriptions[index_description]
        if len(description)>200:
            description=description[:200]#truncates the description if its too long
        #Using validation to make sure the desciption is in the current format.
        if not isinstance(description,str):
            description=str(description)

        #Speed of Obstacles- Difficulty
        #This essentially determines the difficulty of the levels by using the amount of money in order to increase for each level.
        #This money also determines various other factors such as the text, country, background and obstacle type.
        if money <= 20 and money>0:#Makes sure the money is greater than zero by way of format check
           rock_speed = 5
        elif money <= 30:#level 3
            rock_speed = 6
        elif money <=40:#level 4
            rock_speed=7
        elif money<=50:#level 5
            rock_speed=8
        elif money>50:#level 6
            rock_speed=9
        else:
            rock_speed =4 #primary speed
        #Movement of Obstacle
        obstacle1.movedown()
        obstacle1.update_rect()
        
        current_time = pygame.time.get_ticks()
        if passenger_cart.collision_detection(cart_rect, obstacle1.rect):
            lives -= 1#decrement ,ives
            scroll_speed-=1 #Make the background slower so it seems due to fuel leakage the cart is moving slower
            if lives == 0: #import the file from gameover to indicate the player has lost
                from gameover import run_gameover
                run_gameover()
            if current_time - last_collision_time > collision_cooldown:#For given period of time the health bar decreases until a given height
                target_height = max(0, Green_height - 100)  # Reduce the height of the green radar
                obstacle1.randomize_position() 
                last_collision_time = current_time  # update the time of the hit
                print("Lives left:", lives)
        # Check for collision between the cart and obstacle

        Green=pygame.transform.scale(Green, (Green_width, Green_height))
        if Green_height > target_height: #decreases the health bar so it can be blitted smoothly.
           Green_height -= 5

        if Green_height<0 or Green_height>300:#Validation for Green height
            Green_height=max(0,min(300,Green_height))
        
        if passenger_cart.collision_detection(cart_rect, coin1.rect) :
            coin1.safe_randomize_coin(obstacle1) # Makes sure it does not spawn in the same place
            money += 1
        #Movement of the Coin
        coin1.movedown()
        coin1.blink(frame)#Animation of the coin
        coin1.update_rect()#update the position
        screen.blit(coin, (coin1.x, coin1.y))#Puts animated coin in the same position of the normal coin
        # Draw UI and text for the player to undertsand it
        draw_text(f"Score: {money}", text_font, (255, 255, 255), 0, 550)
        draw_text(f"Lives: {lives}", text_font, (255, 255, 255), 0, 570)
        draw_text(f"Country: {country_names[current_bg_index]}", text_font, (255, 255, 255), 0, 525)
        draw_text(f" {description}", text_font, (215, 255, 255), 30, 57) 

        #Additional Icons
        #Back button
        screen.blit(back_button, (10, 10))
        Gauge.blink(frame)
        screen.blit(Red, (Radar_x, Radar_y))  # Draw the red radar
        screen.blit(Green, (Radar_x, Radar_y))  # Draw the green radar
       
        # Update display
        frame += 1
        clock.tick(60)
        pygame.display.flip()
        if not pygame.get_init():
           break
    pygame.quit()
    sys.exit()

# Call the function to run the map3 screen
run_map3()

current_time = pygame.time.get_ticks()


