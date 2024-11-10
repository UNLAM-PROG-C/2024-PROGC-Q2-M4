import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame

ventana = contexto_juego.obtener_ventana()  # Obtener la ventana

def posicionar_botones(botones, espaciado, posicion_y):
    """
    Posiciona un conjunto de botones horizontalmente centrados en la ventana.
    
    Args:
        botones (list[Button]): Lista de botones a posicionar.
        espaciado (int): Espaciado entre los botones.
        posicion_y (int): La posición Y donde se alinearán los botones.
    """
    ancho_total = sum(boton.rect.width for boton in botones) + espaciado * (len(botones) - 1)
    inicio_x = (ventana.get_width() - ancho_total) // 2

    for i, boton in enumerate(botones):
         # Usar el método set_position para establecer las posiciones
        boton.establecer_posicion(inicio_x + i * (boton.rect.width + espaciado), posicion_y)

def verificar_cambio_icono_cursor(botones):
    """
    Cambia el icono del cursor si está sobre uno de los botones en la lista.

    Args:
        botones (list[Button]): Lista de botones a comprobar.
    """
    # Obtener la posición del mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Verificar si el cursor está sobre algún botón
    for boton in botones:
        if boton.rect.collidepoint(mouse_x, mouse_y):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Cursor de mano del sistema
            return

    # Si no se colisiona con ningún botón, se restablece el cursor
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Cursor de flecha del sistema

