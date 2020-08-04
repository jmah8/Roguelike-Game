import pygame
from constant import *


class Menu_Manager:
    """
    Menu Manager to create the menus and handle key event to open
    """

    def __init__(self, game):
        self.game = game
        self.equipment_rects = []

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
        """
        create screens for inventory + equipment menus
        """
        menu_closed = False
        menu_width, menu_height = self.game.camera.camera_width / 2, self.game.camera.camera_height
        menu_surface = pygame.Surface((menu_width, menu_height - SPRITE_SIZE))
        while not menu_closed:
            events_list = pygame.event.get()
            menu_surface.fill(INVENTORY_BEIGE)
            self.game.drawing.draw()

            menu_surface.blit(self._load_inventory_screen(), (0, menu_height/2))
            menu_surface.blit(self._load_equipment_screen(), (0, 0))
            self.game.surface.blit(menu_surface, (menu_width, 0))

            for event in events_list:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        button = self.game.drawing.button_manager.check_if_button_pressed(mouse_x, mouse_y)
                        if button:
                            menu_closed = True
                            break

                if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_TAB:
                    #     self.game.mini_map_on = not self.game.mini_map_on
                    #     if self.game.mini_map_on:
                    #         self.game.drawing.draw_minimap(self.game)
                    if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                        menu_closed = True
            self.game.clock.tick(60)
            pygame.display.update()

    def _load_inventory_screen(self):
        """
        Helper to create inventory with items
        :return:  inventory_surface
        """
        menu_width, menu_height = self.game.camera.camera_width / 2, self.game.camera.camera_height / 2
        item_surface = pygame.Surface((menu_width, menu_height))
        num_items_row = TILE_WIDTH // 2
        num_items_col = TILE_HEIGHT // 2
        counter = 0

        for i in range(0, num_items_row):
            for j in range(0, num_items_col-1):
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
        return item_surface

    def _load_equipment_screen(self):
        """
        Helper to create equipment_screen with items
        :return:  equipment_surface
        """
        menu_width, menu_height = self.game.camera.camera_width / 2, self.game.camera.camera_height / 2
        equipment_surface = pygame.Surface((menu_width, menu_height))

        helmet_tl, helmet_br = (243, 24), (294, 67)
        armor_tl, armor_br = (218, 70), (319, 185)
        amulet_tl, amulet_br = (323, 52), (361, 89)
        main_tl, main_br = (38, 83), (114, 274)
        off_tl, off_br = (390, 83), (466, 274)
        ringL_tl, ringL_br = (176, 171), (214, 208)
        ringR_tl, ringR_br = (323, 171), (361, 208)
        pants_tl, pants_br = (218, 188), (319, 301)
        gloves_tl, gloves_br = (134, 230), (209, 299)
        boots_tl, boots_br = (232, 308), (305,356)

        helmet_rect = pygame.Rect(helmet_tl, ((helmet_br[0]-helmet_tl[0]), (helmet_br[1]-helmet_tl[1])))
        armor_rect = pygame.Rect(armor_tl, ((armor_br[0]-armor_tl[0]), (armor_br[1]-armor_tl[1])))
        amulet_rect = pygame.Rect(amulet_tl, ((amulet_br[0]-amulet_tl[0]), (amulet_br[1]-amulet_tl[1])))
        main_rect = pygame.Rect(main_tl, ((main_br[0]-main_tl[0]), (main_br[1]-main_tl[1])))
        off_rect = pygame.Rect(off_tl, ((off_br[0]-off_tl[0]), (off_br[1]-off_tl[1])))
        ringL_rect = pygame.Rect(ringL_tl, ((ringL_br[0]-ringL_tl[0]), (ringL_br[1]-ringL_tl[1])))
        ringR_rect = pygame.Rect(ringR_tl, ((ringR_br[0]-ringR_tl[0]), (ringR_br[1]-ringR_tl[1])))
        pants_rect = pygame.Rect(pants_tl, ((pants_br[0]-pants_tl[0]), (pants_br[1]-pants_tl[1])))
        gloves_rect = pygame.Rect(gloves_tl, ((gloves_br[0]-gloves_tl[0]), (gloves_br[1]-gloves_tl[1])))
        boots_rect = pygame.Rect(boots_tl, ((boots_br[0]-boots_tl[0]), (boots_br[1]-boots_tl[1])))

        self.equipment_rects.append(helmet_rect)
        self.equipment_rects.append(armor_rect)
        self.equipment_rects.append(amulet_rect)
        self.equipment_rects.append(main_rect)
        self.equipment_rects.append(off_rect)
        self.equipment_rects.append(ringL_rect)
        self.equipment_rects.append(ringR_rect)
        self.equipment_rects.append(pants_rect)
        self.equipment_rects.append(gloves_rect)
        self.equipment_rects.append(boots_rect)

        for rect in self.equipment_rects:
            pygame.draw.rect(equipment_surface, INVENTORY_BEIGE, rect)

        equipment_surface.blit(self.game.game_sprites.equip_screen, (0, 0))

        return equipment_surface

        # equip_dictionary = {
        #     "main": None,
        #     "off": None,
        #     "helmet": None,
        #     "armor": None,
        #     "amulet": None,
        #     "ring": None,
        #     "pants": None,
        #     "boots": None,
        #     "gloves": None,
        # }
