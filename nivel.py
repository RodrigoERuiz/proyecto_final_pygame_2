import pygame
from jugador import Jugador

class Nivel:
    def __init__(self, pantalla, jugador, plataformas, background) -> None:
        self.pantalla = pantalla
        self.jugador = jugador
        self.plataformas = plataformas
        self.background = background
        
    def update(self, lista_eventos):
        pass
    

    def actualizar_pantalla(self):
        self.pantalla.blit(self.background)
        
        for plataforma in self.plataformas:
            plataforma.draw(self.pantalla)
            
        self.jugador.update(self.pantalla, self.plataformas)