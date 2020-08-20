import fov
import gamemap
import magic
import pathfinding
import sprite
from camera import Camera
from constant import *
from draw import Drawing
from entity_generator import *
from menu_manager import Menu_Manager
from queue import LifoQueue

pygame.font.init()


# class GameData:
#     def __init__(self):
#         self.mini_map_on = False
#         self.map_tree = None
#         self.GAME_MESSAGES = []
#         self.GAME_OBJECTS = []
#         self.ENEMIES = []
#         self.CREATURES = []
#         self.item_group = []
#         self.camera = None


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        # Pygame screen
        pygame.init()
        pygame.display.set_caption("Knight's Adventure")
        self.surface = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)

        # Repeat keys when held down
        pygame.key.set_repeat(350, 75)

        self.clock = pygame.time.Clock()

        self.turn_count = 0

        self.running = True

        # Load in all sprites
        self.game_sprites = sprite.GameSprites()

        self.drawing = Drawing(self, self.surface)
        self.menu_manager = Menu_Manager(self)

        self.drawing.add_buttons()

        self.wall_hack = False
        self.free_camera_on = False
        self.mini_map_on = False

        self.GAME_MESSAGES = []

        self.previous_levels = LifoQueue()
        self.next_levels = LifoQueue()

    def new(self):
        """
        Makes new map and entities
        """
        self._generate_new_map()

        self.camera = Camera(self.map_info)

        self._initialize_pathfinding()

        self._populate_map()

    def _populate_map(self):
        """
        Adds entities to map
        """
        # Group with all creatures
        self.all_creature = pygame.sprite.OrderedUpdates()
        # Player group
        self.player_group = []
        # Free camera group
        self.camera_group = pygame.sprite.GroupSingle()
        # Enemy group
        self.enemy_group = []

        # Particle group
        self.particles = []

        self.item_group = []

        # Switches current group to all creatures
        # the current group to move/update
        self.current_group = self.all_creature

        self.free_camera = generate_free_camera(self)

        self.player = generate_player(self.map_info.map_tree, self)

        # TODO: Fix ai for creatures merging when stepping onto same tile
        self.enemy_group = generate_enemies(self.map_info.map_tree, self)

        self.item_group = generate_items(self.map_info.map_tree, self)

        self.player_group.append(self.player)

        self.camera_group.add(self.free_camera)

        for c in self.enemy_group + self.player_group:
            self.all_creature.add(c)

    def _generate_new_map(self):
        """
        Generates new map with MapInfo
        """
        # Holds map info like width and height
        self.map_info = gamemap.MapInfo(self)

    def _initialize_pathfinding(self):
        self.graph = pathfinding.Graph()
        self.graph.make_graph(self.map_info)
        self.graph.neighbour()

    def run(self):
        """
        Main game loop which takes in process player input updates screen
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            pygame.display.flip()

    def update(self):
        # Update what to lock camera on
        if not self.free_camera_on:
            self.camera.update(self.player)
        else:
            self.camera.update(self.free_camera)

        if not self.wall_hack:
            self.fov = fov.new_fov(self.map_info)

        fov.ray_casting(self.map_info, self.map_info.map_array, self.fov, self.player)
        fov.change_seen(self.map_info, self.map_info.tile_array, self.fov, self.game_sprites.unseen_tile)

        self.drawing.draw()

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_event(event)

            # Keyboard press
            if event.type == pygame.KEYDOWN:
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
        if new_width > self.map_info.pixel_width:
            self.camera.camera_width = self.map_info.pixel_width
        else:
            self.camera.camera_width = event.w

        if new_height > self.map_info.pixel_height:
            self.camera.camera_height = self.map_info.pixel_height
        else:
            self.camera.camera_height = event.h
        # This line is only used in pygame 1
        self.surface = pygame.display.set_mode((self.camera.camera_width, self.camera.camera_height),
                                               pygame.RESIZABLE)

    def _handle_keyboard_event(self, event):
        """
        Handles keyboard event

        Args:
            event (Event): Keyboard event to handle
        """
        # Movement
        if event.key == pygame.K_a:
            self.current_group.update(-1, 0)
            self.turn_count += 1
        elif event.key == pygame.K_d:
            self.current_group.update(1, 0)
            self.turn_count += 1
        elif event.key == pygame.K_w:
            self.current_group.update(0, -1)
            self.turn_count += 1
        elif event.key == pygame.K_q:
            self.current_group.update(-1, -1)
            self.turn_count += 1
        elif event.key == pygame.K_e:
            self.current_group.update(1, -1)
            self.turn_count += 1
        elif event.key == pygame.K_z:
            self.current_group.update(-1, 1)
            self.turn_count += 1
        elif event.key == pygame.K_c:
            self.current_group.update(1, 1)
            self.turn_count += 1
        elif event.key == pygame.K_s:
            self.current_group.update(0, 1)
            self.turn_count += 1
        elif event.key == pygame.K_x:
            self.current_group.update(0, 0)
            self.turn_count += 1

        # Mini_map
        elif event.key == pygame.K_TAB:
            self.toggle_minimap()

        # Pickup/Drop Item
        elif event.key == pygame.K_t:
            objects_at_player = self.map_items_at_coord(self.player.x, self.player.y)
            for obj in objects_at_player:
                if obj.item:
                    obj.item.pick_up(self.player)
            self.turn_count += 1

        # TODO: instead of dropping last item dropped, drop mouse event in inventory
        elif event.key == pygame.K_g:
            if len(self.player.container.inventory) > 0:
                self.player.container.inventory[-1].item.drop_item(self.player, self.player.x, self.player.y)
            self.turn_count += 1

        elif event.key == pygame.K_ESCAPE:
            self._toggle_wallhack()

        elif event.key == pygame.K_m:
            self._toggle_free_camera()

        # If free camera on, enter makes you auto move to free camera location
        elif event.key == pygame.K_RETURN:
            self._move_to_free_camera()

        # Auto move
        elif event.key == pygame.K_v:
            self.auto_path(self.graph)

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
            if not self.previous_levels.empty():
                level_data = (self.player.x, self.player.y, self.map_info, self.enemy_group, self.item_group)
                self.next_levels.put(level_data)

                x, y, map_info, enemy_group, item_group = self.previous_levels.get()
                self.player.x = x
                self.player.y = y
                self.player.rect.topleft = (self.player.x * SPRITE_SIZE, self.player.y * SPRITE_SIZE)
                self.enemy_group = enemy_group
                self.item_group = item_group
                self.map_info = map_info

                for c in self.enemy_group + self.player_group:
                    self.all_creature = pygame.sprite.OrderedUpdates()
                    self.all_creature.add(c)


        # Goes to next level
        elif event.key == pygame.K_2:
            level_data = (self.player.x, self.player.y, self.map_info, self.enemy_group, self.item_group)
            self.previous_levels.put(level_data)
            if self.next_levels.empty():
                self.new()
            else:
                x, y, map_info, enemy_group, item_group = self.next_levels.get()
                self.player.x = x
                self.player.y = y
                self.player.rect.topleft = (self.player.x * SPRITE_SIZE, self.player.y * SPRITE_SIZE)
                self.enemy_group = enemy_group
                self.item_group = item_group
                self.map_info = map_info

                for c in self.enemy_group + self.player_group:
                    self.all_creature = pygame.sprite.OrderedUpdates()
                    self.all_creature.add(c)

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
            move_x, move_y = self.camera.get_mouse_coord()

            if not self.map_info.tile_array[move_y][move_x].seen:
                return

            start = (self.player.x, self.player.y)
            goal = (move_x, move_y)
            visited = self.graph.bfs(start, goal)
            if visited:
                path = self.graph.find_path(start, goal, visited)
                self.move_char_auto(path, True)

            self.clock.tick(FPS)
            self.update()
            pygame.display.flip()

    def cast_magic(self):
        """
        Casts lightning at mouse location and prints out the line
        it travels through currently

        Returns:

        """
        move_x, move_y = self.camera.get_mouse_coord()
        start = (self.player.x, self.player.y)
        goal = (move_x, move_y)
        line = magic.line(start, goal, self.map_info.map_array)
        magic.cast_fireball(self, self.player, line)
        # TODO: maybe change this since if player has ai but cast fireball,
        #       player would move + cast fireball at the same time
        self.current_group.update(0, 0)
        self.turn_count += 1

    def _move_to_free_camera(self):
        """
        Moves to free camera location
        """
        if self.free_camera_on:
            # If tile is unexplored do nothing
            if not self.map_info.tile_array[self.free_camera.y][self.free_camera.x].seen:
                return
            start = (self.player.x, self.player.y)
            goal = (self.free_camera.x, self.free_camera.y)
            # Generates path
            visited = self.graph.bfs(start, goal)
            # If path is generated move player
            if visited:
                self._toggle_free_camera()
                path = self.graph.find_path(start, goal, visited)
                self.move_char_auto(path)

    def _toggle_wallhack(self):
        """
        Toggles wallhack. If wallhack is on, then show whole map in player FOV
        else turn back to normal fov
        """
        self.wall_hack = not self.wall_hack
        if self.wall_hack:
            self.fov = [[1 for x in range(0, self.map_info.tile_width)] for y in
                        range(self.map_info.tile_height)]

    def map_items_at_coord(self, coord_x, coord_y):
        objects = [obj for obj in self.item_group if obj.x == coord_x and obj.y == coord_y]
        return objects

    def _toggle_free_camera(self):
        """
        Changes free camera. If free camera is on, make free camera
        have same position as player and make camera follow camera
        else make it follow player
        """
        self.free_camera_on = not self.free_camera_on
        if self.free_camera_on:
            self.current_group = self.camera_group
            self.free_camera.x = self.player.x
            self.free_camera.y = self.player.y
            self.free_camera.rect.topleft = self.player.rect.topleft
        else:
            self.current_group = self.all_creature

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
        old_coord = (self.player.x, self.player.y)
        if len(path) == 0:
            if not ignore:
                # If enemy in FOV stop auto moving
                # If wall hack on disregard
                if self._check_if_enemy_in_fov():
                    return
            self.current_group.update(0, 0)
            self.turn_count += 1
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
                self.current_group.update(dest_x, dest_y)
                self.turn_count += 1
                old_coord = coord

                self.update()
                self.clock.tick(20)
                pygame.display.flip()

    def _check_if_enemy_in_fov(self):
        """
        Returns:
            true if enemy is in player FOV, else false
        """
        for obj in self.enemy_group:
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
        if len(self.map_info.unseen_tiles) < 75:
            start, goal = gamemap.find_closest_unseen_tile_walking_distance(self)
        else:
            start, goal = gamemap.find_closest_unseen_tile(self)

        visited = graph.bfs(start, goal)

        if visited:
            path = self.graph.find_path(start, goal, visited)
            self.move_char_auto(path)

    def toggle_minimap(self):
        """
        Toggles minimap
        """
        self.mini_map_on = not self.mini_map_on
