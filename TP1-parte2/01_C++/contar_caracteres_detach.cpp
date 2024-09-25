#include <atomic>
#include <chrono>
#include <condition_variable>
#include <fstream>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>
#include <thread>
#include <unistd.h>
#include <vector>

using namespace chrono;
using namespace std;

int total = 0;
atomic<int> hilos_activos(0);
mutex mtx;
condition_variable cv;

void EliminarLineasVacias(const string& archivo_original, vector<string>& vector_lineas)
{
  ifstream archivo_entrada(archivo_original);
  if (!archivo_entrada.is_open())
  {
    cerr << "Error al abrir el archivo de entrada." << endl;
    return;
  }
  string linea;
  while (getline(archivo_entrada, linea))
  {
    if (!linea.empty())
    {
      vector_lineas.push_back(linea);
    }
  }
  archivo_entrada.close();
}

void ContarCaracteresEnRango(
    const vector<string>& vector_lineas,
    int inicio,
    int fin,
    int& resultado_parcial)
{
  if (inicio < 0)
  {
    inicio = 0;
  }
  if (fin >= vector_lineas.size())
  {
    fin = vector_lineas.size() - 1;
  }
  for (int i = inicio; i <= fin; ++i)
  {
    resultado_parcial += vector_lineas[i].size();
  }

  hilos_activos--;

  cv.notify_one();
  return;
}

void ProcesarArchivo(
    const vector<string>& vector_lineas,
    int cantidad_de_hilos,
    vector<int>& resultados_por_hilo)
{
  int cantidad_lineas_por_archivo = vector_lineas.size() / cantidad_de_hilos;

  for (int i = 0; i < cantidad_de_hilos; i++)
  {
    int indice_inferior = i * cantidad_lineas_por_archivo;
    int indice_superior = ((i + 1) * cantidad_lineas_por_archivo) - 1;

    if (i == cantidad_de_hilos - 1 && (vector_lineas.size() % cantidad_de_hilos != 0))
    {
      indice_superior += (vector_lineas.size() % cantidad_de_hilos);
    }

    hilos_activos++;

    thread(ContarCaracteresEnRango, cref(vector_lineas), indice_inferior,
           indice_superior, ref(resultados_por_hilo[i])).detach();
  }

  unique_lock<mutex> lock(mtx);
  cv.wait(lock, [] { return hilos_activos == 0; });

  cout << "Todos los hilos han terminado.\n";
}

int main(int argc, char* argv[])
{
  cout << "PID: " << getpid() << endl;
  if (argc != 3)
  {
    cerr << "Uso: " << argv[0] << " <archivo> <numero de threads>" << endl;
    return EXIT_FAILURE;
  }

  string nombre_archivo = argv[1];
  int cantidad_de_hilos = stoi(argv[2]);

  int total = 0;
  vector<string> vector_lineas;
  vector<int> resultados_por_hilo(cantidad_de_hilos, 0);
  EliminarLineasVacias(nombre_archivo, vector_lineas);

  if (vector_lineas.size() < cantidad_de_hilos)
  {
    cout << "La cantidad de hilos supera la cantidad de lineas no vacias del archivo" << endl;
    return EXIT_FAILURE;
  }

  auto start = high_resolution_clock::now();

  ProcesarArchivo(cref(vector_lineas), cantidad_de_hilos, ref(resultados_por_hilo));

  for (int resultado_parcial : resultados_por_hilo)
  {
    total += resultado_parcial;
  }

  auto fin = high_resolution_clock::now();
  auto duracion = duration_cast<nanoseconds>(fin - start);

  cout << "Resultado Total: " + to_string(total) << endl;
  cout << "Tiempo de ejecucion: " << (double)duracion.count() / 1000000 << " ms" << endl;

  return EXIT_SUCCESS;
}
