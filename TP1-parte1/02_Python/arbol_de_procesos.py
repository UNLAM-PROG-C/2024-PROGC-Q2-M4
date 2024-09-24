import os
import time
import sys

ERROR_CREACION_PROCESO = 2
TIEMPO_DE_ESPERA_PARA_MOSTRAR_ARBOL = 10

def crear_proceso(nombre):
  pid = os.fork()
  if pid < 0:
    return ERROR_CREACION_PROCESO
  if pid == 0:
    print(f"Proceso {nombre}: {os.getpid()}")
    sys.stdout.flush()
  return pid

def proceso_b():
  pid_d = crear_proceso("D")
  if pid_d == 0:
    proceso_d()
  os.wait()
  os._exit(0)

def proceso_c():
  pid_e = crear_proceso("E")
  if pid_e == 0:
    proceso_e()
  os.wait()
  os._exit(0)

def proceso_d():
  pid_f = crear_proceso("F")
  if pid_f != 0:
    pid_g = crear_proceso("G")
    if pid_g != 0:
      os.wait()
      os.wait()
      os._exit(0)
    else:
      proceso_hoja()
  else:
    proceso_hoja()

def proceso_e():
  pid_h = crear_proceso("H")
  if pid_h != 0:
    pid_i = crear_proceso("I")
    if pid_i != 0:
      os.wait()
      os.wait()
      os._exit(0)
    else:
      proceso_hoja()
  else:
    proceso_hoja()

def proceso_hoja():
  time.sleep(TIEMPO_DE_ESPERA_PARA_MOSTRAR_ARBOL)
  os._exit(0)

def crear_jerarquia_de_procesos():
  pid_b = crear_proceso("B")
  if pid_b != 0:
    print("Proceso A:", os.getpid())
    sys.stdout.flush()
    os.wait()
    os._exit(0)
  else:
    pid_c = crear_proceso("C")
    if pid_c != 0:
      proceso_b()
    else:
      proceso_c()

if __name__ == "__main__":
  crear_jerarquia_de_procesos()