import os
import pygame
import player 
import map
import constant
from loadAsset import loadImage


def draw_game():
    global SURFACE_MAIN, PLAYER

    draw_map(MAP)

    PLAYER = player.Player()
    SURFACE_MAIN.blit(PLAYER.image, PLAYER.position)

    pygame.display.flip()




def draw_map(map_to_draw):
    for x in range(0, (constant.RESOLUTION[0] // constant.SPRITE_SIZE)):
        for y in range(0, (constant.RESOLUTION[1] // constant.SPRITE_SIZE)):
            if map_to_draw[x][y].walkable == True:
                floor = loadImage('16x16/tiles/floor/floor_1.png')
                SURFACE_MAIN.blit(floor[0], (x * constant.SPRITE_SIZE, y * constant.SPRITE_SIZE))
            else:
                wall = loadImage('16x16/tiles/wall/wall_1.png')
                SURFACE_MAIN.blit(wall[0], (x * constant.SPRITE_SIZE, y * constant.SPRITE_SIZE))
    pygame.display.flip()





def main_loop():
    #TODO: Maybe get rid of global variables later
    global SURFACE_MAIN, PLAYER, BACKGROUND
    draw_game()
    position = PLAYER.rect.move(PLAYER.position)
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            # SURFACE_MAIN.blit(MAP[0], position, position)
            if event.type == pygame.QUIT:
                run = False
                break
            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         position = position.move(-PLAYER.velocity_x, 0)
            #     elif event.key == pygame.K_d:
            #         position = position.move(PLAYER.velocity_x, 0)
            #     elif event.key == pygame.K_s:
            #         position = position.move(0, PLAYER.velocity_y)
            #     elif event.key == pygame.K_w:
            #         position = position.move(0, -PLAYER.velocity_y)
            #     SURFACE_MAIN.blit(PLAYER.image, position)
            #     pygame.display.flip()
            #     pygame.time.delay(10)
    pygame.quit()
    exit()





def init():
    global SURFACE_MAIN, MAP

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(constant.RESOLUTION)
    pygame.display.set_caption('My Pygame')

    MAP = map.create_map()





if __name__ == '__main__':
    init()
    main_loop()