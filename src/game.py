import pickle
from constant import *
import config
import fov
import gamemap
import magic
import pathfinding
from camera import Camera
import draw
from entity_generator import *
import menu_manager
import button_manager

pygame.font.init()


def toggle_minimap():
    """
    Toggles minimap
    """
    config.MINIMAP = not config.MINIMAP


def _check_if_enemy_in_fov():
    """
    Returns:
        true if enemy is in player FOV, else false
    """
    for obj in config.GAME_DATA.creature_data["enemy"]:
        if fov.check_if_in_fov(obj, config.FOV) and not config.WALL_HACK:
            return True
    return False


def map_items_at_coord(coord_x, coord_y):
    """
    Returns list of items at (coord_x, coord_y)

    Args:
        coord_x (int): x coord on map
        coord_y (int): y coord on map

    Returns:
        objects (List): list of items at (coord_x, coord_y)
    """
    objects = [obj for obj in config.GAME_DATA.item_data if obj.x == coord_x and obj.y == coord_y]
    return objects


def _toggle_wallhack():
    """
    Toggles wallhack. If wallhack is on, then show whole map in player FOV
    else turn back to normal fov
    """
    config.WALL_HACK = not config.WALL_HACK
    if config.WALL_HACK:
        config.FOV = [[1 for x in range(0, config.MAP_INFO.tile_width)] for y in
                      range(config.MAP_INFO.tile_height)]


def _update_creatures(dx, dy):
    """
    Updates all creatures and increments turn count

    Args:
        dx (int): x to move player by
        dy (int): y to move player by
    """
    for team in config.GAME_DATA.creature_data:
        for entity in config.GAME_DATA.creature_data[team]:
            entity.update(dx, dy)
    config.TURN_COUNT += 1


def generate_camera():
    """
    Generates camera
    """
    config.CAMERA = Camera(config.MAP_INFO)


def _populate_map():
    """
    Adds entities to map

    Only makes new player on start, then it moves player
    to random location after
    """
    # Particle group
    config.PARTICLE_LIST = []

    config.PLAYER.x, config.PLAYER.y = generate_player_spawn(config.MAP_INFO.map_tree)

    config.GAME_DATA.creature_data["enemy"] = generate_enemies(config.MAP_INFO.map_tree)

    config.GAME_DATA.item_data = generate_items(config.MAP_INFO.map_tree)

    config.GAME_DATA.creature_data["player"] = [config.PLAYER]


def _generate_new_map():
    """
    Generates new map with MapInfo
    """
    # Holds map info like width and height
    config.MAP_INFO = gamemap.MapInfo()


def initialize_pathfinding():
    config.PATHFINDING = pathfinding.Graph()
    config.PATHFINDING.make_graph(config.MAP_INFO)
    config.PATHFINDING.neighbour()


def new():
    """
    Makes new map and entities
    """
    _generate_new_map()

    generate_camera()

    initialize_pathfinding()

    _populate_map()


def update():
    # Update what to lock camera on
    config.CAMERA.update(config.PLAYER)

    if not config.WALL_HACK:
        config.FOV = fov.new_fov(config.MAP_INFO)

    fov.ray_casting(config.MAP_INFO, config.MAP_INFO.tile_array, config.FOV, config.PLAYER)
    fov.change_seen(config.MAP_INFO, config.MAP_INFO.tile_array, config.FOV)

    draw.draw()

    draw.draw_mouse()


def move_char_auto(path, ignore=False):
    """
    Moves current_group (player) according to path and draws character
    with slight delay to show walking animation

    Uses difference in current/old coord and new/destination coord
    to find which direction to move

    Args:
        path (list): path to take
        ignore (boolean): if true, ignore monsters showing up in FOV and
            continue moving, else stop and prevent movement
    """
    old_coord = (config.PLAYER.x, config.PLAYER.y)
    if len(path) == 0:
        if not ignore:
            # If enemy in FOV stop auto moving
            # If wall hack on disregard
            if _check_if_enemy_in_fov():
                return
        _update_creatures(0, 0)
    else:
        for coord in path:
            # If key pressed stop auto moving
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    return

            if not ignore:
                # If enemy in FOV stop auto moving
                # If wall hack on disregard
                if _check_if_enemy_in_fov():
                    return

            # Move to next coord in path
            dest_x = coord[0] - old_coord[0]
            dest_y = coord[1] - old_coord[1]
            _update_creatures(dest_x, dest_y)
            old_coord = coord

            update()
            config.CLOCK.tick(20)
            pygame.display.flip()


def _handle_mouse_event(event):
    """
    Handles mouse clicks

    Args:
        event (Event): Event to handle
    """
    if event.button == 1:
        # Check if button clicked
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button = config.BUTTON_PANEL.check_if_button_pressed(mouse_x, mouse_y)
        if button:
            button.menu_open()
            return

        # Move player to mouse click
        move_x, move_y = config.CAMERA.get_mouse_coord()

        if not config.MAP_INFO.tile_array[move_y][move_x].seen:
            return

        start = (config.PLAYER.x, config.PLAYER.y)
        goal = (move_x, move_y)
        visited = config.PATHFINDING.bfs(start, goal)
        if visited:
            path = config.PATHFINDING.find_path(start, goal, visited)
            move_char_auto(path, True)

        config.CLOCK.tick(FPS)
        update()
        pygame.display.flip()


def _handle_screen_resize(event):
    """
    Handles screen resize event

    Args:
        event (Event): Screen resize event to handle
    """
    new_width = event.w
    new_height = event.h
    # Remove if statements if left and top should be empty
    # else right and bottom is empty
    if new_width > config.MAP_INFO.pixel_width:
        config.CAMERA.camera_width = config.MAP_INFO.pixel_width
    else:
        config.CAMERA.camera_width = event.w

    if new_height > config.MAP_INFO.pixel_height:
        config.CAMERA.camera_height = config.MAP_INFO.pixel_height
    else:
        config.CAMERA.camera_height = event.h
    # This line is only used in pygame 1
    config.SURFACE_MAIN = pygame.display.set_mode((config.CAMERA.camera_width, config.CAMERA.camera_height),
                                                  pygame.RESIZABLE)


def auto_path(graph):
    """
    Automatically move the player to the
    closest unseen tile

    If # of unseen tiles is low, can use find_closest_unseen_tile_walking_distance
    without too much of a performance hit, else use the faster find_closest_unseen_tile

    Args:
        graph (Graph): Graph with nodes representing the walkable tiles
    """
    if len(config.MAP_INFO.unseen_tiles) < 75:
        start, goal = gamemap.find_closest_unseen_tile_walking_distance()
    else:
        start, goal = gamemap.find_closest_unseen_tile()

    visited = graph.bfs(start, goal)

    if visited:
        path = config.PATHFINDING.find_path(start, goal, visited)
        move_char_auto(path)


def cast_magic():
    """
    Casts lightning at mouse location and prints out the line
    it travels through currently
    """
    move_x, move_y = config.CAMERA.get_mouse_coord()
    start = (config.PLAYER.x, config.PLAYER.y)
    goal = (move_x, move_y)
    line = magic.line(start, goal, config.MAP_INFO.tile_array)
    magic.cast_lightning(config.PLAYER, line)
    # TODO: maybe change this since if player has ai but cast fireball,
    #       player would move + cast fireball at the same time
    _update_creatures(0, 0)


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        # Pygame screen
        pygame.init()
        pygame.display.set_caption("Knight's Adventure")

        # Repeat keys when held down
        pygame.key.set_repeat(350, 75)

        self.running = True

        button_manager.add_buttons()

        self.free_camera = generate_free_camera()

    def run(self):
        """
        Main game loop which takes in process player input updates screen
        """
        self.playing = True
        while self.playing:
            config.CLOCK.tick(FPS)
            self.handle_events()
            update()
            pygame.display.flip()

    def handle_events(self):
        """
        Handle player input
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            # For resizing window
            if event.type == pygame.VIDEORESIZE:
                _handle_screen_resize(event)

            # Moving to where mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                _handle_mouse_event(event)

            # Keyboard press
            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard_event(event)

    def _handle_keyboard_event(self, event):
        """
        Handles keyboard event

        Args:
            event (Event): Keyboard event to handle
        """
        # Movement
        if event.key == pygame.K_a:
            _update_creatures(-1, 0)
        elif event.key == pygame.K_d:
            _update_creatures(1, 0)
        elif event.key == pygame.K_w:
            _update_creatures(0, -1)
        elif event.key == pygame.K_q:
            _update_creatures(-1, -1)
        elif event.key == pygame.K_e:
            _update_creatures(1, -1)
        elif event.key == pygame.K_z:
            _update_creatures(-1, 1)
        elif event.key == pygame.K_c:
            _update_creatures(1, 1)
        elif event.key == pygame.K_s:
            _update_creatures(0, 1)
        elif event.key == pygame.K_x:
            _update_creatures(0, 0)

        # Mini_map
        elif event.key == pygame.K_TAB:
            toggle_minimap()

        # Pickup/Drop Item
        elif event.key == pygame.K_t:
            objects_at_player = map_items_at_coord(config.PLAYER.x, config.PLAYER.y)
            for obj in objects_at_player:
                if obj.item:
                    obj.item.pick_up(config.PLAYER)
            _update_creatures(0, 0)

        # TODO: instead of dropping last item dropped, drop mouse event in inventory
        elif event.key == pygame.K_g:
            if len(config.PLAYER.container.inventory) > 0:
                config.PLAYER.container.inventory[-1].item.drop_item(config.PLAYER, config.PLAYER.x, config.PLAYER.y)
            _update_creatures(0, 0)

        elif event.key == pygame.K_ESCAPE:
            _toggle_wallhack()

        elif event.key == pygame.K_m:
            self._toggle_camera()

        # Auto move
        elif event.key == pygame.K_v:
            auto_path(config.PATHFINDING)

        # Menu Buttons
        elif event.key == pygame.K_p:
            menu_manager.menpause_menu()
        elif event.key == pygame.K_i:
            menu_manager.inventory_menu()

        # Use magic
        elif event.key == pygame.K_SPACE:
            menu_manager.magic_targetting_menu()

        # Returns to previous level
        elif event.key == pygame.K_1:
            if config.MAP_INFO.tile_array[config.PLAYER.y][config.PLAYER.x].type == UPSTAIR:
                config.CURRENT_FLOOR -= 1
                config.GAME_DATA.transition_previous_level()

        # Goes to next level
        elif event.key == pygame.K_2:
            if config.CURRENT_FLOOR < NUM_OF_FLOOR and \
                    config.MAP_INFO.tile_array[config.PLAYER.y][config.PLAYER.x].type == DOWNSTAIR:
                config.CURRENT_FLOOR += 1
                config.GAME_DATA.transition_next_level()

        elif event.key == pygame.K_F1:
            save_game()

        elif event.key == pygame.K_F2:
            load_game()

    def _toggle_camera(self):
        camera_on = True
        x, y = config.PLAYER.x, config.PLAYER.y
        self.free_camera.x = x
        self.free_camera.y = y
        while camera_on:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        update(-1, 0)
                    elif event.key == pygame.K_d:
                        update(1, 0)
                    elif event.key == pygame.K_w:
                        update(0, -1)
                    elif event.key == pygame.K_q:
                        update(-1, -1)
                    elif event.key == pygame.K_e:
                        update(1, -1)
                    elif event.key == pygame.K_z:
                        update(-1, 1)
                    elif event.key == pygame.K_c:
                        update(1, 1)
                    elif event.key == pygame.K_s:
                        update(0, 1)
                    elif event.key == pygame.K_RETURN:
                        self._move_to_free_camera()
                        camera_on = False
                    elif event.key == pygame.K_m:
                        camera_on = False
                    elif event.key == pygame.K_ESCAPE:
                        camera_on = False

            config.CLOCK.tick(FPS)
            config.CAMERA.update(self.free_camera)
            if not config.WALL_HACK:
                config.FOV = fov.new_fov(config.MAP_INFO)

            fov.ray_casting(config.MAP_INFO, config.MAP_INFO.tile_array, config.FOV, config.PLAYER)
            fov.change_seen(config.MAP_INFO, config.MAP_INFO.tile_array, config.FOV)

            draw.draw()
            draw.draw_at_camera_offset_without_image(self.free_camera)
            pygame.display.flip()

    def _move_to_free_camera(self):
        """
        Moves to free camera location
        """
        # If tile is unexplored do nothing
        if not config.MAP_INFO.tile_array[self.free_camera.y][self.free_camera.x].seen:
            return
        start = (config.PLAYER.x, config.PLAYER.y)
        goal = (self.free_camera.x, self.free_camera.y)
        # Generates path
        visited = config.PATHFINDING.bfs(start, goal)
        # If path is generated move player
        if visited:
            path = config.PATHFINDING.find_path(start, goal, visited)
            move_char_auto(path)


def save_game():
    """
    Saves game to data/save.txt
    """
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/save.txt')
    with open(path, 'wb') as file:
        pickle.dump([config.CURRENT_FLOOR, config.TURN_COUNT,
                     config.MAP_INFO, config.PLAYER,
                     config.GAME_DATA], file)


def load_game():
    """
    Loads game from data/save.txt
    """
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/save.txt')
    with open(path, 'rb') as file:
        config.CURRENT_FLOOR, \
            config.TURN_COUNT, \
            config.MAP_INFO, \
            config.PLAYER, \
            config.GAME_DATA = pickle.load(file)
