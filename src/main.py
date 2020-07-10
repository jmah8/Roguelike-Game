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
        pygame.key.set_repeat(500, 50)
        self.running = True


    def new(self):
        """
        Makes new map and entity
        """
        global slime

        self.walls = pygame.sprite.Group()
        # self.floors = pygame.sprite.Group()
        self.map_tiles = gamemap.load_data()
        self.all_sprites = pygame.sprite.Group()

        self.camera = gamemap.Camera(self.map_tiles.width, self.map_tiles.height)


        gamemap.draw_map(self.map_tiles.data, self)

        creaturetest = components.creature("Viet", 10)
        self.player = object.object(self,
            12, 11, "player", constant.CHARACTER, creature=creaturetest)

        creaturetest1 = components.creature("Slime", 3, components.death)

        ai_component = components.ai_test()
        slime = object.object(self, 2, 2, "enemy", constant.SLIME,
                            creature=creaturetest1, ai=ai_component)

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

        for sprite in self.all_sprites:
            self.surface.blit(sprite.image, self.camera.apply(sprite))
        self.draw_grid()

        pygame.display.flip()


g = Game()
while g.running:
    g.new()
    g.run()

pygame.quit()

