import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame

ventana = contexto_juego.obtener_ventana()

class Boton:

    def __init__(self, texto, x, y, ancho, alto, color, color_claro=None, color_borde=None, tamano_borde=None, color_texto_claro=None, accion=None):
        self.texto = texto
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.color = color
        self.color_claro = color_claro
        self.color_borde = color_borde
        self.tamano_borde = tamano_borde if color_borde is None else constantes.TAMANIO_BORDE_POR_DEFECTO
        self.color_texto_claro = color_texto_claro or self.texto.color
        self.accion = accion

        # Actualizamos la posición del texto para centrarlo dentro del botón
        self.texto.posicion_x = self.rect.centerx
        self.texto.posicion_y = self.rect.centery

        # Centramos el texto dentro del botón usando las dimensiones del rectángulo del texto
        self._actualizar_posicion_texto()

    # Métodos Públicos

    def dibujar(self):
        # Cambia el color del botón si el mouse está sobre él
        posicion_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion_mouse):
            color = self.color_claro if self.color_claro else self.color
            color_texto = self.color_texto_claro if self.color_texto_claro else self.texto.color
        else:
            color = self.color
            color_texto = self.texto.color

        # Dibuja el botón
        pygame.draw.rect(ventana, color, self.rect)

        # Dibuja el borde del botón, si se especifica
        if self.color_borde is not None:
            pygame.draw.rect(ventana, self.color_borde, self.rect, self.tamano_borde)

        # Cambiar temporalmente el color del texto si es necesario
        color_original = self.texto.color
        self.texto.color = color_texto
        self.texto.dibujar()

        # Restaurar el color original después de dibujar
        self.texto.color = color_original

    def dibujar_gris(self):
        # Definir el color gris para el botón y el texto
        color_gris = (128, 128, 128)
        color_texto_gris = (192, 192, 192)

        # Dibujar el botón en gris
        pygame.draw.rect(ventana, color_gris, self.rect)

        # Dibujar el borde del botón si está especificado
        if self.color_borde is not None:
            pygame.draw.rect(ventana, color_gris, self.rect, self.tamano_borde)

        # Cambiar temporalmente el color del texto a gris
        color_original = self.texto.color
        self.texto.color = color_texto_gris
        self.texto.dibujar()

        # Restaurar el color original después de dibujar
        self.texto.color = color_original

    def es_presionado(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def establecer_posicion(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self._actualizar_posicion_texto()

    # Métodos Privados

    def _actualizar_posicion_texto(self):
        # Cargar la fuente y renderizar temporalmente el texto para obtener su tamaño
        fuente_texto = pygame.font.Font(constantes.RUTA_FUENTES + self.texto.fuente, self.texto.tamaño)
        superficie_texto = fuente_texto.render(self.texto.contenido, True, self.texto.color)

        # Obtener el rectángulo del texto
        rect_texto = superficie_texto.get_rect(center=self.rect.center)

        # Asignar la nueva posición centrada al texto
        self.texto.posicion_x = rect_texto.x
        self.texto.posicion_y = rect_texto.y
