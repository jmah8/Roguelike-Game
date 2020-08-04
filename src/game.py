import os
import pygame
import ai
import gamemap
from constant import *
import object
import components
import sprite
import drawing
import pathfinding
from camera import Camera
import fov
from menu_manager import Menu_Manager

from drawing import Drawing

pygame.font.init()


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        pygame.init()
        pygame.display.set_caption("Knight's Adventure")
        self.surface = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
        self.map_tree = None
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(350, 75)
        self.running = True
        self.GAME_MESSAGES = []
        self.GAME_OBJECTS = []
        self.ENEMIES = []
        self.CREATURES = []
        self.ITEMS = []
        self.drawing = Drawing(self)
        self.menu_manager = Menu_Manager(self)
        self.mini_map_on = False

    def new(self):
        """
        Makes new map and entity and adds them to the relevant groups
        """
        # Group with all walls
        self.walls = pygame.sprite.Group()
        # self.floors = pygame.sprite.Group()

        # Group with all tiles
        self.all_tile = pygame.sprite.Group()
        # Minimap group
        self.minimap = pygame.sprite.Group()
        # Group with all creatures
        self.all_creature = pygame.sprite.OrderedUpdates()
        # Player group
        self.player_group = pygame.sprite.GroupSingle()
        # Free camera group
        self.camera_group = pygame.sprite.GroupSingle()
        # Enemy group
        self.enemy_group = pygame.sprite.Group()

        self.item_group = pygame.sprite.Group()

        # Particle group
        self.particles = pygame.sprite.Group()

        # Switches current group to all creatures
        # the current group to move/update
        self.current_group = self.all_creature

        # Load in all sprites
        self.game_sprites = sprite.GameSprites()

        # Load map data
        # This is for reading maps from text files
        if (READ_FROM_FILE):
            # Holds the map representation (chars)
            self.map_array = gamemap.load_map()

        # This is for generating random maps
        else:
            # Holds the map representation (chars)
            self.map_array = gamemap.gen_map(self)

        # Holds map info like width and height
        self.map_data = gamemap.MapInfo(self.map_array)
        # Holds actual tiles
        self.tile_array = gamemap.draw_map(self.map_array, self)

        self.wall_hack = False

        self.graph = pathfinding.Graph()
        self.graph.make_graph(self.map_array, self.map_data)
        self.graph.neighbour()

        self.camera = Camera(
            self.map_data.width, self.map_data.height)

        self.free_camera_on = False
        camera = components.Creature("Camera", 999, False, walk_through_tile=True)
        self.free_camera = object.object(self, 6, 6, "camera", image=self.game_sprites.mouse_select, creature=camera)

        player_container = components.Container()

        player_com = components.Creature("Viet", 10, enemy_group=self.enemy_group)
        self.player = object.object(self,
                                    6, 6, "player", anim=self.game_sprites.knight_dict, creature=player_com,
                                    container=player_container)

        creature_com = components.Creature("Slime", 3, True, enemy_group=self.player_group)
        ai_component = ai.SmartAi()
        slime = object.object(self, 2, 2, "enemy", anim=self.game_sprites.slime_dict,
                              creature=creature_com, ai=ai_component)

        # TODO: Fix ai for creatures merging when stepping onto same tile
        creaturetest2 = components.Creature("Slime1", 3, True, enemy_group=self.player_group)
        ai_component_1 = ai.SmartAi()
        slime1 = object.object(self, 2, 3, "enemy", anim=self.game_sprites.slime_dict,
                               creature=creaturetest2, ai=ai_component_1)

        item_com = components.Item("Red Potion", 0, 0, True)
        item_potion = object.object(self, 6, 7, "item", image=self.game_sprites.red_potion, item=item_com)

        self.ITEMS = [item_potion]
        for i in self.ITEMS:
            self.item_group.add(i)

        self.CREATURES = [self.player, slime, slime1]
        for c in self.CREATURES:
            self.all_creature.add(c)

        self.player.add(self.player_group)
        self.camera_group.add(self.free_camera)

        self.ENEMIES = [slime, slime1]
        for e in self.ENEMIES:
            self.enemy_group.add(e)

        self.GAME_OBJECTS = [item_potion, slime1, slime, self.player]

        self.drawing.add_buttons()

    def run(self):
        """
        Main game loop which takes in process player input updates screen
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.drawing.draw()
            pygame.display.flip()

    def events(self):
        """
        Handle player input
        """
        events = pygame.event.get()
        for event in events:
            self._game_handle_keys(event)

    def _game_handle_keys(self, event):
        if event.type == pygame.QUIT:
            if self.playing:
                self.playing = False
            self.running = False

        # For resizing window
        if event.type == pygame.VIDEORESIZE:
            new_width = event.w
            new_height = event.h
            # Remove if statements if left and top should be empty
            # else right and bottom is empty
            if (new_width > self.map_data.width):
                self.camera.camera_width = self.map_data.width
            else:
                self.camera.camera_width = event.w

            if (new_height > self.map_data.height):
                self.camera.camera_height = self.map_data.height
            else:
                self.camera.camera_height = event.h
            # This line is only used in pygame 1
            self.surface = pygame.display.set_mode((self.camera.camera_width, self.camera.camera_height),
                                                   pygame.RESIZABLE)
        # Moving to where mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button = self.drawing.button_manager.check_if_button_pressed(mouse_x, mouse_y)
                if button:
                    button()

                mouse_x = mouse_x // SPRITE_SIZE
                mouse_y = mouse_y // SPRITE_SIZE
                resol_x = self.camera.camera_width // SPRITE_SIZE
                resol_y = self.camera.camera_height // SPRITE_SIZE
                move_x = mouse_x
                move_y = mouse_y

                # If map is smaller than resol, this fixes the issue of
                # the mouse coord and map coord not being in sync
                if (self.map_data.tilewidth < resol_x):
                    move_x = mouse_x - (resol_x - self.map_data.tilewidth)
                if (self.map_data.tileheight < resol_y):
                    move_y = mouse_y - (resol_y - self.map_data.tileheight)

                if (not self.tile_array[move_y][move_x].seen):
                    return
                start = (self.player.x, self.player.y)
                goal = (move_x, move_y)
                visited = self.graph.bfs(start, goal)
                if (visited):
                    path = self.graph.find_path(start, goal, visited)
                    self.move_char_auto(path, True)
                self.clock.tick(FPS)
                self.drawing.draw()
                pygame.display.flip()


        if event.type == pygame.KEYDOWN:

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
                self.mini_map_on = not self.mini_map_on

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
                self.wall_hack = not self.wall_hack
                if (self.wall_hack):
                    self.fov = [[1 for x in range(0, self.map_data.tilewidth)] for y in
                                range(self.map_data.tileheight)]

            elif event.key == pygame.K_m:
                self._toggle_free_camera()

            # If free camera on, enter makes you auto move to free canera location
            elif event.key == pygame.K_RETURN:
                if (self.free_camera_on):
                    # If tile is unexplored do nothing
                    if (not self.tile_array[self.free_camera.y][self.free_camera.x].seen):
                        return
                    start = (self.player.x, self.player.y)
                    goal = (self.free_camera.x, self.free_camera.y)
                    # Generates path
                    visited = self.graph.bfs(start, goal)
                    # If path is generated move player
                    if (visited):
                        self._toggle_free_camera()
                        path = self.graph.find_path(start, goal, visited)
                        self.move_char_auto(path)

            # Auto move
            elif event.key == pygame.K_v:
                self.auto_path(self.graph)

            # Menu Buttons
            elif event.key == pygame.K_p:
                self.menu_manager.pause_menu()
            elif event.key == pygame.K_i:
                self.menu_manager.inventory_menu()

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
        if (self.free_camera_on):
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
                        if (fov.check_if_in_fov(self, obj) and not self.wall_hack):
                            return

                dest_x = coord[0] - old_coord[0]
                dest_y = coord[1] - old_coord[1]
                self.current_group.update(dest_x, dest_y)
                old_coord = coord
                self.drawing.draw()
                self.clock.tick(15)
                pygame.display.flip()

    def auto_path(self, graph):
        """
        Automatically move the player to the
        closest unseen tile

        Args:
            graph (Graph): Graph with nodes representing the walkable tiles
        """
        start, goal = gamemap.find_closest_unseen_tile_walking_distance(self)
        visited = graph.bfs(start, goal)
        if visited:
            path = self.graph.find_path(start, goal, visited)
            self.move_char_auto(path)

