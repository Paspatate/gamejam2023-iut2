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

    question_asm = pygame.image.load("data/questions/assembleur.png").convert_alpha()
    bulle_question = pygame.image.load("data/questions/BulleProf.png").convert_alpha()
    qasm_img = pygame.image.load("data/questions/assembleurR.png").convert_alpha()
    list_qasm_img = []
    num_slice = 10
    width_slice = qasm_img.get_width()//num_slice

    for i in range(num_slice):
        list_qasm_img.append(qasm_img.subsurface(pygame.Rect(
                                                            i*width_slice,
                                                            0,
                                                            width_slice,
                                                            qasm_img.get_height())))

    qerr_img = pygame.image.load("data/questions/erreur.png").convert_alpha()
    list_qerr_img = []
    width_slice = qerr_img.get_width()//num_slice
    for i in range(num_slice):
        list_qerr_img.append(qerr_img.subsurface(pygame.Rect(i*width_slice, 0, width_slice, qerr_img.get_height())))
        


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
        screen.blit(bulle_question, (360, 70))
        
        for i in range(len(list_qasm_img)-9):
            screen.blit(list_qasm_img[i], (i*width_slice + 10, 10))

        
        t_bulle_man.draw(screen)
        

        pygame.display.update()
        deltaTime = clock.tick(TARGET_FPS) / 1000
        pygame.display.set_caption(f"fps: {clock.get_fps()}")
    
    pygame.quit()

if __name__ == "__main__":
    main()