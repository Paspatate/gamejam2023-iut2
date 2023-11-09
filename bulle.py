import pygame

class Bulle:
    NOTE_SPEED = 0.5
    bulle_surface = {}
    Y = 350
    def __init__(self, init_x, keycode):
        self.image = pygame.Surface((64,64))
        #self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = Bulle.Y
        self.keycode = keycode
        self.alive = True
        self.answer = False
        self.has_responded = False
        self.pos = pygame.Vector2(init_x,self.rect.y)
        self.can_interact = True

    @staticmethod
    def init_surface():
        Bulle.bulle_surface = {
            pygame.K_f: (pygame.transform.scale(pygame.image.load("data/keybinds/F KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/F KEYused.png").convert_alpha(),(64,64))),

            pygame.K_j: (pygame.transform.scale(pygame.image.load("data/keybinds/J KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/J KEYused.png").convert_alpha(),(64,64))),

            pygame.K_TAB: (pygame.transform.scale(pygame.image.load("data/keybinds/TAB KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/TAB KEYused.png").convert_alpha(),(64,64))),

            pygame.K_SEMICOLON: (pygame.transform.scale(pygame.image.load("data/keybinds/; KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/; KEYused.png").convert_alpha(),(64,64))),

            pygame.K_RETURN: (pygame.transform.scale(pygame.image.load("data/keybinds/ENTER KEY.png").convert_alpha(),(64,64)),
                            pygame.transform.scale(pygame.image.load("data/keybinds/ENTER KEYused.png").convert_alpha(),(64,64))),

            pygame.K_EQUALS: (pygame.transform.scale(pygame.image.load("data/keybinds/EQUAL KEY.png").convert_alpha(),(64,64)),
                              pygame.transform.scale(pygame.image.load("data/keybinds/EQUAL KEYused.png").convert_alpha(),(64,64))),

            "error": pygame.transform.scale(pygame.image.load("data/keybinds/red_cross.png").convert_alpha(),(64,64))
        }
    def draw(self, screen:pygame.Surface):
        if self.alive:
            #screen.blit(self.image, self.rect)
            screen.blit(Bulle.bulle_surface[self.keycode][0], self.rect)
            if self.has_responded and not self.answer:
                screen.blit(Bulle.bulle_surface[self.keycode][1], self.rect)
                screen.blit(Bulle.bulle_surface["error"], self.rect)
        


    def update(self, dt:float):
        #self.rect.x += Bulle.NOTE_SPEED * -1 * dt
        self.pos.x += Bulle.NOTE_SPEED *-1 * dt
        self.rect.x = self.pos.x
        # if not self.answer:
        #     self.

        if self.rect.centerx <= 151:
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


# Gere toute les bulles d'un niveau (détéction, mise a jour et affichage)
class BulleManager:
    def __init__(self):
        self.bulles = []
        self.current = 0

    def add(self, bulle: Bulle):
      print(bulle.keycode)
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
