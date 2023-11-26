from constantes import *
from jugador import Jugador
from enemigo import Enemigo
from plataforma import *
import pygame
from auxiliar import *
from item import Item
from trampa import Trampa
from gestor_niveles import gestionar_niveles

pygame.init()
reloj = pygame.time.Clock()



# path = configuraciones.get('background')
# fondo = pygame.image.load(path)
# fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))


its_running = True

jugador = Jugador(70,0,5)

# enemigos = Enemigo.crear_lista_de_enemigos(3,120)
# grupo_enemigos = pygame.sprite.Group()
# grupo_enemigos.add(enemigos)

# plataforma = Plataforma(200,500,100)
# plataforma_dos = Plataforma(400,400,100)
# plataforma_tres = Plataforma(600,300,100)

# plataformas = pygame.sprite.Group()
# plataformas.add(plataforma)
# plataformas.add(plataforma_dos)
# plataformas.add(plataforma_tres)

grupo_proyectiles = pygame.sprite.Group()

# fruta = Item(425,358)
# grupo_frutas = pygame.sprite.Group()
# fruta_dos = Item(ANCHO_VENTANA-100,400)
# grupo_frutas.add(fruta)
# grupo_frutas.add(fruta_dos)

# trampas = pygame.sprite.Group()
# trampa = Trampa(457, 365)
# trampa_dos = Trampa(649, 266)
# trampa_tres = Trampa(247, 470)
# trampas.add(trampa)
# trampas.add(trampa_dos)
# trampas.add(trampa_tres)

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
        enemigos = Enemigo.crear_lista_de_enemigos(configuraciones.get('cantidad_enemigos'),120)
        grupo_enemigos = pygame.sprite.Group()
        grupo_enemigos.add(enemigos)
        
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
    #print(f'vidas:{jugador.vida}')
    if jugador.esta_muerto(): 
        #hacer animacion de muerte y pantalla de tocar una tecla para reiniciar
        break
    
        
    SCREEN.blit(fondo,(0,0))
    

    teclas_presionadas = pygame.key.get_pressed()
    
    
    jugador.actualizar(plataformas, grupo_frutas, lista_eventos, teclas_presionadas, SCREEN, grupo_proyectiles)
    plataforma.update(SCREEN,jugador,plataformas)
    for fruta in grupo_frutas:
        fruta.update(grupo_frutas,SCREEN,jugador)
    
    #Enemigos   
    enemigos_vivos = len(grupo_enemigos)        # hacer en el modulo enemigos
    for enemigo in grupo_enemigos:
        
        #print(f'enemigos vivos {enemigos_vivos}')
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
        jugador.nivel_actual = 2
        cargar_configuraciones = True
        #print('nivel terminado')

        
    grupo_proyectiles.update()
    grupo_proyectiles.draw(SCREEN)
    SurfaceManager.draw_text(SCREEN, f'Puntuación: {str(jugador.score)}', 25, ANCHO_VENTANA // 2, 10)
    SurfaceManager.draw_dibujar_barra_de_vida(SCREEN,5,5,jugador.vida)
     
    for trampa in grupo_trampas: #implementarlo en trmapa.update
        if jugador.rect.colliderect(trampa.rect):
            jugador.vida -= 5
    grupo_trampas.update()
    grupo_trampas.draw(SCREEN)   
    
    pygame.display.update()

pygame.quit()