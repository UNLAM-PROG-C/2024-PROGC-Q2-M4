import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import copy
import pygame
from menus.menu_salida import confirmar_salida
from clases.texto import Texto

imagen_fondo = pygame.image.load(constantes.RUTA_FONDO + "background_waterfalls" + constantes.EXTENSION_JPG)
imagen_fondo = pygame.transform.scale(imagen_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
personajes = contexto_juego.obtener_personajes()
seleccion_actual = 0 
primer_indice_visible = 0 
ventana = contexto_juego.obtener_ventana()


def cargar_lista_personajes(sprites):
    centro_x_menu_personajes = constantes.ANCHO_VENTANA // 2 - constantes.POSICION_X_MENU_PERSONAJES
    
    base_posicion_y_menu_personajes = constantes.ALTO_VENTANA // 2 - (constantes.CANTIDAD_PERSONAJES_VISIBLES * 100) // 2 + 50
    
    for i in range(primer_indice_visible, min(primer_indice_visible + constantes.CANTIDAD_PERSONAJES_VISIBLES, len(personajes))):
        
        personaje = personajes[i]
        
        posicion_y_menu_personajes = base_posicion_y_menu_personajes + (i - primer_indice_visible) * 100
        
        nombre_personaje = Texto(
            personaje.nombre,
            constantes.FUENTE_JUEGO,
            constantes.TAMANO_FUENTE_PERSONAJES,
            constantes.COLOR_NEGRO_TUPLA,
            centro_x_menu_personajes,
            posicion_y_menu_personajes,
        )
        
        nombre_personaje.dibujar()
        
        if seleccion_actual == i:
            rect_x = centro_x_menu_personajes - 20
            rect_y = posicion_y_menu_personajes - 10
            pygame.draw.rect(ventana, constantes.COLOR_NEGRO_TUPLA, (rect_x, rect_y, 300, 50), 2)

    personaje_seleccionado = personajes[seleccion_actual]
    imagen_a_dibujar = sprites[personaje_seleccionado.nombre]["front"]
    imagen_redimensionada = pygame.transform.scale(imagen_a_dibujar, (constantes.TAMANO_X_PERSONAJE_SELECCIONADO, constantes.TAMANO_Y_PERSONAJE_SELECCIONADO))

    sprite_x = constantes.ANCHO_VENTANA // 2 + constantes.POSICION_X_SPRITE_PERSONAJE_SELECCIONADO
    sprite_y = constantes.ALTO_VENTANA // 2 - constantes.TAMANO_Y_PERSONAJE_SELECCIONADO // 2
    ventana.blit(imagen_redimensionada, (sprite_x, sprite_y))

def actualizar_indice():
    """ Actualiza el índice del primer personaje visible basado en la selección actual. """
    global seleccion_actual, primer_indice_visible
    
    if seleccion_actual < primer_indice_visible:
        primer_indice_visible = seleccion_actual
    elif (seleccion_actual >= primer_indice_visible + constantes.CANTIDAD_PERSONAJES_VISIBLES):
        primer_indice_visible = (seleccion_actual - constantes.CANTIDAD_PERSONAJES_VISIBLES + 1)

def manejar_eventos(estado_juego):
    """ Maneja los eventos de teclado y salida, actualizando el estado del juego. """
    global seleccion_actual, primer_indice_visible

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            confirmar_salida(estado_juego)
            if estado_juego.accion == constantes.ACCION_SALIR_JUEGO:
                return 

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_UP):
                direccion = 1 if event.key == pygame.K_DOWN else -1
                seleccion_actual = (seleccion_actual + direccion) % constantes.NUMERO_DE_PERSONAJES

                actualizar_indice()

            elif event.key == pygame.K_RETURN:
                estado_juego.accion = constantes.ACCION_SELECCIONAR_PERSONAJE
                estado_juego.personaje_seleccionado = copy.deepcopy(personajes[seleccion_actual])
                estado_juego.indice_personaje_elegido = seleccion_actual
                return


def menu_selector(estado_juego):
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    texto_elige_tu_personaje = Texto(
        constantes.ELEGIR_TU_PERSONAJE,
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_FUENTE_TITULO_PERSONAJE,
        constantes.COLOR_NEGRO_TUPLA,
        constantes.POSICION_X_TITULO_SELECTOR_PERSONAJE,
        constantes.POSICION_Y_TITULO_SELECTOR_PERSONAJE,
        constantes.TEXTO_CENTRADO
    )

    ventana.fill(constantes.COLOR_BLANCO_TUPLA)

    while True:

        ventana.blit(imagen_fondo, (0, 0))
        
        texto_elige_tu_personaje.dibujar()
        
        cargar_lista_personajes(contexto_juego.obtener_sprites())

        manejar_eventos(estado_juego)

        if estado_juego.accion == constantes.ACCION_SALIR_JUEGO or estado_juego.accion == constantes.ACCION_SELECCIONAR_PERSONAJE:
            break

        pygame.display.update()
