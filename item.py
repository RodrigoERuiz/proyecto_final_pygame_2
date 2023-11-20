import pygame

class Item( pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animacion = [
                            pygame.image.load('recursos/sprites/frutas/0.png'),
                            pygame.image.load('recursos/sprites/frutas/1.png'),
                            pygame.image.load('recursos/sprites/frutas/2.png'),
                            pygame.image.load('recursos/sprites/frutas/3.png'),
                            pygame.image.load('recursos/sprites/frutas/4.png'),
                            pygame.image.load('recursos/sprites/frutas/5.png'),
                            pygame.image.load('recursos/sprites/frutas/6.png'),
                            pygame.image.load('recursos/sprites/frutas/7.png'),
                            pygame.image.load('recursos/sprites/frutas/8.png'),
                            pygame.image.load('recursos/sprites/frutas/9.png'),
                            pygame.image.load('recursos/sprites/frutas/10.png'),
                            pygame.image.load('recursos/sprites/frutas/11.png'),
                            pygame.image.load('recursos/sprites/frutas/12.png'),
                            pygame.image.load('recursos/sprites/frutas/13.png'),
                            pygame.image.load('recursos/sprites/frutas/14.png'),
                            pygame.image.load('recursos/sprites/frutas/15.png'),
                            pygame.image.load('recursos/sprites/frutas/16.png')
                        ]
        self.frame_actual = 0
        self.image = self.animacion[self.frame_actual]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.frame_tiempo_anterior = pygame.time.get_ticks()
        self.frame_tiempo_intervalo = 100  # Intervalo entre cambios de fotograma en milisegundos

    def update(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion)
            self.image = self.animacion[self.frame_actual]
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)