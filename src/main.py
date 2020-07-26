import os
import pygame
import gamemap
from constant import *
import object
import components
import sprite
import pathfinding

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

    def new(self):
        """
        Makes new map and entity and adds them to the relevant groups
        """
        global slime

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
        self.enemies = pygame.sprite.Group()

        # Switches current group to all creatures
        self.current_group = self.all_creature

        # Load in all sprites
        self.game_sprites = sprite.GameSprites()

        # Load map data
        # This is for reading maps from text files
        if (READ_FROM_FILE):
            self.map_tiles = gamemap.load_data()
            self.map_array = gamemap.draw_tiles(self.map_tiles.data, self)
        else:
        # This is for generating random maps
            self.map_array, self.data_array = gamemap.gen_map(self)
            self.map_tiles = gamemap.MapInfo(self.map_array)
        self.wall_hack = False

        self.graph = pathfinding.Graph()
        self.graph.make_graph(self.data_array, self.map_tiles)
        self.graph.neighbour()

        self.camera = gamemap.Camera(
            self.map_tiles.width, self.map_tiles.height)


        self.free_camera_on = False
        camera = components.creature("Camera", 999, False, walk_through_tile=True)
        self.free_camera = object.object(self, 6, 6, "camera", image=self.game_sprites.spike, creature=camera)



        creaturetest = components.creature("Viet", 10, enemy_group=self.enemies)
        self.player = object.object(self,
                                    3, 3, "player", anim=self.game_sprites.knight_dict, creature=creaturetest)

        creaturetest1 = components.creature("Slime", 3, True, enemy_group=self.player_group)
        ai_component = components.ai_test()
        slime = object.object(self, 1, 1, "enemy", anim=self.game_sprites.slime_dict,
                              creature=creaturetest1, ai=ai_component)

        # TODO: Fix ai for creatures merging when stepping onto same tile
        creaturetest2 = components.creature("Slime1", 3, True, enemy_group=self.player_group)
        ai_component_1 = components.ai_test()
        slime1 = object.object(self, 1, 2, "enemy", anim=self.game_sprites.slime_dict,
                              creature=creaturetest2, ai=ai_component_1)
                              

        # NOTE: Adding player last makes monster ai acts first (more correct)
        # but adding player first means no more monster moves,
        # then player moves resulting in ranged attack
        self.all_creature.add(self.player)
        self.all_creature.add(slime)
        self.all_creature.add(slime1)

        self.player_group.add(self.player)

        self.camera_group.add(self.free_camera)

        self.enemies.add(slime)
        self.enemies.add(slime1)
        self.run()

    def run(self):
        """
        Main game loop which takes in process player input updates screen    
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if (not self.free_camera_on):
                self.camera.update(self.player)
            else:
                self.camera.update(self.free_camera)
            self.draw()

    def events(self):
        """
        Handle player input
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.VIDEORESIZE:
                new_width = event.w
                new_height = event.h
                # Remove if statements if left and top should be empty
                # else right and bottom is empty
                if (new_width > self.map_tiles.width):
                    self.camera.camera_width = self.map_tiles.width
                else:
                    self.camera.camera_width = event.w
                
                if (new_height > self.map_tiles.height):
                    self.camera.camera_height = self.map_tiles.height
                else:
                    self.camera.camera_height = event.h
                # This line is only used in pygame 1
                self.surface = pygame.display.set_mode((self.camera.camera_width, self.camera.camera_height), pygame.RESIZABLE)

            self._handle_key(event)

    def _handle_key(self, event):
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
            if event.key == pygame.K_ESCAPE:
                self.wall_hack = not self.wall_hack
                if (self.wall_hack):
                    self.fov = [[1 for x in range (0, self.map_tiles.tilewidth)] for y in range (self.map_tiles.tileheight)]
            if event.key == pygame.K_m:
                self.free_camera_on = not self.free_camera_on
                if (self.free_camera_on):
                    self.current_group = self.camera_group
                    self.free_camera.x = self.player.x
                    self.free_camera.y = self.player.y
                    self.free_camera.rect.topleft = self.player.rect.topleft
                else:
                    self.current_group = self.all_creature
            if event.key == pygame.K_RETURN:
                if (self.free_camera_on):
                    start = (self.player.x, self.player.y)
                    goal = (self.free_camera.x, self.free_camera.y)
                    visited = self.graph.bfs(start, goal)
                    if (visited):
                        self.current_group = self.all_creature
                        path = self.graph.find_path(start, goal, visited)
                        temp_coord = None
                        # TODO: center camera on player when moving
                        for coord in path:
                            if (not temp_coord):
                                temp_coord = coord
                            else:
                                move_x = coord[0] - temp_coord[0]
                                move_y = coord[1] - temp_coord[1]
                                self.current_group.update(move_x, move_y)
                                temp_coord = coord
                            self.draw()
                            pygame.time.delay(100)
                            
                self.current_group = self.camera_group



    def draw_grid(self):
        """
        Draws grid
        """
        for x in range(0, self.camera.camera_width, SPRITE_SIZE):
            pygame.draw.line(self.surface, GREY, (x, 0), (x, self.camera.camera_height))

        for y in range(0, self.camera.camera_height, SPRITE_SIZE):
            pygame.draw.line(self.surface, GREY, (0, y), (self.camera.camera_width, y))

    def draw(self):
        """
        Draws maps and entities
        """
        if (not self.wall_hack):
            self.fov = gamemap.new_fov(self)
        gamemap.ray_casting(self, self.map_array, self.fov)
        gamemap.draw_seen(self, self.map_array, self.fov)

        # Draws all tiles
        for tile in self.all_tile:
            self.surface.blit(tile.image, self.camera.apply(tile))

        if (self.free_camera_on):
            self.surface.blit(self.free_camera.image, self.camera.apply(self.free_camera))

        # Draws creature if it is in player fov
        for obj in self.all_creature:
            if gamemap.check_if_in_fov(self, obj):  
                obj.update_anim()            
                self.surface.blit(obj.image, self.camera.apply(obj))


        self.draw_grid()

        self.draw_debug()
        self.draw_messages()
        pygame.display.flip()

    def draw_debug(self):
        """
        Draws FPS counter on top right of screen
        """
        self.draw_text(self.surface, (self.camera.camera_width-125, 15), WHITE,
                       "FPS: " + str(int(self.clock.get_fps())), BLACK)

    def draw_text(self, display_surface, coord, text_color, text, text_bg_color=None):
        """
        displays text at coord on given surface

        Arg:
            display_surface (surface, arg): surface to draw to
            coord ((int, int), arg): coord to draw to
            text_color (color, arg): color of text
            text (string, arg): text to draw
            text_bg_color (color, arg): background color of text
        """
        text_surface, text_rect = self._text_to_objects_helper(
            text, text_color, text_bg_color)

        text_rect.topleft = coord

        display_surface.blit(text_surface, text_rect)

    def _text_to_objects_helper(self, inc_text, inc_color, inc_bg_color):
        """
        Helper function for draw_text. Returns the text surface and rect
    
        Arg:
            inc_text (string): text to draw
            inc_color (color, arg): color of text
            inc_bg_color (color, arg): background color of text
        """
        if inc_bg_color:
            text_surface = FONT_DEBUG_MESSAGE.render(
                inc_text, False, inc_color, inc_bg_color)
        else:
            text_surface = FONT_DEBUG_MESSAGE.render(
                inc_text, False, inc_color,)
        return text_surface, text_surface.get_rect()

    def _text_height_helper(self, font):
        font_object = font.render('a', False, (0, 0, 0))
        font_rect = font_object.get_rect()
        return font_rect.height

    def print_game_message(self, ingame_message, message_color):
        self.GAME_MESSAGES.append((ingame_message, message_color))

    def draw_messages(self):

        # last NUM_MESSAGES will be drawn
        if len(self.GAME_MESSAGES) <= NUM_MESSAGES:
            to_draw = self.GAME_MESSAGES
        else:
            to_draw = self.GAME_MESSAGES[-NUM_MESSAGES:]

        text_height = self._text_height_helper(FONT_MESSAGE_TEXT)
        y_pos = self.camera.camera_height - (NUM_MESSAGES*text_height) - TEXT_SPACE_BUFFER
        i = 0
        for message, color in to_draw:
            self.draw_text(self.surface, (TEXT_SPACE_BUFFER,
                                          (y_pos + i*text_height)), color, message, None)
            i += 1


g = Game()
while g.running:
    g.new()
    g.run()

pygame.quit()
