import pygame
from bulle import Bulle

def main():
    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    note_test = Bulle(1000, 300, pygame.K_s)

    deltaTime = 0
    run = True
    keys = dict()
    while run:
        # managment des events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        note_test.handle_key(keys)

        # update du jeu
        note_test.update(deltaTime)

        # rendu
        screen.fill("white")

        note_test.draw(screen)

        pygame.display.update()
        deltaTime = clock.tick(TARGET_FPS) / 1000
        pygame.display.set_caption(f"fps: {clock.get_fps()}")

if __name__ == "__main__":
    main()