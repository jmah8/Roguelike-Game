from constant import *
import config
import fov
import gamemap
import magic
import pathfinding
import sprite
from camera import Camera
from draw import Drawing
from entity_generator import *
from menu_manager import Menu_Manager
from queue import LifoQueue
import pickle

pygame.font.init()

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

        self.drawing = Drawing(self, config.SURFACE_MAIN)
        self.menu_manager = Menu_Manager(self)

        self.drawing.add_buttons()

        self.wall_hack = False
        self.mini_map_on = False

        self.GAME_MESSAGES = []

        self.previous_levels = LifoQueue()
        self.next_levels = LifoQueue()

        self.creature_data = {
            "player": [],
            "enemy": []
        }

        self.free_camera = generate_free_camera(self)

        self.particles = []

        self.floor = 1

    def new(self):
        """
        Makes new map and entities
        """
        self._generate_new_map()

        self._generate_camera()

        self._initialize_pathfinding()

        self._populate_map()

    def _generate_camera(self):
        """
        Generates camera
        """
        config.CAMERA = Camera(config.MAP_INFO)

    def _populate_map(self):
        """
        Adds entities to map

        Only makes new player on start, then it moves player
        to random location after
        """
        # Particle group
        self.particles = []

        if config.TURN_COUNT == 0:
            config.PLAYER = generate_player(config.MAP_INFO.map_tree, self)
        else:
            config.PLAYER.x, config.PLAYER.y = generate_player_spawn(config.MAP_INFO.map_tree)

        self.creature_data["enemy"] = generate_enemies(config.MAP_INFO.map_tree, self)

        self.item_group = generate_items(config.MAP_INFO.map_tree, self)

        self.creature_data["player"] = [config.PLAYER]

    def _generate_new_map(self):
        """
        Generates new map with MapInfo
        """
        # Holds map info like width and height
        config.MAP_INFO = gamemap.MapInfo()

    def _initialize_pathfinding(self):
        config.PATHFINDING = pathfinding.Graph()
        config.PATHFINDING.make_graph(config.MAP_INFO)
        config.PATHFINDING.neighbour()

    def run(self):
        """
        Main game loop which takes in process player input updates screen
        """
        self.playing = True
        while self.playing:
            config.CLOCK.tick(FPS)
            self.handle_events()
            self.update()
            pygame.display.flip()

    def update(self):
        # Update what to lock camera on
        config.CAMERA.update(config.PLAYER)

        if not self.wall_hack:
            self.fov = fov.new_fov(config.MAP_INFO)

        fov.ray_casting(config.MAP_INFO, config.MAP_INFO.tile_array, self.fov, config.PLAYER)
        fov.change_seen(config.MAP_INFO, config.MAP_INFO.tile_array, self.fov)

        self.drawing.draw()

        self.drawing.draw_mouse()

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
                self._handle_screen_resize(event)

            # Moving to where mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_event(event)

            # Keyboard press
            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard_event(event)

    def _handle_screen_resize(self, event):
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

    def _handle_keyboard_event(self, event):
        """
        Handles keyboard event

        Args:
            event (Event): Keyboard event to handle
        """
        # Movement
        if event.key == pygame.K_a:
            self._update_creatures(-1, 0)
        elif event.key == pygame.K_d:
            self._update_creatures(1, 0)
        elif event.key == pygame.K_w:
            self._update_creatures(0, -1)
        elif event.key == pygame.K_q:
            self._update_creatures(-1, -1)
        elif event.key == pygame.K_e:
            self._update_creatures(1, -1)
        elif event.key == pygame.K_z:
            self._update_creatures(-1, 1)
        elif event.key == pygame.K_c:
            self._update_creatures(1, 1)
        elif event.key == pygame.K_s:
            self._update_creatures(0, 1)
        elif event.key == pygame.K_x:
            self._update_creatures(0, 0)

        # Mini_map
        elif event.key == pygame.K_TAB:
            self.toggle_minimap()

        # Pickup/Drop Item
        elif event.key == pygame.K_t:
            objects_at_player = self.map_items_at_coord(config.PLAYER.x, config.PLAYER.y)
            for obj in objects_at_player:
                if obj.item:
                    obj.item.pick_up(config.PLAYER)
            self._update_creatures(0, 0)

        # TODO: instead of dropping last item dropped, drop mouse event in inventory
        elif event.key == pygame.K_g:
            if len(config.PLAYER.container.inventory) > 0:
                config.PLAYER.container.inventory[-1].item.drop_item(config.PLAYER, config.PLAYER.x, config.PLAYER.y)
            self._update_creatures(0, 0)

        elif event.key == pygame.K_ESCAPE:
            self._toggle_wallhack()

        elif event.key == pygame.K_m:
            self._toggle_camera()

        # Auto move
        elif event.key == pygame.K_v:
            self.auto_path(config.PATHFINDING)

        # Menu Buttons
        elif event.key == pygame.K_p:
            self.menu_manager.pause_menu()
        elif event.key == pygame.K_i:
            self.menu_manager.inventory_menu()

        # Use magic
        elif event.key == pygame.K_SPACE:
            self.menu_manager.magic_targetting_menu()

        # Returns to previous level
        elif event.key == pygame.K_1:
            if config.MAP_INFO.tile_array[config.PLAYER.y][config.PLAYER.x].type == UPSTAIR:
                self.floor -= 1
                self.transition_previous_level()

        # Goes to next level
        elif event.key == pygame.K_2:
            if self.floor < NUM_OF_FLOOR and config.MAP_INFO.tile_array[config.PLAYER.y][config.PLAYER.x].type == DOWNSTAIR:
                self.floor += 1
                self.transition_next_level()

        elif event.key == pygame.K_9:
            s = pickle.dumps(config.MAP_INFO.tile_array)
            print(s)

    def _handle_mouse_event(self, event):
        """
        Handles mouse clicks

        Args:
            event (Event): Event to handle
        """
        if event.button == 1:
            # Check if button clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button = self.drawing.button_manager.check_if_button_pressed(mouse_x, mouse_y)
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
                self.move_char_auto(path, True)

            config.CLOCK.tick(FPS)
            self.update()
            pygame.display.flip()

    def _update_creatures(self, dx, dy):
        """
        Updates all creatures and increments turn count

        Args:
            dx (int): x to move player by
            dy (int): y to move player by
        """
        for team in self.creature_data:
            for entity in self.creature_data[team]:
                entity.update(dx, dy)
        config.TURN_COUNT += 1

    def transition_previous_level(self):
        """
        Go to previous level
        """
        if not self.previous_levels.empty():
            # Saves current level to next level list
            level_data = (config.PLAYER.x, config.PLAYER.y, config.MAP_INFO, self.creature_data["enemy"], self.item_group)
            self.next_levels.put(level_data)

            x, y, map_info, enemy_list, item_group = self.previous_levels.get()

            self._load_level_data(enemy_list, item_group, map_info, x, y)

    def transition_next_level(self):
        """
        Goes to next level
        """
        level_data = (config.PLAYER.x, config.PLAYER.y, config.MAP_INFO, self.creature_data["enemy"], self.item_group)
        self.previous_levels.put(level_data)

        if self.next_levels.empty():
            self.new()
            # Places upstair at where the player entered the map at
            config.MAP_INFO.tile_array[config.PLAYER.y][config.PLAYER.x].type = UPSTAIR
        else:
            x, y, map_info, enemy_list, item_group = self.next_levels.get()

            self._load_level_data(enemy_list, item_group, map_info, x, y)

    def _load_level_data(self, enemy_list, item_group, map_info, x, y):
        """
        Loads level data to game variables

        Args:
            enemy_list (List): list of enemies on level
            item_group (List): list of items on level
            map_info (MapInfo): map info of level
            x (int): player's x position on level
            y (int): player's y position on level
        """
        config.PLAYER.x = x
        config.PLAYER.y = y
        self.creature_data["enemy"] = enemy_list
        self.item_group = item_group
        config.MAP_INFO = map_info
        self._generate_camera()
        self._initialize_pathfinding()

    def _toggle_camera(self):
        camera_on = True
        x, y = config.PLAYER.x, config.PLAYER.y
        self.free_camera.x = x
        self.free_camera.y = y
        # self.free_camera.rect.topleft = (self.free_camera.x * SPRITE_SIZE, self.free_camera.y * SPRITE_SIZE)
        while camera_on:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.free_camera.update(-1, 0)
                    elif event.key == pygame.K_d:
                        self.free_camera.update(1, 0)
                    elif event.key == pygame.K_w:
                        self.free_camera.update(0, -1)
                    elif event.key == pygame.K_q:
                        self.free_camera.update(-1, -1)
                    elif event.key == pygame.K_e:
                        self.free_camera.update(1, -1)
                    elif event.key == pygame.K_z:
                        self.free_camera.update(-1, 1)
                    elif event.key == pygame.K_c:
                        self.free_camera.update(1, 1)
                    elif event.key == pygame.K_s:
                        self.free_camera.update(0, 1)
                    elif event.key == pygame.K_RETURN:
                        self._move_to_free_camera()
                        camera_on = False
                    elif event.key == pygame.K_m:
                        camera_on = False

            config.CLOCK.tick(FPS)
            config.CAMERA.update(self.free_camera)
            if not self.wall_hack:
                self.fov = fov.new_fov(config.MAP_INFO)

            fov.ray_casting(config.MAP_INFO, config.MAP_INFO.tile_array, self.fov, config.PLAYER)
            fov.change_seen(config.MAP_INFO, config.MAP_INFO.tile_array, self.fov)

            self.drawing.draw()
            self.drawing.draw_at_camera_offset_without_image(self.free_camera)
            pygame.display.flip()

    def cast_magic(self):
        """
        Casts lightning at mouse location and prints out the line
        it travels through currently
        """
        move_x, move_y = config.CAMERA.get_mouse_coord()
        start = (config.PLAYER.x, config.PLAYER.y)
        goal = (move_x, move_y)
        line = magic.line(start, goal, config.MAP_INFO.tile_array)
        magic.cast_lightning(self, config.PLAYER, line)
        # TODO: maybe change this since if player has ai but cast fireball,
        #       player would move + cast fireball at the same time
        self._update_creatures(0, 0)

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
            self.move_char_auto(path)

    def _toggle_wallhack(self):
        """
        Toggles wallhack. If wallhack is on, then show whole map in player FOV
        else turn back to normal fov
        """
        self.wall_hack = not self.wall_hack
        if self.wall_hack:
            self.fov = [[1 for x in range(0, config.MAP_INFO.tile_width)] for y in
                        range(config.MAP_INFO.tile_height)]

    def map_items_at_coord(self, coord_x, coord_y):
        """
        Returns list of items at (coord_x, coord_y)

        Args:
            coord_x (int): x coord on map
            coord_y (int): y coord on map

        Returns:
            objects (List): list of items at (coord_x, coord_y)
        """
        objects = [obj for obj in self.item_group if obj.x == coord_x and obj.y == coord_y]
        return objects

    def move_char_auto(self, path, ignore=False):
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
                if self._check_if_enemy_in_fov():
                    return
            self._update_creatures(0, 0)
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
                    if self._check_if_enemy_in_fov():
                        return

                # Move to next coord in path
                dest_x = coord[0] - old_coord[0]
                dest_y = coord[1] - old_coord[1]
                self._update_creatures(dest_x, dest_y)
                old_coord = coord

                self.update()
                config.CLOCK.tick(20)
                pygame.display.flip()

    def _check_if_enemy_in_fov(self):
        """
        Returns:
            true if enemy is in player FOV, else false
        """
        for obj in self.creature_data["enemy"]:
            if fov.check_if_in_fov(self, obj) and not self.wall_hack:
                return True
        return False

    def auto_path(self, graph):
        """
        Automatically move the player to the
        closest unseen tile

        If # of unseen tiles is low, can use find_closest_unseen_tile_walking_distance
        without too much of a performance hit, else use the faster find_closest_unseen_tile

        Args:
            graph (Graph): Graph with nodes representing the walkable tiles
        """
        if len(config.MAP_INFO.unseen_tiles) < 75:
            start, goal = gamemap.find_closest_unseen_tile_walking_distance(self)
        else:
            start, goal = gamemap.find_closest_unseen_tile(self)

        visited = graph.bfs(start, goal)

        if visited:
            path = config.PATHFINDING.find_path(start, goal, visited)
            self.move_char_auto(path)

    def toggle_minimap(self):
        """
        Toggles minimap
        """
        self.mini_map_on = not self.mini_map_on
