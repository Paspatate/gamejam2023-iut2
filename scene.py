from bulle import Bulle, BulleManager
import pygame

class Scene:
    erreur = None
    bulle_question = None
    bulle_rep = None
    detec = None

    @staticmethod
    def init_surface():
        Scene.erreur = pygame.image.load("data/questions/erreur.png").convert_alpha()
        Scene.bulle_question = pygame.image.load("data/questions/BulleProf.png").convert_alpha()
        Scene.bulle_rep = pygame.image.load("data/questions/BulleEleve.png").convert_alpha()
        Scene.detec = pygame.Rect((151, 334), (100, 100))




    def __init__(self, name,dialogue : list, bulleManager : BulleManager,buttons: list,bg, exo , music):
        self.name = name
        self.dialogue = dialogue
        self.bullManager = bulleManager
        self.buttons = buttons
        self.rectButtons = []
        self.bg = bg
        self.rep = [[]]
        self.note = 0
        self.exo = exo
        self.numExo = 0
        self.music = music
        self.scenes = {}
        self.listJ = [[]]
        self.listF = [[]]
        

        i = 0
        
        while i < len(exo):
            width_slice = dialogue[i][1].get_width()//exo[i]
            
            for j in range(exo[i]):
                
                self.listJ[i].append(dialogue[i][1].subsurface(pygame.Rect(
                                                                j*width_slice,
                                                                0,
                                                                width_slice,
                                                                dialogue[i][1].get_height())))
                


            for j in range(exo[i]):
                self.listF[i].append(Scene.erreur.subsurface(pygame.Rect(j*width_slice, 0, width_slice, Scene.erreur.get_height())))
            i +=1
        
        
        for button in buttons:
            self.rectButtons.append([button[0].get_rect(topleft = (button[1],button[2])), button[3]])
    

    def setScenes(self, scenes : {}):
        self.scenes = scenes


    def loadM(self):
        pygame.mixer.music.load(self.music,"ogg")
        pygame.mixer.music.play()

    def draw(self, screen , event_list : pygame.event, deltaTime):
        bulle_rep = None
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in self.rectButtons:
                    if rect[0].collidepoint(pygame.mouse.get_pos()):
                        self.name = rect[1]
                        pygame.mixer.music.unload()
                        self.scenes[rect[1]].loadM()
            elif event.type == pygame.KEYDOWN:
                bulle_rep = self.bullManager.handle_key(event.key, Scene.detec)        

        if self.bullManager != None and len(self.dialogue) >0:
            if bulle_rep:
                self.rep[self.numExo].append(self.listJ[self.numExo][self.bullManager.current])
            elif bulle_rep == False:
                
                self.rep[self.numExo].append(self.listF[self.numExo][self.bullManager.current])
            elif (not self.bullManager.bulles[self.bullManager.current-1].has_responded and not self.bullManager.bulles[self.bullManager.current-1].can_interact):
                self.bullManager.bulles[self.bullManager.current-1].has_responded = True
                self.rep[self.numExo].append(self.listF[self.numExo][self.bullManager.current-1])

            self.bullManager.update(deltaTime, Scene.detec)
        


        
        

        screen.blit(self.bg,(0,0))
        for button in self.buttons:
            
            screen.blit(button[0],(button[1],button[2]))
            
            
        if len(self.dialogue) >0:
            for i in range(len(self.rep[self.numExo])):
                
                screen.blit(self.rep[self.numExo][i], (i* self.dialogue[self.numExo][1].get_width()//self.exo[self.numExo] + 100, 568))


        if self.bullManager != None:
            self.bullManager.draw(screen)