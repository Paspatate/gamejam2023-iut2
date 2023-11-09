import pygame
import sys
from bulle import Bulle, BulleManager
from scene import Scene

def main():
    volume = 1
    try:
        volume = float(sys.argv[1])
    except:
        print("volume set to 1 (default)")
        volume = 1

    pygame.init()

    WIN_HEIGHT = 768
    WIN_WIDTH = 1024
    TARGET_FPS = 60

    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    touche = {"f" : pygame.K_f, "j" : pygame.K_j, "s" : pygame.K_s, "d" : pygame.K_d, "k" : pygame.K_k, "l" : pygame.K_l}

    Bulle.init_surface()
    Scene.init_ressource(volume)

    

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
            
            
            while lignes[j] != "Start img\n":
                if current_Scene.bullManager == None:
                    current_Scene.bullManager = BulleManager()
                current_Bulle = lignes[j].rstrip("\n").split(",")
                
                current_Scene.bullManager.add(Bulle(float(current_Bulle[0]),touche[current_Bulle[1]]))
                j +=1
            
            j +=1
            while lignes[j] != "End img\n":
                current_img = lignes[j].rstrip("\n").split(",")
    
                current_Scene.imgs.append([pygame.transform.scale(pygame.image.load(current_img[0]).convert_alpha(),(int(current_img[3]), int(current_img[4]))), int(current_img[1]), int(current_img[2])])
                j += 1

            scenes[current_Scene.name] = current_Scene
            i = j
           
        i +=1
        
    txt.close()

    scoreTxt = open("data/score.txt", "r")
    score = scoreTxt.read()
    score = score.split(",")
    if len(score) > 1:
        if score[0] == "None":
            scenes["R1.04"].bScore = None
        else:
            scenes["R1.04"].bScore =float(score[0])
        if score[1] == "None":
            scenes["R1.07"].bScore = None
        else:
            scenes["R1.07"].bScore =float(score[1])

    
   
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