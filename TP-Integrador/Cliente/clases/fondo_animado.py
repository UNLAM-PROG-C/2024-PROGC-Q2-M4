import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes
from Compartido import contexto_juego
import pygame

class FondoAnimado:
    def __init__(self, ruta, nombre_base, retraso_frame):
        self.ventana = contexto_juego.obtener_ventana()
        self.frames = self.cargar_frames_animacion(ruta, nombre_base)
        self.frame_actual = 0
        self.contador_frame = 0
        self.retraso_frame = retraso_frame

    def actualizar(self):
        self.contador_frame += 1
        if self.contador_frame >= self.retraso_frame:
            self.frame_actual = (self.frame_actual + 1) % len(self.frames)
            self.contador_frame = 0
        return self.frames[self.frame_actual]

    def reiniciar(self):
        self.frame_actual = 0
        self.contador_frame = 0

    def cargar_frames_animacion(self, ruta_frames, nombre_base_frame):
        frames = []
        todos_los_archivos = os.listdir(ruta_frames)
        for nombre_archivo in todos_los_archivos:
            if nombre_archivo.startswith(nombre_base_frame) and nombre_archivo.endswith(constantes.EXTENSION_PNG):
                ruta_frame = os.path.join(ruta_frames, nombre_archivo)
                imagen_frame = pygame.image.load(ruta_frame)
                imagen_frame = pygame.transform.scale(imagen_frame, (self.ventana.get_width(), self.ventana.get_height()))
                frames.append(imagen_frame)
        return frames

    def dibujar_fondo(self):
        self.ventana.blit(self.frames[self.frame_actual], (0, 0))
