import config
import random
import creature
import entity
import ai
import container
import item


def generate_enemies(tree, game):
    """
    Generates one creature in every room

    Args:
        tree (BSP tree): Tree representing rooms
        game (Game): Game with all game data

    Returns:
        enemy_list (List): List of generated enemies
    """
    enemy_list = []
    # get all rooms in map
    for child_room in tree.root.child_room_list:
        # generate monster in room
        _generate_enemy(child_room, game, enemy_list)

    return enemy_list


def _generate_enemy(room, game, enemy_list):
    """
    Generates a random monster in room at random coords
    as long as coords is not the same as player coord

    Args:
        room (Room): Room to generate monste rin
        game (Game): Game with all game data
        enemy_list (list): list to append created enemy to
    """
    x1, y1, x2, y2 = room.coords
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    # This makes it so no mosters spawn on same tile as player
    while (x, y) == (config.PLAYER.x, config.PLAYER.y):
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)

    random_num = random.randint(0, 2)
    if random_num == 0:
        new_enemy = _generate_slime(x, y, game)
    elif random_num == 1:
        new_enemy = _generate_goblin(x, y, game)
    else:
        new_enemy = _generate_skeleton(x, y, game)

    enemy_list.append(new_enemy)


def _generate_slime(x, y, game):
    """
    Generates slime at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    ai_gen = ai.ChaseAI()
    creature_gen = creature.Creature("slime", True, "enemy", level=config.GAME_DATA.floor)
    generated_enemy = entity.Entity(game, x, y, "enemy", creature=creature_gen, ai=ai_gen, image_key="slime_dict")
    return generated_enemy


def _generate_goblin(x, y, game):
    """
    Generates goblin at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    ai_gen = ai.ChaseAI()
    creature_gen = creature.Creature("goblin", True, "enemy", level=config.GAME_DATA.floor)
    generated_enemy = entity.Entity(game, x, y, "enemy", creature=creature_gen, ai=ai_gen, image_key="goblin_dict")
    return generated_enemy


def _generate_skeleton(x, y, game):
    """
    Generates skeleton at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    ai_gen = ai.ChaseAI()
    creature_gen = creature.Creature("skeleton", True, "enemy", level=config.GAME_DATA.floor)
    generated_enemy = entity.Entity(game, x, y, "enemy", creature=creature_gen, ai=ai_gen, image_key="skeleton_dict")
    return generated_enemy


def generate_player(tree, game):
    """
    Generates player in random room

    Args:
        tree (BSP tree): Tree representing rooms
        game (Game): Game with all game data
    """
    room = random.choice(tree.root.child_room_list)
    x1, y1, x2, y2 = room.coords
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    player_container = container.Container()
    player_com = creature.Creature("knight", team="player")
    player = entity.Entity(game, x, y, "player", creature=player_com, container=player_container,
                           image_key="knight_dict")
    return player


def generate_player_spawn(tree):
    """
    Generates player coords for random room

    This is also required on top of generate_player since
    when transitioning to new floors, you want the same player
    but a new spawn point

    Args:
        tree (BSP tree): Tree representing rooms

    Returns:
        x, y (int, int): Coords to spawn player at
    """
    room = random.choice(tree.root.child_room_list)
    x1, y1, x2, y2 = room.coords
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    return x, y


def generate_free_camera(game):
    """
    Generates slime at coords (x, y)

    Args:
        x (int): x coord to generate monster at
        y (int): y coord to generate monster at
        game (Game): Game with all game data
    """
    camera = creature.Creature("Camera", False, walk_through_tile=True)
    free_camera = entity.Entity(game, 0, 0, "camera", creature=camera, image_key="mouse_select")
    return free_camera


def generate_items(tree, game):
    """
    Randomly generates items in rooms

    Args:
        tree (BSP tree): Tree representing rooms
        game (Game): Game with all game data

    Returns:
        item_list (List): list of all items generated
    """
    item_list = []
    # get all rooms in map
    for child_room in tree.root.child_room_list:
        random_num = random.randint(0, 100)
        # 50% chance of spawning item
        if random_num < 50:
            _generate_item(child_room, game, item_list)

    return item_list


def _generate_item(room, game, item_list):
    """
    Generates a item in room at random coords and appends to item_list

    Args:
        room (Room): Room to generate monste rin
        game (Game): Game with all game data
        item_list (list): list to append created item to
    """
    x1, y1, x2, y2 = room.coords
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    random_num = random.randint(0, 1)
    if random_num == 0:
        new_item = _generate_potion(x, y, game)
    else:
        new_item = _generate_sword(x, y, game)

    item_list.append(new_item)


def _generate_potion(x, y, game):
    """
    Generates potion at coords (x, y)

    Args:
        x (int): x coord to generate item at
        y (int): y coord to generate item at
        game (Game): Game with all game data
    """
    item_com = item.Item("Red Potion", 0, 0, True)
    generated_item = entity.Entity(game, x, y, "item", item=item_com, image_key="red_potion")
    return generated_item


def _generate_sword(x, y, game):
    """
    Generates sword at coords (x, y)

    Args:
        x (int): x coord to generate item at
        y (int): y coord to generate item at
        game (Game): Game with all game data
    """
    item_sword_com = item.Item("Sword", 0, 0, False)
    generated_item = entity.Entity(game, x, y, "item", item=item_sword_com, image_key="sword")
    return generated_item
