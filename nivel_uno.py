from constantes import *
from jugador import Jugador
from enemigo import Enemigo
from plataforma import *
import pygame
from auxiliar import *
from item import Item
from trampa import Trampa
from nivel import Nivel


class Nivel_uno(Nivel):
    def __init__(self, pantalla) -> None:
        super().__init__(pantalla)
        
        self.configs = SurfaceManager.get_config('config.json').get('nivel_1')
        self.plataformas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.trampas = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.jugador = Jugador(500,200,5)
        
        



    its_running = True

    while its_running:
        
        fondo = pygame.image.load(self.configs.get('background'))
        fondo = pygame.transform.scale(fondo,(ANCHO_VENTANA,ALTO_VENTANA))

        #PLATAFORMAS
        coordenadas_plataformas = self.configs.get('plataformas_coord')
        plataforma = Plataforma(coordenadas_plataformas[0].get('x'),coordenadas_plataformas[0].get('y'),100)
        plataforma_dos = Plataforma(coordenadas_plataformas[1].get('x'),coordenadas_plataformas[1].get('y'),100)
        plataforma_tres = Plataforma(coordenadas_plataformas[2].get('x'),coordenadas_plataformas[2].get('y'),100)

        plataformas = pygame.sprite.Group()
        plataformas.add(plataforma)
        plataformas.add(plataforma_dos)
        plataformas.add(plataforma_tres)

        #ENEMIGOS
        coordenadas_enemigos = self.configs.get('enemigo').get('coords')
        enemigo_uno = Enemigo(coordenadas_enemigos[0].get('x'), coordenadas_enemigos[0].get('y') )
        enemigo_dos = Enemigo(coordenadas_enemigos[1].get('x'), coordenadas_enemigos[1].get('y') )
        enemigo_tres = Enemigo(coordenadas_enemigos[2].get('x'), coordenadas_enemigos[2].get('y') )
        grupo_enemigos = pygame.sprite.Group()
        grupo_enemigos.add(enemigo_uno)
        grupo_enemigos.add(enemigo_dos)
        grupo_enemigos.add(enemigo_tres)

        
        #FRUTAS
        coordenas_fruta = self.configs.get('coordenadas_frutas')
        grupo_frutas = pygame.sprite.Group()
        for i in range(len(coordenas_fruta)):
            fruta_actual = Item(coordenas_fruta[i].get("x"), coordenas_fruta[i].get("y"))
            grupo_frutas.add(fruta_actual)
            
        #TRAMPAS
        coordenadas_trampas = self.configs.get('coordenadas_trampas')
        grupo_trampas = pygame.sprite.Group()
        for i in range(len(coordenadas_trampas)):
            trampa_actual = Trampa(coordenadas_trampas[i].get("x"), coordenadas_trampas[i].get("y"))
            grupo_trampas.add(trampa_actual)
        