import pygame
from constantes import *

class Trampa(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        
        self.image = pygame.image.load('recursos/sprites/trampas/Spiked Ball.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 5
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self,screen):
        # Mueve el objeto en el eje x
        self.draw(screen)
        self.rect.x += self.velocidad_x
        
        
        # Verifica si ha alcanzado los límites
        if self.rect.right >= ANCHO_VENTANA or self.rect.left <= 0:
            # Cambia la dirección invirtiendo la velocidad
            self.velocidad_x *= -1

        
        
