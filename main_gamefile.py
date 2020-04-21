import pygame
import random
import math
# a class that helps us handle any kind of music in pygame
from pygame import mixer

#  Initialise pygame
pygame.init()

# Creating the Game window
gameWindow = pygame.display.set_mode((800, 600))

# game background Image
game_background = pygame.image.load('Images/game_background.png')

# background music
mixer.music.load('Sounds/background.wav')
mixer.music.play(-1)

# Adding a Game Title
pygame.display.set_caption("Alien Shooter Game")
# Icon for the game
gameIcon = pygame.image.load('Character_Icons/enemy.png')
pygame.display.set_icon(gameIcon)

# Defining Player Image and Starting Position of the player
playerIcon = pygame.image.load('Character_Icons/player_image.png')
playerPosX = 360
playerPosY = 480
# Responsible for the change in direction when user presses left of right key
playerPosx_change = 0

# Enemy
# create a list to store enemies and their relevant information
enemyIcon = []
enemyPosX = []
enemyPosY = []
enemyPosx_change = []
enemyPosy_change = []
# Starting number of enemies
number_of_enemies = 5

# Defining Enemy Image and Starting Position of the Enemies
for i in range(number_of_enemies):
    enemyIcon.append(pygame.image.load('Character_Icons/enemy_image.png'))
    # Randomising our enemy start position to the set range
    enemyPosX.append(random.randint(0, 735))
    enemyPosY.append(random.randint(50, 150))
    # Responsible for the change in direction of the enemy
    enemyPosx_change.append(4)
    # this enables the enemy to move downwards by 40 pixels immediately it hits the window
    enemyPosy_change.append(40)

# Bullet
# Defining Enemy Image and Starting Position of the Enemy
bulletIcon = pygame.image.load('Character_Icons/bullet.png')
# Randomising our bullet start position according to the current x position of our ship
bulletPosX = 0
# our player is always at 480 y-axis and since the bullet is 32 pixels it makes it shorter
bulletPosY = 480
# Responsible for the change in direction of the bullet
bulletPosx_change = 0
bulletPosy_change = 10
# set - unable to see the bullet on the screen but is ready to be fired
# fire - bullet currently moving

bullet_state = 'set'

# variable to store the score value
score = 0
# font name and the font size
score_font = pygame.font.Font('freesansbold.ttf', 32)
# x and y variable of where we want the score to occur on the screen
scoreX = 10
scoreY = 10
# game over text
gameover_font = pygame.font.Font('freesansbold.ttf', 64)


# function that shows the score on the screen
def display_score(x, y):
    # Initialising the text to be displayed
    score_value = score_font.render('Score:' + str(score), True, (255, 255, 255))
    # Displaying the text
    gameWindow.blit(score_value, (x, y))


# function that displays the End Game Text
def game_over_display():
    # Initialising the text to be displayed
    gameover_text = gameover_font.render('FUCK YOU LOSER ', True, (255, 255, 255))
    # Displaying the text
    gameWindow.blit(gameover_text, (200, 250))

# Player Character Function
# Arguments x_axis and y_axis to take user input for moving the player accordingly
def player_character(x_axis, y_axis):
    # the blit() method is used to draw the player's Image icon at the defined positions for x and y
    gameWindow.blit(playerIcon, (x_axis, y_axis))


# Enemy Character Function
def enemy_character(x_axis, y_axis, i):
    # the blit() method is used to draw the player's Image icon at the defined positions for x and y
    gameWindow.blit(enemyIcon[i], (x_axis, y_axis))


# fire bullet Function
def fire_bullet(x, y):
    # global variable so that it can be accessed in the function
    global bullet_state
    bullet_state = 'fire'
    # ensures bullet appears on the screen at the center of the spaceship
    gameWindow.blit(bulletIcon, (x + 16, y + 10))


#     define whether a collison with the enemy has occurred
def coll_detect(enemyPosX, enemyPosY, bulletPosX, bulletPosY):
    # Getting the distance between the bullet and the enemy to check for collision
    game_distance = math.sqrt((math.pow(enemyPosX - bulletPosX, 2)) + (math.pow(enemyPosY - bulletPosY, 2)))
    # If game distance is less than 27 then collision occurs
    if game_distance < 27:
        return True
    else:
        # else no collision
        return False


# Game Loop
# Makes sure the game window runs until the Quit button is pressed
gameRunning = True
while gameRunning is True:
    # Changing the game screen's background using RGB codes
    gameWindow.fill((0, 0, 255))
    # background image(prevents the image from disappearing after a second)
    gameWindow.blit(game_background, (0, 0))
    # This for loop checks for the event that the quit button is pressed by the user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False

        # This Section Handles player movement input along the a axis.
        # If key is pressed check whether it is left or right KEYDOWN - Pressing a key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerPosx_change = -5
            if event.key == pygame.K_RIGHT:
                playerPosx_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'set':
                    # Bullet Sound Plays when bullet is fired!
                    bullet_music = mixer.Sound('Sounds/laser.wav')
                    bullet_music.play()
                    # gets the x coordinate of the spaceship
                    bulletPosX = playerPosX
                    fire_bullet(bulletPosX, bulletPosY)
        # Check if pressed key has been released KEYUP- Releasing the pressed key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerPosx_change = 0

    # This line updates the player's x-axis position according to the above keyboard press conditions
    playerPosX += playerPosx_change

    # This part is meant to create boundaries around the screen such that the player does not leave the game window
    if playerPosX <= 0:
        playerPosX = 0
    # using 736 because of the size of the object this time 64 pixels so that it can remain within the window
    elif playerPosX >= 736:
        playerPosX = 736

        # Enemy movement
        # This line updates the enemy's x-axis position
    for i in range(number_of_enemies):
        # this code is used in ending the game
        # If enemy gets down to the Player's position, Game Ends!
        if enemyPosY[i] > 440:
            for j in range(number_of_enemies):
                # ensures the enemies go below the screen(Removed from the Screen)
                enemyPosY[j] = 2000
            game_over_display()
            break
        enemyPosX[i] += enemyPosx_change[i]

        # This part is meant to create boundaries around the screen such that the enemy does not leave the game window
        if enemyPosX[i] <= 0:
            enemyPosx_change[i] = 4
            enemyPosY[i] += enemyPosy_change[i]
        # using 736 because of the size of the enemy this time 64
        # pixels so that it can remain within the window(subtract 64 from 800)
        elif enemyPosX[i] >= 736:
            enemyPosx_change[i] = -4
            enemyPosY[i] += enemyPosy_change[i]
        # This code handles enemy collision
        character_collision = coll_detect(enemyPosX[i], enemyPosY[i], bulletPosX, bulletPosY)
        # If condition for collision occurs...
        if character_collision:
            explosion_music = mixer.Sound('Sounds/explosion.wav')
            explosion_music.play()
            bulletPosY = 480
            bullet_state = 'set'
            score += 1
            # print(score)
            enemyPosX[i] = random.randint(0, 800)
            enemyPosY[i] = random.randint(50, 150)
        # Instantiate the enemy characters within the for loop
        enemy_character(enemyPosX[i], enemyPosY[i], i)

    # After bullet crosses the 0 y-axis mark, reset bullet position to 480 y-axis
    # This allows our bullet to be fired again
    if bulletPosY <= 100:
        bulletPosY = 480
        bullet_state = 'set'
    #     Bullet movement after firing
    if bullet_state is 'fire':
        fire_bullet(bulletPosX, bulletPosY)
        # Y-Coordinate changes dues to the change in y variable
        bulletPosY -= bulletPosy_change

    # Calling our Player to be displayed
    player_character(playerPosX, playerPosY)
    # Calling our score to be displayed
    display_score(scoreX, scoreY)
    # constantly updating our game window
    pygame.display.update()
