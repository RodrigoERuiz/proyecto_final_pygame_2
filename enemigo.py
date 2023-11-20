import pygame
from auxiliar import SurfaceManager
from constantes import *
from jugador import Jugador
import random
from proyectil import *

class Enemigo(pygame.sprite.Sprite):
    
    def __init__(self, coord_x, coord_y, velocidad):
        super().__init__()
        self.stand_r = [
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_000.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_001.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_002.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_003.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_004.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_005.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_006.png'),
                    ]
        
        self.walk_r = [
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_000.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_001.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_002.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_003.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_004.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_005.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_006.png'),

                    ]
        
        self.run_r = [
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_000.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_001.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_002.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_003.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_004.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_005.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_006.png'),
                    ]
        self.attack_r = [
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_000.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_001.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_002.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_003.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_004.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_005.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_006.png'),

                        ]
        self.die_r = [
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_000.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_001.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_002.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_003.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_004.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_005.png'),
                        pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_006.png')
                    ]
       
        #imagenes de animacion escaladas
        self.run_r = SurfaceManager.preparar_imagen(self.run_r,120,120)
        self.run_l = SurfaceManager.girar_sprites(self.run_r)
        self.stand_r = SurfaceManager.preparar_imagen(self.stand_r,120,120)
        self.stand_l = SurfaceManager.girar_sprites(self.stand_r)
        self.walk_r = SurfaceManager.preparar_imagen(self.walk_r, 120,120)
        self.walk_l = SurfaceManager.girar_sprites(self.walk_r)
        self.attack_r = SurfaceManager.preparar_imagen(self.attack_r,120,120)
        self.attack_l= SurfaceManager.girar_sprites(self.attack_r)
        self.die_r = SurfaceManager.preparar_imagen(self.die_r,120,120)
        self.die_l = SurfaceManager.girar_sprites(self.die_r)
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.frame_actual = 0
        self.animacion_actual = self.stand_l
        self.image = self.animacion_actual[self.frame_actual]
        self.rect = self.image.get_rect()
        self.velocidad  = velocidad
        self.height = self.image.get_height() 
        self.width = self.image.get_width()
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.velocidad_y = -1
        self.frame_tiempo_anterior = pygame.time.get_ticks()
        self.frame_tiempo_intervalo = 30
        self.lives = 3
        self.rect.y = self.coord_y #verficar si conviene dejarlo afuera
        
    def esta_muerto(self):
        return self.lives == 0
        
    def detectar_disparos(self, disparos:pygame.sprite.Group):    #ver si conviene hacerlo con el grupo de sprites
        for disparo in disparos:
            if self.rect.colliderect(disparo.rect):
                self.lives -= 1
                
    def hacer_animacion(self, animacion: str):
        if animacion == 'die':
            self.animacion_actual = self.die_r
            self.frame_actual = 0  # Reiniciar el índice del fotograma

        
    
    
    
    def aplicar_gravedad(self):
        if self.coord_y < ALTO_VENTANA - self.height: #aca estoy aplicando gravedad cuando el personaje salta o cuando no esta en el piso
            self.coord_y -= self.velocidad_y
            self.velocidad_y -= 1  
            
            #Esto controla que el jugador no se vaya por abajo de la pantalla ARREGLAR INTEGRAR A COTROLAR_LIMITES_PANTALLA
            if self.coord_y >= ALTO_VENTANA - self.height:  
                self.coord_y = ALTO_VENTANA - self.height
                self.velocidad_y = 0
    
    
    
    def controlar_limites_pantalla(self):
        if self.rect.right >= ANCHO_VENTANA:
            self.coord_x = ANCHO_VENTANA - self.rect.width
        elif self.rect.left <= 0:
            self.coord_x = 0
            
                
    def mover(self):
        self.animar()
        if self.rect.right >= ANCHO_VENTANA:
            self.direccion = -1  # Cambiar a la izquierda si alcanza el borde derecho
            self.animacion_actual = self.walk_l
        elif self.rect.left <= 0:
            self.direccion = 1   # Cambiar a la derecha si alcanza el borde izquierdo
            self.animacion_actual = self.walk_r
        # Mover en la dirección correspondiente
        self.rect.x += self.velocidad * self.direccion
        
        
    def animar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.stand_r)
            self.image = self.stand_r[self.frame_actual]
                
        self.aplicar_gravedad()
        #self.rect.y = self.coord_y #coloca a los enemigos en el suelo

            
    def actualizar(self):
        self.controlar_limites_pantalla()
        self.mover()

        
        
        
    @staticmethod
    def crear_lista_de_enemigos(n,height):
        lista_retorno = []
        
        for i in range(n):
            enemigo = Enemigo(random.randint(0,ANCHO_VENTANA),ALTO_VENTANA-height,random.randint(1,8))
            lista_retorno.append(enemigo)
        return lista_retorno