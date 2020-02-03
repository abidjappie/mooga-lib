import sys, pygame
from mooga import Scene, Animation, Character, Color

#Initialise Pygame
pygame.init()
#Set the display size to 800 x 600 pixels
#And return a surface to render to
screen = pygame.display.set_mode((800, 600))

#Load images for the right and left player animations
player_right = Animation("assets/player_right/")
player_left = Animation("assets/player_left/")

#Load a static image for the enemy animation
enemy_anim = Animation("assets/enemy.png")

#Create the player Character and assign the 'player_right' animation as the initial animation
#Set the player position to 128, 128
player = Character(player_right)
player.setPosition(128,128)

#Create the enemy Character and set its position
enemy = Character(enemy_anim)
enemy.setPosition(512,256)

#Add the enemy to the player's list of colliders
#Allowing the player to detect collisions with the enemy
player.addColliders(enemy)

#Initialise the Scene with background color as 'medium_sea_green'
#Add the player and enemy characters (as a list) to the scene
scene = Scene(backgroundColor=Color.medium_sea_green)
scene.addCharacters([player, enemy])

#Define the game loop (infinite loop)
while (True):
    #Get the events from pygame
    #Check for events of interest
    for event in pygame.event.get():
        #If the QUIT event is called, exit the game
        if event.type == pygame.QUIT: sys.exit()
        #If a key is pressed
        #Check which key is pressed and manipulate the player acceleration and animation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.xacc = 1
                player.animation = player_right
            if event.key == pygame.K_LEFT:
                player.xacc = -1
                player.animation = player_left
            if event.key == pygame.K_DOWN:
                player.yacc = 1
            if event.key == pygame.K_UP:
                player.yacc = -1
        #Check which key is released and reset the player motion
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.xacc = 0
                player.xvel = 0
            if event.key == pygame.K_LEFT:
                player.xacc = 0
                player.xvel = 0
            if event.key == pygame.K_DOWN:
                player.yacc = 0
                player.yvel = 0
            if event.key == pygame.K_UP:
                player.yacc = 0
                player.yvel = 0
    #scene.autoScrollView(1,0,50)

    #Set the current view to follow the player Character
    #Set the padding to be x=300 and y=200
    #Enable smoothing at 2 pixels every 30 milliseconds
    scene.viewFollowCharacter(player,300,200, smoothing=True, speed=2, milliseconds=30)

    #Update the player motion every 30 milliseconds
    player.autoUpdateMotion(30)
    #Update the player animation framed every 30 milliseconds
    player.autoUpdateFrame(60)
    #Update the scene and render to the screen
    scene.updateScene(screen)
    #Refresh pygame
    pygame.display.flip()