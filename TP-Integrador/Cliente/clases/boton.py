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
        self.texto.posicion_x = self.rect.centerx
        self.texto.posicion_y = self.rect.centery
        self._actualizar_posicion_texto()

    def dibujar(self):
        posicion_mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(posicion_mouse):
            color = self.color_claro if self.color_claro else self.color
            color_texto = self.color_texto_claro if self.color_texto_claro else self.texto.color
        else:
            color = self.color
            color_texto = self.texto.color
        pygame.draw.rect(ventana, color, self.rect)
        if self.color_borde is not None:
            pygame.draw.rect(ventana, self.color_borde, self.rect, self.tamano_borde)
        color_original = self.texto.color
        self.texto.color = color_texto
        self.texto.dibujar()
        self.texto.color = color_original

    def dibujar_gris(self):
        color_gris = (128, 128, 128)
        color_texto_gris = (192, 192, 192)
        pygame.draw.rect(ventana, color_gris, self.rect)
        if self.color_borde is not None:
            pygame.draw.rect(ventana, color_gris, self.rect, self.tamano_borde)
        color_original = self.texto.color
        self.texto.color = color_texto_gris
        self.texto.dibujar()
        self.texto.color = color_original

    def es_presionado(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def establecer_posicion(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self._actualizar_posicion_texto()

    def _actualizar_posicion_texto(self):
        fuente_texto = pygame.font.Font(constantes.RUTA_FUENTES + self.texto.fuente, self.texto.tamaño)
        superficie_texto = fuente_texto.render(self.texto.contenido, True, self.texto.color)
        rect_texto = superficie_texto.get_rect(center=self.rect.center)
        self.texto.posicion_x = rect_texto.x
        self.texto.posicion_y = rect_texto.y
