import os
import pygame
import gamemap
from constant import *
import object
import components
import sprite


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        pygame.init()
        pygame.display.set_caption("Knight's Adventure")
        self.surface = pygame.display.set_mode(RESOLUTION)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 50)
        self.running = True


    def new(self):
        """
        Makes new map and entity and adds them to the relevant groups
        """
        global slime

        self.walls = pygame.sprite.Group()
        # self.floors = pygame.sprite.Group()
        self.map_tiles = gamemap.load_data()
        self.all_sprites = pygame.sprite.OrderedUpdates()

        self.game_sprites = sprite.GameSprites()

        self.camera = gamemap.Camera(self.map_tiles.width, self.map_tiles.height)

        self.map_array, self.fov = gamemap.draw_map(self.map_tiles.data, self)








        creaturetest = components.creature("Viet", 10)
        self.player = object.object(self,
            2, 6, "player", self.game_sprites.player_image, creature=creaturetest)

        creaturetest1 = components.creature("Slime", 3, components.death)

        ai_component = components.ai_test()
        slime = object.object(self, 2, 2, "enemy", self.game_sprites.slime_image,
                            creature=creaturetest1, ai=ai_component)

        # NOTE: Adding player last makes monster ai acts first (more correct)
        # but adding player first means no more monster moves, 
        # then player moves resulting in ranged attack
        self.all_sprites.add(self.player)
        self.all_sprites.add(slime)
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
                    self.all_sprites.update(-1, 0)
                if event.key == pygame.K_d:
                    self.all_sprites.update(1, 0)
                if event.key == pygame.K_w:
                    self.all_sprites.update(0, -1)
                if event.key == pygame.K_q:
                    self.all_sprites.update(-1, -1)
                if event.key == pygame.K_e:
                    self.all_sprites.update(1, -1)
                if event.key == pygame.K_z:
                    self.all_sprites.update(-1, 1)
                if event.key == pygame.K_c:
                    self.all_sprites.update(1, 1)
                if event.key == pygame.K_s:
                    self.all_sprites.update(0, 1)
                if event.key == pygame.K_x:
                    self.all_sprites.update(0, 0)

                print(self.camera.camera.topleft)
                print("player at " + str(self.player.x), str(self.player.y))
                print("player_rect at " + str(self.player.rect))
                print("slime at " + str(slime.x), str(slime.y))
                print("slime_rect at " + str(slime.rect))
                print()

    def draw_grid(self):
        for x in range(0, MAP_WIDTH, SPRITE_SIZE):
            pygame.draw.line(self.surface, GREY, (x, 0), (x, MAP_HEIGHT))

        for y in range(0, MAP_HEIGHT, SPRITE_SIZE):
            pygame.draw.line(self.surface, GREY, (0, y), (MAP_WIDTH, y))

    def draw(self):
        """
        Draws maps and entities
        """
        gamemap.ray_casting(self, self.map_array, self.fov)
        gamemap.draw_shadow(self, self.map_array, self.fov)
        for sprite in self.all_sprites:
            self.surface.blit(sprite.image, self.camera.apply(sprite))
        self.draw_grid()

        self.draw_debug()

        pygame.display.flip()

    def draw_debug(self):
        self.draw_text(self.surface, (15, MAP_HEIGHT-50), WHITE, "FPS: " + str(int(self.clock.get_fps())))

    def draw_text(self, display_surface, coord, text_color, text):
        """
        displays text at coord on given surface
        """
        text_surface, text_rect = self.text_to_objects(text, text_color)
        
        text_rect.topleft = coord

        display_surface.blit(text_surface, text_rect)

    def text_to_objects(self, inc_text, inc_color):
        text_surface = FONT_DEBUG_MESSAGE.render(inc_text, False, inc_color)
        return text_surface, text_surface.get_rect()


g = Game()
while g.running:
    g.new()
    g.run()

pygame.quit()