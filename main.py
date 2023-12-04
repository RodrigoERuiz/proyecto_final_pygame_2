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

its_running = True

jugador = Jugador(500,200,5)

grupo_proyectiles = pygame.sprite.Group()

cargar_configuraciones = True
while its_running:
    
    nivel_actual = jugador.nivel_actual
    
    ##################################################################################
    if cargar_configuraciones:
        print("entró a cargar las configuraciones")
        match(nivel_actual):
            case 1:
                configuraciones = SurfaceManager.get_config('config.json').get('nivel_1')
                        
            case 2:
                configuraciones = SurfaceManager.get_config('config.json').get('nivel_2')
        cargar_configuraciones = False
                
        path = configuraciones.get('background')
        fondo = pygame.image.load(path)
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))

        #PLATAFORMAS
        coordenadas_plataformas = configuraciones.get('plataformas_coord')
        plataforma = Plataforma(coordenadas_plataformas[0].get('x'),coordenadas_plataformas[0].get('y'),100)
        plataforma_dos = Plataforma(coordenadas_plataformas[1].get('x'),coordenadas_plataformas[1].get('y'),100)
        plataforma_tres = Plataforma(coordenadas_plataformas[2].get('x'),coordenadas_plataformas[2].get('y'),100)

        plataformas = pygame.sprite.Group()
        plataformas.add(plataforma)
        plataformas.add(plataforma_dos)
        plataformas.add(plataforma_tres)

        #ENEMIGOS
        coordenadas_enemigos = configuraciones.get('enemigo').get('coords')
        enemigo_uno = Enemigo(coordenadas_enemigos[0].get('x'), coordenadas_enemigos[0].get('y') )
        enemigo_dos = Enemigo(coordenadas_enemigos[1].get('x'), coordenadas_enemigos[1].get('y') )
        enemigo_tres = Enemigo(coordenadas_enemigos[2].get('x'), coordenadas_enemigos[2].get('y') )
        grupo_enemigos = pygame.sprite.Group()
        grupo_enemigos.add(enemigo_uno)
        grupo_enemigos.add(enemigo_dos)
        grupo_enemigos.add(enemigo_tres)

        
        #FRUTAS
        coordenas_fruta = configuraciones.get('coordenadas_frutas')
        grupo_frutas = pygame.sprite.Group()
        for i in range(len(coordenas_fruta)):
            fruta_actual = Item(coordenas_fruta[i].get("x"), coordenas_fruta[i].get("y"))
            grupo_frutas.add(fruta_actual)
            
        #TRAMPAS
        coordenadas_trampas = configuraciones.get('coordenadas_trampas')
        grupo_trampas = pygame.sprite.Group()
        for i in range(len(coordenadas_trampas)):
            trampa_actual = Trampa(coordenadas_trampas[i].get("x"), coordenadas_trampas[i].get("y"))
            grupo_trampas.add(trampa_actual)
    
    ####################################################################################
    
    reloj.tick(FPS)
    lista_eventos = pygame.event.get()
    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            its_running = False
            break
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            print(evento)
    if jugador.esta_muerto(): 
        #hacer animacion de muerte y pantalla de tocar una tecla para reiniciar
        break
    
        
    SCREEN.blit(fondo,(0,0))
    

    teclas_presionadas = pygame.key.get_pressed()
    
    
    #jugador.actualizar(plataformas, grupo_frutas, lista_eventos, teclas_presionadas, SCREEN, grupo_proyectiles,grupo_trampas,grupo_enemigos)
    plataforma.update(SCREEN,jugador,plataformas)
    grupo_frutas.update(grupo_frutas,SCREEN,jugador) 
    grupo_trampas.update(SCREEN)
    grupo_proyectiles.update(SCREEN)
        
        
    
    #Enemigos   
    enemigos_vivos = len(grupo_enemigos)        
    for enemigo in grupo_enemigos:
        enemigo.draw(SCREEN)
        enemigo.update(grupo_proyectiles,grupo_enemigos,jugador)
        for proyectil in grupo_proyectiles:
            enemigo.detectar_disparos(grupo_proyectiles,grupo_enemigos)
            if proyectil.rect.colliderect(enemigo.rect) or proyectil.rect.right > ANCHO_VENTANA or proyectil.rect.left < 0:
                proyectil.kill()
            if enemigo.esta_muerto():
                jugador.score += 10
                enemigo.hacer_animacion('die')
                enemigo.kill()
                #enemigo.update()
    # for enemigo in grupo_enemigos:
    #     enemigo.update(grupo_proyectiles,grupo_enemigos, jugador)
    
    cargar_configuraciones = jugador.actualizar(plataformas, grupo_frutas, lista_eventos, teclas_presionadas, SCREEN, grupo_proyectiles,grupo_trampas,grupo_enemigos)


        
    
    SurfaceManager.draw_text(SCREEN, f'Puntuación: {str(jugador.score)}', 25, ANCHO_VENTANA // 2, 10)
    SurfaceManager.draw_dibujar_barra_de_vida(SCREEN,5,5,jugador.vida)
     

    pygame.display.update()

pygame.quit()