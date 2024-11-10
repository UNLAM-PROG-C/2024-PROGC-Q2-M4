import pygame
import utilidades  # Utilidades
from clases.fondo_animado import FondoAnimado  # Cambié "BackgroundAnimated" a "FondoAnimado"
from clases.boton import Boton  # Cambié "Button" a "Boton"
from clases.texto import Texto  # Cambié "Text" a "Texto"

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego

# =========================================== Variables ===========================================

ventana = contexto_juego.obtener_ventana()

# =========================================== Interfaz ===========================================

def crear_botones():
    """
    Crea los botones de 'Jugar' y 'Salir' con sus respectivas propiedades.
    
    Los botones incluyen funcionalidad para detectar clics y cambiar 
    el color cuando el cursor pasa sobre ellos. Cada botón se inicializa 
    con propiedades como tamaño, colores, posición y texto.

    Returns:
        tuple(Boton, Boton): Una tupla que contiene el botón de 'Jugar' 
        y el botón de 'Salir', ambos instancias de la clase Boton.
    """
    
    # Inicialización de los textos de los botones
    texto_jugar = Texto(constantes.JUGAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TEXTO_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)
    texto_salir = Texto(constantes.SALIR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TEXTO_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)

    boton_jugar = Boton(
        texto_jugar,
        constantes.POSICION_X_BOTONES_MENU_PRINCIPAL,
        constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL,
        constantes.ANCHO_BOTONES_MENU_PRINCIPAL,
        constantes.ALTO_BOTONES_MENU_PRINCIPAL,
        constantes.COLOR_VERDE_TUPLA,
        constantes.COLOR_VERDE_CLARO_TUPLA,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.BORDES_BOTON_PX,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.ACCION_JUGAR
    )

    boton_salir = Boton(
        texto_salir,
        constantes.POSICION_X_BOTONES_MENU_PRINCIPAL,
        constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL,
        constantes.ANCHO_BOTONES_MENU_PRINCIPAL,
        constantes.ALTO_BOTONES_MENU_PRINCIPAL,
        constantes.COLOR_ROJO_TUPLA,
        constantes.COLOR_ROJO_CLARO_TUPLA,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.BORDES_BOTON_PX,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.ACCION_SALIR
    )

    utilidades.posicionar_botones([boton_jugar, boton_salir], constantes.ESPACIADO_BOTONES_MENU_PRINCIPAL, constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL)

    return boton_jugar, boton_salir

def crear_palabras_nombre_juego():
    """
    Crea los objetos de texto para el nombre del juego, palabra por palabra,
    y los devuelve en una lista.
    Returns: list[Texto]: Lista de objetos `Texto` que representan las palabras del nombre del juego.
    """
    posicion_y = constantes.POSICION_Y_TITULO_MENU_PRINCIPAL
    
    # Espaciado entre palabras
    espaciado = constantes.TAMANO_FUENTE_TITULO_MENU_PRINCIPAL + constantes.ESPACIADO_Y_POR_PALABRA

    palabras = []

    for palabra in constantes.NOMBRE_JUEGO.split():

        # Crear un objeto Texto con los parámetros necesarios
        palabras.append(Texto(palabra, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TITULO_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA, None, posicion_y, constantes.TEXTO_CENTRADO))

        # Aumenta la posición Y para la siguiente palabra
        posicion_y += espaciado

    return palabras

# =========================================== Eventos ===========================================

def manejar_eventos(botones):
    """
    Maneja los eventos del menú, la interacción con los botones y 
    el cierre de la ventana.
    Args: botones (list[Boton]): Lista de botones a revisar por clics.
    Returns: str: Retorna la acción seleccionada ('jugar', 'salir') o None si no hubo acción.
    """
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return constantes.ACCION_SALIR
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for boton in botones:
                if boton.es_presionado():
                    return boton.accion

    # Cambia el cursor según la posición del ratón sobre los botones
    utilidades.verificar_cambio_icono_cursor(botones)

    return None

# =========================================== Función Principal ===========================================

def mostrar_pantalla_inicio(estado_juego):
    """
    Muestra la pantalla de inicio del juego, incluyendo el fondo animado, 
    el título y los botones de 'Jugar' y 'Salir'.
    
    Returns:
        str: La acción seleccionada ('jugar' o 'salir').
    """
    boton_jugar, boton_salir = crear_botones()

    palabras_nombre_juego = crear_palabras_nombre_juego()

    # Establecer el cursor predeterminado al inicio
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:

        # Actualiza y dibuja el fondo animado
        estado_juego.fondo_animado.actualizar()
        estado_juego.fondo_animado.dibujar_fondo()

        # Muestra el nombre del juego palabra por palabra
        for palabra in palabras_nombre_juego:
            palabra.dibujar()

        # Dibuja los botones de 'Jugar' y 'Salir'
        boton_jugar.dibujar()
        boton_salir.dibujar()

        # Actualiza la pantalla
        pygame.display.flip()

        # Maneja los eventos (clic en botones, cierre de ventana, etc.)
        accion = manejar_eventos([boton_jugar, boton_salir])

        # Si el jugador selecciona 'Jugar' o 'Salir', retorna la acción
        if accion in [constantes.ACCION_JUGAR, constantes.ACCION_SALIR]:
            estado_juego.accion = accion
            return
