import os
import pygame
import gamemap
from constant import *
import object
import components
import sprite
import drawing
import pathfinding
from camera import Camera
import fov

pygame.font.init()


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        pygame.init()
        pygame.display.set_caption("Knight's Adventure")
        self.surface = pygame.display.set_mode(RESOLUTION, pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(350, 75)
        self.running = True
        self.GAME_MESSAGES = []
        self.GAME_OBJECTS = []
        self.ENEMIES = []
        self.CREATURES = []
        self.ITEMS = []
        self.drawing = drawing.Drawing(self)

    def new(self):
        """
        Makes new map and entity and adds them to the relevant groups
        """
        # Group with all walls
        self.walls = pygame.sprite.Group()
        # self.floors = pygame.sprite.Group()

        # Group with all tiles
        self.all_tile = pygame.sprite.Group()
        # Group with all creatures
        self.all_creature = pygame.sprite.OrderedUpdates()
        # Player group
        self.player_group = pygame.sprite.GroupSingle()
        # Free camera group
        self.camera_group = pygame.sprite.GroupSingle()
        # Enemy group
        self.enemy_group = pygame.sprite.Group()

        self.item_group = pygame.sprite.Group()

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
            # Holds map info like width and height
            self.map_data = gamemap.MapInfo(self.map_array)
            # Holds actual tiles
            self.tile_array = gamemap.draw_map(self.map_array, self)

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
        self.free_camera = object.object(self, 6, 6, "camera", image=self.game_sprites.spike, creature=camera)

        player_container = components.Container()
        player_com = components.Creature("Viet", 10, enemy_group=self.enemy_group)
        self.player = object.object(self,
                                    6, 6, "player", anim=self.game_sprites.knight_dict, creature=player_com, container=player_container)

        creature_com = components.Creature("Slime", 3, True, enemy_group=self.player_group)
        ai_component = components.Ai_test()
        slime = object.object(self, 2, 2, "enemy", anim=self.game_sprites.slime_dict,
                              creature=creature_com, ai=ai_component)

        # TODO: Fix ai for creatures merging when stepping onto same tile
        creaturetest2 = components.Creature("Slime1", 3, True, enemy_group=self.player_group)
        ai_component_1 = components.Ai_test()
        slime1 = object.object(self, 2, 3, "enemy", anim=self.game_sprites.slime_dict,
                               creature=creaturetest2, ai=ai_component_1)

        item_com = components.Item("Red Potion", 0, 0, True)
        item_potion = object.object(self, 3, 3, "item", image=self.game_sprites.red_potion, item=item_com)

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

    def run(self):
        """
        Main game loop which takes in process player input updates screen
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self._draw_game()


    def _draw_game(self):
        """
        Draws camera and game
        """
        if (not self.free_camera_on):
            self.camera.update(self.player)
        else:
            self.camera.update(self.free_camera)
        self.drawing.draw()


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.current_group.update(-1, 0)
            if event.key == pygame.K_d:
                self.current_group.update(1, 0)
            if event.key == pygame.K_w:
                self.current_group.update(0, -1)
            if event.key == pygame.K_q:
                self.current_group.update(-1, -1)
            if event.key == pygame.K_e:
                self.current_group.update(1, -1)
            if event.key == pygame.K_z:
                self.current_group.update(-1, 1)
            if event.key == pygame.K_c:
                self.current_group.update(1, 1)
            if event.key == pygame.K_s:
                self.current_group.update(0, 1)
            if event.key == pygame.K_x:
                self.current_group.update(0, 0)
            if event.key == pygame.K_t:
                objects_at_player = self.map_objects_at_coords(self.player.x, self.player.y)
                for obj in objects_at_player:
                    if obj.item: obj.item.pick_up(self.player)

            if event.key == pygame.K_ESCAPE:
                self.wall_hack = not self.wall_hack
                if (self.wall_hack):
                    self.fov = [[1 for x in range(0, self.map_data.tilewidth)] for y in
                                range(self.map_data.tileheight)]
            if event.key == pygame.K_m:
                self._toggle_free_camera()
            if event.key == pygame.K_RETURN:
                if (self.free_camera_on):
                    # Generates path
                    start = (self.player.x, self.player.y)
                    goal = (self.free_camera.x, self.free_camera.y)
                    visited = self.graph.bfs(start, goal)

                    # If path is generated move player
                    if (visited):
                        self._toggle_free_camera()
                        path = self.graph.find_path(start, goal, visited)
                        self._move_char_auto(path)

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
            self.free_camera
        else:
            self.current_group = self.all_creature

    def _move_char_auto(self, path):
        """
        Moves current_group (player) according to path and draws character
        with slight delay to show walking animation

        Uses difference in current/old coord and new/destination coord
        to find which direction to move

        Args:
            path (list): path to take
        """
        old_coord = (self.player.x, self.player.y)
        for coord in path:
            # If key pressed stop auto moving
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    return

            # If enemy in FOV stop auto moving
            # If wall hack on disregard
            for obj in self.enemy_group:
                print(fov.check_if_in_fov(self, obj))
                print(not self.free_camera_on)
                if (fov.check_if_in_fov(self, obj) and not self.wall_hack):
                    return

            dest_x = coord[0] - old_coord[0]
            dest_y = coord[1] - old_coord[1]
            self.current_group.update(dest_x, dest_y)
            old_coord = coord
            self._draw_game()
            pygame.time.delay(100)
