from jugador import Jugador
from enemigo import Enemigo
from plataforma import Plataforma
from item import Item
from proyectil import Proyectil
from auxiliar import SurfaceManager
from constantes import *



def gestionar_niveles(jugador:Jugador, nivel_actual:int): #evaluar si hace falta que reciba al jugador, evaluar si hace falta que reciba el diccionario configuaraciones
    
    match(nivel_actual):
        case 1:
            configuraciones = SurfaceManager.get_config('config.json').get('nivel_1')
                       
        case 2:
            configuraciones = SurfaceManager.get_config('config.json').get('nivel_2')
                
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
        trampa_actual = Item(coordenas_fruta[i].get("x"), coordenas_fruta[i].get("y"))
        grupo_trampas.add(trampa_actual)
