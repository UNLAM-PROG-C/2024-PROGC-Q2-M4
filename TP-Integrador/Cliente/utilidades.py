import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame

ventana = contexto_juego.obtener_ventana() 

def posicionar_botones(botones, espaciado, posicion_y):
    ancho_total = sum(boton.rect.width for boton in botones) + espaciado * (len(botones) - 1)
    inicio_x = (ventana.get_width() - ancho_total) // 2

    for i, boton in enumerate(botones):
        boton.establecer_posicion(inicio_x + i * (boton.rect.width + espaciado), posicion_y)

def verificar_cambio_icono_cursor(botones):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for boton in botones:
        if boton.rect.collidepoint(mouse_x, mouse_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) 
