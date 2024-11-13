import copy
import pygame
import random
import socket
import menus
import clases
import sys
import os

from menus.menu_principal import mostrar_pantalla_inicio
from menus.menu_seleccionar_personaje import menu_selector
from menus.menu_ganador import mostrar_pantalla_ganador, manejar_eventos, mostrar_pantalla_perdedor
from menus.menu_batalla import iniciar_batalla, obtener_imagen_fondo_aleatoria, crear_elementos_hud, actualizar_display_salud, mostrar_mensaje
from menus.menu_salida import confirmar_salida

from clases.fondo_animado import FondoAnimado
from clases.estado_juego import EstadoJuego

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import contexto_juego
from Compartido import constantes
from Compartido import personaje

socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_cliente.connect(("127.0.0.1", 5000))

CLAVES = {
    "INDICE_PERSONAJE_ELEGIDO": "INDICE_PERSONAJE_ELEGIDO",
    "INDICE_PERSONAJE_ENEMIGO": "INDICE_PERSONAJE_ENEMIGO",
    "ACCION_BATALLA": "ACCION_BATALLA",
    "TURNO_JUGADOR": "TURNO_JUGADOR",
    "INDICE_JUGADOR": "INDICE_JUGADOR",
    "ACTUALIZACION_VIDA": "ACTUALIACION_VIDA"
}

pygame.init()
pygame.mixer.init()
ventana = contexto_juego.obtener_ventana()

accion_actual = ""
turno = ""

def obtener_personaje_enemigo(indice_enemigo):
    personaje = contexto_juego.obtener_personajes()[indice_enemigo]
    copia_personaje = copy.deepcopy(personaje)
    return copia_personaje

def enviar_datos_servidor(dato):
    socket_cliente.send(f"{CLAVES['ACCION_BATALLA']}:{dato}".encode())
    socket_cliente.recv(1024).decode()

    
def recibir_datos_servidor():
    return socket_cliente.recv(1024).decode()


def bucle_juego(estado_juego):
    global accion_actual, turno

    menu_selector(estado_juego)
    if estado_juego.accion == constantes.ACCION_SALIR_JUEGO:
        return estado_juego.accion

    indice = estado_juego.indice_personaje_elegido
    print(f"Indice: {indice}")
    socket_cliente.send(f"{CLAVES['INDICE_PERSONAJE_ELEGIDO']}:{indice}".encode())
    socket_cliente.recv(1024)  

    id_cliente = socket_cliente.recv(1024).decode().split(":")[1]
    socket_cliente.send("ACK".encode())
    print(f"ID Aliado: {id_cliente}")

    id_enemigo = socket_cliente.recv(1024).decode().split(":")[1]
    socket_cliente.send("ACK".encode())
    print(f"ID Enemigo: {id_enemigo}")

    id_personaje = socket_cliente.recv(1024).decode().split(":")[1]
    socket_cliente.send("ACK".encode())
    print(f"Personaje propio: {id_personaje}")

    id_personaje_enemigo = socket_cliente.recv(1024).decode().split(":")[1]
    socket_cliente.send("ACK".encode())
    print(f"Personaje enemigo: {id_personaje_enemigo}")

    estado_juego.personaje_enemigo = obtener_personaje_enemigo(int(id_personaje_enemigo))

    turno = socket_cliente.recv(1024).decode().split(":")[1]
    socket_cliente.send("ACK".encode())

    print(f"Turno: {turno}")

    estado_juego.imagen_de_fondo = obtener_imagen_fondo_aleatoria()

    while True:

        accion = iniciar_batalla(estado_juego, turno)
        
        if turno == "True":
            
            print(f"Acción seleccionada: {accion}")
            socket_cliente.send(accion.encode())
            socket_cliente.recv(1024).decode()
       
        if estado_juego.accion == constantes.ACCION_SALIR_JUEGO:
            return estado_juego.accion
        
        elif estado_juego.accion == constantes.ACCION_GANADOR and estado_juego.ganador is not None:
            mostrar_pantalla_ganador(estado_juego) 
            accion = estado_juego.accion

            if accion == constantes.ACCION_SALIR_JUEGO:
                return accion
            
            elif accion == constantes.ACCION_JUGAR:
                estado_juego.reiniciar_personaje()
                continue

        resultado = socket_cliente.recv(1024).decode()
        socket_cliente.send("ACK".encode())

        print(f"Resultado: {resultado}  -- {str(resultado)}")

        id_cliente_recibido = resultado.split(":")[1]
        vida_cliente_recibido = resultado.split(":")[2]
        id_enemigo_recibido = resultado.split(":")[3]
        vida_enemigo_recibido = resultado.split(":")[4]
        accion_actual = resultado.split(":")[5]

        print("Acción: " + str(accion_actual))
        
        if id_cliente == id_cliente_recibido:
            estado_juego.personaje_seleccionado.vida = int(float(vida_cliente_recibido))
            estado_juego.personaje_enemigo.vida = int(float(vida_enemigo_recibido))
        else:
            estado_juego.personaje_seleccionado.vida = int(float(vida_enemigo_recibido))
            estado_juego.personaje_enemigo.vida = int(float(vida_cliente_recibido))

        if turno != "True":
            mostrar_mensaje(accion_actual)

        condition_current_character, condition_enemy_character = crear_elementos_hud(estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)
        actualizar_display_salud(condition_current_character, condition_enemy_character, estado_juego.personaje_seleccionado, estado_juego.personaje_enemigo)
        pygame.display.update()

        if int(estado_juego.personaje_seleccionado.vida) <= 0:
            estado_juego.ganador = estado_juego.personaje_enemigo
            estado_juego.perdedor = estado_juego.personaje_seleccionado
            mostrar_pantalla_perdedor(estado_juego)
            break   

        if int(estado_juego.personaje_enemigo.vida) <= 0:
            estado_juego.ganador = estado_juego.personaje_seleccionado
            estado_juego.perdedor = estado_juego.personaje_enemigo
            mostrar_pantalla_ganador(estado_juego)
            break 
        
        turno = socket_cliente.recv(1024).decode()
        print(str(turno))
        turno = turno.split(":")[1]
        socket_cliente.send("ACK".encode())
        print(f"Turno: {turno}")

    if estado_juego.accion == constantes.ACCION_SALIR_JUEGO:
        return

    salida = manejar_eventos(estado_juego)
    while salida == None:
        salida = manejar_eventos(estado_juego)
    
    print(f"Salida: {str(salida)}")
    if str(salida) == str(constantes.ACCION_JUGAR):
        socket_cliente.send("PLAY".encode())
        socket_cliente.recv(1024).decode()
        estado_juego.reiniciar_personajes()
        estado_juego = None
        main()

    else:
        socket_cliente.send("QUIT".encode())
        socket_cliente.recv(1024).decode()
        socket_cliente.close()

def main():

    estado_juego = EstadoJuego()
    
    print(str(constantes.RUTA_FONDO_ANIMADO))
    print(str(constantes.NOMBRE_BASE_IMAGEN_FONDO))
    print(str(constantes.DELAY_FUERA_CUADRO))

    estado_juego.fondo_animado = FondoAnimado(
        constantes.RUTA_FONDO_ANIMADO,
        constantes.NOMBRE_BASE_IMAGEN_FONDO,
        constantes.DELAY_FUERA_CUADRO
    )

    mostrar_pantalla_inicio(estado_juego)
    pygame.mixer.music.load("Musica/music.mp3")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)

    while True:

        if estado_juego.accion == constantes.ACCION_JUGAR:
            bucle_juego(estado_juego)

        if estado_juego.accion == constantes.ACCION_SALIR:
            confirmar_salida(estado_juego)
            
        if estado_juego.accion == constantes.ACCION_SALIR_JUEGO:
            break
        else:
            mostrar_pantalla_inicio(estado_juego)

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
