import pygame

class Bulle:
    NOTE_SPEED = 0.5
    bulle_surface = {}
    def __init__(self, init_x, init_y, keycode):
        self.image = pygame.Surface((64,64))
        #self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.keycode = keycode
        self.alive = True
        self.answer = True
        self.has_responded = False
        self.pos = pygame.Vector2(init_x,init_y)
        self.can_interact = True

    @staticmethod
    def init_surface():
        Bulle.bulle_surface = {
            pygame.K_f: pygame.transform.scale(pygame.image.load("data/keybinds/F KEY.png").convert_alpha(),(64,64)),
            pygame.K_j: pygame.transform.scale(pygame.image.load("data/keybinds/J KEY.png").convert_alpha(),(64,64)),
            pygame.K_TAB: pygame.transform.scale(pygame.image.load("data/keybinds/TAB KEY.png").convert_alpha(),(64,64)),
            pygame.K_SEMICOLON: pygame.transform.scale(pygame.image.load("data/keybinds/; KEY.png").convert_alpha(),(64,64)),
            pygame.K_RETURN: pygame.transform.scale(pygame.image.load("data/keybinds/ENTER KEY.png").convert_alpha(),(64,64)),
            pygame.K_EQUALS: pygame.transform.scale(pygame.image.load("data/keybinds/EQUAL KEY.png").convert_alpha(),(64,64)),
            "error": pygame.transform.scale(pygame.image.load("data/keybinds/red_cross.png").convert_alpha(),(64,64))
        }
    def draw(self, screen:pygame.Surface):
        if self.alive:
            #screen.blit(self.image, self.rect)
            screen.blit(Bulle.bulle_surface[self.keycode], self.rect)
            if self.has_responded and not self.answer:
                screen.blit(Bulle.bulle_surface["error"], self.rect)
        


    def update(self, dt:float):
        #self.rect.x += Bulle.NOTE_SPEED * -1 * dt
        self.pos.x += Bulle.NOTE_SPEED *-1 * dt
        self.rect.x = self.pos.x
        # if not self.answer:
        #     self.

        if self.rect.centerx <= 151 or (self.has_responded and self.answer):
            self.answer = False
            self.kill()

    def handle_key(self, keys, detection_zone: pygame.Rect) -> bool:
        if keys == self.keycode and self.can_interact and not self.has_responded:
            self.has_responded = True
            self.answer = detection_zone.collidepoint(self.rect.center)
            return True
        return False
    
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
      self.bulles.append(bulle)

    def update(self, dt:float, detection_zone: pygame.Rect):
        # kill est passage a la suivante quand:
        # pas réponse -> a sortie de la detection_zone,
        # réponse fausse -> entré de la detection zone
        # réponse juste -> dans la zone (forcément)
        if self.current < len(self.bulles):
            if self.bulles[self.current].answer == False:
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
        if (len(self.bulles) <= self.current):
            return None
        pre_has_responded = self.bulles[self.current].has_responded

        self.bulles[self.current].handle_key(keys, detection_zone)
        rep =  self.bulles[self.current].answer if not pre_has_responded else None
        self.bulles[self.current].has_responded = True
        return rep

        

    def draw(self, screen: pygame.Surface):
        for bulle in self.bulles:
            bulle.draw(screen)
