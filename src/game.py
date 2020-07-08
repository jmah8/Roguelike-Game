import os
import pygame
import map
import constant
import object


def draw_game():

    draw_map(MAP)

    SLIME.draw_object(SURFACE_MAIN)
    PLAYER.draw_object(SURFACE_MAIN)

    pygame.display.flip()


# TODO: change path for images to constant when right picture is found
def draw_map(map_to_draw):
    for x in range(0, (constant.RESOLUTION[0] // constant.SPRITE_SIZE)):
        for y in range(0, (constant.RESOLUTION[1] // constant.SPRITE_SIZE)):
            if map_to_draw[x][y].walkable == True:
                floor = object.loadImage('16x16/tiles/floor/floor_1.png')
                SURFACE_MAIN.blit(
                    floor[0], (x * constant.SPRITE_SIZE, y * constant.SPRITE_SIZE))
            else:
                wall = object.loadImage('16x16/tiles/wall/wall_1.png')
                SURFACE_MAIN.blit(
                    wall[0], (x * constant.SPRITE_SIZE, y * constant.SPRITE_SIZE))


def main_loop():
    run = True
    while run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    PLAYER.move(-1, 0, MAP)
                if event.key == pygame.K_d:
                    PLAYER.move(1, 0, MAP)
                if event.key == pygame.K_s:
                    PLAYER.move(0, 1, MAP)
                if event.key == pygame.K_w:
                    PLAYER.move(0, -1, MAP)

        draw_game()

    pygame.quit()
    exit()


def init():
    global SURFACE_MAIN, MAP, PLAYER, SLIME

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(constant.RESOLUTION)
    pygame.display.set_caption('My Pygame')

    MAP = map.create_map()

    PLAYER = object.object(1, 1, constant.CHARACTER)
    SLIME = object.object(6, 6, constant.SLIME)


if __name__ == '__main__':
    init()
    main_loop()
