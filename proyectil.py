
from constantes import *
import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

        self.image = pygame.Surface((10, 10))  # Tamaño del proyectil
        self.image = pygame.image.load('recursos/sprites/weapons/axe.png')
        self.image = pygame.transform.scale(self.image, (40,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction  # Dirección del proyectil (-1 para izquierda, 1 para derecha)
        self.speed = 8  # Velocidad del proyectil
        
        if direction == -1:  # Si el jugador está mirando hacia la izquierda, voltear la imagen
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


    def update(self,screen, enemigos:pygame.sprite.Group, lista_proyectiles_enemigos:pygame.sprite.Group, jugador, plataformas:pygame.sprite.Group,lista_proyectiles_jugador:pygame.sprite.Group):
        self.rect.x += self.speed * self.direction
        self.draw(screen)
        
        #if jugador.rect.colliderect(lista_proyectiles_enemigos.rect):#separar entre proyectiles del jugador y proyectiles del enemigo sino cuando el jugador dispara tambien le saca vida a el
        if pygame.sprite.groupcollide(lista_proyectiles_enemigos, [jugador], True, False) or pygame.sprite.groupcollide(lista_proyectiles_jugador, enemigos, True, True):
            # if jugador.vida > 0:
            #     jugador.vida -= 1
                #if self in lista_proyectiles:
                self.kill()


                
                
        # if self.rect.x < 0 or self.rect.x > ANCHO_VENTANA:
        #     if self in lista_proyectiles_jugador:
        #         self.kill()

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect) and self in lista_proyectiles_jugador:
                if self in lista_proyectiles_jugador:
                    self.kill()

        # for proyectil in lista_proyectiles_jugador:
        #     if proyectil != self and self.rect.colliderect(proyectil.rect):
        #         if self in lista_proyectiles_jugador:
        #             self.kill()


