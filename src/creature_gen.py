import random
import creature
import entity
import ai
import container


def generate_enemies(tree, game):
    """
    Generates one creature in every room

    Args:
        tree (BSP tree): Tree representing rooms
        game (Game): Game with all game data
    """
    # get all rooms in map
    for child_room in tree.root.child_room_list:
        # generate monster in room
        _generate_enemies(child_room, game)


def _generate_enemies(room, game):
    """
    Generates a random monster in room at random coords

    Args:
        room (Room): Room to generate monste rin
        game (Game): Game with all game data
    """
    x1, y1, x2, y2 = room.coords
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    r = random.randint(0, 2)
    if r == 0:
        new_enemy = _generate_slime(x, y, game)
    elif r == 1:
        new_enemy = _generate_goblin(x, y, game)
    else:
        new_enemy = _generate_skeleton(x, y, game)

    game.enemy_group.append(new_enemy)


def _generate_slime(x, y, game):
    """
    Generates slime at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    ai_gen = ai.SmartAi()
    creature_gen = creature.Creature("slime", True, game.player_group)
    enemy_gen = entity.Entity(game, x, y, "enemy", anim=game.game_sprites.slime_dict, creature=creature_gen, ai=ai_gen)
    return enemy_gen


def _generate_goblin(x, y, game):
    """
    Generates goblin at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    ai_gen = ai.SmartAi()
    creature_gen = creature.Creature("goblin", True, game.player_group)
    enemy_gen = entity.Entity(game, x, y, "enemy", anim=game.game_sprites.goblin_dict, creature=creature_gen, ai=ai_gen)
    return enemy_gen


def _generate_skeleton(x, y, game):
    """
    Generates skeleton at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    ai_gen = ai.SmartAi()
    creature_gen = creature.Creature("skeleton", True, game.player_group)
    enemy_gen = entity.Entity(game, x, y, "enemy", anim=game.game_sprites.skeleton_dict, creature=creature_gen, ai=ai_gen)
    return enemy_gen


def generate_player(tree, game):
    """
    Generates player in random room

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    room = random.choice(tree.root.child_room_list)
    x1, y1, x2, y2 = room.coords
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    player_container = container.Container()
    player_com = creature.Creature("knight", enemy_group=game.enemy_group)
    player = entity.Entity(game, x, y, "player",
                           anim=game.game_sprites.knight_dict,
                           creature=player_com,
                           container=player_container)
    return player


def generate_free_camera(game):
    """
    Generates slime at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    camera = creature.Creature("Camera", False, walk_through_tile=True)
    free_camera = entity.Entity(game, 0, 0, "camera", image=game.game_sprites.mouse_select, creature=camera)
    return free_camera
