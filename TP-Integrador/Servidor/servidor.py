import socket
import sys, os
import copy
import threading
from time import sleep

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Compartido import contexto_juego
from Compartido import constantes
from Compartido import personaje

MI_TURNO = 0
TURNO_ENEMIGO = 1
CANTIDAD_DE_JUGADORES = 2
CLAVES = {
    "INDICE_PERSONAJE_ELEGIDO": "INDICE_PERSONAJE_ELEGIDO",
    "INDICE_PERSONAJE_ENEMIGO": "INDICE_PERSONAJE_ENEMIGO",
    "ACCION_BATALLA": "ACCION_BATALLA",
    "TURNO_JUGADOR": "TURNO_JUGADOR",
    "INDICE_JUGADOR": "INDICE_JUGADOR",
    "ACTUALIZACION_VIDA": "ACTUALIZACION_VIDA",
    "ID_CLIENTE": "ID_CLIENTE",
    "ID_ENEMIGO": "ID_ENEMIGO",
    "INDICE_PERSONAJE_JUGADOR": "INDICE_PERSONAJE_JUGADOR"
}

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind(("127.0.0.1", 5000))
socket_servidor.listen(CANTIDAD_DE_JUGADORES)

jugadores = []
indice_jugadores = []
turno_actual = 0
cantidad_conexiones = 0
jugando = True
accion_actual = ""

lock = threading.Lock()
barrera = threading.Barrier(CANTIDAD_DE_JUGADORES)

def manejador_cliente(conexion, direccion, id_cliente):
    global turno_actual, jugadores, indice_jugadores, cantidad_conexiones, jugando, accion_actual
    
    personajes = contexto_juego.obtener_personajes()

    while jugando:

        datos = conexion.recv(1024).decode().split(":")[1]

        conexion.send("ACK".encode()) 
        with lock:
            indice_jugadores.insert(id_cliente, int(datos))
            jugadores.insert(id_cliente, copy.deepcopy(personajes[int(datos)]))

        while len(jugadores) and len(indice_jugadores) < CANTIDAD_DE_JUGADORES:
            sleep(1)

        id_enemigo = 1 if id_cliente == 0 else 0

        print("ID Cliente: " + str(id_cliente))
        conexion.send(f"{CLAVES['ID_CLIENTE']}:{id_cliente}".encode())
        conexion.recv(1024)

        conexion.send(f"{CLAVES['ID_ENEMIGO']}:{id_enemigo}".encode())
        conexion.recv(1024) 

        conexion.send(f"{CLAVES['INDICE_PERSONAJE_JUGADOR']}:{indice_jugadores[id_cliente]}".encode())
        conexion.recv(1024) 
        
        conexion.send(f"{CLAVES['INDICE_PERSONAJE_ENEMIGO']}:{indice_jugadores[id_enemigo]}".encode())
        conexion.recv(1024)  

        with lock:
            if turno_actual == id_cliente:
                conexion.send(f"{CLAVES['TURNO_JUGADOR']}:{True}".encode())
            else:
                conexion.send(f"{CLAVES['TURNO_JUGADOR']}:{False}".encode())

        conexion.recv(1024) 

        try:
            while True:
                if turno_actual == id_cliente:
                    accion_actual = conexion.recv(1024).decode()
                    print("Accion batalla:" + str(accion_actual))
                    conexion.send("ACK".encode()) 
                    
                    id_enemigo = int(1 if id_cliente == 0 else 0)
                    
                    with lock:
                        match str(accion_actual):
                            case "Atacar":
                                ataque = jugadores[id_cliente].atacar()
                                jugadores[id_enemigo].recibir_dano(ataque)
                            case "Defender":
                                jugadores[id_cliente].defender()
                            case "Descansar":
                                jugadores[id_cliente].descansar()
                            case _:
                                jugadores[id_cliente].concentrarse()

                        vida_cliente = jugadores[id_cliente].vida
                        vida_enemigo = jugadores[id_enemigo].vida

                    conexion.send(f"{CLAVES['ACTUALIZACION_VIDA']}:{id_cliente}:{vida_cliente}:{id_enemigo}:{vida_enemigo}:{accion_actual}".encode())
                    conexion.recv(1024).decode() 

                    with lock:
                        turno_actual = 1 - turno_actual

                else:
                    while int(turno_actual) != int(id_cliente):
                        sleep(0.1)

                    with lock:
                        vida_cliente = jugadores[id_cliente].vida
                        vida_enemigo = jugadores[id_enemigo].vida

                    conexion.send(f"{CLAVES['ACTUALIZACION_VIDA']}:{id_cliente}:{vida_cliente}:{id_enemigo}:{vida_enemigo}:{accion_actual}".encode())
                    conexion.recv(1024).decode()  
            
                if int(jugadores[id_cliente].vida) <= 0 or int(jugadores[id_enemigo].vida) <= 0:
                    break
    
                barrera.wait()

                with lock:
                    if int(turno_actual) == int(id_cliente):
                        conexion.send(f"{CLAVES['TURNO_JUGADOR']}:{True}".encode())
                    else:
                        conexion.send(f"{CLAVES['TURNO_JUGADOR']}:{False}".encode()) 
                
                conexion.recv(1024) 
            
            respuesta = conexion.recv(1024).decode()
            conexion.send("ACK".encode())

            print(respuesta) 

            if(str(respuesta) == "PLAY"):
                jugando = True
                barrera.wait()
                with lock:
                    jugadores.clear()

                with lock:
                    indice_jugadores.clear()
            else:
                jugando = False
        except Exception as e:
            print("Error" + str(e))
      
    with lock:
        jugadores.pop(id_cliente)
        cantidad_conexiones -= 1
    conexion.close()
    

def iniciar_servidor():
    print("Servidor esperando conexiones...")
    global cantidad_conexiones
    while True:
        lock.acquire()
        if cantidad_conexiones < CANTIDAD_DE_JUGADORES:
            lock.release()
            conexion, direccion = socket_servidor.accept()
            threading.Thread(target=manejador_cliente, args=(conexion, direccion, cantidad_conexiones)).start()
            with lock:
                cantidad_conexiones += 1
        else:
            lock.release()
            conexion, _ = socket_servidor.accept() 
            conexion.close()

if __name__ == "__main__":
    iniciar_servidor()