import pygame
import sys
from bulle import Bulle, BulleManager

def main():
    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    pygame.mixer.music.load("./data/music/audio_bells.ogg","ogg")
    pygame.mixer.music.play()
    
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    t_note = Bulle(1669.00, 350, pygame.K_f)
    t_bulle_man = BulleManager()
    t_bulle_man.add(t_note)
    t_bulle_man.add(Bulle(2419.00, 350, pygame.K_f))
    t_bulle_man.add(Bulle(3169.00, 350, pygame.K_f))
    t_bulle_man.add(Bulle(3919.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(4669.00, 350, pygame.K_f))
    t_bulle_man.add(Bulle(5419.00, 350, pygame.K_f))    
    t_bulle_man.add(Bulle(6169.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(6919.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(7669.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(8419.00, 350, pygame.K_f))
    t_bulle_man.add(Bulle(9169.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(9919.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(10669.00, 350, pygame.K_f))
    t_bulle_man.add(Bulle(11419.00, 350, pygame.K_f))
    t_bulle_man.add(Bulle(12169.00, 350, pygame.K_j))
    t_bulle_man.add(Bulle(12919.00, 350, pygame.K_f))
    #t_bulle_man.add(Bulle(10669.00, 350, pygame.K_f)) #8bar
    
    Bulle.init_surface()

    detec_surf = pygame.Surface((100, 100))
    detec_surf.fill((250, 150, 10))
    detec = detec_surf.get_rect(center=(201, 384))
    print(detec.left)

    bg = pygame.image.load("data/backgrounds/BackgroundLevelDefault.png").convert()

    question_asm = pygame.image.load("data/questions/assembleur.png").convert_alpha()
    bulle_question = pygame.image.load("data/questions/BulleProf.png").convert_alpha()
    bulle_eleve = pygame.image.load("data/questions/BulleEleve.png").convert_alpha()
    qasm_img = pygame.image.load("data/questions/assembleurR.png").convert_alpha()
    list_qasm_img = []
    num_slice = 16
    width_slice = qasm_img.get_width()//num_slice
    scaleX = 380/ num_slice
    scaleY = 100
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
        
    rep_list = []
    bulle_rep = None

    deltaTime = 0
    run = True
    while run:
        # managment des events
        bulle_rep = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                bulle_rep = t_bulle_man.handle_key(event.key, detec)

        
        if bulle_rep:
            rep_list.append(list_qasm_img[t_bulle_man.current])
        elif bulle_rep == False:
            
            rep_list.append(list_qerr_img[t_bulle_man.current])
        elif (not t_bulle_man.bulles[t_bulle_man.current-1].has_responded and not t_bulle_man.bulles[t_bulle_man.current-1].can_interact):
            t_bulle_man.bulles[t_bulle_man.current-1].has_responded = True
            rep_list.append(list_qerr_img[t_bulle_man.current-1])

        # update du jeu
        t_bulle_man.update(deltaTime, detec)

        # rendu
        screen.blit(bg, (0,0))

        screen.blit(detec_surf, detec.topleft)
        #screen.blit(bulle_question, (360, 70))
        #screen.blit(question_asm,(370, 70))
        screen.blit(bulle_eleve, (260, 70))

        for i in range(len(rep_list)):
            screen.blit(rep_list[i], (i*width_slice + 100, 568))

        for i in range(len(rep_list)):
            screen.blit(pygame.transform.scale(rep_list[i],(scaleX,scaleY)), (i*scaleX + 300, 90))

        

        t_bulle_man.draw(screen)

        

        pygame.display.update()

        deltaTime = clock.get_time()
        clock.tick(TARGET_FPS)
        

        


        pygame.display.set_caption(f"fps: {clock.get_fps()}")
        
    pygame.quit()

if __name__ == "__main__":
    main()