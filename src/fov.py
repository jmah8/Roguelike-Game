from constant import *
from gamemap import *


def new_fov(game):
    new_fov = [[0 for x in range (0, game.map_data.tilewidth)] for y in range (game.map_data.tileheight)]
    return new_fov


def ray_casting(game, map_array, fov):
    for a in range(0, RAYS + 1, STEP):
        ax = sintable[a]
        ay = costable[a]

        x = game.player.x
        y = game.player.y

        for b in range(KNIGHT_FOV):
            x += ax
            y += ay

            if x < 0 or y < 0 or x > game.map_data.tilewidth - 1 or y > game.map_data.tileheight - 1:
                break
                
            fov[int(round(y))][int(round(x))] = 1

            if isinstance(game.map_array[int(round(y))][int(round(x))], Wall):
                break
    
    fov[game.player.y][game.player.x] = 1


def draw_seen(game, map_array, fov):
    for y in range(0, game.map_data.tileheight):
        for x in range(0, game.map_data.tilewidth):
            tile = map_array[y][x]
            if (x, y) == (game.player.x, game.player.y):
                tile.image = tile.image_unexplored
            elif fov[y][x] == 1:
                if isinstance(tile, Floor):
                    tile.image = tile.image_unexplored
                else:
                    tile.image = tile.image_unexplored
                tile.seen = True
            else:
                tile = map_array[y][x]
                if (not tile.seen):
                    tile.image = game.game_sprites.unseen_tile
                else:
                    tile.image = tile.image_explored


def check_if_in_fov(game, obj):
    """
    Checks to see if sprite is in player FOV

    Args:
        sprite (sprite): sprite to check
    """
    x = obj.x
    y = obj.y
    return (game.fov[y][x] == 1)