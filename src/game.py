import os
import pygame
import map
import constant
import object
import components


def draw_game():
    '''
    Draws maps and entities
    '''
    draw_map(MAP)
    constant.com_map = MAP

    ALLSPRITES.draw(SURFACE_MAIN)

    # Might need this later
    # SLIME.draw_object(SURFACE_MAIN)
    # PLAYER.draw_object(SURFACE_MAIN)

    pygame.display.flip()


# TODO: change path for images to constant when right picture is found
def draw_map(map_to_draw):
    '''
    Draws map and makes walkable = True to floor and walkable = False wall

    Loops through every tile in map and draws it in correct position

    Arg:
        map_to_draw (array): map to draw as background
    '''
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
    '''
    Main game loop which takes in player input and moves character    
    '''

    run = True
    while run:

        player_action = handleKeys()
        if player_action == "QUIT":
            run = False

        draw_game()

    pygame.quit()
    exit()

def handleKeys():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            return "QUIT"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                ALLSPRITES.update(-1, 0, MAP)
            if event.key == pygame.K_d:
                ALLSPRITES.update(1, 0, MAP)
            if event.key == pygame.K_w:
                ALLSPRITES.update(0, -1, MAP)
            if event.key == pygame.K_q:
                ALLSPRITES.update(-1, -1, MAP)
            if event.key == pygame.K_e:
                ALLSPRITES.update(1, -1, MAP)
            if event.key == pygame.K_z:
                ALLSPRITES.update(-1, 1, MAP)
            if event.key == pygame.K_c:
                ALLSPRITES.update(1, 1, MAP)
            if event.key == pygame.K_s:
                ALLSPRITES.update(0, 1, MAP)
            if event.key == pygame.K_x:
                ALLSPRITES.update(0, 0, MAP)
    return "no-action"


def init():
    '''
    Initializes pygame and the map and entities
    '''
    global SURFACE_MAIN, MAP, PLAYER, ALLSPRITES, GAME_OBJECTS

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(constant.RESOLUTION)
    pygame.display.set_caption('My Pygame')

    MAP = map.create_map()

    creaturetest = components.creature("Viet")
    PLAYER = object.object(
        1, 1, "knight", constant.CHARACTER, creature=creaturetest)

    creaturetest1 = components.creature("Slime")

    ai_component = components.ai_test()
    SLIME = object.object(6, 6, "slime", constant.SLIME,
                          creature=creaturetest1, ai=ai_component)

    GAME_OBJECTS = [PLAYER, SLIME]
    constant.game_objects = GAME_OBJECTS

    ALLSPRITES = pygame.sprite.OrderedUpdates(SLIME, PLAYER)


if __name__ == '__main__':
    init()
    main_loop()
