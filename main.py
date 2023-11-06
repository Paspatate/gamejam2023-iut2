import pygame
import sys
from bulle import Bulle, BulleManager

def main():
    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    t_note = Bulle(1000, 300, pygame.K_s)
    t_bulle_man = BulleManager()
    t_bulle_man.add(t_note)
    t_bulle_man.add(Bulle(1400, 300, pygame.K_s))

    detec_surf = pygame.Surface((100, 100))
    detec_surf.fill((250, 150, 10))
    detec = detec_surf.get_rect(topleft=(50, 250))

    deltaTime = 0
    run = True
    keys = dict()
    while run:
        # managment des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

        keys = pygame.key.get_pressed()
        t_note.handle_key(keys, detec)

        # update du jeu
        t_note.update(deltaTime)

        # rendu
        screen.fill("white")

        screen.blit(detec_surf, detec.topleft)
        
        t_note.draw(screen)

        pygame.display.update()
        deltaTime = clock.tick(TARGET_FPS) / 1000
        pygame.display.set_caption(f"fps: {clock.get_fps()}")
    
    pygame.quit()

if __name__ == "__main__":
    main()