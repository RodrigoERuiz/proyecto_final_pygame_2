import pygame
from constantes import *
from auxiliar import SurfaceManager
from plataforma import Plataforma
from proyectil import Proyectil


class Jugador :
    def __init__(self, coord_x, coord_y, velocidad) -> None:
        self.stand_r = [
                        pygame.image.load('recursos/sprites/Stand/0.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/1.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/2.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/3.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/4.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/5.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/6.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/7.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/8.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Stand/9.png').convert_alpha()
                    ]
        
        self.walk_r = [
                        pygame.image.load('recursos/sprites/Walk/0.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/1.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/2.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/3.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/4.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/5.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/6.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/7.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/8.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Walk/9.png').convert_alpha()
                    ]
        
        self.run_r = [
                        pygame.image.load('recursos/sprites/Run/0.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/1.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/2.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/3.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/4.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/5.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/6.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/7.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/8.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Run/9.png').convert_alpha()
                    ]

        #imagenes de animacion escaladas
        self.run_r = SurfaceManager.preparar_imagen(self.run_r,120 ,120)
        self.run_l = SurfaceManager.girar_sprites(self.run_r)
        self.stand_r = SurfaceManager.preparar_imagen(self.stand_r,120,120)
        self.stand_l = SurfaceManager.girar_sprites(self.stand_r)
        self.walk_r = SurfaceManager.preparar_imagen(self.walk_r, 120,120)
        self.walk_l = SurfaceManager.girar_sprites(self.walk_r)
        

        self.coord_x = coord_x
        self.coord_y = coord_y
        self.velocidad_walk = velocidad
        self.velocidad_run = velocidad * 1.1
        self.frame_actual = 0
        self.animacion_actual = self.stand_r
        self.frame_tiempo_anterior = pygame.time.get_ticks()
        self.frame_tiempo_intervalo = 30  # Intervalo entre cambios de fotograma en milisegundos
        self.is_looking_right = True
        self.is_jump = False
        self.image= self.animacion_actual[self.frame_actual]
        self.velocidad_y = 0
        #self.piso = pygame.draw.rect(SCREEN, (255, 0, 0), (0, 521, ANCHO_VENTANA, ALTO_VENTANA))  # Ejemplo de coordenadas y tamaño
        self.height = self.image.get_height() 
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.esta_cayendo = False
        self.hubo_colision_previa = False
        self.tiempo_entre_colisiones = 1000  # 1000 milisegundos (1 segundo)
        self.tiempo_ultima_colision = 0 
        self.vida = 100
        self.en_suelo = False
        self.score = 0
        self.en_plataforma = False
        self.hay_que_aplicar_gravedad = True
        #self.rec_ground = pygame.Rect(self.rect.left, self.rect.bottom, self.rect.width /3 - 20, 10)
        self.rec_ground = pygame.Rect(self.rect.centerx - ((self.rect.width / 3 - 20) / 2), self.rect.bottom - 10, self.rect.width / 3 - 20, 10)






        
        
    def aplicar_gravedad(self):
        if self.is_jump or self.en_plataforma or self.coord_y < ALTO_VENTANA - self.height: #aca estoy aplicando gravedad cuando el personaje salta o cuando no esta en el piso
           # poner la animacion de saltar
            # self.coord_y -= self.velocidad_y
            # self.rec_ground.y  -= self.velocidad_y
            self.add_y(- self.velocidad_y)
            self.velocidad_y -= 1     #ver si esto es necesario
            
            #Esto controla que el jugador no se vaya por abajo de la pantalla ARREGLAR INTEGRAR A COTROLAR_LIMITES_PANTALLA
            if self.coord_y >= ALTO_VENTANA - self.height:  
                self.coord_y = ALTO_VENTANA - self.height
                self.is_jump = False
                self.velocidad_y = 0
        

    def actualizar(self,plataformas:pygame.sprite.Group, grupo_frutas:pygame.sprite.Group):
        self.rect.x = self.coord_x
        self.rect.y = self.coord_y
        #self.rec_ground.x = self.coord_x esta es la linea original
        self.rec_ground.x = self.rect.centerx-10
        self.rec_ground.y = self.rect.bottom -30
        
        ################ Si el jugador está sobre la plataforma###############
        # for plataforma in plataformas:
        #     if self.rect.colliderect(plataforma.rect) and self.velocidad_y >= 0:    
        #         self.coord_x += plataforma.velocidad_x
        #         self.coord_y += plataforma.velocidad_y
                
        ######################################################################
        # for fruta in grupo_frutas:
        #     if self.rect.colliderect(fruta):
        #         fruta.kill()
        #         self.vida += 10         
        
        self.controlar_limites_pantalla()
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.stand_r)
            self.image = self.stand_r[self.frame_actual]

        self.aplicar_gravedad()

        
        
    def mover(self, lista_teclas: list,lista_eventos, grupo_proyectiles:pygame.sprite.Group ):
        if lista_teclas[pygame.K_d] and lista_teclas[pygame.K_LSHIFT]:
            self.animacion_actual = self.run_r
            self.is_looking_right = True
            self.coord_x += self.velocidad_run  
            self.rec_ground.x += self.velocidad_run  
            
          #CORRER A LA IZQUIERDA  
        elif lista_teclas[pygame.K_a] and lista_teclas[pygame.K_LSHIFT]:
            self.animacion_actual = self.run_l
            self.is_looking_right = False
            self.coord_x -= self.velocidad_run
            self.rec_ground.x -=  self.velocidad_run
            #CAMINAR A LA DERECHA
            
        elif lista_teclas[pygame.K_d]:
            self.animacion_actual = self.walk_r
            self.coord_x += self.velocidad_walk
            self.rec_ground.x += self.velocidad_walk
            self.is_looking_right = True
            
            #CAMINAR A LA IZQUIERDA
        elif lista_teclas[pygame.K_a]:
            self.animacion_actual = self.walk_l
            self.coord_x -= self.velocidad_walk
            self.rec_ground.x -= self.velocidad_walk
            self.is_looking_right = False
            #QUEDARSE QUIETO
        else:
            if self.is_looking_right:
                self.animacion_actual = self.stand_r
            else:
                self.animacion_actual = self.stand_l
                
            #SALTAR
        if lista_teclas[pygame.K_SPACE] and not self.is_jump:
            self.is_jump = True
            self.velocidad_y = 12
        #disaparo
        for evento in lista_eventos:
            if  evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e:
                    proyectil = self.disparar()
                    grupo_proyectiles.add(proyectil)
            
     
    def controlar_limites_pantalla(self):
        if self.rect.right >= ANCHO_VENTANA:
            self.coord_x = ANCHO_VENTANA - self.rect.width
        elif self.rect.left <= 0:
            self.coord_x = 0

        
    def hubo_colision(self, rect: pygame.Rect):
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.tiempo_ultima_colision >= self.tiempo_entre_colisiones:
            if self.rect.colliderect(rect) and not self.hubo_colision_previa:
                print("Hubo colisión")
                self.vida -= 10
                print(f'Te quedan: {self.vida} puntos de vida')
                self.hubo_colision_previa = True
                self.tiempo_ultima_colision = tiempo_actual
        else:
            self.hubo_colision_previa = False
            
    def disparar(self):
        proyectil = Proyectil(self.rect.centerx, self.rect.centery, 1 if self.is_looking_right else -1)
        return proyectil
    
    def add_x(self, delta_x):
        self.rect.x += delta_x
        self.rec_ground.x += delta_x
    
    def add_y(self, delta_y):
        self.coord_y += delta_y
        self.rec_ground.y += delta_y
        

#(69, 521) x,y piso