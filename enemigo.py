import pygame
from auxiliar import SurfaceManager
from constantes import *
#from jugador import Jugador
import random
from proyectil import *

class Enemigo(pygame.sprite.Sprite):
    
    def __init__(self,coord_x,coord_y,nivel):
        super().__init__()
        self.nivel = nivel
        #self.configs = SurfaceManager.get_config('config.json').get('nivel_1').get('enemigo') VERSION ORIGINAL
        self.configs = SurfaceManager.get_config('config.json').get(f'nivel_{self.nivel}').get('enemigo')
        self.stand_r = [
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_000.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_001.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_002.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_003.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_004.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_005.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\IDLE\IDLE_006.png'),
                        
                        #pygame.image.load(self.configs.get('stand_r')[i]) for i in range(7)
                        pygame.image.load(path) for path in self.configs.get('self.stand_r')

                    ]
        
        self.walk_r = [
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_000.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_001.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_002.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_003.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_004.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_005.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\WALK\WALK_006.png'),
                        pygame.image.load(path) for path in self.configs.get('self.walk_r')

                    ]
        
        self.run_r = [
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_000.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_001.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_002.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_003.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_004.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_005.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\RUN\RUN_006.png'),
                        pygame.image.load(path) for path in self.configs.get('self.run_r')
                    ]
        self.attack_r = [
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_000.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_001.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_002.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_003.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_004.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_005.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\ATTAK\ATTAK_006.png'),
                        pygame.image.load(path) for path in self.configs.get('self.attack_r')

                        ]
        self.die_r = [
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_000.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_001.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_002.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_003.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_004.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_005.png'),
                        # pygame.image.load('recursos\sprites\enemies\ork_sword\DIE\DIE_006.png')
                        pygame.image.load(path) for path in self.configs.get('self.die_r')
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
        # self.coord_x = self.configs.get('coords')[0].get('x')
        # self.coord_y = self.configs.get('coords')[0].get('y')
        self.frame_actual = 0
        self.animacion_actual = self.stand_l
        self.image = self.animacion_actual[self.frame_actual]
        #self.image = pygame.transform.scale(self.image,(80,80)) #borrar si queda mal
        self.rect = self.image.get_rect()
        self.rect.y = self.coord_y #verficar si conviene dejarlo afuera
        self.velocidad_min  = self.configs.get('velocidad_min')
        self.velocidad_max = self.configs.get('velocidad_max')
        self.velocidad = random.randint(self.velocidad_min,self.velocidad_max)
        self.height = self.image.get_height() 
        self.width = self.image.get_width()
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.velocidad_y = -1
        self.frame_tiempo_anterior = pygame.time.get_ticks()
        self.frame_tiempo_intervalo = 30
        self.lives = self.configs.get('vidas')
        self.coordenadas = self.configs.get("coords")
        self.grupo_proyectiles_enemigo = pygame.sprite.Group()
        self.proyectiles_impactados = set()
        
        
        
    def aumentar_nivel(self):
        self.nivel += 1
    
    def draw(self,screen:pygame.surface):
        screen.blit(self.animacion_actual[self.frame_actual],self.rect)
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
            
        
        
    def esta_muerto(self):
        return self.lives == 0
        
                
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
            
                
    def mover(self): #pasarle al jugador por parametro y en caso que este en nivel 2 o mas dotarlos de mas habilidades 
        self.animar()
        tiempo = pygame.time.get_ticks()
        if self.rect.right >= ANCHO_VENTANA:
            self.direccion = -1  # Cambiar a la izquierda si alcanza el borde derecho
            if tiempo % 2 == 0:
                self.animacion_actual = self.walk_l
            else: 
                self.animacion_actual = self.attack_l
        elif self.rect.left <= 0:
            self.direccion = 1   # Cambiar a la derecha si alcanza el borde izquierdo
            if tiempo % 2 == 0:
                self.animacion_actual = self.walk_r
            else:
                self.animacion_actual = self.attack_r
        # Mover en la dirección correspondiente
        self.rect.x += self.velocidad * self.direccion
        self.coord_x = self.rect.x
        
        
    def animar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.stand_r)
            self.image = self.stand_r[self.frame_actual]
                
        self.aplicar_gravedad()
        #self.rect.y = self.coord_y #coloca a los enemigos en el suelo

            
    def update(self,grupo_proyectiles:pygame.sprite.Group,grupo_enemigos:pygame.sprite.Group,jugador): #saque al jugador que estaba pasado como parametro
        
        self.controlar_limites_pantalla()
        self.mover()
        self.coord_x = self.rect.x  # Actualizar la coordenada x
        self.coord_y = self.rect.y  # Actualizar la coordenada y

        #grupo_enemigos.draw(SCREEN)
        for enemigo in grupo_enemigos:
            enemigo.detectar_disparos(grupo_enemigos,jugador)
            # if enemigo.esta_muerto():
            #     #jugador.score += 10
            #     enemigo.hacer_animacion('die')
            #     enemigo.kill()
            #     enemigo.reiniciar_impactos()
                

        
    def detectar_disparos(self,grupo_enemigos:pygame.sprite.Group,jugador):    #ver si conviene hacerlo con el grupo de sprites
        for enemigo in grupo_enemigos:
            for proyectil in jugador.grupo_proyectiles_jugador:
                if enemigo.rect.colliderect(proyectil.rect) and proyectil not in self.proyectiles_impactados:
                    enemigo.lives -= 1
                    self.proyectiles_impactados.add(proyectil)
                    #proyectil.kill()
                if proyectil.rect.right > ANCHO_VENTANA or proyectil.rect.left < 0:
                    proyectil.kill()
                
    # def detectar_disparos(self, grupo_proyectiles, jugador):
    #     for proyectil in grupo_proyectiles:
    #         if proyectil not in self.proyectiles_impactados and self.rect.colliderect(proyectil.rect):
    #             self.lives -= 1
    #             self.proyectiles_impactados.add(proyectil)
    #             proyectil.kill()
                
    def reiniciar_impactos(self):
        self.proyectiles_impactados = set()
        
    @staticmethod
    def crear_lista_de_enemigos(n,height,lista_coord:list[dict],nivel):
        lista_retorno = []
        
        for i in range(n):
            #enemigo = Enemigo(random.randint(0,ANCHO_VENTANA),ALTO_VENTANA-height)
            enemigo = Enemigo(lista_coord[i].get('x'),lista_coord[i].get('y'),nivel)
            print(f'x: {lista_coord[i].get("x")} Y: {lista_coord[i].get("y")} ')
            lista_retorno.append(enemigo)
        return lista_retorno

        
