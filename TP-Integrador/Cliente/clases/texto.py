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

        # Si centrado es True, calcula la posición centrada
        if centrado:
            self._posicion_x = self._calcular_posicion_centrada_x()

    # _renderizar_texto: Es un método privado encargado de generar la superficie de texto (_superficie_texto) que 
    # contiene la representación gráfica del contenido de texto con la fuente, el tamaño y el color especificados.
    # Este método convierte el contenido de texto en una superficie de pygame que luego puede dibujarse en la ventana.
    # _renderizar_texto solo se llama cuando necesitas actualizar la representación del texto, como cuando cambias el
    # contenido, la fuente, el tamaño o el color.
    def _renderizar_texto(self):
        """Funcion privada para renderizar el texto."""
        fuente_texto = pygame.font.Font(constantes.RUTA_FUENTES + self._fuente, self._tamaño)
        return fuente_texto.render(self._contenido, True, self._color)

    # dibujar: Es un método público que simplemente coloca la superficie de texto (_superficie_texto) en la ventana 
    # (ventana) en las coordenadas (posicion_x, posicion_y).
    # dibujar es el método que efectivamente muestra el texto en pantalla en cada fotograma de tu juego, y generalmente 
    # se llama en el bucle de renderizado principal para actualizar la visualización.
    def dibujar(self):
        """Dibuja el texto en la pantalla. Si center_x es True, lo centra horizontalmente."""
        ventana.blit(self._superficie_texto, (self._posicion_x, self._posicion_y))

    def actualizar_contenido(self, nuevo_contenido):
        """Actualiza el contenido del texto y lo renderiza nuevamente."""
        # Solo renderiza si el contenido cambia
        if self._contenido != nuevo_contenido:
            self._contenido = nuevo_contenido
            self._superficie_texto = self._renderizar_texto()
            # Actualiza la posición centrada si se configuró inicialmente
            if self._posicion_x == self._calcular_posicion_centrada_x():
                self._posicion_x = self._calcular_posicion_centrada_x()

    def _calcular_posicion_centrada_x(self):
        """Calcula la posicion X centrada segun el tamanio de la ventana."""
        return (ventana.get_width() - self.ancho) // 2

    @property
    def ancho(self):
        return self._superficie_texto.get_width()

    @property
    def alto(self):
        return self._superficie_texto.get_height()

    # Getters
    
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

    # Setters

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
