import os
import pygame
import map
import constant
import object
import components


def draw_game():
    """
    Draws maps and entities
    """
    map.draw_map(MAP, SURFACE_MAIN)
    # could change this so instead of constant map, pass map into method
    constant.com_map = MAP

    ALLSPRITES.draw(SURFACE_MAIN)

    # Might need this later
    # SLIME.draw_object(SURFACE_MAIN)
    # PLAYER.draw_object(SURFACE_MAIN)

    pygame.display.flip()





def main_loop():
    """
    Main game loop which takes in player input and moves character    
    """

    while True:

        player_action = handleKeys()
        if player_action == "QUIT":
            break

        draw_game()

    pygame.quit()
    exit()




def handleKeys():
    """
    Handle player input
    """
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
            print("PLAYER at " + str(PLAYER.x), str(PLAYER.y))
            print("PLAYER_rect at " + str(PLAYER.rect))
            print("SLIME at " + str(SLIME.x), str(SLIME.y))
            print("SLIME_rect at " + str(SLIME.rect))
            print()
    return "no-action"








def init():
    """
    Initializes pygame and the map and entities
    """
    global SURFACE_MAIN, MAP, PLAYER, ALLSPRITES, GAME_OBJECTS, SLIME

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(constant.RESOLUTION)
    pygame.display.set_caption('My Pygame')

    MAP = map.create_map()

    creaturetest = components.creature("Viet", 10)
    PLAYER = object.object(
        1, 1, "player", constant.CHARACTER, creature=creaturetest)

    creaturetest1 = components.creature("Slime", 3, components.death)

    ai_component = components.ai_test()
    SLIME = object.object(6, 6, "slime", constant.SLIME,
                          creature=creaturetest1, ai=ai_component)

    # GAME_OBJECTS = [PLAYER, SLIME]
    # constant.game_objects = GAME_OBJECTS

    ALLSPRITES = pygame.sprite.OrderedUpdates(SLIME, PLAYER)
    constant.game_objects = ALLSPRITES





if __name__ == '__main__':
    init()
    main_loop()
