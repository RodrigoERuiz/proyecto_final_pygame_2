
import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))  # Tamaño del proyectil
        #self.image.fill((255, 0, 0))  # Color del proyectil
        self.image = pygame.image.load('recursos/sprites/weapons/axe.png')
        self.image = pygame.transform.scale(self.image, (40,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # Dirección del proyectil (-1 para izquierda, 1 para derecha)
        self.speed = 8  # Velocidad del proyectil
        
        if direction == -1:  # Si el jugador está mirando hacia la izquierda, voltear la imagen
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect.x += self.speed * self.direction