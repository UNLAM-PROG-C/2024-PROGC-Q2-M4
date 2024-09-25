import sys
import threading
import time

CANTIDAD_MAXIMA_SOGA = 5
IZQUIERDA = 1
DERECHA = 2
TIEMPO_ESPERA = 1
TIEMPO_PARA_CRUZAR = 1

mutex_region_critica = threading.Lock()
mutex_cuerda = threading.Lock()

cantidad_babuinos = 0
lado_cuerda = 1

def cambiar_de_lado(direccion):
  global lado_cuerda, cantidad_babuinos,cantidad_babuinos_izquierda

  while True:
    if direccion == lado_cuerda:
      with mutex_region_critica:
        if cantidad_babuinos < CANTIDAD_MAXIMA_SOGA:
          cantidad_babuinos += 1
          print(f"Viajando hacia la {'derecha' if IZQUIERDA+direccion%DERECHA == 1 else 'izquierda'}, "
                f"cantidad de babuinos en cuerda: {cantidad_babuinos}")
          sys.stdout.flush()
        else:
          continue

      time.sleep(TIEMPO_PARA_CRUZAR)

      with mutex_region_critica:
        cantidad_babuinos -= 1
        print(f"babuino llegó a la {'derecha' if IZQUIERDA+direccion%DERECHA == 1 else 'izquierda'}, "
        f"cantidad de babuinos en cuerda: {cantidad_babuinos}")
        sys.stdout.flush()

        if cantidad_babuinos == 0:
          print("No hay más babuinos en la cuerda, se libera.")
          sys.stdout.flush()
        if (direccion == 1):
          cantidad_babuinos_izquierda-=1
        return
    else:
      if mutex_cuerda.acquire(blocking=False):
        while( cantidad_babuinos_izquierda > 0):
          time.sleep(TIEMPO_ESPERA)
        print("-------------------------------------------------------------------------------------")
        print(f"Cambiando la dirección de la cuerda hacia la derecha")
        print("-------------------------------------------------------------------------------------")
        sys.stdout.flush()
        lado_cuerda=direccion
        mutex_cuerda.release()


def main():
  global cantidad_babuinos_izquierda

  if len(sys.argv) < 2:
    sys.exit("Se debe indicar la cantidad de monos")
    sys.stdout.flush()
    return
  cantidad_babuinos_a_generar = int(sys.argv[1])
  if cantidad_babuinos_a_generar < 0:
    sys.exit("La cantidad de babuinos no puede ser negativa")
    sys.stdout.flush()

  threads = []
  cantidad_babuinos_izquierda=cantidad_babuinos_a_generar/2

  lado = IZQUIERDA
  for i in range(cantidad_babuinos_a_generar):
    babuino = threading.Thread(target=cambiar_de_lado, args=(lado,))
    threads.append(babuino)
    lado = IZQUIERDA + lado % DERECHA

  for thread in threads:
    thread.start()

  for thread in threads:
    thread.join()


if __name__ == "__main__":
  main()
