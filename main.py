import pygame
import sys
from bulle import Bulle, BulleManager
from scene import Scene

def main():
    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    
    
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
    Scene.init_surface()

    detec_surf = pygame.Surface((100, 100))
    detec_surf.fill((250, 150, 10))
    detec = detec_surf.get_rect(center=(201, 384))
    
    bgM = pygame.image.load("data/backgrounds/BackgroundMenu.png").convert()
    bg = pygame.image.load("data/backgrounds/BackgroundLevelDefault.png").convert()

    buttonP = pygame.image.load("data/buttons/playButton.png").convert_alpha()
    buttonP2 = pygame.image.load("data/buttons/playButtonUsed.png").convert_alpha()

    question_asm = pygame.image.load("data/questions/assembleur.png").convert_alpha()
   
    qasm_img = pygame.image.load("data/questions/assembleurR.png").convert_alpha()
   
    deltaTime = 0
    run = True

    main = Scene("main", [],None, [[buttonP,buttonP2,400,250,"lvl1"]],bgM,[],"./data/music/audio_menu_loop.ogg")
    lvl1 = Scene("lvl1",[[question_asm,qasm_img]],t_bulle_man,[],bg,[8],"./data/music/audio_bells.ogg")

    
        

    scenes = {main.name : main, lvl1.name : lvl1}

    for scene in scenes.keys():
        scenes[scene].setScenes(scenes)

    currentScene = scenes[main.name].name



    main.loadM()
    while run:
        # managment des events
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
                sys.exit()
            
        scenes[currentScene].draw(screen,event_list,deltaTime )
        currentScene = scenes[currentScene].name
        
        for key in scenes.keys():
            if key != scenes[key].name:
                scenes[key].name = key
        

        pygame.display.update()

        deltaTime = clock.get_time()
        clock.tick(TARGET_FPS)
        

        


        pygame.display.set_caption(f"fps: {clock.get_fps()}")
        
    pygame.quit()

if __name__ == "__main__":
    main()