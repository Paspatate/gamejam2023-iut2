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
    vol = None
    font = None



    @staticmethod
    def init_ressource(volume:float):
        Scene.erreur = pygame.image.load("data/questions/erreur.png").convert_alpha()
        Scene.bulle_question = pygame.image.load("data/questions/BulleProf.png").convert_alpha()
        Scene.bulle_rep = pygame.image.load("data/questions/BulleEleve.png").convert_alpha()
        Scene.detec = pygame.Rect((151, 334), (100, 100))
        Scene.vol = volume
        Scene.sCorrect = pygame.mixer.Sound("data/sfx/sfx_touch.ogg")
        Scene.sCorrect.set_volume(volume)
        Scene.sErreur= pygame.mixer.Sound("data/sfx/erreur.ogg")
        Scene.sErreur.set_volume(0.5 * volume)
        Scene.font = pygame.font.SysFont(None, 50)




    def __init__(self):
        self.name =""
        self.dialogue = []
        self.bulleManager = None
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
        self.last_exo = False
        self.nScore = 0
        self.bScore = None
        self.imgs = []


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
        self.bulleManager.reset()
        self.last_exo = False
        if self.bScore == None:
            self.bScore = self.nScore
        elif self.nScore > self.bScore:
            self.bScore = self.nScore
        
        

    
    def saveScore(self):
        score = open("data/score.txt", "w")
        score.write(f"{self.scenes['R1.04'].bScore}")
        score.write(",")
        score.write(f"{self.scenes['R1.07'].bScore}")

        score.close()


    def loadM(self):
        pygame.mixer.music.load(self.music,"ogg")
        pygame.mixer.music.set_volume(Scene.vol)
        pygame.mixer.music.play(loops=-1)


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
                        if self.rectButtons[i][1] != "selection" and self.rectButtons[i][1] != "main"and  self.rectButtons[i][1] != "credit" and self.rectButtons[i][1] != "histoire" and (self.name == "main" or self.name == "selection" or self.name == "score"):
                            pygame.mixer.music.unload()
                            self.scenes[self.rectButtons[i][1]].loadM()
                        self.name = self.rectButtons[i][1]
                        self.buttons[i][5] = 0

                    i += 1

            elif event.type == pygame.KEYDOWN:
                if self.bulleManager != None:
                    bulle_rep = self.bulleManager.handle_key(event.key, Scene.detec)




        if self.bulleManager != None and len(self.dialogue) > 0:

            if self.bulleManager.current == sum_to(self.exo, self.numExo+1) and self.bulleManager.current != 0:
                if not self.last_exo:
                    self.numExo += 1
                    self.rep.append([])
                if self.numExo == len(self.exo):
                    self.last_exo = True

                    if self.bulleManager.bulles[self.bulleManager.current-1].pos.x <=-20:
                        self.nScore = self.bulleManager.calculeScore()
                        self.name = "score"
                        pygame.mixer.music.unload()
                        self.scenes["score"].loadM()
                        self.scenes["score"].nScore = self.nScore
                        self.reset()
                        self.saveScore()
                        

            if not self.last_exo:

                if bulle_rep:
                    self.rep[self.numExo].append(self.listJ[self.numExo][self.bulleManager.current - sum_to(self.exo, self.numExo)])
                    Scene.sCorrect.play()
                    
                elif bulle_rep == False:

                    self.rep[self.numExo].append(self.listF[self.numExo][self.bulleManager.current  - sum_to(self.exo, self.numExo)])
                    Scene.sErreur.play()
                    
                elif (not self.bulleManager.bulles[self.bulleManager.current-1].has_responded and not self.bulleManager.bulles[self.bulleManager.current-1].can_interact) and self.bulleManager.current != 0:
                    self.bulleManager.bulles[self.bulleManager.current-1].has_responded = True
                    if self.bulleManager.current-1 >= sum_to(self.exo, self.numExo):
                        self.rep[self.numExo].append(self.listF[self.numExo][self.bulleManager.current - sum_to(self.exo, self.numExo)-1])
                    Scene.sErreur.play()
                    
            self.bulleManager.update(deltaTime, Scene.detec)



        screen.blit(self.bg,(0,0))
        for button in self.buttons:

            screen.blit(button[button[5]],(button[2],button[3]))


        if len(self.dialogue) >0 and not self.last_exo:
            screen.blit(self.bulle_question, (367, 78))
            screen.blit(self.dialogue[self.numExo][0], (394, 78))
            for i in range(len(self.rep[self.numExo])):

                screen.blit(self.rep[self.numExo][i], (i* self.dialogue[self.numExo][1].get_width()//self.exo[self.numExo] + 100, 568))


        if self.bulleManager != None:
            self.bulleManager.draw(screen)

        for img in self.imgs:
            screen.blit(img[0],(img[1],img[2]))


        if self.name == "score":
            screen.blit(Scene.font.render(f"{self.nScore} / 20", True , "WHITE"), (325,255))

        if self.name == "selection":
            if self.scenes['R1.04'].bScore != None:
                screen.blit(Scene.font.render(f"{self.scenes['R1.04'].bScore} / 20", True , "BLACK"), (65,480))
            if self.scenes['R1.07'].bScore != None:
                screen.blit(Scene.font.render(f"{self.scenes['R1.07'].bScore} / 20", True , "BLACK"), (380,480))


        
        
