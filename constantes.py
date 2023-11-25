import pygame

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
FPS = 30
DEBUG = True

SCREEN = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

backgound = pygame.image.load('recursos/backgrounds/41530.jpg').convert_alpha()
backgound = pygame.transform.scale(backgound,(ANCHO_VENTANA,ALTO_VENTANA))
PLATAFORMA_IMAGE = pygame.image.load('recursos/plataformas/plataforma.png')

NRO_PLATAFORMAS_LVL_1 = 6