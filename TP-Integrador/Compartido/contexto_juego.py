from . import constantes
import os
import pygame
import json
from .personaje import Personaje

# ===================================== Ventana =====================================

ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption(constantes.NOMBRE_JUEGO)

# ===================================== Personajes =====================================

def cargar_personajes_desde_json(carpeta_salida):
    personajes = []

    # Listar todos los archivos JSON en la carpeta de salida
    for nombre_archivo in os.listdir(carpeta_salida):
        if nombre_archivo.endswith(constantes.EXTENSION_JSON):
            ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

            # Leer el archivo JSON
            with open(ruta_archivo, "r") as archivo:
                datos_personaje = json.load(archivo)

                # Extraer la información necesaria
                nombre = datos_personaje["name"]
                salud = datos_personaje["hp"]
                ataque = datos_personaje["attack"]
                defensa = datos_personaje["defense"]
                ruta_sprite_frontal = datos_personaje["front_sprite_path"]
                ruta_sprite_trasero = datos_personaje["back_sprite_path"]

                # Crear una lista de sprites
                sprites = {
                    "front_default": ruta_sprite_frontal,
                    "back_default": ruta_sprite_trasero
                }

                # Instanciar el objeto Personaje
                personaje = Personaje(nombre, salud, ataque, defensa, sprites)

                # Agregar el objeto a la lista
                personajes.append(personaje)
    
    return personajes

#personajes = cargar_personajes_desde_json(constantes.RUTA_PERSONAJES)
personajes = cargar_personajes_desde_json(os.path.join(os.path.dirname(__file__), 'characters'))

# ===================================== Gets =====================================

def obtener_ventana():
    return ventana

def obtener_sprites():
    personajes = obtener_personajes()
    sprites = {}

    for personaje in personajes:
        # Cargar los sprites desde el sistema de archivos
        ruta_sprite_frontal = personaje.sprites["front_default"]  # Ruta del sprite frontal
        ruta_sprite_trasero = personaje.sprites["back_default"]  # Ruta del sprite trasero

        # Cargar las imágenes con pygame
        sprite_frontal = pygame.image.load(ruta_sprite_frontal).convert_alpha()
        sprite_trasero = pygame.image.load(ruta_sprite_trasero).convert_alpha()

        # Almacenar las imágenes cargadas en el diccionario
        sprites[personaje.nombre] = {"front": sprite_frontal, "back": sprite_trasero}

    return sprites

def obtener_personajes():
    return personajes