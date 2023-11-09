import pygame

class Bulle:
    NOTE_SPEED = 0.5
    bulle_surface = {}
    Y = 350
    def __init__(self, init_x, keycode):
        self.init_x = init_x
        self.image = pygame.Surface((64,64))
        #self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = Bulle.Y
        self.keycode = keycode
        self.alive = False
        self.answer = False
        self.has_responded = False
        self.pos = pygame.Vector2(init_x,self.rect.y)
        self.can_interact = True
        self.frame = 0

    @staticmethod
    def init_surface():
        Bulle.bulle_surface = {
            pygame.K_s: (pygame.transform.scale(pygame.image.load("data/keybinds/S_KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/S_KEY_used.png").convert_alpha(),(64,64))),

            pygame.K_d: (pygame.transform.scale(pygame.image.load("data/keybinds/D_KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/D_KEY_used.png").convert_alpha(),(64,64))),

            pygame.K_f: (pygame.transform.scale(pygame.image.load("data/keybinds/F_KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/F_KEY_used.png").convert_alpha(),(64,64))),
            
            pygame.K_j: (pygame.transform.scale(pygame.image.load("data/keybinds/J_KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/J_KEY_used.png").convert_alpha(),(64,64))),
            
            pygame.K_k: (pygame.transform.scale(pygame.image.load("data/keybinds/K_KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/K_KEY_used.png").convert_alpha(),(64,64))),

            pygame.K_l: (pygame.transform.scale(pygame.image.load("data/keybinds/L_KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/L_KEY_used.png").convert_alpha(),(64,64))),

            "error": pygame.transform.scale(pygame.image.load("data/keybinds/red_cross.png").convert_alpha(),(64,64)),

            "correct" : (pygame.transform.scale(pygame.image.load("data/fx/Perfect2.png").convert_alpha(),(128,128)),
                         pygame.transform.scale(pygame.image.load("data/fx/Perfect.png").convert_alpha(),(128,128)))
        }
    def draw(self, screen:pygame.Surface):
        if self.alive:
            #screen.blit(self.image, self.rect)
            screen.blit(Bulle.bulle_surface[self.keycode][0], self.rect)
            if self.has_responded and not self.answer:
                screen.blit(Bulle.bulle_surface[self.keycode][1], self.rect)
                screen.blit(Bulle.bulle_surface["error"], self.rect)
        elif self.has_responded and self.answer and self.frame < 5:
            screen.blit(Bulle.bulle_surface["correct"][0],(135,320))
            self.frame += 1
        elif self.has_responded and self.answer and self.frame < 10:
            screen.blit(Bulle.bulle_surface["correct"][1],(135,320))
            self.frame += 1
            

    def update(self, dt:float):
        #self.rect.x += Bulle.NOTE_SPEED * -1 * dt
        self.pos.x += Bulle.NOTE_SPEED *-1 * dt
        self.rect.x = self.pos.x
        if self.pos.x > 740 and self.pos.x < 800:
            self.alive = True
        # if not self.answer:
        #     self.

        if self.rect.centerx <= 151 or self.answer:
            self.kill()

    def handle_key(self, keys, detection_zone: pygame.Rect) -> int:
        self.has_responded = True
        if self.can_interact:
            if (keys == self.keycode and detection_zone.collidepoint(self.rect.center)):
                self.answer = True
                return 0
            else:
                return 1
        return 2
    
    def kill(self):
        self.alive = False
        self.can_interact = False

    def stop_interaction(self):
        self.can_interact = False

    def reset(self):
        self.rect.x = self.init_x
        self.pos.x = self.rect.x
        self.alive = True
        self.answer = False
        self.has_responded = False
        self.can_interact = True
        self.frame = 0

# Gere toute les bulles d'un niveau (détéction, mise a jour et affichage)
class BulleManager:
    def __init__(self):
        self.bulles = []
        self.current = 0

    def add(self, bulle: Bulle):
      self.bulles.append(bulle)

    def update(self, dt:float, detection_zone: pygame.Rect):
        # kill est passage a la suivante quand:
        # pas réponse -> a sortie de la detection_zone,
        # réponse fausse -> entré de la detection zone
        # réponse juste -> dans la zone (forcément)
        if self.current < len(self.bulles):
            if self.bulles[self.current].answer == False and self.bulles[self.current].has_responded :
                self.bulles[self.current].stop_interaction()
                if detection_zone.right > self.bulles[self.current].rect.centerx:
                    self.current += 1
                # réponse fausse
            elif detection_zone.left > self.bulles[self.current].rect.right:
                # passage a la prochaine
                self.bulles[self.current].kill()
                self.current += 1
                # réponse tard
            elif self.bulles[self.current].has_responded and self.bulles[self.current].answer:
                self.current += 1
                # réponse juste
        
        # réponse just
        for bulle in self.bulles:
            bulle.update(dt)

    def handle_key(self, keys:pygame.event.Event, detection_zone: pygame.Rect):
        # test pour voir si on est a la fin des bulles
        rep = None
        if (len(self.bulles) <= self.current):
            return rep
        match self.bulles[self.current].handle_key(keys, detection_zone) :
            case 0:
                rep = True
            case 1:
                rep = False
            case 2:
                rep = None
        return rep

        

    def draw(self, screen: pygame.Surface):
        for bulle in self.bulles:
            bulle.draw(screen)
    
    def reset(self):
        self.current = 0
        for bulle in self.bulles:
            bulle.reset()

    def calculeScore(self):
        score = 0
        nbPt = 20/len(self.bulles)
        for bulle in self.bulles:
            if bulle.answer == True:
                score += nbPt
        score = round(score,2)
        return score