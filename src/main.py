import os
import pygame
import gamemap
from constant import *
import object
import components
import sprite

pygame.font.init()


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        pygame.init()
        pygame.display.set_caption("Knight's Adventure")
        self.surface = pygame.display.set_mode(RESOLUTION)
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
        self.map_tiles = gamemap.load_data()
        # Group with all tiles
        self.all_tile = pygame.sprite.Group()
        # Group with all creatures
        self.all_creature = pygame.sprite.OrderedUpdates()

        # Load in all sprites
        self.game_sprites = sprite.GameSprites()

        self.camera = gamemap.Camera(
            self.map_tiles.width, self.map_tiles.height)

        self.map_array = gamemap.draw_map(self.map_tiles.data, self)

        creaturetest = components.creature("Viet", 10)
        self.player = object.object(self,
                                    6, 6, "player", anim=self.game_sprites.knight_dict, creature=creaturetest)

        creaturetest1 = components.creature("Slime", 3, True)

        ai_component = components.ai_test()
        slime = object.object(self, 2, 2, "enemy", anim=self.game_sprites.slime_dict,
                              creature=creaturetest1, ai=ai_component)
                              

        # NOTE: Adding player last makes monster ai acts first (more correct)
        # but adding player first means no more monster moves,
        # then player moves resulting in ranged attack
        self.all_creature.add(self.player)
        self.all_creature.add(slime)

        self.player_group = pygame.sprite.GroupSingle()
        self.player_group.add(self.player)

        self.enemies = pygame.sprite.Group()
        self.enemies.add(slime)
        self.run()

    def run(self):
        """
        Main game loop which takes in process player input updates screen    
        """
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.camera.update(self.player)
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.all_creature.update(-1, 0)
                if event.key == pygame.K_d:
                    self.all_creature.update(1, 0)
                if event.key == pygame.K_w:
                    self.all_creature.update(0, -1)
                if event.key == pygame.K_q:
                    self.all_creature.update(-1, -1)
                if event.key == pygame.K_e:
                    self.all_creature.update(1, -1)
                if event.key == pygame.K_z:
                    self.all_creature.update(-1, 1)
                if event.key == pygame.K_c:
                    self.all_creature.update(1, 1)
                if event.key == pygame.K_s:
                    self.all_creature.update(0, 1)
                if event.key == pygame.K_x:
                    self.all_creature.update(0, 0)

                # print(self.camera.camera.topleft)
                # print("player at " + str(self.player.x), str(self.player.y))
                # print("player_rect at " + str(self.player.rect))
                # print("slime at " + str(slime.x), str(slime.y))
                # print("slime_rect at " + str(slime.rect))
                # print()

    def draw_grid(self):
        """
        Draws grid
        """
        for x in range(0, CAMERA_WIDTH, SPRITE_SIZE):
            pygame.draw.line(self.surface, GREY, (x, 0), (x, CAMERA_HEIGHT))

        for y in range(0, CAMERA_HEIGHT, SPRITE_SIZE):
            pygame.draw.line(self.surface, GREY, (0, y), (CAMERA_WIDTH, y))

    def draw(self):
        """
        Draws maps and entities
        """
        self.fov = gamemap.new_fov(self)
        gamemap.ray_casting(self, self.map_array, self.fov)
        gamemap.draw_seen(self, self.map_array, self.fov)

        # Draws all tiles
        for tile in self.all_tile:
            self.surface.blit(tile.image, self.camera.apply(tile))

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
        self.draw_text(self.surface, (CAMERA_WIDTH-125, 15), WHITE,
                       "FPS: " + str(int(self.clock.get_fps())), BLACK)

    def draw_text(self, display_surface, coord, text_color, text, text_bg_color=None):
        """
        displays text at coord on given surface
        """
        text_surface, text_rect = self.text_to_objects_helper(
            text, text_color, text_bg_color)

        text_rect.topleft = coord

        display_surface.blit(text_surface, text_rect)

    def text_to_objects_helper(self, inc_text, inc_color, inc_bg_color):
        if inc_bg_color:
            text_surface = FONT_DEBUG_MESSAGE.render(
                inc_text, False, inc_color, inc_bg_color)
        else:
            text_surface = FONT_DEBUG_MESSAGE.render(
                inc_text, False, inc_color,)
        return text_surface, text_surface.get_rect()

    def text_height_helper(self, font):
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

        text_height = self.text_height_helper(FONT_MESSAGE_TEXT)
        y_pos = CAMERA_HEIGHT - (NUM_MESSAGES*text_height) - TEXT_SPACE_BUFFER
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
