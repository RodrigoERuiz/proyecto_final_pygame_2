from constantes import *
from jugador import Jugador
from enemigo import Enemigo
from plataforma import *
import pygame
from auxiliar import *
from item import Item
from trampa import Trampa

pygame.init()
reloj = pygame.time.Clock()

'''
Hacer algo del estilo de
crear una bandera de si el nivel 1 esta terminado. Si no lo está, en la variable configuraciones cargo el nivel 1 sino alguno de los otros
'''
nivel_1_terminado = False
nivel_2_terminado = False
nivel_3_terminado = False

if not nivel_1_terminado:
    configuraciones = SurfaceManager.get_config('config.json').get('nivel_1') #Usar esta variable para cambiar de nivel
elif not nivel_2_terminado:
    configuraciones = SurfaceManager.get_config('config.json').get('nivel_2')

path = configuraciones.get('background')
fondo = pygame.image.load(path)
fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))


its_running = True

jugador = Jugador(70,0,5)

enemigos = Enemigo.crear_lista_de_enemigos(3,120)
grupo_enemigos = pygame.sprite.Group()
grupo_enemigos.add(enemigos)

plataforma = Plataforma(200,500,100)
plataforma_dos = Plataforma(400,400,100)
plataforma_tres = Plataforma(600,300,100)

plataformas = pygame.sprite.Group()
plataformas.add(plataforma)
plataformas.add(plataforma_dos)
plataformas.add(plataforma_tres)

grupo_proyectiles = pygame.sprite.Group()

fruta = Item(425,358)
grupo_frutas = pygame.sprite.Group()
fruta_dos = Item(ANCHO_VENTANA-100,400)
grupo_frutas.add(fruta)
grupo_frutas.add(fruta_dos)

trampas = pygame.sprite.Group()
trampa = Trampa(457, 365)
trampa_dos = Trampa(649, 266)
trampa_tres = Trampa(247, 470)
trampas.add(trampa)
trampas.add(trampa_dos)
trampas.add(trampa_tres)

while its_running:
    reloj.tick(FPS)
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            its_running = False
            break
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(evento)
    #print(f'vidas:{jugador.vida}')
    if jugador.esta_muerto(): break
    
    print(nivel_1_terminado)
    if nivel_1_terminado:
        nivel_1_terminado=None
        configuraciones = SurfaceManager.get_config('config.json').get('nivel_2')
        path = configuraciones.get('background')
        fondo = pygame.image.load(path)
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
        jugador.vida = 100
        enemigos = Enemigo.crear_lista_de_enemigos(configuraciones.get('cantidad_enemigos'),120)
        grupo_enemigos = pygame.sprite.Group()
        grupo_enemigos.add(enemigos)
        
    SCREEN.blit(fondo,(0,0))
    

    teclas_presionadas = pygame.key.get_pressed()
    
    
    jugador.actualizar(plataformas, grupo_frutas, lista_eventos, teclas_presionadas, SCREEN, grupo_proyectiles)
    plataforma.update(SCREEN,jugador,plataformas)
    fruta.update(grupo_frutas,SCREEN,jugador)
    
    #Enemigos
    enemigos_vivos = len(grupo_enemigos)
    for enemigo in grupo_enemigos:
        
        print(f'enemigos vivos {enemigos_vivos}')
        enemigo.draw(SCREEN)
        enemigo.actualizar()
        jugador.hubo_colision(enemigo.rect)
        for proyectil in grupo_proyectiles:
            enemigo.detectar_disparos(grupo_proyectiles)
            if proyectil.rect.colliderect(enemigo.rect) or proyectil.rect.right > ANCHO_VENTANA or proyectil.rect.left < 0:
                proyectil.kill()
            if enemigo.esta_muerto():
                jugador.score += 10
                enemigo.hacer_animacion('die')
                enemigo.kill()
                enemigo.actualizar()
    if enemigos_vivos == 0:
        nivel_1_terminado = True
        #print('nivel terminado')

        
    grupo_proyectiles.update()
    grupo_proyectiles.draw(SCREEN)
    SurfaceManager.draw_text(SCREEN, f'Puntuación: {str(jugador.score)}', 25, ANCHO_VENTANA // 2, 10)
    SurfaceManager.draw_dibujar_barra_de_vida(SCREEN,5,5,jugador.vida)
     
    for trampa in trampas:
        if jugador.rect.colliderect(trampa.rect):
            jugador.vida -= 5
    trampas.update()
    trampas.draw(SCREEN)   
    
    pygame.display.update()

pygame.quit()