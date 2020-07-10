import os
import pygame
import gamemap
import constant
import object
import components


class Game:
    def __init__(self):
        """
        Initializes pygame
        """
        pygame.init()

        self.surface = pygame.display.set_mode(constant.RESOLUTION)
        pygame.display.set_caption('My Pygame')

        self.clock = pygame.time.Clock()
        self.running = True


    def new(self):
        """
        Makes new map and entity
        """
        global player, slime

        self.walls = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.map_tiles = gamemap.load_data()

        creaturetest = components.creature("Viet", 10)
        player = object.object(
            1, 1, "player", constant.CHARACTER, creature=creaturetest)

        creaturetest1 = components.creature("Slime", 3, components.death)

        ai_component = components.ai_test()
        slime = object.object(6, 6, "slime", constant.SLIME,
                            creature=creaturetest1, ai=ai_component)

        # GAME_OBJECTS = [player, slime]
        # constant.game_objects = GAME_OBJECTS

        self.all_sprites = pygame.sprite.OrderedUpdates(slime, player)
        constant.game_objects = self.all_sprites
        self.run()


    def run(self):
        """
        Main game loop which takes in process player input updates screen    
        """
        self.playing = True
        while self.playing:
            self.clock.tick(constant.FPS)
            self.events()
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
                    self.all_sprites.update(-1, 0, self.map_tiles)
                if event.key == pygame.K_d:
                    self.all_sprites.update(1, 0, self.map_tiles)
                if event.key == pygame.K_w:
                    self.all_sprites.update(0, -1, self.map_tiles)
                if event.key == pygame.K_q:
                    self.all_sprites.update(-1, -1, self.map_tiles)
                if event.key == pygame.K_e:
                    self.all_sprites.update(1, -1, self.map_tiles)
                if event.key == pygame.K_z:
                    self.all_sprites.update(-1, 1, self.map_tiles)
                if event.key == pygame.K_c:
                    self.all_sprites.update(1, 1, self.map_tiles)
                if event.key == pygame.K_s:
                    self.all_sprites.update(0, 1, self.map_tiles)
                if event.key == pygame.K_x:
                    self.all_sprites.update(0, 0, self.map_tiles)
                print("player at, player " + str(player.x), str(player.y))
                print("player_rect at " + str(player.rect))
                print("slime at " + str(slime.x), str(slime.y))
                print("slime_rect at " + str(slime.rect))
                print()
        return "no-action"

    
    def draw_grid(self):
        for x in range(0, constant.MAP_WIDTH, constant.SPRITE_SIZE):
            pygame.draw.line(self.surface, constant.GREY, (x, 0), (x, constant.MAP_HEIGHT))

        for y in range(0, constant.MAP_HEIGHT, constant.SPRITE_SIZE):
            pygame.draw.line(self.surface, constant.GREY, (0, y), (constant.MAP_WIDTH, y))
        


    def draw(self):
        """
        Draws maps and entities
        """
        gamemap.draw_map(self.map_tiles, self)
        self.walls.draw(self.surface)
        self.floors.draw(self.surface)
        self.draw_grid()
        # could change this so instead of constant map, pass map into method
        constant.com_map = self.map_tiles

        self.all_sprites.draw(self.surface)

        # Might need this later
        # slime.draw_object(surface)
        # player.draw_object(surface)

        pygame.display.flip()

g = Game()
while g.running:
    g.new()

pygame.quit()