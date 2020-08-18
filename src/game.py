import os

import pygame
import ai
import container
import gamemap
import item
from constant import *
import entity
import creature
import sprite
import draw
import pathfinding
from camera import Camera
import fov
from menu_manager import Menu_Manager
import magic
from creature_gen import *

from draw import Drawing

pygame.font.init()


# class GameData:
#     def __init__(self):
#         self.mini_map_on = False
#         self.map_tree = None
#         self.GAME_MESSAGES = []
#         self.GAME_OBJECTS = []
#         self.ENEMIES = []
#         self.CREATURES = []
#         self.ITEMS = []
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

        self.running = True

        self.drawing = Drawing(self, self.surface)
        self.menu_manager = Menu_Manager(self)

        self.mini_map_on = False
        self.GAME_MESSAGES = []
        self.GAME_OBJECTS = []

    def new(self):
        """
        Makes new map and entity and adds them to the relevant groups
        """
        # List with all walls
        self.walls = []
        # List with all floors
        self.floors = []

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

        # Switches current group to all creatures
        # the current group to move/update
        self.current_group = self.all_creature

        # Load in all sprites
        self.game_sprites = sprite.GameSprites()

        # Holds map info like width and height
        self.map_info = gamemap.MapInfo(self)

        self.wall_hack = False

        self.graph = pathfinding.Graph()
        self.graph.make_graph(self.map_info.map_array, self.map_info)
        self.graph.neighbour()

        self.camera = Camera(self.map_info)

        self.free_camera_on = False

        self._add_objects()

        self.drawing.add_buttons()

    def _add_objects(self):
        """
        Adds objects to groups
        """
        self.free_camera = generate_free_camera(self)
        # camera = creature.Creature("Camera", False, walk_through_tile=True)
        # self.free_camera = entity.Entity(self, 0, 0, "camera", image=self.game_sprites.mouse_select, creature=camera)
        #

        self.player = generate_player(self.map_info.map_tree, self)
        # player_container = container.Container()
        # player_com = creature.Creature("knight", enemy_group=self.enemy_group)
        # self.player = entity.Entity(self,
        #                             6, 5, "player", anim=self.game_sprites.knight_dict, creature=player_com,
        #                             container=player_container)

        generate_enemies(self.map_info.map_tree, self)
        # creature_com = creature.Creature("slime", True, enemy_group=self.player_group)
        # ai_component = ai.SmartAi()
        # slime = entity.Entity(self, 4, 4, "enemy", anim=self.game_sprites.slime_dict,
        #                       creature=creature_com, ai=ai_component)
        #
        # # TODO: Fix ai for creatures merging when stepping onto same tile
        # creature_com1 = creature.Creature("slime", True, enemy_group=self.player_group)
        # ai_component_1 = ai.SmartAi()
        # slime1 = entity.Entity(self, 4, 5, "enemy", anim=self.game_sprites.slime_dict,
        #                        creature=creature_com1, ai=ai_component_1)
        #
        # creature_com2 = creature.Creature("goblin", True, enemy_group=self.player_group)
        # ai_component_2 = ai.SmartAi()
        # goblin = entity.Entity(self, 5, 5, "enemy", anim=self.game_sprites.goblin_dict,
        #                        creature=creature_com2, ai=ai_component_2)
        #
        # creature_com3 = creature.Creature("skeleton", True, enemy_group=self.player_group)
        # ai_component_3 = ai.SmartAi()
        # skeleton = entity.Entity(self, 5, 4, "enemy", anim=self.game_sprites.skeleton_dict,
        #                        creature=creature_com3, ai=ai_component_3)

        item_potion, item_sword = self._add_items()


        self.player_group.append(self.player)

        self.camera_group.add(self.free_camera)

        for c in self.enemy_group + self.player_group:
            self.all_creature.add(c)

        self.GAME_OBJECTS += self.enemy_group + self.player_group + self.ITEMS

    def _add_items(self):
        """
        Adds items to game
        """
        item_com = item.Item("Red Potion", 0, 0, True)
        item_potion = entity.Entity(self, 6, 7, "item", image=self.game_sprites.red_potion, item=item_com)

        item_sword_com = item.Item("Sword", 0, 0, False)
        item_sword = entity.Entity(self, 4, 4, "item", image=self.game_sprites.sword, item=item_sword_com)

        self.ITEMS = [item_potion, item_sword]

        return item_potion, item_sword

    def run(self):
        """
        Main game loop which takes in process player input updates screen
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            # self.drawing.update()
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
        elif event.key == pygame.K_d:
            self.current_group.update(1, 0)
        elif event.key == pygame.K_w:
            self.current_group.update(0, -1)
        elif event.key == pygame.K_q:
            self.current_group.update(-1, -1)
        elif event.key == pygame.K_e:
            self.current_group.update(1, -1)
        elif event.key == pygame.K_z:
            self.current_group.update(-1, 1)
        elif event.key == pygame.K_c:
            self.current_group.update(1, 1)
        elif event.key == pygame.K_s:
            self.current_group.update(0, 1)
        elif event.key == pygame.K_x:
            self.current_group.update(0, 0)

        # Mini_map
        elif event.key == pygame.K_TAB:
            self.toggle_minimap()

        # Pickup/Drop Item
        elif event.key == pygame.K_t:
            objects_at_player = self.map_objects_at_coords(self.player.x, self.player.y)
            for obj in objects_at_player:
                if obj.item:
                    obj.item.pick_up(self.player)

        # TODO: instead of dropping last item dropped, drop mouse event in inventory
        elif event.key == pygame.K_g:
            if len(self.player.container.inventory) > 0:
                self.player.container.inventory[-1].item.drop_item(self.player, self.player.x, self.player.y)

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

    def map_objects_at_coords(self, coord_x, coord_y):
        objects = [obj for obj in self.GAME_OBJECTS if obj.x == coord_x and obj.y == coord_y]
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
            self.current_group.update(0, 0)
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
                    for obj in self.enemy_group:
                        if fov.check_if_in_fov(self, obj) and not self.wall_hack:
                            return

                # Move to next coord in path
                dest_x = coord[0] - old_coord[0]
                dest_y = coord[1] - old_coord[1]
                self.current_group.update(dest_x, dest_y)
                old_coord = coord

                self.update()
                self.clock.tick(20)
                pygame.display.flip()

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
