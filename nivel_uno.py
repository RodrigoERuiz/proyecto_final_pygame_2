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
    def __init__(self, pantalla, jugador,plataformas,background) -> None:
        super().__init__(pantalla,jugador,plataformas,background)
        
        self.configs = SurfaceManager.get_config('config.json').get('nivel_1')
        self.plataformas = pygame.sprite.Group()
        self.enemigos = pygame.sprite.Group()
        self.trampas = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.proyectiles_jugador = pygame.sprite.Group()
        self.proyectiles_enmigo = pygame.sprite.Group()      
        self.jugador = Jugador(500,200,5)
        self.background = self.configs.get('nivel_1').get('background')
        self.background = pygame.transform.scale(self.background,(ANCHO_VENTANA,ALTO_VENTANA))
        
        

# Crear instancia de Nivel_uno
nivel_actual = Nivel_uno(SCREEN)


coordenadas_plataformas = nivel_actual.configs.get('plataformas_coord')
plataforma = Plataforma(coordenadas_plataformas[0].get('x'),coordenadas_plataformas[0].get('y'),100)
plataforma_dos = Plataforma(coordenadas_plataformas[1].get('x'),coordenadas_plataformas[1].get('y'),100)
plataforma_tres = Plataforma(coordenadas_plataformas[2].get('x'),coordenadas_plataformas[2].get('y'),100)

nivel_actual.plataformas.add(plataforma)
nivel_actual.plataformas.add(plataforma_dos)
nivel_actual.plataformas.add(plataforma_tres)

#ENEMIGOS
coordenadas_enemigos = nivel_actual.configs.get('enemigo').get('coords')
enemigo_uno = Enemigo(coordenadas_enemigos[0].get('x'), coordenadas_enemigos[0].get('y') )
enemigo_dos = Enemigo(coordenadas_enemigos[1].get('x'), coordenadas_enemigos[1].get('y') )
enemigo_tres = Enemigo(coordenadas_enemigos[2].get('x'), coordenadas_enemigos[2].get('y') )
nivel_actual.grupo_enemigos.add(enemigo_uno)
nivel_actual.grupo_enemigos.add(enemigo_dos)
nivel_actual.grupo_enemigos.add(enemigo_tres)


#FRUTAS
coordenas_fruta = nivel_actual.configs.get('coordenadas_frutas')
for i in range(len(coordenas_fruta)):
    fruta_actual = Item(coordenas_fruta[i].get("x"), coordenas_fruta[i].get("y"))
    nivel_actual.items.add(fruta_actual)
    
#TRAMPAS
coordenadas_trampas = nivel_actual.configs.get('coordenadas_trampas')
for i in range(len(coordenadas_trampas)):
    trampa_actual = Trampa(coordenadas_trampas[i].get("x"), coordenadas_trampas[i].get("y"))
    nivel_actual.trampas.add(trampa_actual)
    