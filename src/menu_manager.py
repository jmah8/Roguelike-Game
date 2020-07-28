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

            self.game.drawing.draw_text(self.game.surface, ((CAMERA_WIDTH - FONT_SIZE)/2,(CAMERA_HEIGHT-FONT_SIZE)/2), WHITE, "PAUSED", BLACK)
            self.game.clock.tick(60)
            pygame.display.flip()

    def inventory_menu(self):
        menu_closed = False
        while not menu_closed:
            events_list = pygame.event.get()
            for event in events_list:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_i:
                        menu_closed = True


            self.game.clock.tick(60)

            # TODO: inventory layout


