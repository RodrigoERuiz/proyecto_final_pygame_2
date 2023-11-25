import pygame, random   
from constantes import *
from jugador import Jugador


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        super().__init__()
        
        self.image = pygame.transform.scale(PLATAFORMA_IMAGE,(width,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidad_x = 0 #cambiar valores para mover
        self.velocidad_y = 0 #cambiar valores para mover
        self.top_collision_rect = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, 2)
        
        
        
        
    def draw(self, screen:pygame.surface):
        screen.blit(self.image,self.rect)
        if DEBUG:   
            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
            pygame.draw.rect(screen, (0, 0, 255), self.top_collision_rect, 2)
    
    def update(self,screen:pygame.Surface, jugador:Jugador, plataformas:pygame.sprite.Group):
        self.draw(screen)
        for plataforma in plataformas:
            plataforma.draw(screen)
            if plataforma.top_collision_rect.top <= jugador.rect.bottom and plataforma.top_collision_rect.colliderect(jugador.rect):
                    jugador.rect.bottom = plataforma.top_collision_rect.top
                    jugador.velocidad_y = 0
                    jugador.is_jump = False

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
    