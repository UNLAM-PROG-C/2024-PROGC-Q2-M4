import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame
import utilidades
import clases
from clases.texto import Texto
from clases.boton import Boton
from clases.fondo_animado import FondoAnimado

ventana = contexto_juego.obtener_ventana()

def crear_botones():
    texto_confirmar = Texto(constantes.ACEPTAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TEXTO_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)
    texto_cancelar = Texto(constantes.CANCELAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TEXTO_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)

    boton_confirmar = Boton(
        texto_confirmar,
        constantes.POSICION_X_BOTONES_MENU_PRINCIPAL,
        constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL,
        constantes.ANCHO_BOTONES_MENU_PRINCIPAL,
        constantes.ALTO_BOTONES_MENU_PRINCIPAL,
        constantes.COLOR_NARANJA_TUPLA,
        constantes.COLOR_NARANJA_CLARO_TUPLA,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.BORDES_BOTON_PX,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.ACCION_SALIR_JUEGO
    )

    texto_cancelar = Texto(constantes.CANCELAR, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TEXTO_BOTONES_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA)
    
    boton_cancelar = Boton(
        texto_cancelar,
        constantes.POSICION_X_BOTONES_MENU_PRINCIPAL,
        constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL,
        constantes.ANCHO_BOTONES_MENU_PRINCIPAL,
        constantes.ALTO_BOTONES_MENU_PRINCIPAL,
        constantes.COLOR_VIOLETA_TUPLA,
        constantes.COLOR_VIOLETA_CLARO_TUPLA,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.BORDES_BOTON_PX,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.ACCION_CANCELAR
    )

    utilidades.posicionar_botones([boton_confirmar, boton_cancelar], constantes.ESPACIADO_BOTONES_MENU_PRINCIPAL, constantes.POSICION_Y_BOTONES_MENU_PRINCIPAL)

    return (boton_confirmar, boton_cancelar)

def dibujar_elementos(fondo_animado, texto_confirmar_salida, botones):
    fondo_animado.dibujar_fondo()
    texto_confirmar_salida.dibujar()
    for boton in botones:
        boton.dibujar()

def manejar_eventos(botones):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return constantes.ACCION_SALIR_JUEGO
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for boton in botones:
                if boton.es_presionado():
                    return boton.accion
    utilidades.verificar_cambio_icono_cursor(botones)
    return None 

def confirmar_salida(estado_juego):
    if not estado_juego.fondo_animado:
        estado_juego.fondo_animado = FondoAnimado(
            constantes.RUTA_FONDO_ANIMADO,
            constantes.NOMBRE_BASE_FRAME,
            constantes.RETRASO_FRAME
        )
    
    texto_confirmar_salida = Texto(
        constantes.MENSAJE_CONFIRMAR_SALIR,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_FUENTE_TITULO_CONFIRMAR_SALIR,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_TITULO_CONFIRMAR_SALIR,
        constantes.POSICION_Y_TITULO_CONFIRMAR_SALIR,
        constantes.TEXTO_CENTRADO
    )

    (boton_confirmar, boton_cancelar) = crear_botones()

    while True:
        estado_juego.fondo_animado.actualizar()
        dibujar_elementos(estado_juego.fondo_animado, texto_confirmar_salida, [boton_confirmar, boton_cancelar])
        pygame.display.flip()
        accion = manejar_eventos([boton_confirmar, boton_cancelar])
        if accion in [constantes.ACCION_CANCELAR, constantes.ACCION_SALIR_JUEGO]:
            estado_juego.accion = accion
            return
