import pygame

class Bulle:
    NOTE_SPEED = 100
    def __init__(self, init_x, init_y, keycode):
        self.image = pygame.Surface((32, 32))
        self.image.fill("blue")
        self.rect = self.image.get_rect()
        self.rect.x = init_x
        self.rect.y = init_y
        self.keycode = keycode
        self.alive = True
    
    def draw(self, screen:pygame.Surface):
        if self.alive:
            screen.blit(self.image, self.rect)

    def update(self, dt:float):
        self.rect.x += Bulle.NOTE_SPEED * -1 * dt
    
    def handle_key(self, keys):
        if keys[self.keycode]:
            self.alive = False
