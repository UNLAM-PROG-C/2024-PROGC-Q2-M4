class EstadoJuego:
    def __init__(
        self,
        accion=None,
        personaje_seleccionado=None,
        indice_personaje_elegido=None,
        personaje_enemigo=None,
        ganador=None,
        perdedor=None,
        imagen_de_fondo=None,
        fondo_animado=None
    ):
        self.accion = accion
        self.personaje_seleccionado = personaje_seleccionado
        self.indice_personaje_elegido = indice_personaje_elegido
        self.personaje_enemigo = personaje_enemigo
        self.ganador = ganador
        self.perdedor = perdedor
        self.imagen_de_fondo = imagen_de_fondo
        self.fondo_animado = fondo_animado

    def reiniciar_personajes(self):
        self.accion = None
        self.personaje_seleccionado = None
        self.indice_personaje_elegido = None
        self.personaje_enemigo = None
        self.ganador = None
        self.perdedor = None
        self.imagen_de_fondo = None
        self.fondo_animado = None
