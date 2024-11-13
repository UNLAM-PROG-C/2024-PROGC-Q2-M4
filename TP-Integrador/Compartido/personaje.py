from . import constantes

class Personaje:

    def __init__(self, nombre, vida, ataque, defensa, sprites=None):
        self.nombre = nombre
        self.vida = vida * constantes.MULTIPLICADOR_VIDA_INICIAL
        self.ataque = ataque
        self.defensa = defensa
        self.vida_maxima = vida * constantes.MULTIPLICADOR_VIDA_INICIAL
        self.multiplicador_defensa = 1.0
        self.multiplicador_ataque_concentrado = 1.0
        self.sprites = sprites

    def defender(self):
        self.multiplicador_defensa = 0.5

    def descansar(self):
        recuperacion = int(self.vida_maxima * 0.2)
        if self.vida + recuperacion < self.vida_maxima:
            self.vida += recuperacion
        else:
            self.vida = self.vida_maxima

    def concentrarse(self):
        self.multiplicador_ataque_concentrado = 2.5

    def recibir_dano(self, dano):
        dano *= self.multiplicador_defensa
        self.vida -= dano
        self.multiplicador_defensa = 1.0

    def atacar(self):
        daño = self.ataque * self.multiplicador_ataque_concentrado
        self.multiplicador_ataque_concentrado = 1.0
        return daño

