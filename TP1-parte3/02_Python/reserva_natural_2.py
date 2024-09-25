import threading
import time
import random
import argparse

MINIMO_GRUPO_BABUINOS = 5
PROPORCION_GRUPO_BABUINOS = 4
MAX_BABUINOS_CUERDA = 5
TIEMPO_EN_CUERDA = 1

babuinos_este = 0
babuinos_oeste = 0
babuinos_esperando_este = 0
babuinos_esperando_oeste = 0
prioridad_direccion = 'ninguna'
babuinos_cruzaron_direccion_actual = 0
babuinos_total = 0
babuinos_contador = 0
babuinos_faltan_este = 0
babuinos_faltan_oeste = 0

semaforo_cuerda = threading.Semaphore(MAX_BABUINOS_CUERDA)

condicion_este = threading.Condition()
condicion_oeste = threading.Condition()

def entra_babuino_este():
  global babuinos_esperando_este, babuinos_este, babuinos_faltan_este
  global babuinos_cruzaron_direccion_actual, prioridad_direccion
  with condicion_este:
    babuinos_esperando_este += 1
    while no_puede_cruzar_este():
      condicion_este.wait()
    babuinos_esperando_este -= 1
    semaforo_cuerda.acquire()
    babuinos_este += 1
    prioridad_direccion = 'este'
    babuinos_cruzaron_direccion_actual += 1
    babuinos_faltan_este -= 1
    print(f"Babuino cruzando hacia el este. Total en cuerda: {MAX_BABUINOS_CUERDA - semaforo_cuerda._value}")
    print(f"Babuinos que faltan cruzar al este: {babuinos_faltan_este}")

def entra_babuino_oeste():
  global babuinos_esperando_oeste, babuinos_oeste, babuinos_faltan_oeste
  global babuinos_cruzaron_direccion_actual, prioridad_direccion
  with condicion_oeste:
    babuinos_esperando_oeste += 1
    while no_puede_cruzar_oeste():
      condicion_oeste.wait()
    babuinos_esperando_oeste -= 1
    semaforo_cuerda.acquire()
    babuinos_oeste += 1
    prioridad_direccion = 'oeste'
    babuinos_cruzaron_direccion_actual += 1
    babuinos_faltan_oeste -= 1
    print(f"Babuino cruzando hacia el oeste. Total en cuerda: {MAX_BABUINOS_CUERDA - semaforo_cuerda._value}")
    print(f"Babuinos que faltan cruzar al oeste: {babuinos_faltan_oeste}")

def no_puede_cruzar_este():
  if babuinos_faltan_oeste == 0:
    return (babuinos_oeste > 0 or semaforo_cuerda._value == 0 or
            (prioridad_direccion == 'oeste' and babuinos_oeste > 0))
  else:
    return (babuinos_oeste > 0 or semaforo_cuerda._value == 0 or
            (prioridad_direccion == 'oeste' and babuinos_oeste > 0) or
            (babuinos_cruzaron_direccion_actual >= max_babuinos_grupo and babuinos_esperando_oeste > 0))

def no_puede_cruzar_oeste():
  if babuinos_faltan_este == 0:
    return (babuinos_este > 0 or semaforo_cuerda._value == 0 or
            (prioridad_direccion == 'este' and babuinos_este > 0))
  else:
    return (babuinos_este > 0 or semaforo_cuerda._value == 0 or
            (prioridad_direccion == 'este' and babuinos_este > 0) or
            (babuinos_cruzaron_direccion_actual >= max_babuinos_grupo and babuinos_esperando_este > 0))

def sale_babuino_este():
  global babuinos_este, babuinos_contador
  with condicion_este:
    babuinos_este -= 1
    babuinos_contador += 1
    semaforo_cuerda.release()
    print(f"Babuino terminó de cruzar hacia el este. Total en cuerda: {MAX_BABUINOS_CUERDA - semaforo_cuerda._value}")

    if (MAX_BABUINOS_CUERDA - semaforo_cuerda._value) == 0 and babuinos_contador < babuinos_total:
      if babuinos_faltan_oeste > 0:
        print("------------------------------------------------------------------------------------->>>")
        print(f"Cambiando la dirección de la cuerda hacia el oeste")
        print(f"Babuinos que faltan cruzar al este: {babuinos_faltan_este}, al oeste: {babuinos_faltan_oeste}")
        print("<<<-------------------------------------------------------------------------------------")
        reiniciar_direccion()
        with condicion_oeste:
          condicion_oeste.notify_all()
      else:
        reiniciar_direccion()
        with condicion_este:
          condicion_este.notify_all()

def sale_babuino_oeste():
  global babuinos_oeste, babuinos_contador
  with condicion_oeste:
    babuinos_oeste -= 1
    babuinos_contador += 1
    semaforo_cuerda.release()
    print(f"Babuino terminó de cruzar hacia el oeste. Total en cuerda: {MAX_BABUINOS_CUERDA - semaforo_cuerda._value}")

    if (MAX_BABUINOS_CUERDA - semaforo_cuerda._value) == 0 and babuinos_contador < babuinos_total:
      if babuinos_faltan_este > 0:
        print("<<<-------------------------------------------------------------------------------------")
        print(f"Cambiando la dirección de la cuerda hacia el este")
        print(f"Babuinos que faltan cruzar al este: {babuinos_faltan_este}, al oeste: {babuinos_faltan_oeste}")
        print("------------------------------------------------------------------------------------->>>")
        reiniciar_direccion()
        with condicion_este:
          condicion_este.notify_all()
      else:
        reiniciar_direccion()
        with condicion_oeste:
          condicion_oeste.notify_all()

def reiniciar_direccion():
  global babuinos_cruzaron_direccion_actual
  babuinos_cruzaron_direccion_actual = 0

def babuino(direccion):
  if direccion == 'este':
    entra_babuino_este()
  else:
    entra_babuino_oeste()
  time.sleep(TIEMPO_EN_CUERDA)
  if direccion == 'este':
    sale_babuino_este()
  else:
    sale_babuino_oeste()

def iniciar_babuinos(cantidad_babuinos):
  global babuinos_total, max_babuinos_grupo, babuinos_faltan_este, babuinos_faltan_oeste
  babuinos_total = cantidad_babuinos
  max_babuinos_grupo = max(cantidad_babuinos // PROPORCION_GRUPO_BABUINOS, MINIMO_GRUPO_BABUINOS)

  babuinos = []
  direcciones_asignadas = []

  for _ in range(cantidad_babuinos):
    direccion = random.choice(['este', 'oeste'])
    direcciones_asignadas.append(direccion)
    if direccion == 'este':
      babuinos_faltan_este += 1
    else:
      babuinos_faltan_oeste += 1

  print(f"Babuinos que faltan cruzar al este: {babuinos_faltan_este}, al oeste: {babuinos_faltan_oeste}")
  print("----------------------------------------------------------------------------------------")

  for direccion in direcciones_asignadas:
    t = threading.Thread(target=babuino, args=(direccion,))
    babuinos.append(t)
    t.start()

  for t in babuinos:
    t.join()

def main():
  parser = argparse.ArgumentParser(description="Simulación de babuinos cruzando la cuerda.")
  parser.add_argument("cantidad_babuinos", type=int, help="Cantidad total de babuinos")
  args = parser.parse_args()

  print("----------------------------------------------------------------------------------------")
  print("Comienza la simulación")
  print("----------------------------------------------------------------------------------------")
  iniciar_babuinos(args.cantidad_babuinos)
  print("----------------------------------------------------------------------------------------")
  print("Finaliza la simulación")
  print("----------------------------------------------------------------------------------------")

if __name__ == "__main__":
  main()
