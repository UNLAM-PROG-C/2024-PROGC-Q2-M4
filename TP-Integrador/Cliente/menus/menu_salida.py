import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame
import utilidades
import clases

from clases.fondo_animado import FondoAnimado

ventana = contexto_juego.obtener_ventana()

# ===============================

# Crea los botones de confirmación y cancelación para la ventana de salida
def crear_botones():
    # Crear los textos para los botones
    texto_confirmar = Texto(constantes.ACEPTAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)
    texto_cancelar = Texto(constantes.CANCELAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)

    boton_confirmar = Boton(
        texto_confirmar,
        constantes.POSICION_X_BOTONES_MENU_PRINCIPAL,
        constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL,
        constantes.ANCHO_BOTONES_MENU_PRINCIPAL,
        constantes.ALTO_BOTONES_MENU_PRINCIPAL,
        constantes.COLOR_NARANJA_TUPLA,
        constantes.COLOR_NARANJA_CLARO_TUPLA,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.PIXELES_BORDE_BOTON,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.ACCION_SALIR
    )

    texto_cancelar = Texto(constantes.CANCELAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)
    
    boton_cancelar = Boton(
        texto_cancelar,
        constantes.POSICION_X_BOTONES_MENU_PRINCIPAL,
        constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL,
        constantes.ANCHO_BOTONES_MENU_PRINCIPAL,
        constantes.ALTO_BOTONES_MENU_PRINCIPAL,
        constantes.COLOR_VIOLETA_TUPLA,
        constantes.COLOR_VIOLETA_CLARO_TUPLA,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.PIXELES_BORDE_BOTON,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.ACCION_CANCELAR
    )

    # Posicionar los botones en la pantalla

# Dibuja todos los elementos en pantalla
def dibujar_elementos(fondo_animado, texto_confirmar_salida, botones):
    fondo_animado.dibujar_fondo()
    texto_confirmar_salida.dibujar()
    for boton in botones:
        boton.dibujar()

# Maneja los eventos de la ventana de confirmación
def manejar_eventos(botones):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return constantes.ACCION_SALIR
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for boton in botones:
                if boton.es_presionado():
                    return boton.accion
    utilidades.verificar_cambio_icono_cursor(botones)
    return None  # Indica que no se ha tomado ninguna acción


# ==================================

# Función para confirmar salida
def confirmar_salida(estado_juego):
    if not estado_juego.fondo_animado:
        estado_juego.fondo_animado = FondoAnimado(
            constantes.RUTA_FONDO_ANIMADO,
            constantes.NOMBRE_BASE_FRAME,
            constantes.RETRASO_FRAME
        )
    
    texto_confirmar_salida = Texto(
        constantes.MENSAJE_CONFIRMAR_SALIDA,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_FUENTE_TITULO_CONFIRMAR_SALIDA,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_TITULO_CONFIRMAR_SALIDA,
        constantes.POSICION_Y_TITULO_CONFIRMAR_SALIDA,
        constantes.TEXTO_CENTRADO
    )

    while True:
        estado_juego.fondo_animado.actualizar()
        dibujar_elementos(estado_juego.fondo_animado, texto_confirmar_salida, [boton_confirmar, boton_cancelar])
        pygame.display.flip()
        accion = manejar_eventos([boton_confirmar, boton_cancelar])
        if accion in [constantes.ACCION_CANCELAR, constantes.ACCION_SALIR]:
            estado_juego.accion = accion
            return
