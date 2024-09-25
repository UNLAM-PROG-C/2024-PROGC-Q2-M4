import argparse
import os
import time
import threading

VALIDACION_PARAMETROS_OK = 0
ERROR_PARAMETROS = -1
ERROR_ARCHIVO_INVALIDO = -2
ERROR_HILOS = -3

lista_subtotal = []

def validar_parametros():
  parser = argparse.ArgumentParser(description="Contador de caracteres dado un archivo usando múltiples hilos.")
  parser.add_argument("rutaArchivo", type=str, help="Ruta del archivo.")
  parser.add_argument("cantidadDeHilos", type=int, help="Cantidad de hilos para procesar el archivo.")

  args = parser.parse_args()

  if not os.path.isfile(args.rutaArchivo):
    print(f"Error: El archivo '{args.rutaArchivo}' no existe o la ruta es inválida.")
    return None, None, ERROR_ARCHIVO_INVALIDO

  if args.cantidadDeHilos <= 0:
    print("Error: La cantidad de hilos debe ser un número positivo.")
    return None, None, ERROR_PARAMETROS

  return args.rutaArchivo, args.cantidadDeHilos, VALIDACION_PARAMETROS_OK

def eliminar_lineas_vacias(archivo, vector_lineas):
  with open(archivo, 'r') as f:
    for linea in f:
      if linea:
        vector_lineas.append(linea.strip())

def contar_caracteres_en_rango(vectorLineas, indiceSuperior, indiceInferior):
  subtotal = 0
  for i in range(indiceSuperior, indiceInferior + 1):
    subtotal += len(vectorLineas[i])
  lista_subtotal.append(subtotal)

def procesar_archivo(vector_lineas, cantidad_de_hilos):
  cantidad_de_lineas_por_hilo = len(vector_lineas) // cantidad_de_hilos
  threads = []

  for i in range(cantidad_de_hilos):
    indice_inferior = i * cantidad_de_lineas_por_hilo
    indice_superior = ((i + 1) * cantidad_de_lineas_por_hilo) - 1
    if i == cantidad_de_hilos - 1 and len(vector_lineas) % cantidad_de_hilos:
      indice_superior += len(vector_lineas) % cantidad_de_hilos
    thread = threading.Thread(target=contar_caracteres_en_rango, args=(vector_lineas, indice_inferior, indice_superior))
    threads.append(thread)
    thread.start()

  for thread in threads:
    thread.join()

def main():
  pid = os.getpid()
  print(f"PID: {pid}")

  ruta_archivo, cantidad_de_hilos, resultado = validar_parametros()

  if resultado != VALIDACION_PARAMETROS_OK:
    return resultado

  vector_lineas = []
  eliminar_lineas_vacias(ruta_archivo, vector_lineas)

  if len(vector_lineas) < cantidad_de_hilos:
    print("La cantidad de hilos supera la cantidad de lineas no vacias del archivo")
    return ERROR_HILOS

  inicio = time.time()

  procesar_archivo(vector_lineas, cantidad_de_hilos)

  fin = time.time()

  duracion_milisegundos = (fin - inicio) * 1000

  print(f"Tiempo de ejecución: {duracion_milisegundos:.2f} ms")

  print(f"Resultado Total: {sum(lista_subtotal)}")

if __name__ == "__main__":
  main()
