import pygame

# Variables

WIDTH = 1200
HEIGHT = 600
VELOCITY = 20
TOPLEFT = (0, 0)
PLAYERSTART = (400, 100)

# Code

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

background = pygame.image.load('resource/Background.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

screen.blit(background, TOPLEFT)

player = pygame.image.load('resource/Player.jpg').convert()

# screen.blit(player, (0, 0))
screen.blit(player, PLAYERSTART)

position = player.get_rect().move(PLAYERSTART)

pygame.display.flip()

while True:
    quit = False
    events = pygame.event.get()
    for event in events:
        screen.blit(background, position, position)
        if event.type == pygame.QUIT:
            quit = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                position = position.move(-VELOCITY, 0)
            if event.key == pygame.K_RIGHT:
                position = position.move(VELOCITY, 0)
            if event.key == pygame.K_DOWN:
                position = position.move(0, VELOCITY)
            if event.key == pygame.K_UP:
                position = position.move(0, -VELOCITY)
            screen.blit(player, position)
            pygame.display.flip()
            pygame.time.delay(10)
    if quit:
        break

pygame.quit()