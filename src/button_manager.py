from constant import *
import pygame

class Button_Manager:
    def __init__(self):
        self.button_surface = pygame.Surface((100, 100))

    def button(self, img, coords, game_surface):
        self.button_surface.blit(img, coords)
        # Makes button_surface transparent
        self.button_surface.set_colorkey(BLACK)
        button_rect = img.get_rect()
        button_rect.topright = coords

        # TODO: blit button on surface with an offset to align multiple buttons
        game_surface.blit(self.button_surface,
                          (game_surface.get_width() - SPRITE_SIZE, game_surface.get_height() - SPRITE_SIZE))
        return (img, button_rect)

