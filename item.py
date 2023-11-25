import pygame
from jugador import Jugador

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
        self.item_activo = True
        self.tiempo_reaparicion =  10000 #10 segundos

    def update(self,grupo_frutas:pygame.sprite.Group(),screen:pygame.Surface,jugador:Jugador):
        tiempo_actual = pygame.time.get_ticks()
        
        for fruta in grupo_frutas:
            if fruta.item_activo:
                fruta.draw(screen)
                if jugador.rect.colliderect(fruta.rect):
                    if jugador.vida < 100:
                        jugador.vida += 10
                        fruta.desactivar()
                        fruta.tiempo_reaparicion = pygame.time.get_ticks() + 10000
            else:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual >= fruta.tiempo_reaparicion:
                    fruta.activar()  # Reactivar la fruta después de 10 segundos
        #fruta.update()
        
        
        
        
        
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.animacion)
            self.image = self.animacion[self.frame_actual]
    
    def draw(self, screen):
        if self.item_activo:
            screen.blit(self.image, self.rect)
        
    def desactivar(self):
        self.item_activo = False
    
    def activar(self):
        self.item_activo = True
        