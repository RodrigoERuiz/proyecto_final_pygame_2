import pygame
from auxiliar import SurfaceManager
from constantes import *
from jugador import Jugador
import random
from proyectil import *

class Enemigo(pygame.sprite.Sprite):
    
    def __init__(self,coord_x,coord_y,nivel):
        super().__init__()
        self.nivel = nivel
        self.configs = SurfaceManager.get_config('config.json').get(f'nivel_{self.nivel}').get('enemigo')
        self.stand_r = [
                        pygame.image.load(path) for path in self.configs.get('self.stand_r')
                    ]
        
        self.walk_r = [
                        pygame.image.load(path) for path in self.configs.get('self.walk_r')
                    ]
        
        self.run_r = [
                        pygame.image.load(path) for path in self.configs.get('self.run_r')
                    ]
        self.attack_r = [
                            pygame.image.load(path) for path in self.configs.get('self.attack_r')
                        ]
        self.die_r = [
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
        self.frame_actual = 0
        self.animacion_actual = self.stand_l
        self.image = self.animacion_actual[self.frame_actual]
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
        #self.lives = self.configs.get('vidas')
        self.lives = 3 #BORRAR SI NO FUNCIONA
        self.coordenadas = self.configs.get("coords")
        self.grupo_proyectiles_enemigo = pygame.sprite.Group()
        self.proyectiles_impactados = set()
        self.sonido_die = pygame.mixer.Sound("recursos\sounds\efectos\dieenemy.wav")
        self.is_looking_right = True
        self.tiempo_entre_colisiones = 150
        self.tiempo_ultima_colision = 0 
        self.rect_vision = pygame.Rect(self.rect.left, self.rect.top,ANCHO_VENTANA, 10)
        self.is_shooting = False
        self.cooldown = 1000
        self.tiempo_ultimo_disparo = 0
        
        
    def disparar(self, jugador_principal):
        tiempo_actual = pygame.time.get_ticks()
        if self.rect_vision.colliderect(jugador_principal.rect) and not self.is_shooting and tiempo_actual - self.tiempo_ultimo_disparo >= self.cooldown:
            print("El enemigo ve al jugador y puede disparar")
            self.tiempo_ultimo_disparo = tiempo_actual
            self.is_shooting = True
            #self.sonido_disparo.play()
            proyectil = Proyectil(self.rect.centerx, self.rect.centery, 1 if self.is_looking_right else -1)
            self.grupo_proyectiles_enemigo.add(proyectil)
        else:    
            self.is_shooting = False

    def actualizar_rect_vision(self):
        altura_ojos_enemigo = self.coord_y + self.height // 3  # Posición vertical de los ojos del enemigo

        if self.is_looking_right:
            # Si el enemigo mira hacia la derecha, el rectángulo va desde su posición hasta el borde derecho de la pantalla
            self.rect_vision = pygame.Rect(self.rect.right, altura_ojos_enemigo, ANCHO_VENTANA - self.rect.right, 10)
        else:
            # Si el enemigo mira hacia la izquierda, el rectángulo va desde el borde izquierdo de la pantalla hasta su posición
            self.rect_vision = pygame.Rect(0, altura_ojos_enemigo, self.rect.left, 10)
        
    def aumentar_nivel(self):
        self.nivel += 1
    
    def draw(self,screen:pygame.surface):
        screen.blit(self.animacion_actual[self.frame_actual],self.rect)
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), self.rect, 2)
            pygame.draw.rect(SCREEN, (0, 255, 255), self.rect_vision, 2)
            
        
        
    def esta_muerto(self):
        return self.lives == 0
        
                
    def hacer_animacion(self, animacion: str):
        if animacion == 'die':
            self.animacion_actual = self.die_r
            self.frame_actual = 0  

        
    
    
    
    def aplicar_gravedad(self):
        if self.coord_y < ALTO_VENTANA - self.height: 
            self.actualizar_rect_vision()
            self.coord_y -= self.velocidad_y
            self.velocidad_y -= 1  
            
            
            if self.coord_y >= ALTO_VENTANA - self.height:
                self.actualizar_rect_vision()  
                self.coord_y = ALTO_VENTANA - self.height
                self.velocidad_y = 0
    
    
    
    def controlar_limites_pantalla(self):
        if self.rect.right >= ANCHO_VENTANA:
            self.actualizar_rect_vision()
            self.coord_x = ANCHO_VENTANA - self.rect.width
        elif self.rect.left <= 0:
            self.actualizar_rect_vision()
            self.coord_x = 0
            
                
    def mover(self): 
        self.animar()
        tiempo = pygame.time.get_ticks()
        if self.rect.right >= ANCHO_VENTANA:
            self.is_looking_right = False
            self.direccion = -1  # Cambiar a la izquierda si alcanza el borde derecho
            if tiempo % 2 == 0:
                self.animacion_actual = self.walk_l
            else: 
                self.animacion_actual = self.attack_l
        elif self.rect.left <= 0:
            self.is_looking_right = True
            self.direccion = 1   # Cambiar a la derecha si alcanza el borde izquierdo
            if tiempo % 2 == 0:
                self.animacion_actual = self.walk_r
            else:
                self.animacion_actual = self.attack_r
        self.actualizar_rect_vision()
        self.rect.x += self.velocidad * self.direccion
        self.coord_x = self.rect.x
        
        
    # def disparar(self):
    #     proyectil = Proyectil(self.rect.centerx, self.rect.centery, 1 if self.is_looking_right else -1)
    #     return proyectil
        
        
    def animar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.stand_r)
            self.image = self.stand_r[self.frame_actual]
                
        self.aplicar_gravedad()
        

            
    def update(self,grupo_proyectiles:pygame.sprite.Group,grupo_enemigos:pygame.sprite.Group,jugador): #saque al jugador que estaba pasado como parametro
        
        self.controlar_limites_pantalla()
        self.mover()
        self.coord_x = self.rect.x  
        self.coord_y = self.rect.y 
        self.actualizar_rect_vision()
        #if self.rect_vision.colliderect(jugador.rect):
        self.disparar(jugador)
    
    def detectar_disparos(self, grupo_disparos_jugador, jugador: Jugador):
        tiempo_actual = pygame.time.get_ticks()
        print("entro a la funcion detectar disparo")
        for disparo in grupo_disparos_jugador:
            if disparo.rect.colliderect(self.rect) and disparo not in self.proyectiles_impactados and tiempo_actual - self.tiempo_ultima_colision >= self.tiempo_entre_colisiones:
                self.tiempo_ultima_colision = tiempo_actual
                self.proyectiles_impactados.add(disparo)  # Agregar el proyectil al conjunto de impactados
                self.lives -= 1
                print("Le resto 1 de vida al enemigo impactado")
                if self.esta_muerto():
                    print("Enemigo asesinado")
                    disparo.kill()
                    self.kill()
                    jugador.score += 100
                       
    def reiniciar_impactos(self):
        self.proyectiles_impactados = set()
        
    @staticmethod
    def crear_lista_de_enemigos(n,height,lista_coord:list[dict],nivel):
        lista_retorno = []
        
        for i in range(n):
            #enemigo = Enemigo(random.randint(0,ANCHO_VENTANA),ALTO_VENTANA-height)
            enemigo = Enemigo(lista_coord[i].get('x'),ALTO_VENTANA - 120, nivel)
            #enemigo = Enemigo(lista_coord[i].get('x'),lista_coord[i].get('y'),nivel)
            #print(f'x: {lista_coord[i].get("x")} Y: {lista_coord[i].get("y")} ')
            lista_retorno.append(enemigo)
        return lista_retorno

        