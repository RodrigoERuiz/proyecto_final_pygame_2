import pygame
from constantes import *
from auxiliar import SurfaceManager

from proyectil import Proyectil


class Jugador(pygame.sprite.Sprite) :
    def __init__(self, coord_x, coord_y, velocidad, nivel_actual) -> None:
        super().__init__()
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
        self.jump_r = [
                        pygame.image.load('recursos/sprites/Jump/0.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/1.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/2.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/3.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/4.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/5.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/6.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/7.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/8.png').convert_alpha(),
                        pygame.image.load('recursos/sprites/Jump/9.png').convert_alpha()
                    ]

        #imagenes de animacion escaladas
        self.jump_l = SurfaceManager.preparar_imagen(self.jump_r,50 ,90)
        self.run_r = SurfaceManager.preparar_imagen(self.run_r,50 ,90)
        self.run_l = SurfaceManager.girar_sprites(self.run_r)
        self.stand_r = SurfaceManager.preparar_imagen(self.stand_r,50,90)
        self.stand_l = SurfaceManager.girar_sprites(self.stand_r)
        self.walk_r = SurfaceManager.preparar_imagen(self.walk_r, 50,90)
        self.walk_l = SurfaceManager.girar_sprites(self.walk_r)
        
        self.configs ={}
        self.configs = SurfaceManager.get_config('config.json').get('player')
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.velocidad_walk = velocidad
        self.velocidad_run = self.configs.get('velocidad_run')
        self.frame_actual = 0
        self.animacion_actual = self.stand_r
        self.frame_tiempo_anterior = pygame.time.get_ticks()
        self.frame_tiempo_intervalo = 30  # Intervalo entre cambios de fotograma en milisegundos
        self.is_looking_right = True
        self.is_jump = False
        self.altura_salto = -60
        self.image= self.animacion_actual[self.frame_actual]
        self.velocidad_y = 0
        self.height = self.image.get_height() 
        self.width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.esta_cayendo = False
        self.hubo_colision_previa = False
        self.tiempo_entre_colisiones = 1000 
        self.tiempo_ultima_colision = 0 
        self.vida = self.configs.get('vida')
        self.en_suelo = False
        self.score = 0
        #self.rect_ground = pygame.Rect(self.rect.centerx - ((self.rect.width / 3 - 20) / 2), self.rect.bottom - 10, self.rect.width / 3 - 20, 10)
        self.rect_ground = pygame.Rect(self.rect.left+10, self.rect.bottom-10, self.width,10)
        self.nivel_actual = nivel_actual
        self.grupo_jugador = pygame.sprite.GroupSingle()
        self.grupo_jugador.add(self)
        self.grupo_proyectiles_jugador = pygame.sprite.Group()
        
        self.sonido_disparo = pygame.mixer.Sound("recursos\sounds\efectos\disparo.wav")
        self.sonido_jump = pygame.mixer.Sound("recursos\sounds\efectos\jump.wav")
        self.sonido_daño = pygame.mixer.Sound("recursos\sounds\efectos\dieenemy.wav")
        self.sonido_latidos = pygame.mixer.Sound("recursos\sounds\efectos\latidos.mp3")
        self.sonido_recoleccion = pygame.mixer.Sound("recursos\sounds\efectos\life_pickup.mp3")
        
        self.is_shooting = False
        self.cooldown = 1000
        self.tiempo_ultimo_disparo = 0
    
    def draw(self,screen:pygame.surface):
        screen.blit(self.animacion_actual[self.frame_actual],self.rect)
        if DEBUG:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
           
        
    def aplicar_gravedad(self):
        if self.is_jump or self.coord_y < ALTO_VENTANA - self.height: #aca estoy aplicando gravedad cuando el personaje salta o cuando no esta en el piso
            #poner la animacion de saltar
            #self.coord_y -= self.velocidad_y
            self.add_y(-self.velocidad_y)
            self.velocidad_y -= 1  
            
            #Esto controla que el jugador no se vaya por abajo de la pantalla ARREGLAR INTEGRAR A COTROLAR_LIMITES_PANTALLA
            if self.coord_y >= ALTO_VENTANA - self.height:  
                #self.coord_y = ALTO_VENTANA - self.height
                self.set_y(ALTO_VENTANA - self.height)
                self.is_jump = False
                self.velocidad_y = 0
        
    def actualizar(self, grupo_frutas:pygame.sprite.Group, lista_eventos, lista_teclas, screen: pygame.Surface,\
                    grupo_trampas:pygame.sprite.Group,grupo_enemigos:pygame.sprite.Group):
        self.draw(screen)
        self.mover(lista_teclas)
        self.rect.x = self.coord_x
        self.rect.y = self.coord_y
        self.disparar(lista_eventos)
        self.controlar_limites_pantalla()
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.frame_tiempo_anterior > self.frame_tiempo_intervalo:
            self.frame_tiempo_anterior = tiempo_actual
            self.frame_actual = (self.frame_actual + 1) % len(self.stand_r)
            self.image = self.stand_r[self.frame_actual]

        self.aplicar_gravedad()
        self.controlar_daño_por_trampas(grupo_trampas)
        self.controlar_recoleccion_frutas(grupo_frutas)
        self.hubo_colision(grupo_enemigos)
        self.cotrolar_daños_por_disparo_enemigo(grupo_enemigos)
        if self.vida <= 30:
            self.sonido_latidos.play()
            
    def cotrolar_daños_por_disparo_enemigo(self, grupo_enemigo:pygame.sprite.Group):
        for enemigo in grupo_enemigo:
            for disparo in enemigo.grupo_proyectiles_enemigo:
                if disparo.rect.colliderect(self.rect):
                    disparo.kill()
                    print("Me dispararon")
                    self.sonido_daño.play()
                    self.vida -= 1
        
    def controlar_daño_por_trampas(self, grupo_trampas:pygame.sprite.Group):
        for trampa in grupo_trampas:
            if self.rect.colliderect(trampa.rect):
                self.vida -= 2
                print('colisione con una trampa')
                
    def controlar_recoleccion_frutas(self, grupo_frutas:pygame.sprite.Group):
        for fruta in grupo_frutas:
            if fruta.item_activo and self.rect.colliderect(fruta.rect) and self.vida != 100:
                self.sonido_recoleccion.play()
                self.score += 10
                if self.vida < 80:
                    self.vida = min(self.vida + 20, 100)  # Aumentar en 20 sin pasar de 100
                print('Colisioné con una fruta')
            
    def mover(self, lista_teclas: list):
            #CORRER DERECHA
        if lista_teclas[pygame.K_d] and lista_teclas[pygame.K_LSHIFT]  and not self.is_jump:
            self.animacion_actual = self.run_r
            self.is_looking_right = True
            #self.coord_x += self.velocidad_run
            self.add_x(self.velocidad_run)
            
          #CORRER A LA IZQUIERDA  
        elif lista_teclas[pygame.K_a] and lista_teclas[pygame.K_LSHIFT] and not self.is_jump:
            self.animacion_actual = self.run_l
            self.is_looking_right = False
            #self.coord_x -= self.velocidad_run  
            self.add_x(-self.velocidad_run)
            
            #CAMINAR A LA DERECHA
        elif lista_teclas[pygame.K_d]:
            self.animacion_actual = self.walk_r
            #self.coord_x += self.velocidad_walk
            self.add_x(self.velocidad_walk)
            self.is_looking_right = True
            
            #CAMINAR A LA IZQUIERDA
        elif lista_teclas[pygame.K_a]:
            self.animacion_actual = self.walk_l
            #self.coord_x -= self.velocidad_walk
            self.add_x(-self.velocidad_walk)
            self.is_looking_right = False
            #QUEDARSE QUIETO
        else:
            if self.is_looking_right:
                self.animacion_actual = self.stand_r
            else:
                self.animacion_actual = self.stand_l
                
            #SALTAR
        if lista_teclas[pygame.K_SPACE] and not self.is_jump:
            #self.add_y(-self.velocidad_y)
            #self.animacion_actual = self.jump_r
            self.is_jump = True
            self.velocidad_y = 19
            
            #self.add_y(self.altura_salto)
            self.sonido_jump.play()
            
            
    
    def disparar(self, lista_eventos):
        tiempo_actual = pygame.time.get_ticks()
        for evento in lista_eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_e and not self.is_jump and not self.is_shooting and tiempo_actual - self.tiempo_ultimo_disparo >= self.cooldown:
                    self.tiempo_ultimo_disparo = tiempo_actual
                    self.is_shooting = True
                    self.sonido_disparo.play()
                    proyectil = Proyectil(self.rect.centerx, self.rect.centery, 1 if self.is_looking_right else -1)
                    self.grupo_proyectiles_jugador.add(proyectil)
                else:    
                    self.is_shooting = False
            
    def controlar_limites_pantalla(self):
        if self.rect.right >= ANCHO_VENTANA:
            #self.coord_x = ANCHO_VENTANA - self.rect.width
            self.set_x(ANCHO_VENTANA - self.rect.width)
        elif self.rect.left <= 0:
            #self.coord_x = 0
            self.set_x(0)
                    
    def hubo_colision(self, grupo_enemigos:pygame.sprite.Group):
        '''
        Si el jugador entra en cotacto con cualquier enemigo pierde diez punto de vida
        '''
        tiempo_actual = pygame.time.get_ticks()
        
        if tiempo_actual - self.tiempo_ultima_colision >= self.tiempo_entre_colisiones:
            for enemigo in grupo_enemigos:
                if self.rect.colliderect(enemigo.rect) and not self.hubo_colision_previa:
                    if DEBUG:
                        pass
                        #print("Hubo colisión")
                        #print(f'Te quedan: {self.vida} puntos de vida')
                    self.sonido_daño.play()
                    self.vida -= 10
                    self.hubo_colision_previa = True
                    self.tiempo_ultima_colision = tiempo_actual
        else:
            self.hubo_colision_previa = False
            
            
    
    def add_x(self, delta_x):
        self.coord_x += delta_x
        self.rect_ground.x += delta_x

    def add_y(self, delta_y):
        self.coord_y += delta_y
        self.rect_ground.y += delta_y
        
    def set_x(self, delta_x):
        self.coord_x = delta_x
        self.rect_ground.x = delta_x
        
    def set_y(self, delta_y):
        self.coord_y = delta_y
        self.rect_ground.y = delta_y
        
    def esta_muerto(self)->bool:
        return self.vida <= 0
    
