from constantes import *
from jugador import Jugador
from enemigo import Enemigo
from plataforma import *
import pygame
from auxiliar import *
from item import Item
from trampa import Trampa


def correr_nivel_1():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("C:/Users/RODRIGO/Desktop/pygame desde cero/recursos/sounds/ambiente/ambiente.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    reloj = pygame.time.Clock()


    its_running = True

    jugador = Jugador(500,200,5,1)

    grupo_proyectiles_jugador = pygame.sprite.Group()
    grupo_proyectiles_enemigo = pygame.sprite.Group()

    configuraciones = SurfaceManager.get_config('config.json').get('nivel_1')
    
                        
    fondo = pygame.image.load(configuraciones.get('background'))
    fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))
    
    #PLATAFORMAS
    plataformas = pygame.sprite.Group()
    plataformas.add(Plataforma.crear_lista_plataformas(configuraciones.get('plataformas_coord'),200))

    #ENEMIGOS
    grupo_enemigos = pygame.sprite.Group()
    grupo_enemigos.add(Enemigo.crear_lista_de_enemigos(configuraciones.get('cantidad_enemigos'),12,configuraciones.get('enemigo').get('coords'),jugador.nivel_actual))
    
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
    while its_running:
        
        reloj.tick(FPS)
        lista_eventos = pygame.event.get()
        for evento in lista_eventos:
            if evento.type == pygame.QUIT:
                its_running = False
                break
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                print(evento)
        if jugador.esta_muerto() or len(grupo_enemigos) == 0: 
            from GUI_main import main_menu 
            main_menu()
        
        SCREEN.blit(fondo,(0,0))
        
        teclas_presionadas = pygame.key.get_pressed()
        
        plataformas.update(SCREEN,jugador,plataformas)
        grupo_frutas.update(grupo_frutas,SCREEN,jugador)
        grupo_trampas.update(SCREEN)
        grupo_proyectiles_jugador.update(SCREEN, grupo_enemigos, grupo_proyectiles_enemigo, jugador, plataformas,grupo_proyectiles_jugador)
        grupo_proyectiles_enemigo.update(SCREEN, grupo_enemigos, grupo_proyectiles_jugador, jugador, plataformas,grupo_proyectiles_jugador)
        

        #Enemigos   
        enemigos_vivos = len(grupo_enemigos)        
        for enemigo in grupo_enemigos:
            #print(f'vida enemigo: {enemigo.lives}')
            enemigo.draw(SCREEN)
            enemigo.update(grupo_proyectiles_jugador,grupo_enemigos,jugador)

            # if enemigo.esta_muerto():
            #     jugador.score += 10
            #     enemigo.hacer_animacion('die')
            #     enemigo.kill()

    
        jugador.actualizar(plataformas, grupo_frutas, lista_eventos, teclas_presionadas, SCREEN, grupo_proyectiles_jugador,grupo_trampas,grupo_enemigos)
        
        SurfaceManager.draw_text(SCREEN, f'tiempo: {int(pygame.time.get_ticks()/1000)}', 25, ANCHO_VENTANA -70, 10)
        SurfaceManager.draw_text(SCREEN, f'Puntuación: {str(jugador.score)}', 25, ANCHO_VENTANA // 2, 10)
        SurfaceManager.draw_dibujar_barra_de_vida(SCREEN,5,5,jugador.vida)
        

        pygame.display.update()

    pygame.quit()
    
    # if __name__ == "__main__":
    #     correr_juego()