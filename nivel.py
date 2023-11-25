import pygame

class Nivel:
    def __init__(self, pantalla, jugador, plataformas, background) -> None:
        self.pantalla = pantalla
        self.jugador = jugador
        self.plataformas = plataformas
        self.background = background
        
    def update(self, lista_eventos):
        pass