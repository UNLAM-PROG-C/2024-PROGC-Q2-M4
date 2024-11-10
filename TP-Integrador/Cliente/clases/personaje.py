import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import constantes

class Personaje:

    def __init__(self, nombre, vida, ataque, defensa, sprites=None):
        self.nombre = nombre
        self.vida = vida * constantes.MULTIPLICADOR_VIDA_INICIAL
        self.ataque = ataque
        self.defensa = defensa
        self.vida_maxima = vida * constantes.MULTIPLICADOR_VIDA_INICIAL
        self.multiplicador_defensa = 1.0  # Para controlar la defensa
        self.multiplicador_ataque_concentrado = 1.0  # Para controlar el ataque concentrado
        self.sprites = sprites  # Almacena las rutas locales de los sprites

    def defender(self):
        self.multiplicador_defensa = 0.5  # Reduce el daño a la mitad en el próximo ataque

    def descansar(self):
        # Recuperar el 20% de la salud actual
        recuperacion = int(self.vida_maxima * 0.2)
        if self.vida + recuperacion < self.vida_maxima:
            self.vida += recuperacion
        else:
            self.vida = self.vida_maxima

    def concentrarse(self):
        self.multiplicador_ataque_concentrado = 2.0  # Duplica el daño del próximo ataque

    def recibir_dano(self, dano):
        # Aplica la defensa si está activa
        dano *= self.multiplicador_defensa
        self.vida -= dano
        self.multiplicador_defensa = 1.0  # Reiniciar el multiplicador después de recibir daño
