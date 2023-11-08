import pygame

class Bulle:
    NOTE_SPEED = 500
    bulle_surface = {}
    def __init__(self, init_x, init_y, keycode):
        self.image = pygame.Surface((64,64))
        #self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.keycode = keycode
        self.alive = True
        self.answer = None
        self.pos = pygame.Vector2(init_x,init_y)

    @staticmethod
    def init_surface():
        Bulle.bulle_surface = {
            pygame.K_f: pygame.transform.scale(pygame.image.load("data/keybinds/F KEY.png").convert_alpha(),(64,64)),
            pygame.K_j: pygame.transform.scale(pygame.image.load("data/keybinds/J KEY.png").convert_alpha(),(64,64)),
            pygame.K_TAB: pygame.transform.scale(pygame.image.load("data/keybinds/TAB KEY.png").convert_alpha(),(64,64)),
            pygame.K_SEMICOLON: pygame.transform.scale(pygame.image.load("data/keybinds/; KEY.png").convert_alpha(),(64,64)),
            pygame.K_RETURN: pygame.transform.scale(pygame.image.load("data/keybinds/ENTER KEY.png").convert_alpha(),(64,64)),
            pygame.K_EQUALS: pygame.transform.scale(pygame.image.load("data/keybinds/EQUAL KEY.png").convert_alpha(),(64,64))

        }
    def draw(self, screen:pygame.Surface):
        if self.alive:
            #screen.blit(self.image, self.rect)
            screen.blit(Bulle.bulle_surface[self.keycode], self.rect)

    def update(self, dt:float):
        #self.rect.x += Bulle.NOTE_SPEED * -1 * dt
        self.pos.x += Bulle.NOTE_SPEED *-1 * dt
        self.rect.x = self.pos.x

    def handle_key(self, keys, detection_zone: pygame.Rect) -> bool:
        if keys == self.keycode and self.alive:
            self.kill()
            self.answer = detection_zone.collidepoint(self.rect.center)
            return True
        return False
    def kill(self):
        self.alive = False

    def __str__(self):
        return f"alive: {self.alive}"

# Gere toute les bulles d'un niveau (détéction, mise a jour et affichage)
class BulleManager:
    def __init__(self):
        self.bulles = []
        self.current = 0

    def add(self, bulle: Bulle):
      self.bulles.append(bulle)

    def update(self, dt:float, detection_zone: pygame.Rect):
        if len(self.bulles) > self.current and detection_zone.left > self.bulles[self.current].rect.right:
            # passage a la prochaine
            self.bulles[self.current].kill()
            self.current += 1
        for bulle in self.bulles:
            bulle.update(dt)

    def handle_key(self, keys:pygame.event.Event, detection_zone: pygame.Rect):
        # test pour voir si on est a la fin des bulles
        if (len(self.bulles) <= self.current):
            return

        key_pressed = False
        # test pour voir si la bulle actuelle est passé apprès la zone de détéction
        key_pressed = self.bulles[self.current].handle_key(keys, detection_zone)

        self.current += 1 if key_pressed else 0

    def draw(self, screen: pygame.Surface):
        for bulle in self.bulles:
            bulle.draw(screen)
