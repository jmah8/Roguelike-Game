from constant import *
from gamemap import *


def new_fov(game):
    """
    Makes new fov array

    Args:
        game: Game with game data

    Returns:
        new_fov (2D array): new fov array
    """
    new_fov = [[0 for x in range (0, game.map_data.tilewidth)] for y in range (game.map_data.tileheight)]
    return new_fov


def ray_casting(game, map_array, fov):
    """
    Calculates which tiles are seen

    Args:
        game: Game with game data
        map_array: map_array with representation of map
        fov: fov array telling which tile is seen
    """
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

            if (map_array[int(round(y))][int(round(x))] == WALL):
                break
    
    fov[game.player.y][game.player.x] = 1


def draw_seen(game, map_array, fov):
    """
    Draws unseen tiles, seen tiles and explored tiles

    Args:
        game: Game with game data
        map_array: map_array with representation of map
        fov: fov array telling which tile is seen
    """
    for y in range(0, game.map_data.tileheight):
        for x in range(0, game.map_data.tilewidth):
            tile = map_array[y][x]
            # If tile is where player is, it is seen
            if (x, y) == (game.player.x, game.player.y):
                tile.image = tile.image_in_fov
                # Remove player tile from unseen_tile
                if ((x, y) in game.map_data.unseen_tiles):
                    game.map_data.unseen_tiles.remove((x, y))
            # If tile is seen switch to in fov sprite
            elif fov[y][x] == 1:
                if isinstance(tile, Floor):
                    tile.image = tile.image_in_fov
                else:
                    tile.image = tile.image_in_fov
                tile.seen = True
                # Remove seen tile from unseen_tile
                if ((x, y) in game.map_data.unseen_tiles):
                    game.map_data.unseen_tiles.remove((x, y))
            # Tile is not seen
            else:
                tile = map_array[y][x]
                # If never seen before make black
                if (not tile.seen):
                    tile.image = game.game_sprites.unseen_tile
                # Else shade tile black
                else:
                    tile.image = tile.image_seen


def check_if_in_fov(game, obj):
    """
    Checks to see if sprite is in player FOV

    Args:
        sprite (sprite): sprite to check
    """
    x = obj.x
    y = obj.y
    return (game.fov[y][x] == 1)