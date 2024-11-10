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

# =========================================== Sprites ===========================================

def obtener_sprite_ganador(sprites, personaje):
    """Obtiene el sprite del ganador y lo escala al tamaño deseado."""
    sprite_ganador = sprites.get(personaje.nombre)
    if sprite_ganador and FRONTAL in sprite_ganador:
        sprite_ganador = sprite_ganador[FRONTAL]
        return scale(sprite_ganador, (constantes.ANCHO_SPRITE_GANADOR, constantes.ALTO_SPRITE_GANADOR))
    else:
        return None

def obtener_posicion_centrada(ancho, alto):
    """Calcula la posición centrada para un ancho y alto dados en la ventana."""
    centro_x = (constantes.ANCHO_VENTANA - ancho) // 2
    centro_y = (constantes.ALTO_VENTANA - alto) // 2
    return centro_x, centro_y

def dibujar_sprite(sprite):
    """Dibuja el sprite centrado en la ventana, si el sprite existe."""
    if sprite:
        rect_sprite = sprite.get_rect()
        centro_x, centro_y = obtener_posicion_centrada(rect_sprite.width, rect_sprite.height)
        ventana.blit(sprite, (centro_x, centro_y))

# =========================================== Eventos ===========================================

def manejar_eventos():
    """Maneja los eventos de la ventana y retorna una acción."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            resultado = confirmar_salida()
            if resultado == constantes.ACCION_CONFIRMAR or resultado == constantes.ACCION_SALIR:
                return constantes.ACCION_SALIR
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
            return constantes.ACCION_JUGAR  # Retorna acción de jugar si el usuario presiona Enter
    return None  # Acción por defecto si no ocurre nada

# =========================================== Función Principal ===========================================

def mostrar_pantalla_ganador(estado_juego):
    """Muestra la pantalla del ganador y espera que el usuario presione Enter para continuar."""
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
        # Actualización de pantalla optimizada
        pygame.display.flip()
        accion = manejar_eventos()  # Llama a la función de eventos y revisa la acción retornada
        if accion:
            estado_juego.accion = accion
            return  # Finaliza el bucle y retorna la acción a game_loop

def mostrar_pantalla_perdedor(estado_juego):
    """Muestra la pantalla del perdedor y espera que el usuario presione Enter para continuar."""
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
        # Actualización de pantalla optimizada
        pygame.display.flip()
        accion = manejar_eventos()  # Llama a la función de eventos y revisa la acción retornada
        if accion:
            estado_juego.accion = accion
            return  # Finaliza el bucle y retorna la acción a game_loop

import pygame

# Asumiendo que tienes un método de Texto y ventana como en tu código

def mostrar_mensaje(estado_juego, accion):    
    match str(accion):
        case "Atacar":
            mensaje = "¡El enemigo ha atacado!"
        case "Defender":
            mensaje = "¡El enemigo ha mejorado su defensa!"
        case "Descansar":
            mensaje = "¡El enemigo ha recuperado salud!"
        case _:
            mensaje = "¡El enemigo se ha concentrado para su próximo ataque!"
    
    mensaje_accion = str(mensaje)
    
    texto = Texto(
        mensaje_accion,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_TITULO_PERSONAJE_GANADOR,
        constantes.COLOR_BLANCO_TUPLA,
        constantes.POSICION_X_TITULO_PERSONAJE_GANADOR,
        constantes.POSICION_Y_MENSAJE_PERSONAJE_GANADOR-200,
        constantes.TEXTO_CENTRADO
    )
    
    # Guardar el estado de la pantalla actual
    pantalla_actual = ventana.copy()

    # Tiempo inicial cuando se muestra el mensaje
    inicio_ticks = pygame.time.get_ticks()

    # Mostrar el mensaje y la ventana actualizada
    while pygame.time.get_ticks() - inicio_ticks < 1500:  
        # 1500 milisegundos = 1.5 segundos
        # Dibujar la pantalla anterior (sin el mensaje)
        ventana.blit(pantalla_actual, (0, 0))
        
        # Dibuja el texto del mensaje
        texto.dibujar()
        
        # Actualiza la pantalla
        pygame.display.update()
        
        # Mantén la ventana activa
        pygame.time.wait(100)  # Pausa pequeña para evitar uso excesivo de CPU
    
    # Después de 3 segundos, restaurar la pantalla original (sin el mensaje)
    ventana.blit(pantalla_actual, (0, 0))
    pygame.display.update()