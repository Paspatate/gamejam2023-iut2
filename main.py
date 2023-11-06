import pygame

def main():
    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    deltaTime = 0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        
        deltaTime = clock.tick(TARGET_FPS) / 1000

if __name__ == "__main__":
    main()