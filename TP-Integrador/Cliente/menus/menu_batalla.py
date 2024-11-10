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

# ===================================== Variables =====================================

ventana = contexto_juego.obtener_ventana()
sprites = contexto_juego.obtener_sprites()

# Cargar imágenes de fondo aleatoriamente
imagenes_fondo = [
    archivo for archivo in os.listdir(constantes.RUTA_FONDO)
    if archivo.endswith((constantes.EXTENSION_PNG, constantes.EXTENSION_JPG)) and "background" in archivo
]

# ===================================== Fondo =====================================

def obtener_imagen_fondo_aleatoria():
    """Selecciona, carga y escala una imagen de fondo aleatoriamente."""
    
    # Selecciona una imagen aleatoriamente
    ruta_imagen_fondo = os.path.join(constantes.RUTA_FONDO, random.choice(imagenes_fondo))
    
    imagen_fondo = pygame.image.load(ruta_imagen_fondo)
    
    # Escalar la imagen de fondo a las dimensiones de la ventana
    imagen_fondo = pygame.transform.scale(imagen_fondo, (constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
    
    return imagen_fondo

# ===================================== Botones =====================================

def crear_boton_accion(accion, color, color_claro, posicion_x, posicion_y):
    """Crea un botón de acción para la interfaz de batalla."""
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
    """Crea los botones de acciones (Atacar, Defender, etc.) con colores y posiciones."""
    botones = []

    # Define un espaciado dinámico en función del ancho de la ventana
    espaciado_dinamico = int(constantes.ANCHO_VENTANA * 0.05)  # Por ejemplo, 2% del ancho de la ventana

    # Cálculo del ancho total necesario para todos los botones y el espaciado entre ellos
    ancho_total_botones = constantes.ANCHO_BOTON * constantes.TOTAL_BOTONES
    ancho_total_espaciado = espaciado_dinamico * (constantes.TOTAL_BOTONES - 1)
    ancho_total = ancho_total_botones + ancho_total_espaciado

    # Calcula `inicio_x` para centrar el conjunto de botones en la ventana
    inicio_x = (constantes.ANCHO_VENTANA - ancho_total) // 2

    # Posición Y fija para la fila de botones en la parte inferior de la ventana
    posicion_y = constantes.ALTO_VENTANA - constantes.ALTO_BOTON - constantes.MARGEN_INFERIOR_BOTONES

    for i, accion in enumerate([constantes.ATACAR, constantes.DEFENDER, constantes.DESCANSAR, constantes.CONCENTRARSE]):
        # Calcula la posición x de cada botón
        posicion_x = inicio_x + i * (constantes.ANCHO_BOTON + espaciado_dinamico)
        
        # Obtiene colores de la lista de constantes
        color = constantes.COLORES_BOTONES[i]
        color_hover = constantes.COLORES_BOTONES_AL_PASAR_EL_RATON[i]
        
        # Crea el botón de acción y lo agrega a la lista de botones
        botones.append(crear_boton_accion(accion, color, color_hover, posicion_x, posicion_y))

    return botones

# ===================================== HP =====================================

def crear_texto_hud(personaje, posicion_y):
    """Crea un elemento de texto para el HUD de un personaje."""
    posicion_x = int(constantes.ANCHO_VENTANA * 0.07) # 7% del ancho de la ventana
    return Texto(
        f"{personaje.nombre} HP: {personaje.vida}",
        constantes.FUENTE_JUEGO,
        constantes.TAMANO_SALUD_PERSONAJES,
        constantes.COLOR_BLANCO_TUPLA,
        posicion_x,
        posicion_y
    )

def crear_elementos_hud(personaje_actual, personaje_enemigo):
    """Crea elementos HUD para mostrar el estado de salud de los personajes en la esquina superior izquierda."""
    
    # Posiciones Y ajustadas dinámicamente
    posicion_y_personaje_actual = int(constantes.ANCHO_VENTANA * 0.05)  # 5% del alto de la ventana desde la parte superior
    posicion_y_personaje_enemigo = posicion_y_personaje_actual + constantes.POSICION_Y_SALUD_PERSONAJE_ENEMIGO  # 70 píxeles más abajo
    
    # Creación de textos de HUD
    condicion_personaje_actual = crear_texto_hud(personaje_actual, posicion_y_personaje_actual)
    condicion_personaje_enemigo = crear_texto_hud(personaje_enemigo, posicion_y_personaje_enemigo)
    
    return condicion_personaje_actual, condicion_personaje_enemigo

def actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, personaje_actual, personaje_enemigo):
    """Actualiza el texto de HP de cada personaje en pantalla."""
    condicion_personaje_actual.actualizar_contenido(f"{personaje_actual.nombre} HP: {personaje_actual.vida}")
    condicion_personaje_enemigo.actualizar_contenido(f"{personaje_enemigo.nombre} HP: {personaje_enemigo.vida}")

# ===================================== Sprites =====================================

def escalar_sprite(sprite):
    """Escala un sprite según el factor de escala dado y devuelve el sprite escalado."""
    return pygame.transform.scale(sprite, (int(sprite.get_width() * constantes.FACTOR_ESCALA_SPRITE_COMBATE),
                                           int(sprite.get_height() * constantes.FACTOR_ESCALA_SPRITE_COMBATE)))

def dibujar_personajes(personaje_actual, personaje_enemigo):
    """Dibuja los personajes en pantalla con posiciones y tamaños ajustados dinámicamente."""
    
    # Posiciones calculadas en función de la ventana para mayor flexibilidad
    x_personaje_actual = int(constantes.ANCHO_VENTANA * 0.15)  # Coloca a la izquierda
    y_personaje_actual = int(constantes.ALTO_VENTANA * 0.4)  # Ajusta un poco arriba

    x_personaje_enemigo = int(constantes.ANCHO_VENTANA * 0.55)  # Coloca a la derecha
    y_personaje_enemigo = int(constantes.ALTO_VENTANA * 0.15)  # Ajusta un poco arriba

    # Escala los sprites una vez en lugar de hacerlo cada vez
    sprite_personaje_actual = escalar_sprite(sprites[personaje_actual.nombre]["back"])
    sprite_personaje_enemigo = escalar_sprite(sprites[personaje_enemigo.nombre]["front"])

    # Dibuja los sprites escalados en las posiciones deseadas
    ventana.blit(sprite_personaje_actual, (x_personaje_actual, y_personaje_actual))
    ventana.blit(sprite_personaje_enemigo, (x_personaje_enemigo, y_personaje_enemigo))

def dibujar_pantalla_batalla(condicion_personaje_actual, condicion_personaje_enemigo, botones_acciones, personaje_actual, personaje_enemigo, es_turno_jugador):
    """Dibuja los elementos visuales de la pantalla de batalla."""
    
    # Dibuja el HUD
    condicion_personaje_actual.dibujar()
    condicion_personaje_enemigo.dibujar()

    # Dibuja los personajes
    dibujar_personajes(personaje_actual, personaje_enemigo)
    
    # Dibuja botones de acción
    if es_turno_jugador == "True":
        for boton in botones_acciones:
            boton.dibujar()
        utilidades.verificar_cambio_icono_cursor(botones_acciones)
    else:
        for boton in botones_acciones:
            boton.dibujar_gris()
    
    actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, personaje_actual, personaje_enemigo)
    pygame.display.update()

# ===================================== Batalla =====================================

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
                            # es_turno_jugador = manejar_accion_jugador(boton, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo) == constantes.JUGADOR
                            return boton.accion
                actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)
                pygame.display.update()
        else:
            actualizar_display_salud(condicion_personaje_actual, condicion_personaje_enemigo, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)
            pygame.display.update()
            return

def mostrar_batalla(estado_juego, socket_cliente):

    estado_juego.imagen_fondo = obtener_imagen_fondo_aleatoria()

    condicion_personaje_actual, condicion_personaje_enemigo = crear_elementos_hud(estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    while True:

        # Dibuja la pantalla de batalla con el fondo fijo seleccionado
        ventana.blit(estado_juego.imagen_fondo, (0, 0))

        # Dibuja el HUD
        condicion_personaje_actual.dibujar()
        condicion_personaje_enemigo.dibujar()

        # Dibuja los personajes
        dibujar_personajes(personaje_actual, personaje_enemigo)

        pygame.display.update()

def confirmar_salida_batalla(estado_juego):
    """Muestra un menú de confirmación para salir durante la batalla."""
    confirmar_salida(estado_juego)  # Llama a la pantalla de confirmación de salida

    # Devuelve True si el usuario confirma la salida, de lo contrario False
    return estado_juego.accion == constantes.ACCION_SALIR
