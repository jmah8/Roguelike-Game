import pygame
from constant import *


class Menu_Manager:
    """
    Menu Manager to create the menus and handle key event to open
    """

    def __init__(self, game):
        self.game = game

    def pause_menu(self):
        menu_closed = False
        while not menu_closed:
            events_list = pygame.event.get()
            for event in events_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        menu_closed = True

            self.game.drawing.draw_text(self.game.surface,
                                        ((CAMERA_WIDTH - FONT_SIZE) / 2, (CAMERA_HEIGHT - FONT_SIZE) / 2), WHITE,
                                        "PAUSED", BLACK)
            self.game.clock.tick(60)
            pygame.display.update()


    def inventory_menu(self):
        menu_closed = False
        menu_width, menu_height = self.game.camera.camera_width / 2, self.game.camera.camera_height
        menu_surface = pygame.Surface((menu_width, menu_height))
        item_surface = pygame.Surface((menu_width, menu_height/2))
        while not menu_closed:
            events_list = pygame.event.get()
            menu_surface.fill(BLACK)
            item_surface.fill(WHITE)

            num_items_row = TILE_WIDTH//2
            num_items_col = TILE_HEIGHT//2
            counter = 0

            for i in range(0, num_items_row):
                for j in range(0, num_items_col):
                    inventory_array = self.game.player.container.inventory
                    if len(inventory_array) >= counter + 1:
                        item = inventory_array[counter]
                        item_surface.blit(self.game.game_sprites.empty_inventory_slot, (
                            (0 + i * SPRITE_SIZE, 0 + j * SPRITE_SIZE), (SPRITE_SIZE, SPRITE_SIZE)))
                        item_surface.blit(item.image,
                                          ((0 + i * SPRITE_SIZE, 0 + j * SPRITE_SIZE), (SPRITE_SIZE, SPRITE_SIZE)))
                        counter = counter + 1
                    else:
                        item_surface.blit(self.game.game_sprites.empty_inventory_slot, (
                        (0 + i * SPRITE_SIZE, 0 + j * SPRITE_SIZE), (SPRITE_SIZE, SPRITE_SIZE)))

            menu_surface.blit(item_surface, (0, menu_height/2))
            self.game.surface.blit(menu_surface, (menu_width, 0))

            for event in events_list:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.game.mini_map_on = not self.game.mini_map_on
                        if self.game.mini_map_on:
                            self.game.drawing.draw_minimap(self.game)

                    if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                        menu_closed = True

            self.game.clock.tick(60)
            pygame.display.update()


