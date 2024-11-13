import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import os
import pygame
import random
import threading
from time import sleep
import utilidades
from clases.boton import Boton
from clases.texto import Texto
from menus.menu_salida import confirmar_salida

bloqueo = threading.Lock()

TECLAS = {
    "INDICE_PERSONAJE_ELEGIDO": "INDICE_PERSONAJE_ELEGIDO",
    "INDICE_PERSONAJE_ENEMIGO": "INDICE_PERSONAJE_ENEMIGO",
    "ACCION_BATALLA": "ACCION_BATALLA",
    "TURNO_JUGADOR": "TURNO_JUGADOR",
    "INDICE_JUGADOR": "INDICE_JUGADOR",
    "ACTUALIZACION_VIDA": "ACTUALIACION_VIDA"
}

ventana = contexto_juego.obtener_ventana()
sprites = contexto_juego.obtener_sprites()

imagenes_fondo = [
    archivo for archivo in os.listdir(constantes.RUTA_FONDO)
    if archivo.endswith((constantes.EXTENSION_PNG, constantes.EXTENSION_JPG)) and "background" in archivo
]

def obtener_imagen_fondo_aleatoria():
    
    ruta_imagen_fondo = os.path.join(constantes.RUTA_FONDO, random.choice(imagenes_fondo))
    
    imagen_fondo = pygame.image.load(ruta_imagen_fondo)

    imagen_fondo = pygame.transform.scale(imagen_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    
    return imagen_fondo


def crear_boton_accion(accion, color, color_claro, posicion_x, posicion_y):
    texto_boton = Texto(
        accion,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_FUENTE_BOTONES_MENU_COMBATE,
        constantes.COLOR_BLANCO_TUPLA,
        posicion_x,
        posicion_y
    )

    return Boton(
        texto_boton,
        posicion_x,
        posicion_y,
        constantes.ANCHO_BOTON,
        constantes.ALTO_BOTON,
        color,
        color_claro,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.BORDES_BOTON_PX,
        constantes.COLOR_NEGRO_TUPLA,
        accion,
    )

def crear_botones_acciones():
    botones = []

    espaciado_dinamico = int(constantes.ANCHO_VENTANA * 0.05)  

    ancho_total_botones = constantes.ANCHO_BOTON * constantes.TOTAL_BOTONES
    ancho_total_espaciado = espaciado_dinamico * (constantes.TOTAL_BOTONES - 1)
    ancho_total = ancho_total_botones + ancho_total_espaciado

    inicio_x = (constantes.ANCHO_VENTANA - ancho_total) // 2

    posicion_y = constantes.ALTO_VENTANA - constantes.ALTO_BOTON - constantes.MARGEN_INFERIOR_BOTONES

    for i, accion in enumerate([constantes.ATACAR, constantes.DEFENDER, constantes.DESCANSAR, constantes.CONCENTRARSE]):

        posicion_x = inicio_x + i * (constantes.ANCHO_BOTON + espaciado_dinamico)
        
        color = constantes.COLORES_BOTONES[i]
        color_hover = constantes.COLORES_BOTONES_AL_PASAR_EL_RATON[i]
        
        botones.append(crear_boton_accion(accion, color, color_hover, posicion_x, posicion_y))

    return botones


def crear_texto_hud(personaje, posicion_y):
    posicion_x = int(constantes.ANCHO_VENTANA * 0.07) 
    return Texto(
        f"{personaje.nombre} HP: {personaje.vida}",
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_SALUD_PERSONAJES,
        constantes.COLOR_BLANCO_TUPLA,
        posicion_x,
        posicion_y
    )

def crear_elementos_hud(personaje_actual, personaje_enemigo):    
    posicion_y_personaje_actual = int(constantes.ANCHO_VENTANA * 0.05)  
    posicion_y_personaje_enemigo = posicion_y_personaje_actual + constantes.POSICION_Y_SALUD_PERSONAJE_ENEMIGO  
    
    condicion_personaje_actual = crear_texto_hud(personaje_actual, posicion_y_personaje_actual)
    condicion_personaje_enemigo = crear_texto_hud(personaje_enemigo, posicion_y_personaje_enemigo)
    
    return condicion_personaje_actual, condicion_personaje_enemigo

def actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, personaje_actual, personaje_enemigo):
    condicion_personaje_actual.actualizar_contenido(f"{personaje_actual.nombre} HP: {personaje_actual.vida}")
    condicion_personaje_enemigo.actualizar_contenido(f"{personaje_enemigo.nombre} HP: {personaje_enemigo.vida}")


def escalar_sprite(sprite):
    return pygame.transform.scale(sprite, (int(sprite.get_width() * constantes.FACTOR_ESCALA_SPRITE_COMBATE),
                                           int(sprite.get_height() * constantes.FACTOR_ESCALA_SPRITE_COMBATE)))

def dibujar_personajes(personaje_actual, personaje_enemigo):    
    x_personaje_actual = int(constantes.ANCHO_VENTANA * 0.15)  
    y_personaje_actual = int(constantes.ALTO_VENTANA * 0.4)  

    x_personaje_enemigo = int(constantes.ANCHO_VENTANA * 0.55) 
    y_personaje_enemigo = int(constantes.ALTO_VENTANA * 0.15) 

    sprite_personaje_actual = escalar_sprite(sprites[personaje_actual.nombre]["back"])
    sprite_personaje_enemigo = escalar_sprite(sprites[personaje_enemigo.nombre]["front"])

    ventana.blit(sprite_personaje_actual, (x_personaje_actual, y_personaje_actual))
    ventana.blit(sprite_personaje_enemigo, (x_personaje_enemigo, y_personaje_enemigo))

def dibujar_pantalla_batalla(condicion_personaje_actual, condicion_personaje_enemigo, botones_acciones, personaje_actual, personaje_enemigo, es_turno_jugador):    
    condicion_personaje_actual.dibujar()
    condicion_personaje_enemigo.dibujar()

    dibujar_personajes(personaje_actual, personaje_enemigo)
    
    if es_turno_jugador == "True":
        for boton in botones_acciones:
            boton.dibujar()
        utilidades.verificar_cambio_icono_cursor(botones_acciones)
    else:
        for boton in botones_acciones:
            boton.dibujar_gris()
    
    actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, personaje_actual, personaje_enemigo)
    pygame.display.update()


def iniciar_batalla(estado_juego, es_turno_jugador):
    
    botones_acciones = crear_botones_acciones()

    condicion_personaje_actual, condicion_personaje_enemigo = crear_elementos_hud(estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:

        ventana.blit(estado_juego.imagen_de_fondo, (0, 0))

        dibujar_pantalla_batalla(condicion_personaje_actual, condicion_personaje_enemigo, botones_acciones, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo, es_turno_jugador)

        actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)

        if es_turno_jugador == "True":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if confirmar_salida_batalla(estado_juego):
                        return

                elif evento.type == pygame.MOUSEBUTTONDOWN and es_turno_jugador:
                    for boton in botones_acciones:
                        if boton.es_presionado():
                            return boton.accion
                actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)
                pygame.display.update()
        else:
            actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)
            pygame.display.update()
            return

def confirmar_salida_batalla(estado_juego):
    confirmar_salida(estado_juego)

    return estado_juego.accion == constantes.ACCION_SALIR_JUEGO

def mostrar_mensaje(accion):    
    match str(accion):
        case "Atacar":
            mensaje = "El enemigo ha atacado!"
        case "Defender":
            mensaje = "El enemigo ha mejorado su defensa!"
        case "Descansar":
            mensaje = "El enemigo ha recuperado salud!"
        case _:
            mensaje = "El enemigo se ha concentrado para su proximo ataque!"
    
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
    
    pantalla_actual = ventana.copy()

    inicio_ticks = pygame.time.get_ticks()

    while pygame.time.get_ticks() - inicio_ticks < 1500:  

        ventana.blit(pantalla_actual, (0, 0))
        
        texto.dibujar()
        
        pygame.display.update()
        
        pygame.time.wait(100) 
    
    ventana.blit(pantalla_actual, (0, 0))
    pygame.display.update()
