import sys, pygame
from mooga import Scene, Animation, Character, Color

pygame.init()
screen = pygame.display.set_mode((800, 600))

player_right = Animation("assets/player_right/player_right.png")
player_left = Animation("assets/player_left/")

enemy_anim = Animation("assets/enemy.png")

player = Character(player_right)
player.setPosition(128,128)

enemy = Character(enemy_anim)
enemy.setPosition(512,256)

player.addColliders(enemy)

scene = Scene(backgroundColor=Color.medium_sea_green)
scene.addCharacters([player, enemy])

while (True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        
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
    scene.autoScrollView(1,0,50)

    player.autoUpdateMotion(30)
    player.autoUpdateFrame(60)

    scene.updateScene(screen)
    
    pygame.display.flip()