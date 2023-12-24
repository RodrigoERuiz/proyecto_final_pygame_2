import pygame, sys
from button import Button
from constantes import * 

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("recursos/sounds/ambiente/Prórroga de Tiempo A.ogg")

SCREEN = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG = pygame.transform.scale(BG, (ANCHO_VENTANA, ALTO_VENTANA))
global its_running      #la declare para intentar poner el juego en pausa pero no funcionó
its_running = True 
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)


def main_menu():
    while True:
        
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        LEVEL_1_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 250), 
                            text_input="LEVEL 1", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        LEVEL_2_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="LEVEL 2", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SOUND_MUTE = Button(image=pygame.image.load("recursos/GUI/buttons/audioMute.png"), pos=(1200, 600), 
                            text_input=None, font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SOUND_PLUS = Button(image=pygame.image.load("recursos/GUI/buttons/audioPlus.png"), pos=(1200, 680), 
                            text_input=None, font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [LEVEL_1_BUTTON, LEVEL_2_BUTTON, QUIT_BUTTON, SOUND_MUTE, SOUND_PLUS]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                global its_running
                if event.key == pygame.K_ESCAPE:
                    its_running = not its_running
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL_1_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from primer_nivel import correr_nivel_1
                    correr_nivel_1(its_running)
                if LEVEL_2_BUTTON.checkForInput(MENU_MOUSE_POS):
                    from segundo_nivel import correr_nivel_2
                    correr_nivel_2()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if SOUND_MUTE.checkForInput(MENU_MOUSE_POS):
                    print("presioné el boton de mute")
                    pygame.mixer.music.stop()
                if SOUND_PLUS.checkForInput(MENU_MOUSE_POS):
                    print("presioné el boton de sonido")
                    pygame.mixer.music.play(-1)
                    

        pygame.display.update()

main_menu()