import pygame, random   
from constantes import *


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        
        self.image = pygame.transform.scale(PLATAFORMA_IMAGE,(width,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 0 #cambiar valores para mover
        self.velocidad_y = 0 #cambiar valores para mover

    def mover_plataforma(self):     
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.right >= ANCHO_VENTANA or self.rect.left <= 0:
            self.velocidad_x *= -1

        if self.rect.bottom >= ALTO_VENTANA or self.rect.top <= 0:
            self.velocidad_y *= -1

        

        
        
    @staticmethod
    def crear_lista_plataformas(n:int,x:int,y:int,ancho:int):
        lista_retorno = []
        for i in range(n):
            plataforma = Plataforma(x,y,ancho)
            lista_retorno.append(plataforma)
        return lista_retorno
    