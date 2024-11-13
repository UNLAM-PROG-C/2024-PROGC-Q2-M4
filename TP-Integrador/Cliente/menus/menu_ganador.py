import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame
import utilidades
from clases.texto import Texto
from menus.menu_salida import confirmar_salida
from pygame.transform import scale

ventana = contexto_juego.obtener_ventana()

FRONTAL = 'front'

def obtener_sprite_ganador(sprites, personaje):
    sprite_ganador = sprites.get(personaje.nombre)
    if sprite_ganador and FRONTAL in sprite_ganador:
        sprite_ganador = sprite_ganador[FRONTAL]
        return scale(sprite_ganador, (constantes.ANCHO_SPRITE_GANADOR, constantes.ALTO_SPRITE_GANADOR))
    else:
        return None

def obtener_posicion_centrada(ancho, alto):
    centro_x = (constantes.ANCHO_VENTANA - ancho) // 2
    centro_y = (constantes.ALTO_VENTANA - alto) // 2
    return centro_x, centro_y

def dibujar_sprite(sprite):
    if sprite:
        rect_sprite = sprite.get_rect()
        centro_x, centro_y = obtener_posicion_centrada(rect_sprite.width, rect_sprite.height)
        ventana.blit(sprite, (centro_x, centro_y))

def manejar_eventos(estado_juego):
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            resultado = confirmar_salida(estado_juego)
            if resultado == constantes.ACCION_SALIR_JUEGO:
                return constantes.ACCION_SALIR_JUEGO
            elif resultado == constantes.ACCION_CANCELAR:
                return constantes.ACCION_CANCELAR
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            return constantes.ACCION_JUGAR 
    return None 

def mostrar_pantalla_ganador(estado_juego):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    titulo_personaje_ganador = f"{estado_juego.ganador.nombre} ha ganado!"
    
    texto_personaje_ganador = Texto(
        titulo_personaje_ganador,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_TITULO_PERSONAJE_GANADOR,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_TITULO_PERSONAJE_GANADOR,
        constantes.POSICION_Y_TITULO_PERSONAJE_GANADOR,
        constantes.TEXTO_CENTRADO
    )

    mensaje_ganador = Texto(
        constantes.MENSAJE_PERSONAJE_GANADOR,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_MENSAJE_PERSONAJE_GANADOR,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_MENSAJE_PERSONAJE_GANADOR,
        constantes.POSICION_Y_MENSAJE_PERSONAJE_GANADOR,
        constantes.TEXTO_CENTRADO
    )

    sprite_ganador = obtener_sprite_ganador(contexto_juego.obtener_sprites(), estado_juego.ganador)

    while True:
        ventana.blit(estado_juego.imagen_de_fondo, (0, 0))
        texto_personaje_ganador.dibujar()
        mensaje_ganador.dibujar()
        dibujar_sprite(sprite_ganador)
        pygame.display.flip()
        accion = manejar_eventos(estado_juego) 
        if accion:
            estado_juego.accion = accion
            return  

def mostrar_pantalla_perdedor(estado_juego):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    titulo_personaje_perdedor = f"{estado_juego.perdedor.nombre} ha perdido!"
    
    texto_personaje_perdedor = Texto(
        titulo_personaje_perdedor,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_TITULO_PERSONAJE_GANADOR,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_TITULO_PERSONAJE_GANADOR,
        constantes.POSICION_Y_TITULO_PERSONAJE_GANADOR,
        constantes.TEXTO_CENTRADO
    )

    mensaje_perdedor = Texto(
        constantes.MENSAJE_PERSONAJE_GANADOR,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_MENSAJE_PERSONAJE_GANADOR,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_MENSAJE_PERSONAJE_GANADOR,
        constantes.POSICION_Y_MENSAJE_PERSONAJE_GANADOR,
        constantes.TEXTO_CENTRADO
    )

    sprite_perdedor = obtener_sprite_ganador(contexto_juego.obtener_sprites(), estado_juego.perdedor)

    while True:
        ventana.blit(estado_juego.imagen_de_fondo, (0, 0))
        texto_personaje_perdedor.dibujar()
        mensaje_perdedor.dibujar()
        dibujar_sprite(sprite_perdedor)

        pygame.display.flip()
        accion = manejar_eventos(estado_juego)
        if accion:
            estado_juego.accion = accion
            return  
