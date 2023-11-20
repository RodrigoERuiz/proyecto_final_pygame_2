from constantes import *
from jugador import Jugador
from enemigo import Enemigo
from plataforma import *
import pygame
from auxiliar import *
from item import Item


pygame.init()
reloj = pygame.time.Clock()

its_running = True

jugador = Jugador(70,0,5)
enemigos = Enemigo.crear_lista_de_enemigos(5,120)
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


grupo_frutas = pygame.sprite.Group()
fruta = Item(425,358)
fruta_dos = Item(ANCHO_VENTANA-100,10)
grupo_frutas.add(fruta)
grupo_frutas.add(fruta_dos)


while its_running:
    reloj.tick(FPS)
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            its_running = False
            break
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(evento)
    
    SCREEN.blit(backgound,(0,0))  
    
    teclas_presionadas = pygame.key.get_pressed()
    plataformas.draw(SCREEN)
    
    #Jugador
    if DEBUG:
        pygame.draw.rect(SCREEN, (255, 0, 0), jugador.rect, 2)
    jugador.mover(teclas_presionadas,lista_eventos,grupo_proyectiles)
    jugador.actualizar(plataformas, grupo_frutas)
    SCREEN.blit(pygame.transform.scale(jugador.animacion_actual[jugador.frame_actual],(jugador.height,jugador.width)), jugador.rect)
    
    
    #plataforma
    for plataforma in plataformas:
        if DEBUG:   
            SCREEN.blit(plataforma.image,plataforma.rect)
        plataforma.mover_plataforma()
        if plataforma.rect.colliderect(jugador.rect): #sacar esto de acá
            if plataforma.rect.top <= jugador.rect.bottom:
                jugador.velocidad_y = 0
                jugador.is_jump = False

    
    #Enemigos
    for enemigo in grupo_enemigos:
        if DEBUG:
            pygame.draw.rect(SCREEN, (0, 255, 0), enemigo.rect, 2)
            
        SCREEN.blit(pygame.transform.scale(enemigo.animacion_actual[enemigo.frame_actual],(enemigo.height,enemigo.width)), enemigo.rect)
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
                # tiempo_actual = pygame.time.get_ticks()
                # if tiempo_actual-enemigo.frame_tiempo_anterior > enemigo.frame_tiempo_intervalo:
                #     enemigo.kill()
                
                
        
    grupo_proyectiles.update()
    grupo_proyectiles.draw(SCREEN)
    SurfaceManager.draw_text(SCREEN, f'Puntuación: {str(jugador.score)}', 25, ANCHO_VENTANA // 2, 10)
    SurfaceManager.draw_dibujar_barra_de_vida(SCREEN,5,5,jugador.vida)
    fruta.draw(SCREEN)
    fruta.update()
    pygame.display.update()



pygame.quit()