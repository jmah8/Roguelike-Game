from constant import *
import pygame
import config
import game_text

pygame.init()

pygame.display.set_caption("Test")

BUTTON_WIDTH = CAMERA_WIDTH // 4
BUTTON_HEIGHT = CAMERA_HEIGHT // 12

BUTTON_COORD = (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 4)


class MenuButton:
    def __init__(self, button_text, size, center, colour):
        self.button_text = button_text
        self.size = size
        self.center = center
        self.colour = colour

        self.normal_colour = self.colour
        self.mouse_over_colour = (max(self.colour[0] - 25, 0),
                                  max(self.colour[1] - 25, 0),
                                  max(self.colour[2] - 25, 0))

        self.rect = pygame.Rect((0, 0), size)
        self.rect.center = center

    def draw(self):
        pygame.draw.rect(config.SURFACE_MAIN, self.colour, self.rect)
        game_text.draw_text(config.SURFACE_MAIN, self.center, BLACK, self.button_text, center=True)

    def mouse_over(self):
        if self.colour == self.normal_colour:
            self.colour = self.mouse_over_colour

    def check_mouse_over(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        mouse_over = (self.rect.left <= mouse_x <= self.rect.right and
                      self.rect.top <= mouse_y <= self.rect.bottom)

        if mouse_over:
            self.colour = self.mouse_over_colour
        else:
            self.colour = self.normal_colour


new_button = MenuButton("New Game", (BUTTON_WIDTH, BUTTON_HEIGHT),
                        (CAMERA_WIDTH // 2, CAMERA_HEIGHT // 4), RED)

continue_button = MenuButton("Continue", (BUTTON_WIDTH, BUTTON_HEIGHT),
                             (CAMERA_WIDTH // 2, new_button.rect.midbottom[1] + 100), GREEN)

exit_button = MenuButton("Exit", (BUTTON_WIDTH, BUTTON_HEIGHT),
                         (CAMERA_WIDTH // 2, continue_button.rect.midbottom[1] + 100), GREY)


def main_menu():
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
                        print("New Game")
                    elif continue_button.rect.collidepoint((mouse_x, mouse_y)):
                        print("Continue Game")
                    elif exit_button.rect.collidepoint((mouse_x, mouse_y)):
                        pygame.quit()

        pygame.display.update()


main_menu()
