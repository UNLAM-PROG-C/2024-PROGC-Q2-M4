import pygame
import utilidades 
from clases.fondo_animado import FondoAnimado
from clases.boton import Boton 
from clases.texto import Texto 

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego

ventana = contexto_juego.obtener_ventana()

def crear_botones():
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
    posicion_y = constantes.POSICION_Y_TITULO_MENU_PRINCIPAL
    
    espaciado = constantes.TAMANO_FUENTE_TITULO_MENU_PRINCIPAL + constantes.ESPACIADO_Y_POR_PALABRA

    palabras = []

    for palabra in constantes.NOMBRE_JUEGO.split():
        palabras.append(Texto(palabra, constantes.FUENTE_JUEGO, constantes.TAMANO_FUENTE_TITULO_MENU_PRINCIPAL, constantes.COLOR_BLANCO_TUPLA, None, posicion_y, constantes.TEXTO_CENTRADO))

        posicion_y += espaciado

    return palabras

def manejar_eventos(botones):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return constantes.ACCION_SALIR
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for boton in botones:
                if boton.es_presionado():
                    return boton.accion

    utilidades.verificar_cambio_icono_cursor(botones)

    return None

def mostrar_pantalla_inicio(estado_juego):
    boton_jugar, boton_salir = crear_botones()

    palabras_nombre_juego = crear_palabras_nombre_juego()

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:

        estado_juego.fondo_animado.actualizar()
        estado_juego.fondo_animado.dibujar_fondo()

        for palabra in palabras_nombre_juego:
            palabra.dibujar()

        boton_jugar.dibujar()
        boton_salir.dibujar()

        pygame.display.flip()

        accion = manejar_eventos([boton_jugar, boton_salir])
        if accion in [constantes.ACCION_JUGAR, constantes.ACCION_SALIR]:
            estado_juego.accion = accion
            return
