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

    touche = {"s" : pygame.K_s, "d" : pygame.K_d, "l" : pygame.K_l, "k" : pygame.K_k}

    Bulle.init_surface()
    Scene.init_surface()

    txt = open("data/level.txt", "r")

    lignes = txt.readlines()
    scenes = {}

    i = 0

    while i < len(lignes):
        
        if lignes[i] == "Start level\n":
             
            current_Scene = Scene()
            
            current_Scene.name=lignes[i+1].rstrip("\n")
            current_Scene.bg=pygame.image.load(lignes[i+2].rstrip("\n"))
            current_Scene.music=lignes[i+3].rstrip("\n")
            j = i +4
            while lignes[j] != "Start dialogue\n":
                current_Scene.exo.append(int(lignes[j].rstrip("\n")))
                j += 1
            j += 1
            while lignes[j] != "Start button\n":
                current_dialogue = lignes[j].rstrip("\n").split(",")

                current_Scene.dialogue.append([pygame.image.load(current_dialogue[0]).convert_alpha(), pygame.image.load(current_dialogue[1]).convert_alpha()])
                j +=1
            current_Scene.initDialogue()
            j += 1
            
            while lignes[j] != "Start bulle\n":
                current_Ligne = lignes[j].rstrip("\n").split(",")
                current_Scene.buttons.append([pygame.image.load(current_Ligne[0]).convert_alpha(),pygame.image.load(current_Ligne[1]).convert_alpha()
                                              ,int(current_Ligne[2])  ,int(current_Ligne[3]) ,current_Ligne[4]])
                j += 1
            current_Scene.initButton()
            
            j += 1
            
            
            while lignes[j] != "End bulle\n":
                if current_Scene.bullManager == None:
                    current_Scene.bullManager = BulleManager()
                current_Bulle = lignes[j].rstrip("\n").split(",")
                
                current_Scene.bullManager.add(Bulle(float(current_Bulle[0]),touche[current_Bulle[1]]))
                j +=1
            scenes[current_Scene.name] = current_Scene
        
            i = j
           
        i +=1
        
    txt.close()

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
    

    for scene in scenes.keys():
        scenes[scene].scenes = scenes

    currentScene = scenes["main"].name


    scenes["main"].loadM()
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