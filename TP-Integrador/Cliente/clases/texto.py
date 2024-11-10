import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame

ventana = contexto_juego.obtener_ventana()

class Texto:
    def __init__(self, contenido, fuente, tamaño, color=constantes.COLOR_NEGRO_TUPLA, posicion_x=0, posicion_y=0, centrado=False):
        self._contenido = contenido
        self._fuente = fuente
        self._tamaño = tamaño
        self._color = color
        self._posicion_x = posicion_x
        self._posicion_y = posicion_y
        self._superficie_texto = self._renderizar_texto()
        if centrado:
            self._posicion_x = self._calcular_posicion_centrada_x()

    def _renderizar_texto(self):
        fuente_texto = pygame.font.Font(constantes.RUTA_FUENTES + self._fuente, self._tamaño)
        return fuente_texto.render(self._contenido, True, self._color)

    def dibujar(self):
        ventana.blit(self._superficie_texto, (self._posicion_x, self._posicion_y))

    def actualizar_contenido(self, nuevo_contenido):
        if self._contenido != nuevo_contenido:
            self._contenido = nuevo_contenido
            self._superficie_texto = self._renderizar_texto()
            if self._posicion_x == self._calcular_posicion_centrada_x():
                self._posicion_x = self._calcular_posicion_centrada_x()

    def _calcular_posicion_centrada_x(self):
        return (ventana.get_width() - self.ancho) // 2

    @property
    def ancho(self):
        return self._superficie_texto.get_width()

    @property
    def alto(self):
        return self._superficie_texto.get_height()
    
    @property
    def contenido(self):
        return self._contenido
    
    @property
    def fuente(self):
        return self._fuente
    
    @property
    def tamaño(self):
        return self._tamaño

    @property
    def color(self):
        return self._color

    @property
    def posicion_x(self):
        return self._posicion_x

    @property
    def posicion_y(self):
        return self._posicion_y

    @contenido.setter
    def contenido(self, valor):
        if not valor:
            raise ValueError("El contenido del texto no puede estar vacío.")
        self._contenido = valor
        self._superficie_texto = self._renderizar_texto()

    @fuente.setter
    def fuente(self, valor):
        self._fuente = valor
        self._superficie_texto = self._renderizar_texto()
    
    @tamaño.setter
    def tamaño(self, valor):
        if valor <= 0:
            raise ValueError("El tamaño de la fuente debe ser mayor a 0.")
        self._tamaño = valor
        self._superficie_texto = self._renderizar_texto()
    
    @color.setter
    def color(self, valor):
        if not isinstance(valor, tuple) or len(valor) != 3:
            raise ValueError("El color debe ser una tupla con tres valores (RGB).")
        self._color = valor
        self._superficie_texto = self._renderizar_texto()
    
    @posicion_x.setter
    def posicion_x(self, valor):
        if valor < 0:
            raise ValueError("La posición en X no puede ser negativa.")
        self._posicion_x = valor
    
    @posicion_y.setter
    def posicion_y(self, valor):
        if valor < 0:
            raise ValueError("La posición en Y no puede ser negativa.")
        self._posicion_y = valor
