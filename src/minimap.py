from constant import *
import config
import gamemap


def _draw_minimap_player_generated_map(game, scale_factor_x, scale_factor_y):
    """
    Draws player onto minimap as blue

    Args:
        game (Game): Game to draw player on
        scale_factor_x (int): what to scale x by
        scale_factor_y (int): what to sclae y by
    """
    pygame.draw.rect(config.SURFACE_MAIN, BLUE,
                     ((game.player.rect[0] / scale_factor_x),
                      (game.player.rect[1] / scale_factor_y),
                      # + 1 is to make player directly touch walls
                      # without making too big of difference in size
                      (game.player.size[0] / scale_factor_x + 1),
                      (game.player.size[1] / scale_factor_y + 1)))


def _draw_unseen_tile_generated_map(game, scale_factor_x, scale_factor_y):
    """
    Draws unseen tiles as black

    Args:
        game (Game): Game to draw unseen tile on
        scale_factor_x (int): what to scale x by
        scale_factor_y (int): what to scale y by
    """
    for tile in config.MAP_INFO.unseen_tiles:
        tile_x, tile_y = tile
        pygame.draw.rect(config.SURFACE_MAIN, BLACK,
                         ((tile_x * SPRITE_SIZE / scale_factor_x),
                          (tile_y * SPRITE_SIZE / scale_factor_y),
                          # + 2 is to make black cover everything since
                          # add +1 twice for player and room
                          (SPRITE_SIZE / scale_factor_x + 2),
                          (SPRITE_SIZE / scale_factor_y + 2)))


def _draw_minimap_rooms_generated_map(game, scale_factor_x, scale_factor_y):
    """
    Draws rooms (and paths since paths are considered rooms)
    onto minimap as white

    Args:
        game (Game): Game to draw rooms on
        scale_factor_x (int): what to scale x by
        scale_factor_y (int): what to sclae y by
    """
    list_of_rooms = config.MAP_INFO.map_tree.root.child_room_list + config.MAP_INFO.map_tree.root.path_list
    for room in list_of_rooms:
        pygame.draw.rect(config.SURFACE_MAIN, WHITE,
                         ((room.up_left_x * SPRITE_SIZE / scale_factor_x),
                          (room.up_left_y * SPRITE_SIZE / scale_factor_y),
                          # + 1 is to make paths directly touch room
                          # without making too big of difference in size
                          (room.width * SPRITE_SIZE / scale_factor_x + 1),
                          (room.height * SPRITE_SIZE / scale_factor_y + 1)))


def _draw_minimap_walls_generated_map(game, scale_factor_x, scale_factor_y):
    """
    Draws wall onto minimap as black

    Args:
        game (Game): Game to draw wall on
        scale_factor_x (int): what to scale x by
        scale_factor_y (int): what to sclae y by
    """
    pygame.draw.rect(config.SURFACE_MAIN, BLACK,
                     (0, 0,
                      config.MAP_INFO.pixel_width / scale_factor_x,
                      config.MAP_INFO.pixel_height / scale_factor_y))


def draw_minimap_generated_map(game):
    """
    Draws minimap on topleft of screen. This is a
    representation of the actual map. This is for
    procedurally generated maps

    Arg:
        game (Game): game to load minimap to
    """
    minimap_width, minimap_height = game.camera.camera_width / 2, game.camera.camera_height / 2

    map_data = config.MAP_INFO

    scale_factor_width = minimap_width / map_data.tile_width
    scale_factor_height = minimap_height / map_data.tile_height
    scale_factor_x = SPRITE_SIZE / scale_factor_width
    scale_factor_y = SPRITE_SIZE / scale_factor_height

    _draw_minimap_walls_generated_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_rooms_generated_map(game, scale_factor_x, scale_factor_y)
    _draw_unseen_tile_generated_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_items_both_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_enemies_in_fov_both_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_player_generated_map(game, scale_factor_x, scale_factor_y)


def draw_minimap_loaded_map(game):
    """
    Draws minimap on topleft of screen. This is a
    representation of the actual map. This is for maps
    loaded from text files

    Arg:
        game (Game): game to load minimap to
    """
    minimap_width, minimap_height = game.camera.camera_width / 2, game.camera.camera_height / 2
    map_data = config.MAP_INFO
    scale_factor_width = minimap_width / map_data.tile_width
    scale_factor_height = minimap_height / map_data.tile_height
    scale_factor_x = SPRITE_SIZE / scale_factor_width
    scale_factor_y = SPRITE_SIZE / scale_factor_height

    _draw_minimap_floor_and_walls_loaded_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_items_both_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_enemies_in_fov_both_map(game, scale_factor_x, scale_factor_y)
    _draw_minimap_player_loaded_map(game, scale_factor_x, scale_factor_y)


def _draw_minimap_player_loaded_map(game, scale_factor_x, scale_factor_y):
    """
    Draws player onto minimap as red

    This is for map loaded from .txt files

    Args:
        game (Game): Game to draw player on
        scale_factor_x (int): what to scale x by
        scale_factor_y (int): what to sclae y by
    """
    player = game.player
    pygame.draw.rect(config.SURFACE_MAIN, BLUE,
                     (player.rect[0] // scale_factor_x, player.rect[1] // scale_factor_y,
                      player.size[0] // scale_factor_x + 1, player.size[1] // scale_factor_y + 1))


def _draw_minimap_floor_and_walls_loaded_map(game, scale_factor_x, scale_factor_y):
    """
    Draws floor and walls as black

    This is for map loaded from .txt files

    Args:
        game (Game): Game to load minimap to
        scale_factor_x (int): How much to scale x by
        scale_factor_y (int): How mucg to scale y by
    """
    map_data = config.MAP_INFO
    for y in range(map_data.tile_height):
        for x in range(map_data.tile_width):
            tile = config.MAP_INFO.tile_array[y][x].type
            if tile == WALL:
                pygame.draw.rect(config.SURFACE_MAIN, BLACK,
                                 (tile.rect[0] / scale_factor_x, tile.rect[1] / scale_factor_y,
                                  tile.size[0] / scale_factor_x + 1, tile.size[1] / scale_factor_y + 1))
            elif tile == FLOOR:
                if tile.seen:
                    pygame.draw.rect(config.SURFACE_MAIN, WHITE,
                                     (tile.rect[0] / scale_factor_x,
                                      tile.rect[1] / scale_factor_y,
                                      tile.size[0] / scale_factor_x + 1,
                                      tile.size[1] / scale_factor_y + 1))
                else:
                    pygame.draw.rect(config.SURFACE_MAIN, BLACK,
                                     (tile.rect[0] / scale_factor_x,
                                      tile.rect[1] / scale_factor_y,
                                      tile.size[0] / scale_factor_x + 1,
                                      tile.size[1] / scale_factor_y + 1))


def _draw_minimap_items_both_map(game, scale_factor_x, scale_factor_y):
    """
    Draws seen items on minimap as green

    In this case seen items mean the tile it is on is seen
    This is used for both minimaps

    Args:
        game (Game): Game to draw item to
        scale_factor_x (int): How much to scale x by
        scale_factor_y (int): How mucg to scale y by
    """
    for item in game.item_group:
        if config.MAP_INFO.tile_array[item.y][item.x].seen:
            pygame.draw.rect(config.SURFACE_MAIN, GREEN,
                             ((item.rect[0] / scale_factor_x),
                              (item.rect[1] / scale_factor_y),
                              # + 1 is to make items directly touch walls
                              # without making too big of difference in size
                              (item.size[0] / scale_factor_x + 1),
                              (item.size[1] / scale_factor_y + 1)))


def _draw_minimap_enemies_in_fov_both_map(game, scale_factor_x, scale_factor_y):
    """
    Draws enemies in fov on minimap as red

    This is used for both minimaps

    Args:
        game (Game): Game to draw item to
        scale_factor_x (int): How much to scale x by
        scale_factor_y (int): How mucg to scale y by
    """
    for enemy in game.creature_data["enemy"]:
        if game.fov[enemy.y][enemy.x]:
            pygame.draw.rect(config.SURFACE_MAIN, RED,
                             ((enemy.rect[0] / scale_factor_x),
                              (enemy.rect[1] / scale_factor_y),
                              # + 1 is to make items directly touch walls
                              # without making too big of difference in size
                              (enemy.size[0] / scale_factor_x + 1),
                              (enemy.size[1] / scale_factor_y + 1)))
