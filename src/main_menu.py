from constant import *
import os
import pygame
import config
import game_text
import game

# Pygame screen
pygame.init()
pygame.display.set_caption("Knight's Adventure")
pygame.display.set_icon(config.SPRITE.sword)

# Repeat keys when held down
pygame.key.set_repeat(350, 75)

BUTTON_WIDTH = CAMERA_WIDTH // 4
BUTTON_HEIGHT = CAMERA_HEIGHT // 12

BUTTON_COORD = (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 4)


class MenuButton:
    def __init__(self, button_text, size, center, colour, clickable=True):
        self.button_text = button_text
        self.size = size
        self.center = center
        self.colour = colour
        self.clickable = clickable

        self.normal_colour = self.colour
        # Darkens color
        self.mouse_over_colour = (max(self.colour[0] - 50, 0),
                                  max(self.colour[1] - 50, 0),
                                  max(self.colour[2] - 50, 0))

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center

    def draw(self):
        pygame.draw.rect(config.SURFACE_MAIN, self.colour, self.rect)
        game_text.draw_text(config.SURFACE_MAIN, self.center, BLACK, self.button_text, center=True)

    def mouse_over(self):
        if self.colour == self.normal_colour:
            self.colour = self.mouse_over_colour

    def check_mouse_over(self):
        if self.clickable:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            mouse_over = (self.rect.left <= mouse_x <= self.rect.right and
                          self.rect.top <= mouse_y <= self.rect.bottom)

            if mouse_over:
                self.colour = self.mouse_over_colour
            else:
                self.colour = self.normal_colour

def main():
    # Make buttons
    if os.stat(SAVE_PATH).st_size == 0:
        continue_clickable = False
    else:
        continue_clickable = True

    new_button = MenuButton("New Game", (BUTTON_WIDTH, BUTTON_HEIGHT),
                            (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 4 + 100), RED)

    continue_button = MenuButton("Continue", (BUTTON_WIDTH, BUTTON_HEIGHT),
                                 (CAMERA_WIDTH // 2, new_button.rect.midbottom[1] + 100), GREEN, continue_clickable)

    exit_button = MenuButton("Exit", (BUTTON_WIDTH, BUTTON_HEIGHT),
                             (CAMERA_WIDTH // 2, continue_button.rect.midbottom[1] + 100), GREY)

    g = game.Game()

    while True:
        config.SURFACE_MAIN.fill(WHITE)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        new_button.check_mouse_over()
        continue_button.check_mouse_over()
        exit_button.check_mouse_over()

        new_button.draw()

        continue_button.draw()

        exit_button.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if new_button.rect.collidepoint((mouse_x, mouse_y)):
                        game.populate_map()
                        g.run()
                    elif continue_button.rect.collidepoint((mouse_x, mouse_y)) and continue_button.clickable:
                        game.load_game()
                        g.run()
                    elif exit_button.rect.collidepoint((mouse_x, mouse_y)):
                        pygame.quit()

        pygame.display.update()
