from bulle import Bulle, BulleManager
from utils import sum_to

import pygame

class Scene:
    erreur = None
    bulle_question = None
    bulle_rep = None
    detec = None
    sErreur = None
    sCorrect = None


    @staticmethod
    def init_surface():
        Scene.erreur = pygame.image.load("data/questions/erreur.png").convert_alpha()
        Scene.bulle_question = pygame.image.load("data/questions/BulleProf.png").convert_alpha()
        Scene.bulle_rep = pygame.image.load("data/questions/BulleEleve.png").convert_alpha()
        Scene.detec = pygame.Rect((151, 334), (100, 100))
        Scene.sCorrect = pygame.mixer.Sound("data/sfx/sfx_touch.ogg")
        Scene.sErreur= pygame.mixer.Sound("data/sfx/erreur.ogg")
        Scene.sErreur.set_volume(0.5)




    def __init__(self):
        self.name =""
        self.dialogue = []
        self.bullManager = None
        self.buttons = []
        self.rectButtons = []
        self.bg = ""
        self.rep = [[]]
        self.note = 0
        self.exo = []
        self.numExo = 0
        self.music = ""
        self.scenes = {}
        self.listJ = []
        self.listF = []



    def initDialogue(self):

        i = 0
        while i < len(self.exo):

            self.listJ.append([])
            self.listF.append([])
            width_slice = self.dialogue[i][1].get_width()//self.exo[i]

            for j in range(self.exo[i]):

                self.listJ[i].append(self.dialogue[i][1].subsurface(pygame.Rect(
                                                                j*width_slice,
                                                                0,
                                                                width_slice,
                                                                self.dialogue[i][1].get_height())))



            for j in range(self.exo[i]):
                self.listF[i].append(Scene.erreur.subsurface(pygame.Rect(j*width_slice, 0, width_slice, Scene.erreur.get_height())))

            i +=1

    def initButton(self):

        if len(self.buttons) >0:
            for button in self.buttons:

                self.rectButtons.append([button[0].get_rect(topleft = (button[2],button[3])), button[4]])
                button.append(0)

    def reset(self):
        self.numExo = 0
        self.rep = [[]]
        self.bullManager.reset()




    def loadM(self):
        pygame.mixer.music.load(self.music,"ogg")
        pygame.mixer.music.play()


    def draw(self, screen , event_list : pygame.event, deltaTime):
        bulle_rep = None
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                i = 0
                while i < len(self.rectButtons):
                    if self.rectButtons[i][0].collidepoint(pygame.mouse.get_pos()):
                        self.buttons[i][5] = 1

                    i += 1

            elif event.type == pygame.MOUSEBUTTONUP:
                i = 0
                while i < len(self.rectButtons):
                    if self.rectButtons[i][0].collidepoint(pygame.mouse.get_pos()):
                        if self.rectButtons[i][1] != "selection":
                            pygame.mixer.music.unload()
                            self.scenes[self.rectButtons[i][1]].loadM()
                        self.name = self.rectButtons[i][1]
                        self.buttons[i][5] = 1

                    i += 1

            elif event.type == pygame.KEYDOWN:
                if self.bullManager != None:
                    bulle_rep = self.bullManager.handle_key(event.key, Scene.detec)




        if self.bullManager != None and len(self.dialogue) > 0:
            last_exo = False
            if self.bullManager.current == sum_to(self.exo, self.numExo+1) and self.bullManager.current != 0:
                self.numExo += 1
                self.rep.append([])
                if self.numExo == len(self.exo):
                    last_exo = True
                    self.name = "selection"
                    pygame.mixer.music.unload()
                    self.scenes["selection"].loadM()
                    self.reset()
            if not last_exo:
                if bulle_rep:
                    self.rep[self.numExo].append(self.listJ[self.numExo][self.bullManager.current - sum_to(self.exo, self.numExo)])
                elif bulle_rep == False:

                    self.rep[self.numExo].append(self.listF[self.numExo][self.bullManager.current  - sum_to(self.exo, self.numExo)])
                elif (not self.bullManager.bulles[self.bullManager.current-1].has_responded and not self.bullManager.bulles[self.bullManager.current-1].can_interact):
                    self.bullManager.bulles[self.bullManager.current-1].has_responded = True

                    self.rep[self.numExo].append(self.listF[self.numExo][self.bullManager.current - sum_to(self.exo, self.numExo)-1])

            self.bullManager.update(deltaTime, Scene.detec)



        screen.blit(self.bg,(0,0))
        for button in self.buttons:

            screen.blit(button[button[5]],(button[2],button[3]))


        if len(self.dialogue) >0:
            screen.blit(self.bulle_question, (367, 78))
            screen.blit(self.dialogue[self.numExo][0], (394, 78))
            for i in range(len(self.rep[self.numExo])):

                screen.blit(self.rep[self.numExo][i], (i* self.dialogue[self.numExo][1].get_width()//self.exo[self.numExo] + 100, 568))


        if self.bullManager != None:
            self.bullManager.draw(screen)
