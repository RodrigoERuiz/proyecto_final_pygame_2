import json
import pygame, random
#from plataforma import *

class SurfaceManager:

    @staticmethod
    def get_surface_from_spritesheet(img_path: str, cols: int, rows: int, step = 1, flip: bool = False) -> list[pygame.surface.Surface]:
        sprites_list = list()
        surface_img = pygame.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_height = int(surface_img.get_height()/rows)

        for row in range(rows):

            for column in range(0, cols, step):
                x_axis = column * frame_width
                y_axis = row * frame_height

                frame_surface = surface_img.subsurface(
                    x_axis, y_axis, frame_width, frame_height
                )

                if flip:
                    frame_surface = pygame.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        return sprites_list
    
    @staticmethod
    def girar_sprites(lista_imagenes)->list:
       return [pygame.transform.flip(imagen, True, False) for imagen in lista_imagenes]
    
    @staticmethod
    def preparar_imagen(lista_imagenes:list[pygame.Surface], ancho, alto,):
        lista_retorno = []
        for imagen in lista_imagenes:
            imagen_escalada = pygame.transform.scale(imagen,(ancho,alto))
            lista_retorno.append(imagen_escalada)
        return lista_retorno
    
    
    @staticmethod
    def draw_text(surface: pygame.Surface, text: str, size: int, x, y):
        font = pygame.font.SysFont('Serif', size)
        text_surface = font.render(text, True, 'white')
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
        
    @staticmethod
    def draw_dibujar_barra_de_vida(pantalla: pygame.Surface, x, y, porcentaje_vida: int):
        ancho_barra = 100
        alto_barra = 10
        relleno = (porcentaje_vida / 100) * ancho_barra
        borde_barra = pygame.Rect(x, y, ancho_barra, alto_barra)
        relleno = pygame.Rect(x, y, relleno, alto_barra)
        pygame.draw.rect(pantalla, 'green', relleno)
        pygame.draw.rect(pantalla, 'white', borde_barra, 2)
    
    @staticmethod
    def game_over():
        return True

    @staticmethod
    def get_config(path:str):
        try:
            with open(path, 'r', encoding='UTF-8') as archivo:
                lista_de_jugadores = json.load(archivo)
                return lista_de_jugadores
        except FileNotFoundError:
            print("Error: Archivo no encontrado")
            return None
        
# class funcionesAuxiliares():
#     @staticmethod
#     def verificar_transicion_nivel(grupo_enemigos:pygame.sprite.Group,jugador):
#         if not grupo_enemigos:
#             jugador.nivel_actual += 1
#             return True
class funcionesAuxiliares():
    @staticmethod
    def verificar_transicion_nivel(grupo_enemigos: pygame.sprite.Group, jugador):
        if not grupo_enemigos:
            jugador.nivel_actual += 1
            for enemigo in grupo_enemigos:
                enemigo.aumentar_nivel()
            return True

            
