import pygame
import sys
from bulle import Bulle, BulleManager

def main():
    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    pygame.mixer.music.load("./data/music/music_bells.ogg","ogg")
    pygame.mixer.music.play()
    
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    t_note = Bulle(1000, 350, pygame.K_f)
    t_bulle_man = BulleManager()
    t_bulle_man.add(t_note)
    t_bulle_man.add(Bulle(1400, 350, pygame.K_f))
    t_bulle_man.add(Bulle(1500, 350, pygame.K_RETURN))
    Bulle.init_surface()

    detec_surf = pygame.Surface((100, 100))
    detec_surf.fill((250, 150, 10))
    detec = detec_surf.get_rect(topleft=(151.5, 334))

    bg = pygame.image.load("data/backgrounds/BackgroundLevel.png").convert()

    deltaTime = 0
    run = True
    while run:
        # managment des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                t_bulle_man.handle_key(event.key, detec)
        
        # update du jeu
        t_bulle_man.update(deltaTime, detec)

        # rendu
        screen.blit(bg, (0,0))

        screen.blit(detec_surf, detec.topleft)
        
        t_bulle_man.draw(screen)
        

        pygame.display.update()
        deltaTime = clock.tick(TARGET_FPS) / 1000
        pygame.display.set_caption(f"fps: {clock.get_fps()}")
    
    pygame.quit()

if __name__ == "__main__":
    main()