
import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))  # Tamaño del proyectil
        self.image.fill((255, 0, 0))  # Color del proyectil
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # Dirección del proyectil (-1 para izquierda, 1 para derecha)
        self.speed = 8  # Velocidad del proyectil

    def update(self):
        self.rect.x += self.speed * self.direction